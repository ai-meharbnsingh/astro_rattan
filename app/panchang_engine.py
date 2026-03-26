"""
panchang_engine.py -- Vedic Panchang (Hindu Calendar) Engine
=============================================================
Calculates the five limbs of panchang: Tithi, Nakshatra, Yoga, Karana.
Also provides Rahu Kaal and Choghadiya calculations.

Falls back to pure-math approximations when swisseph is not installed.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple

# ---------- Try swisseph ----------
try:
    import swisseph as swe
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

# We reuse helpers from astro_engine for astronomical calculations
from app.astro_engine import (
    _approx_sun_longitude,
    _approx_moon_longitude,
    _approx_ayanamsa,
    _datetime_to_jd,
    _parse_datetime,
    get_nakshatra_from_longitude,
)

# ============================================================
# TITHIS -- 30 tithis in a lunar month
# ============================================================
TITHIS: List[Dict[str, Any]] = [
    {"number": 1,  "name": "Pratipada",    "paksha": "Shukla"},
    {"number": 2,  "name": "Dwitiya",      "paksha": "Shukla"},
    {"number": 3,  "name": "Tritiya",      "paksha": "Shukla"},
    {"number": 4,  "name": "Chaturthi",    "paksha": "Shukla"},
    {"number": 5,  "name": "Panchami",     "paksha": "Shukla"},
    {"number": 6,  "name": "Shashthi",     "paksha": "Shukla"},
    {"number": 7,  "name": "Saptami",      "paksha": "Shukla"},
    {"number": 8,  "name": "Ashtami",      "paksha": "Shukla"},
    {"number": 9,  "name": "Navami",       "paksha": "Shukla"},
    {"number": 10, "name": "Dashami",      "paksha": "Shukla"},
    {"number": 11, "name": "Ekadashi",     "paksha": "Shukla"},
    {"number": 12, "name": "Dwadashi",     "paksha": "Shukla"},
    {"number": 13, "name": "Trayodashi",   "paksha": "Shukla"},
    {"number": 14, "name": "Chaturdashi",  "paksha": "Shukla"},
    {"number": 15, "name": "Purnima",      "paksha": "Shukla"},
    {"number": 16, "name": "Pratipada",    "paksha": "Krishna"},
    {"number": 17, "name": "Dwitiya",      "paksha": "Krishna"},
    {"number": 18, "name": "Tritiya",      "paksha": "Krishna"},
    {"number": 19, "name": "Chaturthi",    "paksha": "Krishna"},
    {"number": 20, "name": "Panchami",     "paksha": "Krishna"},
    {"number": 21, "name": "Shashthi",     "paksha": "Krishna"},
    {"number": 22, "name": "Saptami",      "paksha": "Krishna"},
    {"number": 23, "name": "Ashtami",      "paksha": "Krishna"},
    {"number": 24, "name": "Navami",       "paksha": "Krishna"},
    {"number": 25, "name": "Dashami",      "paksha": "Krishna"},
    {"number": 26, "name": "Ekadashi",     "paksha": "Krishna"},
    {"number": 27, "name": "Dwadashi",     "paksha": "Krishna"},
    {"number": 28, "name": "Trayodashi",   "paksha": "Krishna"},
    {"number": 29, "name": "Chaturdashi",  "paksha": "Krishna"},
    {"number": 30, "name": "Amavasya",     "paksha": "Krishna"},
]

# ============================================================
# YOGAS -- 27 yogas
# ============================================================
YOGAS: List[str] = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

# ============================================================
# KARANAS -- 11 karana types (cycle: 7 repeating + 4 fixed)
# ============================================================
_REPEATING_KARANAS: List[str] = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",
]
_FIXED_KARANAS: List[str] = [
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]

KARANAS: List[str] = _REPEATING_KARANAS + _FIXED_KARANAS


# ============================================================
# RAHU KAAL timing by weekday
# ============================================================
# Rahu Kaal slot number (1-8) for each weekday (0=Monday ... 6=Sunday)
# Slot 1 = first 1/8 of daytime, Slot 2 = second 1/8, etc.
_RAHU_KAAL_SLOT = {
    0: 2,  # Monday
    1: 7,  # Tuesday
    2: 5,  # Wednesday
    3: 6,  # Thursday
    4: 4,  # Friday
    5: 3,  # Saturday
    6: 8,  # Sunday
}


# ============================================================
# CHOGHADIYA -- Planetary periods
# ============================================================
_DAY_CHOGHADIYA_NAMES = {
    0: ["Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit"],   # Monday
    1: ["Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],     # Tuesday
    2: ["Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh"],    # Wednesday
    3: ["Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh"],   # Thursday
    4: ["Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char"],    # Friday
    5: ["Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal"],    # Saturday
    6: ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],   # Sunday
}

_CHOGHADIYA_QUALITY = {
    "Amrit": "Best",
    "Shubh": "Good",
    "Labh": "Good",
    "Char": "Neutral",
    "Rog": "Inauspicious",
    "Kaal": "Inauspicious",
    "Udveg": "Inauspicious",
}


# ============================================================
# SUNRISE / SUNSET approximation
# ============================================================

def _approx_sunrise_sunset(
    date_str: str, latitude: float, longitude: float,
) -> Tuple[str, str]:
    """
    Approximate sunrise and sunset times for a given date and location.
    Returns (sunrise_str, sunset_str) in "HH:MM" local solar time.
    """
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

    # Day of year
    dt = datetime(year, month, day)
    doy = dt.timetuple().tm_yday

    # Solar declination (approximate)
    declination = 23.45 * math.sin(math.radians(360.0 / 365.0 * (doy - 81)))
    dec_rad = math.radians(declination)
    lat_rad = math.radians(latitude)

    # Hour angle at sunrise/sunset
    cos_ha = -math.tan(lat_rad) * math.tan(dec_rad)
    cos_ha = max(-1.0, min(1.0, cos_ha))  # Clamp for polar regions
    ha = math.degrees(math.acos(cos_ha))

    # Sunrise/sunset in hours from solar noon (12:00 local solar time)
    # Equation of time (approximate)
    b_val = math.radians(360.0 / 365.0 * (doy - 81))
    eot = 9.87 * math.sin(2 * b_val) - 7.53 * math.cos(b_val) - 1.5 * math.sin(b_val)

    # Solar noon in local time (minutes from midnight)
    # Assuming longitude already provides local solar time offset
    solar_noon_minutes = 720  # 12:00 in minutes

    sunrise_minutes = solar_noon_minutes - (ha / 360.0) * 24 * 60
    sunset_minutes = solar_noon_minutes + (ha / 360.0) * 24 * 60

    sunrise_h = int(sunrise_minutes // 60)
    sunrise_m = int(sunrise_minutes % 60)
    sunset_h = int(sunset_minutes // 60)
    sunset_m = int(sunset_minutes % 60)

    return f"{sunrise_h:02d}:{sunrise_m:02d}", f"{sunset_h:02d}:{sunset_m:02d}"


# ============================================================
# PUBLIC: calculate_panchang
# ============================================================

def calculate_panchang(
    date: str, latitude: float, longitude: float,
) -> Dict[str, Any]:
    """
    Calculate Panchang (Hindu calendar elements) for a given date and location.

    Args:
        date:       ISO date "YYYY-MM-DD"
        latitude:   Location latitude
        longitude:  Location longitude

    Returns:
        {
            tithi: {name, number, paksha},
            nakshatra: {name, pada, lord},
            yoga: {name, number},
            karana: {name, number},
            sunrise: "HH:MM",
            sunset: "HH:MM",
        }
    """
    sunrise_str, sunset_str = _approx_sunrise_sunset(date, latitude, longitude)

    # We need Sun and Moon longitudes at sunrise for panchang calculations
    # Parse sunrise time for the given date
    dt_utc = _parse_datetime(date, sunrise_str, longitude / 15.0)  # approx tz from longitude
    jd = _datetime_to_jd(dt_utc)

    if _HAS_SWE:
        sun_lon, moon_lon = _get_sun_moon_swe(jd)
    else:
        sun_lon = _approx_sun_longitude(jd)
        moon_lon = _approx_moon_longitude(jd)

    ayanamsa = _approx_ayanamsa(jd)
    sun_sid = (sun_lon - ayanamsa) % 360.0
    moon_sid = (moon_lon - ayanamsa) % 360.0

    # Tithi: based on elongation of Moon from Sun
    elongation = (moon_lon - sun_lon) % 360.0
    tithi_index = int(elongation / 12.0)
    if tithi_index >= 30:
        tithi_index = 29
    tithi = TITHIS[tithi_index]

    # Nakshatra: Moon's sidereal position
    nakshatra = get_nakshatra_from_longitude(moon_sid)

    # Yoga: (Sun sidereal + Moon sidereal) / (800/60 = 13.333...)
    yoga_sum = (sun_sid + moon_sid) % 360.0
    yoga_index = int(yoga_sum / YOGA_SPAN)
    if yoga_index >= 27:
        yoga_index = 26
    yoga_name = YOGAS[yoga_index]

    # Karana: half-tithi
    karana_index = _get_karana_index(tithi_index)
    karana_name = _get_karana_name(karana_index)

    return {
        "tithi": {
            "name": tithi["name"],
            "number": tithi["number"],
            "paksha": tithi["paksha"],
        },
        "nakshatra": nakshatra,
        "yoga": {"name": yoga_name, "number": yoga_index + 1},
        "karana": {"name": karana_name, "number": karana_index + 1},
        "sunrise": sunrise_str,
        "sunset": sunset_str,
    }


YOGA_SPAN = 360.0 / 27.0  # ~13.3333 degrees


def _get_sun_moon_swe(jd: float) -> Tuple[float, float]:
    """Get tropical Sun and Moon longitudes via swisseph."""
    sun_pos, _ = swe.calc_ut(jd, 0)  # SE_SUN
    moon_pos, _ = swe.calc_ut(jd, 1)  # SE_MOON
    return sun_pos[0], moon_pos[0]


def _get_karana_index(tithi_index: int) -> int:
    """
    Get karana number (0-59) from tithi index (0-29).
    Each tithi has 2 karanas. We return the first karana of the tithi.
    Karanas cycle: first half of Pratipada Shukla = Kimstughna (fixed),
    then 7 repeating karanas cycle, then last 3 fixed at end.
    """
    half_tithi = tithi_index * 2
    return half_tithi % 60


def _get_karana_name(karana_index: int) -> str:
    """
    Map a karana index (0-59) to its name.
    Karana 0 = Kimstughna (fixed)
    Karanas 1-56 cycle through 7 repeating (Bava..Vishti) = 8 full cycles
    Karana 57 = Shakuni, 58 = Chatushpada, 59 = Naga
    """
    if karana_index == 0:
        return "Kimstughna"
    if karana_index >= 57:
        fixed_map = {57: "Shakuni", 58: "Chatushpada", 59: "Naga"}
        return fixed_map.get(karana_index, "Kimstughna")
    # Repeating karanas (1-56 -> index into 7 repeating)
    return _REPEATING_KARANAS[(karana_index - 1) % 7]


# ============================================================
# PUBLIC: calculate_rahu_kaal
# ============================================================

def calculate_rahu_kaal(
    weekday: int, sunrise: str, sunset: str,
) -> Dict[str, str]:
    """
    Calculate Rahu Kaal period for a given weekday.

    Args:
        weekday:  0=Monday, 1=Tuesday, ..., 6=Sunday
        sunrise:  "HH:MM"
        sunset:   "HH:MM"

    Returns: {start: "HH:MM", end: "HH:MM"}
    """
    sr_minutes = _time_to_minutes(sunrise)
    ss_minutes = _time_to_minutes(sunset)
    day_duration = ss_minutes - sr_minutes

    slot = _RAHU_KAAL_SLOT.get(weekday, 1)
    slot_duration = day_duration / 8.0

    start_minutes = sr_minutes + (slot - 1) * slot_duration
    end_minutes = start_minutes + slot_duration

    return {
        "start": _minutes_to_time(start_minutes),
        "end": _minutes_to_time(end_minutes),
    }


# ============================================================
# PUBLIC: calculate_choghadiya
# ============================================================

def calculate_choghadiya(
    weekday: int, sunrise: str, sunset: str,
) -> List[Dict[str, Any]]:
    """
    Calculate Choghadiya (auspicious time periods) for daytime.

    Args:
        weekday:  0=Monday, 1=Tuesday, ..., 6=Sunday
        sunrise:  "HH:MM"
        sunset:   "HH:MM"

    Returns: list of {name, quality, start, end}
    """
    sr_minutes = _time_to_minutes(sunrise)
    ss_minutes = _time_to_minutes(sunset)
    day_duration = ss_minutes - sr_minutes
    slot_duration = day_duration / 8.0

    names = _DAY_CHOGHADIYA_NAMES.get(weekday, _DAY_CHOGHADIYA_NAMES[0])
    result = []
    for i, name in enumerate(names):
        start = sr_minutes + i * slot_duration
        end = start + slot_duration
        result.append(
            {
                "name": name,
                "quality": _CHOGHADIYA_QUALITY.get(name, "Unknown"),
                "start": _minutes_to_time(start),
                "end": _minutes_to_time(end),
            }
        )
    return result


# ============================================================
# INTERNAL: time helpers
# ============================================================

def _time_to_minutes(time_str: str) -> float:
    """Convert "HH:MM" to minutes from midnight."""
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(minutes: float) -> str:
    """Convert minutes from midnight to "HH:MM"."""
    h = int(minutes // 60) % 24
    m = int(minutes % 60)
    return f"{h:02d}:{m:02d}"
