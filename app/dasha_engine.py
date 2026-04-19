"""
dasha_engine.py — Vimshottari Dasha Calculation Engine
=======================================================
Computes Mahadasha, Antardasha, and Pratyantar Dasha periods based on
birth nakshatra. Vimshottari total = 120 years. Order starts from birth
nakshatra lord. The balance of the first dasha is calculated based on
the Moon's position within the nakshatra at birth.

Also provides classical effect synthesis (Phaladeepika Adhyaya 20 & 21):
  - analyze_mahadasha_phala()
  - analyze_antardasha_phala()
  - get_current_dasha_phala()
"""
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


# ============================================================
# CONSTANTS
# ============================================================

# Planet -> years in Vimshottari Dasha system (total = 120)
DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# Fixed cyclic order of Vimshottari Dasha
DASHA_ORDER = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury",
]

# 27 Nakshatras mapped to their ruling planet
NAKSHATRA_LORD = {
    "Ashwini": "Ketu",
    "Bharani": "Venus",
    "Krittika": "Sun",
    "Rohini": "Moon",
    "Mrigashira": "Mars",
    "Ardra": "Rahu",
    "Punarvasu": "Jupiter",
    "Pushya": "Saturn",
    "Ashlesha": "Mercury",
    "Magha": "Ketu",
    "Purva Phalguni": "Venus",
    "Uttara Phalguni": "Sun",
    "Hasta": "Moon",
    "Chitra": "Mars",
    "Swati": "Rahu",
    "Vishakha": "Jupiter",
    "Anuradha": "Saturn",
    "Jyeshtha": "Mercury",
    "Mula": "Ketu",
    "Purva Ashadha": "Venus",
    "Uttara Ashadha": "Sun",
    "Shravana": "Moon",
    "Dhanishta": "Mars",
    "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter",
    "Uttara Bhadrapada": "Saturn",
    "Revati": "Mercury",
}

# Nakshatra order for computing Moon's position within nakshatra
NAKSHATRA_ORDER = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

VIMSHOTTARI_TOTAL = 120  # years
NAKSHATRA_SPAN = 13 + 20.0 / 60.0  # 13°20' = 13.3333°


def _get_dasha_sequence(starting_lord: str) -> list:
    """Return the 9-planet dasha sequence starting from a given lord."""
    start_idx = DASHA_ORDER.index(starting_lord)
    return DASHA_ORDER[start_idx:] + DASHA_ORDER[:start_idx]


def _calculate_dasha_balance(birth_nakshatra: str, moon_longitude: float = None) -> float:
    """
    Calculate the balance (remaining fraction) of the first Mahadasha at birth.

    In Vimshottari Dasha, the first dasha's remaining period depends on how far
    the Moon has traversed through its birth nakshatra. If the Moon is at the
    START of a nakshatra, the full dasha period remains. If at the END, almost
    none remains and the next dasha starts.

    Args:
        birth_nakshatra: Name of Moon's birth nakshatra
        moon_longitude: Moon's sidereal longitude in degrees (0-360).
                       If None, returns 1.0 (full balance — legacy behavior).

    Returns:
        Float between 0.0 and 1.0 representing the remaining fraction of the
        first dasha at birth.
    """
    if moon_longitude is None:
        return 1.0  # Legacy fallback: full dasha from birth

    # Normalize to 0..360 (handles negatives and multiples like -1, 360, 721)
    moon_longitude = moon_longitude % 360.0

    # Find nakshatra index
    try:
        nak_index = NAKSHATRA_ORDER.index(birth_nakshatra)
    except ValueError:
        return 1.0

    # Nakshatra start longitude = index * 13.3333°
    nak_start = nak_index * NAKSHATRA_SPAN

    # How far Moon has traversed this nakshatra
    traversed = moon_longitude - nak_start
    if traversed < 0:
        traversed += 360.0
    if traversed > NAKSHATRA_SPAN:
        traversed = NAKSHATRA_SPAN  # clamp

    # Remaining fraction = how much of the nakshatra is LEFT
    remaining_fraction = (NAKSHATRA_SPAN - traversed) / NAKSHATRA_SPAN

    # Clamp between 0 and 1
    return max(0.0, min(1.0, remaining_fraction))


