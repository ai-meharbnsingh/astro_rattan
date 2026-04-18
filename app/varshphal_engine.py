"""
varshphal_engine.py — Vedic Varshphal (Solar Return / Tajaka) Engine
=====================================================================
Calculates the annual horoscope chart when the Sun returns to its
exact natal sidereal longitude.

Provides:
  - Solar Return moment finder (Newton-Raphson on Swiss Ephemeris)
  - Full chart for Solar Return moment
  - Muntha (annual progressed ascendant)
  - Year Lord (Varsheshwar)
  - Mudda Dasha (annual planetary periods)
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from app.astro_engine import calculate_planet_positions, _datetime_to_jd, _HAS_SWE

if _HAS_SWE:
    import swisseph as swe

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
    6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# Day lords (JD 0 = Monday)
DAY_LORDS = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]

# Mudda Dasha fixed durations (days) — standard Tajaka allocation
MUDDA_DASHA_DAYS = {
    "Sun": 110, "Moon": 60, "Mars": 32, "Mercury": 40,
    "Jupiter": 48, "Venus": 56, "Saturn": 4,
}

# Tajaka year lord cycle
TAJAKA_CYCLE = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]


# ============================================================
# Solar Return Finder
# ============================================================

def _sun_sidereal_longitude(jd: float) -> float:
    """Get sidereal Sun longitude for a Julian Day."""
    if _HAS_SWE:
        from app.astro_engine import _SWE_LOCK
        with _SWE_LOCK:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            pos, _ = swe.calc_ut(jd, swe.SUN)
            ayanamsa = swe.get_ayanamsa(jd)
        return (pos[0] - ayanamsa) % 360.0
    # Fallback: approximate
    from app.astro_engine import _approx_sun_longitude, _approx_ayanamsa
    trop = _approx_sun_longitude(jd)
    aya = _approx_ayanamsa(jd)
    return (trop - aya) % 360.0


def find_solar_return_jd(natal_sun_lon: float, year: int, birth_month: int, birth_day: int) -> float:
    """
    Find the exact Julian Day when Sun returns to natal sidereal longitude.
    Uses Newton-Raphson iteration.
    """
    # Initial guess: birthday in target year
    jd = _datetime_to_jd(datetime(year, birth_month, min(birth_day, 28), 12, 0, 0, tzinfo=timezone.utc))

    for _ in range(50):
        current_lon = _sun_sidereal_longitude(jd)
        delta = current_lon - natal_sun_lon
        # Normalize to [-180, 180]
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360

        if abs(delta) < 0.0001:  # ~0.36 arcsecond accuracy
            return jd

        # Sun moves ~0.9856 deg/day
        jd -= delta / 0.9856

    return jd


def _jd_to_datetime(jd: float) -> datetime:
    """Convert Julian Day to UTC datetime."""
    if _HAS_SWE:
        y, m, d, h = swe.revjul(jd)
        hours = int(h)
        minutes = int((h - hours) * 60)
        seconds = int(((h - hours) * 60 - minutes) * 60)
        return datetime(y, m, d, hours, minutes, seconds, tzinfo=timezone.utc)
    # Rough fallback
    j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return j2000 + timedelta(days=jd - 2451545.0)


# ============================================================
# Muntha Calculation
# ============================================================

def calculate_muntha(natal_asc_lon: float, completed_years: int) -> Dict[str, Any]:
    """
    Muntha advances one sign per year from natal ascendant.
    Returns: {sign, sign_index, degree, lord}
    """
    natal_sign_idx = int(natal_asc_lon / 30.0)
    muntha_sign_idx = (natal_sign_idx + completed_years) % 12
    muntha_degree = muntha_sign_idx * 30.0 + (natal_asc_lon % 30.0)

    return {
        "sign": ZODIAC_SIGNS[muntha_sign_idx],
        "sign_index": muntha_sign_idx,
        "degree": round(muntha_degree % 360.0, 2),
        "lord": SIGN_LORDS[muntha_sign_idx],
    }


# ============================================================
# Year Lord
# ============================================================

def calculate_year_lord(solar_return_jd: float) -> str:
    """Year Lord = lord of the weekday on which the Solar Return falls."""
    day_of_week = int(solar_return_jd + 0.5) % 7
    return DAY_LORDS[day_of_week]


# ============================================================
# Mudda Dasha
# ============================================================

def calculate_mudda_dasha(year_lord: str, solar_return_date: str) -> List[Dict[str, Any]]:
    """
    Calculate Mudda Dasha periods for the Varshphal year.
    Sequence starts from the Year Lord in Tajaka cycle order.
    """
    # Find start index in Tajaka cycle
    if year_lord in TAJAKA_CYCLE:
        start_idx = TAJAKA_CYCLE.index(year_lord)
    else:
        start_idx = 0

    sequence = TAJAKA_CYCLE[start_idx:] + TAJAKA_CYCLE[:start_idx]

    # Parse start date
    try:
        start_dt = datetime.strptime(solar_return_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        start_dt = datetime.now(timezone.utc)

    periods = []
    current_dt = start_dt
    for planet in sequence:
        days = MUDDA_DASHA_DAYS.get(planet, 30)
        end_dt = current_dt + timedelta(days=days)
        periods.append({
            "planet": planet,
            "start_date": current_dt.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "days": days,
        })
        current_dt = end_dt

    return periods


# ============================================================
# Main Varshphal Calculation
# ============================================================

def calculate_varshphal(
    natal_chart_data: Dict[str, Any],
    target_year: int,
    birth_date: str,
    latitude: float,
    longitude: float,
    tz_offset: float = 5.5,
) -> Dict[str, Any]:
    """
    Calculate Varshphal (Solar Return) for a given year.

    Args:
        natal_chart_data: Original birth chart data with planets/ascendant.
        target_year: The year for which to calculate the Varshphal.
        birth_date: Birth date string "YYYY-MM-DD".
        latitude: Birth latitude.
        longitude: Birth longitude.
        tz_offset: Timezone offset from UTC.

    Returns:
        Complete Varshphal data including chart, muntha, year lord, mudda dasha.
    """
    # Get natal Sun longitude
    natal_sun = natal_chart_data.get("planets", {}).get("Sun", {})
    natal_sun_lon = natal_sun.get("longitude", 0.0)
    natal_asc = natal_chart_data.get("ascendant", {})
    natal_asc_lon = natal_asc.get("longitude", 0.0)

    # Parse birth date
    try:
        parts = birth_date.split("-")
        birth_year = int(parts[0])
        birth_month = int(parts[1])
        birth_day = int(parts[2])
    except (ValueError, IndexError):
        birth_year, birth_month, birth_day = 2000, 1, 1

    completed_years = target_year - birth_year

    # Find Solar Return moment
    sr_jd = find_solar_return_jd(natal_sun_lon, target_year, birth_month, birth_day)
    sr_dt = _jd_to_datetime(sr_jd)

    # sr_dt is in UTC — pass directly with tz_offset=0 to avoid double conversion
    # (calculate_planet_positions internally subtracts tz_offset, so passing local time
    # with tz_offset would subtract it twice)
    sr_date_str = sr_dt.strftime("%Y-%m-%d")
    sr_time_str = sr_dt.strftime("%H:%M:%S")

    # Calculate full chart for Solar Return moment (UTC)
    varshphal_chart = calculate_planet_positions(
        birth_date=sr_date_str,
        birth_time=sr_time_str,
        latitude=latitude,
        longitude=longitude,
        tz_offset=0.0,
    )

    # Muntha
    muntha = calculate_muntha(natal_asc_lon, completed_years)

    # Determine Muntha house in Varshphal chart
    vp_asc_sign_idx = int(varshphal_chart.get("ascendant", {}).get("longitude", 0) / 30.0)
    muntha_house = ((muntha["sign_index"] - vp_asc_sign_idx) % 12) + 1

    # Year Lord
    year_lord = calculate_year_lord(sr_jd)

    # Mudda Dasha
    mudda_dasha = calculate_mudda_dasha(year_lord, sr_date_str)

    # Current Mudda Dasha
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    current_mudda = None
    for md in mudda_dasha:
        if md["start_date"] <= today_str <= md["end_date"]:
            current_mudda = md["planet"]
            break

    # If today is before this year's solar return, the active varshphal is the previous year's.
    # Find the active mudda dasha from the previous solar year.
    active_solar_year = target_year
    if current_mudda is None and today_str < sr_date_str:
        active_solar_year = target_year - 1
        prev_sr_jd = find_solar_return_jd(natal_sun_lon, active_solar_year, birth_month, birth_day)
        prev_sr_date = _jd_to_datetime(prev_sr_jd).strftime("%Y-%m-%d")
        prev_year_lord = calculate_year_lord(prev_sr_jd)
        prev_mudda = calculate_mudda_dasha(prev_year_lord, prev_sr_date)
        for md in prev_mudda:
            if md["start_date"] <= today_str <= md["end_date"]:
                current_mudda = md["planet"]
                break

    return {
        "year": target_year,
        "completed_years": completed_years,
        "solar_return": {
            "date": sr_date_str,
            "time": sr_time_str,
            "julian_day": round(sr_jd, 6),
        },
        "chart_data": varshphal_chart,
        "muntha": {
            **muntha,
            "house": muntha_house,
            "favorable": muntha_house in {1, 2, 3, 4, 5, 9, 10, 11},
        },
        "year_lord": year_lord,
        "mudda_dasha": mudda_dasha,
        "current_mudda_dasha": current_mudda,
        "active_solar_year": active_solar_year,
    }
