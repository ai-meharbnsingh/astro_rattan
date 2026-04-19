"""KP Astrology and Lal Kitab Remedies routes."""
import json
import logging

logger = logging.getLogger(__name__)
from datetime import date as _date, datetime as _datetime
from typing import Any, Optional

import httpx

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.astro_engine import calculate_planet_positions
from app.database import get_db
from app.kp_engine import calculate_kp_cuspal, calculate_kp_horary, get_horary_prediction
from app.lalkitab_engine import get_remedies, REMEDIES_BY_HOUSE
from app.lalkitab_remedy_matrix import ABHIMANTRIT_ITEMS
from app.models import KPHoraryRequest, KPHoraryPredictRequest, PrashnaQuickRequest
from app.lalkitab_advanced import (
    calculate_masnui_planets,
    calculate_karmic_debts,
    calculate_karmic_debts_with_hora,
    identify_teva_type,
    get_prohibitions,
    calculate_lk_aspects,
    calculate_sleeping_status,
    calculate_kayam_grah,
    calculate_bunyaad,
    calculate_takkar,
    calculate_enemy_presence,
    calculate_dhoka,
    calculate_achanak_chot,
    enrich_debts_active_passive,
)
from app.lalkitab_interpretations import (
    get_all_interpretations_for_chart,
    get_lk_validated_remedies,
)
from app.lalkitab_translations import PLANET_NAMES_HI

router = APIRouter()

# ─────────────────────────────────────────────────────────────
# Sign → LK house mapping (sidereal: Aries=1 … Pisces=12)
# ─────────────────────────────────────────────────────────────
_SIGN_TO_LK_HOUSE = {
    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
    'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
    'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12,
}

_PLANET_SPEED = {
    'Sun': 'fast', 'Moon': 'fast', 'Mercury': 'fast', 'Venus': 'fast',
    'Mars': 'medium', 'Jupiter': 'slow', 'Saturn': 'slow',
    'Rahu': 'slow', 'Ketu': 'slow',
}

_KNOWN_PLANETS = set(_PLANET_SPEED.keys())

# Static city → (lat, lon, tz_offset_hours) for Hora geocoding fallback.
# Covers 100+ major Indian cities so charts stored without coordinates still
# get a real sunrise and correct Hora lord instead of a silent skip.
_INDIA_CITY_COORDS: dict[str, tuple[float, float, float]] = {
    # North India
    "delhi": (28.6139, 77.2090, 5.5),
    "new delhi": (28.6139, 77.2090, 5.5),
    "noida": (28.5355, 77.3910, 5.5),
    "gurgaon": (28.4595, 77.0266, 5.5),
    "gurugram": (28.4595, 77.0266, 5.5),
    "faridabad": (28.4089, 77.3178, 5.5),
    "ghaziabad": (28.6692, 77.4538, 5.5),
    "agra": (27.1767, 78.0081, 5.5),
    "lucknow": (26.8467, 80.9462, 5.5),
    "kanpur": (26.4499, 80.3319, 5.5),
    "varanasi": (25.3176, 82.9739, 5.5),
    "allahabad": (25.4358, 81.8463, 5.5),
    "prayagraj": (25.4358, 81.8463, 5.5),
    "meerut": (28.9845, 77.7064, 5.5),
    "mathura": (27.4924, 77.6737, 5.5),
    "bareilly": (28.3670, 79.4304, 5.5),
    "aligarh": (27.8974, 78.0880, 5.5),
    "moradabad": (28.8389, 78.7768, 5.5),
    "gorakhpur": (26.7606, 83.3732, 5.5),
    "jhansi": (25.4484, 78.5685, 5.5),
    # Rajasthan
    "jaipur": (26.9124, 75.7873, 5.5),
    "jodhpur": (26.2389, 73.0243, 5.5),
    "udaipur": (24.5854, 73.7125, 5.5),
    "kota": (25.2138, 75.8648, 5.5),
    "ajmer": (26.4499, 74.6399, 5.5),
    "bikaner": (28.0229, 73.3119, 5.5),
    "alwar": (27.5530, 76.6346, 5.5),
    # Punjab / Haryana / HP / J&K
    "chandigarh": (30.7333, 76.7794, 5.5),
    "amritsar": (31.6340, 74.8723, 5.5),
    "ludhiana": (30.9010, 75.8573, 5.5),
    "jalandhar": (31.3260, 75.5762, 5.5),
    "patiala": (30.3398, 76.3869, 5.5),
    "shimla": (31.1048, 77.1734, 5.5),
    "dharamsala": (32.2190, 76.3234, 5.5),
    "srinagar": (34.0837, 74.7973, 5.5),
    "jammu": (32.7266, 74.8570, 5.5),
    # Uttarakhand
    "dehradun": (30.3165, 78.0322, 5.5),
    "haridwar": (29.9457, 78.1642, 5.5),
    "rishikesh": (30.0869, 78.2676, 5.5),
    "nainital": (29.3802, 79.4636, 5.5),
    # Gujarat
    "ahmedabad": (23.0225, 72.5714, 5.5),
    "surat": (21.1702, 72.8311, 5.5),
    "vadodara": (22.3072, 73.1812, 5.5),
    "baroda": (22.3072, 73.1812, 5.5),
    "rajkot": (22.3039, 70.8022, 5.5),
    "bhavnagar": (21.7645, 72.1519, 5.5),
    "gandhinagar": (23.2156, 72.6369, 5.5),
    "jamnagar": (22.4707, 70.0577, 5.5),
    # Maharashtra
    "mumbai": (19.0760, 72.8777, 5.5),
    "bombay": (19.0760, 72.8777, 5.5),
    "pune": (18.5204, 73.8567, 5.5),
    "nagpur": (21.1458, 79.0882, 5.5),
    "nashik": (19.9975, 73.7898, 5.5),
    "aurangabad": (19.8762, 75.3433, 5.5),
    "solapur": (17.6805, 75.9064, 5.5),
    "kolhapur": (16.7050, 74.2433, 5.5),
    "thane": (19.2183, 72.9781, 5.5),
    "navi mumbai": (19.0330, 73.0297, 5.5),
    # Madhya Pradesh
    "bhopal": (23.2599, 77.4126, 5.5),
    "indore": (22.7196, 75.8577, 5.5),
    "gwalior": (26.2183, 78.1828, 5.5),
    "jabalpur": (23.1815, 79.9864, 5.5),
    "ujjain": (23.1765, 75.7885, 5.5),
    # Bihar / Jharkhand
    "patna": (25.5941, 85.1376, 5.5),
    "gaya": (24.7914, 85.0002, 5.5),
    "muzaffarpur": (26.1209, 85.3647, 5.5),
    "ranchi": (23.3441, 85.3096, 5.5),
    "jamshedpur": (22.8046, 86.2029, 5.5),
    "dhanbad": (23.7957, 86.4304, 5.5),
    # West Bengal / Odisha
    "kolkata": (22.5726, 88.3639, 5.5),
    "calcutta": (22.5726, 88.3639, 5.5),
    "howrah": (22.5958, 88.2636, 5.5),
    "durgapur": (23.5204, 87.3119, 5.5),
    "bhubaneswar": (20.2961, 85.8245, 5.5),
    "cuttack": (20.4625, 85.8830, 5.5),
    # Northeast
    "guwahati": (26.1445, 91.7362, 5.5),
    "silchar": (24.8333, 92.7789, 5.5),
    "shillong": (25.5788, 91.8933, 5.5),
    # South — Tamil Nadu
    "chennai": (13.0827, 80.2707, 5.5),
    "madras": (13.0827, 80.2707, 5.5),
    "coimbatore": (11.0168, 76.9558, 5.5),
    "madurai": (9.9252, 78.1198, 5.5),
    "tiruchirappalli": (10.7905, 78.7047, 5.5),
    "trichy": (10.7905, 78.7047, 5.5),
    "salem": (11.6643, 78.1460, 5.5),
    "tirunelveli": (8.7139, 77.7567, 5.5),
    # Karnataka
    "bengaluru": (12.9716, 77.5946, 5.5),
    "bangalore": (12.9716, 77.5946, 5.5),
    "mysuru": (12.2958, 76.6394, 5.5),
    "mysore": (12.2958, 76.6394, 5.5),
    "hubli": (15.3647, 75.1240, 5.5),
    "mangaluru": (12.9141, 74.8560, 5.5),
    "mangalore": (12.9141, 74.8560, 5.5),
    "belagavi": (15.8497, 74.4977, 5.5),
    "belgaum": (15.8497, 74.4977, 5.5),
    # Andhra Pradesh / Telangana
    "hyderabad": (17.3850, 78.4867, 5.5),
    "secunderabad": (17.4399, 78.4983, 5.5),
    "visakhapatnam": (17.6868, 83.2185, 5.5),
    "vizag": (17.6868, 83.2185, 5.5),
    "vijayawada": (16.5062, 80.6480, 5.5),
    "warangal": (17.9689, 79.5941, 5.5),
    "guntur": (16.3008, 80.4428, 5.5),
    # Kerala
    "thiruvananthapuram": (8.5241, 76.9366, 5.5),
    "trivandrum": (8.5241, 76.9366, 5.5),
    "kochi": (9.9312, 76.2673, 5.5),
    "cochin": (9.9312, 76.2673, 5.5),
    "kozhikode": (11.2588, 75.7804, 5.5),
    "calicut": (11.2588, 75.7804, 5.5),
    "thrissur": (10.5276, 76.2144, 5.5),
    # Chhattisgarh
    "raipur": (21.2514, 81.6296, 5.5),
    "bilaspur": (22.0796, 82.1391, 5.5),
    # Goa
    "panaji": (15.4909, 73.8278, 5.5),
    "goa": (15.2993, 74.1240, 5.5),
    # International (common diaspora)
    "dubai": (25.2048, 55.2708, 4.0),
    "abu dhabi": (24.4539, 54.3773, 4.0),
    "london": (51.5074, -0.1278, 0.0),
    "new york": (40.7128, -74.0060, -5.0),
    "toronto": (43.6532, -79.3832, -5.0),
    "singapore": (1.3521, 103.8198, 8.0),
    "kuala lumpur": (3.1390, 101.6869, 8.0),
}


def _lookup_city_coords(birth_place: str | None) -> tuple[float, float, float] | None:
    """Return (lat, lon, tz_offset) from _INDIA_CITY_COORDS for birth_place string."""
    if not birth_place:
        return None
    key = birth_place.strip().lower()
    if key in _INDIA_CITY_COORDS:
        return _INDIA_CITY_COORDS[key]
    # Try partial match: first word, then any contained city name
    for city, coords in _INDIA_CITY_COORDS.items():
        if city in key:
            return coords
    return None


def _derive_lk_house(info: dict) -> int:
    """
    Lal Kitab uses FIXED houses: Aries=H1, Taurus=H2 ... Pisces=H12
    regardless of ascendant. Never use chart_data whole-sign houses here.
    """
    if isinstance(info, dict):
        sign = info.get("sign", "")
        return _SIGN_TO_LK_HOUSE.get(sign, 0)
    return 0


# Status tokens that belong to the Vedic/Parashari overlay but are NOT
# part of Lal Kitab 1952. `_lk_status_string()` filters them out so LK
# surfaces never display "Combust" / "Sandhi" etc. The raw astro_engine
# `status` string is preserved on `info` for any future Vedic module.
_VEDIC_ONLY_TOKENS = {"Combust", "Sandhi"}


def _lk_status_string(info: dict) -> str:
    """
    Return the planet status string as used in Lal Kitab output.

    Strips Vedic-only tokens (Combust, Sandhi) while keeping LK-relevant
    tokens (Exalted, Debilitated, Own Sign, Retrograde, Vargottama).
    """
    raw = (info or {}).get("status", "") if isinstance(info, dict) else ""
    if not raw:
        return ""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    lk_parts = [p for p in parts if p not in _VEDIC_ONLY_TOKENS]
    return ", ".join(lk_parts)


@router.post("/api/kp/cuspal")
def kp_cuspal(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Calculate KP cuspal chart with star lords, sub lords, and significators.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_longitudes and house_cusps from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    # Recalculate chart with KP (Krishnamurti) ayanamsa for accurate KP positions
    chart_data = calculate_planet_positions(
        birth_date=row["birth_date"],
        birth_time=row["birth_time"],
        latitude=row.get("latitude", 0.0),
        longitude=row.get("longitude", 0.0),
        tz_offset=row.get("timezone_offset", 0.0),
        ayanamsa="kp",
    )

    # Extract planet longitudes from chart_data
    planet_longitudes = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        planet_longitudes[planet_name] = info.get("longitude", 0.0)

    # Extract house cusps from chart_data
    house_cusps = chart_data.get("placidus_cusps", chart_data.get("house_cusps", []))
    if not house_cusps or len(house_cusps) != 12:
        # Generate default cusps from ascendant if house_cusps not stored
        asc_lon = chart_data.get("ascendant", {}).get("longitude", 0.0)
        house_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]

    if not planet_longitudes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet longitudes",
        )

    try:
        result = calculate_kp_cuspal(planet_longitudes, house_cusps)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    # Contract response: {cuspal_chart, significators}
    return {
        "cuspal_chart": {
            "cusps": result.get("cusps", []),
            "planets": result.get("planets", {}),
        },
        "significators": result.get("significators", {}),
    }


@router.post("/api/lalkitab/remedies")
def lalkitab_remedies(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Get Lal Kitab remedies for weak or afflicted planets.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_positions from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    chart_data = json.loads(row["chart_data"])

    # Extract planet positions as {planet: sign}. Skip planets without a valid sign
    # rather than silently defaulting to "Aries" (which would fabricate remedies).
    planet_positions = {}
    missing_sign_planets = []
    for planet_name, info in chart_data.get("planets", {}).items():
        sign = info.get("sign")
        if isinstance(sign, str) and sign in _SIGN_TO_LK_HOUSE:
            planet_positions[planet_name] = sign
        else:
            missing_sign_planets.append(planet_name)

    if not planet_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions with valid signs",
        )

    try:
        # Pass chart_data so the enriched strength model runs (house +
        # combustion + retrograde), not just sign-only dignity.
        res = get_remedies(planet_positions, chart_data=chart_data)
        # Transform into flat list for frontend with translations.
        # Look up the authentic Hindi (Devanagari) version from REMEDIES_BY_HOUSE
        # using the planet + lk_house. If no match is found we emit remedy_hi=None
        # rather than duplicating English — duplication would be a fraud pattern.
        remedies_list = []
        for planet, info in res.items():
            if not info.get("remedies"):
                continue
            lk_house = info.get("lk_house", 0)
            house_remedy = REMEDIES_BY_HOUSE.get(planet, {}).get(lk_house, {})
            en_from_house = house_remedy.get("en")
            hi_from_house = house_remedy.get("hi")
            for r_text in info["remedies"]:
                # Match the backward-compat English string against the house remedy.
                # get_remedies() builds compat_remedies from house_remedy["en"],
                # so these should be equal — but fall back safely.
                if en_from_house and r_text == en_from_house and hi_from_house:
                    remedy_hi_val = hi_from_house
                elif hi_from_house:
                    remedy_hi_val = hi_from_house
                else:
                    # No authentic Hindi available — do NOT duplicate English.
                    remedy_hi_val = None
                remedies_list.append({
                    "planet_en": planet,
                    "planet_hi": PLANET_NAMES_HI.get(planet, planet),
                    "remedy_en": r_text,
                    "remedy_hi": remedy_hi_val,
                })
        return {"remedies": remedies_list}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )


