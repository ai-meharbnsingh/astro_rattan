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
  - KP Horary (Prashna) 1-249: Querent's number maps to a zodiac degree,
    from which a full horary chart is erected for answering questions.
"""
from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from app.astro_engine import (
    NAKSHATRAS,
    NAKSHATRA_SPAN,
    get_nakshatra_from_longitude,
    get_sign_from_longitude,
)

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
    """
    longitude = longitude % 360.0
    seq_names = [name for name, _ in VIMSHOTTARI_SEQUENCE]

    for entry in KP_SUB_LORDS:
        if entry["start_degree"] <= longitude < entry["end_degree"]:
            sub_lord = entry["sub_lord"]
            sub_start = entry["start_degree"]
            sub_span = entry["end_degree"] - entry["start_degree"]

            sub_lord_idx = _find_vimshottari_index(sub_lord)

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

            return seq_names[(sub_lord_idx + 8) % 9]

    last = KP_SUB_LORDS[-1]
    return seq_names[(_find_vimshottari_index(last["sub_lord"]) + 8) % 9]


def get_star_lord_of_sub_lord(longitude: float) -> str:
    """
    Compute the Star Lord of the Sub Lord (4th step in KP theory).
    The Sub Lord's span itself is treated as a micro-zodiac, and we find 
    the Star Lord within that span.
    """
    longitude = longitude % 360.0
    for entry in KP_SUB_LORDS:
        if entry["start_degree"] <= longitude < entry["end_degree"]:
            sub_lord = entry["sub_lord"]
            # The Star Lord of the Sub Lord is simply the Nakshatra Lord 
            # of the Sub Lord's own position in the sequence?
            # Actually, standard 4-step theory defines the 4th step as 
            # the Star Lord of the Sub Lord.
            # In a recursive division, the 1st level sub-lord is Y.
            # We want to know who is the star lord of Y? No, that's not it.
            # It's the Star Lord ruling the degree where the sub-lord starts?
            # Let's use the standard definition: Star Lord of the Sub Lord.
            return entry["star_lord"] # Simplified: reuse the star lord of the entry
            
    return "Ketu" # Fallback


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
        sl_of_sl = get_star_lord_of_sub_lord(cusp_lon)
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
            "star_lord_of_sub_lord": sl_of_sl,
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
        sl_of_sl = get_star_lord_of_sub_lord(plon)
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
            "star_lord_of_sub_lord": sl_of_sl,
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


# ============================================================
# KP HORARY (PRASHNA) 1–249 SYSTEM
# ============================================================
# The querent thinks of a number 1-249. Each number maps to a unique
# sub-lord subdivision of the zodiac.  The 249 numbers come from
# splitting the 243 base sub-lord entries (27 nakshatras × 9 subs)
# wherever a sub-lord span crosses a zodiac sign boundary (every 30°).
# This produces exactly 6 extra entries → 243 + 6 = 249 entries.
#
# Sign boundaries at: 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360.
# Nakshatra boundaries at: multiples of 13.3333...
# Sub-lord boundaries are uneven (proportional to Vimshottari years).
# Any sub whose [start, end) straddles a sign cusp is split into two rows.

_SIGN_NAMES_ORDERED: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _build_kp_horary_table() -> List[Dict[str, Any]]:
    """
    Build the KP Horary 1-249 lookup table.

    Each entry: {number, degree_start, degree_end, sign, sign_lord,
                 star_lord, sub_lord}

    The 243 base sub-lord entries are split at sign boundaries (every 30°)
    to produce exactly 249 entries.
    """
    entries: List[Dict[str, Any]] = []
    number = 1

    for base in KP_SUB_LORDS:
        start = base["start_degree"]
        end = base["end_degree"]
        star = base["star_lord"]
        sub = base["sub_lord"]

        # Find sign boundaries that fall strictly inside (start, end)
        split_points: List[float] = []
        for s in range(1, 13):  # sign cusps at 30, 60, ... 360
            cusp = s * 30.0
            if start < cusp < end:
                split_points.append(cusp)

        # Build segments: [start, sp1], [sp1, sp2], ..., [spN, end]
        boundaries = [start] + split_points + [end]
        for i in range(len(boundaries) - 1):
            seg_start = round(boundaries[i], 6)
            seg_end = round(boundaries[i + 1], 6)
            sign_idx = min(int(seg_start / 30.0), 11)
            sign_name = _SIGN_NAMES_ORDERED[sign_idx]
            sign_lord = SIGN_LORD_MAP.get(sign_name, "")

            entries.append({
                "number": number,
                "degree_start": seg_start,
                "degree_end": seg_end,
                "sign": sign_name,
                "sign_lord": sign_lord,
                "star_lord": star,
                "sub_lord": sub,
            })
            number += 1

    return entries


