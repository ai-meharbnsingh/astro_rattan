"""
shadbala_engine.py -- Full Classical Shadbala Calculator (BPHS)
================================================================
Calculates all six components of planetary strength per Brihat Parashara
Hora Shastra.  All intermediate values are in Virupas (1 Rupa = 60 Virupas).

Components:
  1. Sthana Bala  (Positional)  — 5 sub-components
  2. Dig Bala     (Directional)
  3. Kala Bala    (Temporal)     — 6 sub-components
  4. Cheshta Bala (Motional)
  5. Naisargika Bala (Natural)
  6. Drik Bala    (Aspectual)
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Set

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SHADBALA_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Minimum required Shadbala in Virupas
REQUIRED_STRENGTH: Dict[str, float] = {
    "Sun": 390, "Moon": 360, "Mars": 300,
    "Mercury": 420, "Jupiter": 390, "Venus": 330, "Saturn": 300,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sign_name_to_index(sign_name: str) -> int:
    """Convert sign name to 0-based index (Aries=0 .. Pisces=11)."""
    try:
        return _SIGN_NAMES.index(sign_name)
    except ValueError:
        return 0


def _angular_distance(a: float, b: float) -> float:
    """Shortest arc between two longitudes on a 360-degree circle."""
    d = abs(a - b) % 360.0
    return d if d <= 180.0 else 360.0 - d


# ============================================================
# 1. STHANA BALA (Positional Strength) — 5 sub-components
# ============================================================

# --- 1a. Uchcha Bala (exaltation strength) ---
# Exaltation degrees (absolute sidereal longitude)
_EXALTATION_DEGREE: Dict[str, float] = {
    "Sun": 10.0,       # 10° Aries
    "Moon": 33.0,      # 3° Taurus
    "Mars": 298.0,     # 28° Capricorn
    "Mercury": 165.0,  # 15° Virgo
    "Jupiter": 95.0,   # 5° Cancer
    "Venus": 357.0,    # 27° Pisces
    "Saturn": 200.0,   # 20° Libra
}


def _uchcha_bala(planet: str, longitude: Optional[float]) -> float:
    """
    Exaltation strength.  Max 60 Virupas when at exact exaltation degree,
    0 at debilitation (180° away).
    Formula: (180 - |planet_lon - exalt_deg|) / 3  (capped at 0..60).
    """
    if longitude is None:
        return 30.0  # neutral fallback
    exalt = _EXALTATION_DEGREE.get(planet)
    if exalt is None:
        return 30.0
    dist = _angular_distance(longitude, exalt)
    return round(max(0.0, min(60.0, (180.0 - dist) / 3.0)), 2)


# --- 1b. Saptavargaja Bala (dignity across 7 divisional charts) ---
# Dignity scores per chart
_DIGNITY_SCORES = {
    "moolatrikona": 45.0,
    "own": 30.0,
    "great_friend": 22.5,
    "friend": 15.0,
    "neutral": 7.5,
    "enemy": 3.75,
    "great_enemy": 1.875,
}

# Own signs (0-indexed)
_OWN_SIGNS: Dict[str, set] = {
    "Sun": {4},          # Leo
    "Moon": {3},         # Cancer
    "Mars": {0, 7},      # Aries, Scorpio
    "Mercury": {2, 5},   # Gemini, Virgo
    "Jupiter": {8, 11},  # Sagittarius, Pisces
    "Venus": {1, 6},     # Taurus, Libra
    "Saturn": {9, 10},   # Capricorn, Aquarius
}

# Moolatrikona signs
_MOOL_TRIKONA: Dict[str, int] = {
    "Sun": 4, "Moon": 1, "Mars": 0, "Mercury": 5,
    "Jupiter": 8, "Venus": 6, "Saturn": 10,
}

# Exaltation signs (0-indexed)
_EXALTATION_SIGN: Dict[str, int] = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6,
}

# Debilitation signs
_DEBILITATION_SIGN: Dict[str, int] = {
    "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
    "Jupiter": 9, "Venus": 5, "Saturn": 0,
}

# Natural friendships (BPHS)
_NATURAL_FRIENDS: Dict[str, set] = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}

_NATURAL_ENEMIES: Dict[str, set] = {
    "Sun": {"Venus", "Saturn"},
    "Moon": set(),
    "Mars": {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"},
    "Saturn": {"Sun", "Moon", "Mars"},
}


def _get_relationship(planet: str, sign_idx: int) -> str:
    """
    Determine the relationship of planet to the lord of sign_idx.
    Returns one of: moolatrikona, own, great_friend, friend, neutral, enemy, great_enemy.
    """
    # Sign lords (0-indexed sign -> planet name)
    sign_lords = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
        4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
        8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
    }
    lord = sign_lords.get(sign_idx, "")

    # Moolatrikona check
    if _MOOL_TRIKONA.get(planet) == sign_idx:
        return "moolatrikona"

    # Own sign check
    if sign_idx in _OWN_SIGNS.get(planet, set()):
        return "own"

    if lord == planet:
        return "own"

    # Friendship
    friends = _NATURAL_FRIENDS.get(planet, set())
    enemies = _NATURAL_ENEMIES.get(planet, set())

    if lord in friends:
        return "friend"
    elif lord in enemies:
        return "enemy"
    else:
        return "neutral"


def _divisional_sign(longitude: float, division: int) -> int:
    """
    Return the 0-indexed sign for a given divisional chart.
    D1=1, D2=2, D3=3, D7=7, D9=9, D12=12, D30=30.
    """
    if longitude is None:
        return 0
    base_sign = int(longitude // 30) % 12
    degree_in_sign = longitude % 30.0

    if division == 1:
        return base_sign
    elif division == 2:
        # Hora: 0-15 = sign, 15-30 = sign+1 (mod 12) simplified
        # Odd signs: 0-15 Sun(Leo=4), 15-30 Moon(Cancer=3)
        # Even signs: 0-15 Moon(Cancer=3), 15-30 Sun(Leo=4)
        is_odd = (base_sign % 2) == 0  # Aries=0 is odd sign
        if degree_in_sign < 15:
            return 4 if is_odd else 3  # Leo or Cancer
        else:
            return 3 if is_odd else 4
    elif division == 3:
        # Drekkana: each 10° segment maps to a trine sign
        third = int(degree_in_sign // 10)
        return (base_sign + third * 4) % 12
    elif division == 7:
        # Saptamsa: each 30/7 ≈ 4.2857° segment
        part = int(degree_in_sign / (30.0 / 7.0))
        part = min(part, 6)
        if (base_sign % 2) == 0:  # odd sign
            return (base_sign + part) % 12
        else:  # even sign
            return (base_sign + 6 + part) % 12
    elif division == 9:
        # Navamsa: each 3°20' segment
        part = int(degree_in_sign / (30.0 / 9.0))
        part = min(part, 8)
        # Fire signs start from Aries, Earth from Cap, Air from Libra, Water from Cancer
        element_start = {0: 0, 1: 9, 2: 6, 3: 3}  # fire, earth, air, water
        element = base_sign % 4  # 0=fire, 1=earth, 2=air, 3=water
        return (element_start[element] + part) % 12
    elif division == 12:
        # Dwadasamsa: each 2°30' segment
        part = int(degree_in_sign / 2.5)
        part = min(part, 11)
        return (base_sign + part) % 12
    elif division == 30:
        # Trimsamsa: unequal portions, varies by odd/even sign
        is_odd = (base_sign % 2) == 0  # Aries(0)=odd
        if is_odd:
            if degree_in_sign < 5:
                return 0  # Mars -> Aries
            elif degree_in_sign < 10:
                return 10  # Saturn -> Aquarius
            elif degree_in_sign < 18:
                return 8  # Jupiter -> Sagittarius
            elif degree_in_sign < 25:
                return 2  # Mercury -> Gemini
            else:
                return 1  # Venus -> Taurus
        else:
            if degree_in_sign < 5:
                return 1  # Venus -> Taurus
            elif degree_in_sign < 12:
                return 5  # Mercury -> Virgo
            elif degree_in_sign < 20:
                return 11  # Jupiter -> Pisces
            elif degree_in_sign < 25:
                return 9  # Saturn -> Capricorn
            else:
                return 7  # Mars -> Scorpio
    return base_sign


def _saptavargaja_bala(planet: str, longitude: Optional[float]) -> float:
    """
    Sum dignity scores across D1, D2, D3, D7, D9, D12, D30.
    """
    if longitude is None:
        # Fallback: 7 charts * neutral (7.5) = 52.5
        return 52.5

    divisions = [1, 2, 3, 7, 9, 12, 30]
    total = 0.0
    for div in divisions:
        div_sign = _divisional_sign(longitude, div)
        relationship = _get_relationship(planet, div_sign)
        total += _DIGNITY_SCORES.get(relationship, 7.5)
    return round(total, 2)


# --- 1c. Ojhayugma Bala (odd/even sign and bhava) ---

def _ojhayugma_bala(planet: str, sign: str, house: int) -> float:
    """
    Moon and Venus get 15 Virupas in even signs; all others in odd signs.
    Same logic for house (bhava). Max 30.
    """
    sign_idx = _sign_name_to_index(sign)
    is_even_sign = (sign_idx % 2) == 1   # Taurus(1)=even, etc.
    is_even_house = (house % 2) == 0       # 2,4,6,8,10,12 = even

    score = 0.0
    if planet in ("Moon", "Venus"):
        if is_even_sign:
            score += 15.0
        if is_even_house:
            score += 15.0
    else:
        if not is_even_sign:   # odd sign
            score += 15.0
        if not is_even_house:  # odd house
            score += 15.0
    return score


# --- 1d. Kendra Bala ---

def _kendra_bala(house: int) -> float:
    """
    Kendra houses (1,4,7,10)=60; Panaphara (2,5,8,11)=30; Apoklima (3,6,9,12)=15.
    """
    h = ((house - 1) % 12) + 1
    if h in (1, 4, 7, 10):
        return 60.0
    elif h in (2, 5, 8, 11):
        return 30.0
    else:
        return 15.0


# --- 1e. Drekkana Bala ---

def _drekkana_bala(planet: str, longitude: Optional[float], sign: str) -> float:
    """
    Male planets (Sun, Mars, Jupiter) strong in 1st drekkana (0-10°) = 15.
    Female (Moon, Venus) strong in 3rd drekkana (20-30°) = 15.
    Neutral (Mercury, Saturn) strong in 2nd drekkana (10-20°) = 15.
    """
    if longitude is not None:
        deg_in_sign = longitude % 30.0
    else:
        deg_in_sign = 15.0  # fallback to middle

    if deg_in_sign < 10.0:
        drekkana = 1
    elif deg_in_sign < 20.0:
        drekkana = 2
    else:
        drekkana = 3

    male = {"Sun", "Mars", "Jupiter"}
    female = {"Moon", "Venus"}
    # Mercury and Saturn are neutral

    if planet in male and drekkana == 1:
        return 15.0
    elif planet in female and drekkana == 3:
        return 15.0
    elif planet not in male and planet not in female and drekkana == 2:
        return 15.0
    return 0.0


def _sthana_bala(
    planet: str,
    sign: str,
    house: int,
    longitude: Optional[float],
) -> Dict[str, float]:
    """
    Total Sthana Bala = Uchcha + Saptavargaja + Ojhayugma + Kendra + Drekkana.
    Returns dict with breakdown and total.
    """
    uchcha = _uchcha_bala(planet, longitude)
    saptavargaja = _saptavargaja_bala(planet, longitude)
    ojhayugma = _ojhayugma_bala(planet, sign, house)
    kendra = _kendra_bala(house)
    drekkana = _drekkana_bala(planet, longitude, sign)

    total = round(uchcha + saptavargaja + ojhayugma + kendra + drekkana, 2)
    return {
        "uchcha": uchcha,
        "saptavargaja": saptavargaja,
        "ojhayugma": ojhayugma,
        "kendra": kendra,
        "drekkana": drekkana,
        "total": total,
    }


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
    Directional strength.
    Max 60 at strongest house, decreasing linearly to 0 at the opposite house.
    Formula: 60 * (1 - min_distance / 6)  where distance on 12-house circle.
    """
    strong_house = _STRONG_HOUSE.get(planet, 1)
    dist = abs(house - strong_house)
    if dist > 6:
        dist = 12 - dist
    return round(60.0 * (1.0 - dist / 6.0), 2)