def _parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _build_pratyantar_periods(
    antardasha_planet: str,
    antardasha_duration_days: float,
    antardasha_start: datetime,
    now: datetime,
) -> list:
    """Build Pratyantar Dasha periods within an Antardasha."""
    pratyantar_seq = _get_dasha_sequence(antardasha_planet)
    pratyantar_periods = []
    p_start = antardasha_start

    for p_planet in pratyantar_seq:
        p_years = DASHA_YEARS[p_planet]
        # Pratyantar duration = (antardasha_duration_days * p_years / 120)
        p_duration_days = (antardasha_duration_days * p_years) / VIMSHOTTARI_TOTAL
        p_end = p_start + timedelta(days=p_duration_days)

        is_current = (p_start <= now <= p_end)

        pratyantar_periods.append({
            "planet": p_planet,
            "start": p_start.strftime("%Y-%m-%d"),
            "end": p_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        p_start = p_end

    return pratyantar_periods


def _build_antardasha_periods(
    mahadasha_planet: str,
    mahadasha_years: int,
    mahadasha_start: datetime,
    now: datetime,
) -> list:
    """Build Antardasha periods (with nested Pratyantar) within a Mahadasha."""
    antardasha_seq = _get_dasha_sequence(mahadasha_planet)
    antardasha_periods = []
    ad_start = mahadasha_start

    for ad_planet in antardasha_seq:
        ad_years = DASHA_YEARS[ad_planet]
        # Antardasha duration = (mahadasha_years * ad_years / 120) years in days
        ad_duration_days = (mahadasha_years * ad_years / VIMSHOTTARI_TOTAL) * 365.25
        ad_end = ad_start + timedelta(days=ad_duration_days)

        is_current = (ad_start <= now <= ad_end)

        # Build pratyantar only for current antardasha to keep payload reasonable
        pratyantar = []
        if is_current:
            pratyantar = _build_pratyantar_periods(
                ad_planet, ad_duration_days, ad_start, now
            )

        antardasha_periods.append({
            "planet": ad_planet,
            "start": ad_start.strftime("%Y-%m-%d"),
            "end": ad_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
            "pratyantar": pratyantar,
        })
        ad_start = ad_end

    return antardasha_periods


def calculate_dasha(birth_nakshatra: str, birth_date: str, moon_longitude: float = None) -> dict:
    """
    Calculate Vimshottari Dasha periods from birth nakshatra and birth date.

    The first dasha's balance is calculated from the Moon's position within
    the nakshatra. Only the REMAINING portion of the first dasha applies
    from birth — the elapsed portion is excluded.

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini", "Rohini")
        birth_date: Birth date as "YYYY-MM-DD"
        moon_longitude: Moon's sidereal longitude in degrees (0-360)

    Returns:
        {
            mahadasha_periods: [{planet, start_date, end_date, years}],
            current_dasha: str,
            current_antardasha: str,
        }
    """
    if birth_nakshatra not in NAKSHATRA_LORD:
        return {
            "mahadasha_periods": [],
            "current_dasha": "Unknown",
            "current_antardasha": "Unknown",
            "error": f"Unknown nakshatra: {birth_nakshatra}",
        }

    starting_lord = NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Calculate balance of first dasha at birth
    balance = _calculate_dasha_balance(birth_nakshatra, moon_longitude)

    # Build mahadasha periods
    mahadasha_periods = []
    current_start = birth_dt

    for i, planet in enumerate(sequence):
        full_years = DASHA_YEARS[planet]
        # First planet gets only the remaining balance
        # No intermediate rounding — only round for display, not date math
        if i == 0:
            effective_years = full_years * balance
        else:
            effective_years = full_years
        end_dt = current_start + timedelta(days=effective_years * 365.25)
        mahadasha_periods.append({
            "planet": planet,
            "start_date": current_start.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "years": round(effective_years, 4),
        })
        current_start = end_dt

    # Extend with additional cycles until we cover at least 240 years from birth
    min_coverage = birth_dt + timedelta(days=240 * 365.25)
    while current_start < min_coverage:
        for planet in sequence:
            full_years = DASHA_YEARS[planet]
            end_dt = current_start + timedelta(days=full_years * 365.25)
            mahadasha_periods.append({
                "planet": planet,
                "start_date": current_start.strftime("%Y-%m-%d"),
                "end_date": end_dt.strftime("%Y-%m-%d"),
                "years": full_years,
            })
            current_start = end_dt

    # Determine current mahadasha
    current_dasha = "Unknown"
    current_dasha_start = None
    current_dasha_years = 0
    for period in mahadasha_periods:
        start_dt = _parse_date(period["start_date"])
        end_dt = _parse_date(period["end_date"])
        if start_dt <= now <= end_dt:
            current_dasha = period["planet"]
            current_dasha_start = start_dt
            current_dasha_years = period["years"]
            break

    # If now is still beyond all periods, use the last period as fallback
    if current_dasha == "Unknown" and now > _parse_date(mahadasha_periods[-1]["end_date"]):
        current_dasha = mahadasha_periods[-1]["planet"]
        current_dasha_start = _parse_date(mahadasha_periods[-1]["start_date"])
        current_dasha_years = mahadasha_periods[-1]["years"]

    # Determine current antardasha within the mahadasha
    current_antardasha = "Unknown"
    if current_dasha != "Unknown" and current_dasha_start is not None:
        antardasha_seq = _get_dasha_sequence(current_dasha)
        antardasha_start = current_dasha_start
        mahadasha_total_days = current_dasha_years * 365.25

        for sub_planet in antardasha_seq:
            # Antardasha duration = (mahadasha_years * sub_planet_years / 120) years
            sub_years = DASHA_YEARS[sub_planet]
            sub_duration_days = (current_dasha_years * sub_years / VIMSHOTTARI_TOTAL) * 365.25
            sub_end = antardasha_start + timedelta(days=sub_duration_days)

            if antardasha_start <= now <= sub_end:
                current_antardasha = sub_planet
                break
            antardasha_start = sub_end

    return {
        "mahadasha_periods": mahadasha_periods,
        "current_dasha": current_dasha,
        "current_antardasha": current_antardasha,
    }


def calculate_extended_dasha(birth_nakshatra: str, birth_date: str, moon_longitude: float = None) -> dict:
    """
    Calculate extended Vimshottari Dasha with Mahadasha -> Antardasha -> Pratyantar.

    The first dasha's balance is calculated from the Moon's position within
    the nakshatra at birth.

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini", "Rohini")
        birth_date: Birth date as "YYYY-MM-DD"
        moon_longitude: Moon's sidereal longitude in degrees (0-360)

    Returns:
        {
            mahadasha: [{planet, start, end, is_current, antardasha: [{...}]}],
            current_dasha: str,
            current_antardasha: str,
            current_pratyantar: str,
        }
    """
    if birth_nakshatra not in NAKSHATRA_LORD:
        return {
            "mahadasha": [],
            "current_dasha": "Unknown",
            "current_antardasha": "Unknown",
            "current_pratyantar": "Unknown",
            "error": f"Unknown nakshatra: {birth_nakshatra}",
        }

    starting_lord = NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Calculate balance of first dasha at birth
    balance = _calculate_dasha_balance(birth_nakshatra, moon_longitude)

    mahadasha_list = []
    current_start = birth_dt
    current_dasha = "Unknown"
    current_antardasha = "Unknown"
    current_pratyantar = "Unknown"

    def _append_mahadasha(planet, effective_years, current_start, is_first_cycle_first_planet=False):
        """Helper to build and append a single mahadasha entry."""
        nonlocal current_dasha, current_antardasha, current_pratyantar
        end_dt = current_start + timedelta(days=effective_years * 365.25)
        is_current = (current_start <= now <= end_dt)

        if is_current:
            current_dasha = planet

        # Build antardasha for every mahadasha (but pratyantar only for current)
        antardasha = _build_antardasha_periods(
            planet, effective_years, current_start, now
        )

        # Find current antardasha and pratyantar
        if is_current:
            for ad in antardasha:
                if ad["is_current"]:
                    current_antardasha = ad["planet"]
                    for pt in ad.get("pratyantar", []):
                        if pt["is_current"]:
                            current_pratyantar = pt["planet"]
                            break
                    break

        mahadasha_list.append({
            "planet": planet,
            "start": current_start.strftime("%Y-%m-%d"),
            "end": end_dt.strftime("%Y-%m-%d"),
            "years": round(effective_years, 4),
            "is_current": is_current,
            "antardasha": antardasha,
        })
        return end_dt

    # First cycle (9 periods, first one gets balance)
    for i, planet in enumerate(sequence):
        full_years = DASHA_YEARS[planet]
        # No intermediate rounding — only round for display, not date math
        effective_years = full_years * balance if i == 0 else full_years
        current_start = _append_mahadasha(planet, effective_years, current_start)

    # Extend with additional cycles until we cover at least 240 years from birth
    min_coverage = birth_dt + timedelta(days=240 * 365.25)
    while current_start < min_coverage:
        for planet in sequence:
            full_years = DASHA_YEARS[planet]
            current_start = _append_mahadasha(planet, full_years, current_start)

    return {
        "mahadasha": mahadasha_list,
        "current_dasha": current_dasha,
        "current_antardasha": current_antardasha,
        "current_pratyantar": current_pratyantar,
    }


# ============================================================
# PHALADEEPIKA ADHYAYA 20 + 21 — DASHA-PHALA SYNTHESIS
# ============================================================

# Data file path
_DASHA_PHALA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "dasha_phala.json"
)

# Classical tables (kept local so this module has no hard dependency
# on ayurdaya_engine and remains importable even if that module changes)
_SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
_EXALTATION_SIGN = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra",
}
_DEBILITATION_SIGN = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries",
}
_KENDRAS = {1, 4, 7, 10}
_TRIKONAS = {1, 5, 9}
_DUSTHANAS = {6, 8, 12}
_BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

_ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
_SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}
_HOUSE_AREAS_EN: Dict[int, str] = {
    1: "self/health/identity", 2: "wealth/family/speech", 3: "courage/siblings/travel",
    4: "home/mother/comfort", 5: "children/creativity/education", 6: "enemies/debts/disease",
    7: "marriage/partnerships", 8: "longevity/transformation/inheritance",
    9: "fortune/father/dharma", 10: "career/status/authority",
    11: "gains/social network/desires", 12: "losses/expenses/liberation",
}
_HOUSE_AREAS_HI: Dict[int, str] = {
    1: "स्व/स्वास्थ्य", 2: "धन/परिवार", 3: "पराक्रम/भाई",
    4: "गृह/माता", 5: "संतान/शिक्षा", 6: "शत्रु/ऋण/रोग",
    7: "विवाह/साझेदारी", 8: "आयु/परिवर्तन", 9: "भाग्य/पिता/धर्म",
    10: "कर्म/प्रतिष्ठा", 11: "लाभ/इच्छापूर्ति", 12: "व्यय/मोक्ष",
}

_DASHA_PHALA_CACHE: Optional[Dict[str, Any]] = None


def _load_dasha_phala() -> Dict[str, Any]:
    """Load the Phaladeepika mahadasha + antardasha effect data (cached)."""
    global _DASHA_PHALA_CACHE
    if _DASHA_PHALA_CACHE is not None:
        return _DASHA_PHALA_CACHE
    try:
        with open(_DASHA_PHALA_PATH, "r", encoding="utf-8") as f:
            _DASHA_PHALA_CACHE = json.load(f)
    except (OSError, json.JSONDecodeError):
        _DASHA_PHALA_CACHE = {"mahadasha_effects": {}, "antardasha_matrix": {}}
    return _DASHA_PHALA_CACHE


def _planet_info(planet: str, chart_data: dict) -> Dict[str, Any]:
    """Safely extract {sign, house, combust, retrograde} for a planet."""
    planets = (chart_data or {}).get("planets", {}) or {}
    info = planets.get(planet) or {}
    sign = str(info.get("sign", "") or "")
    try:
        house = int(info.get("house", 0) or 0)
    except (TypeError, ValueError):
        house = 0
    combust = bool(info.get("combust", info.get("is_combust", False)))
    retro = bool(info.get("retrograde", info.get("is_retrograde", False)))
    return {"sign": sign, "house": house, "combust": combust, "retrograde": retro}