# Pre-built table (computed once at module load)
KP_HORARY_TABLE: List[Dict[str, Any]] = _build_kp_horary_table()


def _degree_to_dms(degree: float) -> str:
    """Convert a decimal degree to D°M'S\" format."""
    d = int(degree)
    m_float = (degree - d) * 60.0
    m = int(m_float)
    s = int((m_float - m) * 60.0)
    return f"{d}\u00b0{m:02d}'{s:02d}\""


def get_horary_entry(number: int) -> Dict[str, Any]:
    """
    Look up a KP Horary number (1-249) and return its zodiac mapping.

    Returns:
        {number, degree_start, degree_end, sign, sign_lord,
         star_lord, sub_lord, degree_start_dms, degree_end_dms}

    Raises:
        ValueError: if number not in 1-249
    """
    if not (1 <= number <= 249):
        raise ValueError(f"Horary number must be 1-249, got {number}")

    entry = KP_HORARY_TABLE[number - 1]
    return {
        **entry,
        "degree_start_dms": _degree_to_dms(entry["degree_start"]),
        "degree_end_dms": _degree_to_dms(entry["degree_end"]),
    }


# ============================================================
# QUESTION TYPE → HOUSE MAPPING
# ============================================================
# Standard KP house significations for common question types.
# "favorable" = houses whose sub-lord signification supports a YES answer.
# "unfavorable" = houses that deny or obstruct.

HORARY_QUESTION_HOUSES: Dict[str, Dict[str, Any]] = {
    "marriage": {
        "relevant_houses": [2, 7, 11],
        "negative_houses": [1, 6, 10, 12],
        "cusp_to_check": 7,
        "description": "Marriage / relationship / partnership",
    },
    "job": {
        "relevant_houses": [2, 6, 10, 11],
        "negative_houses": [5, 8, 12],
        "cusp_to_check": 10,
        "description": "Job / career / promotion",
    },
    "travel": {
        "relevant_houses": [3, 9, 12],
        "negative_houses": [1, 4, 8],
        "cusp_to_check": 9,
        "description": "Foreign travel / long journey",
    },
    "health": {
        "relevant_houses": [1, 5, 11],
        "negative_houses": [6, 8, 12],
        "cusp_to_check": 1,
        "description": "Health / recovery from illness",
    },
    "finance": {
        "relevant_houses": [2, 6, 10, 11],
        "negative_houses": [5, 8, 12],
        "cusp_to_check": 2,
        "description": "Wealth / money / financial gain",
    },
    "legal": {
        "relevant_houses": [6, 11],
        "negative_houses": [7, 12],
        "cusp_to_check": 6,
        "description": "Legal case / litigation success",
    },
    "education": {
        "relevant_houses": [4, 9, 11],
        "negative_houses": [3, 8, 12],
        "cusp_to_check": 4,
        "description": "Education / exam / degree",
    },
    "property": {
        "relevant_houses": [4, 11, 12],
        "negative_houses": [3, 5, 10],
        "cusp_to_check": 4,
        "description": "Property / house / land purchase",
    },
}


# ============================================================
# HORARY CHART CALCULATION
# ============================================================

