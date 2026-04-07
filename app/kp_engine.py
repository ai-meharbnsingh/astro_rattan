"""
kp_engine.py -- Krishnamurti Paddhati (KP) Astrology Engine
=============================================================
Implements the KP system of astrology, which uses the Vimshottari Dasha
sub-lord system to determine significators for each house cusp.

Key concepts:
  - Star Lord: the Nakshatra lord of the cusp/planet position
  - Sub Lord: finer Vimshottari subdivision within the Nakshatra
  - Sub-Sub Lord: even finer Vimshottari subdivision within the Sub
  - Significators: planets that signify (influence) particular houses
  - Ruling Planets: key planets at the moment of query/birth
  - House Significations: occupants + nakshatra-based signification chains
  - Planet Significator Strengths: 4-level strength classification
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from app.astro_engine import NAKSHATRAS, NAKSHATRA_SPAN, get_nakshatra_from_longitude

# ============================================================
# VIMSHOTTARI DASHA SEQUENCE & YEARS
# ============================================================
# Total cycle = 120 years
VIMSHOTTARI_SEQUENCE: List[Tuple[str, float]] = [
    ("Ketu",    7.0),
    ("Venus",   20.0),
    ("Sun",     6.0),
    ("Moon",    10.0),
    ("Mars",    7.0),
    ("Rahu",    18.0),
    ("Jupiter", 16.0),
    ("Saturn",  19.0),
    ("Mercury", 17.0),
]

VIMSHOTTARI_TOTAL_YEARS = 120.0

# Planet -> years mapping for quick lookup
_DASHA_YEARS: Dict[str, float] = {name: years for name, years in VIMSHOTTARI_SEQUENCE}

# ============================================================
# KP SUB-LORD TABLE
# ============================================================
# Each nakshatra (13deg 20min = 13.3333 deg) is divided into 9 sub-parts
# proportional to the Vimshottari dasha years of each planet.
# The sub-lord sequence starts from the nakshatra lord and follows
# the Vimshottari order.

def _build_kp_sub_lords() -> List[Dict[str, Any]]:
    """
    Build the complete KP sub-lord mapping for 0-360 degrees.
    Returns a sorted list of {start_degree, end_degree, star_lord, sub_lord}.
    """
    entries: List[Dict[str, Any]] = []

    # Build Vimshottari sequence as a list with cumulative lookup
    seq_names = [name for name, _ in VIMSHOTTARI_SEQUENCE]

    for nak in NAKSHATRAS:
        star_lord = nak["lord"]
        nak_start = nak["start_degree"]

        # Find the position of the star_lord in the Vimshottari sequence
        star_lord_idx = _find_vimshottari_index(star_lord)

        # Sub-divisions within this nakshatra, proportional to dasha years
        current_deg = nak_start
        for i in range(9):
            sub_planet_idx = (star_lord_idx + i) % 9
            sub_planet_name = seq_names[sub_planet_idx]
            sub_planet_years = _DASHA_YEARS[sub_planet_name]

            # Span in degrees = (sub_planet_years / 120) * nakshatra_span
            span = (sub_planet_years / VIMSHOTTARI_TOTAL_YEARS) * NAKSHATRA_SPAN
            end_deg = current_deg + span

            entries.append({
                "start_degree": round(current_deg, 6),
                "end_degree": round(end_deg, 6),
                "star_lord": star_lord,
                "sub_lord": sub_planet_name,
            })
            current_deg = end_deg

    return entries


def _find_vimshottari_index(planet_name: str) -> int:
    """Find the index of a planet in the Vimshottari sequence."""
    for i, (name, _) in enumerate(VIMSHOTTARI_SEQUENCE):
        if name == planet_name:
            return i
    raise ValueError(f"Planet {planet_name} not in Vimshottari sequence")


# Pre-built table (computed once at module load)
KP_SUB_LORDS: List[Dict[str, Any]] = _build_kp_sub_lords()


def get_sub_lord(longitude: float) -> Dict[str, str]:
    """
    Get the star lord and sub lord for a given sidereal longitude.

    Args:
        longitude: sidereal longitude in degrees (0-360)

    Returns:
        {star_lord, sub_lord}
    """
    longitude = longitude % 360.0

    for entry in KP_SUB_LORDS:
        if entry["start_degree"] <= longitude < entry["end_degree"]:
            return {
                "star_lord": entry["star_lord"],
                "sub_lord": entry["sub_lord"],
            }

    # Edge case: exactly 360.0 or rounding
    last = KP_SUB_LORDS[-1]
    return {"star_lord": last["star_lord"], "sub_lord": last["sub_lord"]}


def get_sub_sub_lord(longitude: float) -> str:
    """
    Compute the sub-sub lord for a given sidereal longitude.

    The sub-sub lord is computed by further dividing each sub-lord's span
    in the same Vimshottari proportion, starting from the sub-lord itself.

    Args:
        longitude: sidereal longitude in degrees (0-360)

    Returns:
        The sub-sub lord planet name.
    """
    longitude = longitude % 360.0
    seq_names = [name for name, _ in VIMSHOTTARI_SEQUENCE]

    for entry in KP_SUB_LORDS:
        if entry["start_degree"] <= longitude < entry["end_degree"]:
            sub_lord = entry["sub_lord"]
            sub_start = entry["start_degree"]
            sub_span = entry["end_degree"] - entry["start_degree"]

            # Find position of sub_lord in Vimshottari sequence
            sub_lord_idx = _find_vimshottari_index(sub_lord)

            # Divide the sub span into 9 sub-sub parts (same Vimshottari proportions)
            current_deg = sub_start
            for i in range(9):
                ss_idx = (sub_lord_idx + i) % 9
                ss_name = seq_names[ss_idx]
                ss_years = _DASHA_YEARS[ss_name]
                ss_span = (ss_years / VIMSHOTTARI_TOTAL_YEARS) * sub_span
                ss_end = current_deg + ss_span

                if current_deg <= longitude < ss_end:
                    return ss_name
                current_deg = ss_end

            # Fallback: last sub-sub in this sub
            last_ss_idx = (sub_lord_idx + 8) % 9
            return seq_names[last_ss_idx]

    # Edge case
    last = KP_SUB_LORDS[-1]
    sub_lord_idx = _find_vimshottari_index(last["sub_lord"])
    last_ss_idx = (sub_lord_idx + 8) % 9
    return seq_names[last_ss_idx]


# ============================================================
# NAKSHATRA & SIGN UTILITIES
# ============================================================

# Sign lord mapping (rashi lord)
SIGN_LORD_MAP: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Day of week -> ruling planet (standard Vedic mapping)
_DAY_LORDS = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
# Python weekday(): Monday=0 ... Sunday=6


def _longitude_to_dms_in_sign(longitude: float) -> str:
    """
    Convert a sidereal longitude to degree:min:sec within its zodiac sign.
    E.g. 85.547 -> "25:32:48" (25 deg 32 min 48 sec within Gemini).
    """
    deg_in_sign = longitude % 30.0
    degrees = int(deg_in_sign)
    remainder = (deg_in_sign - degrees) * 60.0
    minutes = int(remainder)
    seconds = int((remainder - minutes) * 60.0)
    return f"{degrees}:{minutes:02d}:{seconds:02d}"


# ============================================================
# HOUSE SIGNIFICATOR DETERMINATION
# ============================================================

def _get_houses_owned(planet: str) -> List[int]:
    """
    Return the house numbers (1-12) whose signs are owned by the given planet.
    This is a generic mapping; actual ownership depends on the ascendant.
    """
    # Standard rulership: sign index -> ruling planet
    _SIGN_RULERS = {
        0: "Mars",      # Aries
        1: "Venus",     # Taurus
        2: "Mercury",   # Gemini
        3: "Moon",      # Cancer
        4: "Sun",       # Leo
        5: "Mercury",   # Virgo
        6: "Venus",     # Libra
        7: "Mars",      # Scorpio (traditional)
        8: "Jupiter",   # Sagittarius
        9: "Saturn",    # Capricorn
        10: "Saturn",   # Aquarius
        11: "Jupiter",  # Pisces
    }
    # Invert: planet -> list of sign indices
    owned_signs: List[int] = []
    for sign_idx, ruler in _SIGN_RULERS.items():
        if ruler == planet:
            owned_signs.append(sign_idx)
    return owned_signs


# ============================================================
# PUBLIC: calculate_kp_cuspal
# ============================================================

def calculate_kp_cuspal(
    planet_longitudes: Dict[str, float],
    house_cusps: List[float],
    chart_data: Optional[Dict[str, Any]] = None,
    birth_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calculate KP cuspal chart with full KP analysis.

    Enhanced output includes: star lords, sub lords, sub-sub lords, nakshatras,
    padas, retrograde status, DMS degrees, house significations, planet
    significator strengths, and ruling planets.

    Args:
        planet_longitudes: {planet_name: sidereal_longitude}
        house_cusps: list of 12 sidereal cusp longitudes (house 1-12)
        chart_data: optional full chart dict from astro_engine (provides
                    retrograde status and ascendant info)
        birth_date: optional ISO date "YYYY-MM-DD" (used for day_lord in
                    ruling planets)

    Returns:
        {
            "cusps": [{house, sign, sign_lord, degree, degree_dms,
                       star_lord, sub_lord, sub_sub_lord,
                       nakshatra, pada}],
            "planets": {planet: {longitude, sign, sign_lord,
                                  star_lord, sub_lord, sub_sub_lord,
                                  nakshatra, pada, degree_dms,
                                  retrograde}},
            "significators": {planet: [houses]},
            "house_significations": {house: {occupants, ...}},
            "planet_significator_strengths": {planet: {very_strong, ...}},
            "ruling_planets": {day_lord, lagna_lord, ...},
        }
    """
    from app.astro_engine import get_sign_from_longitude

    # ------------------------------------------------------------------
    # Chart data extraction helpers
    # ------------------------------------------------------------------
    _chart_planets = (chart_data or {}).get("planets", {})
    _chart_ascendant = (chart_data or {}).get("ascendant", {})

    def _is_retrograde(planet_name: str) -> bool:
        """Determine retrograde status from chart_data if available."""
        pinfo = _chart_planets.get(planet_name, {})
        if "retrograde" in pinfo:
            return bool(pinfo["retrograde"])
        # Rahu and Ketu are always retrograde by convention
        if planet_name in ("Rahu", "Ketu"):
            return True
        return False

    # ------------------------------------------------------------------
    # Cusp analysis (enhanced)
    # ------------------------------------------------------------------
    cusps_result: List[Dict[str, Any]] = []
    for i, cusp_lon in enumerate(house_cusps):
        cusp_lon = cusp_lon % 360.0
        sub_info = get_sub_lord(cusp_lon)
        sub_sub = get_sub_sub_lord(cusp_lon)
        sign = get_sign_from_longitude(cusp_lon)
        nak_info = get_nakshatra_from_longitude(cusp_lon)
        cusps_result.append({
            "house": i + 1,
            "sign": sign,
            "sign_lord": SIGN_LORD_MAP.get(sign, ""),
            "degree": round(cusp_lon, 4),
            "degree_dms": _longitude_to_dms_in_sign(cusp_lon),
            "star_lord": sub_info["star_lord"],
            "sub_lord": sub_info["sub_lord"],
            "sub_sub_lord": sub_sub,
            "nakshatra": nak_info["name"],
            "pada": nak_info["pada"],
        })

    # ------------------------------------------------------------------
    # Planet analysis (enhanced)
    # ------------------------------------------------------------------
    planets_result: Dict[str, Dict[str, Any]] = {}
    # Also track which house each planet occupies (needed for significations)
    planet_house_map: Dict[str, int] = {}

    for pname, plon in planet_longitudes.items():
        plon = plon % 360.0
        sub_info = get_sub_lord(plon)
        sub_sub = get_sub_sub_lord(plon)
        sign = get_sign_from_longitude(plon)
        nak_info = get_nakshatra_from_longitude(plon)
        occupied_house = _find_house_for_planet(plon, house_cusps)
        planet_house_map[pname] = occupied_house

        planets_result[pname] = {
            "longitude": round(plon, 4),
            "sign": sign,
            "sign_lord": SIGN_LORD_MAP.get(sign, ""),
            "star_lord": sub_info["star_lord"],
            "sub_lord": sub_info["sub_lord"],
            "sub_sub_lord": sub_sub,
            "nakshatra": nak_info["name"],
            "pada": nak_info["pada"],
            "degree_dms": _longitude_to_dms_in_sign(plon),
            "retrograde": _is_retrograde(pname),
        }

    # ------------------------------------------------------------------
    # Build lookup: nakshatra_lord -> list of planets in that lord's nak
    # (planet X's nak lord is Y  =>  nak_lord_to_planets[Y] includes X)
    # ------------------------------------------------------------------
    nak_lord_to_planets: Dict[str, List[str]] = {}
    for pname, pdata in planets_result.items():
        nl = pdata["star_lord"]  # star_lord == nakshatra lord
        nak_lord_to_planets.setdefault(nl, []).append(pname)

    # ------------------------------------------------------------------
    # Significators (existing logic preserved)
    # ------------------------------------------------------------------
    significators: Dict[str, List[int]] = {}

    for pname in planet_longitudes:
        houses_signified: set = set()

        # 1. Occupation: which house does this planet sit in?
        houses_signified.add(planet_house_map[pname])

        # 2. Ownership: which cusp signs does this planet rule?
        for cusp_info in cusps_result:
            if SIGN_LORD_MAP.get(cusp_info["sign"]) == pname:
                houses_signified.add(cusp_info["house"])

        # 3. Star lord connection: which cusps have this planet as star lord?
        for cusp_info in cusps_result:
            if cusp_info["star_lord"] == pname:
                houses_signified.add(cusp_info["house"])

        significators[pname] = sorted(houses_signified)

    # ------------------------------------------------------------------
    # House Significations (NEW)
    # ------------------------------------------------------------------
    # For each house:
    #   occupants = planets physically in that house
    #   planets_in_nak_of_occupants = planets whose nak lord is an occupant
    #   cusp_sign_lord = sign lord of the cusp
    #   planets_in_nak_of_cusp_sign_lord = planets whose nak lord is the cusp sign lord
    house_significations: Dict[int, Dict[str, Any]] = {}

    # Build house -> occupants mapping
    house_occupants: Dict[int, List[str]] = {}
    for pname, house_num in planet_house_map.items():
        house_occupants.setdefault(house_num, []).append(pname)

    for h in range(1, 13):
        occupants = house_occupants.get(h, [])
        cusp_info = cusps_result[h - 1]
        cusp_sign_lord = cusp_info["sign_lord"]

        # Planets in nakshatra of occupants:
        # any planet whose nak lord is one of this house's occupants
        planets_in_nak_of_occ: List[str] = []
        for occ in occupants:
            for p in nak_lord_to_planets.get(occ, []):
                if p not in planets_in_nak_of_occ:
                    planets_in_nak_of_occ.append(p)

        # Planets in nakshatra of cusp sign lord:
        # any planet whose nak lord equals the cusp sign lord
        planets_in_nak_of_csl: List[str] = []
        for p in nak_lord_to_planets.get(cusp_sign_lord, []):
            if p not in planets_in_nak_of_csl:
                planets_in_nak_of_csl.append(p)

        house_significations[h] = {
            "occupants": occupants,
            "planets_in_nak_of_occupants": planets_in_nak_of_occ,
            "cusp_sign_lord": cusp_sign_lord,
            "planets_in_nak_of_cusp_sign_lord": planets_in_nak_of_csl,
        }

    # ------------------------------------------------------------------
    # Planet Significator Strengths (NEW)
    # ------------------------------------------------------------------
    # 4 levels per KP:
    #   Level 1 (very_strong): planet is occupant of house
    #   Level 2 (strong):      planet is in nakshatra of an occupant of house
    #   Level 3 (normal):      planet is in nakshatra of cusp sign lord
    #   Level 4 (weak):        planet IS the cusp sign lord (but not occupant)
    planet_significator_strengths: Dict[str, Dict[str, List[int]]] = {}

    for pname in planet_longitudes:
        very_strong: List[int] = []
        strong: List[int] = []
        normal: List[int] = []
        weak: List[int] = []

        pnak_lord = planets_result[pname]["star_lord"]

        for h in range(1, 13):
            hs = house_significations[h]

            # Level 1: planet is occupant of this house
            if pname in hs["occupants"]:
                very_strong.append(h)

            # Level 2: planet is in nak of an occupant of this house
            # (planet's nak lord is one of the occupants)
            if pnak_lord in hs["occupants"] and h not in very_strong:
                strong.append(h)

            # Level 3: planet is in nak of cusp sign lord of this house
            if pnak_lord == hs["cusp_sign_lord"]:
                normal.append(h)

            # Level 4: planet IS the cusp sign lord (ownership) but not occupant
            if pname == hs["cusp_sign_lord"] and pname not in hs["occupants"]:
                weak.append(h)

        planet_significator_strengths[pname] = {
            "very_strong": very_strong,
            "strong": strong,
            "normal": normal,
            "weak": weak,
        }

    # ------------------------------------------------------------------
    # Ruling Planets (NEW)
    # ------------------------------------------------------------------
    ruling_planets: Dict[str, str] = {}

    # Day lord
    if birth_date:
        try:
            from datetime import datetime as _dt
            bd = _dt.strptime(birth_date, "%Y-%m-%d")
            ruling_planets["day_lord"] = _DAY_LORDS[bd.weekday()]
        except (ValueError, IndexError):
            ruling_planets["day_lord"] = ""
    else:
        ruling_planets["day_lord"] = ""

    # Ascendant-based ruling planets
    asc_lon = _chart_ascendant.get("longitude", house_cusps[0] % 360.0)
    asc_lon = asc_lon % 360.0
    asc_sign = get_sign_from_longitude(asc_lon)
    asc_nak = get_nakshatra_from_longitude(asc_lon)
    asc_sub = get_sub_lord(asc_lon)

    ruling_planets["lagna_lord"] = SIGN_LORD_MAP.get(asc_sign, "")
    ruling_planets["lagna_nak_lord"] = asc_nak["lord"]
    ruling_planets["lagna_sub_lord"] = asc_sub["sub_lord"]

    # Moon-based ruling planets
    moon_lon = planet_longitudes.get("Moon", 0.0) % 360.0
    moon_sign = get_sign_from_longitude(moon_lon)
    moon_nak = get_nakshatra_from_longitude(moon_lon)
    moon_sub = get_sub_lord(moon_lon)

    ruling_planets["moon_rashi_lord"] = SIGN_LORD_MAP.get(moon_sign, "")
    ruling_planets["moon_nak_lord"] = moon_nak["lord"]
    ruling_planets["moon_sub_lord"] = moon_sub["sub_lord"]

    # ------------------------------------------------------------------
    # Final result
    # ------------------------------------------------------------------
    return {
        "cusps": cusps_result,
        "planets": planets_result,
        "significators": significators,
        "house_significations": house_significations,
        "planet_significator_strengths": planet_significator_strengths,
        "ruling_planets": ruling_planets,
    }


def _find_house_for_planet(planet_lon: float, house_cusps: List[float]) -> int:
    """Determine which house (1-12) a planet occupies given cusp degrees."""
    planet_lon = planet_lon % 360.0
    for i in range(12):
        cusp_start = house_cusps[i] % 360.0
        cusp_end = house_cusps[(i + 1) % 12] % 360.0

        if cusp_end < cusp_start:
            # Wraps around 360
            if planet_lon >= cusp_start or planet_lon < cusp_end:
                return i + 1
        else:
            if cusp_start <= planet_lon < cusp_end:
                return i + 1

    return 1  # Default