# ============================================================
# ITEMS 5 & 6 — Dasha Quality Tags (Phaladeepika Adh. 20)
# Auspicious: exalted / Vargottama
# Challenging: debilitated / combust / Papakartari
# ============================================================

# Navamsha starting sign index for each D1 sign index
# fire→Aries(0), earth→Capricorn(9), air→Libra(6), water→Cancer(3)
_NAVAMSHA_START_IDX: Dict[int, int] = {
    0: 0, 1: 9, 2: 6, 3: 3,
    4: 0, 5: 9, 6: 6, 7: 3,
    8: 0, 9: 9, 10: 6, 11: 3,
}


def _d9_sign(longitude: float) -> str:
    """Compute D9 (Navamsha) sign from absolute ecliptic longitude."""
    sign_idx = int(longitude / 30) % 12
    deg_in_sign = longitude % 30
    nav_part = int(deg_in_sign / (10.0 / 3.0))  # 0–8
    start = _NAVAMSHA_START_IDX[sign_idx]
    d9_idx = (start + nav_part) % 12
    return _ZODIAC[d9_idx]


def _is_vargottama(longitude: float, d1_sign: str) -> bool:
    """True when D1 sign == D9 sign — planet is Vargottama."""
    if longitude <= 0 or not d1_sign:
        return False
    return _d9_sign(longitude) == d1_sign


def _is_in_papakartari(planet: str, planet_house: int, planets: dict) -> bool:
    """
    Planet is in Papakartari when malefics occupy BOTH adjacent houses.
    house_before = (house - 2) % 12 + 1, house_after = house % 12 + 1.
    """
    if not (1 <= planet_house <= 12):
        return False
    house_before = ((planet_house - 2) % 12) + 1
    house_after = (planet_house % 12) + 1

    mal_before = any(
        m != planet
        and isinstance(planets.get(m), dict)
        and int((planets[m] or {}).get("house", 0) or 0) == house_before
        for m in _MALEFICS
    )
    mal_after = any(
        m != planet
        and isinstance(planets.get(m), dict)
        and int((planets[m] or {}).get("house", 0) or 0) == house_after
        for m in _MALEFICS
    )
    return mal_before and mal_after


def _dasha_quality_tag(
    planet: str,
    chart_data: dict,
    factors: list,
) -> dict:
    """
    Build dasha quality tag per Phaladeepika Adh. 20 dignity rules.

    Returns:
        {
          "tag": "Auspicious" | "Challenging" | "Neutral",
          "tag_hi": str,
          "label_en": str,
          "label_hi": str,
          "reasons": [str, ...],
          "sloka_ref": "Phaladeepika Adh. 20"
        }
    """
    planets = (chart_data or {}).get("planets", {}) or {}
    pdata = planets.get(planet) or {}
    longitude = float(pdata.get("longitude", 0.0) or 0.0)
    d1_sign = str(pdata.get("sign", "") or "")
    house = int(pdata.get("house", 0) or 0)

    reasons: List[str] = []
    auspicious_count = 0
    challenging_count = 0

    # --- Auspicious signals ---
    if "exalted" in factors:
        auspicious_count += 2
        reasons.append(
            f"{planet} is exalted — exceptional strength; "
            f"dasha gives superior results (Uccha-bala)."
        )
    if _is_vargottama(longitude, d1_sign):
        auspicious_count += 2
        reasons.append(
            f"{planet} is Vargottama (same sign D1 and D9) — double dignity; "
            f"dasha results are consistent, strong, and long-lasting."
        )
    if "own_sign" in factors and "exalted" not in factors:
        auspicious_count += 1
        reasons.append(f"{planet} in own sign — stable, beneficial dasha results.")
    if "kendra" in factors and auspicious_count == 0:
        auspicious_count += 1
        reasons.append(f"{planet} in Kendra — angular strength supports the dasha.")

    # --- Challenging signals ---
    if "debilitated" in factors:
        challenging_count += 2
        reasons.append(
            f"{planet} is debilitated — weakened; "
            f"dasha may bring hardship, delays, and frustration."
        )
    if "combust" in factors:
        challenging_count += 2
        reasons.append(
            f"{planet} is combust (within orb of Sun) — diminished by solar rays; "
            f"significations of {planet} suffer during this dasha."
        )
    if _is_in_papakartari(planet, house, planets):
        challenging_count += 1
        reasons.append(
            f"{planet} is in Papakartari — malefics flank it on both sides; "
            f"the dasha activates a period of obstruction and difficulty."
        )

    # --- Determine tag ---
    if auspicious_count >= 2 and challenging_count == 0:
        tag = "Auspicious"
        tag_hi = "शुभ"
        label_en = (
            "Auspicious (Shubha) Dasha — planet is dignified, "
            "giving strong positive results."
        )
        label_hi = (
            "शुभ दशा — ग्रह बली एवं प्रतिष्ठित है; श्रेष्ठ परिणाम प्राप्त होते हैं।"
        )
    elif challenging_count >= 2 or ("debilitated" in factors and "combust" in factors):
        tag = "Challenging"
        tag_hi = "कठिन"
        label_en = (
            "Challenging (Kashta) Dasha — planet is afflicted; "
            "period brings hardship requiring effort and remedies."
        )
        label_hi = (
            "कठिन दशा — ग्रह पीड़ित है; यह काल कठिनाइयाँ लाता है, "
            "उपाय एवं परिश्रम आवश्यक है।"
        )
    elif auspicious_count > 0 and challenging_count == 0:
        tag = "Auspicious"
        tag_hi = "शुभ"
        label_en = (
            "Mildly Auspicious Dasha — planet has some dignity; "
            "generally positive results."
        )
        label_hi = "मध्यम शुभ दशा — ग्रह में कुछ बल है; सामान्यतः सकारात्मक परिणाम।"
    elif challenging_count > 0 and auspicious_count == 0:
        tag = "Challenging"
        tag_hi = "कठिन"
        label_en = (
            "Mildly Challenging Dasha — planet has some affliction; "
            "care and remedies recommended."
        )
        label_hi = (
            "मध्यम कठिन दशा — ग्रह पर कुछ पीड़ा है; सावधानी एवं उपाय अनुशंसित।"
        )
    else:
        tag = "Neutral"
        tag_hi = "मध्यम"
        label_en = (
            "Neutral Dasha — mixed signals; "
            "results depend on the Antardasha lord and transits."
        )
        label_hi = (
            "मध्यम दशा — मिश्रित संकेत; "
            "परिणाम अंतर्दशा स्वामी एवं गोचर पर निर्भर।"
        )

    return {
        "tag": tag,
        "tag_hi": tag_hi,
        "label_en": label_en,
        "label_hi": label_hi,
        "reasons": reasons,
        "sloka_ref": "Phaladeepika Adh. 20",
    }


def _assess_planet_strength(planet: str, chart_data: dict) -> Dict[str, Any]:
    """
    Classify a planet as 'strong' | 'weak' | 'neutral' and collect evidence.

    Rules (Phaladeepika-aligned):
      STRONG  : exalted, own-sign, OR in Kendra (1/4/7/10) or Trikona (1/5/9)
      WEAK    : debilitated, in Dusthana (6/8/12), or combust
      NEUTRAL : anything else
    """
    info = _planet_info(planet, chart_data)
    sign, house = info["sign"], info["house"]
    factors: List[str] = []

    if not sign and not house:
        return {"strength": "neutral", "factors": ["no_data"], "info": info}

    # Strong signals
    if _EXALTATION_SIGN.get(planet) == sign:
        factors.append("exalted")
    if _SIGN_LORD.get(sign) == planet:
        factors.append("own_sign")
    if house in _KENDRAS:
        factors.append("kendra")
    if house in _TRIKONAS:
        factors.append("trikona")

    # Weak signals
    if _DEBILITATION_SIGN.get(planet) == sign:
        factors.append("debilitated")
    if house in _DUSTHANAS:
        factors.append("dusthana")
    if info["combust"]:
        factors.append("combust")

    strong_hits = {"exalted", "own_sign", "kendra", "trikona"} & set(factors)
    weak_hits = {"debilitated", "dusthana", "combust"} & set(factors)

    # Debilitated/combust dominates any positional goodness
    if {"debilitated", "combust"} & weak_hits:
        strength = "weak"
    elif strong_hits and not weak_hits:
        strength = "strong"
    elif weak_hits and not strong_hits:
        strength = "weak"
    elif strong_hits and weak_hits:
        strength = "neutral"
    else:
        strength = "neutral"

    return {"strength": strength, "factors": factors, "info": info}