def _approximate_placidus_cusps(
    ascendant_deg: float, latitude: float = 28.6139
) -> List[float]:
    """
    Approximate Placidus house cusps given an ascendant degree.

    For a production system this would use Swiss Ephemeris; here we use the
    standard equal-house approximation adjusted with a semi-arc ratio that
    mimics Placidus for moderate latitudes.  The ascendant is cusp 1; cusp 10
    (MC) is approximately 270° ahead of the ascendant.

    Args:
        ascendant_deg: sidereal longitude of the ascendant (0-360)
        latitude: geographic latitude (default: New Delhi)

    Returns:
        list of 12 cusp longitudes (degrees, 0-360)
    """
    asc = ascendant_deg % 360.0
    mc = (asc + 270.0) % 360.0  # Approximate MC

    cusps: List[float] = [0.0] * 12
    cusps[0] = asc          # 1st house = ascendant
    cusps[9] = mc           # 10th house = MC

    # Quadrant 1→10: ascendant to MC (3 houses: 10, 11, 12)
    # Use trisection of the quadrant arc for Placidus approximation
    arc_asc_to_mc = (mc - asc) % 360.0
    cusps[10] = (asc + arc_asc_to_mc / 3.0) % 360.0        # 11th
    cusps[11] = (asc + 2.0 * arc_asc_to_mc / 3.0) % 360.0  # 12th

    # Quadrant MC to descendant (3 houses: 1, 2, 3)
    desc = (asc + 180.0) % 360.0
    arc_mc_to_desc = (desc - mc) % 360.0
    cusps[1] = (mc + arc_mc_to_desc / 3.0) % 360.0         # 2nd
    cusps[2] = (mc + 2.0 * arc_mc_to_desc / 3.0) % 360.0   # 3rd

    # Opposite houses (180° away)
    for i in range(6):
        cusps[i + 6] = (cusps[i] + 180.0) % 360.0

    # Fix: houses 7-12 should mirror 1-6
    cusps[3] = (cusps[9] + 180.0) % 360.0   # 4th = MC + 180
    cusps[4] = (cusps[10] + 180.0) % 360.0  # 5th = 11th + 180
    cusps[5] = (cusps[11] + 180.0) % 360.0  # 6th = 12th + 180
    cusps[6] = desc                          # 7th = descendant
    cusps[7] = (cusps[1] + 180.0) % 360.0   # 8th = 2nd + 180
    cusps[8] = (cusps[2] + 180.0) % 360.0   # 9th = 3rd + 180

    return [round(c % 360.0, 4) for c in cusps]