# ============================================================
# 3. KALA BALA (Temporal Strength) — 6 sub-components
# ============================================================

# Day-strong / Night-strong classification
_DAY_STRONG = {"Sun", "Jupiter", "Venus"}
_NIGHT_STRONG = {"Moon", "Mars", "Saturn"}

# Weekday lords: Monday=0..Sunday=6 (Python weekday())
# But Vedic vara: Sun=Sunday, Moon=Monday, Mars=Tuesday, Mercury=Wednesday,
# Jupiter=Thursday, Venus=Friday, Saturn=Saturday
_WEEKDAY_LORD = {
    6: "Sun",       # Sunday
    0: "Moon",      # Monday
    1: "Mars",      # Tuesday
    2: "Mercury",   # Wednesday
    3: "Jupiter",   # Thursday
    4: "Venus",     # Friday
    5: "Saturn",    # Saturday
}

# Year lords cycle (same 7 planets in order used for Abda lord)
_YEAR_LORD_CYCLE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Month lord cycle
_MONTH_LORD_CYCLE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def _nathonnatha_bala(planet: str, birth_hour: float) -> float:
    """
    Diurnal/nocturnal strength based on birth hour.
    Diurnal planets (Sun, Jupiter, Venus): max 60 at noon (12), 0 at midnight (0/24).
    Nocturnal planets (Moon, Mars, Saturn): max 60 at midnight, 0 at noon.
    Mercury: always 60 (ubhaya — both day and night).
    """
    if planet == "Mercury":
        return 60.0

    # Distance from noon in hours (0-12 scale)
    hour = birth_hour % 24.0
    dist_from_noon = abs(hour - 12.0)
    if dist_from_noon > 12.0:
        dist_from_noon = 24.0 - dist_from_noon

    # Noon=0 distance, midnight=12 distance
    # Diurnal: strength = 60 * (1 - dist/12)
    diurnal_strength = round(60.0 * (1.0 - dist_from_noon / 12.0), 2)

    if planet in _DAY_STRONG:
        return diurnal_strength
    elif planet in _NIGHT_STRONG:
        return round(60.0 - diurnal_strength, 2)
    return 30.0  # fallback


