"""
shadbala_engine.py -- Shadbala (Six-fold Strength) Calculator
=============================================================
Calculates the six components of planetary strength in Vedic astrology:
  1. Sthana Bala (Positional Strength)
  2. Dig Bala (Directional Strength)
  3. Kala Bala (Temporal Strength)
  4. Cheshta Bala (Motional Strength)
  5. Naisargika Bala (Natural Strength)
  6. Drik Bala (Aspectual Strength)

Total Shadbala = sum of all six. Compared against minimum required (Rupas).
"""
from __future__ import annotations

from typing import Any, Dict

# Sign names
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# The 7 planets for Shadbala (Rahu/Ketu excluded)
_SHADBALA_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Minimum required Shadbala (in Rupas/Virupas -- using Virupas here)
REQUIRED_STRENGTH: Dict[str, float] = {
    "Sun": 390, "Moon": 360, "Mars": 300,
    "Mercury": 420, "Jupiter": 390, "Venus": 330, "Saturn": 300,
}


# ============================================================
# 1. STHANA BALA (Positional Strength)
# ============================================================

# Exaltation signs (0-indexed)
_EXALTATION: Dict[str, int] = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6,
}

# Own signs
_OWN_SIGNS: Dict[str, list] = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7],
    "Mercury": [2, 5], "Jupiter": [8, 11],
    "Venus": [1, 6], "Saturn": [9, 10],
}

# Mool Trikona signs
_MOOL_TRIKONA: Dict[str, int] = {
    "Sun": 4, "Moon": 1, "Mars": 0, "Mercury": 5,
    "Jupiter": 8, "Venus": 6, "Saturn": 10,
}

# Debilitation signs (opposite of exaltation)
_DEBILITATION: Dict[str, int] = {
    "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
    "Jupiter": 9, "Venus": 5, "Saturn": 0,
}

# Friendly signs for each planet
_FRIENDLY_SIGNS: Dict[str, set] = {
    "Sun": {0, 3, 4, 8, 7},       # Aries, Cancer, Leo, Sag, Scorpio
    "Moon": {1, 2, 3, 4, 5, 6},   # Taurus through Libra
    "Mars": {0, 3, 4, 7, 8, 11},  # Aries, Cancer, Leo, Scorpio, Sag, Pisces
    "Mercury": {1, 2, 4, 5, 6},   # Taurus, Gemini, Leo, Virgo, Libra
    "Jupiter": {0, 3, 4, 7, 8, 11},
    "Venus": {1, 2, 5, 6, 9, 10, 11},
    "Saturn": {1, 2, 5, 6, 9, 10},
}


def _sign_name_to_index(sign_name: str) -> int:
    """Convert sign name to 0-based index."""
    try:
        return _SIGN_NAMES.index(sign_name)
    except ValueError:
        return 0


def _sthana_bala(planet: str, sign: str) -> float:
    """Calculate positional strength."""
    sign_idx = _sign_name_to_index(sign)

    if sign_idx == _EXALTATION.get(planet, -1):
        return 60.0
    if sign_idx in _OWN_SIGNS.get(planet, []):
        return 45.0
    if sign_idx == _MOOL_TRIKONA.get(planet, -1):
        return 40.0
    if sign_idx in _FRIENDLY_SIGNS.get(planet, set()):
        return 30.0
    if sign_idx == _DEBILITATION.get(planet, -1):
        return 0.0
    return 15.0  # Neutral


# ============================================================
# 2. DIG BALA (Directional Strength)
# ============================================================

# Strongest house (1-indexed) for each planet
_STRONG_HOUSE: Dict[str, int] = {
    "Sun": 10, "Moon": 4, "Mars": 10,
    "Mercury": 1, "Jupiter": 1, "Venus": 4, "Saturn": 7,
}


def _dig_bala(planet: str, house: int) -> float:
    """
    Calculate directional strength.
    Max 60 when in strongest house, decreasing with distance.
    """
    strong_house = _STRONG_HOUSE.get(planet, 1)
    # Calculate minimum distance on the 12-house circle
    dist = abs(house - strong_house)
    if dist > 6:
        dist = 12 - dist
    return round(60.0 * (1.0 - dist / 6.0), 2)


# ============================================================
# 3. KALA BALA (Temporal Strength)
# ============================================================

# Day-strong vs Night-strong planets
_DAY_STRONG = {"Sun", "Jupiter", "Venus"}
_NIGHT_STRONG = {"Moon", "Mars", "Saturn"}


def _kala_bala(planet: str, is_daytime: bool = True) -> float:
    """
    Calculate temporal strength.
    Day/night strength: favorable = 30, unfavorable = 15.
    Mercury is always moderate (22.5).
    """
    if planet == "Mercury":
        return 22.5  # Mercury is neutral day/night
    if is_daytime:
        return 30.0 if planet in _DAY_STRONG else 15.0
    else:
        return 30.0 if planet in _NIGHT_STRONG else 15.0