@router.get("/api/lalkitab/remedies/enriched/{kundli_id}")
def get_enriched_remedies(kundli_id: str, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Return enriched remedies for ALL 9 planets: problem / reason / remedy / how_it_works.
    Always returns all planets (not just weak ones) so the UI can show education for every house.
    """
    row = db.execute(
        "SELECT chart_data, birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    # Only include planets with valid signs — do NOT silently default to Aries.
    planet_positions = {
        p: info.get("sign")
        for p, info in chart_data.get("planets", {}).items()
        if isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
    }
    if not planet_positions:
        raise HTTPException(status_code=400, detail="No planet positions with valid signs in chart")

    # Pass chart_data so enriched remedies use the full strength model
    # (house + combustion + retrograde), not sign-only dignity.
    res = get_remedies(planet_positions, chart_data=chart_data)
    enriched = []
    for planet, info in res.items():
        r = info["remedy"]
        enriched.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "sign": info["sign"],
            "lk_house": info["lk_house"],
            "dignity": info["dignity"],
            "strength": info["strength"],
            "has_remedy": info["has_remedy"],
            "urgency": r.get("urgency", "low"),
            "material": r.get("material", ""),
            "day": r.get("day", ""),
            # Remedy action
            "remedy_en": r.get("en", ""),
            "remedy_hi": r.get("hi", ""),
            # Education fields
            "problem_en": r.get("problem_en", ""),
            "problem_hi": r.get("problem_hi", ""),
            "reason_en": r.get("reason_en", ""),
            "reason_hi": r.get("reason_hi", ""),
            "how_en": r.get("how_en", ""),
            "how_hi": r.get("how_hi", ""),
            # P0 safety layer (LK 4.08 / 4.09 / 2.12 / 4.14)
            "savdhaniyan": info.get("savdhaniyan"),
            "time_rule": info.get("time_rule"),
            "reversal_risk": info.get("reversal_risk"),
            "andhe_grah_warning": info.get("andhe_grah_warning"),
            # P2.11 — direction/colour/material matrix
            "remedy_matrix": info.get("remedy_matrix"),
            # P1.11 — tier classification (trial / remedy / good_conduct)
            "classification": r.get("classification", ""),
            "classification_en": r.get("classification_en", ""),
            "classification_hi": r.get("classification_hi", ""),
            "classification_desc_en": r.get("classification_desc_en", ""),
            "classification_desc_hi": r.get("classification_desc_hi", ""),
        })
    # Sort: weak/high urgency first, then by house number
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    enriched.sort(key=lambda x: (0 if x["has_remedy"] else 1, urgency_order.get(x["urgency"], 2), x["lk_house"]))
    return {"remedies": enriched}


#
# NOTE: Legacy endpoints `/api/lalkitab/tracker/*` intentionally removed.
# The authoritative, actively-used tracker feature is `/api/lalkitab/remedy-tracker/*`
# (see below) which supports per-remedy schedules, check-ins, and deletions.
#


# ─────────────────────────────────────────────────────────────
# Lal Kitab Chandra Chalana Protocol
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/chandra")
def get_chandra_state(kundli_id: Optional[int] = None, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Return the user's Chandra protocol state with personalized tasks when kundli_id is supplied."""
    from app.lalkitab_chandra_tasks import CHANDRA_CHAALANA_TASKS, get_personalized_tasks
    user_id = user["sub"]
    row = db.execute(
        "SELECT start_date, completed_days FROM lk_chandra_protocol WHERE user_id = %s",
        (user_id,),
    ).fetchone()
    journal = db.execute(
        "SELECT date, note FROM lk_journal_entries WHERE user_id = %s AND source = 'chandra' ORDER BY created_at DESC LIMIT 60",
        (user_id,),
    ).fetchall()

    tasks = CHANDRA_CHAALANA_TASKS
    moon_house = None
    if kundli_id:
        try:
            lk_row = db.execute(
                "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
                (kundli_id, user_id),
            ).fetchone()
            if lk_row:
                chart = json.loads(lk_row["chart_data"] or "{}")
                planets = chart.get("planets", chart.get("lalkitab_planets", []))
                for p in planets:
                    name = (p.get("name") or p.get("planet") or "").lower()
                    if name in ("moon", "chandra"):
                        moon_house = int(p.get("lk_house") or p.get("house") or 0) or None
                        break
                if moon_house:
                    tasks = get_personalized_tasks(moon_house)
        except Exception:
            pass  # fall back to universal tasks silently

    base = {
        "journal": [{"date": r["date"], "note": r["note"]} for r in journal],
        "tasks": tasks,
        "moon_house": moon_house,
    }
    if row:
        return {**base, "start_date": row["start_date"], "completed_days": json.loads(row["completed_days"] or "[]")}
    return {**base, "start_date": None, "completed_days": []}


@router.post("/api/lalkitab/chandra/start")
def start_chandra_protocol(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Start or restart the 43-day Chandra protocol. payload: {start_date}"""
    user_id = user["sub"]
    start_date = payload.get("start_date")
    if not start_date:
        raise HTTPException(status_code=400, detail="start_date required")
    row = db.execute("SELECT id FROM lk_chandra_protocol WHERE user_id = %s", (user_id,)).fetchone()
    if row:
        db.execute(
            "UPDATE lk_chandra_protocol SET start_date = %s, completed_days = '[]', updated_at = NOW() WHERE user_id = %s",
            (start_date, user_id),
        )
    else:
        db.execute(
            "INSERT INTO lk_chandra_protocol (user_id, start_date, completed_days) VALUES (%s, %s, '[]')",
            (user_id, start_date),
        )
    db.commit()
    return {"start_date": start_date, "completed_days": []}


@router.post("/api/lalkitab/chandra/mark-done")
def mark_chandra_day_done(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Mark today as done in the protocol. payload: {date}"""
    user_id = user["sub"]
    date = payload.get("date")
    if not date:
        raise HTTPException(status_code=400, detail="date required")
    row = db.execute("SELECT completed_days FROM lk_chandra_protocol WHERE user_id = %s", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Protocol not started")
    days = json.loads(row["completed_days"] or "[]")
    if date not in days:
        days.append(date)
        db.execute(
            "UPDATE lk_chandra_protocol SET completed_days = %s, updated_at = NOW() WHERE user_id = %s",
            (json.dumps(days), user_id),
        )
        db.commit()
    return {"completed_days": days}


@router.post("/api/lalkitab/chandra/journal")
def add_chandra_journal(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Add a Chandra protocol journal entry. payload: {date, note}"""
    user_id = user["sub"]
    date = payload.get("date")
    note = (payload.get("note") or "").strip()
    if not date or not note:
        raise HTTPException(status_code=400, detail="date and note required")
    db.execute(
        "INSERT INTO lk_journal_entries (user_id, source, date, note) VALUES (%s, 'chandra', %s, %s)",
        (user_id, date, note),
    )
    db.commit()
    return {"ok": True}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Gochar (Live Transit Positions)
# ─────────────────────────────────────────────────────────────

_PAKKA_GHAR_GOCHAR: dict[str, set] = {
    "Sun": {1}, "Moon": {4}, "Mars": {3, 8}, "Mercury": {3, 6},
    "Jupiter": {2, 9, 12}, "Venus": {7}, "Saturn": {7, 10},
    "Rahu": {6, 11, 12}, "Ketu": {3, 6, 12},
}

_GOCHAR_PLANET_RULES: dict[str, dict[int, dict]] = {
    "Sun": {
        1:  {"en": "Sun transiting H1 (Pakka Ghar) — vitality and authority peak. Bold self-expression and health focus. Ideal for leadership decisions.", "hi": "सूर्य गोचर भाव 1 (पक्का घर) — जीवनशक्ति और प्रभुत्व का शिखर। साहसी आत्म-अभिव्यक्ति और स्वास्थ्य पर ध्यान।", "positive": True},
        2:  {"en": "Sun transiting H2 — family wealth and speech gain authority. Financial confidence rises. Ego in family matters needs balance.", "hi": "सूर्य गोचर भाव 2 — पारिवारिक धन और वाणी में अधिकार। आर्थिक आत्मविश्वास बढ़ता है। परिवार में अहंकार पर संतुलन जरूरी।", "positive": True},
        3:  {"en": "Sun transiting H3 — courage and communication peak. Sibling bonds active. Short journeys and new initiatives succeed.", "hi": "सूर्य गोचर भाव 3 — साहस और संचार चरम पर। भाई-बहन संबंध सक्रिय। छोटी यात्राएँ और नई पहल सफल।", "positive": True},
        4:  {"en": "Sun transiting H4 — home and mother in focus. Real estate matters active. Father may be away or absorbed in career.", "hi": "सूर्य गोचर भाव 4 — घर और माता पर ध्यान। संपत्ति के मामले सक्रिय। पिता व्यस्त या दूर हो सकते हैं।", "positive": True},
        5:  {"en": "Sun transiting H5 — intelligence and creative expression peak. Pride in children. Speculation may be ego-driven — exercise caution.", "hi": "सूर्य गोचर भाव 5 — बुद्धि और रचनात्मक अभिव्यक्ति उच्च। संतान पर गर्व। सट्टे में अहंकार — सावधानी बरतें।", "positive": True},
        6:  {"en": "Sun transiting H6 — enemies are defeated. Government service or authority work excels. Health concerns need attention.", "hi": "सूर्य गोचर भाव 6 — शत्रुओं पर विजय। सरकारी सेवा या अधिकार-कार्य उत्कृष्ट। स्वास्थ्य पर ध्यान दें।", "positive": True},
        7:  {"en": "Sun transiting H7 — partnerships under spotlight. Ego vs. partner dynamic active. Marriage matters or legal negotiations are highlighted.", "hi": "सूर्य गोचर भाव 7 — साझेदारी में अहंकार बनाम साझेदार का द्वंद्व। विवाह और कानूनी वार्ता प्रमुख।", "positive": False},
        8:  {"en": "Sun transiting H8 — hidden matters surface. In-law tensions possible. Transformation through authority or government sources.", "hi": "सूर्य गोचर भाव 8 — छुपे मामले सामने आते हैं। ससुराल में तनाव संभव। सरकारी या अधिकार-स्रोत से परिवर्तन।", "positive": False},
        9:  {"en": "Sun transiting H9 — dharma and luck blessed. Father's guidance active. Long journeys and religious activities are favorable.", "hi": "सूर्य गोचर भाव 9 — धर्म और भाग्य का आशीर्वाद। पिता का मार्गदर्शन सक्रिय। लंबी यात्राएँ और धार्मिक कार्य शुभ।", "positive": True},
        10: {"en": "Sun transiting H10 — career peak. Recognition, authority, and leadership opportunities arise. Government favor is possible.", "hi": "सूर्य गोचर भाव 10 — करियर का शिखर। मान-सम्मान, अधिकार और नेतृत्व के अवसर। सरकारी कृपा संभव।", "positive": True},
        11: {"en": "Sun transiting H11 — gains through influential connections. Father's network or authority figures help fulfill desires.", "hi": "सूर्य गोचर भाव 11 — प्रभावशाली संपर्कों से लाभ। पिता का नेटवर्क या अधिकारी वर्ग से इच्छापूर्ति।", "positive": True},
        12: {"en": "Sun transiting H12 — expenditures on status. Possible ego battles in secret. Foreign isolation or spiritual retreat.", "hi": "सूर्य गोचर भाव 12 — प्रतिष्ठा पर खर्च। गुप्त अहंकार की लड़ाई। विदेश में एकांत या आध्यात्मिक साधना।", "positive": False},
    },
    "Moon": {
        1:  {"en": "Moon transiting H1 — emotional sensitivity peaks. Intuition-led new beginnings. Health and mind are deeply linked — rest is important.", "hi": "चंद्र गोचर भाव 1 — भावनात्मक संवेदनशीलता चरम। अंतर्ज्ञान से नई शुरुआत। स्वास्थ्य और मन जुड़े हैं — आराम जरूरी।", "positive": True},
        2:  {"en": "Moon transiting H2 — emotional attachment to family and wealth. Mother's financial matters active. Speech becomes nurturing.", "hi": "चंद्र गोचर भाव 2 — परिवार और धन से भावनात्मक लगाव। माता के आर्थिक मामले सक्रिय। वाणी में पोषण।", "positive": True},
        3:  {"en": "Moon transiting H3 — emotional communication. Sibling bonds emotionally active. Short travel based on feelings or family needs.", "hi": "चंद्र गोचर भाव 3 — भावनात्मक संवाद। भाई-बहन संबंध भावनात्मक रूप से सक्रिय। भावनात्मक या पारिवारिक जरूरत से यात्रा।", "positive": True},
        4:  {"en": "Moon transiting H4 (Pakka Ghar) — Moon at peak strength. Emotional contentment, home peace, and mother's wellbeing are highlighted.", "hi": "चंद्र गोचर भाव 4 (पक्का घर) — चंद्र की उच्च शक्ति। भावनात्मक संतोष, घर की शांति और माता का स्वास्थ्य।", "positive": True},
        5:  {"en": "Moon transiting H5 — creative and emotional intelligence rises. Children and love life active. Intuitive speculation possible.", "hi": "चंद्र गोचर भाव 5 — रचनात्मक और भावनात्मक बुद्धि उच्च। संतान और प्रेम जीवन सक्रिय। अंतर्ज्ञान से सट्टा संभव।", "positive": True},
        6:  {"en": "Moon transiting H6 — emotional health challenges. Nurturing others drains energy. Enemies may exploit emotions — stay grounded.", "hi": "चंद्र गोचर भाव 6 — भावनात्मक स्वास्थ्य चुनौतियाँ। दूसरों की देखभाल से ऊर्जा खर्च। शत्रु भावनाओं का दोहन कर सकते हैं।", "positive": False},
        7:  {"en": "Moon transiting H7 — emotional availability in partnerships. Romantic phase active. Relationships need emotional depth and expression.", "hi": "चंद्र गोचर भाव 7 — साझेदारी में भावनात्मक उपलब्धता। रोमांटिक काल। संबंधों में भावनात्मक गहराई जरूरी।", "positive": True},
        8:  {"en": "Moon transiting H8 — emotional transformation. Hidden fears or intuitions surface. In-law emotional dynamics need sensitivity.", "hi": "चंद्र गोचर भाव 8 — भावनात्मक परिवर्तन। छुपे भय या अंतर्ज्ञान सामने आते हैं। ससुराल की भावनात्मक गतिशीलता।", "positive": False},
        9:  {"en": "Moon transiting H9 — intuitive dharma. Emotional journeys to sacred places. Spiritual feelings and mother's guidance peak.", "hi": "चंद्र गोचर भाव 9 — अंतर्ज्ञानी धर्म। पवित्र स्थलों की भावनात्मक यात्राएँ। आध्यात्मिक भावनाएँ और माता का मार्गदर्शन।", "positive": True},
        10: {"en": "Moon transiting H10 — career through emotional intelligence. Public emotional presence. Nurturing leadership style is effective.", "hi": "चंद्र गोचर भाव 10 — भावनात्मक बुद्धि से करियर। सार्वजनिक भावनात्मक उपस्थिति। पोषण देने वाली नेतृत्व शैली प्रभावी।", "positive": True},
        11: {"en": "Moon transiting H11 — emotional gains and wishes fulfilled through social bonds. Mother's wishes or friends bring happiness.", "hi": "चंद्र गोचर भाव 11 — भावनात्मक लाभ और सामाजिक बंधनों से इच्छापूर्ति। माता की इच्छाएँ या मित्र खुशी लाते हैं।", "positive": True},
        12: {"en": "Moon transiting H12 — emotional withdrawal or isolation. Spiritual emotions peak. Foreign emotional connections or past-life feelings surface.", "hi": "चंद्र गोचर भाव 12 — भावनात्मक वापसी या एकांत। आध्यात्मिक भावनाएँ चरम। विदेशी भावनात्मक संपर्क या पूर्वजन्म की भावनाएँ।", "positive": False},
    },
    "Mercury": {
        1:  {"en": "Mercury transiting H1 — communication and intellect peak. Quick thinking and sharp wit. Excellent for business deals and negotiations.", "hi": "बुध गोचर भाव 1 — संवाद और बुद्धि चरम पर। त्वरित सोच और तीखी बुद्धि। व्यापार सौदों और वार्ता के लिए उत्कृष्ट।", "positive": True},
        2:  {"en": "Mercury transiting H2 — financial communication and family business discussions active. Speech brings wealth. Good for writing or teaching.", "hi": "बुध गोचर भाव 2 — आर्थिक संवाद और पारिवारिक व्यापार चर्चा सक्रिय। वाणी से धन। लेखन या अध्यापन के लिए अच्छा।", "positive": True},
        3:  {"en": "Mercury transiting H3 (Pakka Ghar) — Mercury at peak power. Ideal for contracts, writing, sibling connections, and productive short journeys.", "hi": "बुध गोचर भाव 3 (पक्का घर) — बुध की उच्चतम शक्ति। अनुबंध, लेखन, भाई-बहन संपर्क और उत्पादक यात्राओं के लिए आदर्श।", "positive": True},
        4:  {"en": "Mercury transiting H4 — home-based work and real estate communication active. Mother's educational or analytical matters highlighted.", "hi": "बुध गोचर भाव 4 — घर-आधारित कार्य और संपत्ति संवाद सक्रिय। माता के शैक्षिक या विश्लेषणात्मक मामले प्रमुख।", "positive": True},
        5:  {"en": "Mercury transiting H5 — intelligence and analytical speculation rise. Writing, teaching, and children's education matters are active.", "hi": "बुध गोचर भाव 5 — बुद्धि और विश्लेषणात्मक सट्टा उच्च। लेखन, अध्यापन और संतान की शिक्षा के मामले सक्रिय।", "positive": True},
        6:  {"en": "Mercury transiting H6 (Pakka Ghar) — analytical intelligence for defeating enemies. Health research and service excellence peak.", "hi": "बुध गोचर भाव 6 (पक्का घर) — शत्रुओं पर विजय के लिए विश्लेषणात्मक बुद्धि। स्वास्थ्य शोध और सेवा उत्कृष्टता।", "positive": True},
        7:  {"en": "Mercury transiting H7 — business partnerships and contracts highlighted. Marriage communication improves. Legal documents favorable.", "hi": "बुध गोचर भाव 7 — व्यापार साझेदारी और अनुबंध प्रमुख। वैवाहिक संवाद बेहतर। कानूनी दस्तावेज अनुकूल।", "positive": True},
        8:  {"en": "Mercury transiting H8 — research, occult communication, and tax matters active. Hidden information surfaces through analysis.", "hi": "बुध गोचर भाव 8 — शोध, गुप्त संवाद और कर मामले सक्रिय। विश्लेषण से छुपी जानकारी सामने आती है।", "positive": False},
        9:  {"en": "Mercury transiting H9 — dharma through writing and teaching. Religious texts and long-distance communication are highlighted.", "hi": "बुध गोचर भाव 9 — लेखन और अध्यापन से धर्म। धार्मिक ग्रंथ और दूरस्थ संवाद प्रमुख।", "positive": True},
        10: {"en": "Mercury transiting H10 — career through communication, media, and intelligence. Business proposals and writing bring professional gains.", "hi": "बुध गोचर भाव 10 — संचार, मीडिया और बुद्धि से करियर। व्यापार प्रस्ताव और लेखन से पेशेवर लाभ।", "positive": True},
        11: {"en": "Mercury transiting H11 — gains through networking and communication. Social media and business contacts are highly productive.", "hi": "बुध गोचर भाव 11 — नेटवर्किंग और संवाद से लाभ। सोशल मीडिया और व्यापारिक संपर्क अत्यंत उत्पादक।", "positive": True},
        12: {"en": "Mercury transiting H12 — spiritual or foreign writing active. Hidden intellectual work pays off. Communication with foreign or distant people.", "hi": "बुध गोचर भाव 12 — आध्यात्मिक या विदेशी लेखन सक्रिय। छुपा बौद्धिक कार्य फल देता है। विदेशी या दूर के लोगों से संवाद।", "positive": False},
    },
    "Jupiter": {
        1:  {"en": "Jupiter transiting H1 — wisdom, optimism, and health are elevated. New beginnings carry Jupiter's blessings. Weight gain possible.", "hi": "गुरु गोचर भाव 1 — ज्ञान, आशावाद और स्वास्थ्य ऊँचा। नई शुरुआत पर गुरु का आशीर्वाद। वजन बढ़ने की संभावना।", "positive": True},
        2:  {"en": "Jupiter transiting H2 — wealth, family, and speech are blessed. Good time for savings and family investments.", "hi": "गुरु गोचर भाव 2 — धन, परिवार और वाणी को शुभ फल। बचत और पारिवारिक निवेश का उत्तम समय।", "positive": True},
        3:  {"en": "Jupiter transiting H3 — courage and communication get Jupiter's wisdom. Sibling bonds are enriched. Writing and teaching produce results.", "hi": "गुरु गोचर भाव 3 — साहस और संचार में गुरु का ज्ञान। भाई-बहन संबंध समृद्ध। लेखन और अध्यापन फलदायक।", "positive": True},
        4:  {"en": "Jupiter transiting H4 — home, mother, and real estate blessed. Emotional peace and property gains are favored.", "hi": "गुरु गोचर भाव 4 — घर, माता और संपत्ति को शुभ फल। भावनात्मक शांति और संपत्ति लाभ।", "positive": True},
        5:  {"en": "Jupiter transiting H5 — intelligence, children, and speculation favored. Creativity and wisdom peak together.", "hi": "गुरु गोचर भाव 5 — बुद्धि, संतान और सट्टे में लाभ। रचनात्मकता और ज्ञान एक साथ उच्च।", "positive": True},
        6:  {"en": "Jupiter transiting H6 — enemies are neutralized by wisdom. Health improves through good habits. Service yields reward.", "hi": "गुरु गोचर भाव 6 — शत्रु ज्ञान से निष्क्रिय होते हैं। अच्छी आदतों से स्वास्थ्य सुधरता है। सेवा का फल मिलता है।", "positive": True},
        7:  {"en": "Jupiter transiting H7 — partnerships and marriage prospects brighten. Legal matters resolve favorably with wisdom.", "hi": "गुरु गोचर भाव 7 — साझेदारी और विवाह संभावनाएँ उज्ज्वल। ज्ञान से कानूनी मामले अनुकूल।", "positive": True},
        8:  {"en": "Jupiter transiting H8 — transformational wisdom. Research, occult knowledge, and in-law relations need careful handling.", "hi": "गुरु गोचर भाव 8 — परिवर्तनकारी ज्ञान। शोध, गुप्त विद्या और ससुराल संबंधों में सावधानी।", "positive": False},
        9:  {"en": "Jupiter transiting H9 — peak luck, dharma, and long journeys. Father's blessings and religious pursuits are highly auspicious.", "hi": "गुरु गोचर भाव 9 — भाग्य, धर्म और लंबी यात्राएँ चरम। पिता का आशीर्वाद और धार्मिक कार्य अत्यंत शुभ।", "positive": True},
        10: {"en": "Jupiter transiting H10 — career expansion and recognition. Authority and leadership roles come through wisdom and merit.", "hi": "गुरु गोचर भाव 10 — करियर विस्तार और मान्यता। ज्ञान और योग्यता से अधिकार और नेतृत्व।", "positive": True},
        11: {"en": "Jupiter transiting H11 — significant financial gains and fulfillment of desires. Elder siblings and wise friends bring support.", "hi": "गुरु गोचर भाव 11 — उल्लेखनीय आर्थिक लाभ और इच्छापूर्ति। बड़े भाई-बहन और बुद्धिमान मित्र सहयोग करते हैं।", "positive": True},
        12: {"en": "Jupiter transiting H12 — spiritual gains but material losses possible. Excellent for foreign travel, philanthropy, and moksha-seeking.", "hi": "गुरु गोचर भाव 12 — आध्यात्मिक लाभ पर भौतिक हानि संभव। विदेश यात्रा, दान और मोक्ष-साधना के लिए उत्कृष्ट।", "positive": False},
    },
    "Venus": {
        1:  {"en": "Venus transiting H1 — beauty, charm, and physical attraction increase. Artistic expression peaks. Health glows and social life brightens.", "hi": "शुक्र गोचर भाव 1 — सौंदर्य, आकर्षण और शारीरिक सुंदरता बढ़ती है। कलात्मक अभिव्यक्ति उच्च। स्वास्थ्य और सामाजिक जीवन उज्ज्वल।", "positive": True},
        2:  {"en": "Venus transiting H2 — family wealth and luxuries increase. Speech becomes charming and persuasive. Family harmony improves.", "hi": "शुक्र गोचर भाव 2 — पारिवारिक धन और विलासिता बढ़ती है। वाणी आकर्षक और प्रेरक। पारिवारिक सामंजस्य सुधरता है।", "positive": True},
        3:  {"en": "Venus transiting H3 — artistic communication and creative short journeys. Sibling bonds become harmonious. Writing, music, and arts flourish.", "hi": "शुक्र गोचर भाव 3 — कलात्मक संवाद और रचनात्मक यात्राएँ। भाई-बहन संबंध सामंजस्यपूर्ण। लेखन, संगीत और कला फलती है।", "positive": True},
        4:  {"en": "Venus transiting H4 — home is beautified. Real estate gains possible. Mother's comfort and domestic happiness increase.", "hi": "शुक्र गोचर भाव 4 — घर सुंदर होता है। संपत्ति लाभ संभव। माता का आराम और घरेलू सुख बढ़ता है।", "positive": True},
        5:  {"en": "Venus transiting H5 — creative arts, romance, and intelligent speculation all peak. Children bring joy. Love life is vibrant.", "hi": "शुक्र गोचर भाव 5 — रचनात्मक कला, प्रेम और बुद्धिमान सट्टा सभी उच्च। संतान आनंद लाती है। प्रेम जीवन जीवंत।", "positive": True},
        6:  {"en": "Venus transiting H6 — enemies dissolve through charm and grace. Health matters resolve gently. Service work brings appreciation.", "hi": "शुक्र गोचर भाव 6 — आकर्षण और शालीनता से शत्रु घुलते हैं। स्वास्थ्य मामले सहजता से सुलझते हैं। सेवा कार्य सराहा जाता है।", "positive": True},
        7:  {"en": "Venus transiting H7 (Pakka Ghar) — peak placement for Venus. Best period for marriage, romantic partnerships, and harmonious legal agreements.", "hi": "शुक्र गोचर भाव 7 (पक्का घर) — शुक्र की उच्चतम स्थिति। विवाह, रोमांटिक साझेदारी और सामंजस्यपूर्ण कानूनी समझौतों का सर्वोत्तम काल।", "positive": True},
        8:  {"en": "Venus transiting H8 — hidden pleasures and in-law harmony. Financial inheritance or legacy matters surface. Occult arts and sensuality blend.", "hi": "शुक्र गोचर भाव 8 — छुपे सुख और ससुराल सामंजस्य। वित्तीय विरासत के मामले सामने आते हैं। गुप्त कला और कामुकता का मेल।", "positive": False},
        9:  {"en": "Venus transiting H9 — luck through beauty, art, and pleasure. Travel for pleasure and cultural enrichment. Religious tolerance expands.", "hi": "शुक्र गोचर भाव 9 — सौंदर्य, कला और आनंद से भाग्य। सुख के लिए यात्रा और सांस्कृतिक समृद्धि। धार्मिक सहिष्णुता बढ़ती है।", "positive": True},
        10: {"en": "Venus transiting H10 — career in arts, beauty, luxury, or entertainment. Public charm and grace bring professional success.", "hi": "शुक्र गोचर भाव 10 — कला, सौंदर्य, विलासिता या मनोरंजन में करियर। सार्वजनिक आकर्षण और शालीनता से पेशेवर सफलता।", "positive": True},
        11: {"en": "Venus transiting H11 — gains through beauty, relationships, and charm. Elder siblings or beautiful friends bring wealth and fulfillment.", "hi": "शुक्र गोचर भाव 11 — सौंदर्य, संबंधों और आकर्षण से लाभ। बड़े भाई-बहन या सुंदर मित्र धन और संतुष्टि लाते हैं।", "positive": True},
        12: {"en": "Venus transiting H12 — secret pleasures and foreign romances. Spiritual devotion through beauty. Hidden artistic work may emerge.", "hi": "शुक्र गोचर भाव 12 — गुप्त सुख और विदेशी रोमांस। सौंदर्य के माध्यम से आध्यात्मिक भक्ति। छुपा कलात्मक कार्य उभर सकता है।", "positive": False},
    },
    "Saturn": {
        1:  {"en": "Saturn transiting H1 — significant life pressure on health and identity. Discipline and patience are essential. Sadesati may apply.", "hi": "शनि गोचर भाव 1 — स्वास्थ्य और व्यक्तित्व पर भारी दबाव। अनुशासन और धैर्य अनिवार्य। साढ़ेसाती संभव।", "positive": False},
        2:  {"en": "Saturn transiting H2 — family wealth comes slowly. Careful, disciplined speech is needed. Save rather than spend — lean months possible.", "hi": "शनि गोचर भाव 2 — पारिवारिक धन धीमे आता है। सावधान और अनुशासित वाणी जरूरी। बचत करें — कठिन महीने संभव।", "positive": False},
        3:  {"en": "Saturn transiting H3 — sibling relationships are tested. Hard work in communications yields delayed results. Discipline in efforts pays eventually.", "hi": "शनि गोचर भाव 3 — भाई-बहन संबंध परखे जाते हैं। संचार में कठिन परिश्रम से देर से फल। प्रयासों में अनुशासन अंततः फलता है।", "positive": False},
        4:  {"en": "Saturn transiting H4 — domestic difficulties and mother's health need attention. Property disputes or delayed home repairs possible.", "hi": "शनि गोचर भाव 4 — घरेलू कठिनाइयाँ और माता के स्वास्थ्य पर ध्यान। संपत्ति विवाद या घर की मरम्मत में देरी संभव।", "positive": False},
        5:  {"en": "Saturn transiting H5 — children matters require patience. Speculation is unfavorable. Study and creative work with discipline bear long-term fruit.", "hi": "शनि गोचर भाव 5 — संतान के मामलों में धैर्य जरूरी। सट्टा प्रतिकूल। अनुशासन से पढ़ाई और रचनात्मक कार्य दीर्घकालिक फल देते हैं।", "positive": False},
        6:  {"en": "Saturn transiting H6 — excellent for overcoming enemies through persistence. Health needs disciplined management. Service to others is highly rewarded.", "hi": "शनि गोचर भाव 6 — दृढ़ता से शत्रुओं पर विजय के लिए उत्कृष्ट। स्वास्थ्य का अनुशासित प्रबंधन जरूरी। सेवा कार्य अत्यधिक पुरस्कृत।", "positive": True},
        7:  {"en": "Saturn transiting H7 (Pakka Ghar) — relationships stabilize through effort and commitment. Contractual and legal matters resolve with patience.", "hi": "शनि गोचर भाव 7 (पक्का घर) — प्रयास और प्रतिबद्धता से संबंध स्थिर। अनुबंध और कानूनी मामले धैर्य से सुलझते हैं।", "positive": True},
        8:  {"en": "Saturn transiting H8 — karmic debts surface. Hidden obstacles and chronic health concerns. Spiritual discipline and patience help navigate this phase.", "hi": "शनि गोचर भाव 8 — कर्म ऋण उभरते हैं। छुपी बाधाएँ और दीर्घकालीन स्वास्थ्य चिंताएँ। आध्यात्मिक अनुशासन और धैर्य सहायक।", "positive": False},
        9:  {"en": "Saturn transiting H9 — dharma and luck come through hard work and perseverance. Travel is possible but with delays. Father's health needs attention.", "hi": "शनि गोचर भाव 9 — धर्म और भाग्य कठिन परिश्रम से आते हैं। यात्रा में देरी संभव। पिता के स्वास्थ्य पर ध्यान।", "positive": False},
        10: {"en": "Saturn transiting H10 (Pakka Ghar) — career sees steady hard-won progress. Authority and recognition come through consistent discipline.", "hi": "शनि गोचर भाव 10 (पक्का घर) — कठिन परिश्रम से करियर में स्थिर प्रगति। लगातार अनुशासन से अधिकार और मान-सम्मान।", "positive": True},
        11: {"en": "Saturn transiting H11 — slow but sure financial gains. Elder siblings may face burdens. Long-term wishes fulfill gradually through persistence.", "hi": "शनि गोचर भाव 11 — धीमे पर पक्के आर्थिक लाभ। बड़े भाई-बहन बोझ से दब सकते हैं। दीर्घकालिक इच्छाएँ धीरे-धीरे पूरी होती हैं।", "positive": True},
        12: {"en": "Saturn transiting H12 — expenditures rise and isolation increases. Spiritual retreat or long-term foreign stay is indicated. Past karma requires closure.", "hi": "शनि गोचर भाव 12 — खर्च बढ़ता है और एकांत में वृद्धि। आध्यात्मिक साधना या विदेश में दीर्घकालीन प्रवास। पुराने कर्म का समाधान जरूरी।", "positive": False},
    },
    "Mars": {
        1:  {"en": "Mars transiting H1 — high energy, ambition, and bold action. Excellent for new ventures and physical activities. Control temper to avoid conflicts.", "hi": "मंगल गोचर भाव 1 — उच्च ऊर्जा, महत्वाकांक्षा और साहसिक कार्य। नई परियोजनाओं और शारीरिक गतिविधियों के लिए उत्कृष्ट। क्रोध नियंत्रित करें।", "positive": True},
        2:  {"en": "Mars transiting H2 — family tensions and financial impulsiveness. Avoid hasty spending or harsh speech. Energy directed to earning is productive.", "hi": "मंगल गोचर भाव 2 — पारिवारिक तनाव और आर्थिक आवेग। जल्दबाजी में खर्च या कटु वाणी से बचें। कमाई की ओर ऊर्जा उत्पादक।", "positive": False},
        3:  {"en": "Mars transiting H3 (Pakka Ghar) — courage, energy, and sibling relations strengthened. Bold decisions and physical challenges succeed.", "hi": "मंगल गोचर भाव 3 (पक्का घर) — साहस, ऊर्जा और भाई-बहन संबंध मजबूत। साहसिक निर्णय और शारीरिक चुनौतियाँ सफल।", "positive": True},
        4:  {"en": "Mars transiting H4 — domestic disputes and property conflicts possible. Mother's health needs attention. Avoid renovation that triggers conflicts.", "hi": "मंगल गोचर भाव 4 — घरेलू झगड़े और संपत्ति विवाद संभव। माता के स्वास्थ्य पर ध्यान। झगड़े भड़काने वाले नवीनीकरण से बचें।", "positive": False},
        5:  {"en": "Mars transiting H5 — speculation is risky. Children may be energetic or troublesome. Creative energy is high — channel it into sports or arts.", "hi": "मंगल गोचर भाव 5 — सट्टा जोखिमपूर्ण। संतान उत्साही या परेशानीपूर्ण। रचनात्मक ऊर्जा उच्च — खेल या कला में लगाएँ।", "positive": False},
        6:  {"en": "Mars transiting H6 — excellent for defeating enemies and competition. Warrior energy works for you. Health improves through physical discipline.", "hi": "मंगल गोचर भाव 6 — शत्रुओं और प्रतिस्पर्धा पर विजय के लिए उत्कृष्ट। योद्धा ऊर्जा आपके पक्ष में। शारीरिक अनुशासन से स्वास्थ्य।", "positive": True},
        7:  {"en": "Mars transiting H7 — conflict in partnerships. Aggression in relationships needs control. Legal disputes possible. Passion is high but temper it.", "hi": "मंगल गोचर भाव 7 — साझेदारी में संघर्ष। संबंधों में आक्रामकता नियंत्रित करें। कानूनी विवाद संभव। जोश उच्च पर संयम रखें।", "positive": False},
        8:  {"en": "Mars transiting H8 (Pakka Ghar) — intense transformation. Sudden events, surgeries, or occult research may be active. Energy toward research succeeds.", "hi": "मंगल गोचर भाव 8 (पक्का घर) — तीव्र परिवर्तन। अचानक घटनाएँ, शल्य चिकित्सा या गुप्त अनुसंधान सक्रिय। शोध में ऊर्जा सफल।", "positive": False},
        9:  {"en": "Mars transiting H9 — aggressive pursuit of luck and dharma. Adventure travel and bold religious actions succeed. Father's dynamic energy is active.", "hi": "मंगल गोचर भाव 9 — भाग्य और धर्म की आक्रामक खोज। साहसिक यात्रा और साहसिक धार्मिक कार्य सफल। पिता की गतिशील ऊर्जा सक्रिय।", "positive": True},
        10: {"en": "Mars transiting H10 — career energy peaks. Ambition drives promotion and recognition. Leadership by action and assertion is effective.", "hi": "मंगल गोचर भाव 10 — करियर ऊर्जा चरम। महत्वाकांक्षा से पदोन्नति और मान्यता। कार्य और दृढ़ता से नेतृत्व प्रभावी।", "positive": True},
        11: {"en": "Mars transiting H11 — gains through bold action and aggression in networking. Elder sibling tensions possible. Impulsive purchases should be avoided.", "hi": "मंगल गोचर भाव 11 — नेटवर्किंग में साहसिक कार्य और आक्रामकता से लाभ। बड़े भाई-बहन में तनाव संभव। आवेगी खरीद से बचें।", "positive": True},
        12: {"en": "Mars transiting H12 — hidden aggression drains energy. Spiritual battles and secret struggles. Watch for injuries or unexpected expenditures.", "hi": "मंगल गोचर भाव 12 — छुपी आक्रामकता ऊर्जा खींचती है। आध्यात्मिक संघर्ष और गुप्त लड़ाइयाँ। चोट या अप्रत्याशित खर्च से सावधान।", "positive": False},
    },
    "Rahu": {
        1:  {"en": "Rahu transiting H1 — identity confusion and unusual experiences. Unconventional opportunities or foreign travel arise. Ambition intensifies unusually.", "hi": "राहु गोचर भाव 1 — पहचान में भ्रम और असामान्य अनुभव। अपरंपरागत अवसर या विदेश यात्रा। महत्वाकांक्षा असामान्य रूप से तीव्र।", "positive": False},
        2:  {"en": "Rahu transiting H2 — family speech becomes unusual or deceptive. Financial speculation with foreign elements. Unusual items or food enter the home.", "hi": "राहु गोचर भाव 2 — पारिवारिक वाणी असामान्य या भ्रामक। विदेशी तत्वों के साथ आर्थिक सट्टा। असामान्य वस्तुएँ या भोजन घर में आते हैं।", "positive": False},
        3:  {"en": "Rahu transiting H3 — unusual courage emerges. Digital communications, foreign sibling connections, or unconventional short journeys are active.", "hi": "राहु गोचर भाव 3 — असामान्य साहस उभरता है। डिजिटल संवाद, विदेशी भाई-बहन संपर्क, या अपरंपरागत यात्राएँ सक्रिय।", "positive": False},
        4:  {"en": "Rahu transiting H4 — domestic disruption or renovation. Mother's health may take an unusual turn. Foreign property or unconventional home matters.", "hi": "राहु गोचर भाव 4 — घरेलू व्यवधान या नवीनीकरण। माता का स्वास्थ्य असामान्य मोड़ ले सकता है। विदेशी संपत्ति या अपरंपरागत घर के मामले।", "positive": False},
        5:  {"en": "Rahu transiting H5 — speculative gains possible but highly risky. Unconventional children or creative ideas. Past karma in intelligence surfaces.", "hi": "राहु गोचर भाव 5 — सट्टे में लाभ संभव पर अत्यधिक जोखिम। अपरंपरागत संतान या रचनात्मक विचार। बुद्धि में पूर्वकर्म सामने आता है।", "positive": False},
        6:  {"en": "Rahu transiting H6 (Pakka Ghar) — enemies are confused and weakened. Unconventional solutions defeat opponents. Healing through non-traditional methods.", "hi": "राहु गोचर भाव 6 (पक्का घर) — शत्रु भ्रमित और कमजोर होते हैं। अपरंपरागत उपायों से विजय। गैर-पारंपरिक तरीकों से उपचार।", "positive": True},
        7:  {"en": "Rahu transiting H7 — unconventional relationships or business partnerships. Foreign spouse connection possible. Deception in partnerships needs vigilance.", "hi": "राहु गोचर भाव 7 — अपरंपरागत संबंध या व्यापार साझेदारी। विदेशी जीवनसाथी संबंध संभव। साझेदारी में धोखे पर सतर्कता।", "positive": False},
        8:  {"en": "Rahu transiting H8 — occult and research intensified. Sudden inheritance or legacy matters from foreign sources. Hidden transformations are rapid.", "hi": "राहु गोचर भाव 8 — गुप्त विद्या और शोध तीव्र। विदेशी स्रोत से अचानक विरासत या संपत्ति। छुपे परिवर्तन तीव्र गति से।", "positive": False},
        9:  {"en": "Rahu transiting H9 — unconventional beliefs and foreign guru or teacher. Luck comes through strange channels. Long-distance travel with unusual experiences.", "hi": "राहु गोचर भाव 9 — अपरंपरागत विश्वास और विदेशी गुरु। भाग्य अजीब रास्तों से। असामान्य अनुभवों के साथ दूर यात्रा।", "positive": False},
        10: {"en": "Rahu transiting H10 — ambitious career gains through unconventional means. Foreign, government, or tech-based career opportunities appear suddenly.", "hi": "राहु गोचर भाव 10 — अपरंपरागत तरीकों से महत्वाकांक्षी करियर लाभ। विदेशी, सरकारी या टेक-आधारित अवसर अचानक आते हैं।", "positive": True},
        11: {"en": "Rahu transiting H11 (Pakka Ghar) — unexpected financial gains and foreign connections bring wealth. Ambitions are fulfilled through unusual or indirect routes.", "hi": "राहु गोचर भाव 11 (पक्का घर) — अप्रत्याशित आर्थिक लाभ और विदेशी संपर्क धन लाते हैं। इच्छाएँ असामान्य या अप्रत्यक्ष मार्गों से पूरी होती हैं।", "positive": True},
        12: {"en": "Rahu transiting H12 (Pakka Ghar) — deep foreign connections and hidden spending. Spiritual obsession possible. Past karma from foreign lands surfaces.", "hi": "राहु गोचर भाव 12 (पक्का घर) — गहरे विदेशी संपर्क और छुपा खर्च। आध्यात्मिक जुनून संभव। विदेशी भूमि से पूर्वकर्म सामने।", "positive": False},
    },
    "Ketu": {
        1:  {"en": "Ketu transiting H1 — detachment from ego. Past-life identity active. Spiritual experiences and mysterious health fluctuations. Focus on inner truth.", "hi": "केतु गोचर भाव 1 — अहंकार से वैराग्य। पूर्वजन्म की पहचान सक्रिय। आध्यात्मिक अनुभव और रहस्यमय स्वास्थ्य उतार-चढ़ाव। आंतरिक सत्य पर ध्यान।", "positive": False},
        2:  {"en": "Ketu transiting H2 — family detachment. Speech becomes spiritual or unclear. Wealth has a past-life karmic flavor — unexpected gains or losses.", "hi": "केतु गोचर भाव 2 — परिवार से वैराग्य। वाणी आध्यात्मिक या अस्पष्ट। धन में पूर्वजन्म का कर्म — अप्रत्याशित लाभ या हानि।", "positive": False},
        3:  {"en": "Ketu transiting H3 (Pakka Ghar) — intuitive courage and past-life sibling connections. Spiritual journeys and inner communication are powerful.", "hi": "केतु गोचर भाव 3 (पक्का घर) — अंतर्ज्ञानी साहस और पूर्वजन्म के भाई-बहन संबंध। आध्यात्मिक यात्राएँ और आंतरिक संवाद शक्तिशाली।", "positive": True},
        4:  {"en": "Ketu transiting H4 — home detachment. Ancestral property karma resolves. Mother's spiritual matters are highlighted. Need for inner home-peace.", "hi": "केतु गोचर भाव 4 — घर से वैराग्य। पैतृक संपत्ति कर्म सुलझता है। माता के आध्यात्मिक मामले प्रमुख। आंतरिक घरेलू शांति की जरूरत।", "positive": False},
        5:  {"en": "Ketu transiting H5 — past-life intelligence surfaces. Children have a karmic connection. Speculation has a spiritual or intuitive dimension.", "hi": "केतु गोचर भाव 5 — पूर्वजन्म की बुद्धि सामने आती है। संतान से कर्म संबंध। सट्टे में आध्यात्मिक या अंतर्ज्ञानी आयाम।", "positive": False},
        6:  {"en": "Ketu transiting H6 (Pakka Ghar) — enemies dissolve through past karma. Disease karma from previous lives resolves. Detached service brings spiritual protection.", "hi": "केतु गोचर भाव 6 (पक्का घर) — पूर्वजन्म के कर्म से शत्रु घुलते हैं। पूर्वजन्म के रोग कर्म सुलझते हैं। वैराग्यपूर्ण सेवा से आध्यात्मिक सुरक्षा।", "positive": True},
        7:  {"en": "Ketu transiting H7 — partnership detachment. Spouse connection feels karmically destined from a past life. Marriage may feel spiritually driven.", "hi": "केतु गोचर भाव 7 — साझेदारी से वैराग्य। जीवनसाथी संबंध पूर्वजन्म से कर्मपूर्वक नियत। विवाह आध्यात्मिक रूप से संचालित।", "positive": False},
        8:  {"en": "Ketu transiting H8 — deep spiritual transformation. Past-life occult knowledge surfaces. Liberation through crisis — this period reshapes the soul.", "hi": "केतु गोचर भाव 8 — गहरी आध्यात्मिक परिवर्तन। पूर्वजन्म का गुप्त ज्ञान सामने। संकट से मुक्ति — यह काल आत्मा को पुनर्आकार देता है।", "positive": False},
        9:  {"en": "Ketu transiting H9 — spiritual dharma from past lives activates. Guru connection deepens. Religious detachment leads to genuine wisdom.", "hi": "केतु गोचर भाव 9 — पूर्वजन्म से आध्यात्मिक धर्म सक्रिय। गुरु संबंध गहरा होता है। धार्मिक वैराग्य वास्तविक ज्ञान की ओर।", "positive": True},
        10: {"en": "Ketu transiting H10 — career detachment. Work feels karmically driven. Past-life authority patterns surface — detach from outcomes for best results.", "hi": "केतु गोचर भाव 10 — करियर से वैराग्य। कार्य कर्मपूर्वक संचालित। पूर्वजन्म के अधिकार पैटर्न सामने — फल से वैराग्य से सर्वोत्तम परिणाम।", "positive": False},
        11: {"en": "Ketu transiting H11 — gains detachment. Elder sibling has a past-life connection. Spiritual desires are fulfilled while material wishes feel hollow.", "hi": "केतु गोचर भाव 11 — लाभ से वैराग्य। बड़े भाई-बहन से पूर्वजन्म का संबंध। आध्यात्मिक इच्छाएँ पूरी होती हैं, भौतिक इच्छाएँ खोखी लगती हैं।", "positive": False},
        12: {"en": "Ketu transiting H12 (Pakka Ghar) — Ketu at peak spiritual power. Deep moksha energy, foreign past-life connections, and liberation are strongly active.", "hi": "केतु गोचर भाव 12 (पक्का घर) — केतु की उच्चतम आध्यात्मिक शक्ति। गहरी मोक्ष ऊर्जा, विदेशी पूर्वजन्म संबंध और मुक्ति प्रबल रूप से सक्रिय।", "positive": True},
    },
}


@router.get("/api/lalkitab/gochar")
def get_gochar_transits(
    kundli_id: Optional[str] = Query(default=None, description="Natal chart ID for personalized comparison"),
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return today's live planetary positions mapped to LK houses with optional natal chart comparison."""
    from app.mundane_engine import _get_current_planet_positions

    try:
        transit_planets = _get_current_planet_positions()
    except Exception as exc:
        logger.error("gochar: failed to compute planet positions: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Could not compute planetary positions")

    # Load natal chart for personalized comparison if kundli_id provided
    natal_houses: dict[str, int] = {}
    if kundli_id:
        row = db.execute(
            "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
            (kundli_id, user["sub"]),
        ).fetchone()
        if row:
            chart_data = json.loads(row["chart_data"])
            for pname, info in chart_data.get("planets", {}).items():
                if pname in _KNOWN_PLANETS:
                    natal_houses[pname] = _derive_lk_house(info)

    transits = []
    # Build transit-house → planets map for compound detection
    transit_house_map: dict[int, list] = {}
    for pname, pdata in transit_planets.items():
        if pname not in _KNOWN_PLANETS:
            continue
        sign = pdata.get("sign", "Aries")
        lk_house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        transit_house_map.setdefault(lk_house, []).append(pname)

    for pname, pdata in transit_planets.items():
        if pname not in _KNOWN_PLANETS:
            continue
        sign = pdata.get("sign", "Aries")
        lk_house = _SIGN_TO_LK_HOUSE.get(sign, 0)

        entry: dict = {
            "planet": pname,
            "sign": sign,
            "sign_degree": round(pdata.get("sign_degree") or 0.0, 2),
            "nakshatra": pdata.get("nakshatra"),
            "retrograde": bool(pdata.get("retrograde", False)),
            "lk_house": lk_house,
            "speed_note": _PLANET_SPEED.get(pname, "medium"),
        }

        # Personalized natal comparison
        if natal_houses:
            natal_house = natal_houses.get(pname, 0)
            entry["natal_house"] = natal_house
            entry["on_natal_position"] = (lk_house == natal_house and natal_house != 0)

            # Pakka Ghar check
            pakka = _PAKKA_GHAR_GOCHAR.get(pname, set())
            entry["in_pakka_ghar"] = lk_house in pakka

            # LK gochar canonical note for this planet's transit house
            planet_rules = _GOCHAR_PLANET_RULES.get(pname, {})
            rule = planet_rules.get(lk_house)
            if rule:
                entry["lk_gochar_note_en"] = rule["en"]
                entry["lk_gochar_note_hi"] = rule["hi"]
                entry["transit_positive"] = rule["positive"]

            # Natal hit: transit planet conjunct a natal planet in the same house
            natal_cohabitants = [
                p for p, nh in natal_houses.items()
                if nh == lk_house and p != pname
            ]
            if natal_cohabitants:
                entry["natal_hit_planets"] = natal_cohabitants
                entry["natal_hit_note_en"] = (
                    f"Transit {pname} is now in H{lk_house}, the natal house of "
                    f"{', '.join(natal_cohabitants)}. This intensifies the significations of both planets."
                )
                entry["natal_hit_note_hi"] = (
                    f"गोचर {pname} अब भाव {lk_house} में है — यही {', '.join(natal_cohabitants)} का जन्म भाव है। "
                    "दोनों ग्रहों के कारकत्व तीव्र होते हैं।"
                )

        transits.append(entry)

    # Compound transit alerts (Angarak, Shrapit, Guru-Chandal in LK houses)
    alerts = []
    for house, planets_in_house in transit_house_map.items():
        planet_set = set(p.lower() for p in planets_in_house)
        if "mars" in planet_set and "rahu" in planet_set:
            alerts.append({"type": "Angarak_Yoga", "house": house, "planets": ["Mars", "Rahu"],
                           "note_en": f"Mars and Rahu both transiting LK H{house} — Angarak Yoga active. Impulsive decisions and accidents risk elevated.",
                           "note_hi": f"मंगल और राहु दोनों गोचर भाव {house} में — अंगारक योग सक्रिय। आवेगपूर्ण निर्णयों और दुर्घटना का जोखिम बढ़ा।"})
        if "saturn" in planet_set and "rahu" in planet_set:
            alerts.append({"type": "Shrapit_Yoga", "house": house, "planets": ["Saturn", "Rahu"],
                           "note_en": f"Saturn and Rahu both transiting LK H{house} — Shrapit Yoga in transit. Karmic obstacles in H{house} matters.",
                           "note_hi": f"शनि और राहु दोनों गोचर भाव {house} में — श्रापित योग। भाव {house} के मामलों में कर्म बाधाएँ।"})
        if "jupiter" in planet_set and ("rahu" in planet_set or "ketu" in planet_set):
            malefic = "Rahu" if "rahu" in planet_set else "Ketu"
            alerts.append({"type": "Guru_Chandal", "house": house, "planets": ["Jupiter", malefic],
                           "note_en": f"Jupiter and {malefic} both transiting LK H{house} — Guru Chandal Yoga. Wisdom may be clouded; decisions need extra scrutiny.",
                           "note_hi": f"गुरु और {malefic} दोनों गोचर भाव {house} में — गुरु चांडाल योग। निर्णय सावधानी से लें।"})

    result = {"transits": transits, "as_of": _date.today().isoformat(), "alerts": alerts}
    if natal_houses:
        result["natal_chart_used"] = True
    return result


# ─────────────────────────────────────────────────────────────
# Lal Kitab Nishaniyan (Signs/Omens from DB)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/nishaniyan/{kundli_id}")
def get_nishaniyan(
    kundli_id: str,
    category: str = None,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return nishaniyan (omens/signs) from DB matched to chart planet positions."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    # Build list of (planet_lower, lk_house) tuples
    planet_house_pairs = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        # Unified derivation: prefer explicit house, fall back to sign
        house = _derive_lk_house(info)
        if house:
            planet_house_pairs.append((planet_name.lower(), house))

    if not planet_house_pairs:
        return {"nishaniyan": []}

    # Build parameterised WHERE clause
    placeholders = " OR ".join(
        "(planet = %s AND house = %s)" for _ in planet_house_pairs
    )
    params = [val for pair in planet_house_pairs for val in pair]

    if category:
        query = (
            f"SELECT * FROM nishaniyan_master WHERE ({placeholders}) AND category = %s"
            " ORDER BY planet, house"
        )
        params.append(category)
    else:
        query = (
            f"SELECT * FROM nishaniyan_master WHERE ({placeholders})"
            " ORDER BY planet, house"
        )

    rows = db.execute(query, params).fetchall()
    nishaniyan = []
    seen: set[tuple] = set()
    for r in rows:
        # Deduplicate on (planet, house, text) — DB may contain duplicate rows
        dedup_key = (r["planet"], r["house"], r.get("nishani_text_en") or r.get("nishani_text") or "")
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        nishaniyan.append({
            "id": r["id"],
            "planet": r["planet"],
            "house": r["house"],
            "nishani_text": r["nishani_text"],
            "nishani_text_en": r["nishani_text_en"],
            "category": r["category"],
            "severity": r["severity"],
        })
    return {"nishaniyan": nishaniyan}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Rin (Karmic Debts)
# ─────────────────────────────────────────────────────────────

# Which houses indicate affliction/weakness → activates related rin
_AFFLICTION_HOUSES = {6, 8, 12}

# LK 1952 Pakka Ghar — planet's permanent house (strongest placement)
_PAKKA_GHAR: dict[str, set] = {
    "sun": {1},
    "moon": {4},
    "mars": {3, 8},
    "mercury": {3, 6},
    "jupiter": {2, 9, 12},
    "venus": {7},
    "saturn": {7, 10},
    "rahu": {6, 11, 12},
    "ketu": {3, 6, 12},
}


def _is_pakka_ghar(planet: str, house: int) -> bool:
    return house in _PAKKA_GHAR.get(planet.lower(), set())

# Planet → rin debt_type mapping (primary planet for each debt)
_PLANET_TO_RIN = {
    "sun": "पितृ ऋण",
    "moon": "मातृ ऋण",
    "mercury": "भ्रातृ ऋण",
    "jupiter": "देव ऋण",
    "venus": "स्त्री ऋण",
    "mars": "शत्रु ऋण",
    "saturn": "पितामह ऋण",
    "rahu": "प्रपितामह ऋण",
    "ketu": "प्रपितामह ऋण",
}


@router.get("/api/lalkitab/rin/{kundli_id}")
def get_rin(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Lal Kitab rin (karmic debts) with active flag based on chart."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    # Build planet list for the canonical debt engine
    planet_list = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        house = _derive_lk_house(info)
        planet_list.append({"planet": planet_name, "house": house})

    # Full karmic debt engine (LK 1952 canonical triggers — not just 6/8/12)
    from app.lalkitab_advanced import calculate_karmic_debts
    active_karmic_debts = calculate_karmic_debts(planet_list)

    # Fetch canonical 8-debt catalogue from DB for UI display
    debt_rows = db.execute(
        "SELECT * FROM lal_kitab_debts ORDER BY debt_type"
    ).fetchall()

    # Map active debts to DB catalogue by matching name keywords
    active_names_en = {d.get("name", {}).get("en", "").lower() for d in active_karmic_debts}

    def _debt_is_active(debt_type: str) -> bool:
        dt = (debt_type or "").lower()
        return any(kw in dt for kw in active_names_en) or any(kw in dt for kw in [
            kw for name in active_names_en for kw in name.split()
        ])

    catalogue = []
    for r in debt_rows:
        catalogue.append({
            "id": r["id"],
            "debt_type": r["debt_type"],
            "planet": r["planet"],
            "description": r["description"],
            "indication": r["indication"],
            "remedy": r["remedy"],
            "active": _debt_is_active(r["debt_type"]),
        })

    # Planets that triggered active debts
    triggered_planets = sorted({
        p["planet"].lower()
        for p in planet_list
        if _is_pakka_ghar(p["planet"], p["house"]) is False and p["house"] in _AFFLICTION_HOUSES
        or any(p["planet"].lower() in (d.get("reason", {}).get("en", "") or "").lower()
               for d in active_karmic_debts)
    })

    return {
        "debts": catalogue,
        "active_karmic_debts": active_karmic_debts,
        "active_count": len(active_karmic_debts),
        "triggered_planets": triggered_planets,
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab Predictions (Marriage / Career / Health / Wealth)
# ─────────────────────────────────────────────────────────────

_MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}

# 10th house planet → career mapping
_CAREER_MAP = {
    "sun": {
        "careers": ["सरकारी नौकरी", "प्रशासन", "राजनीति", "डॉक्टर"],
        "en_careers": ["Government Service", "Administration", "Politics", "Doctor"],
        "nature": "job",
    },
    "moon": {
        "careers": ["व्यापार", "जल व्यवसाय", "कृषि", "दूध-डेयरी"],
        "en_careers": ["Trade", "Water-related business", "Agriculture", "Dairy"],
        "nature": "business",
    },
    "mars": {
        "careers": ["सेना", "पुलिस", "इंजीनियरिंग", "ठेकेदारी"],
        "en_careers": ["Military", "Police", "Engineering", "Contracting"],
        "nature": "job",
    },
    "mercury": {
        "careers": ["लेखन", "व्यापार", "एकाउंटेंट", "मीडिया"],
        "en_careers": ["Writing", "Trade", "Accounting", "Media"],
        "nature": "business",
    },
    "jupiter": {
        "careers": ["शिक्षा", "धर्म", "न्याय", "बैंकिंग"],
        "en_careers": ["Education", "Religion", "Law", "Banking"],
        "nature": "job",
    },
    "venus": {
        "careers": ["कला", "फैशन", "मनोरंजन", "होटल"],
        "en_careers": ["Arts", "Fashion", "Entertainment", "Hospitality"],
        "nature": "business",
    },
    "saturn": {
        "careers": ["मजदूरी", "निर्माण", "खनिज", "तेल-गैस"],
        "en_careers": ["Labour", "Construction", "Mining", "Oil & Gas"],
        "nature": "job",
    },
    "rahu": {
        "careers": ["तकनीक", "विदेश व्यापार", "अनुसंधान", "राजनीति"],
        "en_careers": ["Technology", "Foreign Trade", "Research", "Politics"],
        "nature": "business",
    },
    "ketu": {
        "careers": ["अध्यात्म", "चिकित्सा", "गुप्त विज्ञान", "खोज"],
        "en_careers": ["Spirituality", "Medicine", "Occult", "Research"],
        "nature": "business",
    },
}

# 6/8/12 house planets → health areas
_HEALTH_MAP = {
    "sun": {"area": "हृदय, आंखें, रीढ़", "en_area": "Heart, Eyes, Spine"},
    "moon": {"area": "मन, फेफड़े, तरल", "en_area": "Mind, Lungs, Fluids"},
    "mars": {"area": "रक्त, मांसपेशी, सर्जरी", "en_area": "Blood, Muscles, Surgery risk"},
    "mercury": {"area": "नसें, त्वचा, पाचन", "en_area": "Nerves, Skin, Digestion"},
    "jupiter": {"area": "यकृत, मोटापा, मधुमेह", "en_area": "Liver, Obesity, Diabetes"},
    "venus": {"area": "गुर्दे, त्वचा, प्रजनन", "en_area": "Kidneys, Skin, Reproductive"},
    "saturn": {"area": "हड्डियां, जोड़, दांत", "en_area": "Bones, Joints, Teeth"},
    "rahu": {"area": "मानसिक विकार, अज्ञात रोग", "en_area": "Mental disorders, Unknown ailments"},
    "ketu": {"area": "संक्रमण, रहस्यमय रोग", "en_area": "Infections, Mysterious illness"},
}

# Jupiter/Venus house → wealth potential
_WEALTH_MAP = {
    1: {"potential": "उत्तम", "en": "Excellent", "score": 90},
    2: {"potential": "श्रेष्ठ", "en": "Superior", "score": 95},
    4: {"potential": "अच्छा", "en": "Good", "score": 75},
    5: {"potential": "उत्तम", "en": "Excellent", "score": 88},
    7: {"potential": "व्यापार से", "en": "Through business", "score": 80},
    9: {"potential": "भाग्यशाली", "en": "Lucky", "score": 92},
    10: {"potential": "कर्म से", "en": "Through hard work", "score": 78},
    11: {"potential": "श्रेष्ठ", "en": "Superior", "score": 93},
    3: {"potential": "मध्यम", "en": "Moderate", "score": 60},
    6: {"potential": "संघर्ष", "en": "Struggle", "score": 45},
    8: {"potential": "उतार-चढ़ाव", "en": "Fluctuating", "score": 55},
    12: {"potential": "व्यय", "en": "Expenditure", "score": 40},
}


def _get_planet_positions(kundli_id: str, user_id: str, db: Any) -> dict:
    """Fetch chart_data and return {planet_lower: lk_house} mapping."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        return None
    chart_data = json.loads(row["chart_data"])
    positions = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        house = _derive_lk_house(info)
        positions[planet_name.lower()] = house
    return positions


def _get_chart_with_meta(kundli_id: str, user_id: str, db: Any):
    """Return ({planet_lower: lk_house}, birth_date_str, planet_list_for_engine) or (None, None, None)."""
    row = db.execute(
        "SELECT chart_data, birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        return None, None, None
    chart_data = json.loads(row["chart_data"])
    positions = {}
    planet_list = []  # [{planet: "Sun", house: 5}, ...] for lalkitab_advanced engines
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        house = _derive_lk_house(info)
        positions[planet_name.lower()] = house
        planet_list.append({"planet": planet_name, "house": house})
    return positions, str(row.get("birth_date") or ""), planet_list


def _get_current_saala_grah(birth_date: str) -> Optional[dict]:
    """Return current Saala Grah dict or None if birth_date unavailable."""
    if not birth_date:
        return None
    try:
        dasha = _get_dasha_timeline(birth_date, _date_today.today().isoformat())
        return dasha.get("current_saala_grah")
    except Exception:
        return None


@router.get("/api/lalkitab/predictions/marriage/{kundli_id}")
def predict_marriage(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Marriage predictions: Manglik check, 7th house lord, Venus placement."""
    positions, birth_date, _pl = _get_chart_with_meta(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")
    saala_grah = _get_current_saala_grah(birth_date)

    mars_house = positions.get("mars", 0)
    is_manglik = mars_house in _MANGLIK_HOUSES
    manglik_severity = (
        "strong" if mars_house in {1, 7, 8} else
        "moderate" if mars_house in {2, 4, 12} else
        "none"
    )

    venus_house = positions.get("venus", 0)
    seventh_planets = [p for p, h in positions.items() if h == 7]

    # Spouse quality based on Venus house
    venus_descriptions = {
        1: {"hi": "आकर्षक और प्रभावशाली जीवनसाथी", "en": "Attractive, dominant spouse"},
        2: {"hi": "धनी और सुखी परिवार", "en": "Wealthy, happy family life"},
        3: {"hi": "साहसी, यात्रा-प्रिय साथी", "en": "Adventurous, travel-loving partner"},
        4: {"hi": "घरेलू और सुखी जीवन", "en": "Domestic, happy life"},
        5: {"hi": "प्रेम-विवाह, रचनात्मक साथी", "en": "Love marriage, creative partner"},
        6: {"hi": "स्वास्थ्य-सावधानी, सेवा-प्रिय साथी", "en": "Health-conscious, service-oriented partner"},
        7: {"hi": "उत्तम वैवाहिक जीवन", "en": "Excellent marital life"},
        8: {"hi": "गहरा बंधन, पारिवारिक सम्पत्ति", "en": "Deep bond, inherited property"},
        9: {"hi": "भाग्यशाली, धार्मिक साथी", "en": "Lucky, religious partner"},
        10: {"hi": "कार्यक्षेत्र से मिलन, उच्च पद", "en": "Career-driven partner, high status"},
        11: {"hi": "मित्र से विवाह, लाभदायक", "en": "Friendship leads to marriage, profitable"},
        12: {"hi": "विदेश-निवास संभव, अध्यात्मिक साथी", "en": "Foreign settlement possible, spiritual partner"},
    }

    spouse_desc = venus_descriptions.get(venus_house, {"hi": "सामान्य वैवाहिक जीवन", "en": "Average marital life"})

    # Manglik remedies
    manglik_remedies = []
    if is_manglik:
        manglik_remedies = [
            "मंगलवार को हनुमान चालीसा पाठ करें",
            "लाल मसूर या गुड़ मंगलवार को दान करें",
            "मंगल यंत्र स्थापित करें",
        ]

    venus_pakka = _is_pakka_ghar("venus", venus_house)
    mars_pakka = _is_pakka_ghar("mars", mars_house)
    # Venus in H7 (Pakka Ghar) greatly strengthens marriage prospects
    marriage_boost = venus_pakka

    return {
        "is_manglik": is_manglik,
        "manglik_severity": manglik_severity,
        "mars_house": mars_house,
        "mars_pakka_ghar": mars_pakka,
        "venus_house": venus_house,
        "venus_pakka_ghar": venus_pakka,
        "marriage_boost": marriage_boost,
        "spouse_description": spouse_desc,
        "seventh_house_planets": seventh_planets,
        "manglik_remedies": manglik_remedies,
        "compatibility_note": {
            "hi": "मांगलिक दोष होने पर मांगलिक से विवाह शुभ होता है" if is_manglik else "मंगल दोष नहीं — सामान्य विवाह योग",
            "en": "Manglik should marry a Manglik for harmony" if is_manglik else "No Manglik dosha — normal marriage prospects",
        },
        "current_saala_grah": saala_grah,
        "dasha_note": {
            "hi": f"वर्तमान साल ग्रह {saala_grah['planet_hi']} — विवाह निर्णय इस वर्ष {'अनुकूल' if saala_grah['planet'] in ('venus', 'jupiter', 'moon') else 'सोच-समझकर लें'}" if saala_grah else None,
            "en": f"Current year ruler: {saala_grah['planet'].capitalize()} — marriage decisions this year {'are favoured' if saala_grah['planet'] in ('venus', 'jupiter', 'moon') else 'need careful consideration'}" if saala_grah else None,
        },
    }


@router.get("/api/lalkitab/predictions/career/{kundli_id}")
def predict_career(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Career predictions: 10th house planet, Saturn, Sun placements."""
    positions, birth_date, _pl = _get_chart_with_meta(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")
    saala_grah = _get_current_saala_grah(birth_date)

    tenth_planets = [p for p, h in positions.items() if h == 10]
    primary = tenth_planets[0] if tenth_planets else None

    career_info = _CAREER_MAP.get(primary, {
        "careers": ["विविध क्षेत्र", "स्वतंत्र कार्य"],
        "en_careers": ["Diverse fields", "Self-employment"],
        "nature": "business",
    }) if primary else {
        "careers": ["विविध क्षेत्र", "स्वतंत्र कार्य"],
        "en_careers": ["Diverse fields", "Self-employment"],
        "nature": "business",
    }

    sun_house = positions.get("sun", 0)
    saturn_house = positions.get("saturn", 0)
    mercury_house = positions.get("mercury", 0)

    # Business vs job suitability
    business_indicators = sum([
        positions.get("mercury", 0) in {2, 3, 7, 10, 11},
        positions.get("venus", 0) in {2, 7, 11},
        positions.get("jupiter", 0) in {2, 5, 9, 11},
        positions.get("moon", 0) in {2, 7, 11},
    ])
    job_indicators = sum([
        positions.get("sun", 0) in {1, 9, 10},
        positions.get("saturn", 0) in {3, 6, 10, 11},
        positions.get("mars", 0) in {1, 3, 6, 10},
    ])
    suitability = "business" if business_indicators > job_indicators else "job"

    # Favourable age periods by 10th house planet
    favourable_ages = {
        "sun": [22, 32, 42],
        "moon": [24, 32, 40],
        "mars": [28, 36, 44],
        "mercury": [25, 34, 45],
        "jupiter": [30, 39, 48],
        "venus": [25, 33, 41],
        "saturn": [32, 42, 52],
        "rahu": [27, 35, 42],
        "ketu": [30, 40, 50],
    }

    primary_pakka = _is_pakka_ghar(primary, positions.get(primary, 0)) if primary else False
    sun_pakka = _is_pakka_ghar("sun", sun_house)
    saturn_pakka = _is_pakka_ghar("saturn", saturn_house)

    return {
        "tenth_house_planets": tenth_planets,
        "primary_planet": primary,
        "primary_pakka_ghar": primary_pakka,
        "career_options": career_info["careers"],
        "career_options_en": career_info["en_careers"],
        "nature": career_info["nature"],
        "suitability": suitability,
        "favourable_ages": favourable_ages.get(primary, [28, 36, 44]),
        "sun_house": sun_house,
        "sun_pakka_ghar": sun_pakka,
        "saturn_house": saturn_house,
        "saturn_pakka_ghar": saturn_pakka,
        "mercury_house": mercury_house,
        "advice": {
            "hi": f"{'व्यापार में अधिक लाभ' if suitability == 'business' else 'नौकरी में स्थिरता'} — दसवें भाव में {'कोई ग्रह नहीं' if not primary else primary.capitalize()} है",
            "en": f"{'Business favoured for higher gains' if suitability == 'business' else 'Job brings stability'} — {primary.capitalize() if primary else 'No planet'} in 10th house",
        },
        "current_saala_grah": saala_grah,
        "dasha_note": {
            "hi": f"वर्तमान साल ग्रह {saala_grah['planet_hi']} — {'करियर में उन्नति की संभावना' if saala_grah['planet'] in ('sun', 'jupiter', 'mercury') else 'मेहनत से परिणाम'}" if saala_grah else None,
            "en": f"Current year ruler: {saala_grah['planet'].capitalize()} — {'career advancement likely' if saala_grah['planet'] in ('sun', 'jupiter', 'mercury') else 'results through consistent effort'}" if saala_grah else None,
        },
    }


@router.get("/api/lalkitab/predictions/health/{kundli_id}")
def predict_health(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Health predictions: planets in 6/8/12 houses, Sun/Moon/Mars/Saturn placements."""
    positions, birth_date, _pl = _get_chart_with_meta(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")
    saala_grah = _get_current_saala_grah(birth_date)

    # Planets in health-sensitive houses
    health_house_planets = {
        6: [p for p, h in positions.items() if h == 6],
        8: [p for p, h in positions.items() if h == 8],
        12: [p for p, h in positions.items() if h == 12],
    }

    vulnerable_areas = []
    precautions = []
    chronic_risk = []

    for house, planets in health_house_planets.items():
        for planet in planets:
            info = _HEALTH_MAP.get(planet, {})
            if info:
                vulnerable_areas.append({
                    "planet": planet,
                    "house": house,
                    "area_hi": info["area"],
                    "area_en": info["en_area"],
                })
            if house == 8:
                chronic_risk.append(planet)

    # Additional key planet checks
    sun_house = positions.get("sun", 0)
    moon_house = positions.get("moon", 0)
    mars_house = positions.get("mars", 0)
    saturn_house = positions.get("saturn", 0)

    if sun_house in {6, 8, 12}:
        precautions.append({"hi": "हृदय रोग से सावधानी, नियमित जांच करें", "en": "Beware of heart issues, regular checkups"})
    if moon_house in {6, 8, 12}:
        precautions.append({"hi": "मानसिक स्वास्थ्य पर ध्यान दें, ध्यान करें", "en": "Focus on mental health, meditate regularly"})
    if mars_house in {6, 8, 12}:
        precautions.append({"hi": "रक्त-विकार व चोट से बचें", "en": "Avoid blood disorders, be cautious of injuries"})
    if saturn_house in {6, 8, 12}:
        precautions.append({"hi": "जोड़ों व हड्डियों की देखभाल करें", "en": "Take care of joints and bones"})

    overall = "caution" if len(vulnerable_areas) >= 3 else "moderate" if vulnerable_areas else "good"

    # Pakka Ghar planets in affliction houses are not truly afflicted — they're in strength
    mitigated = [
        p for p in (vulnerable_areas or [])
        if _is_pakka_ghar(p["planet"], p["house"])
    ]

    return {
        "overall_health": overall,
        "vulnerable_areas": vulnerable_areas,
        "mitigated_by_pakka_ghar": mitigated,
        "precautions": precautions,
        "chronic_risk_planets": [p for p in chronic_risk if not _is_pakka_ghar(p, positions.get(p, 0))],
        "health_house_planets": {str(k): v for k, v in health_house_planets.items()},
        "sun_house": sun_house,
        "moon_house": moon_house,
        "mars_house": mars_house,
        "saturn_house": saturn_house,
        "current_saala_grah": saala_grah,
        "dasha_note": {
            "hi": f"वर्तमान साल ग्रह {saala_grah['planet_hi']} — {'स्वास्थ्य सावधानी आवश्यक' if saala_grah['planet'] in ('saturn', 'rahu', 'ketu', 'mars') else 'स्वास्थ्य सामान्य रहेगा'}" if saala_grah else None,
            "en": f"Current year ruler: {saala_grah['planet'].capitalize()} — {'health caution advised this year' if saala_grah['planet'] in ('saturn', 'rahu', 'ketu', 'mars') else 'health generally stable'}" if saala_grah else None,
        },
    }


@router.get("/api/lalkitab/predictions/wealth/{kundli_id}")
def predict_wealth(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Wealth predictions: Jupiter/Venus placement, 2nd/11th house analysis."""
    positions, birth_date, _pl = _get_chart_with_meta(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")
    saala_grah = _get_current_saala_grah(birth_date)

    jupiter_house = positions.get("jupiter", 0)
    venus_house = positions.get("venus", 0)
    second_planets = [p for p, h in positions.items() if h == 2]
    eleventh_planets = [p for p, h in positions.items() if h == 11]

    jup_wealth = _WEALTH_MAP.get(jupiter_house, {"potential": "मध्यम", "en": "Moderate", "score": 60})
    ven_wealth = _WEALTH_MAP.get(venus_house, {"potential": "मध्यम", "en": "Moderate", "score": 60})
    wealth_score = round((jup_wealth["score"] + ven_wealth["score"]) / 2)

    # Income sources based on 2nd/11th house planets
    income_source_map = {
        "sun": {"hi": "सरकार/पिता से आय", "en": "Income from government/father"},
        "moon": {"hi": "व्यापार/माता से आय", "en": "Income from trade/mother"},
        "mars": {"hi": "भूमि/साहस से आय", "en": "Income from land/courage"},
        "mercury": {"hi": "बुद्धि/व्यापार से आय", "en": "Income from intellect/business"},
        "jupiter": {"hi": "शिक्षा/धर्म से आय", "en": "Income from education/spirituality"},
        "venus": {"hi": "कला/विलासिता से आय", "en": "Income from arts/luxury"},
        "saturn": {"hi": "मेहनत/सेवा से आय", "en": "Income from hard work/service"},
        "rahu": {"hi": "तकनीक/विदेश से आय", "en": "Income from technology/foreign"},
        "ketu": {"hi": "गुप्त/अध्यात्म से आय", "en": "Income from occult/spirituality"},
    }

    income_sources = []
    for p in second_planets + eleventh_planets:
        src = income_source_map.get(p)
        if src and src not in income_sources:
            income_sources.append(src)

    # Investment advice based on Jupiter house
    investment_map = {
        1: {"hi": "स्वयं के व्यवसाय में निवेश करें", "en": "Invest in own business"},
        2: {"hi": "सोना, चांदी, नकद बचत", "en": "Gold, silver, cash savings"},
        4: {"hi": "भूमि, मकान में निवेश", "en": "Real estate investment"},
        5: {"hi": "शेयर, लॉटरी, सट्टे में सावधानी", "en": "Stocks with caution, avoid speculation"},
        7: {"hi": "साझेदारी में निवेश लाभदायक", "en": "Partnership investments beneficial"},
        9: {"hi": "धर्म-स्थान, विदेश में निवेश", "en": "Religious places, foreign investment"},
        10: {"hi": "व्यवसाय विस्तार में निवेश", "en": "Business expansion investment"},
        11: {"hi": "सभी प्रकार का निवेश शुभ", "en": "All types of investment favourable"},
    }
    investment_advice = investment_map.get(
        jupiter_house,
        {"hi": "सावधानी से निवेश करें", "en": "Invest cautiously"},
    )

    # Pakka Ghar boost: Jupiter in H2/H9/H12 or Venus in H7 = real wealth strength
    jup_pakka = _is_pakka_ghar("jupiter", jupiter_house)
    ven_pakka = _is_pakka_ghar("venus", venus_house)
    if jup_pakka:
        wealth_score = min(100, wealth_score + 8)
    if ven_pakka:
        wealth_score = min(100, wealth_score + 5)

    return {
        "wealth_score": wealth_score,
        "wealth_potential_hi": jup_wealth["potential"],
        "wealth_potential_en": jup_wealth["en"],
        "jupiter_house": jupiter_house,
        "jupiter_pakka_ghar": jup_pakka,
        "venus_house": venus_house,
        "venus_pakka_ghar": ven_pakka,
        "second_house_planets": second_planets,
        "eleventh_house_planets": eleventh_planets,
        "income_sources": income_sources,
        "investment_advice": investment_advice,
        "savings_tip": {
            "hi": "गुरु ११वें भाव में हो तो बचत अवश्य करें" if jupiter_house == 11 else "नियमित बचत और दान दोनों आवश्यक हैं",
            "en": "Jupiter in 11th — always save regularly" if jupiter_house == 11 else "Regular savings and charity both essential",
        },
        "current_saala_grah": saala_grah,
        "dasha_note": {
            "hi": f"वर्तमान साल ग्रह {saala_grah['planet_hi']} — {'धन लाभ की संभावना' if saala_grah['planet'] in ('jupiter', 'venus', 'mercury', 'moon') else 'खर्च पर नियंत्रण रखें'}" if saala_grah else None,
            "en": f"Current year ruler: {saala_grah['planet'].capitalize()} — {'financial gains likely' if saala_grah['planet'] in ('jupiter', 'venus', 'mercury', 'moon') else 'control expenditure this year'}" if saala_grah else None,
        },
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab Remedies Master (position-based from DB)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/remedies/master/{kundli_id}")
def get_remedies_master(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return position-based remedies from remedies_master for each planet in its LK house."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    # Build list of active planet-house pairs (skip house=0)
    active_planets = [p for p, h in positions.items() if h != 0]
    active_houses = [h for p, h in positions.items() if h != 0]

    remedies = []
    if active_planets:
        # Single query instead of N separate queries (one per planet)
        rows = db.execute(
            "SELECT * FROM remedies_master WHERE planet = ANY(%s) AND house = ANY(%s)",
            (active_planets, active_houses),
        ).fetchall()
        # Filter to only matching (planet, house) pairs since ANY is OR-based
        valid_pairs = {(p, h) for p, h in positions.items() if h != 0}
        # Codex D6 — attach Savdhaniyan + Andhe-Grah safety layer to
        # the master-remedies response so the UI can render them
        # alongside remedies from any endpoint, not just /enriched.
        from app.lalkitab_savdhaniyan import get_remedy_precautions
        from app.lalkitab_andhe_grah import detect_andhe_grah
        # P1.11 — Trial / Remedy / Good Conduct tier classification
        from app.lalkitab_remedy_classifier import classify_remedy, classification_label, classification_description

        # Build planet_positions list for the blind-planet detector
        pp_list = [
            {"planet": p.capitalize(), "house": h}
            for p, h in positions.items() if h != 0
        ]
        andhe = detect_andhe_grah(pp_list)
        blind_map = andhe.get("per_planet") or {}

        for r in rows:
            if (r["planet"], r["house"]) in valid_pairs:
                planet_cap = r["planet"].capitalize()
                precaution_bundle = get_remedy_precautions(
                    planet_cap,
                    house=r["house"],
                    remedy_material=(r.get("remedy_type") or "") if isinstance(r, dict) else "",
                )
                blind_info = blind_map.get(planet_cap) or {}
                andhe_warning = None
                if blind_info.get("is_blind"):
                    andhe_warning = {
                        "kind": "blind_planet",
                        "severity": blind_info.get("severity"),
                        "reasons": blind_info.get("reasons"),
                        "en": blind_info.get("warning_en"),
                        "hi": blind_info.get("warning_hi"),
                        "lk_ref": "4.14",
                    }
                # P1.11 — classify this remedy. The classifier reads from
                # the `en` text, so synthesise a dict that looks like the
                # stamped remedy shape used in lalkitab_engine.
                cls_input = {
                    "en": r.get("remedy_text") or r.get("instructions") or "",
                    "hi": "",
                    "material": r.get("remedy_type") or "",
                }
                cls = classify_remedy(cls_input)
                remedies.append({
                    "planet": r["planet"],
                    "house": r["house"],
                    "remedy_text": r["remedy_text"],
                    "remedy_type": r["remedy_type"],
                    "duration_days": r["duration_days"],
                    "instructions": r["instructions"],
                    "caution": r["caution"],
                    # D6 safety layer
                    "savdhaniyan": precaution_bundle,
                    "time_rule": precaution_bundle["time_rule"],
                    "reversal_risk": precaution_bundle["reversal_risk"],
                    "andhe_grah_warning": andhe_warning,
                    # P1.11 tier classification
                    "classification": cls,
                    "classification_en": classification_label(cls, is_hi=False),
                    "classification_hi": classification_label(cls, is_hi=True),
                    "classification_desc_en": classification_description(cls, is_hi=False),
                    "classification_desc_hi": classification_description(cls, is_hi=True),
                })

    return {"remedies": remedies}


@router.get("/api/lalkitab/advanced/{kundli_id}")
def get_lalkitab_advanced(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return advanced Lal Kitab analysis: Masnui Grah, Karmic Debts (with Hora), Teva type, and Prohibitions."""
    # Use the shared helper so we get the authoritative house derivation
    # (prefers explicit chart_data.planets[p]["house"], falls back to sign).
    # This eliminates the earlier sign-only bug that contradicted _get_lk_positions.
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)

    # formatted_positions: list of {"planet": "Sun", "house": N} — already correct shape.
    formatted_positions = [
        {"planet": p["planet"].capitalize(), "house": p["house"]}
        for p in positions
    ]

    # Calculate Hora-based karmic debts if birth datetime available.
    # Hora requires the REAL sunrise for the birth date + location — we compute
    # it from panchang_engine and only enable the Hora path when sunrise
    # succeeds. When it fails we pass sunrise_time=None so the advanced
    # calculator emits "_skipped=True" rather than silently using 06:00.
    hora_debt_analysis = None
    hora_debt_available = False
    hora_debt_reason = None
    try:
        from datetime import datetime
        birth_datetime = datetime.combine(
            datetime.strptime(row["birth_date"], "%Y-%m-%d").date(),
            datetime.strptime(row["birth_time"], "%H:%M:%S").time()
        )

        # Pull real sunrise from Panchang engine (uses Swiss Ephemeris
        # when available, falls back to NOAA approximation).
        sunrise_time_obj = None
        # Resolve coordinates: prefer stored lat/lon, fall back to city lookup.
        _lat = row.get("latitude")
        _lon = row.get("longitude")
        _tz = row.get("timezone_offset")
        if (_lat is None or _lon is None or _tz is None):
            _city_coords = _lookup_city_coords(row.get("birth_place"))
            if _city_coords:
                _lat, _lon, _tz = _city_coords
                logger.debug("Hora geocoding: resolved '%s' → lat=%.4f lon=%.4f tz=%.1f",
                             row.get("birth_place"), _lat, _lon, _tz)

        if (_lat is None or _lon is None or _tz is None):
            hora_debt_reason = "kundli missing location/timezone — Hora requires real birth coordinates"
        else:
            try:
                from app.panchang_engine import _compute_sun_times
                sun_times = _compute_sun_times(
                    row["birth_date"],
                    float(_lat),
                    float(_lon),
                    float(_tz),
                )
                sr_str = sun_times.get("sunrise")
                if sr_str and sr_str != "--:--":
                    sunrise_time_obj = datetime.strptime(sr_str, "%H:%M").time()
            except Exception as sr_exc:
                logger.warning("Sunrise computation failed for Hora: %s", sr_exc)
                hora_debt_reason = "sunrise computation failed"

        if sunrise_time_obj is None and hora_debt_reason is None:
            hora_debt_reason = "sunrise not available"

        hora_debt_analysis = calculate_karmic_debts_with_hora(
            formatted_positions,
            birth_datetime=birth_datetime,
            sunrise_time=sunrise_time_obj,
        )
        # If the analysis skipped (no sunrise), surface the flag; otherwise
        # treat as available.
        hora_info_local = (hora_debt_analysis or {}).get("hora_analysis") or {}
        if hora_info_local.get("_skipped"):
            hora_debt_available = False
            hora_debt_reason = hora_debt_reason or "sunrise not computed"
        else:
            hora_debt_available = True
    except Exception as e:
        logger.warning("Hora calculation failed: %s", e)
        hora_debt_reason = f"exception: {type(e).__name__}"

    # Calculate new logic
    lk_aspects = calculate_lk_aspects(formatted_positions)
    sleeping_info = calculate_sleeping_status(formatted_positions)
    kayam_planets = calculate_kayam_grah(formatted_positions, lk_aspects)

    # Parse chart_data once — needed by Andhe Grah (P1.1), Chakar cycle
    # (P1.3) for the ascendant sign, and any downstream consumer.
    try:
        _raw_chart = row["chart_data"]
        chart_data = json.loads(_raw_chart) if isinstance(_raw_chart, str) else (_raw_chart or {})
    except (json.JSONDecodeError, TypeError, KeyError):
        chart_data = {}

    # P1.1 — Modified Analytical Tewa needs Andhe Grah detection on every
    # chart (not just remedies). Wire the blind-planet detector into the
    # /advanced endpoint so the Tewa tab can colour-code planets by state.
    from app.lalkitab_andhe_grah import detect_andhe_grah
    andhe_info = detect_andhe_grah(formatted_positions, chart_data=chart_data)

    # P1.5 — Rahu-Ketu 1-7 axis (shadow axis) canonical combined effect.
    # LK 1952 §2.17: Rahu and Ketu always sit 180° apart, so they are
    # always in a 1-7 relationship. LK prescribes specific combined
    # effects on BOTH endpoint houses for each of the 6 unique axis
    # configurations. Non-fatal — detector returns None if either node
    # is missing or the data is not a clean 1-7 pair.
    try:
        from app.lalkitab_rahu_ketu_axis import detect_rahu_ketu_axis
        rahu_ketu_axis = detect_rahu_ketu_axis(formatted_positions)
    except Exception as e:
        logger.warning("Rahu-Ketu axis detection failed: %s", e)
        rahu_ketu_axis = None

    # P1.3 — 35-Sala vs 36-Sala Chakar auto-determination.
    # Ascendant sign + planets occupying the 1st house drive the decision.
    try:
        from app.lalkitab_chakar import detect_chakar_cycle
        asc_sign = (chart_data.get("ascendant") or {}).get("sign", "") if isinstance(chart_data, dict) else ""
        planets_in_h1 = [
            p["planet"] for p in formatted_positions
            if int(p.get("house") or 0) == 1
        ]
        chakar_cycle = detect_chakar_cycle(asc_sign, planets_in_h1)
    except Exception as e:
        logger.warning("Chakar cycle detection failed: %s", e)
        chakar_cycle = None

    # P1.4 — Day + Time (Hora) planet — non-remediable fate signature (LK 2.16).
    # Reuses the Hora sunrise we already computed (when available) so both
    # engines agree on the Hora lord.
    try:
        from app.lalkitab_time_planet import detect_time_planet
        sunrise_hms_val = None
        try:
            _srt = locals().get("sunrise_time_obj")
            if _srt is not None:
                sunrise_hms_val = _srt.strftime("%H:%M:%S")
        except Exception:
            sunrise_hms_val = None

        time_planet_info = detect_time_planet(
            birth_date_iso=row["birth_date"],
            birth_time_hms=row["birth_time"],
            sunrise_hms=sunrise_hms_val,
            allow_sunrise_fallback=True,
        )
    except Exception as e:
        logger.warning("Time-planet detection failed: %s", e)
        time_planet_info = None

    return {
        "masnui_planets": calculate_masnui_planets(formatted_positions),
        "karmic_debts": hora_debt_analysis["final_debts"] if hora_debt_analysis else calculate_karmic_debts(formatted_positions),
        "karmic_debts_hora_analysis": hora_debt_analysis,
        "hora_debt_available": hora_debt_available,
        "hora_debt_reason": hora_debt_reason,
        "teva_type": identify_teva_type(formatted_positions),
        "prohibitions": get_prohibitions(formatted_positions),
        "aspects": lk_aspects,
        "sleeping": sleeping_info,
        "kayam": kayam_planets,
        # P1.1 — per-planet blind-planet state for Analytical Tewa colour coding
        "andhe": andhe_info,
        # P1.5 — canonical Rahu-Ketu 1-7 axis combined effect (LK 2.17)
        "rahu_ketu_axis": rahu_ketu_axis,
        # P1.3 — 35-Sala vs 36-Sala Chakar cycle determination
        "chakar_cycle": chakar_cycle,
        # P1.4 — Day + Time (Hora) planet (non-remediable fate signature)
        "time_planet": time_planet_info,
    }


# ─────────────────────────────────────────────────────────────
# P1.12 — Chandra Kundali as INDEPENDENT LK framework (LK 1952)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/chandra-kundali/{kundli_id}")
def get_chandra_kundali(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Return the Chandra Kundali (Moon-chart) read as an INDEPENDENT LK
    predictive framework — per LK 1952 canon.

    Unlike the Vedic practice of shifting house numbers with the SAME
    interpretation table, this endpoint:
      1. Re-anchors all planets so Moon becomes H1 of the Chandra chart.
      2. Uses LK-specific Chandra readings (emotion / mother / mental states
         focus) — NOT copied from the Lagna interpretation table.
      3. Cross-checks every planet's Lagna vs Chandra reading and flags
         meaningful disagreements so the native sees both voices.
    """
    from app.lalkitab_chandra_kundali import compute_chandra_kundali

    positions, _row = _get_lk_positions(kundli_id, user["sub"], db)
    if not positions:
        raise HTTPException(
            status_code=400,
            detail="No valid planet positions in chart",
        )

    # Find Moon's natal house — required anchor.
    moon_house = next(
        (p["house"] for p in positions if p.get("planet") == "Moon"),
        None,
    )
    if not isinstance(moon_house, int) or not (1 <= moon_house <= 12):
        raise HTTPException(
            status_code=422,
            detail="Moon position not available — Chandra Kundali cannot be computed",
        )

    lagna_interps = get_all_interpretations_for_chart(positions)

    return compute_chandra_kundali(
        positions,
        moon_house,
        lagna_interpretations=lagna_interps,
    )


# ─────────────────────────────────────────────────────────────
# Lal Kitab Bunyaad / Takkar / Enemy Presence Analysis
# ─────────────────────────────────────────────────────────────

@router.post("/api/lalkitab/lk-analysis")
@router.post("/api/kp-lalkitab/lk-analysis")
def lk_analysis(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Combined Lal Kitab analysis: Bunyaad (Foundation), Takkar (Collision), Enemy Presence.

    Contract input: {kundli_id}
    Returns bunyaad, takkar, and enemy_presence results.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    # Build formatted_positions matching the pattern used by advanced endpoint
    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        # Unified derivation: prefer explicit house, fall back to sign
        house = _derive_lk_house(info)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        bunyaad = calculate_bunyaad(formatted_positions)
        takkar = calculate_takkar(formatted_positions)
        enemy_presence = calculate_enemy_presence(formatted_positions)
    except Exception as exc:
        logger.error("LK analysis error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {
        "bunyaad": bunyaad,
        "takkar": takkar,
        "enemy_presence": enemy_presence,
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab House-by-House Planet Interpretations
# ─────────────────────────────────────────────────────────────

@router.post("/api/lalkitab/lk-interpretations")
@router.post("/api/kp-lalkitab/lk-interpretations")
def lk_interpretations(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Return per-house Lal Kitab interpretations for every planet in the kundli.

    Contract input: {kundli_id}
    Returns list of interpretation dicts with nature, effect_en/hi, conditions, keywords.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        # Unified derivation: prefer explicit house, fall back to sign
        house = _derive_lk_house(info)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        interpretations = get_all_interpretations_for_chart(formatted_positions)
    except Exception as exc:
        logger.error("LK interpretations error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {"interpretations": interpretations}


@router.post("/api/lalkitab/lk-validated-remedies")
@router.post("/api/kp-lalkitab/lk-validated-remedies")
def lk_validated_remedies(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Return applicable validated Lal Kitab remedies based on planet positions.

    Contract input: {kundli_id}
    Returns list of remedy dicts with name, procedure, validation status.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        # Unified derivation: prefer explicit house, fall back to sign
        house = _derive_lk_house(info)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        remedies = get_lk_validated_remedies(formatted_positions)
    except Exception as exc:
        logger.error("LK validated remedies error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    # Codex D6 — enrich each validated remedy with the Savdhaniyan
    # safety bundle + Andhe-Grah warning, so UIs rendering validated
    # remedies get the same LK 4.08/4.09/4.14 protection as /enriched.
    from app.lalkitab_savdhaniyan import get_remedy_precautions
    from app.lalkitab_andhe_grah import detect_andhe_grah
    andhe = detect_andhe_grah(formatted_positions)
    blind_map = andhe.get("per_planet") or {}

    def _enrich(r: dict) -> dict:
        planet = r.get("for_planet") or r.get("planet") or ""
        if not planet:
            return r
        # Find the planet's LK house from the positions list.
        house = next(
            (p.get("house") for p in formatted_positions if p.get("planet") == planet),
            None,
        )
        precaution_bundle = get_remedy_precautions(
            planet,
            house=house,
            remedy_material=r.get("material", "") if isinstance(r, dict) else "",
        )
        blind_info = blind_map.get(planet) or {}
        andhe_warning = None
        if blind_info.get("is_blind"):
            andhe_warning = {
                "kind": "blind_planet",
                "severity": blind_info.get("severity"),
                "reasons": blind_info.get("reasons"),
                "en": blind_info.get("warning_en"),
                "hi": blind_info.get("warning_hi"),
                "lk_ref": "4.14",
            }
        # P1.11 — classify the remedy tier (trial / remedy / good_conduct).
        from app.lalkitab_remedy_classifier import (
            classify_remedy, classification_label, classification_description,
        )
        cls_input = {
            "en": r.get("en") or r.get("text") or r.get("remedy_text") or "",
            "hi": r.get("hi") or "",
            "material": r.get("material") or r.get("remedy_type") or "",
        }
        cls = classify_remedy(cls_input)
        return {
            **r,
            "savdhaniyan": precaution_bundle,
            "time_rule": precaution_bundle["time_rule"],
            "reversal_risk": precaution_bundle["reversal_risk"],
            "andhe_grah_warning": andhe_warning,
            # P1.11 tier classification
            "classification": cls,
            "classification_en": classification_label(cls, is_hi=False),
            "classification_hi": classification_label(cls, is_hi=True),
            "classification_desc_en": classification_description(cls, is_hi=False),
            "classification_desc_hi": classification_description(cls, is_hi=True),
        }

    remedies = [_enrich(r) for r in (remedies or [])]
    return {"remedies": remedies}


# ─────────────────────────────────────────────────────────────
# Saved Predictions (Bookmark)
# ─────────────────────────────────────────────────────────────

@router.post("/api/lalkitab/predictions/save")
def save_prediction(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Save a prediction bookmark. payload: {kundli_id, prediction_type, prediction_data, note}"""
    kundli_id = payload.get("kundli_id")
    prediction_type = payload.get("prediction_type", "").strip()
    prediction_data = payload.get("prediction_data", {})
    note = (payload.get("note") or "").strip()

    if not kundli_id or not prediction_type:
        raise HTTPException(status_code=400, detail="kundli_id and prediction_type required")

    db.execute(
        "INSERT INTO saved_predictions (user_id, kundli_id, prediction_type, prediction_data, note) "
        "VALUES (%s, %s, %s, %s, %s)",
        (user["sub"], kundli_id, prediction_type, json.dumps(prediction_data), note),
    )
    db.commit()
    return {"ok": True}


@router.get("/api/lalkitab/predictions/saved/{kundli_id}")
def get_saved_predictions(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return all saved predictions for a kundli."""
    rows = db.execute(
        "SELECT id, prediction_type, prediction_data, note, created_at "
        "FROM saved_predictions WHERE user_id = %s AND kundli_id = %s ORDER BY created_at DESC",
        (user["sub"], kundli_id),
    ).fetchall()

    predictions = []
    for r in rows:
        predictions.append({
            "id": r["id"],
            "prediction_type": r["prediction_type"],
            "prediction_data": json.loads(r["prediction_data"]) if r["prediction_data"] else {},
            "note": r["note"],
            "created_at": r["created_at"].isoformat() if r["created_at"] else None,
        })

    return {"predictions": predictions}


@router.delete("/api/lalkitab/predictions/saved/{prediction_id}")
def delete_saved_prediction(
    prediction_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Delete a saved prediction by ID (owner-only)."""
    result = db.execute(
        "DELETE FROM saved_predictions WHERE id = %s AND user_id = %s",
        (prediction_id, user["sub"]),
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"ok": True}


# ─────────────────────────────────────────────────────────────
# Prashna Quick — public, no auth, auto-number
# ─────────────────────────────────────────────────────────────

@router.post("/api/prashna/quick")
async def prashna_quick(body: PrashnaQuickRequest):
    """Public Prashna Kundli — no login required.
    KP horary number is derived from the sidereal ascendant at query moment (KP tradition).
    Accepts question_type + optional city/coordinates.
    """
    now = _datetime.now()
    query_dt = now.strftime("%Y-%m-%d %H:%M:%S")

    lat, lon = body.latitude, body.longitude
    if (lat is None or lon is None) and body.city:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                r = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": body.city, "format": "json", "limit": 1},
                    headers={"User-Agent": "AstroRattan/1.0"},
                )
                results = r.json()
                if results:
                    lat = float(results[0]["lat"])
                    lon = float(results[0]["lon"])
        except Exception:
            pass

    query_place = {
        "latitude": lat if lat is not None else 28.6139,
        "longitude": lon if lon is not None else 77.2090,
        "tz_offset": 5.5,
    }

    # Derive prashna number from sidereal ASC at query moment (KP tradition).
    # Each of the 249 KP sub-divisions spans 360/249 = 1°26'40". The querent's
    # number is determined by which sub-division the ASC falls in at query time.
    number_source = "timestamp_fallback"
    number = (int(now.timestamp()) % 249) + 1  # fallback
    try:
        import swisseph as _swe
        import datetime as _dt_mod
        tz_h = query_place.get("tz_offset", 5.5)
        utc = now - _dt_mod.timedelta(hours=tz_h)
        jd = _swe.julday(utc.year, utc.month, utc.day,
                         utc.hour + utc.minute / 60.0 + utc.second / 3600.0)
        _swe.set_sid_mode(_swe.SIDM_LAHIRI)
        _, ascmc = _swe.houses(jd, query_place["latitude"], query_place["longitude"], b"P")
        asc_sid = (ascmc[0] - _swe.get_ayanamsa(jd)) % 360.0
        number = max(1, min(249, int(asc_sid * 249 / 360) + 1))
        number_source = "ascendant"
    except Exception:
        pass

    try:
        chart = get_horary_prediction(
            number=number,
            question_type=body.question_type,
            query_datetime=query_dt,
            query_place=query_place,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        logger.error("Prashna quick error: %s", exc)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Calculation error — please try again")

    pred = chart.get("prediction", {}) or {}
    return {
        "number": number,
        "number_source": number_source,
        "question_type": body.question_type,
        "verdict": pred.get("verdict", "neutral"),
        "verdict_detail": pred.get("verdict_detail", ""),
        "timing": pred.get("timing", ""),
        "description": pred.get("description", ""),
        "sub_lord_of_cusp": pred.get("sub_lord_of_cusp", ""),
        "cusp_checked": pred.get("cusp_checked", 0),
        "queried_at": query_dt,
    }


# ─────────────────────────────────────────────────────────────
# KP Horary (Prashna) — 1-249 Number System
# ─────────────────────────────────────────────────────────────

@router.post("/api/kp/horary")
def kp_horary(
    body: KPHoraryRequest,
    user: dict = Depends(get_current_user),
):
    """
    Calculate a full KP Horary chart from querent's number (1-249).

    Returns horary number details, house cusps, planets with star/sub lords,
    significators, and ruling planets for the query moment.
    """
    try:
        result = calculate_kp_horary(
            number=body.number,
            query_datetime=body.query_datetime,
            query_place=body.query_place,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("KP Horary calculation error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


@router.post("/api/kp/horary/predict")
def kp_horary_predict(
    body: KPHoraryPredictRequest,
    user: dict = Depends(get_current_user),
):
    """
    Get a KP Horary prediction for a specific question type.

    Supported question types: marriage, job, travel, health, finance,
    legal, education, property.

    Returns full horary chart plus prediction analysis with verdict
    (favorable / unfavorable / mixed) and timing estimate.
    """
    try:
        result = get_horary_prediction(
            number=body.number,
            question_type=body.question_type,
            query_datetime=body.query_datetime,
            query_place=body.query_place,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("KP Horary prediction error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


# ═══════════════════════════════════════════════════════════════════
# HELPER — extract LK planet positions from kundli_id
# ═══════════════════════════════════════════════════════════════════

def _get_lk_positions(kundli_id: str, user_sub: str, db: Any):
    """Load kundli from DB, convert to LK planet-position list."""
    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_sub),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")
    try:
        raw = row["chart_data"]
        chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=500, detail="Corrupt chart data")
    positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        if not isinstance(info, dict):
            continue
        house = _derive_lk_house(info)
        if house > 0:
            positions.append({"planet": planet_name, "house": house})
    return positions, row


# ═══════════════════════════════════════════════════════════════════
# PALMISTRY (Samudrik Shastra)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/palm/zones")
def get_palm_zones():
    """Return all palm zones (mounts + lines) with planet/house mappings. No auth required."""
    from app.lalkitab_palmistry import get_palm_zones as _zones, MARK_TYPES
    return {"zones": _zones(), "mark_types": MARK_TYPES}


@router.post("/api/lalkitab/palm/correlate")
def correlate_palm_marks(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    payload: {kundli_id, palm_marks: [{zone_id, mark_type}]}
    Returns palm-to-chart correlations with interpretations and remedies.
    """
    from app.lalkitab_palmistry import calculate_palm_correlations
    kundli_id = payload.get("kundli_id")
    marks = payload.get("palm_marks", payload.get("marks", []))  # accept both keys
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id required")
    if not isinstance(marks, list):
        raise HTTPException(status_code=400, detail="palm_marks must be a list")
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return calculate_palm_correlations(positions, marks)


# ═══════════════════════════════════════════════════════════════════
# AGE MILESTONE TRIGGERS (Safar-e-Zindagi)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/milestones/{kundli_id}")
def get_age_milestones(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Safar-e-Zindagi age milestone analysis with countdown to next trigger."""
    from app.lalkitab_milestones import calculate_age_milestones
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    birth_date = str(row.get("birth_date") or row.get("dob") or "").strip()
    if not birth_date:
        try:
            raw = row["chart_data"]
            cd = json.loads(raw) if isinstance(raw, str) else (raw or {})
            birth_date = cd.get("birth_date", "")
        except Exception:
            birth_date = ""
    if not birth_date:
        raise HTTPException(status_code=422, detail="birth_date not found in kundli")
    return calculate_age_milestones(birth_date, positions)


# ═══════════════════════════════════════════════════════════════════
# TECHNICAL LOGIC (Chalti Gaadi, Dhur-Dhur-Aage, Soya Ghar)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/technical/{kundli_id}")
def get_technical_analysis(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Chalti Gaadi, Dhur-Dhur-Aage, Soya Ghar, Planet Statuses, Muththi and Kayam Grah analysis."""
    from app.lalkitab_technical import (
        calculate_chalti_gaadi,
        calculate_dhur_dhur_aage,
        calculate_soya_ghar,
        classify_all_planet_statuses,
        calculate_muththi,
    )
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    lk_aspects = calculate_lk_aspects(positions)
    return {
        "chalti_gaadi": calculate_chalti_gaadi(positions),
        "dhur_dhur_aage": calculate_dhur_dhur_aage(positions),
        "soya_ghar": calculate_soya_ghar(positions),
        "planet_statuses": classify_all_planet_statuses(positions),
        "muththi": calculate_muththi(positions),
        "kayam": calculate_kayam_grah(positions, lk_aspects),
    }


# ═══════════════════════════════════════════════════════════════════
# BALI KA BAKRA (Sacrifice Analysis)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/sacrifice/{kundli_id}")
def get_sacrifice_analysis(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Bali Ka Bakra sacrifice chain analysis for this chart."""
    from app.lalkitab_sacrifice import analyze_sacrifice
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    results = analyze_sacrifice(positions)
    return {
        "kundli_id": kundli_id,
        "sacrifice_count": len(results),
        "has_sacrifices": len(results) > 0,
        "results": results,
    }


# ═══════════════════════════════════════════════════════════════════
# FORBIDDEN REMEDIES
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/forbidden/{kundli_id}")
def get_forbidden_list(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return dynamic forbidden actions list based on this chart's planet placements."""
    from app.lalkitab_forbidden import get_forbidden_remedies
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    results = get_forbidden_remedies(positions)
    return {
        "kundli_id": kundli_id,
        "forbidden_count": len(results),
        "rules": results,
    }


# ═══════════════════════════════════════════════════════════════════
# FAMILY CHART LINKING (Grah-Gasti)
# ═══════════════════════════════════════════════════════════════════

def _positions_from_chart(chart_data: dict) -> list:
    """Parse planet positions from a chart_data dict (no DB lookup)."""
    positions = []
    for planet_name, info in (chart_data or {}).get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS or not isinstance(info, dict):
            continue
        house = _derive_lk_house(info)
        if house > 0:
            positions.append({"planet": planet_name, "house": house})
    return positions


@router.get("/api/lalkitab/family/{kundli_id}")
def get_family_links(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return family chart links with per-member harmony analysis."""
    from app.lalkitab_family import calculate_family_harmony, get_family_dominant_planet, get_family_theme

    owner_row = db.execute(
        "SELECT id, chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not owner_row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    try:
        raw = owner_row["chart_data"]
        owner_chart = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        owner_chart = {}
    owner_positions = _positions_from_chart(owner_chart)

    links = db.execute(
        """SELECT lf.id AS link_id, lf.member_kundli_id, lf.relation,
                  k.person_name, k.birth_date, k.chart_data
           FROM lal_kitab_family_links lf
           JOIN kundlis k ON k.id = lf.member_kundli_id
           WHERE lf.owner_kundli_id = %s AND lf.user_id = %s
           ORDER BY lf.created_at""",
        (kundli_id, user["sub"]),
    ).fetchall()

    linked_members = []
    all_scores = []
    all_positions = list(owner_positions)

    for link in links:
        try:
            raw_m = link["chart_data"]
            member_chart = json.loads(raw_m) if isinstance(raw_m, str) else (raw_m or {})
        except Exception:
            member_chart = {}
        member_positions = _positions_from_chart(member_chart)
        harmony = calculate_family_harmony(owner_positions, member_positions, member_name=link["person_name"])
        all_scores.append(harmony["harmony_score"])
        all_positions.extend(member_positions)
        linked_members.append({
            "link_id": link["link_id"],
            "kundli_id": link["member_kundli_id"],
            "name": link["person_name"],
            "relation": link["relation"],
            "birth_date": link["birth_date"],
            "harmony_score": harmony["harmony_score"],
            "shared_planets": harmony["shared_planets"],
            "support_planets": harmony["support_planets"],
            "tension_planets": harmony["tension_planets"],
            "theme": harmony["theme"],
            "cross_waking_narratives": harmony["cross_waking_narratives"],
        })

    avg_score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
    dominant_planet = get_family_dominant_planet(all_positions) if all_positions else None
    family_theme = get_family_theme(avg_score) if all_scores else None

    return {
        "kundli_id": kundli_id,
        "linked_members": linked_members,
        "family_harmony": avg_score,
        "dominant_planet": dominant_planet,
        "family_theme": family_theme,
    }


@router.post("/api/lalkitab/family/{kundli_id}/link")
def add_family_link(
    kundli_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Link a family member kundli to the owner kundli. payload: {member_kundli_id, relation}"""
    member_kundli_id = payload.get("member_kundli_id", "").strip()
    relation = payload.get("relation", "family").strip()
    if not member_kundli_id:
        raise HTTPException(status_code=400, detail="member_kundli_id required")
    if member_kundli_id == kundli_id:
        raise HTTPException(status_code=400, detail="Cannot link kundli to itself")

    owner = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner kundli not found")

    member = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (member_kundli_id, user["sub"]),
    ).fetchone()
    if not member:
        raise HTTPException(status_code=404, detail="Member kundli not found or not yours")

    try:
        row = db.execute(
            """INSERT INTO lal_kitab_family_links (owner_kundli_id, member_kundli_id, relation, user_id)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (owner_kundli_id, member_kundli_id) DO UPDATE SET relation = EXCLUDED.relation
               RETURNING id""",
            (kundli_id, member_kundli_id, relation, user["sub"]),
        ).fetchone()
        db.commit()
    except Exception as e:
        logger.warning("[family_link] insert error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to create link")

    return {"link_id": row["id"], "status": "linked"}


@router.delete("/api/lalkitab/family/{kundli_id}/link/{link_id}")
def remove_family_link(
    kundli_id: str,
    link_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Remove a family member link."""
    row = db.execute(
        """DELETE FROM lal_kitab_family_links
           WHERE id = %s AND owner_kundli_id = %s AND user_id = %s
           RETURNING id""",
        (link_id, kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Link not found")
    db.commit()
    return {"status": "unlinked"}


# ═══════════════════════════════════════════════════════════════════
# VASTU DIRECTIONAL DIAGNOSIS (Makaan)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/vastu/{kundli_id}")
def get_vastu_diagnosis_route(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Vastu home-layout diagnosis from LK planet positions."""
    from app.lalkitab_vastu import get_vastu_diagnosis
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return get_vastu_diagnosis(positions)


# ═══════════════════════════════════════════════════════════════════
# 7-YEAR SUB-CYCLE
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/seven-year-cycle/{kundli_id}")
def get_seven_year_cycle_route(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the active 7-year sub-cycle for a kundli."""
    from app.lalkitab_milestones import get_seven_year_cycle
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    birth_date_str = row.get("birth_date", "")
    try:
        from datetime import date
        bdate = _date.fromisoformat(birth_date_str)
        current_age = (date.today() - bdate).days // 365
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="birth_date missing or invalid — cannot compute seven-year cycle",
        )
    return get_seven_year_cycle(current_age, positions)


# ═══════════════════════════════════════════════════════════════════
# DHOKA (DECEPTION) + ACHANAK CHOT (SUDDEN STRIKE)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/relationship-engine/{kundli_id}")
def get_relationship_engine(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Returns Takkar, Dhoka, Achanak Chot, and Bunyaad analysis."""
    from app.lalkitab_advanced import calculate_takkar, calculate_bunyaad, calculate_dhoka, calculate_achanak_chot
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return {
        "takkar":      calculate_takkar(positions),
        "dhoka":       calculate_dhoka(positions),
        "achanak_chot": calculate_achanak_chot(positions),
        "bunyaad":     calculate_bunyaad(positions),
    }


# ═══════════════════════════════════════════════════════════════════
# ACTIVE vs PASSIVE RIN
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/rin-active/{kundli_id}")
def get_active_rin(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Returns karmic debts with active/passive activation status.

    P1.10 — now also consults the current Saala Grah (annual ruling
    planet) via lalkitab_dasha.get_dasha_timeline so Rins whose
    activating_planet matches the current dasha get a dasha_active=True
    overlay with urgency escalation.
    """
    from app.lalkitab_advanced import calculate_karmic_debts, enrich_debts_active_passive
    from app.lalkitab_compound_debt import rank_compound_debts
    from app.lalkitab_dasha import get_dasha_timeline
    from datetime import date as _date
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    debts = calculate_karmic_debts(positions)

    # ── P1.10 — resolve current Saala Grah if birth_date is available ──
    current_dasha_lord = None
    upcoming_dasha_lords = None
    try:
        birth_date = str(row.get("birth_date") or row.get("dob") or "").strip()
        if not birth_date:
            raw = row.get("chart_data")
            cd = json.loads(raw) if isinstance(raw, str) else (raw or {})
            birth_date = cd.get("birth_date", "")
        if birth_date:
            timeline = get_dasha_timeline(birth_date, _date.today().isoformat())
            current_dasha_lord = (timeline.get("current_saala_grah") or {}).get("planet")
            upcoming_dasha_lords = timeline.get("upcoming_periods") or []
    except Exception:
        # If anything in the dasha lookup fails we still return the
        # natal-only enrichment — the dasha overlay is additive.
        current_dasha_lord = None
        upcoming_dasha_lords = None

    enriched = enrich_debts_active_passive(
        debts, positions,
        current_dasha_lord=current_dasha_lord,
        upcoming_dasha_lords=upcoming_dasha_lords,
    )
    # P2.9 — compound-debt priority analysis (LK canon Rina-Shodhan Krama).
    # Keeps the existing `debts` list contract but additionally returns a
    # `compound_analysis` payload with ranked order, clusters, and
    # blocked-by relationships. The ranked list is a separate copy —
    # `debts` order is untouched for backwards compatibility.
    try:
        compound_analysis = rank_compound_debts(enriched, positions)
    except Exception:
        # Non-fatal — the raw debt list still ships.
        compound_analysis = None

    afflicted_planets = sorted({
        str(d.get("planet") or "").lower()
        for d in enriched
        if d.get("activation_status") == "active" or d.get("dasha_active")
        if d.get("planet")
    })

    return {
        "debts": enriched,
        "afflicted_planets": afflicted_planets,
        "current_dasha_lord": current_dasha_lord,
        "compound_analysis": compound_analysis,
    }


# ═══════════════════════════════════════════════════════════════════
# 43-DAY REMEDY TRACKER
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/remedy-tracker/{kundli_id}")
def list_remedy_trackers(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all remedy trackers for a kundli."""
    rows = db.execute(
        "SELECT * FROM remedy_trackers WHERE user_id = %s AND kundli_id = %s ORDER BY created_at DESC",
        (user["sub"], kundli_id),
    ).fetchall()
    result = []
    for r in rows:
        try:
            check_ins = json.loads(r["check_ins"]) if r["check_ins"] else []
        except Exception:
            check_ins = []
        result.append({
            "id": r["id"],
            "remedy_title": r["remedy_title"],
            "remedy_description": r["remedy_description"],
            "planet": r["planet"],
            "started_at": str(r["started_at"]),
            "target_days": r["target_days"],
            "completed_days": r["completed_days"],
            "check_ins": check_ins,
            "status": r["status"],
            "progress_pct": round(r["completed_days"] / r["target_days"] * 100) if r["target_days"] > 0 else 0,
        })
    return {"trackers": result}


@router.post("/api/lalkitab/remedy-tracker/{kundli_id}")
def create_remedy_tracker(
    kundli_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Start a new 43-day remedy tracker."""
    title = payload.get("remedy_title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="remedy_title required")
    # Verify kundli ownership
    k = db.execute("SELECT id FROM kundlis WHERE id = %s AND user_id = %s", (kundli_id, user["sub"])).fetchone()
    if not k:
        raise HTTPException(status_code=404, detail="Kundli not found")
    from datetime import date as _date_cls
    started_at = payload.get("started_at") or str(_date_cls.today())
    row = db.execute(
        """INSERT INTO remedy_trackers
           (user_id, kundli_id, remedy_title, remedy_description, planet, started_at, target_days)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (user["sub"], kundli_id, title,
         payload.get("remedy_description", ""),
         payload.get("planet"),
         started_at,
         int(payload.get("target_days", 43))),
    ).fetchone()
    db.commit()
    return {"tracker_id": row["id"], "status": "created"}


@router.post("/api/lalkitab/remedy-tracker/{tracker_id}/checkin")
def checkin_remedy_tracker(
    tracker_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Mark today as completed for a tracker.

    P0.5 — LK 4.10 enforcement: if there's a gap between the last check-in
    and today (≥2 days elapsed since last check-in), the chain is
    automatically broken per Lal Kitab 1952 canon ("the 43-day bond
    requires continuity; a single missed day voids the entire cycle").
    The user cannot override this — the restart is mandatory.

    If 'missed' is True in payload, status becomes 'broken' and completed_days resets.
    """
    from datetime import date as _date_cls, timedelta as _timedelta
    today_obj = _date_cls.today()
    today = str(today_obj)
    row = db.execute(
        "SELECT * FROM remedy_trackers WHERE id = %s AND user_id = %s",
        (tracker_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tracker not found")
    if row["status"] not in ("active", "paused"):
        raise HTTPException(status_code=400, detail=f"Tracker is {row['status']} — cannot check in")
    try:
        check_ins = json.loads(row["check_ins"]) if row["check_ins"] else []
    except Exception:
        check_ins = []
    missed = payload.get("missed", False)
    if missed:
        # Explicit self-reported miss — same reset path as auto-detect.
        db.execute(
            "UPDATE remedy_trackers SET status='broken', completed_days=0, check_ins='[]', updated_at=NOW() WHERE id=%s",
            (tracker_id,),
        )
        db.commit()
        return {
            "status": "broken",
            "completed_days": 0,
            "target_days": row["target_days"],
            "progress_pct": 0,
            "days_remaining": row["target_days"],
            "broken_reason": "self_reported_miss",
            "restart_alert": {
                "en": (
                    "43-day chain broken. Per LK 4.10, the remedy must be restarted from day 1 "
                    "with fresh resolve — partial credit is not permitted in Lal Kitab canon."
                ),
                "hi": (
                    "43-दिन की श्रृंखला टूट गई। लाल किताब 4.10 के अनुसार उपाय को दिन 1 से नए "
                    "संकल्प के साथ पुनः आरंभ करना होगा — आंशिक प्रगति लाल किताब में मान्य नहीं।"
                ),
            },
            "lk_ref": "4.10",
        }

    # ── P0.5 auto-gap detection ──
    # Compute the gap (in days) between the most recent check-in and today.
    # Any gap >= 2 days (i.e. user skipped at least one full day) triggers
    # the automatic reset. A gap of 0 (checking in again the same day) or
    # 1 (checked in yesterday) is valid continuity.
    auto_break = False
    auto_break_reason = None
    if check_ins:
        try:
            last_str = sorted(check_ins)[-1]
            last_obj = _date_cls.fromisoformat(last_str)
            gap_days = (today_obj - last_obj).days
            if gap_days >= 2:
                auto_break = True
                auto_break_reason = f"gap_{gap_days}_days"
        except (ValueError, TypeError):
            # Corrupt check_in entry — don't penalise the user.
            pass

    if auto_break:
        db.execute(
            "UPDATE remedy_trackers SET status='broken', completed_days=0, check_ins='[]', updated_at=NOW() WHERE id=%s",
            (tracker_id,),
        )
        db.commit()
        return {
            "status": "broken",
            "completed_days": 0,
            "target_days": row["target_days"],
            "progress_pct": 0,
            "days_remaining": row["target_days"],
            "broken_reason": auto_break_reason,
            "restart_alert": {
                "en": (
                    f"Chain automatically broken — a gap was detected since your last check-in. "
                    f"Per LK 4.10, the 43-day remedy requires unbroken continuity. "
                    f"Restart from day 1 whenever you are ready; the progress counter has been reset."
                ),
                "hi": (
                    f"श्रृंखला स्वचालित रूप से टूटी — पिछले चेक-इन के बाद अंतराल पाया गया। "
                    f"लाल किताब 4.10 के अनुसार 43-दिन का उपाय बिना रुकावट होना चाहिए। "
                    f"जब तैयार हों दिन 1 से पुनः आरंभ करें; प्रगति रीसेट कर दी गई है।"
                ),
            },
            "lk_ref": "4.10",
        }

    if today not in check_ins:
        check_ins.append(today)
    completed = len(check_ins)
    new_status = "completed" if completed >= row["target_days"] else "active"
    db.execute(
        "UPDATE remedy_trackers SET completed_days=%s, check_ins=%s, status=%s, updated_at=NOW() WHERE id=%s",
        (completed, json.dumps(check_ins), new_status, tracker_id),
    )
    db.commit()
    return {
        "status": new_status,
        "completed_days": completed,
        "target_days": row["target_days"],
        "progress_pct": round(completed / row["target_days"] * 100),
        "days_remaining": max(0, row["target_days"] - completed),
    }


@router.get("/api/lalkitab/remedy-tracker/{tracker_id}/risk")
def remedy_tracker_risk(
    tracker_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    P0.5 — Passive risk check. Returns a "warning" / "at_risk" / "safe" signal
    based on how long it's been since the last check-in, so the UI can show
    an escalating alert BEFORE the chain is auto-broken.

      safe     — checked in today or yesterday (≤ 1 day gap)
      warning  — not checked in today; chain still intact
      at_risk  — already a gap; one more missed day triggers auto-break
      broken   — chain is already broken (auto or manual)
    """
    from datetime import date as _date_cls
    today_obj = _date_cls.today()
    row = db.execute(
        "SELECT * FROM remedy_trackers WHERE id = %s AND user_id = %s",
        (tracker_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tracker not found")

    if row["status"] == "broken":
        return {
            "risk": "broken",
            "gap_days": None,
            "message_en": "Chain already broken — restart to resume tracking.",
            "message_hi": "श्रृंखला टूट चुकी है — ट्रैकिंग फिर से शुरू करें।",
            "lk_ref": "4.10",
        }
    if row["status"] == "completed":
        return {
            "risk": "safe",
            "gap_days": 0,
            "message_en": "43-day cycle complete — no further check-ins required.",
            "message_hi": "43-दिन का चक्र पूर्ण — अब चेक-इन की आवश्यकता नहीं।",
            "lk_ref": "4.10",
        }

    try:
        check_ins = json.loads(row["check_ins"]) if row["check_ins"] else []
    except Exception:
        check_ins = []

    if not check_ins:
        return {
            "risk": "warning",
            "gap_days": None,
            "message_en": "No check-ins yet — start today to begin the 43-day chain.",
            "message_hi": "अभी तक चेक-इन नहीं — 43-दिन की श्रृंखला आज से आरंभ करें।",
            "lk_ref": "4.10",
        }

    try:
        last_obj = _date_cls.fromisoformat(sorted(check_ins)[-1])
        gap = (today_obj - last_obj).days
    except (ValueError, TypeError):
        gap = 0

    if gap == 0:
        risk, en, hi = "safe", "Checked in today — chain intact.", "आज चेक-इन हो चुका है — श्रृंखला बनी हुई है।"
    elif gap == 1:
        risk, en, hi = (
            "warning",
            "You haven't checked in today. Check in before midnight to keep the 43-day chain alive.",
            "आज चेक-इन नहीं हुआ। श्रृंखला बनाए रखने के लिए आधी रात से पहले चेक-इन करें।",
        )
    else:
        # gap ≥ 2 — this is actually already broken; the next checkin call
        # will auto-reset. Flag it here so the UI can warn immediately.
        risk, en, hi = (
            "at_risk",
            f"{gap} days since last check-in — the next check-in will auto-reset the chain per LK 4.10.",
            f"पिछले चेक-इन के बाद {gap} दिन बीत गए — अगला चेक-इन लाल किताब 4.10 के अनुसार श्रृंखला को रीसेट कर देगा।",
        )

    return {
        "risk": risk,
        "gap_days": gap,
        "message_en": en,
        "message_hi": hi,
        "lk_ref": "4.10",
    }


@router.delete("/api/lalkitab/remedy-tracker/{tracker_id}")
def delete_remedy_tracker(
    tracker_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Delete a remedy tracker."""
    row = db.execute(
        "DELETE FROM remedy_trackers WHERE id=%s AND user_id=%s RETURNING id",
        (tracker_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tracker not found")
    db.commit()
    return {"status": "deleted"}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Saala Grah — 35-Year Dasha Timeline
# ─────────────────────────────────────────────────────────────
from app.lalkitab_dasha import get_dasha_timeline as _get_dasha_timeline
from datetime import date as _date_today


@router.get("/api/lalkitab/dasha/{kundli_id}")
def get_lk_dasha(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """LK Saala Grah (Year Ruler) Dasha timeline — which planet rules each year of life."""
    row = db.execute(
        "SELECT birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    result = _get_dasha_timeline(
        birth_date=str(row["birth_date"]),
        current_date=_date_today.today().isoformat(),
    )
    return result


# ─────────────────────────────────────────────────────────────
# Lal Kitab Prediction Feedback (per-kundli, per-area ratings)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/predictions/feedback/{kundli_id}")
def get_prediction_feedback(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return saved prediction feedback ratings for a kundli."""
    row = db.execute(
        "SELECT feedback FROM lk_prediction_feedback WHERE user_id = %s AND kundli_id = %s",
        (user["sub"], kundli_id),
    ).fetchone()
    return {"feedback": json.loads(row["feedback"]) if row else {}}


@router.post("/api/lalkitab/predictions/feedback")
def save_prediction_feedback(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Upsert prediction feedback ratings. payload: {kundli_id, feedback: {areaKey: rating}}"""
    kundli_id = payload.get("kundli_id")
    feedback = payload.get("feedback", {})
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id required")

    # Verify kundli ownership
    row = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    existing = db.execute(
        "SELECT id FROM lk_prediction_feedback WHERE user_id = %s AND kundli_id = %s",
        (user["sub"], kundli_id),
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE lk_prediction_feedback SET feedback = %s, updated_at = NOW() WHERE user_id = %s AND kundli_id = %s",
            (json.dumps(feedback), user["sub"], kundli_id),
        )
    else:
        db.execute(
            "INSERT INTO lk_prediction_feedback (user_id, kundli_id, feedback) VALUES (%s, %s, %s)",
            (user["sub"], kundli_id, json.dumps(feedback)),
        )
    db.commit()
    return {"ok": True}


# ═══════════════════════════════════════════════════════════════════
# DOSHA DETECTION
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/doshas/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_doshas(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Detect Lal Kitab doshas from the kundli's planet positions."""
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)

    from app.lalkitab_dosha import detect_lalkitab_doshas
    doshas = detect_lalkitab_doshas(positions)

    return {
        "kundli_id": kundli_id,
        "doshas": doshas,
        "total": len(doshas),
        "high_severity_count": sum(1 for d in doshas if d["severity"] == "high"),
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab Relations / Rules / Prediction Studio (Backend)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/relations/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_relations(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return conjunctions/aspects computed from the saved chart."""
    positions, _row = _get_lk_positions(kundli_id, user["sub"], db)
    planet_positions = {p["planet"].capitalize(): int(p["house"]) for p in positions if p.get("house")}
    from app.lalkitab_relations_engine import build_relations
    return {"kundli_id": kundli_id, **build_relations(planet_positions)}


@router.get("/api/lalkitab/rules/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_rules(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return mirror-axis + cross-rule triggers computed from the saved chart."""
    positions, _row = _get_lk_positions(kundli_id, user["sub"], db)
    planet_positions = {p["planet"].capitalize(): int(p["house"]) for p in positions if p.get("house")}
    from app.lalkitab_rules_engine import build_rules
    return {"kundli_id": kundli_id, **build_rules(planet_positions)}


@router.get("/api/lalkitab/predictions/studio/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_prediction_studio(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the general (multi-area) prediction studio scores computed from chart."""
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    planet_positions = {p["planet"].capitalize(): int(p["house"]) for p in positions if p.get("house")}

    raw = row["chart_data"]
    chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    planets = chart_data.get("planets", {}) if isinstance(chart_data, dict) else {}
    planet_lons = {}
    for pname, info in planets.items():
        if pname in _KNOWN_PLANETS and isinstance(info, dict):
            lon = info.get("longitude")
            if lon is not None:
                try:
                    planet_lons[pname] = float(lon)
                except Exception:
                    pass

    from app.lalkitab_prediction_studio import build_prediction_studio
    return {"kundli_id": kundli_id, **build_prediction_studio(planet_positions, planet_lons)}


@router.get("/api/lalkitab/age-activation/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_age_activation(
    kundli_id: str,
    as_of: str = None,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the Lal Kitab age activation buckets and current active planet."""
    row = db.execute(
        "SELECT birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")
    birth_date = str(row.get("birth_date") or "").strip()
    if not birth_date:
        raise HTTPException(status_code=400, detail="birth_date not available")
    from app.lalkitab_age_activation import get_age_activation
    return {"kundli_id": kundli_id, **get_age_activation(birth_date, as_of=as_of)}


# ═══════════════════════════════════════════════════════════════════
# CONSOLIDATED FULL ENDPOINT — eliminates 15+ waterfall API calls
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/full/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_full(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Consolidated Lal Kitab endpoint — returns all core analysis in one response.
    Eliminates waterfall of individual API calls from the frontend.

    Each section is independently try/except-wrapped so a single failure
    does not kill the entire response. Failed sections appear in _errors.
    """
    result = {
        "kundli_id": kundli_id,
        "positions": [],
        "advanced": None,
        "remedies": None,
        "dasha": None,
        "technical": None,
        "sacrifice": None,
        "forbidden": None,
        "milestones": None,
        "_errors": {},
    }

    # ── Positions (always needed — if this fails, bail out entirely) ──
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    result["positions"] = positions

    raw = row["chart_data"]
    chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    birth_date = str(row.get("birth_date") or row.get("dob") or "").strip()

    # Pre-compute formatted_positions used by multiple sections
    formatted_positions = [
        {"planet": p["planet"].capitalize(), "house": p["house"]}
        for p in positions
    ]

    # ── Advanced (masnui, karmic debts with hora, teva, prohibitions, etc.) ──
    try:
        # Hora-based karmic debts
        hora_debt_analysis = None
        hora_debt_available = False
        hora_debt_reason = None
        try:
            from datetime import datetime
            birth_datetime = datetime.combine(
                datetime.strptime(row["birth_date"], "%Y-%m-%d").date(),
                datetime.strptime(row["birth_time"], "%H:%M:%S").time()
            )
            sunrise_time_obj = None
            if row["latitude"] is None or row["longitude"] is None or row["timezone_offset"] is None:
                hora_debt_reason = "kundli missing location/timezone — Hora requires real birth coordinates"
            else:
                try:
                    from app.panchang_engine import _compute_sun_times
                    sun_times = _compute_sun_times(
                        row["birth_date"],
                        float(row["latitude"]),
                        float(row["longitude"]),
                        float(row["timezone_offset"]),
                    )
                    sr_str = sun_times.get("sunrise")
                    if sr_str and sr_str != "--:--":
                        sunrise_time_obj = datetime.strptime(sr_str, "%H:%M").time()
                except Exception as sr_exc:
                    logger.warning("full: Sunrise computation failed for Hora: %s", sr_exc)
                    hora_debt_reason = "sunrise computation failed"

            if sunrise_time_obj is None and hora_debt_reason is None:
                hora_debt_reason = "sunrise not available"

            hora_debt_analysis = calculate_karmic_debts_with_hora(
                formatted_positions,
                birth_datetime=birth_datetime,
                sunrise_time=sunrise_time_obj,
            )
            hora_info_local = (hora_debt_analysis or {}).get("hora_analysis") or {}
            if hora_info_local.get("_skipped"):
                hora_debt_available = False
                hora_debt_reason = hora_debt_reason or "sunrise not computed"
            else:
                hora_debt_available = True
        except Exception as e:
            logger.warning("full: Hora calculation failed: %s", e)
            hora_debt_reason = f"exception: {type(e).__name__}"

        lk_aspects = calculate_lk_aspects(formatted_positions)
        sleeping_info = calculate_sleeping_status(formatted_positions)
        kayam_planets = calculate_kayam_grah(formatted_positions, lk_aspects)

        result["advanced"] = {
            "masnui_planets": calculate_masnui_planets(formatted_positions),
            "karmic_debts": hora_debt_analysis["final_debts"] if hora_debt_analysis else calculate_karmic_debts(formatted_positions),
            "karmic_debts_hora_analysis": hora_debt_analysis,
            "hora_debt_available": hora_debt_available,
            "hora_debt_reason": hora_debt_reason,
            "teva_type": identify_teva_type(formatted_positions),
            "prohibitions": get_prohibitions(formatted_positions),
            "aspects": lk_aspects,
            "sleeping": sleeping_info,
            "kayam": kayam_planets,
        }
    except Exception as e:
        logger.warning("full: advanced section failed: %s", e, exc_info=True)
        result["_errors"]["advanced"] = str(e)

    # ── Remedies (enriched) ──
    try:
        planet_positions = {
            p: info.get("sign")
            for p, info in chart_data.get("planets", {}).items()
            if isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
        }
        if planet_positions:
            res = get_remedies(planet_positions, chart_data=chart_data)
            enriched = []
            for planet, info in res.items():
                r = info["remedy"]
                enriched.append({
                    "planet": planet,
                    "planet_hi": PLANET_NAMES_HI.get(planet, planet),
                    "sign": info["sign"],
                    "lk_house": info["lk_house"],
                    "dignity": info["dignity"],
                    "strength": info["strength"],
                    "has_remedy": info["has_remedy"],
                    "urgency": r.get("urgency", "low"),
                    "remedy_en": r.get("en", ""),
                    "remedy_hi": r.get("hi", ""),
                    "problem_en": r.get("problem_en", ""),
                    "problem_hi": r.get("problem_hi", ""),
                    "reason_en": r.get("reason_en", ""),
                    "reason_hi": r.get("reason_hi", ""),
                    "how_en": r.get("how_en", ""),
                    "how_hi": r.get("how_hi", ""),
                })
            urgency_order = {"high": 0, "medium": 1, "low": 2}
            enriched.sort(key=lambda x: (0 if x["has_remedy"] else 1, urgency_order.get(x["urgency"], 2), x["lk_house"]))
            result["remedies"] = {"remedies": enriched}
        else:
            result["_errors"]["remedies"] = "no planet positions with valid signs"
    except Exception as e:
        logger.warning("full: remedies section failed: %s", e, exc_info=True)
        result["_errors"]["remedies"] = str(e)

    # ── Dasha (Saala Grah timeline) ──
    try:
        if birth_date:
            result["dasha"] = _get_dasha_timeline(
                birth_date=birth_date,
                current_date=_date.today().isoformat(),
            )
        else:
            result["_errors"]["dasha"] = "birth_date not available"
    except Exception as e:
        logger.warning("full: dasha section failed: %s", e, exc_info=True)
        result["_errors"]["dasha"] = str(e)

    # ── Technical (chalti gaadi, dhur-dhur-aage, soya ghar, etc.) ──
    try:
        from app.lalkitab_technical import (
            calculate_chalti_gaadi,
            calculate_dhur_dhur_aage,
            calculate_soya_ghar,
            classify_all_planet_statuses,
            calculate_muththi,
        )
        lk_aspects_tech = calculate_lk_aspects(positions)
        result["technical"] = {
            "chalti_gaadi": calculate_chalti_gaadi(positions),
            "dhur_dhur_aage": calculate_dhur_dhur_aage(positions),
            "soya_ghar": calculate_soya_ghar(positions),
            "planet_statuses": classify_all_planet_statuses(positions),
            "muththi": calculate_muththi(positions),
            "kayam": calculate_kayam_grah(positions, lk_aspects_tech),
        }
    except Exception as e:
        logger.warning("full: technical section failed: %s", e, exc_info=True)
        result["_errors"]["technical"] = str(e)

    # ── Sacrifice (Bali Ka Bakra) ──
    try:
        from app.lalkitab_sacrifice import analyze_sacrifice
        sacrifice_results = analyze_sacrifice(positions)
        result["sacrifice"] = {
            "sacrifice_count": len(sacrifice_results),
            "has_sacrifices": len(sacrifice_results) > 0,
            "results": sacrifice_results,
        }
    except Exception as e:
        logger.warning("full: sacrifice section failed: %s", e, exc_info=True)
        result["_errors"]["sacrifice"] = str(e)

    # ── Forbidden ──
    try:
        from app.lalkitab_forbidden import get_forbidden_remedies
        forbidden_results = get_forbidden_remedies(positions)
        result["forbidden"] = {
            "forbidden_count": len(forbidden_results),
            "rules": forbidden_results,
        }
    except Exception as e:
        logger.warning("full: forbidden section failed: %s", e, exc_info=True)
        result["_errors"]["forbidden"] = str(e)

    # ── Milestones (Safar-e-Zindagi) ──
    try:
        from app.lalkitab_milestones import calculate_age_milestones
        if birth_date:
            result["milestones"] = calculate_age_milestones(birth_date, positions)
        else:
            result["_errors"]["milestones"] = "birth_date not available"
    except Exception as e:
        logger.warning("full: milestones section failed: %s", e, exc_info=True)
        result["_errors"]["milestones"] = str(e)

    # ── Doshas (Lal Kitab dosha detection) ──
    try:
        from app.lalkitab_dosha import detect_lalkitab_doshas
        result["doshas"] = detect_lalkitab_doshas(positions)
    except Exception as e:
        logger.warning("full: doshas section failed: %s", e, exc_info=True)
        result["_errors"]["doshas"] = str(e)

    # Always expose diagnostics so callers can distinguish success from silent failure
    errors = result["_errors"]
    result["_diagnostics"] = {
        "sections_ok": sum(1 for k in ("advanced","remedies","dasha","technical","sacrifice","forbidden","milestones","doshas") if k not in errors),
        "sections_failed": len(errors),
        "errors": errors,
    }
    del result["_errors"]

    return result


# ═══════════════════════════════════════════════════════════════════
# P2.6 — COMPREHENSIVE LK PDF REPORT (MVP)
# Aggregates existing endpoints into a single, printable JSON payload.
# Frontend renders to HTML and uses window.print() → browser PDF.
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/pdf-report/{kundli_id}", status_code=status.HTTP_200_OK)
def get_lalkitab_pdf_report(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    P2.6 — Aggregated Lal Kitab report payload (MVP, ~10-15 printable pages).

    Pulls together: Tewa chart, per-planet analysis, detected doshas,
    karmic debts (Rin), Prediction Studio scores, remedies, Varshphal
    (current year), and source-tag references — so the frontend can
    render one long, structured document and offer a print-to-PDF action.

    Design notes:
      - Each section is independently try/except-wrapped; one section's
        failure does NOT kill the whole report. Failures surface in
        `_errors.<section>` so the UI can gracefully hide them.
      - No new PDF engine dependency — the MVP relies on the browser's
        `window.print()` to produce a real PDF.
      - Caches nothing — recomputes on every call. The kundli itself is
        the cache.
    """
    report: dict[str, Any] = {
        "kundli_id": kundli_id,
        "generated_at": _date.today().isoformat(),
        "person": {},
        "tewa": None,
        "planets": [],
        "doshas": None,
        "karmic_debts": None,
        "prediction_studio": None,
        "remedies": None,
        "varshphal": None,
        "sources": [],
        "_errors": {},
    }

    # ── Fetch raw kundli + positions (mandatory — bail out on failure) ──
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    raw = row["chart_data"]
    chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})

    # ── Person / cover page ──
    report["person"] = {
        "person_name": row.get("person_name") or "",
        "birth_date": row.get("birth_date") or "",
        "birth_time": row.get("birth_time") or "",
        "birth_place": row.get("birth_place") or "",
        "latitude": row.get("latitude"),
        "longitude": row.get("longitude"),
        "timezone_offset": row.get("timezone_offset"),
        "gender": row.get("gender") or "",
    }

    # Pre-compute formatted_positions used by multiple sections
    formatted_positions = [
        {"planet": p["planet"].capitalize(), "house": p["house"]}
        for p in positions
    ]

    # ── Tewa (identification + classification) ──
    try:
        lk_aspects = calculate_lk_aspects(formatted_positions)
        sleeping_info = calculate_sleeping_status(formatted_positions)
        kayam_planets = calculate_kayam_grah(formatted_positions, lk_aspects)
        from app.lalkitab_andhe_grah import detect_andhe_grah
        andhe_info = detect_andhe_grah(formatted_positions, chart_data=chart_data)
        report["tewa"] = {
            "chart_data": chart_data,
            "positions": positions,
            "teva_type": identify_teva_type(formatted_positions),
            "masnui_planets": calculate_masnui_planets(formatted_positions),
            "sleeping": sleeping_info,
            "kayam": kayam_planets,
            "andhe": andhe_info,
            "aspects": lk_aspects,
        }
    except Exception as e:
        logger.warning("pdf-report: tewa section failed: %s", e, exc_info=True)
        report["_errors"]["tewa"] = str(e)

    # ── Per-planet analysis (9 planets × key fields) ──
    try:
        planets_dict = chart_data.get("planets", {}) if isinstance(chart_data, dict) else {}
        planets_out = []
        for pname in [
            "Sun", "Moon", "Mars", "Mercury", "Jupiter",
            "Venus", "Saturn", "Rahu", "Ketu",
        ]:
            info = planets_dict.get(pname) or {}
            lk_house = _derive_lk_house(info) if isinstance(info, dict) else 0
            planets_out.append({
                "planet": pname,
                "planet_hi": PLANET_NAMES_HI.get(pname, pname),
                "sign": info.get("sign") if isinstance(info, dict) else None,
                "lk_house": lk_house,
                "nakshatra": info.get("nakshatra") if isinstance(info, dict) else None,
                "sign_degree": info.get("sign_degree") if isinstance(info, dict) else None,
                "longitude": info.get("longitude") if isinstance(info, dict) else None,
                "is_retrograde": bool(info.get("retrograde") or info.get("is_retrograde")) if isinstance(info, dict) else False,
                "status": _lk_status_string(info) if isinstance(info, dict) else "",
            })
        report["planets"] = planets_out
    except Exception as e:
        logger.warning("pdf-report: planets section failed: %s", e, exc_info=True)
        report["_errors"]["planets"] = str(e)

    # ── Doshas ──
    try:
        from app.lalkitab_dosha import detect_lalkitab_doshas
        report["doshas"] = detect_lalkitab_doshas(positions)
    except Exception as e:
        logger.warning("pdf-report: doshas section failed: %s", e, exc_info=True)
        report["_errors"]["doshas"] = str(e)

    # ── Karmic Debts (Rin) — use enriched list with active/passive flag ──
    try:
        base_debts = calculate_karmic_debts(formatted_positions)
        try:
            active_enriched = enrich_debts_active_passive(base_debts, formatted_positions)
        except Exception:
            active_enriched = base_debts
        report["karmic_debts"] = {
            "debts": active_enriched,
            "count": len(active_enriched or []),
        }
    except Exception as e:
        logger.warning("pdf-report: karmic_debts section failed: %s", e, exc_info=True)
        report["_errors"]["karmic_debts"] = str(e)

    # ── Prediction Studio ──
    try:
        planet_positions = {p["planet"].capitalize(): int(p["house"]) for p in positions if p.get("house")}
        planets_dict_ps = chart_data.get("planets", {}) if isinstance(chart_data, dict) else {}
        planet_lons: dict[str, float] = {}
        for pname, info in planets_dict_ps.items():
            if pname in _KNOWN_PLANETS and isinstance(info, dict):
                lon = info.get("longitude")
                if lon is not None:
                    try:
                        planet_lons[pname] = float(lon)
                    except Exception:
                        pass
        from app.lalkitab_prediction_studio import build_prediction_studio
        report["prediction_studio"] = build_prediction_studio(planet_positions, planet_lons)
    except Exception as e:
        logger.warning("pdf-report: prediction_studio section failed: %s", e, exc_info=True)
        report["_errors"]["prediction_studio"] = str(e)

    # ── Remedies (enriched, with savdhaniyan + classification) ──
    try:
        planet_positions_r = {
            p: info.get("sign")
            for p, info in chart_data.get("planets", {}).items()
            if isinstance(info, dict) and isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
        }
        if planet_positions_r:
            res = get_remedies(planet_positions_r, chart_data=chart_data)
            enriched = []
            for planet, info in res.items():
                r = info["remedy"]
                enriched.append({
                    "planet": planet,
                    "planet_hi": PLANET_NAMES_HI.get(planet, planet),
                    "sign": info["sign"],
                    "lk_house": info["lk_house"],
                    "dignity": info["dignity"],
                    "strength": info["strength"],
                    "has_remedy": info["has_remedy"],
                    "urgency": r.get("urgency", "low"),
                    "remedy_en": r.get("en", ""),
                    "remedy_hi": r.get("hi", ""),
                    "problem_en": r.get("problem_en", ""),
                    "problem_hi": r.get("problem_hi", ""),
                    "reason_en": r.get("reason_en", ""),
                    "reason_hi": r.get("reason_hi", ""),
                    "how_en": r.get("how_en", ""),
                    "how_hi": r.get("how_hi", ""),
                    "savdhaniyan": info.get("savdhaniyan"),
                    "andhe_grah_warning": info.get("andhe_grah_warning"),
                    "remedy_matrix": info.get("remedy_matrix"),
                    "classification": r.get("classification") or r.get("category") or "",
                })
            urgency_order = {"high": 0, "medium": 1, "low": 2}
            enriched.sort(key=lambda x: (0 if x["has_remedy"] else 1, urgency_order.get(x["urgency"], 2), x["lk_house"]))
            report["remedies"] = {"remedies": enriched, "count": len(enriched)}
        else:
            report["_errors"]["remedies"] = "no planet positions with valid signs"
    except Exception as e:
        logger.warning("pdf-report: remedies section failed: %s", e, exc_info=True)
        report["_errors"]["remedies"] = str(e)

    # ── Varshphal (current year) ──
    try:
        from datetime import datetime as _dt
        from app.varshphal_engine import calculate_varshphal
        cur_year = _dt.now().year
        vp = calculate_varshphal(
            natal_chart_data=chart_data,
            target_year=cur_year,
            birth_date=row["birth_date"],
            latitude=row.get("latitude") or 0.0,
            longitude=row.get("longitude") or 0.0,
            tz_offset=row.get("timezone_offset") or 5.5,
        )
        report["varshphal"] = {"year": cur_year, **(vp or {})}
    except Exception as e:
        logger.warning("pdf-report: varshphal section failed: %s", e, exc_info=True)
        report["_errors"]["varshphal"] = str(e)

    # ── Sources (every LK reference surfaced in the report) ──
    # Static catalog — MVP version. A future phase can pull real citations
    # from the in-repo LK 1952 engine tags.
    try:
        sources = [
            {"tag": "LK-1952", "title_en": "Lal Kitab 1952 (Arun Sanhita)",
             "title_hi": "लाल किताब १९५२ (अरुण संहिता)",
             "summary_en": "Canonical primary source for all LK rules — Teva, Rin, doshas, remedies.",
             "summary_hi": "समस्त तेवा, ऋण, दोष एवं उपाय-नियमों का मूल प्रमाण।"},
            {"tag": "LK-1941", "title_en": "Lal Kitab 1941",
             "title_hi": "लाल किताब १९४१",
             "summary_en": "Second edition — alternative remedy readings for edge cases.",
             "summary_hi": "द्वितीय संस्करण — विशेष परिस्थितियों में वैकल्पिक उपाय।"},
            {"tag": "LK-1939", "title_en": "Lal Kitab 1939",
             "title_hi": "लाल किताब १९३९",
             "summary_en": "First edition — foundational house-planet delineations.",
             "summary_hi": "प्रथम संस्करण — मूल भाव-ग्रह विवेचना।"},
            {"tag": "LK-Teva", "title_en": "LK Teva (Chart Classification)",
             "title_hi": "तेवा — कुंडली वर्गीकरण",
             "summary_en": "Andha / Ratondha / Dharmi / Nabalig / Khali — overall chart type.",
             "summary_hi": "अंधा / रतौंधा / धर्मी / नाबालिग / खाली — सम्पूर्ण कुंडली प्रकार।"},
            {"tag": "LK-Rin", "title_en": "LK Rin (Karmic Debts)",
             "title_hi": "ऋण — कर्म-ऋण",
             "summary_en": "Pitra, Matra, Stri, Bhratra, Swarna, etc. — nine classical debts.",
             "summary_hi": "पित्र, मातृ, स्त्री, भ्रातृ, स्वर्ण आदि — नौ शास्त्रीय ऋण।"},
            {"tag": "LK-Doshas", "title_en": "LK Doshas",
             "title_hi": "दोष",
             "summary_en": "Afflictions detected by house/sign/planet combinations.",
             "summary_hi": "भाव-राशि-ग्रह संयोजन से पहचाने गये दोष।"},
            {"tag": "LK-Varshphal", "title_en": "LK Varshphal (Solar Return)",
             "title_hi": "वर्षफल",
             "summary_en": "Annual chart — Muntha, Varshesh, Mudda Dasha.",
             "summary_hi": "वार्षिक कुंडली — मुंथा, वर्षेश, मुद्दा दशा।"},
            {"tag": "LK-Remedies", "title_en": "LK Remedies (Upay)",
             "title_hi": "उपाय",
             "summary_en": "Concrete LK remedies with savdhaniyan (cautions) and classification.",
             "summary_hi": "ठोस उपाय — सावधानियाँ एवं वर्गीकरण सहित।"},
        ]
        report["sources"] = sources
    except Exception as e:
        logger.warning("pdf-report: sources section failed: %s", e, exc_info=True)
        report["_errors"]["sources"] = str(e)

    if not report["_errors"]:
        del report["_errors"]
    return report
# P2.4 — REMEDY WIZARD (intent → conditions → ranked remedies)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/remedy-wizard/intents")
def get_remedy_wizard_intents():
    """Return the list of supported intents for the wizard Step 1 card grid.

    Public (no auth) — this is static catalog data driving the UI, not any
    per-user chart information. Keeps the frontend snappy.
    """
    from app.lalkitab_remedy_wizard import list_intents, LK_DERIVED
    return {"intents": list_intents(), "source": LK_DERIVED}


@router.post("/api/lalkitab/remedy-wizard")
def lalkitab_remedy_wizard(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Intent → ranked remedies.

    Input:  {kundli_id: str, intent: str}
    Output: {intent, intent_label_en/hi, focus_planets, focus_houses,
             avoid, ranked_remedies, top_picks, source}

    Re-uses the same enriched remedies the /remedies/enriched endpoint
    already produces — the wizard layer only RE-RANKS by intent affinity,
    so every remedy returned retains its LK_CANONICAL provenance.
    """
    from app.lalkitab_remedy_wizard import recommend_remedies

    kundli_id = payload.get("kundli_id")
    intent = payload.get("intent")
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id is required")
    if not intent:
        raise HTTPException(status_code=400, detail="intent is required")

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    try:
        raw = row["chart_data"]
        chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=500, detail="Corrupt chart data")

    # Build enriched remedy list using the SAME path as /remedies/enriched.
    planet_positions = {
        p: info.get("sign")
        for p, info in chart_data.get("planets", {}).items()
        if isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
    }
    if not planet_positions:
        raise HTTPException(
            status_code=400,
            detail="No planet positions with valid signs in chart",
        )

    res = get_remedies(planet_positions, chart_data=chart_data)
    enriched: list[dict] = []
    afflictions_map: dict[str, list[str]] = {}
    for planet, info in res.items():
        r = info.get("remedy") or {}
        afflictions_map[planet] = list(info.get("afflictions", []) or [])
        enriched.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "sign": info.get("sign"),
            "lk_house": info.get("lk_house", 0),
            "dignity": info.get("dignity", ""),
            "strength": info.get("strength", 0.0),
            "has_remedy": info.get("has_remedy", False),
            "urgency": r.get("urgency", "low"),
            "material": r.get("material", ""),
            "day": r.get("day", ""),
            "remedy_en": r.get("en", ""),
            "remedy_hi": r.get("hi", ""),
            "problem_en": r.get("problem_en", ""),
            "problem_hi": r.get("problem_hi", ""),
            "reason_en": r.get("reason_en", ""),
            "reason_hi": r.get("reason_hi", ""),
            "how_en": r.get("how_en", ""),
            "how_hi": r.get("how_hi", ""),
            "afflictions": afflictions_map[planet],
        })

    return recommend_remedies(
        intent=intent,
        planet_positions=enriched,
        afflictions=afflictions_map,
    )


# ═══════════════════════════════════════════════════════════════════
# P2.12 — CALCULATION DETAILS (professional verification)
# ═══════════════════════════════════════════════════════════════════

def _degrees_to_dms(longitude: float) -> dict:
    """Split a decimal longitude into degree / minute / second pieces.

    Returns the sign-relative degree (0..30), the sign name, and a DMS
    string. Used in the calculation-detail payload so pandits can verify
    against manual ephemeris lookups.
    """
    try:
        lon = float(longitude) % 360.0
    except (TypeError, ValueError):
        return {"deg": 0, "min": 0, "sec": 0.0, "dms": "", "sign_deg": 0.0}
    sign_deg = lon % 30.0
    deg = int(sign_deg)
    rem_min = (sign_deg - deg) * 60.0
    minute = int(rem_min)
    second = round((rem_min - minute) * 60.0, 2)
    return {
        "deg": deg,
        "min": minute,
        "sec": second,
        "dms": f"{deg}\u00b0{minute:02d}'{second:05.2f}\"",
        "sign_deg": round(sign_deg, 6),
    }


@router.get("/api/lalkitab/calculation-details/{kundli_id}")
def get_calculation_details(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return raw calculation steps so an astrologer can audit the software.

    Payload sections:
      ayanamsa:         system + numeric value + sidereal offset
      planets:          per-planet longitude with DMS precision, sign,
                        nakshatra, nakshatra_pada, retrograde, combust,
                        derived Lal Kitab house (Aries=H1 scheme)
      ascendant:        longitude + DMS
      houses:           LK fixed house map
      bunyaad:          foundation check with friend/enemy resolution
      takkar:           confrontation pairs
      masnui:           masnui detections
      aspects:          Lal Kitab aspect calculations
      source_references: every value's provenance tag
    """
    from app.lalkitab_advanced import (
        calculate_bunyaad,
        calculate_takkar,
        calculate_masnui_planets,
        calculate_lk_aspects,
        LK_FRIENDS,
        LK_ENEMIES,
        PAKKA_GHAR,
        BUNYAAD_HOUSE,
    )
    from app.lalkitab_source_tags import source_of, LK_CANONICAL, LK_DERIVED

    row = db.execute(
        "SELECT chart_data, birth_date, birth_time, latitude, longitude, timezone_offset "
        "FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    try:
        raw = row["chart_data"]
        chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=500, detail="Corrupt chart data")

    # ── Ayanamsa ──
    ayanamsa_value = chart_data.get("ayanamsa_value")
    ayanamsa_system = chart_data.get("ayanamsa_system", "lahiri")
    ayanamsa_section = {
        "system": ayanamsa_system,
        "value_degrees": ayanamsa_value,
        "sidereal_offset_dms": _degrees_to_dms(ayanamsa_value)["dms"] if ayanamsa_value is not None else None,
        "note_en": (
            "Sidereal longitudes = tropical_longitude - ayanamsa. "
            "Lahiri is the default for Vedic; KP uses Krishnamurti."
        ),
        "note_hi": (
            "\u0938\u093e\u092f\u0928 \u0930\u093e\u0936\u093f = \u0909\u0937\u094d\u0923 - \u0905\u092f\u0928\u093e\u0902\u0936\u0964 "
            "\u0935\u0948\u0926\u093f\u0915 \u092e\u0947\u0902 \u0932\u093e\u0939\u093f\u0930\u0940 \u0921\u093f\u092b\u093c\u0949\u0932\u094d\u091f, KP \u092e\u0947\u0902 \u0915\u0943\u0937\u094d\u0923\u092e\u0942\u0930\u094d\u0924\u093f\u0964"
        ),
        "source": LK_CANONICAL,
    }

    # ── Planet longitudes ──
    planet_rows: list[dict] = []
    formatted_positions: list[dict] = []  # for downstream calculators
    for planet_name, info in (chart_data.get("planets") or {}).items():
        if not isinstance(info, dict):
            continue
        longitude = info.get("longitude")
        dms = _degrees_to_dms(longitude) if longitude is not None else {
            "deg": None, "min": None, "sec": None, "dms": None, "sign_deg": info.get("sign_degree"),
        }
        sign = info.get("sign", "")
        lk_house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if lk_house > 0:
            formatted_positions.append({"planet": planet_name.capitalize(), "house": lk_house})
        planet_rows.append({
            "planet": planet_name,
            "longitude": longitude,
            "sign": sign,
            "sign_degree": info.get("sign_degree"),
            "dms": dms.get("dms"),
            "deg": dms.get("deg"),
            "min": dms.get("min"),
            "sec": dms.get("sec"),
            "nakshatra": info.get("nakshatra"),
            "nakshatra_pada": info.get("nakshatra_pada"),
            "vedic_house": info.get("house"),       # whole-sign from ascendant
            "lk_house": lk_house,                    # LK fixed-house (Aries=H1)
            "retrograde": info.get("retrograde", False),
            "is_combust": info.get("is_combust", False),
            "is_vargottama": info.get("is_vargottama", False),
            "is_sandhi": info.get("is_sandhi", False),
            "status": info.get("status", ""),
        })

    asc = chart_data.get("ascendant") or {}
    asc_dms = _degrees_to_dms(asc.get("longitude")) if asc.get("longitude") is not None else {}
    ascendant_section = {
        "longitude": asc.get("longitude"),
        "sign": asc.get("sign"),
        "sign_degree": asc.get("sign_degree"),
        "dms": asc_dms.get("dms"),
        "note_en": (
            "Lal Kitab uses FIXED houses (Aries=H1 ... Pisces=H12) regardless of "
            "ascendant. The Vedic ascendant is shown here only for reference."
        ),
        "note_hi": (
            "\u0932\u093e\u0932 \u0915\u093f\u0924\u093e\u092c \u092e\u0947\u0902 \u0918\u0930 \u0938\u0926\u093e \u0938\u094d\u0925\u093f\u0930 \u0939\u094b\u0924\u0947 \u0939\u0948\u0902 "
            "(\u092e\u0947\u0937=H1 ... \u092e\u0940\u0928=H12), \u0932\u0917\u094d\u0928 \u0915\u0941\u091b \u092d\u0940 \u0939\u094b\u0964"
        ),
        "source": LK_CANONICAL,
    }

    # ── LK Houses map ──
    houses_map = {
        h: {"sign": s, "planets": [r["planet"] for r in planet_rows if r["lk_house"] == h]}
        for s, h in _SIGN_TO_LK_HOUSE.items()
    }

    # ── Bunyaad (friend/enemy resolution) ──
    try:
        bunyaad = calculate_bunyaad(formatted_positions)
    except Exception as e:
        logger.warning("calculation-details: bunyaad failed: %s", e)
        bunyaad = {"_error": str(e)}
    friend_tables = {
        p: {
            "pakka_ghar": PAKKA_GHAR.get(p),
            "bunyaad_house": BUNYAAD_HOUSE.get(p),
            "friends": sorted(list(LK_FRIENDS.get(p, set()))),
            "enemies": sorted(list(LK_ENEMIES.get(p, set()))),
        }
        for p in PAKKA_GHAR.keys()
    }

    # ── Takkar pairs ──
    try:
        takkar = calculate_takkar(formatted_positions)
    except Exception as e:
        logger.warning("calculation-details: takkar failed: %s", e)
        takkar = {"_error": str(e)}

    # ── Masnui detections ──
    try:
        masnui = calculate_masnui_planets(formatted_positions)
    except Exception as e:
        logger.warning("calculation-details: masnui failed: %s", e)
        masnui = {"_error": str(e)}

    # ── Aspects ──
    try:
        aspects = calculate_lk_aspects(formatted_positions)
    except Exception as e:
        logger.warning("calculation-details: aspects failed: %s", e)
        aspects = {"_error": str(e)}

    # ── Source references block ──
    source_references = {
        "ayanamsa":          {"source": LK_CANONICAL,
                              "note_en": "Swiss Ephemeris (Lahiri/KP)",
                              "note_hi": "\u0938\u094d\u0935\u093f\u0938 \u090f\u092b\u0947\u092e\u0947\u0930\u093f\u0938"},
        "planet_longitudes": {"source": LK_CANONICAL,
                              "note_en": "Sidereal = tropical - ayanamsa",
                              "note_hi": "\u0938\u093e\u092f\u0928 = \u0909\u0937\u094d\u0923 - \u0905\u092f\u0928\u093e\u0902\u0936"},
        "lk_houses":         {"source": LK_CANONICAL,
                              "note_en": "Fixed house map: Aries=H1 ... Pisces=H12",
                              "note_hi": "\u0938\u094d\u0925\u093f\u0930 \u092d\u093e\u0935: \u092e\u0947\u0937=H1 ... \u092e\u0940\u0928=H12"},
        "bunyaad":           {"source": source_of("calculate_bunyaad"),
                              "note_en": "Foundation = 9th from pakka ghar",
                              "note_hi": "\u092c\u0941\u0928\u093f\u092f\u093e\u0926 = \u092a\u0915\u094d\u0915\u093e \u0918\u0930 \u0938\u0947 \u0928\u094c\u0935\u093e\u0902"},
        "takkar":            {"source": source_of("calculate_takkar"),
                              "note_en": "Axis confrontations 1-7, 2-8, etc.",
                              "note_hi": "\u0905\u0915\u094d\u0937 \u091f\u0915\u0930\u093e\u0935 1-7, 2-8"},
        "masnui":            {"source": source_of("calculate_masnui_planets"),
                              "note_en": "Masnui (artificial) planets formed by combinations",
                              "note_hi": "\u0938\u0902\u092f\u094b\u091c\u0928\u094b\u0902 \u0938\u0947 \u092c\u0928\u0947 \u092e\u0938\u0928\u0942\u0908 \u0917\u094d\u0930\u0939"},
        "aspects":           {"source": source_of("calculate_lk_aspects"),
                              "note_en": "Lal Kitab aspects (not Parashari 3/7/10)",
                              "note_hi": "\u0932\u093e\u0932 \u0915\u093f\u0924\u093e\u092c \u0915\u0940 \u0926\u0943\u0937\u094d\u091f\u093f"},
    }

    return {
        "kundli_id": kundli_id,
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "ayanamsa": ayanamsa_section,
        "ascendant": ascendant_section,
        "planets": planet_rows,
        "houses": houses_map,
        "bunyaad": bunyaad,
        "takkar": takkar,
        "masnui": masnui,
        "aspects": aspects,
        "friend_tables": friend_tables,
        "source_references": source_references,
        "source": LK_DERIVED,
    }


@router.get("/api/lalkitab/remedies/abhimantrit")
def get_abhimantrit_items(
    kundli_id: str,
    user: dict = Depends(get_current_user),
):
    """Return the static Abhimantrit specialty items catalogue (LK 4.20)."""
    return {"kundli_id": kundli_id, "items": ABHIMANTRIT_ITEMS, "source": "LK_ABHIMANTRIT"}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Sapt Var (7-Day Weekly Forecast)
# ─────────────────────────────────────────────────────────────

_DAY_LORDS = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter", 4: "Venus", 5: "Saturn", 6: "Sun"}
_DAY_NAMES_EN = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
_DAY_NAMES_HI = {0: "सोमवार", 1: "मंगलवार", 2: "बुधवार", 3: "गुरुवार", 4: "शुक्रवार", 5: "शनिवार", 6: "रविवार"}

_SAPT_VAR_HOUSE_THEMES = {
    1:  {"en": "self, health, personality, and fresh starts", "hi": "स्वयं, स्वास्थ्य, व्यक्तित्व और नई शुरुआत"},
    2:  {"en": "family, wealth, speech, and food", "hi": "परिवार, धन, वाणी और भोजन"},
    3:  {"en": "courage, siblings, communication, and short journeys", "hi": "साहस, भाई-बहन, संवाद और छोटी यात्राएँ"},
    4:  {"en": "home, mother, real estate, and emotional peace", "hi": "घर, माता, संपत्ति और भावनात्मक शांति"},
    5:  {"en": "intelligence, children, creativity, and speculation", "hi": "बुद्धि, संतान, रचनात्मकता और सट्टा"},
    6:  {"en": "enemies, debts, health challenges, and service", "hi": "शत्रु, ऋण, स्वास्थ्य चुनौतियाँ और सेवा"},
    7:  {"en": "partnerships, marriage, contracts, and open dealings", "hi": "साझेदारी, विवाह, अनुबंध और खुले व्यवहार"},
    8:  {"en": "transformation, in-laws, occult, and hidden matters", "hi": "परिवर्तन, ससुराल, गुप्त विद्या और छुपे मामले"},
    9:  {"en": "luck, dharma, father, religion, and long journeys", "hi": "भाग्य, धर्म, पिता, धर्म और लंबी यात्राएँ"},
    10: {"en": "career, reputation, authority, and public life", "hi": "करियर, प्रतिष्ठा, अधिकार और सार्वजनिक जीवन"},
    11: {"en": "gains, desires, elder siblings, and social networks", "hi": "लाभ, इच्छाएँ, बड़े भाई-बहन और सामाजिक संपर्क"},
    12: {"en": "expenditure, isolation, foreign matters, and spirituality", "hi": "खर्च, एकांत, विदेशी मामले और आध्यात्मिकता"},
}

_DUSTHANA_SV = {6, 8, 12}
_KENDRA_SV = {1, 4, 7, 10}
_TRIKONA_SV = {1, 5, 9}

_LK_PAKKA_SV: dict[str, set] = {
    "Sun": {1}, "Moon": {4}, "Mars": {3, 8}, "Mercury": {3, 6},
    "Jupiter": {2, 9, 12}, "Venus": {7}, "Saturn": {7, 10},
    "Rahu": {6, 11, 12}, "Ketu": {3, 6, 12},
}
_LK_FRIENDLY_SV: dict[str, set] = {
    "Sun": {9, 10, 11}, "Moon": {1, 2, 7, 11}, "Mars": {1, 4, 9},
    "Mercury": {1, 2, 10, 11}, "Jupiter": {5, 7, 11}, "Venus": {1, 4, 5, 11},
    "Saturn": {2, 3, 11}, "Rahu": {3, 9}, "Ketu": {9},
}
_LK_ENEMY_SV: dict[str, set] = {
    "Sun": {7, 12}, "Moon": {8, 12}, "Mars": {2, 6, 12},
    "Mercury": {7, 12}, "Jupiter": {3, 6, 8}, "Venus": {8, 12},
    "Saturn": {1, 4, 8}, "Rahu": {2, 4, 7, 8}, "Ketu": {1, 2, 5, 7, 10},
}


def _lk_natal_strength_sv(planet: str, natal_house: int) -> tuple[int, str]:
    if natal_house in _LK_PAKKA_SV.get(planet, set()):
        score, label = 92, "pakka_ghar"
    elif natal_house in _LK_FRIENDLY_SV.get(planet, set()):
        score, label = 70, "friendly"
    elif natal_house in _LK_ENEMY_SV.get(planet, set()):
        score, label = 28, "enemy"
    else:
        score, label = 50, "neutral"
    if natal_house in _DUSTHANA_SV and label != "pakka_ghar":
        score = max(10, score - 15)
        label = f"{label}_dusthana"
    if label == "neutral" and natal_house in (_KENDRA_SV | _TRIKONA_SV):
        score = min(65, score + 10)
        label = "neutral_angular"
    return score, label


def _build_sapt_var_entry(date_obj, weekday_num: int, day_lord: str,
                          natal_house: int, lk_score: int, lk_label: str) -> dict:
    theme = _SAPT_VAR_HOUSE_THEMES.get(natal_house, {"en": "", "hi": ""})
    day_en = _DAY_NAMES_EN[weekday_num]
    day_hi = _DAY_NAMES_HI[weekday_num]
    is_pakka = lk_label == "pakka_ghar"

    if is_pakka:
        strength_label = "strong"
        pred_en = (
            f"{day_en} is ruled by {day_lord}, which sits in its Pakka Ghar (H{natal_house}) "
            f"in your chart. This is an exceptionally powerful day for: {theme['en']}. "
            f"Initiate important activities, sign contracts, or make key decisions today."
        )
        pred_hi = (
            f"{day_hi} का स्वामी {day_lord} आपकी जन्म कुंडली में अपने पक्के घर (भाव {natal_house}) में है। "
            f"यह दिन अत्यंत शक्तिशाली है: {theme['hi']}। "
            f"महत्वपूर्ण कार्य, अनुबंध या मुख्य निर्णय आज ही करें।"
        )
    elif lk_score >= 65:
        strength_label = "strong"
        pred_en = (
            f"{day_en} ({day_lord}'s day) is favorable for you. "
            f"{day_lord} in H{natal_house} activates {theme['en']}. "
            f"Use this day's energy for forward momentum in these areas."
        )
        pred_hi = (
            f"{day_hi} ({day_lord} का दिन) आपके लिए अनुकूल है। "
            f"भाव {natal_house} में {day_lord} सक्रिय करता है: {theme['hi']}। "
            f"इन क्षेत्रों में आगे बढ़ने के लिए इस दिन की ऊर्जा का उपयोग करें।"
        )
    elif lk_score >= 40:
        strength_label = "moderate"
        pred_en = (
            f"{day_en} ({day_lord}'s day) brings mixed results. "
            f"{day_lord} in H{natal_house} touches {theme['en']}, "
            f"but with some friction. Plan carefully and avoid major commitments."
        )
        pred_hi = (
            f"{day_hi} ({day_lord} का दिन) मिश्रित परिणाम देता है। "
            f"भाव {natal_house} में {day_lord} — {theme['hi']} — पर कुछ घर्षण है। "
            f"सावधानी से योजना बनाएँ और बड़ी प्रतिबद्धताओं से बचें।"
        )
    else:
        strength_label = "weak"
        pred_en = (
            f"{day_en} ({day_lord}'s day) requires extra care. "
            f"{day_lord} in H{natal_house} creates challenges in {theme['en']}. "
            f"Apply patience, perform the planet's LK remedy, and avoid impulsive actions."
        )
        pred_hi = (
            f"{day_hi} ({day_lord} का दिन) अतिरिक्त सावधानी चाहता है। "
            f"भाव {natal_house} में {day_lord} — {theme['hi']} — में चुनौतियाँ। "
            f"धैर्य रखें, ग्रह का लाल किताब उपाय करें और आवेगी कार्यों से बचें।"
        )

    return {
        "date": date_obj.isoformat(),
        "weekday_en": day_en,
        "weekday_hi": day_hi,
        "day_lord": day_lord,
        "natal_house": natal_house,
        "is_pakka_ghar": is_pakka,
        "lk_strength_score": lk_score,
        "strength_label": strength_label,
        "house_theme_en": theme["en"],
        "house_theme_hi": theme["hi"],
        "prediction_en": pred_en,
        "prediction_hi": pred_hi,
    }


@router.get("/api/lalkitab/sapt_var/{kundli_id}")
def get_sapt_var(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    LK Sapt Var (7-day weekly forecast).
    Each weekday is ruled by a planet; that planet's natal LK house determines
    which life area activates that day and how powerfully (LK Pakka Ghar system).
    """
    from datetime import timedelta

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    natal_lk_houses: dict[str, int] = {}
    for pname, info in chart_data.get("planets", {}).items():
        if pname in _KNOWN_PLANETS:
            natal_lk_houses[pname] = _derive_lk_house(info)

    today = _date.today()
    week: list[dict] = []
    for offset in range(7):
        day = today + timedelta(days=offset)
        wd = day.weekday()
        day_lord = _DAY_LORDS[wd]
        natal_house = natal_lk_houses.get(day_lord, 0)
        if natal_house == 0:
            week.append({
                "date": day.isoformat(),
                "weekday_en": _DAY_NAMES_EN[wd],
                "weekday_hi": _DAY_NAMES_HI[wd],
                "day_lord": day_lord,
                "natal_house": None,
                "strength_label": "unknown",
                "prediction_en": f"{day_lord} position not found in natal chart.",
                "prediction_hi": f"जन्म कुंडली में {day_lord} की स्थिति नहीं मिली।",
            })
            continue
        lk_score, lk_label = _lk_natal_strength_sv(day_lord, natal_house)
        week.append(_build_sapt_var_entry(day, wd, day_lord, natal_house, lk_score, lk_label))

    return {
        "kundli_id": kundli_id,
        "today": week[0] if week else {},
        "week": week,
        "note_en": "Each day's energy is determined by its ruling planet's strength in your natal Lal Kitab chart (Pakka Ghar system).",
        "note_hi": "प्रत्येक दिन की ऊर्जा उसके शासक ग्रह की आपकी जन्म लाल किताब कुंडली में शक्ति (पक्का घर प्रणाली) से निर्धारित होती है।",
    }


# ═══════════════════════════════════════════════════════════════════
# MASTER SUMMARY
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/master-summary/{kundli_id}")
def get_master_summary(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Single-call master summary: core life pattern, main problem, top-3 remedy
    actions, and 2-year dasha outlook. All derived from actual chart data.
    """
    from app.lalkitab_master_summary import generate_master_summary
    from app.lalkitab_sacrifice import analyze_sacrifice
    from app.lalkitab_dasha import get_dasha_timeline

    row = db.execute(
        "SELECT chart_data, birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"]) if isinstance(row["chart_data"], str) else (row["chart_data"] or {})

    # Build position list: [{planet, house, sign, dignity, strength}]
    planet_positions_sign = {
        p: info.get("sign")
        for p, info in chart_data.get("planets", {}).items()
        if isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
    }
    remedies_raw = get_remedies(planet_positions_sign, chart_data=chart_data) if planet_positions_sign else {}
    enriched_remedies = []
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    for planet, info in remedies_raw.items():
        r = info["remedy"]
        enriched_remedies.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "sign": info["sign"],
            "lk_house": info["lk_house"],
            "dignity": info["dignity"],
            "strength": info["strength"],
            "has_remedy": info["has_remedy"],
            "urgency": r.get("urgency", "low"),
            "remedy_en": r.get("en", ""),
            "remedy_hi": r.get("hi", ""),
            "problem_en": r.get("problem_en", ""),
            "problem_hi": r.get("problem_hi", ""),
            "how_en": r.get("how_en", ""),
            "how_hi": r.get("how_hi", ""),
            "day": r.get("day", ""),
            "classification": r.get("classification", ""),
        })
    enriched_remedies.sort(key=lambda x: (0 if x["has_remedy"] else 1, urgency_order.get(x["urgency"], 2), x["lk_house"]))

    # Positions list for sacrifice engine
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    sacrifice_results = analyze_sacrifice(positions)

    # Karmic debts
    try:
        karmic_debts = calculate_karmic_debts(positions)
    except Exception:
        karmic_debts = []

    # Dasha timeline
    dasha_data = get_dasha_timeline(
        birth_date=str(row["birth_date"]),
        current_date=_date.today().isoformat(),
    )

    summary = generate_master_summary(
        positions=positions,
        remedies=enriched_remedies,
        karmic_debts=karmic_debts,
        sacrifice_results=sacrifice_results,
        dasha_data=dasha_data,
    )

    return {"kundli_id": kundli_id, **summary}


# ═══════════════════════════════════════════════════════════════════
# MARRIAGE / H7 ANALYSIS
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/marriage/{kundli_id}")
def get_marriage_analysis(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Lal Kitab marriage and relationship analysis.
    Derives all predictions from actual H7 planets, Venus house/dignity,
    Moon house/dignity, and Saturn placement — no hardcoded text.
    """
    from app.lalkitab_marriage import analyze_marriage

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"]) if isinstance(row["chart_data"], str) else (row["chart_data"] or {})

    # Build enriched positions with sign, dignity, strength from remedy engine
    planet_positions_sign = {
        p: info.get("sign")
        for p, info in chart_data.get("planets", {}).items()
        if isinstance(info.get("sign"), str) and info.get("sign") in _SIGN_TO_LK_HOUSE
    }
    remedies_raw = get_remedies(planet_positions_sign, chart_data=chart_data) if planet_positions_sign else {}

    enriched_positions = []
    for planet, info in remedies_raw.items():
        enriched_positions.append({
            "planet": planet,
            "house": info["lk_house"],
            "sign": info["sign"],
            "dignity": info["dignity"],
            "strength": info["strength"],
        })

    result = analyze_marriage(enriched_positions)
    return {"kundli_id": kundli_id, **result}