def _paksha_bala(planet: str, moon_sun_elongation: float) -> float:
    """
    Paksha (lunar phase) strength.
    Benefics (Jupiter, Venus, Moon, Mercury) strong in Shukla Paksha.
    moon_sun_elongation = Moon longitude - Sun longitude (mod 360), i.e. the
    tithi angle. Shukla Paksha = 0-180, Krishna Paksha = 180-360.
    Benefic value = elongation / 3 (for Shukla) or (360-elongation) / 3 (for Krishna).
    Malefics get (60 - benefic_value).
    """
    elong = moon_sun_elongation % 360.0
    # Convert to 0-180 range: in Shukla the elongation itself gives strength,
    # in Krishna, the distance from next new moon gives strength.
    if elong <= 180.0:
        benefic_val = round(elong / 3.0, 2)
    else:
        benefic_val = round((360.0 - elong) / 3.0, 2)

    benefic_val = min(60.0, max(0.0, benefic_val))

    _BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
    if planet in _BENEFICS:
        return benefic_val
    else:
        return round(60.0 - benefic_val, 2)


def _tribhaga_bala(planet: str, birth_hour: float, is_daytime: bool) -> float:
    """
    Day divided into 3 equal parts, night into 3 equal parts.
    Day: 1st third=Mercury(60), 2nd=Sun(60), 3rd=Saturn(60).
    Night: 1st third=Moon(60), 2nd=Venus(60), 3rd=Mars(60).
    Jupiter always gets 60.
    """
    if planet == "Jupiter":
        return 60.0

    hour = birth_hour % 24.0

    if is_daytime:
        # Approximate day: 6:00-18:00 -> 3 parts of 4 hours each
        day_hour = hour - 6.0
        if day_hour < 0:
            day_hour += 24.0
        day_fraction = day_hour / 12.0  # 0.0 to 1.0 during daytime

        if day_fraction < 1.0 / 3.0:
            return 60.0 if planet == "Mercury" else 0.0
        elif day_fraction < 2.0 / 3.0:
            return 60.0 if planet == "Sun" else 0.0
        else:
            return 60.0 if planet == "Saturn" else 0.0
    else:
        # Night: 18:00-06:00 -> 3 parts of 4 hours each
        night_hour = hour - 18.0
        if night_hour < 0:
            night_hour += 24.0
        night_fraction = night_hour / 12.0

        if night_fraction < 1.0 / 3.0:
            return 60.0 if planet == "Moon" else 0.0
        elif night_fraction < 2.0 / 3.0:
            return 60.0 if planet == "Venus" else 0.0
        else:
            return 60.0 if planet == "Mars" else 0.0