# ============================================================
# 4. CHESHTA BALA (Motional Strength)
# ============================================================

def _cheshta_bala(planet: str, is_retrograde: bool = False) -> float:
    """
    Calculate motional strength.
    Sun and Moon don't go retrograde, assigned fixed values.
    Retrograde = 60, Direct = 30, Stationary = 15.
    """
    if planet == "Sun":
        return 30.0  # Sun never retrogrades, moderate
    if planet == "Moon":
        return 30.0  # Moon never retrogrades, moderate
    if is_retrograde:
        return 60.0
    return 30.0  # Direct motion


# ============================================================
# 5. NAISARGIKA BALA (Natural Strength)
# ============================================================

_NAISARGIKA: Dict[str, float] = {
    "Sun": 60.0, "Moon": 51.43, "Mars": 17.14,
    "Mercury": 25.71, "Jupiter": 34.29, "Venus": 42.86, "Saturn": 8.57,
}


def _naisargika_bala(planet: str) -> float:
    """Natural (innate) strength -- fixed values."""
    return _NAISARGIKA.get(planet, 0.0)


# ============================================================
# 6. DRIK BALA (Aspectual Strength)
# ============================================================

_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


def _drik_bala(planet: str, planet_houses: Dict[str, int]) -> float:
    """
    Calculate aspectual strength based on aspects from benefics/malefics.
    Benefic aspect on this planet's house = +15.
    Malefic aspect on this planet's house = -15.
    Standard aspect: all planets aspect 7th house from their position.
    """
    if planet not in planet_houses:
        return 0.0
    planet_house = planet_houses[planet]
    total = 0.0

    for other, other_house in planet_houses.items():
        if other == planet:
            continue

        # Check if other planet aspects this planet's house
        # Standard 7th house aspect
        aspect_houses = {((other_house - 1 + 7) % 12) + 1}

        # Special aspects
        if other == "Mars":
            aspect_houses.add(((other_house - 1 + 4) % 12) + 1)
            aspect_houses.add(((other_house - 1 + 8) % 12) + 1)
        elif other == "Jupiter":
            aspect_houses.add(((other_house - 1 + 5) % 12) + 1)
            aspect_houses.add(((other_house - 1 + 9) % 12) + 1)
        elif other == "Saturn":
            aspect_houses.add(((other_house - 1 + 3) % 12) + 1)
            aspect_houses.add(((other_house - 1 + 10) % 12) + 1)

        if planet_house in aspect_houses:
            if other in _BENEFICS:
                total += 15.0
            elif other in _MALEFICS:
                total -= 15.0

    return round(total, 2)


# ============================================================
# PUBLIC API
# ============================================================

def calculate_shadbala(
    planet_signs: Dict[str, str],
    planet_houses: Dict[str, int],
    is_daytime: bool = True,
    retrograde_planets: set = None,
) -> Dict[str, Any]:
    """
    Calculate Shadbala for all 7 planets.

    Args:
        planet_signs: {planet: sign_name} for Sun through Saturn
        planet_houses: {planet: house_number} for all planets
        is_daytime: whether the birth was during daytime
        retrograde_planets: set of planet names that are retrograde

    Returns:
        {
            "planets": {
                planet: {
                    sthana, dig, kala, cheshta, naisargika, drik,
                    total, required, ratio, is_strong
                }
            }
        }
    """
    if retrograde_planets is None:
        retrograde_planets = set()

    planets_result: Dict[str, Dict[str, Any]] = {}

    for planet in _SHADBALA_PLANETS:
        sign = planet_signs.get(planet, "Aries")
        house = planet_houses.get(planet, 1)
        is_retro = planet in retrograde_planets

        sthana = _sthana_bala(planet, sign)
        dig = _dig_bala(planet, house)
        kala = _kala_bala(planet, is_daytime)
        cheshta = _cheshta_bala(planet, is_retro)
        naisargika = _naisargika_bala(planet)
        drik = _drik_bala(planet, planet_houses)

        total = round(sthana + dig + kala + cheshta + naisargika + drik, 2)
        required = REQUIRED_STRENGTH.get(planet, 300)
        ratio = round(total / required, 2) if required > 0 else 0.0

        planets_result[planet] = {
            "sthana": sthana,
            "dig": dig,
            "kala": kala,
            "cheshta": cheshta,
            "naisargika": naisargika,
            "drik": drik,
            "total": total,
            "required": required,
            "ratio": ratio,
            "is_strong": total >= required,
        }

    return {"planets": planets_result}