def _houses_for_planet(planet: str, chart_data: dict) -> Dict[str, Any]:
    """Return owned, occupied, and aspected house numbers for a dasha planet."""
    asc_sign = str(((chart_data or {}).get("ascendant") or {}).get("sign", "") or "")
    info = _planet_info(planet, chart_data)
    occupied_house = info["house"]

    owned_houses: List[int] = []
    if asc_sign in _ZODIAC:
        asc_idx = _ZODIAC.index(asc_sign)
        for sign, lord in _SIGN_LORD.items():
            if lord == planet:
                sign_idx = _ZODIAC.index(sign)
                owned_houses.append(((sign_idx - asc_idx) % 12) + 1)
        owned_houses = sorted(set(owned_houses))

    aspected_houses: List[int] = []
    if 1 <= occupied_house <= 12:
        offsets = [7] + list(_SPECIAL_ASPECTS.get(planet, []))
        for n in offsets:
            aspected_houses.append(((occupied_house - 1 + (n - 1)) % 12) + 1)
        aspected_houses = sorted(set(aspected_houses))

    return {
        "owned_houses": owned_houses,
        "occupied_house": occupied_house,
        "aspected_houses": aspected_houses,
    }


def analyze_mahadasha_phala(planet: str, chart_data: dict) -> Dict[str, Any]:
    """
    Synthesize the classical effect of a mahadasha per Phaladeepika Adh. 20.

    Args:
        planet: One of Sun/Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus
        chart_data: Kundli chart dict with `planets` keyed by name.

    Returns:
        {
            planet, strength, factors, effect_en, effect_hi,
            when_strong_en/hi, when_weak_en/hi, general_en/hi,
            sloka_ref
        }
    """
    data = _load_dasha_phala()
    entry = (data.get("mahadasha_effects") or {}).get(planet, {})

    if not entry:
        return {
            "planet": planet,
            "strength": "neutral",
            "factors": [],
            "effect_en": "",
            "effect_hi": "",
            "sloka_ref": "",
            "error": f"No mahadasha data for planet: {planet}",
        }

    assessment = _assess_planet_strength(planet, chart_data or {})
    strength = assessment["strength"]
    quality_tag = _dasha_quality_tag(planet, chart_data or {}, assessment["factors"])

    if strength == "strong":
        effect_en = entry.get("when_strong_en", entry.get("general_en", ""))
        effect_hi = entry.get("when_strong_hi", entry.get("general_hi", ""))
    elif strength == "weak":
        effect_en = entry.get("when_weak_en", entry.get("general_en", ""))
        effect_hi = entry.get("when_weak_hi", entry.get("general_hi", ""))
    else:
        effect_en = entry.get("general_en", "")
        effect_hi = entry.get("general_hi", "")

    # P1 #13: House synthesis — dasha planet delivers results of owned + occupied + aspected houses
    # (Phaladeepika Adh. 20: phalaṃ dadyāt svakṣetrasthāna-dṛṣṭa-bhavānāṃ)
    h_info = _houses_for_planet(planet, chart_data or {})
    all_activated = sorted(set(
        h_info["owned_houses"]
        + ([h_info["occupied_house"]] if h_info["occupied_house"] else [])
        + h_info["aspected_houses"]
    ))
    activated_descs_en = [f"H{h} ({_HOUSE_AREAS_EN.get(h, '')})" for h in all_activated]
    activated_descs_hi = [f"भाव {h} ({_HOUSE_AREAS_HI.get(h, '')})" for h in all_activated]
    owned_str = ", ".join(f"H{h}" for h in h_info["owned_houses"]) or "none"
    owned_str_hi = ", ".join(f"भाव {h}" for h in h_info["owned_houses"]) or "कोई नहीं"
    asp_str = ", ".join(str(h) for h in h_info["aspected_houses"]) or "none"
    asp_str_hi = ", ".join(str(h) for h in h_info["aspected_houses"]) or "कोई नहीं"

    house_synthesis_en = (
        f"During {planet}'s Mahadasha, life areas activated: {', '.join(activated_descs_en)}. "
        f"{planet} owns {owned_str}, occupies H{h_info['occupied_house'] or '?'}, "
        f"and aspects houses {asp_str} (Phaladeepika Adh. 20)."
    )
    house_synthesis_hi = (
        f"{planet} की महादशा में सक्रिय क्षेत्र: {', '.join(activated_descs_hi)}। "
        f"{planet} {owned_str_hi} का स्वामी है, भाव {h_info['occupied_house'] or '?'} में स्थित है, "
        f"तथा भाव {asp_str_hi} पर दृष्टि डालता है (फलदीपिका अ. 20)।"
    )

    # --- Dignity Modifier (Phaladeepika Adh. 19-20) ---
    factors = assessment["factors"]
    planets_data = (chart_data or {}).get("planets", {}) or {}
    pdata_entry = planets_data.get(planet) or {}
    planet_lon = float(pdata_entry.get("longitude", 0.0) or 0.0)
    planet_d1_sign = str(pdata_entry.get("sign", "") or "")
    planet_house = int(pdata_entry.get("house", 0) or 0)

    is_exalted_dm = "exalted" in factors
    is_vargottama_dm = _is_vargottama(planet_lon, planet_d1_sign)
    is_debilitated_dm = "debilitated" in factors
    is_combust_dm = "combust" in factors
    is_papakartari_dm = _is_in_papakartari(planet, planet_house, planets_data)

    if is_exalted_dm or is_vargottama_dm:
        dignity_modifier = "excellent"
        if is_exalted_dm and is_vargottama_dm:
            dignity_note_en = (
                f"{planet} is both exalted and Vargottama — dasha promises the highest elevated results."
            )
            dignity_note_hi = (
                f"{planet} उच्च और वर्गोत्तम दोनों है — दशा सर्वोत्तम उत्कृष्ट फल देगी।"
            )
        elif is_exalted_dm:
            dignity_note_en = (
                f"{planet} is exalted — dasha promises elevated results (Phaladeepika Adh. 19)."
            )
            dignity_note_hi = (
                f"{planet} उच्च है — दशा उत्कृष्ट फल देगी (फलदीपिका अ. 19)।"
            )
        else:
            dignity_note_en = (
                f"{planet} is Vargottama (same sign D1 & D9) — dasha gives consistent, elevated results."
            )
            dignity_note_hi = (
                f"{planet} वर्गोत्तम है (D1 और D9 में समान राशि) — दशा सुसंगत उत्कृष्ट फल देगी।"
            )
    elif is_debilitated_dm or is_combust_dm:
        dignity_modifier = "challenged"
        if is_debilitated_dm and is_combust_dm:
            dignity_note_en = (
                f"{planet} is both debilitated and combust — dasha period is severely challenged; "
                f"remedies strongly recommended."
            )
            dignity_note_hi = (
                f"{planet} नीच और अस्त दोनों है — दशा काल अत्यंत कठिन; उपाय अत्यावश्यक।"
            )
        elif is_debilitated_dm:
            dignity_note_en = (
                f"{planet} is debilitated — dasha brings hardship and reduced signification results."
            )
            dignity_note_hi = (
                f"{planet} नीच है — दशा में कठिनाई और ग्रह-फल में कमी।"
            )
        else:
            dignity_note_en = (
                f"{planet} is combust (too close to Sun) — dasha significations are diminished."
            )
            dignity_note_hi = (
                f"{planet} अस्त है (सूर्य के निकट) — दशा में ग्रह-कारकत्व न्यून।"
            )
    elif is_papakartari_dm:
        dignity_modifier = "obstructed"
        dignity_note_en = (
            f"{planet} is in Papakartari (malefics on both adjacent houses) — "
            f"dasha activates a period of obstruction and difficulty."
        )
        dignity_note_hi = (
            f"{planet} पापकर्तरी में है (दोनों आसन्न भावों में पापग्रह) — "
            f"दशा में अवरोध और कठिनाई।"
        )
    else:
        dignity_modifier = "neutral"
        dignity_note_en = (
            f"{planet} is in a neutral dignity state — dasha gives mixed or average results "
            f"based on house placement and transits."
        )
        dignity_note_hi = (
            f"{planet} मध्यम बल में है — दशा में मिश्रित या सामान्य फल; "
            f"भाव-स्थिति और गोचर पर निर्भर।"
        )

    return {
        "planet": planet,
        "strength": strength,
        "factors": assessment["factors"],
        "effect_en": effect_en,
        "effect_hi": effect_hi,
        "general_en": entry.get("general_en", ""),
        "general_hi": entry.get("general_hi", ""),
        "when_strong_en": entry.get("when_strong_en", ""),
        "when_strong_hi": entry.get("when_strong_hi", ""),
        "when_weak_en": entry.get("when_weak_en", ""),
        "when_weak_hi": entry.get("when_weak_hi", ""),
        "sloka_ref": entry.get("sloka_ref", ""),
        "owned_houses": h_info["owned_houses"],
        "occupied_house": h_info["occupied_house"],
        "aspected_houses": h_info["aspected_houses"],
        "house_synthesis_en": house_synthesis_en,
        "house_synthesis_hi": house_synthesis_hi,
        "dasha_quality": quality_tag,
        "dignity_modifier": dignity_modifier,
        "dignity_note_en": dignity_note_en,
        "dignity_note_hi": dignity_note_hi,
    }


