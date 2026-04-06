"""
aspects_engine.py -- Vedic Planetary Aspects Calculator
========================================================
Calculates graha drishti (planetary aspects) in the Vedic system.

All planets aspect the 7th house from their position.
Special aspects:
  - Mars    → additionally aspects 4th and 8th houses
  - Jupiter → additionally aspects 5th and 9th houses
  - Saturn  → additionally aspects 3rd and 10th houses
  - Rahu    → additionally aspects 5th and 9th houses (like Jupiter)
  - Ketu    → additionally aspects 5th and 9th houses (like Jupiter)

Provides:
  1. Aspects on Planets — Which planets aspect which other planets.
  2. Aspects on Bhavas  — Which planets aspect which houses (bhavas).
"""
from __future__ import annotations
from typing import Any, Dict, List, Set

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Standard special aspect houses (offset from planet position, 1-indexed)
# Every planet aspects 7th. These are ADDITIONAL aspects.
_SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}

# Aspect strength values (full = 1.0, three-quarter = 0.75, half = 0.5, quarter = 0.25)
# In Vedic astrology, aspects have varying strengths based on distance
_ASPECT_STRENGTHS: Dict[int, float] = {
    3: 0.25,   # Saturn special
    4: 0.75,   # Mars special
    5: 0.50,   # Jupiter special
    7: 1.00,   # Universal full aspect
    8: 0.75,   # Mars special
    9: 0.50,   # Jupiter special
    10: 0.25,  # Saturn special
}


def _get_aspected_houses(planet_name: str, planet_house: int) -> List[Dict[str, Any]]:
    """
    Get all houses aspected by a planet from its current house.

    Returns list of {house, offset, strength, type}.
    """
    aspects = []

    # Universal 7th aspect (full strength)
    h7 = ((planet_house - 1 + 7) % 12) + 1
    aspects.append({
        "house": h7,
        "offset": 7,
        "strength": 1.0,
        "type": "full (7th)",
    })

    # Special aspects
    for offset in _SPECIAL_ASPECTS.get(planet_name, []):
        target_house = ((planet_house - 1 + offset) % 12) + 1
        strength = _ASPECT_STRENGTHS.get(offset, 0.5)
        aspects.append({
            "house": target_house,
            "offset": offset,
            "strength": strength,
            "type": f"special ({offset}th)",
        })

    return aspects


def calculate_aspects(
    planets: Dict[str, Dict[str, Any]],
    houses: Any = None,
) -> Dict[str, Any]:
    """
    Calculate all planetary aspects.

    Args:
        planets: {planet_name: {sign, house, longitude, ...}}
        houses: Optional list of house data [{number, sign}]

    Returns:
        {
          "aspects_on_planets": [
            {aspecting, aspected, house_from, house_to, offset, strength, type}
          ],
          "aspects_on_bhavas": {
            house_number: [{planet, offset, strength, type}]
          },
          "planet_aspects_summary": {
            planet: {
              aspects_from: [{planet, offset, strength, type}],
              aspects_to: [{house, offset, strength, type, planets_in_house: [...]}]
            }
          }
        }
    """
    planet_names = list(planets.keys())

    # Build planet -> house mapping
    planet_houses: Dict[str, int] = {}
    for pname, pdata in planets.items():
        planet_houses[pname] = pdata.get("house", 1)

    # Build house -> planets mapping
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for pname, house in planet_houses.items():
        house_planets[house].append(pname)

    # ── Aspects on Bhavas ────────────────────────────────────────
    aspects_on_bhavas: Dict[int, List[Dict[str, Any]]] = {h: [] for h in range(1, 13)}
    for pname in planet_names:
        p_house = planet_houses[pname]
        aspected = _get_aspected_houses(pname, p_house)
        for asp in aspected:
            aspects_on_bhavas[asp["house"]].append({
                "planet": pname,
                "from_house": p_house,
                "offset": asp["offset"],
                "strength": asp["strength"],
                "type": asp["type"],
            })

    # ── Aspects on Planets ───────────────────────────────────────
    aspects_on_planets: List[Dict[str, Any]] = []
    for pname in planet_names:
        p_house = planet_houses[pname]
        aspected = _get_aspected_houses(pname, p_house)
        for asp in aspected:
            target_house = asp["house"]
            # Check which planets are in the aspected house
            for target_planet in house_planets.get(target_house, []):
                if target_planet != pname:
                    aspects_on_planets.append({
                        "aspecting": pname,
                        "aspected": target_planet,
                        "house_from": p_house,
                        "house_to": target_house,
                        "offset": asp["offset"],
                        "strength": asp["strength"],
                        "type": asp["type"],
                    })

    # ── Planet Summary ───────────────────────────────────────────
    planet_summary: Dict[str, Dict[str, Any]] = {}
    for pname in planet_names:
        p_house = planet_houses[pname]

        # Aspects FROM this planet
        aspects_from: List[Dict[str, Any]] = []
        for asp in aspects_on_planets:
            if asp["aspected"] == pname:
                aspects_from.append({
                    "planet": asp["aspecting"],
                    "from_house": asp["house_from"],
                    "offset": asp["offset"],
                    "strength": asp["strength"],
                    "type": asp["type"],
                })

        # Aspects TO (houses this planet aspects)
        aspected_houses = _get_aspected_houses(pname, p_house)
        aspects_to: List[Dict[str, Any]] = []
        for asp in aspected_houses:
            target_h = asp["house"]
            aspects_to.append({
                "house": target_h,
                "offset": asp["offset"],
                "strength": asp["strength"],
                "type": asp["type"],
                "planets_in_house": house_planets.get(target_h, []),
            })

        planet_summary[pname] = {
            "house": p_house,
            "aspected_by": aspects_from,
            "aspects_to": aspects_to,
            "total_aspects_received": len(aspects_from),
            "benefic_aspects": sum(
                1 for a in aspects_from
                if a["planet"] in ("Jupiter", "Venus", "Moon", "Mercury")
            ),
            "malefic_aspects": sum(
                1 for a in aspects_from
                if a["planet"] in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
            ),
        }

    # ── Bhava Summary ────────────────────────────────────────────
    bhava_summary: List[Dict[str, Any]] = []
    for h in range(1, 13):
        asp_list = aspects_on_bhavas[h]
        bhava_summary.append({
            "house": h,
            "sign": _SIGN_NAMES[(h - 1) % 12] if not houses else None,
            "planets_in_house": house_planets[h],
            "aspected_by": [a["planet"] for a in asp_list],
            "total_aspects": len(asp_list),
            "benefic_aspects": sum(
                1 for a in asp_list
                if a["planet"] in ("Jupiter", "Venus", "Moon", "Mercury")
            ),
            "malefic_aspects": sum(
                1 for a in asp_list
                if a["planet"] in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
            ),
        })

    return {
        "aspects_on_planets": aspects_on_planets,
        "aspects_on_bhavas": {str(h): asp_list for h, asp_list in aspects_on_bhavas.items()},
        "planet_aspects_summary": planet_summary,
        "bhava_summary": bhava_summary,
    }
