"""
ashtakvarga_engine.py -- Ashtakvarga Calculation Engine
========================================================
Calculates the Ashtakvarga point system used in Vedic astrology for
transit predictions. Each planet gets 0 or 1 point (bindu) from each
of the 7 contributing planets + Ascendant for each of the 12 signs.

The Sarvashtakvarga is the sum of all individual planet ashtakvargas.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set

# Sign names
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# ============================================================
# BENEFIC POINTS -- Houses from each contributing planet that
# give a benefic point (bindu). Houses are 1-indexed relative
# to the contributing planet's position.
# Format: BENEFIC_POINTS[receiving_planet][contributing_planet] = set of house numbers
# ============================================================

BENEFIC_POINTS: Dict[str, Dict[str, Set[int]]] = {
    "Sun": {
        "Sun":       {1, 2, 4, 7, 8, 9, 10, 11},
        "Moon":      {3, 6, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 9, 11},
        "Venus":     {6, 7, 12},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {3, 4, 6, 10, 11, 12},
    },
    "Moon": {
        "Sun":       {3, 6, 7, 8, 10, 11},
        "Moon":      {1, 3, 6, 7, 10, 11},
        "Mars":      {2, 3, 5, 6, 9, 10, 11},
        "Mercury":   {1, 3, 4, 5, 7, 8, 10, 11},
        "Jupiter":   {1, 4, 7, 8, 10, 11, 12},
        "Venus":     {3, 4, 5, 7, 9, 10, 11},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {3, 6, 10, 11},
    },
    "Mars": {
        "Sun":       {3, 5, 6, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {3, 5, 6, 11},
        "Jupiter":   {6, 10, 11, 12},
        "Venus":     {6, 8, 11, 12},
        "Saturn":    {1, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 3, 6, 10, 11},
    },
    "Mercury": {
        "Sun":       {5, 6, 9, 11, 12},
        "Moon":      {2, 4, 6, 8, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {1, 3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {6, 8, 11, 12},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 11},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 2, 4, 6, 8, 10, 11},
    },
    "Jupiter": {
        "Sun":       {1, 2, 3, 4, 7, 8, 9, 10, 11},
        "Moon":      {2, 5, 7, 9, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {1, 2, 4, 5, 6, 9, 10, 11},
        "Jupiter":   {1, 2, 3, 4, 7, 8, 10, 11},
        "Venus":     {2, 5, 6, 9, 10, 11},
        "Saturn":    {3, 5, 6, 12},
        "Ascendant": {1, 2, 4, 5, 6, 7, 9, 10, 11},
    },
    "Venus": {
        "Sun":       {8, 11, 12},
        "Moon":      {1, 2, 3, 4, 5, 8, 9, 11, 12},
        "Mars":      {3, 5, 6, 9, 11, 12},
        "Mercury":   {3, 5, 6, 9, 11},
        "Jupiter":   {5, 8, 9, 10, 11},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 10, 11},
        "Saturn":    {3, 4, 5, 8, 9, 10, 11},
        "Ascendant": {1, 2, 3, 4, 5, 8, 9, 11},
    },
    "Saturn": {
        "Sun":       {1, 2, 4, 7, 8, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {3, 5, 6, 10, 11, 12},
        "Mercury":   {6, 8, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 11, 12},
        "Venus":     {6, 11, 12},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {1, 3, 4, 6, 10, 11},
    },
}


def _sign_name_to_index(sign_name: str) -> int:
    """Convert sign name to 0-based index."""
    return _SIGN_NAMES.index(sign_name)


def calculate_ashtakvarga(planet_signs: Dict[str, str]) -> Dict[str, Any]:
    """
    Calculate the Ashtakvarga system for a given chart.

    Args:
        planet_signs: dict of {planet_name: sign_name}
                      Must include: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
                      May include: Ascendant (sign of the ascendant)

    Returns:
        {
            "planet_bindus": {
                planet: {sign: points}  -- for each of the 7 planets
            },
            "sarvashtakvarga": {sign: total_points}  -- summed across all planets,
            "planet_details": {
                planet: {
                    "contributors": {
                        contributor: {sign: 0_or_1}  -- 8 contributors per planet
                    },
                    "totals": {sign: points}  -- same as planet_bindus[planet]
                }
            }
        }

        Contributors are keyed as: Sun, Moon, Mars, Mercury, Jupiter, Venus,
        Saturn, Lagna (Ascendant mapped to "Lagna" in output).
    """
    # Validate required planets
    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    available = set(planet_signs.keys())
    missing = required - available
    if missing:
        raise ValueError(f"Missing planets for Ashtakvarga: {missing}")

    # Build position map: planet/ascendant -> 0-based sign index
    positions: Dict[str, int] = {}
    for name, sign in planet_signs.items():
        if name in required or name == "Ascendant":
            positions[name] = _sign_name_to_index(sign)

    # If Ascendant not provided, use Aries as default
    if "Ascendant" not in positions:
        positions["Ascendant"] = 0

    # Contributing bodies (7 planets + Ascendant)
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]

    # Display name mapping: internal "Ascendant" -> output "Lagna"
    _CONTRIB_DISPLAY = {c: ("Lagna" if c == "Ascendant" else c) for c in contributors}

    planet_bindus: Dict[str, Dict[str, int]] = {}
    planet_details: Dict[str, Dict[str, Any]] = {}
    sarvashtakvarga: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

    # Calculate for each receiving planet
    for recv_planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        recv_table = BENEFIC_POINTS[recv_planet]
        bindus: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}
        contrib_matrix: Dict[str, Dict[str, int]] = {}

        for contrib in contributors:
            display_name = _CONTRIB_DISPLAY[contrib]
            # Initialise this contributor's row to all zeros
            contrib_row: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

            if contrib in recv_table and contrib in positions:
                benefic_houses = recv_table[contrib]
                contrib_sign_index = positions[contrib]

                # For each benefic house, mark the corresponding sign
                for house_num in benefic_houses:
                    # House N from contributor = sign at (contributor_sign + N - 1) mod 12
                    target_sign_index = (contrib_sign_index + house_num - 1) % 12
                    target_sign = _SIGN_NAMES[target_sign_index]
                    contrib_row[target_sign] = 1
                    bindus[target_sign] += 1

            contrib_matrix[display_name] = contrib_row

        planet_bindus[recv_planet] = bindus
        planet_details[recv_planet] = {
            "contributors": contrib_matrix,
            "totals": bindus,
        }

        # Accumulate into sarvashtakvarga
        for sign in _SIGN_NAMES:
            sarvashtakvarga[sign] += bindus[sign]

    return {
        "planet_bindus": planet_bindus,
        "sarvashtakvarga": sarvashtakvarga,
        "planet_details": planet_details,
    }
