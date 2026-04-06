"""
sodashvarga_engine.py -- Sodashvarga (16 Divisional Charts) Summary & Vimshopak Bala
====================================================================================
Calculates planet placements across all 16 standard divisional charts and
computes the Vimshopak Bala (20-point strength) for each planet.

Provides two views:
  1. By Sign   — For each planet, which sign it falls in across each varga.
  2. By Planet — Vimshopak Bala score (weighted average of dignity across vargas).
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.divisional_charts import calculate_divisional_chart_detailed

# ── Sign/Lord Mappings ───────────────────────────────────────────
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Exaltation sign for each planet
_EXALTATION: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra", "Rahu": "Taurus", "Ketu": "Scorpio",
}

# Debilitation sign for each planet
_DEBILITATION: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries", "Rahu": "Scorpio", "Ketu": "Taurus",
}

# Own signs for each planet
_OWN_SIGNS: Dict[str, List[str]] = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
    "Rahu": ["Aquarius"],
    "Ketu": ["Scorpio"],
}

# Moolatrikona signs for each planet
_MOOLATRIKONA: Dict[str, str] = {
    "Sun": "Leo", "Moon": "Taurus", "Mars": "Aries",
    "Mercury": "Virgo", "Jupiter": "Sagittarius",
    "Venus": "Libra", "Saturn": "Aquarius",
}

# Friend/Enemy relationships (simplified)
_FRIENDS: Dict[str, List[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
}

_ENEMIES: Dict[str, List[str]] = {
    "Sun": ["Venus", "Saturn"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
}

# The 16 standard varga divisions
SODASHVARGA_DIVISIONS = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]

VARGA_NAMES: Dict[int, str] = {
    1: "D1 (Rashi)", 2: "D2 (Hora)", 3: "D3 (Drekkana)", 4: "D4 (Chaturthamsha)",
    7: "D7 (Saptamsha)", 9: "D9 (Navamsha)", 10: "D10 (Dashamsha)", 12: "D12 (Dwadashamsha)",
    16: "D16 (Shodashamsha)", 20: "D20 (Vimshamsha)", 24: "D24 (Chaturvimshamsha)",
    27: "D27 (Bhamsha)", 30: "D30 (Trimshamsha)", 40: "D40 (Khavedamsha)",
    45: "D45 (Akshavedamsha)", 60: "D60 (Shashtiamsha)",
}

# Vimshopak weights — Sodashvarga scheme (total = 20)
_VIMSHOPAK_WEIGHTS: Dict[int, float] = {
    1: 3.5, 2: 1.0, 3: 1.0, 4: 0.5,
    7: 0.5, 9: 3.0, 10: 0.5, 12: 0.5,
    16: 2.0, 20: 0.5, 24: 0.5, 27: 0.5,
    30: 1.0, 40: 0.5, 45: 0.5, 60: 4.0,
}

# Dignity scores (0–20 scale, will be multiplied by weight)
_DIGNITY_SCORES = {
    "exalted": 20,
    "moolatrikona": 18,
    "own": 15,
    "friend": 10,
    "neutral": 7,
    "enemy": 5,
    "debilitated": 2,
}


def _get_dignity(planet: str, sign: str) -> str:
    """Determine the dignity of a planet in a given sign."""
    if _EXALTATION.get(planet) == sign:
        return "exalted"
    if _DEBILITATION.get(planet) == sign:
        return "debilitated"
    if _MOOLATRIKONA.get(planet) == sign:
        return "moolatrikona"
    if sign in _OWN_SIGNS.get(planet, []):
        return "own"

    sign_lord = _SIGN_LORD.get(sign, "")
    if sign_lord == planet:
        return "own"
    if sign_lord in _FRIENDS.get(planet, []):
        return "friend"
    if sign_lord in _ENEMIES.get(planet, []):
        return "enemy"
    return "neutral"


def calculate_sodashvarga(
    planet_longitudes: Dict[str, float],
) -> Dict[str, Any]:
    """
    Calculate Sodashvarga for all planets.

    Args:
        planet_longitudes: {planet_name: longitude_degrees}

    Returns:
        {
          "by_sign": {planet: {division: {sign, dignity}}},
          "by_planet": {planet: {vimshopak_bala, dignities_summary, ...}},
          "varga_table": [{division, name, planets: {planet: sign}}]
        }
    """
    planets_list = [p for p in planet_longitudes if p not in ("Ascendant", "_Ascendant")]

    # Calculate all 16 varga charts
    varga_results: Dict[int, Dict[str, Dict[str, Any]]] = {}
    for div in SODASHVARGA_DIVISIONS:
        varga_results[div] = calculate_divisional_chart_detailed(planet_longitudes, div)

    # ── By Sign View ─────────────────────────────────────────────
    by_sign: Dict[str, Dict[str, Dict[str, str]]] = {}
    for planet in planets_list:
        by_sign[planet] = {}
        for div in SODASHVARGA_DIVISIONS:
            info = varga_results[div].get(planet)
            if info:
                sign = info["sign"]
                dignity = _get_dignity(planet, sign)
                by_sign[planet][str(div)] = {
                    "sign": sign,
                    "dignity": dignity,
                }

    # ── By Planet View (Vimshopak Bala)  ─────────────────────────
    by_planet: Dict[str, Dict[str, Any]] = {}
    for planet in planets_list:
        weighted_sum = 0.0
        total_weight = 0.0
        dignity_counts = {d: 0 for d in _DIGNITY_SCORES}

        for div in SODASHVARGA_DIVISIONS:
            info = varga_results[div].get(planet)
            if not info:
                continue
            sign = info["sign"]
            dignity = _get_dignity(planet, sign)
            dignity_counts[dignity] += 1
            score = _DIGNITY_SCORES.get(dignity, 7)
            weight = _VIMSHOPAK_WEIGHTS.get(div, 0.5)
            weighted_sum += (score / 20.0) * weight
            total_weight += weight

        vimshopak = round(weighted_sum, 2) if total_weight > 0 else 0
        by_planet[planet] = {
            "vimshopak_bala": vimshopak,
            "max_possible": 20.0,
            "percentage": round((vimshopak / 20.0) * 100, 1),
            "strength": "Strong" if vimshopak >= 12 else "Medium" if vimshopak >= 8 else "Weak",
            "dignities": dignity_counts,
        }

    # ── Varga Table (for tabular display) ────────────────────────
    varga_table: List[Dict[str, Any]] = []
    for div in SODASHVARGA_DIVISIONS:
        row: Dict[str, Any] = {
            "division": div,
            "name": VARGA_NAMES.get(div, f"D{div}"),
            "planets": {},
        }
        for planet in planets_list:
            info = varga_results[div].get(planet)
            if info:
                row["planets"][planet] = info["sign"]
        varga_table.append(row)

    return {
        "by_sign": by_sign,
        "by_planet": by_planet,
        "varga_table": varga_table,
    }
