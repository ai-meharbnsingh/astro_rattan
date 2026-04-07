"""
jaimini_engine.py — Jaimini Astrology Calculator
==================================================
Implements key Jaimini system components:
  1. Chara Karakas (7 variable significators by degree)
  2. Special Lagnas (Arudha, Upapada, Karakamsha)
  3. Jaimini Drishti (sign-based aspects)
  4. Chara Dasha (sign-based timing)
  5. Indu Lagna (wealth indicator)
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Sign modality
CARDINAL = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

# Kaksha values for Indu Lagna
KAKSHA_VALUES = {
    "Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8,
    "Jupiter": 10, "Venus": 12, "Saturn": 1,
}

KARAKA_NAMES = ["AK", "AmK", "BK", "MK", "PiK", "GnK", "DK"]
KARAKA_FULL = {
    "AK": ("Atmakaraka", "आत्मकारक", "Soul / Self"),
    "AmK": ("Amatyakaraka", "अमात्यकारक", "Career / Minister"),
    "BK": ("Bhratrikaraka", "भ्रातृकारक", "Siblings"),
    "MK": ("Matrikaraka", "मातृकारक", "Mother"),
    "PiK": ("Pitrikaraka", "पितृकारक", "Father"),
    "GnK": ("Gnatikaraka", "ज्ञातिकारक", "Relatives / Enemies"),
    "DK": ("Darakaraka", "दारकारक", "Spouse"),
}


def _sign_index(sign: str) -> int:
    try:
        return ZODIAC.index(sign)
    except ValueError:
        return 0


def _sign_distance(from_sign: str, to_sign: str) -> int:
    """Count houses from from_sign to to_sign (1-indexed)."""
    return ((_sign_index(to_sign) - _sign_index(from_sign)) % 12) + 1


def _sign_at_offset(sign: str, offset: int) -> str:
    """Get sign at N houses from given sign (1-indexed offset)."""
    return ZODIAC[(_sign_index(sign) + offset - 1) % 12]


def _get_planet_sign(planets: Dict, planet_name: str) -> str:
    return planets.get(planet_name, {}).get("sign", "Aries")


def _get_planet_degree(planets: Dict, planet_name: str) -> float:
    p = planets.get(planet_name, {})
    return float(p.get("sign_degree", p.get("longitude", 0.0) % 30.0))


# ============================================================
# 1. CHARA KARAKAS
# ============================================================

def calculate_chara_karakas(planets: Dict) -> List[Dict]:
    """
    Sort 7 planets (Sun through Saturn) by sign_degree descending.
    Highest degree = Atmakaraka, lowest = Darakaraka.
    """
    karaka_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    entries = []
    for name in karaka_planets:
        deg = _get_planet_degree(planets, name)
        entries.append({"planet": name, "degree": round(deg, 2)})

    entries.sort(key=lambda x: x["degree"], reverse=True)

    result = []
    for i, entry in enumerate(entries):
        karaka = KARAKA_NAMES[i] if i < len(KARAKA_NAMES) else f"K{i+1}"
        full = KARAKA_FULL.get(karaka, (karaka, karaka, ""))
        result.append({
            "planet": entry["planet"],
            "degree": entry["degree"],
            "karaka": karaka,
            "name_en": full[0],
            "name_hi": full[1],
            "significance": full[2],
        })

    return result


# ============================================================
# 2. SPECIAL LAGNAS
# ============================================================

def calculate_special_lagnas(planets: Dict, ascendant: Dict, d9_planets: Optional[Dict] = None) -> Dict:
    """
    Arudha Lagna (AL), Upapada Lagna (UL), Karakamsha.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"

    # --- Arudha Lagna ---
    asc_lord = SIGN_LORD[asc_sign]
    lord_sign = _get_planet_sign(planets, asc_lord)
    dist = _sign_distance(asc_sign, lord_sign)

    # Exception: if lord in 1st or 7th from ascendant, use 10th or 4th instead
    if dist == 1:
        al_sign = _sign_at_offset(asc_sign, 10)
    elif dist == 7:
        al_sign = _sign_at_offset(asc_sign, 4)
    else:
        al_sign = _sign_at_offset(lord_sign, dist)

    # --- Upapada Lagna (from 12th house) ---
    twelfth_sign = _sign_at_offset(asc_sign, 12)
    twelfth_lord = SIGN_LORD[twelfth_sign]
    twelfth_lord_sign = _get_planet_sign(planets, twelfth_lord)
    dist12 = _sign_distance(twelfth_sign, twelfth_lord_sign)

    if dist12 == 1:
        ul_sign = _sign_at_offset(twelfth_sign, 10)
    elif dist12 == 7:
        ul_sign = _sign_at_offset(twelfth_sign, 4)
    else:
        ul_sign = _sign_at_offset(twelfth_lord_sign, dist12)

    # --- Karakamsha (D9 sign of Atmakaraka) ---
    karakas = calculate_chara_karakas(planets)
    ak_planet = karakas[0]["planet"] if karakas else "Sun"

    karakamsha_sign = "Unknown"
    if d9_planets:
        karakamsha_sign = _get_planet_sign(d9_planets, ak_planet)
    else:
        # Approximate: use sign degree to compute Navamsha sign
        ak_lon = planets.get(ak_planet, {}).get("longitude", 0.0)
        d9_index = int((float(ak_lon) % 360.0) / (360.0 / 108.0)) % 12
        karakamsha_sign = ZODIAC[d9_index]

    return {
        "arudha_lagna": {
            "sign": al_sign,
            "house": _sign_distance(asc_sign, al_sign),
        },
        "upapada_lagna": {
            "sign": ul_sign,
            "house": _sign_distance(asc_sign, ul_sign),
        },
        "karakamsha": {
            "sign": karakamsha_sign,
            "atmakaraka": ak_planet,
            "house": _sign_distance(asc_sign, karakamsha_sign),
        },
    }


