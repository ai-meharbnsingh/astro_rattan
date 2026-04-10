"""
panchang_engine.py -- Production-Grade Vedic Panchang Engine
=============================================================
Swiss Ephemeris-powered panchang with accurate calculations for:
- Tithi, Nakshatra, Yoga, Karana with end times (binary search)
- Sunrise/Sunset/Moonrise/Moonset via Swiss Ephemeris
- Planetary positions (Navgraha) with Rashi
- Rahu Kaal, Gulika Kaal, Yamaganda Kaal
- Auspicious timings (Abhijit Muhurat, Brahma Muhurat)
- Hindu calendar (Vikram/Shaka Samvat, Maas, Ritu, Ayana)
- Choghadiya periods
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------- Try swisseph ----------
try:
    import swisseph as swe
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

from app.astro_engine import (
    _approx_sun_longitude,
    _approx_moon_longitude,
    _approx_ayanamsa,
    _datetime_to_jd,
    _parse_datetime,
    get_nakshatra_from_longitude,
    get_sign_from_longitude,
    PLANETS as PLANET_IDS,
    SE_SUN,
    SE_MOON,
    SE_MEAN_NODE,
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

YOGA_SPAN = 360.0 / 27.0  # ~13.3333 degrees

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
# RAHU KAAL / GULIKA / YAMAGANDA timing by weekday
# ============================================================
# Slot number (1-8) for each weekday (0=Monday ... 6=Sunday)
_RAHU_KAAL_SLOT = {
    0: 2,  # Monday
    1: 7,  # Tuesday
    2: 5,  # Wednesday
    3: 6,  # Thursday
    4: 4,  # Friday
    5: 3,  # Saturday
    6: 8,  # Sunday
}

_GULIKA_KAAL_SLOT = {
    0: 6,  # Monday
    1: 5,  # Tuesday
    2: 4,  # Wednesday
    3: 3,  # Thursday
    4: 2,  # Friday
    5: 1,  # Saturday
    6: 7,  # Sunday
}

_YAMAGANDA_SLOT = {
    0: 4,  # Monday
    1: 3,  # Tuesday
    2: 2,  # Wednesday
    3: 1,  # Thursday
    4: 6,  # Friday
    5: 5,  # Saturday
    6: 8,  # Sunday (some traditions say 5)
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
# HINDU MONTH NAMES
# ============================================================
_HINDU_MONTHS = [
    "Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
    "Shravana", "Bhadrapada", "Ashwin", "Kartik",
    "Margashirsha", "Pausha", "Magha", "Phalguna",
]

_RITU = [
    ("Vasanta", "Spring"),    # Chaitra-Vaishakha
    ("Grishma", "Summer"),    # Jyeshtha-Ashadha
    ("Varsha", "Monsoon"),    # Shravana-Bhadrapada
    ("Sharad", "Autumn"),     # Ashwin-Kartik
    ("Hemanta", "Pre-winter"), # Margashirsha-Pausha
    ("Shishira", "Winter"),   # Magha-Phalguna
]

_AYANA = ["Uttarayana", "Dakshinayana"]

# ============================================================
# VAAR (Weekday) NAMES
# ============================================================
_VAAR_NAMES = [
    "Somvar",   # Monday
    "Mangalvar", # Tuesday
    "Budhvar",   # Wednesday
    "Guruvar",   # Thursday
    "Shukravar", # Friday
    "Shanivar",  # Saturday
    "Ravivar",   # Sunday
]

_VAAR_ENGLISH = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


# ============================================================
# SUNRISE / SUNSET via Swiss Ephemeris or NOAA fallback
# ============================================================

def _swe_sunrise_sunset(date_str: str, latitude: float, longitude: float) -> Tuple[float, float, float, float]:
    """
    Compute sunrise, sunset, moonrise, moonset using Swiss Ephemeris.
    Returns (sunrise_jd, sunset_jd, moonrise_jd, moonset_jd).
    """
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    jd_start = swe.julday(year, month, day, 0.0)

    # Sunrise (upper limb, atmospheric refraction)
    try:
        sunrise_jd = swe.rise_trans(
            jd_start, swe.SUN, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        sunrise_jd = jd_start + 0.25  # fallback ~6 AM

    try:
        sunset_jd = swe.rise_trans(
            jd_start, swe.SUN, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        sunset_jd = jd_start + 0.75  # fallback ~6 PM

    try:
        moonrise_jd = swe.rise_trans(
            jd_start, swe.MOON, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        moonrise_jd = 0.0

    try:
        moonset_jd = swe.rise_trans(
            jd_start, swe.MOON, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        moonset_jd = 0.0

    return sunrise_jd, sunset_jd, moonrise_jd, moonset_jd


def _jd_to_local_time_str(jd: float, tz_hours: float) -> str:
    """Convert JD to local HH:MM string."""
    if jd == 0.0:
        return "--:--"
    # Convert JD to UTC components
    ut_hours = (jd - int(jd) - 0.5) * 24.0
    if ut_hours < 0:
        ut_hours += 24.0
    local_hours = ut_hours + tz_hours
    if local_hours >= 24:
        local_hours -= 24
    elif local_hours < 0:
        local_hours += 24
    h = int(local_hours)
    m = int((local_hours - h) * 60)
    return f"{h:02d}:{m:02d}"


def _approx_sunrise_sunset(
    date_str: str, latitude: float, longitude: float,
) -> Tuple[str, str]:
    """
    Approximate sunrise and sunset times for a given date and location.
    Returns (sunrise_str, sunset_str) in "HH:MM" local solar time.
    """
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

    dt = datetime(year, month, day)
    doy = dt.timetuple().tm_yday

    declination = 23.45 * math.sin(math.radians(360.0 / 365.0 * (doy - 81)))
    dec_rad = math.radians(declination)
    lat_rad = math.radians(latitude)

    cos_ha = -math.tan(lat_rad) * math.tan(dec_rad)
    cos_ha = max(-1.0, min(1.0, cos_ha))
    ha = math.degrees(math.acos(cos_ha))

    b_val = math.radians(360.0 / 365.0 * (doy - 81))
    eot = 9.87 * math.sin(2 * b_val) - 7.53 * math.cos(b_val) - 1.5 * math.sin(b_val)

    solar_noon_minutes = 720
    sunrise_minutes = solar_noon_minutes - (ha / 360.0) * 24 * 60
    sunset_minutes = solar_noon_minutes + (ha / 360.0) * 24 * 60

    sunrise_h = int(sunrise_minutes // 60)
    sunrise_m = int(sunrise_minutes % 60)
    sunset_h = int(sunset_minutes // 60)
    sunset_m = int(sunset_minutes % 60)

    return f"{sunrise_h:02d}:{sunrise_m:02d}", f"{sunset_h:02d}:{sunset_m:02d}"


def _compute_sun_times(date_str: str, latitude: float, longitude: float, tz_offset: float = None) -> Dict[str, str]:
    """
    Compute sunrise, sunset, moonrise, moonset.
    Uses Swiss Ephemeris if available, otherwise NOAA approximation.
    Returns dict with sunrise, sunset, moonrise, moonset as HH:MM strings.
    """
    if tz_offset is None:
        tz_offset = 5.5 if 68.0 <= longitude <= 97.5 else round(longitude / 15.0 * 2) / 2

    if _HAS_SWE:
        try:
            sr_jd, ss_jd, mr_jd, ms_jd = _swe_sunrise_sunset(date_str, latitude, longitude)
            return {
                "sunrise": _jd_to_local_time_str(sr_jd, tz_offset),
                "sunset": _jd_to_local_time_str(ss_jd, tz_offset),
                "moonrise": _jd_to_local_time_str(mr_jd, tz_offset),
                "moonset": _jd_to_local_time_str(ms_jd, tz_offset),
            }
        except Exception:
            pass

    sr, ss = _approx_sunrise_sunset(date_str, latitude, longitude)
    # Approximate moonrise/moonset
    sr_min = _time_to_minutes(sr)
    return {
        "sunrise": sr,
        "sunset": ss,
        "moonrise": _minutes_to_time(sr_min + 50),
        "moonset": _minutes_to_time(_time_to_minutes(ss) + 50),
    }


# ============================================================
# ASTRONOMICAL COMPUTATIONS -- Sun/Moon longitudes at a given JD
# ============================================================

def _get_sun_moon_swe(jd: float) -> Tuple[float, float]:
    """Get tropical Sun and Moon longitudes via swisseph."""
    sun_pos, _ = swe.calc_ut(jd, 0)  # SE_SUN
    moon_pos, _ = swe.calc_ut(jd, 1)  # SE_MOON
    return sun_pos[0], moon_pos[0]


def _get_sidereal_longitudes(jd: float) -> Tuple[float, float, float]:
    """Return (sun_sid, moon_sid, ayanamsa) at given JD."""
    if _HAS_SWE:
        sun_lon, moon_lon = _get_sun_moon_swe(jd)
        ayanamsa = swe.get_ayanamsa(jd)
    else:
        sun_lon = _approx_sun_longitude(jd)
        moon_lon = _approx_moon_longitude(jd)
        ayanamsa = _approx_ayanamsa(jd)
    sun_sid = (sun_lon - ayanamsa) % 360.0
    moon_sid = (moon_lon - ayanamsa) % 360.0
    return sun_sid, moon_sid, ayanamsa


def _get_elongation(jd: float) -> float:
    """Get Moon-Sun elongation (0-360) at given JD. Used for tithi/karana."""
    if _HAS_SWE:
        sun_lon, moon_lon = _get_sun_moon_swe(jd)
    else:
        sun_lon = _approx_sun_longitude(jd)
        moon_lon = _approx_moon_longitude(jd)
    return (moon_lon - sun_lon) % 360.0


def _get_moon_longitude_sidereal(jd: float) -> float:
    """Get sidereal Moon longitude. Used for nakshatra boundary detection."""
    if _HAS_SWE:
        moon_pos, _ = swe.calc_ut(jd, 1)
        ayanamsa = swe.get_ayanamsa(jd)
        return (moon_pos[0] - ayanamsa) % 360.0
    else:
        moon_lon = _approx_moon_longitude(jd)
        ayanamsa = _approx_ayanamsa(jd)
        return (moon_lon - ayanamsa) % 360.0


def _get_yoga_angle(jd: float) -> float:
    """Get (Sun_sid + Moon_sid) % 360. Used for yoga boundary detection."""
    sun_sid, moon_sid, _ = _get_sidereal_longitudes(jd)
    return (sun_sid + moon_sid) % 360.0


# ============================================================
# END TIME CALCULATIONS -- Binary search for boundary crossings
# ============================================================

def _find_boundary_time(
    jd_start: float,
    angle_func,
    boundary_degree: float,
    span: float,
    max_hours: float = 30.0,
    tolerance_minutes: float = 0.5,
) -> Optional[float]:
    """
    Binary search to find when angle_func(jd) crosses boundary_degree.
    Returns JD of crossing, or None if not found within max_hours.

    angle_func: callable(jd) -> float (0-360)
    boundary_degree: the target boundary value
    span: the span of one unit (12 for tithi, 13.333 for nakshatra, etc.)
    """
    jd_end = jd_start + max_hours / 24.0
    step = 1.0 / 24.0  # 1 hour steps for coarse scan

    # Determine which unit we are in at start
    start_val = angle_func(jd_start)
    start_index = int(start_val / span)

    # Coarse scan to find the hour bracket where the boundary is crossed
    jd_a = jd_start
    prev_index = start_index
    found = False

    t = jd_start + step
    while t <= jd_end:
        cur_val = angle_func(t)
        cur_index = int(cur_val / span)
        # Handle wraparound
        if cur_index != prev_index:
            jd_a = t - step
            found = True
            break
        prev_index = cur_index
        t += step

    if not found:
        return None

    # Binary search within [jd_a, jd_a + step]
    jd_lo = jd_a
    jd_hi = jd_a + step
    tol = tolerance_minutes / (24.0 * 60.0)  # convert to JD units

    for _ in range(50):  # max iterations
        if (jd_hi - jd_lo) < tol:
            break
        jd_mid = (jd_lo + jd_hi) / 2.0
        mid_index = int(angle_func(jd_mid) / span)
        if mid_index == start_index:
            jd_lo = jd_mid
        else:
            jd_hi = jd_mid

    return (jd_lo + jd_hi) / 2.0


def _compute_tithi_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current tithi after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_elongation, 0.0, 12.0)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_nakshatra_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current nakshatra after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_moon_longitude_sidereal, 0.0, NAKSHATRA_SPAN)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_yoga_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current yoga after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_yoga_angle, 0.0, YOGA_SPAN)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_karana_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current karana (half-tithi) after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_elongation, 0.0, 6.0)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


NAKSHATRA_SPAN = 360.0 / 27.0  # 13.3333 degrees


# ============================================================
# PLANETARY POSITIONS (NAVGRAHA)
# ============================================================

def calculate_planetary_positions(jd: float) -> List[Dict[str, Any]]:
    """
    Calculate sidereal positions for all 9 Vedic planets (Navgraha).
    Returns list of {name, longitude, degree, rashi, rashi_index}.
    """
    planets = []
    if _HAS_SWE:
        ayanamsa = swe.get_ayanamsa(jd)
        planet_list = [
            ("Sun", 0), ("Moon", 1), ("Mars", 4), ("Mercury", 2),
            ("Jupiter", 5), ("Venus", 3), ("Saturn", 6), ("Rahu", 10),
        ]
        for name, pid in planet_list:
            pos, _ = swe.calc_ut(jd, pid)
            sid_lon = (pos[0] - ayanamsa) % 360.0
            rashi = get_sign_from_longitude(sid_lon)
            planets.append({
                "name": name,
                "longitude": round(sid_lon, 4),
                "degree": round(sid_lon % 30.0, 2),
                "rashi": rashi,
                "rashi_index": int(sid_lon / 30.0),
            })
        # Ketu = Rahu + 180
        rahu_lon = next(p["longitude"] for p in planets if p["name"] == "Rahu")
        ketu_lon = (rahu_lon + 180.0) % 360.0
        planets.append({
            "name": "Ketu",
            "longitude": round(ketu_lon, 4),
            "degree": round(ketu_lon % 30.0, 2),
            "rashi": get_sign_from_longitude(ketu_lon),
            "rashi_index": int(ketu_lon / 30.0),
        })
    else:
        # Fallback -- use approximations from astro_engine
        from app.astro_engine import _approx_planet_longitude, _approx_rahu_longitude
        ayanamsa = _approx_ayanamsa(jd)
        approx_funcs = {
            "Sun": lambda: _approx_sun_longitude(jd),
            "Moon": lambda: _approx_moon_longitude(jd),
            "Mars": lambda: _approx_planet_longitude(jd, "Mars"),
            "Mercury": lambda: _approx_planet_longitude(jd, "Mercury"),
            "Jupiter": lambda: _approx_planet_longitude(jd, "Jupiter"),
            "Venus": lambda: _approx_planet_longitude(jd, "Venus"),
            "Saturn": lambda: _approx_planet_longitude(jd, "Saturn"),
            "Rahu": lambda: _approx_rahu_longitude(jd),
        }
        for name, func in approx_funcs.items():
            trop = func()
            sid_lon = (trop - ayanamsa) % 360.0
            rashi = get_sign_from_longitude(sid_lon)
            planets.append({
                "name": name,
                "longitude": round(sid_lon, 4),
                "degree": round(sid_lon % 30.0, 2),
                "rashi": rashi,
                "rashi_index": int(sid_lon / 30.0),
            })
        rahu_lon = next(p["longitude"] for p in planets if p["name"] == "Rahu")
        ketu_lon = (rahu_lon + 180.0) % 360.0
        planets.append({
            "name": "Ketu",
            "longitude": round(ketu_lon, 4),
            "degree": round(ketu_lon % 30.0, 2),
            "rashi": get_sign_from_longitude(ketu_lon),
            "rashi_index": int(ketu_lon / 30.0),
        })
    return planets


# ============================================================
# RAHU KAAL / GULIKA KAAL / YAMAGANDA KAAL
# ============================================================

def _compute_kaal_period(weekday: int, sunrise: str, sunset: str, slot_map: dict) -> Dict[str, str]:
    """Divide daytime into 8 equal parts and return the slot for the weekday."""
    sr_min = _time_to_minutes(sunrise)
    ss_min = _time_to_minutes(sunset)
    day_duration = ss_min - sr_min
    slot = slot_map.get(weekday, 1)
    slot_duration = day_duration / 8.0
    start_min = sr_min + (slot - 1) * slot_duration
    end_min = start_min + slot_duration
    return {
        "start": _minutes_to_time(start_min),
        "end": _minutes_to_time(end_min),
    }


def calculate_rahu_kaal(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Rahu Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _RAHU_KAAL_SLOT)


def calculate_gulika_kaal(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Gulika Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _GULIKA_KAAL_SLOT)


def calculate_yamaganda(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Yamaganda Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _YAMAGANDA_SLOT)


# ============================================================
# AUSPICIOUS TIMINGS
# ============================================================

def calculate_abhijit_muhurat(sunrise: str, sunset: str) -> Dict[str, str]:
    """
    Abhijit Muhurat: the 8th muhurat of the day (midday window).
    Divide daytime into 15 muhurats; the 8th is Abhijit.
    """
    sr_min = _time_to_minutes(sunrise)
    ss_min = _time_to_minutes(sunset)
    day_duration = ss_min - sr_min
    muhurat_duration = day_duration / 15.0
    start = sr_min + 7 * muhurat_duration
    end = start + muhurat_duration
    return {
        "start": _minutes_to_time(start),
        "end": _minutes_to_time(end),
    }


def calculate_brahma_muhurat(sunrise: str) -> Dict[str, str]:
    """
    Brahma Muhurat: ~1 hour 36 minutes (2 muhurats) before sunrise.
    One muhurat = 48 minutes. Brahma Muhurat = 96 to 48 min before sunrise.
    """
    sr_min = _time_to_minutes(sunrise)
    start = sr_min - 96
    end = sr_min - 48
    if start < 0:
        start += 1440
    if end < 0:
        end += 1440
    return {
        "start": _minutes_to_time(start),
        "end": _minutes_to_time(end),
    }


# ============================================================
# HINDU CALENDAR SYSTEM (Vikram Samvat, Shaka Samvat)
# ============================================================

def _compute_hindu_calendar(date_str: str, tithi_index: int, sun_sid: float) -> Dict[str, Any]:
    """
    Compute Hindu calendar elements.
    - Vikram Samvat = Gregorian year + 57 (approx, adjusted for Chaitra)
    - Shaka Samvat = Gregorian year - 78 (approx)
    - Maas from Sun sidereal longitude (solar month)
    - Paksha from tithi
    - Ritu and Ayana from solar position
    """
    parts = date_str.split("-")
    year = int(parts[0])
    month = int(parts[1])

    # Solar month index (0-11) from Sun sidereal longitude
    solar_month_idx = int(sun_sid / 30.0) % 12
    # Map: Aries=0 -> Chaitra, etc. (Mesh Sankranti starts Chaitra)
    # Traditional: Chaitra starts when Sun enters Pisces/Aries boundary
    maas_index = solar_month_idx  # 0=Mesha->Chaitra
    maas_name = _HINDU_MONTHS[maas_index]

    # Paksha
    paksha = "Shukla" if tithi_index < 15 else "Krishna"

    # Vikram Samvat (starts ~March/April, Chaitra Shukla Pratipada)
    vikram_samvat = year + 57
    if month < 4:  # Before April
        vikram_samvat -= 1

    # Shaka Samvat
    shaka_samvat = year - 78
    if month < 4:
        shaka_samvat -= 1

    # Ritu (season) -- 2 months per ritu
    ritu_index = maas_index // 2
    ritu_name, ritu_english = _RITU[ritu_index]

    # Ayana -- Uttarayana (Capricorn to Gemini = months 9-2), Dakshinayana (Cancer to Sagittarius = 3-8)
    if solar_month_idx >= 9 or solar_month_idx <= 2:
        ayana = _AYANA[0]  # Uttarayana
    else:
        ayana = _AYANA[1]  # Dakshinayana

    return {
        "vikram_samvat": vikram_samvat,
        "shaka_samvat": shaka_samvat,
        "maas": maas_name,
        "paksha": paksha,
        "ritu": ritu_name,
        "ritu_english": ritu_english,
        "ayana": ayana,
    }


# ============================================================
# KARANA HELPERS
# ============================================================

def _get_karana_index(tithi_index: int) -> int:
    """Get karana number (0-59) from tithi index (0-29)."""
    half_tithi = tithi_index * 2
    return half_tithi % 60


def _get_karana_name(karana_index: int) -> str:
    """Map a karana index (0-59) to its name."""
    if karana_index == 0:
        return "Kimstughna"
    if karana_index >= 57:
        fixed_map = {57: "Shakuni", 58: "Chatushpada", 59: "Naga"}
        return fixed_map.get(karana_index, "Kimstughna")
    return _REPEATING_KARANAS[(karana_index - 1) % 7]


# ============================================================
# CHOGHADIYA
# ============================================================

def calculate_choghadiya(
    weekday: int, sunrise: str, sunset: str,
) -> List[Dict[str, Any]]:
    """Calculate Choghadiya (auspicious time periods) for daytime."""
    sr_minutes = _time_to_minutes(sunrise)
    ss_minutes = _time_to_minutes(sunset)
    day_duration = ss_minutes - sr_minutes
    slot_duration = day_duration / 8.0

    names = _DAY_CHOGHADIYA_NAMES.get(weekday, _DAY_CHOGHADIYA_NAMES[0])
    result = []
    for i, name in enumerate(names):
        start = sr_minutes + i * slot_duration
        end = start + slot_duration
        result.append({
            "name": name,
            "quality": _CHOGHADIYA_QUALITY.get(name, "Unknown"),
            "start": _minutes_to_time(start),
            "end": _minutes_to_time(end),
        })
    return result


# ============================================================
# TIME HELPERS
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


# ============================================================
# PUBLIC: calculate_panchang (ENHANCED)
# ============================================================

def calculate_panchang(
    date: str, latitude: float, longitude: float, tz_offset: float = None,
) -> Dict[str, Any]:
    """
    Calculate complete Panchang for a given date and location.

    Returns the original contract keys (tithi, nakshatra, yoga, karana, sunrise, sunset)
    plus extended data for the enhanced UI.
    """
    if tz_offset is None:
        # Default to IST for India, otherwise approximate from longitude
        if 68.0 <= longitude <= 97.5:
            tz_offset = 5.5  # IST
        else:
            tz_offset = round(longitude / 15.0 * 2) / 2  # round to nearest 0.5h

    # 1. Sunrise/Sunset/Moonrise/Moonset
    sun_times = _compute_sun_times(date, latitude, longitude)
    sunrise_str = sun_times["sunrise"]
    sunset_str = sun_times["sunset"]

    # 2. Julian Day at sunrise for panchang calculations
    dt_utc = _parse_datetime(date, sunrise_str, tz_offset)
    jd_sunrise = _datetime_to_jd(dt_utc)

    # 3. Sidereal longitudes at sunrise
    sun_sid, moon_sid, ayanamsa = _get_sidereal_longitudes(jd_sunrise)

    # 4. Elongation for Tithi
    elongation = _get_elongation(jd_sunrise)
    tithi_index = int(elongation / 12.0)
    if tithi_index >= 30:
        tithi_index = 29
    tithi = TITHIS[tithi_index]

    # 5. Nakshatra
    nakshatra = get_nakshatra_from_longitude(moon_sid)

    # 6. Yoga
    yoga_sum = (sun_sid + moon_sid) % 360.0
    yoga_index = int(yoga_sum / YOGA_SPAN)
    if yoga_index >= 27:
        yoga_index = 26
    yoga_name = YOGAS[yoga_index]

    # 7. Karana
    karana_index = _get_karana_index(tithi_index)
    karana_name = _get_karana_name(karana_index)

    # 8. End times via binary search
    tithi_end = _compute_tithi_end(jd_sunrise, tz_offset)
    nakshatra_end = _compute_nakshatra_end(jd_sunrise, tz_offset)
    yoga_end = _compute_yoga_end(jd_sunrise, tz_offset)
    karana_end = _compute_karana_end(jd_sunrise, tz_offset)

    # 9. Weekday / Vaar
    parts = date.split("-")
    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    weekday = dt.weekday()

    # 10. Rahu Kaal, Gulika Kaal, Yamaganda
    rahu_kaal = calculate_rahu_kaal(weekday, sunrise_str, sunset_str)
    gulika_kaal = calculate_gulika_kaal(weekday, sunrise_str, sunset_str)
    yamaganda = calculate_yamaganda(weekday, sunrise_str, sunset_str)

    # 11. Auspicious timings
    abhijit = calculate_abhijit_muhurat(sunrise_str, sunset_str)
    brahma = calculate_brahma_muhurat(sunrise_str)

    # 12. Planetary positions
    planetary_positions = calculate_planetary_positions(jd_sunrise)

    # 13. Hindu calendar
    hindu_calendar = _compute_hindu_calendar(date, tithi_index, sun_sid)

    # 14. Choghadiya
    choghadiya = calculate_choghadiya(weekday, sunrise_str, sunset_str)

    # 15. Next Tithi, Nakshatra, Yoga
    next_tithi_idx = (tithi_index + 1) % 30
    next_tithi = TITHIS[next_tithi_idx]
    next_nakshatra_idx = (nakshatra.get("index", 0) + 1) % 27
    from app.astro_engine import NAKSHATRAS
    next_nak_name = NAKSHATRAS[next_nakshatra_idx]["name"] if next_nakshatra_idx < len(NAKSHATRAS) else ""
    next_yoga_idx = (yoga_index + 1) % 27
    next_yoga_name = YOGAS[next_yoga_idx] if next_yoga_idx < len(YOGAS) else ""

    # 16. Second Karana
    second_karana_idx = _get_karana_index(tithi_index) + 1
    if second_karana_idx >= 60:
        second_karana_idx = 0
    second_karana_name = _get_karana_name(second_karana_idx)

    # 17. Sun sign + Moon sign
    sun_sign = get_sign_from_longitude(sun_sid)
    moon_sign = get_sign_from_longitude(moon_sid)

    # 18. Dinamana / Ratrimana / Madhyahna
    sunrise_mins = _time_to_minutes(sunrise_str)
    sunset_mins = _time_to_minutes(sunset_str)
    dinamana_mins = sunset_mins - sunrise_mins
    ratrimana_mins = 1440 - dinamana_mins
    madhyahna_mins = sunrise_mins + dinamana_mins / 2
    dinamana_str = f"{int(dinamana_mins // 60)} Hours {int(dinamana_mins % 60)} Mins"
    ratrimana_str = f"{int(ratrimana_mins // 60)} Hours {int(ratrimana_mins % 60)} Mins"
    madhyahna_str = _minutes_to_time(madhyahna_mins)

    # 19. Additional Muhurtas
    day_duration_mins = dinamana_mins
    muhurta_duration = day_duration_mins / 15  # each muhurta = 1/15th of day

    # Godhuli Muhurta: ~24 min around sunset
    godhuli = {"start": _minutes_to_time(sunset_mins - 24), "end": _minutes_to_time(sunset_mins)}
    # Sayahna Sandhya: sunset to sunset+48min
    sayahna = {"start": sunset_str, "end": _minutes_to_time(sunset_mins + 48)}
    # Nishita Muhurta: midnight ± 24min
    midnight_mins = sunset_mins + ratrimana_mins / 2
    nishita = {"start": _minutes_to_time(midnight_mins - 24), "end": _minutes_to_time(midnight_mins + 24)}
    # Pratah Sandhya: sunrise-48min to sunrise
    pratah = {"start": _minutes_to_time(sunrise_mins - 48), "end": sunrise_str}
    # Ravi Yoga: sunrise to sunrise + 1/5 of day (first 1/5 of daytime on Sunday)
    ravi_yoga_end = sunrise_mins + day_duration_mins * 3 / 15
    ravi_yoga = {"start": sunrise_str, "end": _minutes_to_time(ravi_yoga_end)}
    # Vijaya Muhurta: 7th muhurta of the day
    vijaya_start = sunrise_mins + muhurta_duration * 6
    vijaya = {"start": _minutes_to_time(vijaya_start), "end": _minutes_to_time(vijaya_start + muhurta_duration)}

    # 20. Dur Muhurtam (8th muhurta on most days)
    dur_start = sunrise_mins + muhurta_duration * 7
    dur_muhurtam = {"start": _minutes_to_time(dur_start), "end": _minutes_to_time(dur_start + muhurta_duration)}

    # 21. Varjyam (inauspicious period based on nakshatra)
    # Simplified: ~1.5 hours, position depends on nakshatra number
    nak_num = nakshatra.get("index", 0) % 9
    varjyam_offset = (nak_num * 2 + 1) * 60  # rough calculation
    varjyam_start = sunrise_mins + varjyam_offset % (dinamana_mins * 0.8)
    varjyam = {"start": _minutes_to_time(varjyam_start), "end": _minutes_to_time(varjyam_start + 90)}

    # 22. Hora Table (planetary hours — 24 horas, day + night)
    hora_sequence_day = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    # Day lord based on weekday
    day_lord_idx = [0, 3, 6, 2, 5, 1, 4][weekday]  # Sun=0(Sun), Mon=3(Moon), Tue=6(Mars)...
    hora_duration_day = dinamana_mins / 12
    hora_duration_night = ratrimana_mins / 12
    hora_table = []
    for i in range(12):
        lord = hora_sequence_day[(day_lord_idx + i) % 7]
        start = _minutes_to_time(sunrise_mins + i * hora_duration_day)
        end = _minutes_to_time(sunrise_mins + (i + 1) * hora_duration_day)
        hora_table.append({"hora": i + 1, "lord": lord, "start": start, "end": end, "type": "day"})
    for i in range(12):
        lord = hora_sequence_day[(day_lord_idx + 12 + i) % 7]
        start = _minutes_to_time(sunset_mins + i * hora_duration_night)
        end = _minutes_to_time(sunset_mins + (i + 1) * hora_duration_night)
        hora_table.append({"hora": i + 13, "lord": lord, "start": start, "end": end, "type": "night"})

    # 23. Lagna Table (Udaya Lagna — rising sign changes through the day)
    lagna_table = []
    _RASHI_NAMES = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    # Approximate: each lagna lasts ~2 hours, starting from ascendant at sunrise
    asc_sign_idx = int(sun_sid / 30) % 12
    for i in range(12):
        sign_idx = (asc_sign_idx + i) % 12
        start = _minutes_to_time(sunrise_mins + i * (1440 / 12))
        end = _minutes_to_time(sunrise_mins + (i + 1) * (1440 / 12))
        lagna_table.append({"lagna": _RASHI_NAMES[sign_idx], "start": start, "end": end})

    # 24. Chandrabalam (Moon strength for each Rashi)
    moon_rashi_idx = int(moon_sid / 30)
    chandrabalam = []
    for i in range(12):
        house_from_moon = ((i - moon_rashi_idx) % 12) + 1
        good = house_from_moon in [1, 3, 6, 7, 10, 11]
        chandrabalam.append({
            "rashi": _RASHI_NAMES[i],
            "house_from_moon": house_from_moon,
            "balam": "Shubh" if good else "Ashubh",
            "good": good,
        })

    # 25. Tarabalam (Star strength for each Nakshatra)
    from app.astro_engine import NAKSHATRAS as _ALL_NAKS
    moon_nak_idx = nakshatra.get("index", 0)
    tarabalam = []
    tara_names = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyari", "Sadhaka", "Vadha", "Mitra", "Ati-Mitra"]
    for i in range(27):
        tara_num = ((i - moon_nak_idx) % 9)
        tara_name = tara_names[tara_num]
        good = tara_name in ["Sampat", "Kshema", "Sadhaka", "Mitra", "Ati-Mitra"]
        tarabalam.append({
            "nakshatra": _ALL_NAKS[i]["name"] if i < len(_ALL_NAKS) else f"Nak-{i+1}",
            "tara": tara_name,
            "tara_number": tara_num + 1,
            "good": good,
        })

    # 26. Gowri Panchangam (8 periods, day + night)
    gowri_names_day = ["Udvega", "Chara", "Labha", "Amruta", "Kaala", "Shubha", "Roga", "Dhanada"]
    gowri_names_night = ["Kaala", "Shubha", "Roga", "Dhanada", "Udvega", "Chara", "Labha", "Amruta"]
    gowri_day_dur = dinamana_mins / 8
    gowri_night_dur = ratrimana_mins / 8
    gowri_panchang = []
    for i in range(8):
        gowri_panchang.append({
            "name": gowri_names_day[(day_lord_idx + i) % 8],
            "start": _minutes_to_time(sunrise_mins + i * gowri_day_dur),
            "end": _minutes_to_time(sunrise_mins + (i + 1) * gowri_day_dur),
            "type": "day",
            "quality": "good" if gowri_names_day[(day_lord_idx + i) % 8] in ["Labha", "Amruta", "Shubha", "Dhanada"] else "bad",
        })
    for i in range(8):
        gowri_panchang.append({
            "name": gowri_names_night[(day_lord_idx + i) % 8],
            "start": _minutes_to_time(sunset_mins + i * gowri_night_dur),
            "end": _minutes_to_time(sunset_mins + (i + 1) * gowri_night_dur),
            "type": "night",
            "quality": "good" if gowri_names_night[(day_lord_idx + i) % 8] in ["Labha", "Amruta", "Shubha", "Dhanada"] else "bad",
        })

    # 27. Do Ghati Muhurta (30 muhurtas in a day)
    total_day_mins = 1440
    ghati_duration = total_day_mins / 30
    do_ghati = []
    muhurta_names_30 = ["Rudra", "Ahi", "Mitra", "Pitru", "Vasu", "Varah", "Vishwadeva", "Vidhi",
                        "Satamukhi", "Puruhuta", "Vahini", "Naktanchara", "Varuna", "Aryaman", "Bhaga",
                        "Girisha", "Ajapada", "Ahirbudhnya", "Pushan", "Ashwini", "Yama", "Agni",
                        "Vidhata", "Chanda", "Aditi", "Jeeva", "Vishnu", "Dyumadgadyuti", "Brahma", "Samudra"]
    for i in range(30):
        start_min = sunrise_mins + i * ghati_duration
        do_ghati.append({
            "muhurta": i + 1,
            "name": muhurta_names_30[i] if i < len(muhurta_names_30) else f"M-{i+1}",
            "start": _minutes_to_time(start_min % 1440),
            "end": _minutes_to_time((start_min + ghati_duration) % 1440),
            "quality": "good" if i in [0, 2, 3, 4, 6, 7, 10, 13, 14, 19, 25, 26, 28] else "neutral",
        })

    # 28. Panchaka check (5 elements — inauspicious when Moon in certain nakshatras)
    panchaka_nakshatras = [1, 6, 11, 16, 21, 26]  # Bharani, Ardra, P.Phalguni, Vishakha, P.Ashadha, U.Bhadrapada
    is_panchaka = moon_nak_idx in panchaka_nakshatras
    panchaka = {"active": is_panchaka, "rahita": not is_panchaka}

    return {
        # Original contract keys
        "tithi": {
            "name": tithi["name"],
            "number": tithi["number"],
            "paksha": tithi["paksha"],
            "end_time": tithi_end,
            "next": next_tithi["name"],
        },
        "nakshatra": {
            **nakshatra,
            "end_time": nakshatra_end,
            "next": next_nak_name,
        },
        "yoga": {
            "name": yoga_name,
            "number": yoga_index + 1,
            "end_time": yoga_end,
            "next": next_yoga_name,
        },
        "karana": {
            "name": karana_name,
            "number": karana_index + 1,
            "end_time": karana_end,
            "second_karana": second_karana_name,
        },
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        # Extended data
        "moonrise": sun_times["moonrise"],
        "moonset": sun_times["moonset"],
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "vaar": {
            "name": _VAAR_NAMES[weekday],
            "english": _VAAR_ENGLISH[weekday],
            "number": weekday,
        },
        "dinamana": dinamana_str,
        "ratrimana": ratrimana_str,
        "madhyahna": madhyahna_str,
        "rahu_kaal": rahu_kaal,
        "gulika_kaal": gulika_kaal,
        "yamaganda": yamaganda,
        "abhijit_muhurat": abhijit,
        "brahma_muhurat": brahma,
        "ravi_yoga": ravi_yoga,
        "vijaya_muhurta": vijaya,
        "godhuli_muhurta": godhuli,
        "sayahna_sandhya": sayahna,
        "nishita_muhurta": nishita,
        "pratah_sandhya": pratah,
        "dur_muhurtam": dur_muhurtam,
        "varjyam": varjyam,
        "planetary_positions": planetary_positions,
        "hindu_calendar": hindu_calendar,
        "choghadiya": choghadiya,
        "ayanamsa": round(ayanamsa, 4),
        "sun_longitude": round(sun_sid, 4),
        "moon_longitude": round(moon_sid, 4),
        # Advanced Panchang
        "hora_table": hora_table,
        "lagna_table": lagna_table,
        "chandrabalam": chandrabalam,
        "tarabalam": tarabalam,
        "gowri_panchang": gowri_panchang,
        "do_ghati_muhurta": do_ghati,
        "panchaka": panchaka,
    }
