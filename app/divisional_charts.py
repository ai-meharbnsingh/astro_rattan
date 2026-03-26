"""
divisional_charts.py -- Vedic Divisional Chart Calculator
==========================================================
Calculates divisional (varga) charts used in Vedic astrology.
Supports D9 (Navamsa), D10 (Dasamsa), and generic divisional charts.

Each divisional chart maps a planet's longitude in the Rasi (D1) chart
to a sign in the divisional chart based on specific mathematical divisions.
"""
from __future__ import annotations

from typing import Any, Dict, List

# Sign names in order (0-indexed)
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _sign_index(sign_name: str) -> int:
    """Return the 0-based index of a zodiac sign."""
    return _SIGN_NAMES.index(sign_name)


# ============================================================
# D9 -- Navamsa
# ============================================================

def calculate_d9_navamsa(planet_longitudes: Dict[str, float]) -> Dict[str, str]:
    """
    Calculate the Navamsa (D9) sign for each planet.

    Navamsa divides each 30-degree sign into 9 equal parts of 3deg 20min each.
    The starting sign for each rasi sign's navamsa cycle:
      - Fire signs (Aries, Leo, Sagittarius) start from Aries
      - Earth signs (Taurus, Virgo, Capricorn) start from Capricorn
      - Air signs (Gemini, Libra, Aquarius) start from Libra
      - Water signs (Cancer, Scorpio, Pisces) start from Cancer

    Args:
        planet_longitudes: {planet_name: sidereal_longitude_degrees}

    Returns:
        {planet_name: navamsa_sign_name}
    """
    result: Dict[str, str] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0

        # Which of the 9 navamsa divisions (0-8)
        navamsa_part = int(degree_in_sign / (30.0 / 9.0))
        if navamsa_part >= 9:
            navamsa_part = 8

        # Starting sign based on element of the rasi sign
        element = rasi_index % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
        start_signs = {0: 0, 1: 9, 2: 6, 3: 3}  # Aries=0, Cap=9, Libra=6, Cancer=3
        start = start_signs[element]

        navamsa_sign_index = (start + navamsa_part) % 12
        result[planet] = _SIGN_NAMES[navamsa_sign_index]

    return result


# ============================================================
# D10 -- Dasamsa
# ============================================================

def calculate_d10_dasamsa(planet_longitudes: Dict[str, float]) -> Dict[str, str]:
    """
    Calculate the Dasamsa (D10) sign for each planet.

    Dasamsa divides each 30-degree sign into 10 equal parts of 3 degrees each.
    For odd signs (Aries=1, Gemini=3, ...): starts from the same sign.
    For even signs (Taurus=2, Cancer=4, ...): starts from the 9th sign from it.

    Args:
        planet_longitudes: {planet_name: sidereal_longitude_degrees}

    Returns:
        {planet_name: dasamsa_sign_name}
    """
    result: Dict[str, str] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0

        # Which of the 10 dasamsa divisions (0-9)
        dasamsa_part = int(degree_in_sign / 3.0)
        if dasamsa_part >= 10:
            dasamsa_part = 9

        # Odd sign (1-indexed): starts from same sign
        # Even sign (1-indexed): starts from 9th sign
        sign_number = rasi_index + 1  # 1-indexed
        if sign_number % 2 == 1:
            # Odd sign: start from same sign
            start = rasi_index
        else:
            # Even sign: start from 9th sign (0-indexed: rasi_index + 8)
            start = (rasi_index + 9) % 12

        dasamsa_sign_index = (start + dasamsa_part) % 12
        result[planet] = _SIGN_NAMES[dasamsa_sign_index]

    return result


# ============================================================
# GENERIC -- Any divisional chart
# ============================================================

def calculate_divisional_chart(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, str]:
    """
    Calculate a generic divisional chart for any division number.

    Uses the standard Parashari formula:
      - Divide each sign (30 deg) into `division` equal parts.
      - The starting sign depends on the specific division type.

    For D9 and D10, delegates to the specialized functions.
    For other divisions, uses the simplified cyclic method:
      part_index = floor(degree_in_sign / (30/division))
      result_sign = (rasi_index * division + part_index) mod 12

    Args:
        planet_longitudes: {planet_name: sidereal_longitude_degrees}
        division: divisional chart number (2, 3, 4, 7, 9, 10, 12, 16, etc.)

    Returns:
        {planet_name: divisional_sign_name}
    """
    if division == 9:
        return calculate_d9_navamsa(planet_longitudes)
    if division == 10:
        return calculate_d10_dasamsa(planet_longitudes)
    if division < 1:
        raise ValueError("Division must be >= 1")

    result: Dict[str, str] = {}
    part_size = 30.0 / division

    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0

        part_index = int(degree_in_sign / part_size)
        if part_index >= division:
            part_index = division - 1

        # Generic cyclic formula
        div_sign_index = (rasi_index * division + part_index) % 12
        result[planet] = _SIGN_NAMES[div_sign_index]

    return result