def _abda_bala(planet: str, birth_year: int) -> float:
    """Year lord gets 15 Virupas. Simplified: cycle through year lords."""
    # Kali Yuga year lord cycle: epoch-based approximation
    # A common method: year lord = planet at index (year % 7) in cycle
    idx = birth_year % 7
    year_lord = _YEAR_LORD_CYCLE[idx]
    return 15.0 if planet == year_lord else 0.0


def _masa_bala(planet: str, birth_month: int) -> float:
    """Month lord gets 30 Virupas. Simplified: cycle through month lords."""
    idx = (birth_month - 1) % 7
    month_lord = _MONTH_LORD_CYCLE[idx]
    return 30.0 if planet == month_lord else 0.0


def _vara_bala(planet: str, weekday: int) -> float:
    """Day lord gets 45 Virupas. weekday: Python weekday (Monday=0..Sunday=6)."""
    day_lord = _WEEKDAY_LORD.get(weekday)
    return 45.0 if planet == day_lord else 0.0


def _kala_bala(
    planet: str,
    is_daytime: bool,
    birth_hour: float,
    moon_sun_elongation: float,
    weekday: int = 0,
    birth_year: int = 2000,
    birth_month: int = 1,
) -> Dict[str, float]:
    """
    Total Kala Bala = Nathonnatha + Paksha + Tribhaga + Abda + Masa + Vara.
    Returns dict with breakdown and total.
    """
    nathonnatha = _nathonnatha_bala(planet, birth_hour)
    paksha = _paksha_bala(planet, moon_sun_elongation)
    tribhaga = _tribhaga_bala(planet, birth_hour, is_daytime)
    abda = _abda_bala(planet, birth_year)
    masa = _masa_bala(planet, birth_month)
    vara = _vara_bala(planet, weekday)

    total = round(nathonnatha + paksha + tribhaga + abda + masa + vara, 2)
    return {
        "nathonnatha": nathonnatha,
        "paksha": paksha,
        "tribhaga": tribhaga,
        "abda": abda,
        "masa": masa,
        "vara": vara,
        "total": total,
    }


