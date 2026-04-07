"""
retrograde_engine.py — Planetary Retrograde Station Calculator
===============================================================
Calculates exact dates when planets go retrograde (station retrograde)
and direct (station direct) for a given year using Swiss Ephemeris.

Only computes for Mercury, Venus, Mars, Jupiter, Saturn.
(Sun/Moon never retrograde; Rahu/Ketu always retrograde.)
"""
from __future__ import annotations
import os
from typing import Any, Dict, List

try:
    import swisseph as swe
    _HAS_SWE = True
    _ephe_path = os.getenv("EPHE_PATH", "")
    if _ephe_path:
        swe.set_ephe_path(_ephe_path)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
except ImportError:
    _HAS_SWE = False

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Planets to check (swisseph IDs)
_RETRO_PLANETS = {
    "Mercury": 2,
    "Venus": 3,
    "Mars": 4,
    "Jupiter": 5,
    "Saturn": 6,
}


def _jd_to_date(jd: float) -> str:
    """Convert Julian Day to YYYY-MM-DD string."""
    year, month, day, hour = swe.revjul(jd)
    return f"{year:04d}-{month:02d}-{int(day):02d}"


def _jd_to_datetime(jd: float) -> str:
    """Convert Julian Day to YYYY-MM-DD HH:MM string."""
    year, month, day, hour = swe.revjul(jd)
    h = int(hour)
    m = int((hour - h) * 60)
    return f"{year:04d}-{month:02d}-{int(day):02d} {h:02d}:{m:02d}"


def _get_speed(jd: float, planet_id: int) -> float:
    """Get daily speed of planet at given Julian Day."""
    pos = swe.calc_ut(jd, planet_id)
    return pos[0][3]  # daily speed in longitude


def _get_longitude(jd: float, planet_id: int) -> float:
    """Get sidereal longitude of planet at given Julian Day."""
    pos = swe.calc_ut(jd, planet_id)
    lon = pos[0][0]
    ayanamsa = swe.get_ayanamsa(jd)
    return (lon - ayanamsa) % 360.0


def _binary_search_station(jd_start: float, jd_end: float, planet_id: int, precision: float = 0.01) -> float:
    """
    Binary search for exact moment when planet speed crosses zero.
    Precision ~15 minutes (0.01 day).
    """
    while (jd_end - jd_start) > precision:
        mid = (jd_start + jd_end) / 2.0
        speed_start = _get_speed(jd_start, planet_id)
        speed_mid = _get_speed(mid, planet_id)
        # If speed sign changes between start and mid, station is in first half
        if (speed_start > 0 and speed_mid <= 0) or (speed_start <= 0 and speed_mid > 0):
            jd_end = mid
        else:
            jd_start = mid
    return (jd_start + jd_end) / 2.0


def calculate_retrograde_stations(year: int) -> Dict[str, Any]:
    """
    Calculate all retrograde and direct station dates for a year.

    Returns:
        {
            "Mercury": [
                {"station": "retrograde", "date": "2026-01-15", "sign": "Capricorn", "longitude": 285.3},
                {"station": "direct", "date": "2026-02-05", "sign": "Capricorn", "longitude": 278.7},
                ...
            ],
            ...
        }
    """
    if not _HAS_SWE:
        return {name: [] for name in _RETRO_PLANETS}

    # Time range: full year with 15-day buffer on each side
    jd_start = swe.julday(year, 1, 1, 0.0)
    jd_end = swe.julday(year, 12, 31, 23.99)
    jd_start -= 15  # buffer for retrograde that started in Dec prev year
    jd_end += 15    # buffer for direct station in Jan next year

    result: Dict[str, List[Dict[str, Any]]] = {}

    for planet_name, planet_id in _RETRO_PLANETS.items():
        stations: List[Dict[str, Any]] = []
        step = 1.0  # 1-day steps (fine enough to detect speed sign changes)

        jd = jd_start
        prev_speed = _get_speed(jd, planet_id)

        while jd < jd_end:
            jd += step
            curr_speed = _get_speed(jd, planet_id)

            # Speed sign change detected
            if (prev_speed > 0 and curr_speed <= 0) or (prev_speed <= 0 and curr_speed > 0):
                # Binary search for exact station
                exact_jd = _binary_search_station(jd - step, jd, planet_id)
                station_date = _jd_to_date(exact_jd)

                # Only include if station date falls within the requested year
                date_year = int(station_date[:4])
                if date_year == year:
                    lon = _get_longitude(exact_jd, planet_id)
                    sign_idx = int(lon / 30.0) % 12
                    sign = _SIGN_NAMES[sign_idx]
                    station_type = "retrograde" if prev_speed > 0 else "direct"

                    stations.append({
                        "station": station_type,
                        "date": station_date,
                        "datetime": _jd_to_datetime(exact_jd),
                        "sign": sign,
                        "longitude": round(lon, 2),
                        "sign_degree": round(lon % 30.0, 2),
                    })

            prev_speed = curr_speed

        result[planet_name] = stations

    return result