def _planet_nature(planet: str) -> str:
    """Return 'benefic' | 'malefic' | 'neutral' for a planet (rough)."""
    if planet in _BENEFICS:
        return "benefic"
    if planet in _MALEFICS:
        return "malefic"
    return "neutral"


def analyze_antardasha_phala(
    mahadasha_lord: str, bhukti_lord: str, chart_data: dict
) -> Dict[str, Any]:
    """
    Synthesize the combined effect of an antardasha per Phaladeepika Adh. 21.

    Args:
        mahadasha_lord: Outer (mahadasha) planet
        bhukti_lord: Inner (antardasha) planet
        chart_data: Kundli chart dict

    Returns:
        {
            mahadasha, bhukti, effect_en, effect_hi, sloka_ref,
            severity: 'favorable' | 'mixed' | 'challenging',
            severity_factors: [...]
        }
    """
    data = _load_dasha_phala()
    matrix = data.get("antardasha_matrix", {}) or {}
    row = matrix.get(mahadasha_lord, {}) or {}
    entry = row.get(bhukti_lord, {}) or {}

    if not entry:
        return {
            "mahadasha": mahadasha_lord,
            "bhukti": bhukti_lord,
            "effect_en": "",
            "effect_hi": "",
            "sloka_ref": "",
            "severity": "mixed",
            "severity_factors": [],
            "error": f"No antardasha data for {mahadasha_lord}-{bhukti_lord}",
        }

    # Start from the classical baseline nature (from the data file)
    base = str(entry.get("nature", "mixed")).lower()
    if base not in {"favorable", "mixed", "challenging"}:
        base = "mixed"

    # Adjust using chart placement
    md_assess = _assess_planet_strength(mahadasha_lord, chart_data or {})
    bk_assess = _assess_planet_strength(bhukti_lord, chart_data or {})
    md_quality = _dasha_quality_tag(mahadasha_lord, chart_data or {}, md_assess["factors"])
    bk_quality = _dasha_quality_tag(bhukti_lord, chart_data or {}, bk_assess["factors"])

    factors: List[str] = []
    score = 0  # positive -> favorable, negative -> challenging
    if base == "favorable":
        score += 1
    elif base == "challenging":
        score -= 1

    for who, a in (("md", md_assess), ("bk", bk_assess)):
        if a["strength"] == "strong":
            score += 1
            factors.append(f"{who}_strong")
        elif a["strength"] == "weak":
            score -= 1
            factors.append(f"{who}_weak")

    # Benefic/malefic leaning
    if _planet_nature(mahadasha_lord) == "benefic":
        factors.append("md_benefic")
    elif _planet_nature(mahadasha_lord) == "malefic":
        factors.append("md_malefic")
    if _planet_nature(bhukti_lord) == "benefic":
        factors.append("bk_benefic")
    elif _planet_nature(bhukti_lord) == "malefic":
        factors.append("bk_malefic")

    if score >= 2:
        severity = "favorable"
    elif score <= -2:
        severity = "challenging"
    else:
        severity = "mixed"

    # P0-6: Combined synthesis — MD lord × AD lord blended narrative
    # (Phaladeepika Adh. 20-21: a planet gives results of its owned + occupied + aspected houses
    # during its period; the antardasha lord modifies that through its own chart placement.)
    md_strength = md_assess["strength"]
    bk_strength = bk_assess["strength"]
    md_sign = md_assess["info"].get("sign", "")
    bk_sign = bk_assess["info"].get("sign", "")
    md_house = md_assess["info"].get("house", 0)
    bk_house = bk_assess["info"].get("house", 0)

    # Build combined synthesis from MD general effect + AD specific effect
    md_data = _load_dasha_phala().get("mahadasha_effects", {}).get(mahadasha_lord, {})
    md_general = md_data.get("general_en", "") if md_strength == "neutral" else (
        md_data.get("when_strong_en", "") if md_strength == "strong" else md_data.get("when_weak_en", "")
    )
    ad_effect = entry.get("effect_en", "")

    md_qualifier = (
        f"a strong {mahadasha_lord} (in {md_sign}, house {md_house})"
        if md_strength == "strong" else
        f"a weakened {mahadasha_lord} (in {md_sign}, house {md_house})"
        if md_strength == "weak" else
        f"{mahadasha_lord} (in {md_sign}, house {md_house})"
    )
    bk_qualifier = (
        f"a strong {bhukti_lord} (in {bk_sign}, house {bk_house})"
        if bk_strength == "strong" else
        f"a weakened {bhukti_lord} (in {bk_sign}, house {bk_house})"
        if bk_strength == "weak" else
        f"{bhukti_lord} (in {bk_sign}, house {bk_house})"
    )
    combined_en = (
        f"During {md_qualifier}'s Mahadasha: {md_general} "
        f"Within this, {bk_qualifier}'s Antardasha produces: {ad_effect} "
        f"Overall outlook: {severity.upper()}."
    ).strip()

    # Hindi synthesis
    md_data_hi = md_data.get("general_hi", "") if md_strength == "neutral" else (
        md_data.get("when_strong_hi", "") if md_strength == "strong" else md_data.get("when_weak_hi", "")
    )
    ad_effect_hi = entry.get("effect_hi", "")
    md_qualifier_hi = (
        f"बलवान {mahadasha_lord} ({md_sign}, भाव {md_house})"
        if md_strength == "strong" else
        f"दुर्बल {mahadasha_lord} ({md_sign}, भाव {md_house})"
        if md_strength == "weak" else
        f"{mahadasha_lord} ({md_sign}, भाव {md_house})"
    )
    bk_qualifier_hi = (
        f"बलवान {bhukti_lord} ({bk_sign}, भाव {bk_house})"
        if bk_strength == "strong" else
        f"दुर्बल {bhukti_lord} ({bk_sign}, भाव {bk_house})"
        if bk_strength == "weak" else
        f"{bhukti_lord} ({bk_sign}, भाव {bk_house})"
    )
    severity_hi = {"favorable": "शुभ", "challenging": "कठिन", "mixed": "मिश्रित"}.get(severity, severity)
    combined_hi = (
        f"{md_qualifier_hi} की महादशा में: {md_data_hi} "
        f"इसके भीतर {bk_qualifier_hi} की अंतर्दशा: {ad_effect_hi} "
        f"समग्र दृष्टिकोण: {severity_hi}।"
    ).strip()

    return {
        "mahadasha": mahadasha_lord,
        "bhukti": bhukti_lord,
        "effect_en": entry.get("effect_en", ""),
        "effect_hi": entry.get("effect_hi", ""),
        "sloka_ref": entry.get("sloka_ref", ""),
        "severity": severity,
        "severity_factors": factors,
        "base_nature": base,
        "combined_synthesis_en": combined_en,
        "combined_synthesis_hi": combined_hi,
        "mahadasha_quality": md_quality,
        "bhukti_quality": bk_quality,
    }


