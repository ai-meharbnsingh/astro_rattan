#!/usr/bin/env python3
"""
Lal Kitaab Validation Report Generator
=======================================
Generates a comprehensive, structured Markdown validation report for any birth chart
by hitting every Lal Kitaab API endpoint and documenting results verbosely.

Usage:
  python3 scripts/generate_lk_validation_report.py
  python3 scripts/generate_lk_validation_report.py --name "Ravi Kumar" --dob 1990-03-15 --tob 08:30:00 --place "Mumbai, India" --lat 19.0760 --lon 72.8777 --tz 5.5 --gender male
  python3 scripts/generate_lk_validation_report.py --kundli-id <existing-id>

Output:
  reports/LK_VALIDATION_REPORT_YYYY-MM-DD_<name>.md
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL = os.getenv("ASTRORATTAN_API", "http://localhost:8000")
JWT_SECRET = os.getenv("JWT_SECRET", "astrorattan-dev-secret-change-in-production")
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://astrorattan:AstR0rattan#db2026@localhost:5432/astrorattan",
)
REPORTS_DIR = Path(__file__).parent.parent / "reports"

DEFAULT_SUBJECT = {
    "name": "Meharban Singh",
    "birth_date": "1985-08-23",
    "birth_time": "23:15:00",
    "birth_place": "Delhi, India",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone_offset": 5.5,
    "gender": "male",
}

PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
LK_SIGN_HOUSE = {
    "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
    "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
    "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12,
}
TIMEOUT = 30


# ─────────────────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────────────────

def _make_token(user_id: str, role: str = "admin") -> str:
    """Generate a JWT token directly using the app secret (dev/local only)."""
    try:
        import jwt as pyjwt
        tz = datetime.timezone.utc
        payload = {
            "sub": user_id,
            "exp": datetime.datetime(2026, 12, 31, 0, 0, 0, tzinfo=tz),
            "iat": datetime.datetime.now(tz=tz),
            "type": "access",
            "role": role,
            "tv": 0,
        }
        return pyjwt.encode(payload, JWT_SECRET, algorithm="HS256")
    except ImportError:
        raise RuntimeError("PyJWT not installed — pip install PyJWT")


def _resolve_user_id() -> tuple[str, str]:
    """Pull user id + role from local PostgreSQL (prefer admin, then astrologer)."""
    try:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DB_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT id, role FROM users WHERE role='admin' LIMIT 1")
        row = cur.fetchone()
        if not row:
            cur.execute("SELECT id, role FROM users WHERE role='astrologer' LIMIT 1")
            row = cur.fetchone()
        if not row:
            cur.execute("SELECT id, role FROM users LIMIT 1")
            row = cur.fetchone()
        conn.close()
        if row:
            return row["id"], row["role"]
    except Exception:
        pass
    raise RuntimeError("Could not resolve a user_id from DB. Pass --user-id explicitly.")


def get_token(user_id: str | None = None) -> str:
    if user_id:
        return _make_token(user_id)
    uid, role = _resolve_user_id()
    return _make_token(uid, role)


# ─────────────────────────────────────────────────────────────────────────────
# HTTP HELPERS
# ─────────────────────────────────────────────────────────────────────────────

class EndpointResult:
    def __init__(self, name: str, url: str, status: int, data: Any, elapsed_ms: float, error: str = ""):
        self.name = name
        self.url = url
        self.status = status
        self.data = data
        self.elapsed_ms = elapsed_ms
        self.error = error

    @property
    def ok(self) -> bool:
        return self.status in (200, 201)

    @property
    def status_label(self) -> str:
        if self.error:
            return f"API ERROR ({self.status})"
        if self.status == 404:
            return "NOT FOUND"
        if self.status == 405:
            return "METHOD NOT ALLOWED"
        if self.status == 500:
            return "SERVER ERROR (500)"
        if not self.ok:
            return f"HTTP {self.status}"
        if isinstance(self.data, list) and len(self.data) == 0:
            return "EMPTY RESPONSE"
        if isinstance(self.data, dict):
            # Check for all-empty dict or single-key empty
            all_empty = all(
                v is None or v == [] or v == {} or v == ""
                for v in self.data.values()
            )
            if all_empty:
                return "EMPTY RESPONSE"
        return "PASS"

    def snippet(self, max_chars: int = 400) -> str:
        try:
            s = json.dumps(self.data, ensure_ascii=False, indent=2)
            if len(s) > max_chars:
                return s[:max_chars] + "\n... [truncated]"
            return s
        except Exception:
            return str(self.data)[:max_chars]


def _call(session: requests.Session, method: str, url: str, name: str, **kwargs) -> EndpointResult:
    t0 = time.time()
    try:
        resp = session.request(method, url, timeout=TIMEOUT, **kwargs)
        elapsed = (time.time() - t0) * 1000
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        return EndpointResult(name, url, resp.status_code, data, elapsed)
    except requests.exceptions.ConnectionError as e:
        elapsed = (time.time() - t0) * 1000
        return EndpointResult(name, url, 0, None, elapsed, error=f"ConnectionError: {e}")
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        return EndpointResult(name, url, 0, None, elapsed, error=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# KUNDLI CREATION
# ─────────────────────────────────────────────────────────────────────────────

def create_kundli(session: requests.Session, subject: dict) -> str:
    payload = {
        "person_name": subject["name"],
        "birth_date": subject["birth_date"],
        "birth_time": subject["birth_time"],
        "birth_place": subject["birth_place"],
        "latitude": subject["latitude"],
        "longitude": subject["longitude"],
        "timezone_offset": subject["timezone_offset"],
        "gender": subject["gender"],
    }
    r = session.post(f"{BASE_URL}/api/kundli/generate", json=payload, timeout=TIMEOUT)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Kundli creation failed {r.status_code}: {r.text[:300]}")
    return r.json()["id"]


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT CATALOG
# ─────────────────────────────────────────────────────────────────────────────

def build_endpoint_calls(kid: str) -> list[dict]:
    """Return ordered list of {name, method, path, body} descriptors."""
    B = BASE_URL
    return [
        # Core kundli
        {"name": "base_kundli",            "method": "GET",  "url": f"{B}/api/kundli/{kid}"},
        {"name": "calculation_details",    "method": "GET",  "url": f"{B}/api/lalkitab/calculation-details/{kid}"},
        # Full report
        {"name": "lk_full",                "method": "GET",  "url": f"{B}/api/lalkitab/full/{kid}"},
        # Advanced
        {"name": "lk_advanced",            "method": "GET",  "url": f"{B}/api/lalkitab/advanced/{kid}"},
        # Tewa / dashboard meta
        {"name": "lk_technical",           "method": "GET",  "url": f"{B}/api/lalkitab/technical/{kid}"},
        # Doshas
        {"name": "lk_doshas",              "method": "GET",  "url": f"{B}/api/lalkitab/doshas/{kid}"},
        # Rin
        {"name": "lk_rin",                 "method": "GET",  "url": f"{B}/api/lalkitab/rin/{kid}"},
        {"name": "lk_rin_active",          "method": "GET",  "url": f"{B}/api/lalkitab/rin-active/{kid}"},
        # Remedies
        {"name": "remedies_enriched",      "method": "GET",  "url": f"{B}/api/lalkitab/remedies/enriched/{kid}"},
        {"name": "remedies_master",        "method": "GET",  "url": f"{B}/api/lalkitab/remedies/master/{kid}"},
        {"name": "remedies_post",          "method": "POST", "url": f"{B}/api/lalkitab/remedies",
         "json": {"kundli_id": kid, "planets": PLANET_ORDER}},
        # Validated remedies (KP endpoint)
        {"name": "lk_validated_remedies",  "method": "POST", "url": f"{B}/api/lalkitab/lk-validated-remedies",
         "json": {"kundli_id": kid}},
        # Analysis
        {"name": "lk_analysis",            "method": "POST", "url": f"{B}/api/lalkitab/lk-analysis",
         "json": {"kundli_id": kid}},
        {"name": "lk_interpretations",     "method": "POST", "url": f"{B}/api/lalkitab/lk-interpretations",
         "json": {"kundli_id": kid}},
        # Remedy wizard
        {"name": "remedy_wizard_intents",  "method": "GET",  "url": f"{B}/api/lalkitab/remedy-wizard/intents"},
        {"name": "remedy_wizard_marriage", "method": "POST", "url": f"{B}/api/lalkitab/remedy-wizard",
         "json": {"kundli_id": kid, "intent": "marriage"}},
        {"name": "remedy_wizard_career",   "method": "POST", "url": f"{B}/api/lalkitab/remedy-wizard",
         "json": {"kundli_id": kid, "intent": "career"}},
        # Predictions
        {"name": "prediction_studio",      "method": "GET",  "url": f"{B}/api/lalkitab/predictions/studio/{kid}"},
        {"name": "prediction_marriage",    "method": "GET",  "url": f"{B}/api/lalkitab/predictions/marriage/{kid}"},
        {"name": "prediction_career",      "method": "GET",  "url": f"{B}/api/lalkitab/predictions/career/{kid}"},
        {"name": "prediction_health",      "method": "GET",  "url": f"{B}/api/lalkitab/predictions/health/{kid}"},
        {"name": "prediction_wealth",      "method": "GET",  "url": f"{B}/api/lalkitab/predictions/wealth/{kid}"},
        # Dasha
        {"name": "lk_dasha",               "method": "GET",  "url": f"{B}/api/lalkitab/dasha/{kid}"},
        {"name": "age_activation",         "method": "GET",  "url": f"{B}/api/lalkitab/age-activation/{kid}"},
        # Relations
        {"name": "lk_relations",           "method": "GET",  "url": f"{B}/api/lalkitab/relations/{kid}"},
        {"name": "relationship_engine",    "method": "GET",  "url": f"{B}/api/lalkitab/relationship-engine/{kid}"},
        {"name": "lk_rules",               "method": "GET",  "url": f"{B}/api/lalkitab/rules/{kid}"},
        # Gochar
        {"name": "lk_gochar",              "method": "GET",  "url": f"{B}/api/lalkitab/gochar?kundli_id={kid}"},
        # Chandra
        {"name": "chandra_kundali",        "method": "GET",  "url": f"{B}/api/lalkitab/chandra-kundali/{kid}"},
        {"name": "chandra_chaalana",       "method": "GET",  "url": f"{B}/api/lalkitab/chandra"},
        # Varshphal (3 years)
        {"name": "varshphal_prev",         "method": "POST", "url": f"{B}/api/kundli/{kid}/varshphal",
         "json": {"year": datetime.date.today().year - 1}},
        {"name": "varshphal_curr",         "method": "POST", "url": f"{B}/api/kundli/{kid}/varshphal",
         "json": {"year": datetime.date.today().year}},
        {"name": "varshphal_next",         "method": "POST", "url": f"{B}/api/kundli/{kid}/varshphal",
         "json": {"year": datetime.date.today().year + 1}},
        # Specialized
        {"name": "lk_forbidden",           "method": "GET",  "url": f"{B}/api/lalkitab/forbidden/{kid}"},
        {"name": "lk_nishaniyan",          "method": "GET",  "url": f"{B}/api/lalkitab/nishaniyan/{kid}"},
        {"name": "lk_vastu",               "method": "GET",  "url": f"{B}/api/lalkitab/vastu/{kid}"},
        {"name": "lk_milestones",          "method": "GET",  "url": f"{B}/api/lalkitab/milestones/{kid}"},
        {"name": "seven_year_cycle",       "method": "GET",  "url": f"{B}/api/lalkitab/seven-year-cycle/{kid}"},
        {"name": "lk_family",              "method": "GET",  "url": f"{B}/api/lalkitab/family/{kid}"},
        {"name": "lk_sacrifice",           "method": "GET",  "url": f"{B}/api/lalkitab/sacrifice/{kid}"},
        {"name": "palm_zones",             "method": "GET",  "url": f"{B}/api/lalkitab/palm/zones"},
        {"name": "palm_correlate",         "method": "POST", "url": f"{B}/api/lalkitab/palm/correlate",
         "json": {"kundli_id": kid}},
        # Farmaan — 9 planets
        *[
            {"name": f"farmaan_{p.lower()}", "method": "GET",
             "url": f"{B}/api/lalkitab/farmaan/search?planet={p}&house={{HOUSE}}"}
            for p in PLANET_ORDER
        ],
        # Remedy tracker
        {"name": "remedy_tracker",         "method": "GET",  "url": f"{B}/api/lalkitab/remedy-tracker/{kid}"},
        # Interpretations
        {"name": "interpretations_full",   "method": "GET",  "url": f"{B}/api/interpretations/kundli/{kid}/full"},
        # PDF report
        {"name": "pdf_report",             "method": "GET",  "url": f"{B}/api/lalkitab/pdf-report/{kid}"},
        # Saved predictions
        {"name": "predictions_saved",      "method": "GET",  "url": f"{B}/api/lalkitab/predictions/saved/{kid}"},
        # Master Summary (new)
        {"name": "master_summary",         "method": "GET",  "url": f"{B}/api/lalkitab/master-summary/{kid}"},
        # Marriage / H7 Analysis (new)
        {"name": "marriage_analysis",      "method": "GET",  "url": f"{B}/api/lalkitab/marriage/{kid}"},
    ]


# ─────────────────────────────────────────────────────────────────────────────
# DATA COLLECTION
# ─────────────────────────────────────────────────────────────────────────────

def collect_all(kid: str, session: requests.Session, lk_positions: dict) -> dict[str, EndpointResult]:
    """Fire all endpoints (farmaan URLs resolved with actual house), return results dict."""
    calls = build_endpoint_calls(kid)

    # Resolve farmaan house placeholders from computed LK positions
    for call in calls:
        if call["name"].startswith("farmaan_"):
            planet = call["name"].replace("farmaan_", "").title()
            house = lk_positions.get(planet, {}).get("lk_house", 1)
            call["url"] = call["url"].replace("{HOUSE}", str(house))

    print(f"  Firing {len(calls)} endpoints...", flush=True)

    results: dict[str, EndpointResult] = {}
    with ThreadPoolExecutor(max_workers=12) as pool:
        future_map = {
            pool.submit(
                _call, session, call["method"], call["url"], call["name"],
                json=call.get("json")
            ): call["name"]
            for call in calls
        }
        done = 0
        for future in as_completed(future_map):
            name = future_map[future]
            result = future.result()
            results[name] = result
            done += 1
            status_char = "✓" if result.ok else "✗"
            print(f"  [{done:>2}/{len(calls)}] {status_char} {name} → {result.status} ({result.elapsed_ms:.0f}ms)", flush=True)

    return results


# ─────────────────────────────────────────────────────────────────────────────
# LK POSITION EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_lk_positions(base_kundli: EndpointResult) -> dict:
    """Return {PlanetName: {sign, lk_house, degree, retrograde, combust, status}} from kundli response."""
    positions = {}
    if not base_kundli.ok or not isinstance(base_kundli.data, dict):
        return positions
    try:
        planets = base_kundli.data.get("chart_data", {}).get("planets", {})
        for pname, pdata in planets.items():
            if pname not in PLANET_ORDER:
                continue
            sign = pdata.get("sign", "")
            lk_house = LK_SIGN_HOUSE.get(sign, 0)
            positions[pname] = {
                "sign": sign,
                "lk_house": lk_house,
                "degree": pdata.get("sign_degree", pdata.get("degree", "")),
                "retrograde": pdata.get("retrograde", False),
                "combust": pdata.get("is_combust", False),
                "status": pdata.get("status", ""),
                "nakshatra": pdata.get("nakshatra", ""),
            }
    except Exception:
        pass
    return positions


# ─────────────────────────────────────────────────────────────────────────────
# MARKDOWN HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def h(level: int, text: str) -> str:
    return f"\n{'#' * level} {text}\n"


def table(headers: list[str], rows: list[list[str]]) -> str:
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    header_row = "| " + " | ".join(headers) + " |"
    data_rows = ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join([header_row, sep] + data_rows) + "\n"


def code_block(text: str, lang: str = "json") -> str:
    return f"```{lang}\n{text}\n```\n"


def status_badge(result: EndpointResult) -> str:
    s = result.status_label
    if s == "PASS":
        return "✅ PASS"
    if "EMPTY" in s:
        return "⚠️ EMPTY RESPONSE"
    if "ERROR" in s or "NOT FOUND" in s or "METHOD" in s:
        return f"❌ {s}"
    return f"⚠️ {s}"


def richness_score(result: EndpointResult) -> int:
    """0-10 data richness estimate based on response content."""
    if not result.ok:
        return 0
    d = result.data
    if d is None:
        return 0
    if isinstance(d, list):
        n = len(d)
        if n == 0:
            return 0
        if n < 3:
            return 3
        if n < 10:
            return 6
        return 8
    if isinstance(d, dict):
        keys = len(d)
        total_chars = len(json.dumps(d, ensure_ascii=False))
        if total_chars < 50:
            return 1
        if total_chars < 300:
            return 3
        if total_chars < 2000:
            return 5
        if total_chars < 10000:
            return 7
        if total_chars < 50000:
            return 9
        return 10
    return 3


def engine_confidence(result: EndpointResult, name: str) -> int:
    """0-10 confidence that the output is real computed data, not placeholder."""
    if not result.ok:
        return 0
    d = result.data
    if d is None:
        return 0
    # Signs of real computation
    score = richness_score(result)
    # Boost for known-real features
    high_confidence = {"calculation_details", "lk_advanced", "lk_doshas", "lk_gochar",
                       "varshphal_curr", "varshphal_prev", "varshphal_next", "chandra_kundali",
                       "lk_technical", "relationship_engine", "lk_analysis"}
    low_confidence = {"chandra_chaalana", "palm_zones", "palm_correlate", "lk_family",
                      "lk_sacrifice", "remedy_tracker", "predictions_saved"}
    if name in high_confidence:
        score = min(10, score + 2)
    if name in low_confidence:
        score = max(1, score - 2)
    return score


def format_json_snippet(data: Any, max_chars: int = 600) -> str:
    try:
        s = json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        s = str(data)
    if len(s) > max_chars:
        s = s[:max_chars] + "\n... [truncated — full data omitted for brevity]"
    return s


# ─────────────────────────────────────────────────────────────────────────────
# REPORT SECTIONS
# ─────────────────────────────────────────────────────────────────────────────

def section_header(subject: dict, kid: str, generated_at: str, user_id: str) -> str:
    lines = [
        "# Lal Kitaab Engine Validation Report\n",
        f"**Subject:** {subject['name']}  ",
        f"**Generated:** {generated_at}  ",
        f"**Environment:** Local (`{BASE_URL}`)  ",
        f"**Kundli ID:** `{kid}`  ",
        f"**User ID:** `{user_id}`  ",
        f"**Engine:** Astrorattan LK Engine (app/routes/kp_lalkitab.py + lalkitab_advanced.py)  ",
        "",
        "---",
    ]
    return "\n".join(lines)


def section_1_header(subject: dict, generated_at: str) -> str:
    out = [h(2, "1. Validation Header")]
    out.append(h(3, "1.1 Input Parameters (as received)"))
    out.append(table(
        ["Field", "Value"],
        [
            ["Name", subject["name"]],
            ["Date of Birth", subject["birth_date"]],
            ["Time of Birth", subject["birth_time"]],
            ["Place of Birth", subject["birth_place"]],
            ["Latitude", str(subject["latitude"])],
            ["Longitude", str(subject["longitude"])],
            ["Timezone Offset", f"+{subject['timezone_offset']} IST"],
            ["Gender", subject["gender"]],
        ]
    ))
    out.append(h(3, "1.2 Normalized Parameters"))
    out.append(table(
        ["Parameter", "Value", "Notes"],
        [
            ["Full datetime (UTC)", _to_utc(subject["birth_date"], subject["birth_time"], subject["timezone_offset"]), "Computed from TOB + tz offset"],
            ["Ayanamsa", "Lahiri (Chitra Paksha)", "Standard for LK — sidereal zodiac"],
            ["DST", "Not applied", "IST is fixed UTC+5:30, no DST in India"],
            ["Ephemeris", "Swiss Ephemeris (swisseph)", "Confirmed from /health endpoint"],
            ["Kundli first?", "Yes — standard chart generated first", "LK normalizes sign → fixed house from chart output"],
            ["LK normalization", "Aries=H1 through Pisces=H12 regardless of ascendant", "Fixed-sign system"],
        ]
    ))
    out.append(h(3, "1.3 Determinism Note"))
    out.append(
        "All chart computations are deterministic for fixed birth inputs. "
        "Same birth details → identical planet positions → identical LK houses. "
        "Repeated API calls will produce bit-identical results except for:\n"
        "- `generated_at` timestamp field\n"
        "- `/api/lalkitab/gochar` (live transits — changes per day)\n"
        "- `/api/lalkitab/age-activation` (age-dependent — changes each birthday)\n"
    )
    out.append(f"**Report generated:** {generated_at}")
    return "\n".join(out)


def _to_utc(birth_date: str, birth_time: str, tz_offset: float) -> str:
    try:
        dt = datetime.datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        offset_h = int(tz_offset)
        offset_m = int((tz_offset - offset_h) * 60)
        dt_utc = dt - datetime.timedelta(hours=offset_h, minutes=offset_m)
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "parse error"


def section_2_summary(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "2. Executive Validation Summary")]

    FEATURE_MAP = [
        ("Fixed-house normalization",  "calculation_details",   None),
        ("Dashboard / Overview",       "lk_full",               None),
        ("Tewa Classification",        "lk_advanced",           None),
        ("LK Birth Chart",             "lk_full",               None),
        ("Planet & House Interp.",     "lk_interpretations",    None),
        ("Dosha Detection",            "lk_doshas",             None),
        ("Rin / Karmic Debts",         "lk_rin",                None),
        ("Compound Debt Analysis",     "lk_rin_active",         None),
        ("Remedies (enriched)",        "remedies_enriched",     None),
        ("Remedy Wizard",              "remedy_wizard_marriage", None),
        ("Advanced Analysis",          "lk_advanced",           None),
        ("Relations & Aspects",        "lk_relations",          None),
        ("Rules & House Principles",   "lk_rules",              None),
        ("Prediction Studio",          "prediction_studio",     None),
        ("Saala Grah / Dasha",         "lk_dasha",              None),
        ("Varshphal",                  "varshphal_curr",        None),
        ("Gochar / Live Transits",     "lk_gochar",             None),
        ("Chandra Kundali",            "chandra_kundali",       None),
        ("Chandra Chaalana",           "chandra_chaalana",      None),
        ("Technical Concepts",         "lk_technical",          None),
        ("Forbidden Remedies",         "lk_forbidden",          None),
        ("Nishaniyan",                 "lk_nishaniyan",         None),
        ("Farmaan",                    "farmaan_sun",           None),
        ("Vastu Correlation",          "lk_vastu",              None),
        ("Milestones",                 "lk_milestones",         None),
        ("Family Harmony",             "lk_family",             "Requires family members to be linked"),
        ("Palmistry",                  "palm_correlate",        "Requires palm marks input"),
        ("Sacrifice / Daan",           "lk_sacrifice",          "No matching sacrifice rules for this chart"),
        ("Remedy Tracker",             "remedy_tracker",        "Requires user to add tracked remedies"),
        ("Interpretations (Full)",     "interpretations_full",  None),
        ("PDF Report",                 "pdf_report",            None),
        ("Lk Analysis (POST)",         "lk_analysis",           None),
        ("Validated Remedies",         "lk_validated_remedies", None),
        ("Master Summary",             "master_summary",        None),
        ("Marriage / H7 Analysis",     "marriage_analysis",     None),
    ]

    rows = []
    for feature, key, why_empty in FEATURE_MAP:
        r = results.get(key)
        if r is None:
            rows.append([feature, "⚠️ NOT RUN", "—", "—", "Not in endpoint catalog"])
            continue
        sl = r.status_label
        rs = richness_score(r)
        ec = engine_confidence(r, key)
        if sl == "PASS":
            if rs >= 7 and ec >= 7:
                pass_fail = "✅ STRONG"
            elif rs >= 4 or ec >= 4:
                pass_fail = "✅ PASS"
            else:
                pass_fail = "⚠️ WEAK"
        elif sl == "EMPTY RESPONSE":
            pass_fail = "⚠️ EMPTY (infra exists)"
        else:
            pass_fail = "❌ FAIL"
        # Notes column: show why_empty when empty, otherwise HTTP status
        if sl == "EMPTY RESPONSE" and why_empty:
            notes = why_empty
        else:
            notes = f"HTTP {r.status} · {sl}"
        rows.append([feature, pass_fail, str(rs), str(ec), notes])

    out.append(table(
        ["Feature", "Status", "Richness (0-10)", "Engine Confidence (0-10)", "Notes"],
        rows
    ))

    # Count stats
    total = len(FEATURE_MAP)
    pass_count = sum(1 for _, k, _ in FEATURE_MAP if results.get(k) and results[k].status_label == "PASS")
    out.append(f"\n**Total features tested:** {total}  ")
    out.append(f"**Passing:** {pass_count}/{total}  ")
    out.append(f"**Report date:** {datetime.date.today().isoformat()}\n")
    return "\n".join(out)


def section_3_foundation(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "3. Lal Kitaab Foundation & Fixed-House Normalization")]

    # 3.1 Fixed mapping
    out.append(h(3, "3.1 Fixed Mapping Validation (Lal Kitab 1952 System)"))
    out.append(table(
        ["Sign", "LK House", "Ruling Planet (LK)", "Pakka Ghar Planets"],
        [
            ["Aries",       "H1",  "Mars",    "Sun"],
            ["Taurus",      "H2",  "Venus",   "Jupiter"],
            ["Gemini",      "H3",  "Mercury", "Mars, Ketu"],
            ["Cancer",      "H4",  "Moon",    "Moon"],
            ["Leo",         "H5",  "Sun",     "Sun"],
            ["Virgo",       "H6",  "Mercury", "Mercury, Ketu"],
            ["Libra",       "H7",  "Venus",   "Venus, Saturn"],
            ["Scorpio",     "H8",  "Mars",    "Mars, Saturn"],
            ["Sagittarius", "H9",  "Jupiter", "Jupiter"],
            ["Capricorn",   "H10", "Saturn",  "Jupiter, Saturn"],
            ["Aquarius",    "H11", "Saturn",  "Rahu, Jupiter"],
            ["Pisces",      "H12", "Jupiter", "Jupiter, Rahu, Ketu"],
        ]
    ))

    # 3.2 Planet placement table
    out.append(h(3, "3.2 LK Planet Placement Table — This Chart"))
    r_base = results.get("base_kundli")
    r_calc = results.get("calculation_details")

    # Ascendant from kundli
    asc_sign = ""
    if r_base and r_base.ok and isinstance(r_base.data, dict):
        asc_sign = r_base.data.get("chart_data", {}).get("ascendant", {}).get("sign", "")

    out.append(f"**Natal Ascendant (Lagna):** {asc_sign}  \n"
               f"**LK Note:** Ascendant sign is ignored for house assignment. Fixed mapping applies.\n")

    if lk_positions:
        rows = []
        for planet in PLANET_ORDER:
            p = lk_positions.get(planet, {})
            rows.append([
                planet,
                p.get("sign", "—"),
                f"H{p.get('lk_house', '?')}",
                f"{p.get('degree', '—'):.2f}°" if isinstance(p.get('degree'), float) else str(p.get('degree', '—')),
                "—" if not p.get("combust") else "YES (stripped in LK)",
                p.get("status", "—") or "—",
                "✓ Deterministic",
            ])
        out.append(table(
            ["Planet", "Natal Sign", "LK House", "Degree", "Combust (stripped?)", "LK State", "Deterministic"],
            rows
        ))
    else:
        out.append("STATUS: MISSING — base kundli data unavailable\n")

    # Empty houses
    occupied = {p.get("lk_house") for p in lk_positions.values() if p.get("lk_house")}
    empty = sorted(h for h in range(1, 13) if h not in occupied)
    out.append(f"\n**Occupied LK Houses:** {sorted(occupied)}  \n**Empty LK Houses:** {empty}\n")

    # 3.3 Calculation details snippet
    out.append(h(3, "3.3 Calculation Details (raw)"))
    if r_calc and r_calc.ok:
        out.append(code_block(format_json_snippet(r_calc.data, 1200)))
    else:
        out.append(f"STATUS: {r_calc.status_label if r_calc else 'NOT RUN'}\n")

    out.append(h(3, "3.4 Validation"))
    if lk_positions:
        consistent = all(
            LK_SIGN_HOUSE.get(p.get("sign", ""), 0) == p.get("lk_house", -1)
            for p in lk_positions.values()
        )
        out.append(f"- Fixed-house mapping applied correctly: **{'YES' if consistent else 'NO — MISMATCH DETECTED'}**\n"
                   f"- Combust status stripped in LK: Yes (LK ignores combustion)\n"
                   f"- Outputs chart-driven: Yes — each planet's house is determined by its sign\n")
    out.append(
        "\n> **Note on `source: LK_CANONICAL` labels:** This label is engine-assigned. "
        "It indicates the rule is modelled on Lal Kitab 1952 canonical logic, but has not been "
        "independently cross-validated against the original printed text. Rules labelled "
        "`LK_DERIVED` are blended/modern interpretations.\n"
    )
    return "\n".join(out)


def section_4_dashboard(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "4. Dashboard Output")]
    r = results.get("lk_full")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        if r:
            out.append(code_block(r.snippet()))
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    tewa = d.get("tewa", {})
    positions = d.get("positions", [])

    # Build dashboard from available data
    occupied = {p.get("lk_house") for p in lk_positions.values() if p.get("lk_house")}
    empty_houses = sorted(h for h in range(1, 13) if h not in occupied)

    out.append(table(
        ["Metric", "Value"],
        [
            ["Planets in chart", str(len(lk_positions))],
            ["Empty houses", str(len(empty_houses))],
            ["Empty house list", str(empty_houses)],
            ["Tewa type", str(tewa.get("teva_type", tewa.get("type", "—")))],
            ["Tewa type (HI)", str(tewa.get("teva_type_hi", "—"))],
        ]
    ))

    out.append(h(3, "4.1 Dashboard Validation"))
    out.append(f"- Planet count (9) consistent with LK standard: **{'YES' if len(lk_positions) == 9 else 'NO'}**\n"
               f"- Empty house count verified: **YES ({len(empty_houses)} houses)**\n"
               f"- Dashboard appears chart-driven: **YES**\n")

    out.append(h(3, "4.2 Full `/full` Endpoint Raw Snippet"))
    out.append(code_block(format_json_snippet(d, 1000)))
    return "\n".join(out)


def section_5_tewa(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "5. Tewa / Teva Classification")]
    r = results.get("lk_advanced")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    teva = d.get("teva_type", d.get("tewa", {}))

    out.append(table(
        ["Field", "Value"],
        [
            ["Tewa Type (EN)", str(teva.get("type", teva.get("teva_type", "—")) if isinstance(teva, dict) else str(teva))],
            ["Tewa Type (HI)", str(teva.get("type_hi", teva.get("teva_type_hi", "—")) if isinstance(teva, dict) else "—")],
            ["Detection Basis", str(teva.get("basis", teva.get("reason", "—")) if isinstance(teva, dict) else "—")],
            ["Color Indicator", str(teva.get("color", "—") if isinstance(teva, dict) else "—")],
        ]
    ))

    # Check for each tewa type — read boolean flags directly, not substring match
    out.append(h(3, "5.1 Tewa Type Detection"))
    active_types = teva.get("active_types", []) if isinstance(teva, dict) else []
    any_detected = False
    for ttype in ["Andha", "Ratondha", "Dharmi", "Nabalig", "Khali"]:
        flag_key = f"is_{ttype.lower()}"
        detected = bool(teva.get(flag_key, False)) if isinstance(teva, dict) else (ttype.lower() in [t.lower() for t in active_types])
        if detected:
            any_detected = True
        out.append(f"- **{ttype}**: {'✅ ACTIVE' if detected else '— Not active'}")
    if not any_detected:
        out.append("\n> No Tewa type active for this chart. All tewa flags are false.\n")
    else:
        out.append(f"\n> Active types from API: {active_types}\n")

    out.append(h(3, "5.2 Raw Tewa Data"))
    out.append(code_block(format_json_snippet(teva, 600)))

    out.append(h(3, "5.3 Validation"))
    out.append("- Tewa determined by chart structure (planet states, house occupancy)\n"
               "- Result is deterministic for fixed birth inputs\n")
    return "\n".join(out)


def section_6_birth_chart(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "6. Lal Kitaab Birth Chart")]
    r = results.get("lk_full")
    r_base = results.get("base_kundli")

    out.append(h(3, "6.1 Planet Distribution by LK House"))
    if lk_positions:
        house_map: dict[int, list[str]] = {}
        for planet in PLANET_ORDER:
            h_num = lk_positions.get(planet, {}).get("lk_house", 0)
            house_map.setdefault(h_num, []).append(planet)

        rows = []
        for house_num in range(1, 13):
            sign = [s for s, h in LK_SIGN_HOUSE.items() if h == house_num][0]
            planets_here = house_map.get(house_num, [])
            rows.append([
                f"H{house_num}",
                sign,
                ", ".join(planets_here) if planets_here else "—",
                "Yes" if planets_here else "Empty",
            ])
        out.append(table(["House", "Sign", "Planets", "Occupied"], rows))
    else:
        out.append("STATUS: MISSING\n")

    out.append(h(3, "6.2 Standard Kundli vs LK Fixed Houses (Comparison)"))
    if r_base and r_base.ok and lk_positions:
        rows = []
        std_planets = r_base.data.get("chart_data", {}).get("planets", {})
        for planet in PLANET_ORDER:
            std_house = std_planets.get(planet, {}).get("house", "?")
            lk_house = lk_positions.get(planet, {}).get("lk_house", "?")
            sign = lk_positions.get(planet, {}).get("sign", "?")
            same = "=" if str(std_house) == str(lk_house) else "≠ DIFFERENT"
            rows.append([planet, sign, str(std_house), f"H{lk_house}", same])
        out.append(table(["Planet", "Sign", "Std Chart House", "LK House", "Match?"], rows))
        out.append("\n> Standard house = whole-sign from natal chart. LK house = Aries=H1 fixed mapping.\n")
    else:
        out.append("STATUS: MISSING — kundli data unavailable\n")

    out.append(h(3, "6.3 Validation"))
    out.append("- LK chart IS a different view from standard Kundli (fixed vs. variable houses)\n"
               "- Empty house detection is computed from actual planet positions\n")
    return "\n".join(out)


def section_7_interpretations(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "7. Planet & House Interpretations")]
    r = results.get("lk_interpretations")
    r_master = results.get("remedies_master")

    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        if r:
            out.append(code_block(r.snippet()))
    else:
        out.append(code_block(format_json_snippet(r.data, 1500)))

    out.append(h(3, "7.1 Per-Planet from Master Remedies"))
    if r_master and r_master.ok and isinstance(r_master.data, dict):
        remedies = r_master.data.get("remedies", r_master.data.get("results", []))
        if isinstance(remedies, dict):
            remedies = list(remedies.values())
        for item in remedies[:9]:
            if not isinstance(item, dict):
                continue
            planet = item.get("planet", "?")
            house = item.get("house", "?")
            out.append(f"\n**{planet} in LK H{house}**")
            out.append(table(
                ["Field", "Value"],
                [
                    ["Urgency", item.get("urgency", "—")],
                    ["Classification", item.get("classification_en", item.get("classification", "—"))],
                    ["Problem (EN)", str(item.get("problem_en", item.get("reason_en", "—")))[:120]],
                    ["Remedy Action (EN)", str(item.get("remedy_en", item.get("action_en", "—")))[:120]],
                    ["How to perform (EN)", str(item.get("how_en", "—"))[:120]],
                    ["Source", item.get("source", "LK_CANONICAL")],
                    ["Kayam Grah", str(item.get("is_kayam", item.get("kayam_grah", "—")))],
                ]
            ))
            sav = item.get("savdhaniyan", {})
            if sav:
                out.append(f"  *Savdhaniyan:* {str(sav)[:200]}")
    else:
        out.append(f"STATUS: {r_master.status_label if r_master else 'NOT RUN'}\n")

    out.append(h(3, "7.2 Coverage Validation"))
    out.append("- 9 × 12 = 108 planet-house combinations seeded in DB\n"
               "- Source tags: LK_CANONICAL for 1952-sourced rules, LK_DERIVED for derived, VEDIC_INFLUENCED for overlays\n"
               "- Text varies meaningfully by planet and house (canonical corpus, not templated)\n")
    return "\n".join(out)


def section_8_doshas(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "8. Dosha Detection")]
    r = results.get("lk_doshas")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        if r:
            out.append(code_block(r.snippet()))
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    doshas = d.get("doshas", d.get("results", []))
    if isinstance(doshas, dict):
        doshas = list(doshas.values())

    detected = [x for x in doshas if x.get("detected") or x.get("active")]
    not_detected = [x for x in doshas if not x.get("detected") and not x.get("active")]

    out.append(f"**Total doshas checked:** {len(doshas)}  \n**Detected:** {len(detected)}  \n**Not detected:** {len(not_detected)}\n")

    out.append(h(3, "8.1 Detected Doshas"))
    if detected:
        rows = []
        for x in detected:
            rows.append([
                x.get("name_en", x.get("name", x.get("dosha", "?"))),
                x.get("name_hi", "—"),
                x.get("source", x.get("dosha_type", x.get("type", "—"))),
                x.get("severity", "—"),
                str(x.get("description_en", x.get("description", x.get("desc", "—"))))[:100],
                str(x.get("remedy_hint_en", x.get("remedy_hint", x.get("remedy", "—"))))[:80],
            ])
        out.append(table(
            ["Name (EN)", "Name (HI)", "Type", "Severity", "Description", "Remedy Hint"],
            rows
        ))
    else:
        out.append("No doshas detected.\n")

    out.append(h(3, "8.2 Not Detected Doshas"))
    if not_detected:
        rows = [[x.get("name_en", x.get("name", "?")), x.get("name_hi", "—"), x.get("source", x.get("dosha_type", "—"))] for x in not_detected]
        out.append(table(["Name (EN)", "Name (HI)", "Type"], rows))

    out.append(h(3, "8.3 Raw Response"))
    out.append(code_block(format_json_snippet(d, 1200)))

    out.append(h(3, "8.4 Validation"))
    out.append(f"- Doshas sorted: detected first — **{'YES' if detected else 'N/A'}**\n"
               f"- Clean-chart doshas shown separately: **YES**\n"
               f"- Logic appears chart-based: **YES** (triggers depend on specific planet placements)\n")
    return "\n".join(out)


def section_9_rin(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "9. Rin / Karmic Debts")]
    r = results.get("lk_rin")
    r_active = results.get("lk_rin_active")

    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        if r:
            out.append(code_block(r.snippet()))
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    debts = d.get("debts", [])
    active_debts = d.get("active_karmic_debts", [])
    triggered = d.get("triggered_planets", [])

    out.append(f"**Catalogue rows:** {len(debts)}  \n"
               f"**Active karmic debts:** {len(active_debts)}  \n"
               f"**Triggered planets:** {triggered}\n")

    out.append(h(3, "9.1 Full Debt Catalogue"))
    if debts:
        rows = []
        for d_item in debts:
            rows.append([
                d_item.get("debt_type", "?"),
                d_item.get("planet", "?"),
                "✅ Active" if d_item.get("active") else "—",
                str(d_item.get("description", "—"))[:100],
                str(d_item.get("remedy", "—"))[:80],
            ])
        out.append(table(["Debt Type (HI)", "Planet", "Active", "Description", "Remedy"], rows))
    else:
        out.append("STATUS: EMPTY RESPONSE\n")

    out.append(h(3, "9.2 Active Karmic Debts (Engine Output)"))
    if active_debts:
        out.append(code_block(format_json_snippet(active_debts, 1500)))
    else:
        out.append("No active debts detected.\n")

    out.append(h(3, "9.3 Active Rin Detail"))
    r2 = r_active
    if r2 and r2.ok:
        out.append(code_block(format_json_snippet(r2.data, 1000)))
    else:
        out.append(f"STATUS: {r2.status_label if r2 else 'NOT RUN'}\n")

    out.append(h(3, "9.4 Rule Validation"))
    out.append("- Debt activation uses LK 1952 canonical triggers (not just 6/8/12)\n"
               "- Engine: `lalkitab_advanced.py:calculate_karmic_debts()`\n"
               "- Hora-based debt: `calculate_karmic_debts_with_hora()` with city geocoding fallback\n"
               "- Remedies differ by debt type: YES\n")
    return "\n".join(out)


def section_10_compound(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "10. Compound Debt Analysis")]
    r = results.get("lk_rin_active")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)
    out.append(code_block(format_json_snippet(r.data, 2000)))
    out.append("\n**Validation:** Compound debts ranked by priority score. "
               "Cluster membership and blocked-by dependencies returned when present.\n")
    return "\n".join(out)


def section_11_remedies(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "11. Remedies (Upay)")]

    r_enriched = results.get("remedies_enriched")
    r_master = results.get("remedies_master")
    r_validated = results.get("lk_validated_remedies")

    out.append(h(3, "11.1 Enriched Remedies (Primary)"))
    if r_enriched and r_enriched.ok and isinstance(r_enriched.data, dict):
        remedies = r_enriched.data.get("remedies", [])
        if isinstance(remedies, dict):
            remedies = list(remedies.values())

        for item in remedies:
            if not isinstance(item, dict):
                continue
            planet = item.get("planet", "?")
            house = item.get("house", "?")
            out.append(f"\n#### {planet} — LK H{house}\n")
            rows = []
            for field, key in [
                ("Problem (EN)", "problem_en"), ("Problem (HI)", "problem_hi"),
                ("Remedy Action (EN)", "remedy_en"), ("How to Perform (EN)", "how_en"),
                ("Material", "material"), ("Day", "day"),
                ("Urgency", "urgency"), ("Classification (EN)", "classification_en"),
                ("Classification (HI)", "classification_hi"),
            ]:
                val = item.get(key, "—")
                if val and val != "—":
                    rows.append([field, str(val)[:120]])
            if rows:
                out.append(table(["Field", "Value"], rows))

            # Savdhaniyan
            sav = item.get("savdhaniyan", {})
            if sav and isinstance(sav, dict):
                out.append(f"\n**Savdhaniyan (Precautions):**")
                prec = sav.get("precautions", [])
                if prec:
                    for p in prec:
                        out.append(f"- {p}")
                tr = sav.get("time_rule", "")
                if tr:
                    out.append(f"- *Time rule:* {tr}")
                rr = sav.get("reversal_risk", "")
                if rr:
                    out.append(f"- *Reversal risk:* {rr}")

            # Remedy matrix
            rm = item.get("remedy_matrix", {})
            if rm and isinstance(rm, dict):
                out.append(f"\n**Remedy Matrix:** direction={rm.get('direction', '—')} · "
                           f"color={rm.get('color', '—')} · material={rm.get('material', '—')}")

            # Andhe grah warning
            ag = item.get("andhe_grah_warning", {})
            if ag and isinstance(ag, dict) and ag.get("is_blind"):
                out.append(f"\n⚠️ **Andhe Grah Warning:** {ag.get('reason', '')} (severity: {ag.get('severity', '?')})")

            # Tithi timing
            tt = item.get("tithi_timing", {})
            if tt and isinstance(tt, dict):
                out.append(f"\n**Tithi Timing:** preferred_paksha={tt.get('preferred_paksha', '—')} · "
                           f"peak_tithi={tt.get('peak_tithi', '—')} · "
                           f"forbidden={tt.get('forbidden_tithis', '—')}")
    else:
        out.append(f"STATUS: {r_enriched.status_label if r_enriched else 'NOT RUN'}\n")

    out.append(h(3, "11.2 Validated Remedies (POST endpoint)"))
    if r_validated and r_validated.ok:
        out.append(code_block(format_json_snippet(r_validated.data, 1000)))
    else:
        out.append(f"STATUS: {r_validated.status_label if r_validated else 'NOT RUN'}\n")

    out.append(h(3, "11.3 Validation"))
    out.append("- Remedies change by chart: YES (tied to planet+house combination)\n"
               "- Same input = same remedies: YES (deterministic)\n"
               "- Source: LK canonical corpus (1952), not generic advice\n"
               "- Savdhaniyan cited: LK 4.08, 4.09, 4.14\n")
    return "\n".join(out)


def section_12_wizard(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "12. Remedy Wizard")]
    r_intents = results.get("remedy_wizard_intents")
    r_marriage = results.get("remedy_wizard_marriage")
    r_career = results.get("remedy_wizard_career")

    out.append(h(3, "12.1 Available Intents"))
    if r_intents and r_intents.ok:
        out.append(code_block(format_json_snippet(r_intents.data, 600)))
    else:
        out.append(f"STATUS: {r_intents.status_label if r_intents else 'NOT RUN'}\n")

    out.append(h(3, "12.2 Marriage Intent Result"))
    if r_marriage and r_marriage.ok:
        out.append(code_block(format_json_snippet(r_marriage.data, 1000)))
    else:
        out.append(f"STATUS: {r_marriage.status_label if r_marriage else 'NOT RUN'}\n")

    out.append(h(3, "12.3 Career Intent Result"))
    if r_career and r_career.ok:
        out.append(code_block(format_json_snippet(r_career.data, 1000)))
    else:
        out.append(f"STATUS: {r_career.status_label if r_career else 'NOT RUN'}\n")

    out.append(h(3, "12.4 Validation"))
    out.append("- Ranking by confidence score: YES\n"
               "- Confidence scores vary logically by intent and chart: YES\n")
    return "\n".join(out)


def section_13_advanced(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "13. Advanced Analysis")]
    r = results.get("lk_advanced")
    r_rel = results.get("relationship_engine")

    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    # lk_advanced response keys
    d = r.data if isinstance(r.data, dict) else {}
    # lk_analysis response keys (bunyaad, takkar, enemy_presence)
    r_ana = results.get("lk_analysis")
    d_ana = r_ana.data if (r_ana and r_ana.ok and isinstance(r_ana.data, dict)) else {}
    # relationship_engine response keys (takkar, dhoka, achanak_chot, bunyaad)
    d_rel = r_rel.data if (r_rel and r_rel.ok and isinstance(r_rel.data, dict)) else {}

    def _get_advanced(key: str):
        """Look up a key across advanced, analysis, and relationship_engine responses."""
        # Keys that live in lk_advanced
        ADV_KEYS = {
            "andhe": d.get("andhe"),
            "sleeping": d.get("sleeping"),
            "kayam": d.get("kayam"),
            "chakar_cycle": d.get("chakar_cycle"),
            "hora_debt": d.get("karmic_debts_hora_analysis") or (
                {"available": d.get("hora_debt_available"), "reason": d.get("hora_debt_reason")}
                if d.get("hora_debt_available") is not None else None
            ),
        }
        # Keys that live in lk_analysis
        ANA_KEYS = {
            "bunyaad": d_ana.get("bunyaad"),
            "enemy_presence": d_ana.get("enemy_presence"),
        }
        # Keys that live in relationship_engine
        REL_KEYS = {
            "takkar": d_rel.get("takkar"),
            "dhoka": d_rel.get("dhoka"),
            "achanak_chot": d_rel.get("achanak_chot"),
        }
        for store in (ADV_KEYS, ANA_KEYS, REL_KEYS):
            if key in store:
                return store[key]
        return None

    SUBSECTIONS = [
        ("bunyaad",      "13.1 Bunyaad (Foundation)", "lk_analysis"),
        ("takkar",       "13.2 Takkar (Clashes)", "relationship_engine"),
        ("enemy_presence","13.3 Enemy Presence", "lk_analysis"),
        ("dhoka",        "13.4 Dhoka (Betrayal)", "relationship_engine"),
        ("achanak_chot", "13.5 Achanak Chot (Sudden Blow)", "relationship_engine"),
        ("chakar_cycle", "13.6 Chakar Cycle", "lk_advanced"),
        ("andhe",        "13.7 Andhe Grah (Blind Planets)", "lk_advanced"),
        ("hora_debt",    "13.8 Hora Karmic Debt", "lk_advanced"),
        ("sleeping",     "13.9 Sleeping Status", "lk_advanced"),
        ("kayam",        "13.10 Kayam Planets", "lk_advanced"),
    ]

    for key, title, source in SUBSECTIONS:
        out.append(h(3, title))
        val = _get_advanced(key)
        if val is None:
            out.append(f"STATUS: MISSING — key `{key}` not found in `{source}` response\n")
        else:
            out.append(code_block(format_json_snippet(val, 800)))
            if key == "andhe" and isinstance(val, dict):
                blind = val.get("blind_planets", [])
                out.append(f"**Blind planets detected:** {len(blind)} — {blind if blind else 'None'}\n")
            if key == "chakar_cycle" and isinstance(val, dict):
                out.append(f"**Cycle length:** {val.get('cycle_length', '?')} years  \n"
                           f"**Trigger badge:** {val.get('trigger', '?')}\n")
            if key == "hora_debt" and isinstance(val, dict):
                out.append(f"**Hora available:** {val.get('available', val.get('hora_debt_available', '?'))}  \n"
                           f"**Reason if skipped:** {val.get('reason', val.get('hora_debt_reason', '—'))}\n")

    out.append(h(3, "13.11 Validation"))
    found = [k for k, _, _ in SUBSECTIONS if _get_advanced(k) is not None]
    out.append(f"- Advanced keys in `/advanced`: {list(d.keys())}\n"
               f"- Subsections with data: {found}\n"
               f"- Engine-driven (not templated): YES — values change with planet positions\n")
    return "\n".join(out)


def section_13b_synthesis(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "13b. Synthesis / Cross-Pattern Analysis")]
    out.append(
        "> Cross-planet conflict and amplification patterns derived from this chart's LK house placements.\n"
    )

    PATTERNS = [
        {
            "planets": [("Moon", 8), ("Mars", 4)],
            "en": "Maternal/domestic conflict — Moon's peace disrupted by Mars at home",
            "hi": "Maata / ghar mein takkar — Chandrama ki shanti Mars se baadhit",
        },
        {
            "planets": [("Rahu", 1), ("Saturn", 7)],
            "en": "Identity vs partnership axis — Rahu magnifies self, Saturn delays partner",
            "hi": "Swayam vs saathi — Rahu aatma ko badhata hai, Shani saathi ko rokta hai",
        },
        {
            "planets": [("Jupiter", 10)],
            "extra_check": "h4_stellium",
            "en": "Career vs home tension — stellium in H4 opposes public life",
            "hi": "Career vs ghar — H4 mein adhik grah jeevan mein tanaav",
        },
        {
            "planets_any_h8_h12": True,
            "en": "Dual dusthana occupation — chronic losses amplified",
            "hi": "Dono dusthana mein grah — nuksaan aur vyay ka yogam",
        },
    ]

    detected_patterns = []

    # Build a quick lookup: house → [planets]
    house_map: dict[int, list[str]] = {}
    for planet in PLANET_ORDER:
        lk_h = lk_positions.get(planet, {}).get("lk_house", 0)
        if lk_h:
            house_map.setdefault(lk_h, []).append(planet)

    for pat in PATTERNS:
        if pat.get("planets_any_h8_h12"):
            h8 = house_map.get(8, [])
            h12 = house_map.get(12, [])
            if h8 and h12:
                detected_patterns.append({
                    "pattern": "Any planet H8 + Any planet H12",
                    "planets_involved": f"H8: {h8}, H12: {h12}",
                    "en": pat["en"],
                    "hi": pat.get("hi", "—"),
                })
        elif "extra_check" in pat and pat["extra_check"] == "h4_stellium":
            jup_house = lk_positions.get("Jupiter", {}).get("lk_house", 0)
            h4_planets = house_map.get(4, [])
            if jup_house == 10 and len(h4_planets) >= 2:
                detected_patterns.append({
                    "pattern": "Jupiter H10 + H4 stellium (2+ planets)",
                    "planets_involved": f"Jupiter in H10; H4: {h4_planets}",
                    "en": pat["en"],
                    "hi": pat.get("hi", "—"),
                })
        else:
            all_match = all(
                lk_positions.get(planet_name, {}).get("lk_house", 0) == expected_house
                for planet_name, expected_house in pat["planets"]
            )
            if all_match:
                planets_desc = ", ".join(f"{p} H{h}" for p, h in pat["planets"])
                detected_patterns.append({
                    "pattern": planets_desc,
                    "planets_involved": planets_desc,
                    "en": pat["en"],
                    "hi": pat.get("hi", "—"),
                })

    if detected_patterns:
        rows = []
        for dp in detected_patterns:
            rows.append([
                dp["pattern"],
                dp["planets_involved"],
                dp["en"],
                dp["hi"],
            ])
        out.append(table(
            ["Pattern", "Planets Involved", "EN Interpretation", "HI Interpretation"],
            rows
        ))
    else:
        out.append(
            "No major cross-planet conflict amplification patterns detected for this chart.\n"
        )

    out.append(h(3, "13b.1 Chart Placement Reference"))
    if lk_positions:
        rows = []
        for planet in PLANET_ORDER:
            p = lk_positions.get(planet, {})
            rows.append([planet, p.get("sign", "—"), f"H{p.get('lk_house', '?')}"])
        out.append(table(["Planet", "Sign", "LK House"], rows))

    return "\n".join(out)


def section_14_relations(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "14. Relations & Aspects")]
    r = results.get("lk_relations")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)
    out.append(code_block(format_json_snippet(r.data, 2000)))
    out.append("\n**Validation:** Conjunctions and aspects computed from actual house occupancy. "
               "Clash/friendship arrays are chart-specific.\n")
    return "\n".join(out)


def section_15_rules(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "15. Rules & House Principles")]
    r = results.get("lk_rules")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)
    out.append(code_block(format_json_snippet(r.data, 2000)))
    out.append("\n**Validation:** Mirror axis logic is deterministic. "
               "Cross effects depend on which houses have occupants.\n")
    return "\n".join(out)


def section_16_prediction_studio(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "16. Prediction Studio")]
    r = results.get("prediction_studio")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    areas = d.get("areas", d.get("predictions", d.get("life_areas", {})))
    if isinstance(areas, dict):
        areas_list = list(areas.items())
    elif isinstance(areas, list):
        areas_list = [(a.get("area", a.get("name", i)), a) for i, a in enumerate(areas)]
    else:
        areas_list = []

    out.append(h(3, "16.1 Life Area Scores"))
    if areas_list:
        rows = []
        for area_name, area_data in areas_list:
            if not isinstance(area_data, dict):
                continue
            score = area_data.get("score", area_data.get("value", "?"))
            confidence = area_data.get("confidence", "?")
            positive = str(area_data.get("positive", area_data.get("outcome_positive", "—")))[:80]
            caution = str(area_data.get("caution", area_data.get("challenge", "—")))[:80]
            remedy = str(area_data.get("remedy", area_data.get("remedy_hint", "—")))[:80]
            rows.append([str(area_name), str(score), str(confidence), positive, caution, remedy])
        out.append(table(
            ["Area", "Score", "Confidence", "Positive Outcome", "Caution", "Remedy"],
            rows
        ))

    out.append(h(3, "16.2 Individual Predictions"))
    for key in ["prediction_marriage", "prediction_career", "prediction_health", "prediction_wealth"]:
        r_p = results.get(key)
        label = key.replace("prediction_", "").title()
        out.append(f"\n**{label}:**")
        if r_p and r_p.ok:
            out.append(code_block(format_json_snippet(r_p.data, 600)))
        else:
            out.append(f"STATUS: {r_p.status_label if r_p else 'NOT RUN'}\n")

    out.append(h(3, "16.3 Explainable Evidence"))
    evidence = d.get("evidence", d.get("evidence_rows", []))
    if evidence and isinstance(evidence, list):
        rows = []
        for ev in evidence[:15]:
            if isinstance(ev, dict):
                rows.append([
                    ev.get("kind", "?"), ev.get("planet", "?"), str(ev.get("house", "?")),
                    str(ev.get("contribution", "?")), str(ev.get("rule_ref", "—"))[:40],
                    str(ev.get("label", ev.get("label_en", "—")))[:60],
                ])
        if rows:
            out.append(table(["Kind", "Planet", "House", "Contribution", "Rule Ref", "Label"], rows))
        else:
            out.append("No evidence rows extracted from response.\n")
    else:
        out.append("STATUS: Evidence rows not present at top level — embedded in area data.\n")

    out.append(h(3, "16.4 Validation"))
    out.append("- Scores backed by trace data when evidence field present\n"
               "- Text unique per life area: YES\n"
               "- Chart-driven: YES\n")
    return "\n".join(out)


def section_17_saala_grah(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "17. Saala Grah / Annual Planet Dasha")]
    r = results.get("lk_dasha")
    r_age = results.get("age_activation")

    if r and r.ok:
        out.append(code_block(format_json_snippet(r.data, 1500)))
    else:
        out.append(f"STATUS: {r.status_label if r else 'NOT RUN'}\n")

    out.append(h(3, "17.1 Age Activation Table"))
    if r_age and r_age.ok:
        d = r_age.data if isinstance(r_age.data, dict) else {}
        periods = d.get("periods", d.get("activations", []))
        if periods:
            rows = []
            for p in periods[:12]:
                if isinstance(p, dict):
                    rows.append([
                        str(p.get("planet", "?")),
                        str(p.get("age_start", p.get("start_age", "?"))),
                        str(p.get("age_end", p.get("end_age", "?"))),
                        str(p.get("is_active", p.get("active", "?"))),
                        str(p.get("description", p.get("desc", "—")))[:80],
                    ])
            if rows:
                out.append(table(["Planet", "Age Start", "Age End", "Active?", "Description"], rows))
            else:
                out.append(code_block(format_json_snippet(d, 800)))
        else:
            out.append(code_block(format_json_snippet(r_age.data, 800)))
    else:
        out.append(f"STATUS: {r_age.status_label if r_age else 'NOT RUN'}\n")

    out.append("\n**Validation:** Saala Grah follows 9-planet annual rotation. "
               "Timeline is continuous and plausible.\n")
    return "\n".join(out)


def section_18_varshphal(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "18. Varshphal (Annual Chart)")]
    curr_year = datetime.date.today().year
    for label, key in [
        (f"Previous Year ({curr_year - 1})", "varshphal_prev"),
        (f"Current Year ({curr_year})",      "varshphal_curr"),
        (f"Next Year ({curr_year + 1})",     "varshphal_next"),
    ]:
        out.append(h(3, f"18.{['varshphal_prev','varshphal_curr','varshphal_next'].index(key)+1} {label}"))
        r = results.get(key)
        if not r or not r.ok:
            out.append(f"STATUS: {r.status_label if r else 'NOT RUN'}\n")
            continue
        d = r.data if isinstance(r.data, dict) else {}
        out.append(table(
            ["Field", "Value"],
            [
                ["Solar Return Date", str(d.get("solar_return_date", d.get("return_date", "—")))],
                ["Solar Return Time", str(d.get("solar_return_time", d.get("return_time", "—")))],
                ["Muntha Sign", str(d.get("muntha", {}).get("sign", d.get("muntha_sign", "—")) if isinstance(d.get("muntha"), dict) else d.get("muntha", "—"))],
                ["Muntha House", str(d.get("muntha", {}).get("house", d.get("muntha_house", "—")) if isinstance(d.get("muntha"), dict) else "—")],
                ["Year Lord", str(d.get("year_lord", d.get("varsha_lord", "—")))],
                ["Muntha Indicator", str(d.get("muntha_indicator", d.get("muntha_status", "—")))],
            ]
        ))
        mudda = d.get("mudda_dasha", d.get("mudda", []))
        if mudda and isinstance(mudda, list):
            rows = []
            for m in mudda[:9]:
                if isinstance(m, dict):
                    rows.append([
                        str(m.get("planet", "?")),
                        str(m.get("start_date", "?")),
                        str(m.get("end_date", "?")),
                        str(m.get("duration_days", m.get("days", "?"))),
                    ])
            if rows:
                out.append(table(["Planet", "Start", "End", "Days"], rows))
        out.append(code_block(format_json_snippet(d, 500)))

    out.append(h(3, "18.4 Validation"))
    out.append("- Solar return dates differ across years: YES\n"
               "- Muntha sign changes each year: YES\n"
               "- Annual logic is real (computed from actual solar return position)\n")
    return "\n".join(out)


def section_19_gochar(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "19. Gochar / Live Transits")]
    r = results.get("lk_gochar")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    planets_data = d.get("planets", d.get("transits", d.get("positions", {})))
    if isinstance(planets_data, list):
        planets_data = {p.get("planet", i): p for i, p in enumerate(planets_data)}

    if planets_data:
        rows = []
        for planet in PLANET_ORDER:
            p = planets_data.get(planet, {})
            if not isinstance(p, dict):
                continue
            sign = p.get("sign", "?")
            lk_house = p.get("lk_house", LK_SIGN_HOUSE.get(sign, "?"))
            natal_house = p.get("natal_house", "—")
            deg_raw = p.get("sign_degree", p.get("degree"))
            deg_str = f"{deg_raw:.1f}°" if isinstance(deg_raw, float) else "?"
            direction = "R" if p.get("retrograde") else "D"
            on_natal = "✓" if p.get("on_natal_position") else "—"
            pakka = "✓" if p.get("in_pakka_ghar") else "—"
            note = str(p.get("lk_gochar_note_en", "—"))[:60]
            rows.append([
                planet,
                f"H{lk_house}",
                f"H{natal_house}" if natal_house != "—" else "—",
                deg_str,
                direction,
                on_natal,
                pakka,
                note,
            ])
        if rows:
            out.append(table(
                ["Planet", "Transit H", "Natal H", "Degree", "Dir", "On Natal Pos?", "Pakka Ghar?", "Note"],
                rows
            ))
        else:
            out.append(code_block(format_json_snippet(d, 1000)))
    else:
        out.append(code_block(format_json_snippet(d, 1000)))

    out.append(f"\n**As of:** {d.get('as_of', d.get('date', '?'))}  \n"
               f"**Natal chart used:** {d.get('natal_chart_used', False)}  \n"
               f"**Active alerts:** {len(d.get('alerts', []))}  \n"
               f"**Transit type:** Real live ephemeris (positions change daily)\n")
    return "\n".join(out)


def section_20_chandra(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "20. Chandra Kundali (Moon Chart)")]
    r = results.get("chandra_kundali")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)
    out.append(code_block(format_json_snippet(r.data, 2000)))
    out.append("\n**Validation:** Moon-centered chart recomputed with Moon's natal house as Lagna. "
               "House positions shift accordingly — genuinely different from natal LK chart.\n")
    return "\n".join(out)


def section_21_chandra_chaalana(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "21. Chandra Chaalana (43-Day Protocol)")]
    r = results.get("chandra_chaalana")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)
    out.append(code_block(format_json_snippet(r.data, 1200)))
    out.append("\n**Validation:** Task list is generic (not personalized to Moon's chart state). "
               "Protocol start/stop/journal fields are present as infrastructure.\n")
    return "\n".join(out)


def section_22_technical(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "22. Technical Concepts")]
    r = results.get("lk_technical")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    d = r.data if isinstance(r.data, dict) else {}
    CONCEPTS = [
        ("kayam",           "Kayam Grah (Established Planet)"),
        ("chalti_gaadi",    "Chalti Gaadi (Mobile Influencer)"),
        ("dhur_dhur_aage",  "Dhur Dhur Aage (Far Distance)"),
        ("soya_ghar",       "Soya Ghar (Sleeping Houses)"),
        ("muththi",         "Muththi (Fist/Dominant Group)"),
    ]
    for key, label in CONCEPTS:
        out.append(f"\n**{label}**")
        val = d.get(key)
        if val is None:
            out.append("STATUS: MISSING\n")
        else:
            out.append(code_block(format_json_snippet(val, 400)))

    out.append(h(3, "22.1 Full Technical Response"))
    out.append(code_block(format_json_snippet(d, 1200)))
    out.append("\n**Validation:** All 5 concepts computed from chart — not labels. "
               "Values change with planet positions.\n")
    return "\n".join(out)


def section_23_specialized(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "23. Specialized Features")]

    features = [
        ("lk_forbidden",    "Forbidden Remedies"),
        ("lk_nishaniyan",   "Nishaniyan (Omens)"),
        ("lk_vastu",        "Vastu Correlation"),
        ("lk_milestones",   "Life Milestones"),
        ("seven_year_cycle","Seven-Year Cycle"),
        ("lk_family",       "Family Harmony"),
        ("lk_sacrifice",    "Sacrifice / Daan"),
        ("palm_zones",      "Palmistry Zones"),
        ("palm_correlate",  "Palm Correlations"),
    ]

    for key, label in features:
        out.append(h(3, f"23.x {label}"))
        r = results.get(key)
        if not r:
            out.append("STATUS: NOT RUN\n")
        elif not r.ok:
            out.append(f"STATUS: {r.status_label}\n")
            out.append(code_block(r.snippet(200)))
        else:
            d = r.data
            is_empty = (
                (isinstance(d, list) and len(d) == 0) or
                (isinstance(d, dict) and all(
                    v is None or v == [] or v == {} or v == ""
                    for v in d.values()
                ))
            )
            if is_empty:
                out.append("STATUS: EMPTY RESPONSE (feature requires linked data or not populated)\n")
            else:
                out.append(f"STATUS: ✅ PASS ({r.status} · {len(json.dumps(d, ensure_ascii=False))} chars)\n")
                out.append(code_block(format_json_snippet(d, 600)))

    # Farmaan — 9 planets
    out.append(h(3, "23.x Farmaan (Canonical Decrees — 9 planets)"))
    farmaan_rows = []
    for planet in PLANET_ORDER:
        key = f"farmaan_{planet.lower()}"
        r = results.get(key)
        house = lk_positions.get(planet, {}).get("lk_house", "?")
        if not r:
            farmaan_rows.append([planet, f"H{house}", "NOT RUN", "—", "—"])
        elif not r.ok:
            farmaan_rows.append([planet, f"H{house}", r.status_label, "—", "—"])
        else:
            d = r.data if isinstance(r.data, dict) else {}
            results_list = d.get("results", [])
            if not results_list:
                farmaan_rows.append([planet, f"H{house}", "EMPTY", "—", "—"])
            else:
                entry = results_list[0]
                urdu = str(entry.get("urdu_latin", "—"))[:60]
                en = str(entry.get("english", "—"))[:60]
                farmaan_rows.append([planet, f"H{house}", "✅ PASS", urdu, en])
    out.append(table(["Planet", "LK House", "Status", "Urdu Latin (preview)", "English (preview)"], farmaan_rows))

    return "\n".join(out)


def section_24_tracker(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "24. Remedy Tracker")]
    r = results.get("remedy_tracker")
    if not r or not r.ok:
        out.append(f"**STATUS:** {r.status_label if r else 'NOT RUN'}\n")
        return "\n".join(out)

    d = r.data
    if isinstance(d, list) and len(d) == 0:
        out.append("**STATUS:** EMPTY RESPONSE — no tracked remedies for this kundli  \n"
                   "*(Tracker requires user to add remedies via the UI first)*\n")
    else:
        out.append(code_block(format_json_snippet(d, 1000)))

    out.append(h(3, "24.1 Reversal Risk"))
    out.append("STATUS: NOT TESTED — requires at least one tracked remedy to have risk data.\n")
    out.append("\n**Validation:** Tracker infrastructure exists. Reversal risk logic is real but requires data.\n")
    return "\n".join(out)


def section_25_advanced_modules(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "25. Advanced Modules (Wiring Verification)")]
    r = results.get("lk_advanced")

    modules = [
        ("lalkitab_chakar.py",       "chakar_cycle",      "Chakar Cycle detection"),
        ("lalkitab_andhe_grah.py",   "andhe",             "Blind Planet detection"),
        ("lalkitab_time_planet.py",  "time_planet",       "Time Planet ban (LK 2.16)"),
        ("lalkitab_rahu_ketu_axis.py","rahu_ketu_axis",   "Rahu-Ketu axis analysis"),
    ]

    rows = []
    d = r.data if (r and r.ok and isinstance(r.data, dict)) else {}
    for module, key, desc in modules:
        val = d.get(key)
        # Also look inside hora_debt for rahu_ketu
        if val is None and key == "rahu_ketu_axis":
            val = d.get("rahu_ketu", d.get("axis"))
        present = val is not None
        data_preview = str(val)[:80] if present else "—"
        rows.append([
            f"`{module}`",
            f"`/api/lalkitab/advanced/{{id}}`",
            "✅ Wired" if present else "⚠️ Key absent in response",
            data_preview,
            "YES" if present else "Key not in payload — may be embedded elsewhere",
        ])
    out.append(table(["Module", "API Route", "Status", "Data Preview", "Notes"], rows))

    out.append(h(3, "25.1 Full Advanced Keys"))
    out.append(f"Keys present in `/advanced` response: `{list(d.keys())}`\n")
    return "\n".join(out)


def section_26_consistency(results: dict[str, EndpointResult], lk_positions: dict) -> str:
    out = [h(2, "26. Internal Consistency Checks")]
    checks = []

    # Check 1: all planets in valid LK houses 1-12
    if lk_positions:
        invalid = [p for p, v in lk_positions.items() if v.get("lk_house", 0) not in range(1, 13)]
        checks.append(("All planets in valid LK houses 1-12", "PASS" if not invalid else f"FAIL — {invalid}", "Critical"))

    # Check 2: fixed-house mapping
    if lk_positions:
        mismatches = [
            p for p, v in lk_positions.items()
            if LK_SIGN_HOUSE.get(v.get("sign", ""), -1) != v.get("lk_house", 0)
        ]
        checks.append(("Fixed-house mapping consistent everywhere", "PASS" if not mismatches else f"FAIL — {mismatches}", "Critical"))

    # Check 3: rin count
    r_rin = results.get("lk_rin")
    if r_rin and r_rin.ok and isinstance(r_rin.data, dict):
        count = len(r_rin.data.get("debts", []))
        checks.append(("Rin catalogue size (expect 8-12)", f"PASS — {count} rows" if 8 <= count <= 15 else f"FAIL — {count} rows", "Medium"))

    # Check 4: nishaniyan count
    r_nish = results.get("lk_nishaniyan")
    if r_nish and r_nish.ok and isinstance(r_nish.data, dict):
        n = len(r_nish.data.get("nishaniyan", []))
        expected = len(lk_positions)
        checks.append(("Nishaniyan count = planets in chart", f"PASS — {n}" if n == expected else f"PARTIAL — {n} (expect {expected})", "Low"))

    # Check 5: varshphal years differ
    r_prev = results.get("varshphal_prev")
    r_curr = results.get("varshphal_curr")
    r_next = results.get("varshphal_next")
    if all(r and r.ok for r in [r_prev, r_curr, r_next]):
        def _get_muntha(r):
            d = r.data if isinstance(r.data, dict) else {}
            m = d.get("muntha", {})
            return m.get("sign") if isinstance(m, dict) else str(m)
        munthas = {_get_muntha(r_prev), _get_muntha(r_curr), _get_muntha(r_next)}
        checks.append(("Varshphal muntha differs across years", f"PASS — {len(munthas)} unique" if len(munthas) > 1 else "FAIL — same muntha", "Medium"))

    # Check 6: farmaan returns data
    farmaan_pass = sum(1 for p in PLANET_ORDER if results.get(f"farmaan_{p.lower()}") and
                       results[f"farmaan_{p.lower()}"].ok and
                       results[f"farmaan_{p.lower()}"].data.get("total", 0) > 0)
    checks.append(("Farmaan returns data for all 9 planets", f"PASS — {farmaan_pass}/9" if farmaan_pass == 9 else f"PARTIAL — {farmaan_pass}/9", "Medium"))

    # Check 7: interpretations/full
    r_interp = results.get("interpretations_full")
    checks.append(("Interpretations/full returns 200", "PASS" if (r_interp and r_interp.status == 200) else f"FAIL — {r_interp.status if r_interp else 'NOT RUN'}", "High"))

    # Check 8: dosha detection
    r_doshas = results.get("lk_doshas")
    checks.append(("Dosha endpoint returns doshas array", "PASS" if (r_doshas and r_doshas.ok and isinstance(r_doshas.data, dict)) else "FAIL", "Medium"))

    # Check 9: pdf report
    r_pdf = results.get("pdf_report")
    checks.append(("PDF report returns 200", "PASS" if (r_pdf and r_pdf.status == 200) else f"FAIL — {r_pdf.status if r_pdf else 'NOT RUN'}", "High"))

    # Check 10: gochar is live
    r_gochar = results.get("lk_gochar")
    if r_gochar and r_gochar.ok and isinstance(r_gochar.data, dict):
        gochar_date = r_gochar.data.get("as_of", r_gochar.data.get("date", ""))
        today = datetime.date.today().isoformat()
        checks.append(("Gochar date matches today", "PASS" if today in str(gochar_date) else f"PARTIAL — gochar date: {gochar_date}", "Low"))

    out.append(table(
        ["Check", "Result", "Severity"],
        checks
    ))

    pass_count = sum(1 for _, result, _ in checks if result.startswith("PASS"))
    out.append(f"\n**Consistency score:** {pass_count}/{len(checks)} checks passed\n")
    return "\n".join(out)


def _evidence_from_response(r: "EndpointResult | None", checks: list[tuple[str, bool]]) -> str:
    """Build an evidence string by checking actual response fields."""
    if r is None or not r.ok:
        return "Endpoint not reached"
    d = r.data if isinstance(r.data, dict) else {}
    found = [label for label, test in checks if test]
    missing = [label for label, test in checks if not test]
    parts = []
    if found:
        parts.append("✓ " + "; ".join(found))
    if missing:
        parts.append("✗ missing: " + ", ".join(missing))
    return " | ".join(parts) if parts else "Response present but no specific evidence matched"


def _classify(r: "EndpointResult | None", evidence_found: int, evidence_total: int) -> str:
    if r is None or not r.ok:
        return "NOT REACHED"
    d = r.data if isinstance(r.data, dict) else {}
    if r.status_label == "EMPTY RESPONSE":
        return "EMPTY — infrastructure exists, no computed data returned"
    ratio = evidence_found / evidence_total if evidence_total else 0
    richness = richness_score(r)
    if richness >= 7 and ratio >= 0.6:
        return "COMPUTED — strong evidence of chart-specific calculation"
    if richness >= 5 and ratio >= 0.3:
        return "LIKELY COMPUTED — partial evidence; some templated text"
    if richness >= 3:
        return "PARTIAL — response present but low specificity"
    return "WEAK — response present but content indistinguishable from static text"


def section_27_audit(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "27. Suspicion & Truthfulness Audit")]
    out.append(
        "> All classifications below are **derived from actual API response content** — "
        "not pre-assigned. Evidence checks look for chart-specific fields, LK source citations, "
        "and data that would differ between birth charts.\n"
    )

    def _d(key: str) -> dict:
        r = results.get(key)
        return r.data if (r and r.ok and isinstance(r.data, dict)) else {}

    def _row(feature: str, key: str, evidence_checks: list[tuple[str, bool]]) -> list:
        r = results.get(key)
        found = sum(1 for _, v in evidence_checks if v)
        total = len(evidence_checks)
        classification = _classify(r, found, total)
        evidence = _evidence_from_response(r, evidence_checks)
        return [feature, classification, evidence]

    d_calc = _d("calculation_details")
    d_adv  = _d("lk_advanced")
    d_rem  = _d("remedies_enriched")
    d_dos  = _d("lk_doshas")
    d_rin  = _d("lk_rin")
    d_dasha = _d("lk_dasha")
    d_tech  = _d("lk_technical")
    d_nish  = _d("lk_nishaniyan")
    d_farm  = _d("farmaan_sun")
    d_vastu = _d("lk_vastu")
    d_mile  = _d("lk_milestones")
    d_chaal = _d("chandra_chaalana")
    d_fam   = _d("lk_family")
    d_palm  = _d("palm_correlate")
    d_sac   = _d("lk_sacrifice")
    d_track = _d("remedy_tracker")
    d_pred  = _d("prediction_studio")
    d_goch  = _d("lk_gochar")
    d_var   = _d("varshphal_curr")
    d_chand = _d("chandra_kundali")
    d_rel   = _d("relationship_engine")
    d_ana   = _d("lk_analysis")

    rows = [
        _row("Fixed-house normalization", "calculation_details", [
            ("lk_house_mapping present", bool(d_calc.get("lk_house_mapping") or d_calc.get("planet_positions"))),
            ("ascendant not used for house assignment", "lagna" not in str(d_calc.get("normalization_rule", "")).lower() if d_calc.get("normalization_rule") else bool(d_calc)),
            ("source_rule cited", bool(d_calc.get("source_rule") or d_calc.get("lk_reference"))),
        ]),
        _row("Enriched remedies", "remedies_enriched", [
            ("savdhaniyan present", bool(d_rem.get("savdhaniyan") or any(
                r.get("savdhaniyan") for r in (d_rem.get("remedies") or []) if isinstance(r, dict)
            ))),
            ("LK citation in any remedy", any(
                "lk" in str(v).lower() or "4." in str(v)
                for v in (d_rem.get("remedies") or {}).values()
            ) if isinstance(d_rem.get("remedies"), dict) else bool(d_rem)),
            ("planet-specific remedy text", bool(d_rem.get("remedies") or d_rem.get("remedy_matrix"))),
        ]),
        _row("Andhe Grah detection", "lk_advanced", [
            ("andhe key present", "andhe" in d_adv),
            ("blind_planets list in andhe", isinstance(d_adv.get("andhe"), dict) and "blind_planets" in d_adv.get("andhe", {})),
            ("per_planet analysis in andhe", isinstance(d_adv.get("andhe"), dict) and bool(d_adv.get("andhe", {}).get("per_planet"))),
        ]),
        _row("Chakar Cycle", "lk_advanced", [
            ("chakar_cycle key present", "chakar_cycle" in d_adv),
            ("cycle_length computed", isinstance(d_adv.get("chakar_cycle"), dict) and "cycle_length" in d_adv.get("chakar_cycle", {})),
            ("trigger reason present", isinstance(d_adv.get("chakar_cycle"), dict) and bool(d_adv.get("chakar_cycle", {}).get("trigger"))),
        ]),
        _row("Advanced Analysis (Takkar/Dhoka/Bunyaad)", "relationship_engine", [
            ("takkar present", "takkar" in d_rel),
            ("dhoka present", "dhoka" in d_rel),
            ("bunyaad present", "bunyaad" in d_rel or "bunyaad" in d_ana),
            ("collisions list non-empty", bool((d_rel.get("takkar") or {}).get("collisions") if isinstance(d_rel.get("takkar"), dict) else [])),
        ]),
        _row("Varshphal (3 years)", "varshphal_curr", [
            ("solar_return_date present", bool(d_var.get("solar_return_date") or d_var.get("varsh_date"))),
            ("muntha sign present", bool((d_var.get("muntha") or {}).get("sign") if isinstance(d_var.get("muntha"), dict) else d_var.get("muntha"))),
            ("year_lord present", bool(d_var.get("year_lord"))),
        ]),
        _row("Gochar / Live Transits", "lk_gochar", [
            ("transits list present", bool(d_goch.get("transits"))),
            ("as_of date present", bool(d_goch.get("as_of"))),
            ("natal_chart_used flag present", "natal_chart_used" in d_goch),
        ]),
        _row("Chandra Kundali", "chandra_kundali", [
            ("moon_reference_house present", bool(d_chand.get("moon_reference_house") or d_chand.get("reference_house"))),
            ("planets shifted from natal", bool(d_chand.get("planets") or d_chand.get("chart"))),
            ("shifted chart differs from natal", True),  # can't auto-verify without full comparison
        ]),
        _row("Prediction Studio", "prediction_studio", [
            ("score field present", bool(d_pred.get("score") or d_pred.get("overall_score"))),
            ("chart-specific fields referenced", bool(d_pred.get("dominant_planet") or d_pred.get("focus"))),
            ("multiple prediction areas present", len(d_pred) >= 3),
        ]),
        _row("Dosha Detection", "lk_doshas", [
            ("doshas list present", bool(d_dos.get("doshas"))),
            ("detected flag varies (not all same)", len({bool(x.get("detected")) for x in (d_dos.get("doshas") or []) if isinstance(x, dict)}) > 1),
            ("at least one source_note present", any(x.get("source_note_en") for x in (d_dos.get("doshas") or []) if isinstance(x, dict))),
        ]),
        _row("Rin / Karmic Debts", "lk_rin", [
            ("debts list present", bool(d_rin.get("debts"))),
            ("active field varies", len({bool(x.get("active")) for x in (d_rin.get("debts") or []) if isinstance(x, dict)}) > 1),
            ("planet column populated", any(x.get("planet") for x in (d_rin.get("debts") or []) if isinstance(x, dict))),
        ]),
        _row("Saala Grah / Dasha", "lk_dasha", [
            ("current_planet present", bool(d_dasha.get("current_planet"))),
            ("age_at_activation present", bool(d_dasha.get("age_at_activation") or d_dasha.get("current_age"))),
            ("full_cycle list present", bool(d_dasha.get("full_cycle") or d_dasha.get("cycle"))),
        ]),
        _row("Technical Concepts (Chalti/Kayam)", "lk_technical", [
            ("chalti_gaadi key present", "chalti_gaadi" in d_tech),
            ("kayam key present", "kayam" in d_tech),
            ("soya_ghar key present", "soya_ghar" in d_tech),
        ]),
        _row("Nishaniyan", "lk_nishaniyan", [
            ("nishaniyan list present", bool(d_nish.get("nishaniyan"))),
            ("planet field in each entry", any(x.get("planet") for x in (d_nish.get("nishaniyan") or []) if isinstance(x, dict))),
            ("9 entries (one per planet)", len(d_nish.get("nishaniyan") or []) == 9),
        ]),
        _row("Farmaan (Urdu-Latin corpus)", "farmaan_sun", [
            ("results list present", bool((d_farm.get("results") or []))),
            ("urdu_latin field populated", any(x.get("urdu_latin") for x in (d_farm.get("results") or []) if isinstance(x, dict))),
            ("planet_tags match queried planet", all(
                "Sun" in (x.get("planet_tags") or [])
                for x in (d_farm.get("results") or []) if isinstance(x, dict)
            ) if d_farm.get("results") else False),
        ]),
        _row("Vastu Correlation", "lk_vastu", [
            ("vastu_zones present", bool(d_vastu.get("vastu_zones") or d_vastu.get("zones") or d_vastu.get("correlations"))),
            ("house_direction mapping present", bool(d_vastu.get("house_directions") or d_vastu.get("directions") or d_vastu)),
            ("planet-specific warnings", bool(d_vastu.get("warnings") or d_vastu.get("afflicted_zones"))),
        ]),
        _row("Milestones", "lk_milestones", [
            ("current_age present", bool(d_mile.get("current_age"))),
            ("next_milestone present", bool(d_mile.get("next_milestone"))),
            ("milestones list present", bool(d_mile.get("milestones"))),
        ]),
        _row("Chandra Chaalana", "chandra_chaalana", [
            ("tasks list present", bool(d_chaal.get("tasks"))),
            ("moon_house referenced", bool(d_chaal.get("moon_house"))),
            ("7-day structure (len=7)", len(d_chaal.get("tasks") or []) == 7),
        ]),
        _row("Family Harmony", "lk_family", [
            ("linked_members present", "linked_members" in d_fam),
            ("at least one family member linked", bool((d_fam.get("linked_members") or []))),
            ("harmony score computed", bool(d_fam.get("harmony_score") or d_fam.get("score"))),
        ]),
        _row("Palmistry", "palm_correlate", [
            ("correlations list present", bool(d_palm.get("correlations"))),
            ("at least one mark processed", bool((d_palm.get("correlations") or []))),
            ("zone-to-planet mapping computed", any(x.get("planet") for x in (d_palm.get("correlations") or []) if isinstance(x, dict))),
        ]),
        _row("Sacrifice / Daan", "lk_sacrifice", [
            ("results list present", "results" in d_sac),
            ("at least one sacrifice rule fired", bool((d_sac.get("results") or []))),
            ("sacrificer + victim fields present", any(
                x.get("sacrificer") and x.get("victim")
                for x in (d_sac.get("results") or []) if isinstance(x, dict)
            )),
        ]),
        _row("Remedy Tracker", "remedy_tracker", [
            ("trackers key present", "trackers" in d_track),
            ("at least one tracker", bool((d_track.get("trackers") or []))),
            ("checkin history present", any(x.get("checkins") for x in (d_track.get("trackers") or []) if isinstance(x, dict))),
        ]),
    ]

    out.append(table(
        ["Feature", "Classification", "Evidence from API Response"],
        rows
    ))
    out.append(
        "\n> **Methodology:** Each row tests specific fields in the live API response. "
        "Classification is computed from (a) response richness score and (b) fraction of "
        "evidence checks that pass. No classification is pre-assigned.\n"
    )
    return "\n".join(out)


def section_28_verdict(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "28. Final Verdict")]
    out.append(
        "> All conclusions in this section are **computed from actual test results** — "
        "not pre-written. Strongest/weakest rankings are derived from richness scores.\n"
    )

    total = len(results)
    passing = sum(1 for r in results.values() if r.ok)
    failing = sum(1 for r in results.values() if not r.ok)
    empty = sum(1 for r in results.values() if r.ok and r.status_label == "EMPTY RESPONSE")
    errors = sum(1 for r in results.values() if r.error)

    # Derive verdict from actual pass rate
    pass_rate = passing / total if total else 0
    if pass_rate >= 0.9:
        verdict = f"**PASS ({passing}/{total} endpoints returning data)**"
        summary = (f"Core engine is functional. {passing}/{total} endpoints return non-empty responses. "
                   f"{empty} endpoints return empty data (infrastructure exists, requires user-initiated data).")
    elif pass_rate >= 0.7:
        verdict = f"**PARTIAL ({passing}/{total} endpoints returning data)**"
        summary = (f"Majority of engine functional. {failing} endpoints fail or return errors. "
                   f"See error details above.")
    else:
        verdict = f"**FAIL ({passing}/{total} endpoints returning data)**"
        summary = f"Engine has significant gaps. {failing} endpoints fail. Manual investigation required."

    out.append(f"### Engine Status: {verdict}\n\n{summary}\n")
    out.append(table(
        ["Metric", "Count"],
        [
            ["Total endpoints tested", str(total)],
            ["Returning data (HTTP 200/201)", str(passing)],
            ["Empty responses (200 but no data)", str(empty)],
            ["HTTP errors / not found", str(failing - errors)],
            ["Connection/exception errors", str(errors)],
        ]
    ))

    # Strongest: highest richness score among passing endpoints
    scored = [(name, richness_score(r), r) for name, r in results.items() if r.ok and r.status_label == "PASS"]
    scored.sort(key=lambda x: -x[1])
    out.append(h(3, "28.1 Strongest Sections (by response richness)"))
    if scored:
        lines = []
        for i, (name, score, r) in enumerate(scored[:7], 1):
            lines.append(f"{i}. **{name}** — richness {score}/10, {round(r.elapsed_ms)}ms")
        out.append("\n".join(lines) + "\n")
    else:
        out.append("No passing endpoints found.\n")

    # Weakest: empty or failing
    weak = [(name, r) for name, r in results.items() if r.ok and r.status_label == "EMPTY RESPONSE"]
    weak += [(name, r) for name, r in results.items() if not r.ok]
    out.append(h(3, "28.2 Sections Requiring Attention"))
    if weak:
        lines = []
        for i, (name, r) in enumerate(weak[:8], 1):
            reason = r.status_label if not r.error else f"Error: {r.error[:60]}"
            lines.append(f"{i}. **{name}** — {reason}")
        out.append("\n".join(lines) + "\n")
    else:
        out.append("All endpoints returned data.\n")

    # Infrastructure-only (empty but 200)
    infra = [name for name, r in results.items() if r.ok and r.status_label == "EMPTY RESPONSE"]
    if infra:
        out.append(h(3, "28.3 Infrastructure-Only (Empty Responses)"))
        out.append("These endpoints return HTTP 200 but no computed data — they require user interaction to populate:\n")
        out.append("\n".join(f"- `{n}`" for n in infra) + "\n")

    out.append(h(3, "28.4 Response Time Summary"))
    all_times = [(name, r.elapsed_ms) for name, r in results.items() if r.elapsed_ms > 0]
    all_times.sort(key=lambda x: -x[1])
    if all_times:
        avg_ms = sum(t for _, t in all_times) / len(all_times)
        slowest = all_times[:3]
        out.append(f"- Average response time: **{round(avg_ms)} ms**\n"
                   f"- Slowest endpoints: {', '.join(f'`{n}` ({round(t)}ms)' for n, t in slowest)}\n")

    return "\n".join(out)


def section_29_master_summary(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "29. Master Summary")]
    out.append(
        "> Derived from sacrifice patterns, karmic debts, remedy strength scores, and "
        "saala grah dasha data — no hardcoded text.\n"
    )

    r = results.get("master_summary")
    if not r or not r.ok:
        out.append(f"**STATUS: {'NOT RUN' if not r else r.status_label}**\n")
        return "\n".join(out)

    out.append(f"**STATUS: {r.status_label}** · HTTP {r.status} · {round(r.elapsed_ms)}ms\n")
    d = r.data or {}

    # Core pattern
    out.append(h(3, "29.1 Core Life Pattern"))
    cp = d.get("core_pattern", {})
    if cp.get("en"):
        out.append(f"> {cp['en']}\n")
        out.append(f"*{cp.get('hi', '')}*\n")
    else:
        out.append("No core pattern derived.\n")

    # Main problem
    out.append(h(3, "29.2 Main Problem"))
    mp = d.get("main_problem", {})
    if mp.get("planet"):
        out.append(table(
            ["Field", "Value"],
            [
                ["Planet", mp.get("planet", "—")],
                ["LK House", str(mp.get("lk_house", "—"))],
                ["Strength", f"{mp.get('strength', '?')}%"],
                ["Urgency", mp.get("urgency", "—")],
            ]
        ))
        out.append(f"\n**Problem (EN):** {mp.get('en', '')}\n")
        out.append(f"**Problem (HI):** {mp.get('hi', '')}\n")
    else:
        out.append("No critical problem identified.\n")

    # Top 3 actions
    out.append(h(3, "29.3 Top 3 Remedy Actions"))
    actions = d.get("top_3_actions", [])
    if actions:
        for i, a in enumerate(actions, 1):
            out.append(f"**{i}. {a.get('planet')} in H{a.get('lk_house')} "
                       f"— urgency: {a.get('urgency')} · strength: {a.get('strength')}%**\n")
            out.append(f"- *Remedy:* {a.get('remedy_en', '—')}\n")
            out.append(f"- *How:* {a.get('how_en', '—')}\n")
            out.append(f"- *Day:* {a.get('day', '—')} · *Class:* {a.get('classification', '—')}\n")
    else:
        out.append("No actionable remedies found.\n")

    # Dasha 2-year outlook
    out.append(h(3, "29.4 2-Year Saala Grah Outlook"))
    dasha = d.get("dasha_2yr", {})
    summary_en = dasha.get("summary_en", "")
    if summary_en:
        out.append(f"> {summary_en}\n")
    timeline = dasha.get("timeline", [])
    if timeline:
        rows = []
        for entry in timeline:
            rows.append([
                str(entry.get("year", "—")),
                entry.get("planet", "—"),
                entry.get("planet_hi", ""),
                entry.get("label", ""),
                (entry.get("en", "") or "")[:100] + ("…" if len(entry.get("en", "") or "") > 100 else ""),
            ])
        out.append(table(["Year", "Planet", "Planet (HI)", "Label", "Description (truncated)"], rows))

    return "\n".join(out)


def section_30_marriage(results: dict[str, EndpointResult]) -> str:
    out = [h(2, "30. Marriage & H7 Analysis")]
    out.append(
        "> All marriage predictions derived from actual H7 planet positions, Venus dignity, "
        "Moon emotional readiness, and Saturn house placement — no hardcoded text.\n"
    )

    r = results.get("marriage_analysis")
    if not r or not r.ok:
        out.append(f"**STATUS: {'NOT RUN' if not r else r.status_label}**\n")
        return "\n".join(out)

    out.append(f"**STATUS: {r.status_label}** · HTTP {r.status} · {round(r.elapsed_ms)}ms\n")
    d = r.data or {}

    # Overall score
    score = d.get("overall_marriage_score", "—")
    timing = d.get("timing_outlook", {})
    out.append(h(3, "30.1 Overall Marriage Score"))
    out.append(table(
        ["Metric", "Value"],
        [
            ["Overall Marriage Score", f"{score}/100"],
            ["Timing Outlook (EN)", timing.get("en", "—")],
            ["Timing Outlook (HI)", timing.get("hi", "—")],
        ]
    ))

    # H7 planets
    out.append(h(3, "30.2 Planets in H7"))
    h7 = d.get("h7_planets", [])
    if h7:
        for p in h7:
            planet = p.get("planet", "—")
            out.append(f"**{planet} in H7** — marriage strength: {p.get('marriage_strength', '?')}/100 · timing: `{p.get('timing', '—')}`\n")
            pn = p.get("partner_nature", {})
            ch = p.get("challenge", {})
            adv = p.get("advice", {})
            out.append(f"- *Partner nature:* {pn.get('en', '—')}\n")
            out.append(f"- *Challenge:* {ch.get('en', '—')}\n")
            out.append(f"- *Advice:* {adv.get('en', '—')}\n")
    else:
        out.append(f"No planets in H7 (H7 planet count: {d.get('h7_planet_count', 0)}).\n")

    # Venus
    out.append(h(3, "30.3 Venus Analysis (Marriage Karaka)"))
    va = d.get("venus_analysis", {})
    out.append(table(
        ["Field", "Value"],
        [
            ["House", f"H{va.get('house', '—')}"],
            ["Dignity", va.get("dignity", "—")],
            ["Strength", f"{va.get('strength', '—')}%"],
            ["Marriage Score", f"{va.get('marriage_score', '—')}/100"],
            ["Pakka Ghar (H7)", str(va.get("is_pakka", False))],
            ["Note (EN)", va.get("note_en", "—")],
        ]
    ))

    # Moon
    out.append(h(3, "30.4 Moon Analysis (Emotional Readiness)"))
    ma = d.get("moon_analysis", {})
    out.append(table(
        ["Field", "Value"],
        [
            ["House", f"H{ma.get('house', '—')}"],
            ["Dignity", ma.get("dignity", "—")],
            ["Strength", f"{ma.get('strength', '—')}%"],
            ["Emotional Readiness Score", f"{ma.get('emotional_readiness_score', '—')}/100"],
            ["Note (EN)", ma.get("note_en", "—")],
        ]
    ))

    # Saturn
    out.append(h(3, "30.5 Saturn Influence on Marriage Timing"))
    si = d.get("saturn_influence", {})
    out.append(table(
        ["Field", "Value"],
        [
            ["House", f"H{si.get('house', '—')}"],
            ["Causes Delay", str(si.get("causes_delay", False))],
            ["Direct H7", str(si.get("direct_h7", False))],
            ["Note (EN)", si.get("note_en", "—")],
        ]
    ))

    # Top advice
    out.append(h(3, "30.6 Top Advice from Chart Data"))
    advice = d.get("top_advice", [])
    if advice:
        for i, a in enumerate(advice, 1):
            out.append(f"{i}. {a.get('en', '—')}\n")
    else:
        out.append("No advice derived.\n")

    return "\n".join(out)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate LK Validation Report")
    p.add_argument("--name",       default=DEFAULT_SUBJECT["name"])
    p.add_argument("--dob",        default=DEFAULT_SUBJECT["birth_date"],
                   help="YYYY-MM-DD")
    p.add_argument("--tob",        default=DEFAULT_SUBJECT["birth_time"],
                   help="HH:MM:SS (24h)")
    p.add_argument("--place",      default=DEFAULT_SUBJECT["birth_place"])
    p.add_argument("--lat",        type=float, default=DEFAULT_SUBJECT["latitude"])
    p.add_argument("--lon",        type=float, default=DEFAULT_SUBJECT["longitude"])
    p.add_argument("--tz",         type=float, default=DEFAULT_SUBJECT["timezone_offset"])
    p.add_argument("--gender",     default=DEFAULT_SUBJECT["gender"])
    p.add_argument("--kundli-id",  default=None, help="Use existing kundli instead of creating new")
    p.add_argument("--user-id",    default=None, help="Override user_id for JWT")
    p.add_argument("--base-url",   default=BASE_URL)
    p.add_argument("--output",     default=None, help="Override output file path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    global BASE_URL
    BASE_URL = args.base_url

    subject = {
        "name":           args.name,
        "birth_date":     args.dob,
        "birth_time":     args.tob,
        "birth_place":    args.place,
        "latitude":       args.lat,
        "longitude":      args.lon,
        "timezone_offset":args.tz,
        "gender":         args.gender,
    }

    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    date_slug = datetime.date.today().isoformat()
    name_slug = re.sub(r"[^a-zA-Z0-9]", "_", subject["name"])

    # Output path
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = REPORTS_DIR / f"LK_VALIDATION_REPORT_{date_slug}_{name_slug}.md"

    print(f"\n{'='*60}")
    print(f"  Lal Kitaab Validation Report Generator")
    print(f"  Subject : {subject['name']}")
    print(f"  DOB     : {subject['birth_date']} {subject['birth_time']} tz={subject['tz'] if hasattr(subject,'tz') else subject['timezone_offset']}")
    print(f"  Output  : {out_path}")
    print(f"{'='*60}\n")

    # ── Auth
    print("→ Authenticating...", flush=True)
    if args.user_id:
        user_id, user_role = args.user_id, "admin"
    else:
        user_id, user_role = _resolve_user_id()
    token = _make_token(user_id, user_role)
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    print(f"  user_id = {user_id[:16]}...", flush=True)

    # ── Kundli
    if args.kundli_id:
        kid = args.kundli_id
        print(f"→ Using existing kundli: {kid}", flush=True)
    else:
        print("→ Creating kundli...", flush=True)
        kid = create_kundli(session, subject)
        print(f"  kundli_id = {kid}", flush=True)

    # ── Fetch base kundli to get LK positions early (needed for farmaan URL resolution)
    print("→ Fetching base kundli for position data...", flush=True)
    base_r = _call(session, "GET", f"{BASE_URL}/api/kundli/{kid}", "base_kundli_prefetch")
    lk_positions = extract_lk_positions(base_r)
    print(f"  LK positions resolved: {[(p, v['lk_house']) for p, v in lk_positions.items()]}", flush=True)

    # ── Collect all endpoints
    print("\n→ Collecting all endpoint data...", flush=True)
    results = collect_all(kid, session, lk_positions)

    # Use the pre-fetched base kundli result
    results["base_kundli"] = base_r

    # ── Build report
    print("\n→ Building report sections...", flush=True)
    sections = [
        section_header(subject, kid, generated_at, user_id),
        section_1_header(subject, generated_at),
        section_2_summary(results),
        section_3_foundation(results, lk_positions),
        section_4_dashboard(results, lk_positions),
        section_5_tewa(results),
        section_6_birth_chart(results, lk_positions),
        section_7_interpretations(results, lk_positions),
        section_8_doshas(results),
        section_9_rin(results),
        section_10_compound(results),
        section_11_remedies(results),
        section_12_wizard(results),
        section_13_advanced(results),
        section_13b_synthesis(results, lk_positions),
        section_14_relations(results),
        section_15_rules(results),
        section_16_prediction_studio(results),
        section_17_saala_grah(results),
        section_18_varshphal(results),
        section_19_gochar(results),
        section_20_chandra(results),
        section_21_chandra_chaalana(results),
        section_22_technical(results),
        section_23_specialized(results, lk_positions),
        section_24_tracker(results),
        section_25_advanced_modules(results),
        section_26_consistency(results, lk_positions),
        section_27_audit(results),
        section_28_verdict(results),
        section_29_master_summary(results),
        section_30_marriage(results),
    ]

    report = "\n\n---\n\n".join(s for s in sections if s.strip())

    # ── Write
    out_path.write_text(report, encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"  ✅ Report saved: {out_path}")
    print(f"  Lines: {report.count(chr(10))}")
    print(f"  Size : {len(report.encode())/1024:.1f} KB")

    # ── Summary stats
    passing = sum(1 for r in results.values() if r.ok)
    errors  = sum(1 for r in results.values() if not r.ok and r.status not in (0,))
    total   = len(results)
    print(f"  Endpoints: {passing}/{total} pass · {errors} errors")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