# ============================================================
# 4. CHESHTA BALA (Motional Strength)
# ============================================================

# Average daily speeds (degrees/day) for planets
_AVG_DAILY_SPEED: Dict[str, float] = {
    "Mars": 0.524,
    "Mercury": 1.383,
    "Jupiter": 0.083,
    "Venus": 1.2,
    "Saturn": 0.034,
}


def _cheshta_bala(
    planet: str,
    is_retrograde: bool = False,
    planet_speed: Optional[float] = None,
) -> float:
    """
    Motional strength.
    Sun and Moon don't get Cheshta Bala (Sun uses Ayana Bala via Paksha;
    Moon uses Paksha Bala). We assign 0 for them here — their strength
    comes from other components.
    Retrograde = 60, Stationary (speed < 0.1 * avg) = 45,
    Normal direct = 30, Fast (speed > 1.5 * avg) = 15.
    """
    if planet in ("Sun", "Moon"):
        return 0.0

    if is_retrograde:
        return 60.0

    avg = _AVG_DAILY_SPEED.get(planet, 0.5)
    if planet_speed is not None:
        abs_speed = abs(planet_speed)
        if abs_speed < 0.1 * avg:
            return 45.0  # stationary
        elif abs_speed > 1.5 * avg:
            return 15.0  # fast
    return 30.0  # normal direct


# ============================================================
# 5. NAISARGIKA BALA (Natural Strength)
# ============================================================

_NAISARGIKA: Dict[str, float] = {
    "Sun": 60.0, "Moon": 51.43, "Mars": 17.14,
    "Mercury": 25.71, "Jupiter": 34.29, "Venus": 42.86, "Saturn": 8.57,
}


def _naisargika_bala(planet: str) -> float:
    """Natural (innate) strength — fixed values."""
    return _NAISARGIKA.get(planet, 0.0)


# ============================================================
# 6. DRIK BALA (Aspectual Strength)
# ============================================================

_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
_MALEFICS = {"Sun", "Mars", "Saturn"}