# ============================================================
# FEATURE #29 — Sookshma (4th) + Prana (5th) Dasha Subdivisions
# Phaladeepika Adhyaya 21
# ============================================================

# Classical planetary themes for Prana-level interpretation
_PRANA_THEMES_EN = {
    "Sun":     "authority, vitality, and government matters",
    "Moon":    "emotional sensitivity, mind, and nurturing themes",
    "Mars":    "energy, courage, and conflict resolution",
    "Rahu":    "ambition, foreign matters, and sudden shifts",
    "Jupiter": "wisdom, expansion, and spiritual growth",
    "Saturn":  "discipline, delays, and karmic lessons",
    "Mercury": "communication, intellect, and commerce",
    "Ketu":    "detachment, spiritual insight, and past karma",
    "Venus":   "creative and relational themes",
}

_PRANA_THEMES_HI = {
    "Sun":     "सत्ता, जीवन-शक्ति एवं राजकीय विषय",
    "Moon":    "भावनात्मक संवेदनशीलता, मन एवं पोषण",
    "Mars":    "ऊर्जा, साहस एवं संघर्ष-समाधान",
    "Rahu":    "महत्त्वाकांक्षा, विदेश-संबंध एवं आकस्मिक परिवर्तन",
    "Jupiter": "ज्ञान, विस्तार एवं आध्यात्मिक विकास",
    "Saturn":  "अनुशासन, विलम्ब एवं कार्मिक पाठ",
    "Mercury": "संचार, बुद्धि एवं वाणिज्य",
    "Ketu":    "विरक्ति, आध्यात्मिक अंतर्दृष्टि एवं पूर्व-कर्म",
    "Venus":   "सृजनात्मक व संबंध-सम्बन्धी विषय",
}


