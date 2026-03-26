"""
kp_engine.py -- Krishnamurti Paddhati (KP) Astrology Engine
=============================================================
Implements the KP system of astrology, which uses the Vimshottari Dasha
sub-lord system to determine significators for each house cusp.

Key concepts:
  - Star Lord: the Nakshatra lord of the cusp/planet position
  - Sub Lord: finer Vimshottari subdivision within the Nakshatra
  - Significators: planets that signify (influence) particular houses
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

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
) -> Dict[str, Any]:
    """
    Calculate KP cuspal chart with star lords, sub lords, and significators.

    Args:
        planet_longitudes: {planet_name: sidereal_longitude}
        house_cusps: list of 12 sidereal cusp longitudes (house 1-12)

    Returns:
        {
            "cusps": [
                {house, sign, degree, star_lord, sub_lord}
            ],
            "planets": {
                planet: {longitude, star_lord, sub_lord}
            },
            "significators": {
                planet: [list of house numbers the planet signifies]
            }
        }
    """
    from app.astro_engine import get_sign_from_longitude

    # Cusp analysis
    cusps_result: List[Dict[str, Any]] = []
    for i, cusp_lon in enumerate(house_cusps):
        cusp_lon = cusp_lon % 360.0
        sub_info = get_sub_lord(cusp_lon)
        sign = get_sign_from_longitude(cusp_lon)
        cusps_result.append({
            "house": i + 1,
            "sign": sign,
            "degree": round(cusp_lon, 4),
            "star_lord": sub_info["star_lord"],
            "sub_lord": sub_info["sub_lord"],
        })

    # Planet star/sub lords
    planets_result: Dict[str, Dict[str, Any]] = {}
    for pname, plon in planet_longitudes.items():
        plon = plon % 360.0
        sub_info = get_sub_lord(plon)
        planets_result[pname] = {
            "longitude": round(plon, 4),
            "star_lord": sub_info["star_lord"],
            "sub_lord": sub_info["sub_lord"],
        }

    # Significators: each planet signifies houses through 3 levels:
    # 1. Occupation: the house the planet sits in
    # 2. Ownership: houses whose cusp signs are ruled by the planet
    # 3. Star lord connection: houses whose cusp star lord is this planet
    significators: Dict[str, List[int]] = {}

    # Sign rulers for ownership determination
    _SIGN_RULERS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
    }

    for pname in planet_longitudes:
        houses_signified: set = set()

        # 1. Occupation: which house does this planet sit in?
        planet_lon = planet_longitudes[pname] % 360.0
        occupied_house = _find_house_for_planet(planet_lon, house_cusps)
        houses_signified.add(occupied_house)

        # 2. Ownership: which cusp signs does this planet rule?
        for cusp_info in cusps_result:
            if _SIGN_RULERS.get(cusp_info["sign"]) == pname:
                houses_signified.add(cusp_info["house"])

        # 3. Star lord connection: which cusps have this planet as star lord?
        for cusp_info in cusps_result:
            if cusp_info["star_lord"] == pname:
                houses_signified.add(cusp_info["house"])

        significators[pname] = sorted(houses_signified)

    return {
        "cusps": cusps_result,
        "planets": planets_result,
        "significators": significators,
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
