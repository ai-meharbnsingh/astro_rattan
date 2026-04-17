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
    now = datetime.utcnow()

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
    now = datetime.utcnow()

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

    if strength == "strong":
        effect_en = entry.get("when_strong_en", entry.get("general_en", ""))
        effect_hi = entry.get("when_strong_hi", entry.get("general_hi", ""))
    elif strength == "weak":
        effect_en = entry.get("when_weak_en", entry.get("general_en", ""))
        effect_hi = entry.get("when_weak_hi", entry.get("general_hi", ""))
    else:
        effect_en = entry.get("general_en", "")
        effect_hi = entry.get("general_hi", "")

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

    return {
        "mahadasha": mahadasha_lord,
        "bhukti": bhukti_lord,
        "effect_en": entry.get("effect_en", ""),
        "effect_hi": entry.get("effect_hi", ""),
        "sloka_ref": entry.get("sloka_ref", ""),
        "severity": severity,
        "severity_factors": factors,
        "base_nature": base,
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
            "as_of": as_of_date or datetime.utcnow().strftime("%Y-%m-%d"),
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
            "as_of": as_of_date or datetime.utcnow().strftime("%Y-%m-%d"),
            "error": f"Invalid birth_date: {birth_date}",
            "mahadasha": None,
            "antardasha": None,
        }

    if as_of_date:
        try:
            now = _parse_date(as_of_date)
        except ValueError:
            now = datetime.utcnow()
    else:
        now = datetime.utcnow()

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