# ============================================================
# 3. JAIMINI DRISHTI (Sign-based aspects)
# ============================================================

def calculate_jaimini_drishti() -> Dict:
    """
    Cardinal signs aspect Fixed signs (except adjacent).
    Fixed signs aspect Cardinal signs (except adjacent).
    Dual signs aspect all other Dual signs.
    """
    aspects: Dict[str, List[str]] = {}

    for sign in ZODIAC:
        idx = _sign_index(sign)
        aspected = []

        if sign in CARDINAL:
            for target in FIXED:
                t_idx = _sign_index(target)
                if abs(idx - t_idx) != 1 and abs(idx - t_idx) != 11:
                    aspected.append(target)
        elif sign in FIXED:
            for target in CARDINAL:
                t_idx = _sign_index(target)
                if abs(idx - t_idx) != 1 and abs(idx - t_idx) != 11:
                    aspected.append(target)
        else:  # DUAL
            for target in DUAL:
                if target != sign:
                    aspected.append(target)

        aspects[sign] = aspected

    return {"sign_aspects": aspects}


# ============================================================
# 4. CHARA DASHA (Sign-based timing)
# ============================================================

def calculate_chara_dasha(planets: Dict, ascendant: Dict, birth_date: str) -> Dict:
    """
    Chara Dasha periods based on sign distances.
    Each sign gets a period = distance from sign to its lord's sign.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    asc_idx = _sign_index(asc_sign)

    # Determine order: odd sign = forward, even sign = backward
    is_odd = asc_idx % 2 == 0  # Aries=0 (odd sign), Taurus=1 (even sign)

    if is_odd:
        sign_order = [ZODIAC[(asc_idx + i) % 12] for i in range(12)]
    else:
        sign_order = [ZODIAC[(asc_idx - i) % 12] for i in range(12)]

    # Calculate period for each sign
    periods = []
    try:
        start = datetime.strptime(str(birth_date).split("T")[0].split(" ")[0], "%Y-%m-%d")
    except Exception:
        start = datetime(2000, 1, 1)

    for sign in sign_order:
        lord = SIGN_LORD[sign]
        lord_sign = _get_planet_sign(planets, lord)
        dist = _sign_distance(sign, lord_sign)

        # For even signs, adjust: years = 12 - dist
        s_idx = _sign_index(sign)
        if s_idx % 2 == 1:  # even sign
            years = 12 - dist
        else:
            years = dist - 1  # 0-indexed

        years = max(1, min(years, 12))  # clamp 1-12

        end = start + timedelta(days=years * 365.25)
        periods.append({
            "sign": sign,
            "lord": lord,
            "years": years,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
        })
        start = end

    # Mark current period
    now = datetime.now()
    current_idx = -1
    for i, p in enumerate(periods):
        s = datetime.strptime(p["start_date"], "%Y-%m-%d")
        e = datetime.strptime(p["end_date"], "%Y-%m-%d")
        if s <= now <= e:
            current_idx = i
            break

    return {
        "periods": periods,
        "current_period_index": current_idx,
        "total_years": sum(p["years"] for p in periods),
    }


# ============================================================
# 5. INDU LAGNA (Wealth indicator)
# ============================================================

def calculate_indu_lagna(planets: Dict, ascendant: Dict) -> Dict:
    """
    Indu Lagna calculation:
    1. Find 9th lord from Lagna
    2. Find 9th lord from Moon
    3. Add Kaksha values of both lords
    4. Remainder when divided by 12 → count from Moon sign
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    moon_sign = _get_planet_sign(planets, "Moon")

    # 9th house from Lagna
    ninth_from_lagna = _sign_at_offset(asc_sign, 9)
    ninth_lord_lagna = SIGN_LORD[ninth_from_lagna]

    # 9th house from Moon
    ninth_from_moon = _sign_at_offset(moon_sign, 9)
    ninth_lord_moon = SIGN_LORD[ninth_from_moon]

    kaksha_1 = KAKSHA_VALUES.get(ninth_lord_lagna, 1)
    kaksha_2 = KAKSHA_VALUES.get(ninth_lord_moon, 1)
    total = kaksha_1 + kaksha_2
    remainder = total % 12

    indu_sign = _sign_at_offset(moon_sign, remainder + 1)

    return {
        "indu_lagna_sign": indu_sign,
        "indu_lagna_house": _sign_distance(asc_sign, indu_sign),
        "ninth_lord_lagna": ninth_lord_lagna,
        "ninth_lord_moon": ninth_lord_moon,
        "kaksha_sum": total,
        "remainder": remainder,
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_jaimini(chart_data: Dict, birth_date: str = "") -> Dict:
    """Calculate all Jaimini components from chart data."""
    planets = chart_data.get("planets", {})
    ascendant = chart_data.get("ascendant", {})

    return {
        "chara_karakas": calculate_chara_karakas(planets),
        "special_lagnas": calculate_special_lagnas(planets, ascendant),
        "jaimini_drishti": calculate_jaimini_drishti(),
        "chara_dasha": calculate_chara_dasha(planets, ascendant, birth_date),
        "indu_lagna": calculate_indu_lagna(planets, ascendant),
    }