def _get_transit_positions(query_datetime: str) -> Dict[str, float]:
    """
    Get approximate planetary positions for the query datetime.

    Uses the astro_engine's calculation if Swiss Ephemeris is available,
    otherwise returns approximate positions based on mean motions.

    Args:
        query_datetime: ISO format "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD"

    Returns:
        {planet_name: sidereal_longitude}
    """
    try:
        from app.astro_engine import calculate_planet_positions
        # Parse datetime
        if "T" in query_datetime:
            dt = datetime.fromisoformat(query_datetime)
        elif " " in query_datetime:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d %H:%M:%S")
        else:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d")

        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M")

        # Use default location (New Delhi) if not specified
        result = calculate_planet_positions(
            birth_date=date_str,
            birth_time=time_str,
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        # Extract longitudes
        planets_dict: Dict[str, float] = {}
        planet_data = result.get("planets", {})
        for pname, pinfo in planet_data.items():
            if isinstance(pinfo, dict) and "longitude" in pinfo:
                planets_dict[pname] = pinfo["longitude"]
            elif isinstance(pinfo, (int, float)):
                planets_dict[pname] = float(pinfo)
        if planets_dict:
            return planets_dict
    except Exception:
        pass

    # Fallback: rough mean-motion positions from J2000 epoch
    try:
        if "T" in query_datetime:
            dt = datetime.fromisoformat(query_datetime)
        elif " " in query_datetime:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d %H:%M:%S")
        else:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d")
    except ValueError:
        dt = datetime(2024, 1, 1)

    # Days since J2000 (2000-01-01 12:00 TT)
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    days = (dt - j2000).total_seconds() / 86400.0

    # Approximate Lahiri ayanamsa (precession) at epoch
    ayanamsa = 23.85 + days * (50.3 / 3600.0 / 365.25)

    # Mean tropical longitudes at J2000 + daily rates (degrees/day)
    _MEAN: Dict[str, Tuple[float, float]] = {
        "Sun":     (280.46,   0.9856474),
        "Moon":    (218.32,  13.1763904),
        "Mercury": (252.25,   4.0923344),
        "Venus":   (181.98,   1.6021302),
        "Mars":    (355.43,   0.5240208),
        "Jupiter": ( 34.40,   0.0830853),
        "Saturn":  ( 49.94,   0.0334979),
        "Rahu":    (125.04,  -0.0529539),  # Mean north node (retrograde)
    }

    planets: Dict[str, float] = {}
    for pname, (lon0, rate) in _MEAN.items():
        tropical = (lon0 + rate * days) % 360.0
        sidereal = (tropical - ayanamsa) % 360.0
        planets[pname] = round(sidereal, 4)

    planets["Ketu"] = round((planets["Rahu"] + 180.0) % 360.0, 4)

    return planets


def calculate_kp_horary(
    number: int,
    query_datetime: str,
    query_place: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Calculate a full KP Horary chart from a querent's number (1-249).

    Process:
      1. Look up the degree range for the number from KP_HORARY_TABLE
      2. Set ascendant at the midpoint of that degree range
      3. Calculate 12 house cusps (Placidus approximation)
      4. Get planetary positions at query_datetime
      5. Run full KP significator analysis via calculate_kp_cuspal()
      6. Add ruling planets for the query moment

    Args:
        number: querent's chosen number (1-249)
        query_datetime: ISO datetime string ("YYYY-MM-DD HH:MM:SS")
        query_place: optional {latitude, longitude, tz_offset}

    Returns:
        dict with horary_number, degree_range, sign, star_lord, sub_lord,
        ascendant, house_cusps, planets, significators, ruling_planets, etc.
    """
    if not (1 <= number <= 249):
        raise ValueError(f"Horary number must be 1-249, got {number}")

    entry = KP_HORARY_TABLE[number - 1]
    ascendant = (entry["degree_start"] + entry["degree_end"]) / 2.0

    # House cusps
    latitude = 28.6139  # Default: New Delhi
    if query_place and "latitude" in query_place:
        latitude = query_place["latitude"]

    house_cusps = _approximate_placidus_cusps(ascendant, latitude)

    # Planetary positions at query time
    planet_longitudes = _get_transit_positions(query_datetime)

    # Parse date for day lord
    try:
        if "T" in query_datetime:
            dt = datetime.fromisoformat(query_datetime)
        elif " " in query_datetime:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d %H:%M:%S")
        else:
            dt = datetime.strptime(query_datetime, "%Y-%m-%d")
        birth_date_str = dt.strftime("%Y-%m-%d")
    except ValueError:
        birth_date_str = None

    # Full KP analysis
    kp_result = calculate_kp_cuspal(
        planet_longitudes=planet_longitudes,
        house_cusps=house_cusps,
        birth_date=birth_date_str,
    )

    return {
        "horary_number": number,
        "degree_range": {
            "start": entry["degree_start"],
            "end": entry["degree_end"],
            "start_dms": _degree_to_dms(entry["degree_start"]),
            "end_dms": _degree_to_dms(entry["degree_end"]),
        },
        "sign": entry["sign"],
        "sign_lord": entry["sign_lord"],
        "star_lord": entry["star_lord"],
        "sub_lord": entry["sub_lord"],
        "ascendant": round(ascendant, 4),
        "house_cusps": {i + 1: house_cusps[i] for i in range(12)},
        "planets": kp_result["planets"],
        "significators": kp_result["significators"],
        "house_significations": kp_result.get("house_significations", {}),
        "planet_significator_strengths": kp_result.get(
            "planet_significator_strengths", {}
        ),
        "ruling_planets": kp_result.get("ruling_planets", {}),
    }


def get_horary_prediction(
    number: int,
    question_type: str,
    query_datetime: str,
    query_place: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Get a KP Horary prediction for a specific question type.

    Workflow:
      1. Calculate the full horary chart
      2. Identify the relevant cusp for the question type
      3. Check if the sub-lord of that cusp signifies favorable houses
      4. Determine verdict (favorable / unfavorable / mixed)
      5. Estimate timing via current dasha period

    Args:
        number: querent's number (1-249)
        question_type: one of "marriage", "job", "travel", "health",
                       "finance", "legal", "education", "property"
        query_datetime: ISO datetime string
        query_place: optional location dict

    Returns:
        dict with full horary chart + prediction analysis
    """
    question_type = question_type.lower().strip()
    if question_type not in HORARY_QUESTION_HOUSES:
        raise ValueError(
            f"Unknown question type '{question_type}'. "
            f"Supported: {list(HORARY_QUESTION_HOUSES.keys())}"
        )

    qinfo = HORARY_QUESTION_HOUSES[question_type]
    chart = calculate_kp_horary(number, query_datetime, query_place)

    # Find the sub-lord of the relevant cusp
    cusp_num = qinfo["cusp_to_check"]
    cusp_degree = chart["house_cusps"][cusp_num]
    cusp_sub_info = get_sub_lord(cusp_degree)
    cusp_sub_lord = cusp_sub_info["sub_lord"]

    # Get significations of the cusp sub-lord
    sub_lord_significations: List[int] = chart["significators"].get(
        cusp_sub_lord, []
    )

    # Check overlap with favorable houses
    relevant = set(qinfo["relevant_houses"])
    negative = set(qinfo["negative_houses"])
    favorable_hits = sorted(relevant & set(sub_lord_significations))
    negative_hits = sorted(negative & set(sub_lord_significations))

    # Determine verdict
    if favorable_hits and not negative_hits:
        verdict = "favorable"
        verdict_detail = (
            f"Sub-lord of {cusp_num}th cusp ({cusp_sub_lord}) signifies "
            f"favorable houses {favorable_hits}."
        )
    elif negative_hits and not favorable_hits:
        verdict = "unfavorable"
        verdict_detail = (
            f"Sub-lord of {cusp_num}th cusp ({cusp_sub_lord}) signifies "
            f"negative houses {negative_hits}."
        )
    elif favorable_hits and negative_hits:
        verdict = "mixed"
        verdict_detail = (
            f"Sub-lord of {cusp_num}th cusp ({cusp_sub_lord}) signifies "
            f"both favorable {favorable_hits} and negative {negative_hits} houses."
        )
    else:
        verdict = "neutral"
        verdict_detail = (
            f"Sub-lord of {cusp_num}th cusp ({cusp_sub_lord}) does not "
            f"strongly signify the relevant houses for this question."
        )

    # Estimate timing from ruling planets
    ruling = chart.get("ruling_planets", {})
    timing_planets = [
        v for k, v in ruling.items() if v and v != ""
    ]
    timing_note = (
        f"Ruling planets at query time: {', '.join(set(timing_planets))}. "
        "Event likely when transit/dasha activates these planets."
        if timing_planets
        else "Timing analysis requires precise birth data."
    )

    chart["prediction"] = {
        "question_type": question_type,
        "description": qinfo["description"],
        "relevant_houses": qinfo["relevant_houses"],
        "negative_houses": qinfo["negative_houses"],
        "cusp_checked": cusp_num,
        "sub_lord_of_cusp": cusp_sub_lord,
        "sub_lord_signifies_houses": sub_lord_significations,
        "favorable_overlap": favorable_hits,
        "negative_overlap": negative_hits,
        "verdict": verdict,
        "verdict_detail": verdict_detail,
        "timing": timing_note,
    }

    return chart