def _aspect_strength(aspecting_planet: str, house_distance: int) -> float:
    """
    Return aspect strength in Virupas for a given house distance (1-12).
    Full (7th house) aspect = 60 for all planets.
    Mars special: 4th and 8th = 45.
    Jupiter special: 5th and 9th = 45.
    Saturn special: 3rd and 10th = 45.
    All other distances = 0 (no aspect).
    """
    if house_distance == 7:
        return 60.0

    if aspecting_planet == "Mars" and house_distance in (4, 8):
        return 45.0
    if aspecting_planet == "Jupiter" and house_distance in (5, 9):
        return 45.0
    if aspecting_planet == "Saturn" and house_distance in (3, 10):
        return 45.0

    return 0.0


def _drik_bala(planet: str, planet_houses: Dict[str, int]) -> float:
    """
    Aspectual strength.  For each other planet aspecting this planet's house:
    benefic aspect adds strength, malefic aspect subtracts.
    """
    if planet not in planet_houses:
        return 0.0
    planet_house = planet_houses[planet]
    total = 0.0

    for other, other_house in planet_houses.items():
        if other == planet:
            continue
        if other not in _SHADBALA_PLANETS:
            continue  # skip Rahu/Ketu for Drik Bala

        # House distance from aspecting planet to target planet's house
        # _aspect_strength expects 1-based distance (1..12), so add 1 to the
        # 0-based modular result, mapping 0→12 (conjunction, no standard aspect).
        dist = ((planet_house - other_house) % 12) or 12

        strength = _aspect_strength(other, dist)
        if strength > 0:
            if other in _BENEFICS:
                total += strength
            elif other in _MALEFICS:
                total -= strength

    return round(total, 2)


# ============================================================
# PUBLIC API
# ============================================================

def calculate_shadbala(
    planet_signs: Dict[str, str],
    planet_houses: Dict[str, int],
    is_daytime: bool = True,
    retrograde_planets: Set[str] = None,
    planet_longitudes: Dict[str, float] = None,
    birth_hour: float = 12.0,
    moon_sun_elongation: float = 0.0,
    weekday: int = 0,
    birth_year: int = 2000,
    birth_month: int = 1,
    planet_speeds: Dict[str, float] = None,
) -> Dict[str, Any]:
    """
    Calculate full classical Shadbala for the 7 Vedic planets.

    Args:
        planet_signs:        {planet: sign_name}
        planet_houses:       {planet: house_number}  (1-indexed)
        is_daytime:          True if birth was during daytime (6-18h)
        retrograde_planets:  set of planet names that are retrograde
        planet_longitudes:   {planet: sidereal_longitude_0_360}  for Uchcha Bala
        birth_hour:          decimal hour (0-24) for Nathonnatha / Tribhaga
        moon_sun_elongation: Moon longitude minus Sun longitude (mod 360) for Paksha Bala
        weekday:             Python weekday (Monday=0 .. Sunday=6) for Vara Bala
        birth_year:          year of birth for Abda Bala
        birth_month:         month of birth (1-12) for Masa Bala
        planet_speeds:       {planet: daily_speed_degrees} for Cheshta Bala refinement

    Returns:
        {"planets": {planet: {sthana, dig, kala, cheshta, naisargika, drik,
                              total, required, ratio, is_strong}}}
    """
    if retrograde_planets is None:
        retrograde_planets = set()
    if planet_longitudes is None:
        planet_longitudes = {}
    if planet_speeds is None:
        planet_speeds = {}

    planets_result: Dict[str, Dict[str, Any]] = {}

    for planet in _SHADBALA_PLANETS:
        sign = planet_signs.get(planet, "Aries")
        house = planet_houses.get(planet, 1)
        is_retro = planet in retrograde_planets
        lon = planet_longitudes.get(planet)
        speed = planet_speeds.get(planet)

        # 1. Sthana Bala (5 sub-components)
        sthana_detail = _sthana_bala(planet, sign, house, lon)
        sthana = sthana_detail["total"]

        # 2. Dig Bala
        dig = _dig_bala(planet, house)

        # 3. Kala Bala (6 sub-components)
        kala_detail = _kala_bala(
            planet, is_daytime, birth_hour, moon_sun_elongation,
            weekday=weekday, birth_year=birth_year, birth_month=birth_month,
        )
        kala = kala_detail["total"]

        # 4. Cheshta Bala
        cheshta = _cheshta_bala(planet, is_retro, speed)

        # 5. Naisargika Bala
        naisargika = _naisargika_bala(planet)

        # 6. Drik Bala
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
            # Sub-component breakdowns for detailed display
            "sthana_detail": sthana_detail,
            "kala_detail": kala_detail,
        }

    return {"planets": planets_result}