def _build_sookshma_periods(
    pratyantar_planet: str,
    pratyantar_duration_days: float,
    pratyantar_start: datetime,
    now: datetime,
) -> list:
    """
    Build Sookshma Dasha periods (4th level) within a Pratyantar Dasha.

    Each Sookshma duration = (pratyantar_duration_days × planet_years) / 120.

    Args:
        pratyantar_planet: The Pratyantar lord (sequence starts from this planet).
        pratyantar_duration_days: Total duration of the Pratyantar in days.
        pratyantar_start: Start datetime of the Pratyantar.
        now: Reference datetime for is_current flag.

    Returns:
        List of 9 dicts: {planet, duration_days, start, end, is_current}
    """
    sookshma_seq = _get_dasha_sequence(pratyantar_planet)
    sookshma_periods = []
    sk_start = pratyantar_start

    for sk_planet in sookshma_seq:
        sk_years = DASHA_YEARS[sk_planet]
        # Sookshma duration = (pratyantar_duration_days × planet_years) / 120
        sk_duration_days = (pratyantar_duration_days * sk_years) / VIMSHOTTARI_TOTAL
        sk_end = sk_start + timedelta(days=sk_duration_days)

        is_current = (sk_start <= now <= sk_end)

        sookshma_periods.append({
            "planet": sk_planet,
            "duration_days": sk_duration_days,
            "start": sk_start.strftime("%Y-%m-%d"),
            "end": sk_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        sk_start = sk_end

    return sookshma_periods


def _build_prana_periods(
    sookshma_planet: str,
    sookshma_duration_days: float,
    sookshma_start: datetime,
    now: datetime,
) -> list:
    """
    Build Prana Dasha periods (5th level) within a Sookshma Dasha.

    Each Prana duration = (sookshma_duration_days × planet_years) / 120.
    Prana periods are very short (hours to a few days).

    Args:
        sookshma_planet: The Sookshma lord (sequence starts from this planet).
        sookshma_duration_days: Total duration of the Sookshma in days.
        sookshma_start: Start datetime of the Sookshma.
        now: Reference datetime for is_current flag.

    Returns:
        List of 9 dicts: {planet, duration_days, start, end, is_current}
    """
    prana_seq = _get_dasha_sequence(sookshma_planet)
    prana_periods = []
    pr_start = sookshma_start

    for pr_planet in prana_seq:
        pr_years = DASHA_YEARS[pr_planet]
        # Prana duration = (sookshma_duration_days × planet_years) / 120
        pr_duration_days = (sookshma_duration_days * pr_years) / VIMSHOTTARI_TOTAL
        pr_end = pr_start + timedelta(days=pr_duration_days)

        is_current = (pr_start <= now <= pr_end)

        prana_periods.append({
            "planet": pr_planet,
            "duration_days": pr_duration_days,
            "start": pr_start.strftime("%Y-%m-%d"),
            "end": pr_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        pr_start = pr_end

    return prana_periods


def calculate_sookshma_prana(
    birth_nakshatra: str,
    birth_date: str,
    moon_longitude: float = None,
    target_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calculate the current Sookshma (4th) and Prana (5th) Dasha subdivisions.

    Computes the full dasha chain up to the current/target date and returns
    only the CURRENT period at each of the 5 levels (MD → AD → PAD → SK → PR).

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini")
        birth_date: Birth date as "YYYY-MM-DD"
        moon_longitude: Moon's sidereal longitude in degrees (0-360). Optional.
        target_date: Optional "YYYY-MM-DD" — if given, find period at that date
                     instead of today.

    Returns:
        {
            current_mahadasha: {planet, start, end},
            current_antardasha: {planet, start, end},
            current_pratyantar: {planet, start, end},
            current_sookshma: {planet, start, end, duration_days},
            current_prana: {planet, start, end, duration_days},
            interpretation_en: str,
            interpretation_hi: str,
            sloka_ref: "Phaladeepika Adh. 21",
        }
    """
    if birth_nakshatra not in NAKSHATRA_LORD:
        return {
            "error": f"Unknown nakshatra: {birth_nakshatra}",
            "current_mahadasha": None,
            "current_antardasha": None,
            "current_pratyantar": None,
            "current_sookshma": None,
            "current_prana": None,
        }

    # Determine the reference datetime
    if target_date:
        try:
            now = datetime.strptime(target_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            now = datetime.now(timezone.utc)
    else:
        now = datetime.now(timezone.utc)

    starting_lord = NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date).replace(tzinfo=timezone.utc)

    balance = _calculate_dasha_balance(birth_nakshatra, moon_longitude)

    # ── Level 1: Mahadasha ──────────────────────────────────────
    mahadasha_record = None
    current_start = birth_dt
    full_seq = sequence * 4  # covers ~480 years

    for i, planet in enumerate(full_seq):
        full_years = DASHA_YEARS[planet]
        effective_years = full_years * balance if i == 0 else full_years
        end_dt = current_start + timedelta(days=effective_years * 365.25)

        if current_start <= now <= end_dt:
            mahadasha_record = {
                "planet": planet,
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "_start_dt": current_start,
                "_years": effective_years,
            }
            break
        current_start = end_dt

    if mahadasha_record is None:
        return {
            "error": "target_date outside computed mahadasha chain",
            "current_mahadasha": None,
            "current_antardasha": None,
            "current_pratyantar": None,
            "current_sookshma": None,
            "current_prana": None,
        }

    md_planet = mahadasha_record["planet"]
    md_start = mahadasha_record["_start_dt"]
    md_years = mahadasha_record["_years"]

    # ── Level 2: Antardasha ──────────────────────────────────────
    antardasha_record = None
    ad_seq = _get_dasha_sequence(md_planet)
    ad_start = md_start

    for ad_planet in ad_seq:
        ad_years = DASHA_YEARS[ad_planet]
        ad_duration_days = (md_years * ad_years / VIMSHOTTARI_TOTAL) * 365.25
        ad_end = ad_start + timedelta(days=ad_duration_days)

        if ad_start <= now <= ad_end:
            antardasha_record = {
                "planet": ad_planet,
                "start": ad_start.strftime("%Y-%m-%d"),
                "end": ad_end.strftime("%Y-%m-%d"),
                "_start_dt": ad_start,
                "_duration_days": ad_duration_days,
            }
            break
        ad_start = ad_end

    if antardasha_record is None:
        return {
            "error": "Could not find current antardasha",
            "current_mahadasha": {k: v for k, v in mahadasha_record.items() if not k.startswith("_")},
            "current_antardasha": None,
            "current_pratyantar": None,
            "current_sookshma": None,
            "current_prana": None,
        }

    ad_planet = antardasha_record["planet"]
    ad_start_dt = antardasha_record["_start_dt"]
    ad_duration_days = antardasha_record["_duration_days"]

    # ── Level 3: Pratyantar ──────────────────────────────────────
    pratyantar_record = None
    pt_seq = _get_dasha_sequence(ad_planet)
    pt_start = ad_start_dt

    for pt_planet in pt_seq:
        pt_years = DASHA_YEARS[pt_planet]
        pt_duration_days = (ad_duration_days * pt_years) / VIMSHOTTARI_TOTAL
        pt_end = pt_start + timedelta(days=pt_duration_days)

        if pt_start <= now <= pt_end:
            pratyantar_record = {
                "planet": pt_planet,
                "start": pt_start.strftime("%Y-%m-%d"),
                "end": pt_end.strftime("%Y-%m-%d"),
                "_start_dt": pt_start,
                "_duration_days": pt_duration_days,
            }
            break
        pt_start = pt_end

    if pratyantar_record is None:
        return {
            "error": "Could not find current pratyantar",
            "current_mahadasha": {k: v for k, v in mahadasha_record.items() if not k.startswith("_")},
            "current_antardasha": {k: v for k, v in antardasha_record.items() if not k.startswith("_")},
            "current_pratyantar": None,
            "current_sookshma": None,
            "current_prana": None,
        }

    pt_planet = pratyantar_record["planet"]
    pt_start_dt = pratyantar_record["_start_dt"]
    pt_duration_days = pratyantar_record["_duration_days"]

    # ── Level 4: Sookshma ────────────────────────────────────────
    sookshma_periods = _build_sookshma_periods(pt_planet, pt_duration_days, pt_start_dt, now)
    sookshma_record = None
    for sk in sookshma_periods:
        if sk["is_current"]:
            sookshma_record = sk
            break
    # Fallback to last sookshma if none matched (edge case at exact boundary)
    if sookshma_record is None and sookshma_periods:
        sookshma_record = sookshma_periods[-1]

    sk_planet = sookshma_record["planet"]
    sk_start_dt = datetime.strptime(sookshma_record["start"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    sk_duration_days = sookshma_record["duration_days"]

    # ── Level 5: Prana ───────────────────────────────────────────
    prana_periods = _build_prana_periods(sk_planet, sk_duration_days, sk_start_dt, now)
    prana_record = None
    for pr in prana_periods:
        if pr["is_current"]:
            prana_record = pr
            break
    # Fallback to last prana if none matched
    if prana_record is None and prana_periods:
        prana_record = prana_periods[-1]

    pr_planet = prana_record["planet"]

    # ── Build interpretation ─────────────────────────────────────
    theme_en = _PRANA_THEMES_EN.get(pr_planet, "subtle influences")
    theme_hi = _PRANA_THEMES_HI.get(pr_planet, "सूक्ष्म प्रभाव")

    interpretation_en = (
        f"Currently in {md_planet} MD > {ad_planet} AD > {pt_planet} PAD > "
        f"{sk_planet} SK > {pr_planet} Prana. "
        f"The Prana lord {pr_planet} brings {theme_en} "
        f"to this brief but potent window."
    )
    interpretation_hi = (
        f"वर्तमान में {md_planet} महादशा > {ad_planet} अंतर्दशा > "
        f"{pt_planet} प्रत्यंतर > {sk_planet} सूक्ष्म > {pr_planet} प्राण दशा। "
        f"प्राण-स्वामी {pr_planet} इस अल्पकालिक किन्तु प्रभावशाली काल में "
        f"{theme_hi} लाते हैं।"
    )

    return {
        "current_mahadasha": {
            "planet": md_planet,
            "start": mahadasha_record["start"],
            "end": mahadasha_record["end"],
        },
        "current_antardasha": {
            "planet": ad_planet,
            "start": antardasha_record["start"],
            "end": antardasha_record["end"],
        },
        "current_pratyantar": {
            "planet": pt_planet,
            "start": pratyantar_record["start"],
            "end": pratyantar_record["end"],
        },
        "current_sookshma": {
            "planet": sk_planet,
            "start": sookshma_record["start"],
            "end": sookshma_record["end"],
            "duration_days": sk_duration_days,
        },
        "current_prana": {
            "planet": pr_planet,
            "start": prana_record["start"],
            "end": prana_record["end"],
            "duration_days": prana_record["duration_days"],
        },
        "interpretation_en": interpretation_en,
        "interpretation_hi": interpretation_hi,
        "sloka_ref": "Phaladeepika Adh. 21",
    }


def get_current_dasha_phala(
    chart_data: dict, birth_date: str, as_of_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return classical effect narrative for the currently running
    Mahadasha + Antardasha of the native.

    Args:
        chart_data: Kundli chart dict with `planets` and Moon's `nakshatra`.
        birth_date: Birth date as 'YYYY-MM-DD'
        as_of_date: Optional 'YYYY-MM-DD' — defaults to today.

    Returns:
        {
            as_of,
            mahadasha: {planet, start, end, analysis(=analyze_mahadasha_phala)},
            antardasha: {planet, start, end, analysis(=analyze_antardasha_phala)},
        }
    """
    planets = (chart_data or {}).get("planets", {}) or {}
    moon = planets.get("Moon", {}) or {}
    moon_nakshatra = moon.get("nakshatra", "Ashwini")
    moon_longitude = moon.get("longitude", None)

    if moon_nakshatra not in NAKSHATRA_LORD:
        return {
            "as_of": as_of_date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "error": f"Unknown nakshatra: {moon_nakshatra}",
            "mahadasha": None,
            "antardasha": None,
        }

    starting_lord = NAKSHATRA_LORD[moon_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    try:
        birth_dt = _parse_date(birth_date)
    except (ValueError, TypeError):
        return {
            "as_of": as_of_date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "error": f"Invalid birth_date: {birth_date}",
            "mahadasha": None,
            "antardasha": None,
        }

    if as_of_date:
        try:
            now = _parse_date(as_of_date)
        except ValueError:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
    else:
        now = datetime.now(timezone.utc).replace(tzinfo=None)

    balance = _calculate_dasha_balance(moon_nakshatra, moon_longitude)

    # Walk mahadasha chain until we find the one containing `now`
    current_start = birth_dt
    mahadasha_record = None
    # Iterate up to 3 full cycles (enough for 360 years)
    full_seq = sequence * 3
    for i, planet in enumerate(full_seq):
        full_years = DASHA_YEARS[planet]
        effective_years = full_years * balance if i == 0 else full_years
        end_dt = current_start + timedelta(days=effective_years * 365.25)
        if current_start <= now <= end_dt:
            mahadasha_record = {
                "planet": planet,
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "years": round(effective_years, 4),
            }
            md_start = current_start
            md_years = effective_years
            break
        current_start = end_dt

    if mahadasha_record is None:
        return {
            "as_of": now.strftime("%Y-%m-%d"),
            "error": "as_of_date outside computed mahadasha chain",
            "mahadasha": None,
            "antardasha": None,
        }

    md_planet = mahadasha_record["planet"]
    md_analysis = analyze_mahadasha_phala(md_planet, chart_data or {})
    mahadasha_record["analysis"] = md_analysis

    # Find the antardasha within this mahadasha
    antardasha_record = None
    ad_seq = _get_dasha_sequence(md_planet)
    ad_start = md_start
    for ad_planet in ad_seq:
        ad_years = DASHA_YEARS[ad_planet]
        ad_duration_days = (md_years * ad_years / VIMSHOTTARI_TOTAL) * 365.25
        ad_end = ad_start + timedelta(days=ad_duration_days)
        if ad_start <= now <= ad_end:
            antardasha_record = {
                "planet": ad_planet,
                "start": ad_start.strftime("%Y-%m-%d"),
                "end": ad_end.strftime("%Y-%m-%d"),
                "analysis": analyze_antardasha_phala(md_planet, ad_planet, chart_data or {}),
            }
            break
        ad_start = ad_end

    return {
        "as_of": now.strftime("%Y-%m-%d"),
        "mahadasha": mahadasha_record,
        "antardasha": antardasha_record,
    }


# ─────────────────────────────────────────────────────────────
# Phaladeepika Adhyaya 19-21 — DASHA TIMING HALF RULE
# ─────────────────────────────────────────────────────────────

_HOUSE_AREAS_EN_DASHA = {
    1: "self/body", 2: "wealth/family", 3: "courage/siblings",
    4: "home/mother", 5: "children/intelligence", 6: "enemies/disease",
    7: "marriage/partnerships", 8: "longevity/transformation",
    9: "fortune/dharma", 10: "career/status",
    11: "gains/income", 12: "losses/liberation",
}
_HOUSE_AREAS_HI_DASHA = {
    1: "स्वयं/शरीर", 2: "धन/परिवार", 3: "पराक्रम/भाई-बहन",
    4: "गृह/माता", 5: "संतान/बुद्धि", 6: "शत्रु/रोग",
    7: "विवाह/साझेदारी", 8: "आयु/परिवर्तन",
    9: "भाग्य/धर्म", 10: "कर्म/प्रतिष्ठा",
    11: "लाभ/आय", 12: "व्यय/मोक्ष",
}

_EXALTATION_D = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
}
_DEBILITATION_D = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
}
_OWN_SIGNS_D = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
}
_DASHA_YEARS_HALF = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16,
    "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20,
}


def analyze_dasha_half_rule(planet: str, chart_data: dict) -> Dict[str, Any]:
    """
    Per Phaladeepika Adh. 19-21: determine when in a dasha period
    the planet's results manifest — first half, second half, or throughout.

    Args:
        planet: dasha lord (e.g., "Jupiter")
        chart_data: full kundli chart dict

    Returns:
        {
          planet, house, house_type (odd/even),
          strength, timing_phase (first_half/second_half/throughout),
          timing_en, timing_hi, dasha_years, sloka_ref
        }
    """
    planets = chart_data.get("planets", {}) if isinstance(chart_data, dict) else {}
    pdata = planets.get(planet, {})
    if not isinstance(pdata, dict):
        return {"planet": planet, "error": f"Planet {planet} not found in chart."}

    house = int(pdata.get("house", 0) or 0)
    sign = str(pdata.get("sign", ""))
    years = _DASHA_YEARS_HALF.get(planet, 0)

    # Odd or even house
    is_odd_house = house % 2 == 1 if house else None
    house_type = "odd" if is_odd_house else ("even" if house else "unknown")

    # Strength
    is_exalted = _EXALTATION_D.get(planet) == sign
    is_debilitated = _DEBILITATION_D.get(planet) == sign
    is_own = sign in _OWN_SIGNS_D.get(planet, set())
    if is_exalted or is_own:
        strength = "strong"
    elif is_debilitated:
        strength = "weak"
    else:
        strength = "neutral"

    # Timing phase per Adh. 19-21
    if strength == "strong" and is_odd_house:
        phase = "first_half"
        phase_en = "FIRST HALF (early in dasha)"
        phase_hi = "प्रथम अर्ध (दशा के प्रारंभ में)"
    elif strength == "strong" and not is_odd_house:
        phase = "first_half"
        phase_en = "FIRST HALF (strength brings early results even from even house)"
        phase_hi = "प्रथम अर्ध (बली ग्रह सम भाव से भी जल्दी फल देता है)"
    elif strength == "weak":
        phase = "second_half"
        phase_en = "SECOND HALF (weak planet delays results to latter portion)"
        phase_hi = "द्वितीय अर्ध (दुर्बल ग्रह दशा के उत्तरार्ध में फल देता है)"
    elif is_odd_house:
        phase = "first_half"
        phase_en = "FIRST HALF (odd house — results manifest early)"
        phase_hi = "प्रथम अर्ध (विषम भाव — फल शीघ्र प्राप्त होते हैं)"
    else:
        phase = "second_half"
        phase_en = "SECOND HALF (even house — results emerge in the latter half)"
        phase_hi = "द्वितीय अर्ध (सम भाव — फल उत्तरार्ध में प्रकट होते हैं)"

    house_area = _HOUSE_AREAS_EN_DASHA.get(house, f"house {house}")
    house_area_hi = _HOUSE_AREAS_HI_DASHA.get(house, f"भाव {house}")
    half_years = round(years / 2, 1)

    strong_note_en = "Exalted/strong planet gives results at the START of the dasha period." if strength == "strong" else ""
    weak_note_en = "Debilitated planet gives results late and partially unfulfilled." if strength == "weak" else ""
    timing_en = (
        f"{planet}'s {years}-year Mahadasha: results peak in the {phase_en}. "
        f"{planet} occupies house {house} ({house_area}) — a {'odd' if is_odd_house else 'even'} house, "
        f"and is {strength}. "
        f"Phaladeepika Adh. 19-21: planets in odd houses give results in the first ~{half_years} years; "
        f"planets in even houses or weak planets deliver results in the latter ~{half_years} years. "
        f"{strong_note_en}"
        f"{weak_note_en}"
    )
    timing_hi = (
        f"{planet} की {years} वर्षीय महादशा: फल {phase_hi} में प्राप्त होते हैं। "
        f"{planet} भाव {house} ({house_area_hi}) में — {'विषम' if is_odd_house else 'सम'} भाव, बल: {strength}। "
        f"फलदीपिका अ. 19-21: विषम भाव के ग्रह प्रथम {half_years} वर्षों में, "
        f"सम भाव या दुर्बल ग्रह उत्तरार्ध {half_years} वर्षों में फल देते हैं।"
    )

    return {
        "planet": planet,
        "house": house,
        "house_area_en": house_area,
        "house_area_hi": house_area_hi,
        "house_type": house_type,
        "strength": strength,
        "is_exalted": is_exalted,
        "is_debilitated": is_debilitated,
        "is_own_sign": is_own,
        "timing_phase": phase,
        "timing_phase_label_en": phase_en,
        "timing_phase_label_hi": phase_hi,
        "timing_en": timing_en,
        "timing_hi": timing_hi,
        "dasha_years": years,
        "sloka_ref": "Phaladeepika Adh. 19-21",
    }


def analyze_all_dasha_timing(chart_data: dict) -> Dict[str, Any]:
    """
    Analyze the first/second half timing rule for all 9 dasha lords.
    Returns a summary of when each planet's dasha delivers its results.
    """
    _PLANETS = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
    results = {}
    for planet in _PLANETS:
        results[planet] = analyze_dasha_half_rule(planet, chart_data)

    first_half = [p for p, r in results.items() if r.get("timing_phase") == "first_half"]
    second_half = [p for p, r in results.items() if r.get("timing_phase") == "second_half"]

    summary_en = (
        f"First-half dasha planets (results in early dasha period): {', '.join(first_half) or 'none'}. "
        f"Second-half planets (results in latter dasha period): {', '.join(second_half) or 'none'}. "
        f"Per Phaladeepika Adh. 19-21."
    )
    summary_hi = (
        f"प्रथम अर्ध दशा ग्रह: {', '.join(first_half) or 'कोई नहीं'}। "
        f"द्वितीय अर्ध दशा ग्रह: {', '.join(second_half) or 'कोई नहीं'}। "
        f"फलदीपिका अ. 19-21 के अनुसार।"
    )

    return {
        "planets": results,
        "first_half_planets": first_half,
        "second_half_planets": second_half,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 19-21",
    }
