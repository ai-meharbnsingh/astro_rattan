#!/usr/bin/env python3
"""
AstroRattan API Validation CLI
================================
Tests every authenticated endpoint using feature-specific test accounts.

Accounts (password: Astrorattan@2026):
  kundli@astrorattan.com      → Kundli endpoints
  lalkitab@astrorattan.com    → Lal Kitab endpoints
  numerology@astrorattan.com  → Numerology endpoints
  panchang@astrorattan.com    → Panchang endpoints
  vastu@astrorattan.com       → Vastu endpoints
  horoscope@astrorattan.com   → Horoscope endpoints

Usage:
  python3 scripts/validate_api.py                  # run all
  python3 scripts/validate_api.py kundli           # run only kundli suite
  python3 scripts/validate_api.py kundli lalkitab  # run specific suites
"""

import sys
import json
import datetime
import requests

BASE = "http://localhost:8000"
PASSWORD = "Astrorattan@2026"

TEST_BIRTH = {
    "person_name": "Meharban Singh",
    "birth_date": "1985-08-23",
    "birth_time": "23:15:00",
    "birth_place": "Delhi, India",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone_offset": 5.5,
    "gender": "male",
}

# ─────────────────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────────────────

def login(email: str) -> str:
    """Login and return JWT token. Raises on failure."""
    r = requests.post(f"{BASE}/api/auth/login", json={"email": email, "password": PASSWORD}, timeout=10)
    if r.status_code != 200:
        raise RuntimeError(f"Login failed for {email}: {r.status_code} — {r.text[:200]}")
    return r.json()["token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────────────────
# RESULT TRACKING
# ─────────────────────────────────────────────────────────

results = []

def check(label: str, r: requests.Response, expect_keys: list = None) -> dict:
    ok = r.status_code in (200, 201)
    data = {}
    try:
        data = r.json()
    except Exception:
        pass
    key_ok = True
    if ok and expect_keys:
        key_ok = all(k in data for k in expect_keys)
        ok = ok and key_ok
    entry = {
        "label": label,
        "status": r.status_code,
        "pass": ok,
        "keys_found": list(data.keys()) if isinstance(data, dict) else "[]",
        "missing_keys": [k for k in (expect_keys or []) if k not in data] if isinstance(data, dict) else [],
    }
    results.append(entry)
    marker = "✓" if ok else "✗"
    print(f"  {marker} [{r.status_code}] {label}")
    if not ok and data:
        err = data.get("detail") or data.get("error") or str(data)[:120]
        print(f"       → {err}")
    return data


# ─────────────────────────────────────────────────────────
# KUNDLI SUITE
# ─────────────────────────────────────────────────────────

def run_kundli():
    print("\n── KUNDLI (kundli@astrorattan.com) ────────────────────")
    token = login("kundli@astrorattan.com")
    H = auth_headers(token)

    # Generate kundli
    r = requests.post(f"{BASE}/api/kundli/generate", json=TEST_BIRTH, headers=H, timeout=30)
    gen = check("POST /api/kundli/generate", r, ["id"])
    kid = gen.get("id") or gen.get("kundli_id")
    if not kid:
        print("  ✗ Cannot get kundli_id — skipping sub-endpoints")
        return

    endpoints = [
        # Core chart
        ("GET",  f"/api/kundli/{kid}",                       None,              ["chart_data"]),
        # Dasha
        ("GET",  f"/api/kundli/{kid}/dasha",                 None,              ["mahadasha_periods"]),
        ("POST", f"/api/kundli/{kid}/extended-dasha",        {},                None),
        ("GET",  f"/api/kundli/{kid}/dasha-phala",           None,              None),
        ("GET",  f"/api/kundli/{kid}/sookshma-prana",        None,              None),
        ("GET",  f"/api/kundli/{kid}/yogini-dasha",          None,              None),
        ("GET",  f"/api/kundli/{kid}/kalachakra-dasha",      None,              None),
        ("GET",  f"/api/kundli/{kid}/ashtottari-dasha",      None,              None),
        ("GET",  f"/api/kundli/{kid}/tara-dasha",            None,              None),
        # Doshas
        ("POST", f"/api/kundli/{kid}/dosha",                 {},                None),
        ("POST", f"/api/kundli/{kid}/yogas-doshas",          {},                None),
        ("GET",  f"/api/kundli/{kid}/lifelong-sadesati",     None,              None),
        # Charts
        ("GET",  f"/api/kundli/{kid}/divisional-charts",     None,              None),
        ("POST", f"/api/kundli/{kid}/divisional",            {"chart": "D9"},   None),
        ("GET",  f"/api/kundli/{kid}/d108-analysis",         None,              ["moksha_potential"]),
        ("GET",  f"/api/kundli/{kid}/sarvatobhadra",         None,              None),
        # Strength
        ("POST", f"/api/kundli/{kid}/ashtakvarga",           {},                None),
        ("GET",  f"/api/kundli/{kid}/ashtakvarga-phala",     None,              None),
        ("POST", f"/api/kundli/{kid}/shadbala",              {},                None),
        ("GET",  f"/api/kundli/{kid}/sodashvarga",           None,              None),
        # Bhava & interpretation
        ("GET",  f"/api/kundli/{kid}/bhava-phala",           None,              None),
        ("GET",  f"/api/kundli/{kid}/bhava-vichara",         None,              None),
        ("GET",  f"/api/kundli/{kid}/avakhada",              None,              None),
        ("GET",  f"/api/kundli/{kid}/planet-properties",     None,              None),
        ("GET",  f"/api/kundli/{kid}/panchadha-maitri",      None,              None),
        ("GET",  f"/api/kundli/{kid}/graha-sambandha",       None,              None),
        ("GET",  f"/api/kundli/{kid}/nadi-analysis",         None,              None),
        # Aspects & conjunctions
        ("GET",  f"/api/kundli/{kid}/aspects",               None,              None),
        ("GET",  f"/api/kundli/{kid}/western-aspects",       None,              None),
        ("GET",  f"/api/kundli/{kid}/conjunctions",          None,              None),
        # Transits
        ("POST", f"/api/kundli/{kid}/transits",              {},                None),
        ("POST", f"/api/kundli/{kid}/transit-forecast",      {},                None),
        ("GET",  f"/api/kundli/{kid}/transit-interpretations",None,             None),
        ("GET",  f"/api/kundli/{kid}/transit-lucky",         None,              None),
        ("GET",  f"/api/kundli/{kid}/gochara-vedha",         None,              None),
        ("GET",  f"/api/kundli/{kid}/retrograde-stations",   None,              None),
        # Varshphal
        ("POST", f"/api/kundli/{kid}/varshphal",             {"year": 2026},    None),
        # Longevity & health
        ("GET",  f"/api/kundli/{kid}/ayu-classification",    None,              None),
        ("GET",  f"/api/kundli/{kid}/lifespan",              None,              None),
        ("GET",  f"/api/kundli/{kid}/longevity-indicators",  None,              None),
        ("GET",  f"/api/kundli/{kid}/pindayu",               None,              None),
        ("GET",  f"/api/kundli/{kid}/roga-analysis",         None,              None),
        # Jaimini & KP
        ("GET",  f"/api/kundli/{kid}/jaimini",               None,              None),
        ("POST", f"/api/kundli/{kid}/kp-analysis",           {},                None),
        # Upagrahas
        ("GET",  f"/api/kundli/{kid}/upagrahas",             None,              None),
        # Yoga
        ("GET",  f"/api/kundli/{kid}/raja-yogas",            None,              None),
        ("GET",  f"/api/kundli/{kid}/maha-yogas",            None,              None),
        # Specialized
        ("GET",  f"/api/kundli/{kid}/pravrajya",             None,              None),
        ("GET",  f"/api/kundli/{kid}/apatya",                None,              None),
        ("GET",  f"/api/kundli/{kid}/vritti",                None,              None),
        ("GET",  f"/api/kundli/{kid}/janma-predictions",     None,              None),
        ("GET",  f"/api/kundli/{kid}/navamsha-profession",   None,              None),
        ("GET",  f"/api/kundli/{kid}/family-timing",         None,              None),
        ("GET",  f"/api/kundli/{kid}/family-demise-timing",  None,              None),
        ("GET",  f"/api/kundli/{kid}/dasha-timing-rule",     None,              None),
    ]

    for method, path, body, keys in endpoints:
        url = f"{BASE}{path}"
        try:
            if method == "POST":
                r = requests.post(url, json=body or {}, headers=H, timeout=30)
            else:
                r = requests.get(url, headers=H, timeout=30)
            check(f"{method} {path}", r, keys)
        except Exception as e:
            results.append({"label": f"{method} {path}", "status": 0, "pass": False, "keys_found": [], "missing_keys": [], "error": str(e)})
            print(f"  ✗ [ERR] {method} {path} → {e}")


# ─────────────────────────────────────────────────────────
# LAL KITAB SUITE
# ─────────────────────────────────────────────────────────

def run_lalkitab():
    print("\n── LAL KITAB (lalkitab@astrorattan.com) ───────────────")
    token = login("lalkitab@astrorattan.com")
    H = auth_headers(token)

    # Generate a kundli first (LK endpoints hang off kundli_id)
    r = requests.post(f"{BASE}/api/kundli/generate", json=TEST_BIRTH, headers=H, timeout=30)
    gen = check("POST /api/kundli/generate (for LK)", r, ["id"])
    kid = gen.get("id") or gen.get("kundli_id")

    lk_get = [
        "/api/lalkitab/chandra",
        "/api/lalkitab/gochar",
        "/api/lalkitab/palm/zones",
    ]
    for path in lk_get:
        try:
            r = requests.get(f"{BASE}{path}", headers=H, timeout=20)
            check(f"GET {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] GET {path} → {e}")

    if kid:
        kid_endpoints = [
            f"/api/lalkitab/nishaniyan/{kid}",
            f"/api/lalkitab/rin/{kid}",
            f"/api/lalkitab/advanced/{kid}",
            f"/api/lalkitab/chandra-kundali/{kid}",
            f"/api/lalkitab/milestones/{kid}",
            f"/api/lalkitab/technical/{kid}",
            f"/api/lalkitab/sacrifice/{kid}",
            f"/api/lalkitab/forbidden/{kid}",
            f"/api/lalkitab/family/{kid}",
            f"/api/lalkitab/vastu/{kid}",
            f"/api/lalkitab/seven-year-cycle/{kid}",
            f"/api/lalkitab/rin-active/{kid}",
            f"/api/lalkitab/predictions/marriage/{kid}",
            f"/api/lalkitab/predictions/career/{kid}",
            f"/api/lalkitab/predictions/health/{kid}",
            f"/api/lalkitab/predictions/wealth/{kid}",
            f"/api/lalkitab/remedies/master/{kid}",
            f"/api/lalkitab/remedies/enriched/{kid}",
        ]
        for path in kid_endpoints:
            try:
                r = requests.get(f"{BASE}{path}", headers=H, timeout=20)
                check(f"GET {path}", r)
            except Exception as e:
                print(f"  ✗ [ERR] GET {path} → {e}")

    # POST endpoints
    lk_post = [
        ("/api/lalkitab/lk-analysis",       {"kundli_id": kid}),
        ("/api/lalkitab/lk-interpretations", {"kundli_id": kid}),
        ("/api/lalkitab/lk-validated-remedies", {"kundli_id": kid}),
    ]
    for path, body in lk_post:
        try:
            r = requests.post(f"{BASE}{path}", json=body, headers=H, timeout=20)
            check(f"POST {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] POST {path} → {e}")


# ─────────────────────────────────────────────────────────
# NUMEROLOGY SUITE
# ─────────────────────────────────────────────────────────

def run_numerology():
    print("\n── NUMEROLOGY (numerology@astrorattan.com) ─────────────")
    token = login("numerology@astrorattan.com")
    H = auth_headers(token)

    payload = {"name": "Meharban Singh", "birth_date": "1985-08-23"}
    endpoints = [
        ("POST", "/api/numerology/calculate", payload),
        ("POST", "/api/numerology/forecast",  {**payload, "year": 2026}),
        ("POST", "/api/numerology/name",      {"full_name": "Meharban Singh", "birth_date": "1985-08-23"}),
        ("POST", "/api/numerology/mobile",    {"phone_number": "9999999999", "birth_date": "1985-08-23"}),
    ]
    for method, path, body in endpoints:
        try:
            url = f"{BASE}{path}"
            r = requests.post(url, json=body, headers=H, timeout=20) if method == "POST" else requests.get(url, headers=H, timeout=20)
            check(f"{method} {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] {method} {path} → {e}")


# ─────────────────────────────────────────────────────────
# PANCHANG SUITE
# ─────────────────────────────────────────────────────────

def run_panchang():
    print("\n── PANCHANG (panchang@astrorattan.com) ─────────────────")
    token = login("panchang@astrorattan.com")
    H = auth_headers(token)

    today = datetime.date.today().isoformat()
    q = f"date={today}&lat=28.6139&lon=77.2090&tz=5.5"
    endpoints = [
        ("GET",  f"/api/panchang?{q}",                   None),
        ("GET",  f"/api/panchang/month?year={datetime.date.today().year}&month={datetime.date.today().month}&lat=28.6139&lon=77.2090&tz=5.5", None),
        ("GET",  f"/api/panchang/muhurat?muhurat_type=marriage&year={datetime.date.today().year}&month={datetime.date.today().month}", None),
        ("GET",  f"/api/panchang/sankranti?year=2026",   None),
        ("GET",  f"/api/panchang/choghadiya?{q}",        None),
        ("GET",  "/api/festivals?lat=28.6139&lon=77.2090&tz=5.5", None),
    ]
    for method, path, body in endpoints:
        try:
            url = f"{BASE}{path}"
            r = requests.post(url, json=body, headers=H, timeout=20) if method == "POST" else requests.get(url, headers=H, timeout=20)
            check(f"{method} {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] {method} {path} → {e}")


# ─────────────────────────────────────────────────────────
# VASTU SUITE
# ─────────────────────────────────────────────────────────

def run_vastu():
    print("\n── VASTU (vastu@astrorattan.com) ────────────────────────")
    token = login("vastu@astrorattan.com")
    H = auth_headers(token)

    endpoints = [
        ("POST", "/api/vastu/analyze",       {"building_type": "residential", "facing": "North"}),
        ("POST", "/api/vastu/remedies",      {"problems": ["health", "wealth"]}),
        ("GET",  "/api/vastu/mandala",       None),
        ("GET",  "/api/vastu/entrance?direction=North", None),
        ("GET",  "/api/vastu/room-placement",None),
    ]
    for method, path, body in endpoints:
        try:
            url = f"{BASE}{path}"
            r = requests.post(url, json=body, headers=H, timeout=20) if method == "POST" else requests.get(url, headers=H, timeout=20)
            check(f"{method} {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] {method} {path} → {e}")


# ─────────────────────────────────────────────────────────
# HOROSCOPE SUITE
# ─────────────────────────────────────────────────────────

def run_horoscope():
    print("\n── HOROSCOPE (horoscope@astrorattan.com) ───────────────")
    token = login("horoscope@astrorattan.com")
    H = auth_headers(token)

    today = datetime.date.today().isoformat()
    q_sign = "sign=Taurus"
    endpoints = [
        ("GET",  f"/api/horoscope/daily?{q_sign}&date={today}",  None),
        ("GET",  f"/api/horoscope/weekly?{q_sign}&date={today}", None),
        ("GET",  f"/api/horoscope/monthly?{q_sign}&month={datetime.date.today().month}&year={datetime.date.today().year}", None),
        ("GET",  f"/api/horoscope/yearly?{q_sign}&year=2026",    None),
        ("GET",  "/api/horoscope/all",                           None),
        ("GET",  f"/api/horoscope/tomorrow?{q_sign}",            None),
        ("GET",  f"/api/horoscope/transits?{q_sign}",            None),
    ]
    for method, path, body in endpoints:
        try:
            url = f"{BASE}{path}"
            r = requests.post(url, json=body, headers=H, timeout=20) if method == "POST" else requests.get(url, headers=H, timeout=20)
            check(f"{method} {path}", r)
        except Exception as e:
            print(f"  ✗ [ERR] {method} {path} → {e}")


# ─────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────

def print_summary():
    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    print(f"\n{'═'*55}")
    print(f"SUMMARY: {passed}/{total} passed | {failed} failed")
    print(f"{'═'*55}")
    if failed:
        print("\nFailed endpoints:")
        for r in results:
            if not r["pass"]:
                missing = f" | missing keys: {r['missing_keys']}" if r.get("missing_keys") else ""
                print(f"  ✗ [{r['status']}] {r['label']}{missing}")


# ─────────────────────────────────────────────────────────
# SUITE REGISTRY
# ─────────────────────────────────────────────────────────

SUITES = {
    "kundli":     run_kundli,
    "lalkitab":   run_lalkitab,
    "numerology": run_numerology,
    "panchang":   run_panchang,
    "vastu":      run_vastu,
    "horoscope":  run_horoscope,
}

if __name__ == "__main__":
    args = sys.argv[1:]
    selected = args if args else list(SUITES.keys())
    print(f"AstroRattan API Validator — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running suites: {', '.join(selected)}")
    print(f"Base URL: {BASE}")

    for name in selected:
        if name not in SUITES:
            print(f"Unknown suite '{name}'. Available: {', '.join(SUITES)}")
            continue
        try:
            SUITES[name]()
        except RuntimeError as e:
            print(f"  ✗ AUTH ERROR: {e}")

    print_summary()
