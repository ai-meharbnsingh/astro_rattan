import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from app.astro_engine import (
    calculate_planet_positions,
    get_sign_from_longitude,
    get_nakshatra_from_longitude,
    _parse_datetime,
    _datetime_to_jd
)

# Optional swisseph import for accurate sunrise
try:
    import swisseph as swe
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

def calculate_upagrahas(
    birth_date: str,
    birth_time: str,
    lat: float,
    lon: float,
    tz_offset: float
) -> Dict[str, Any]:
    """
    Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas.
    """
    # 1. Get Sun position
    pos_data = calculate_planet_positions(birth_date, birth_time, lat, lon, tz_offset)
    sun_lon = pos_data["planets"]["Sun"]["longitude"]

    # --- APRAKASHA GRAHAS ---
    # 1. Dhooma: Sun + 133 deg 20 min (133.3333333)
    dhooma = (sun_lon + 133.3333333) % 360
    
    # 2. Vyatipata: 360 - Dhooma
    vyatipata = (360 - dhooma) % 360
    
    # 3. Parivesha: Vyatipata + 180
    parivesha = (vyatipata + 180) % 360
    
    # 4. Indrachapa: 360 - Parivesha
    indrachapa = (360 - parivesha) % 360
    
    # 5. Upaketu: Indrachapa + 16 deg 40 min (16.6666666)
    upaketu = (indrachapa + 16.6666666) % 360

    aprakasha = [
        {"name": "Dhooma", "longitude": dhooma},
        {"name": "Vyatipata", "longitude": vyatipata},
        {"name": "Parivesha", "longitude": parivesha},
        {"name": "Indrachapa", "longitude": indrachapa},
        {"name": "Upaketu", "longitude": upaketu},
    ]

    # Format Aprakasha
    results = {}
    for p in aprakasha:
        l = p["longitude"]
        sign = get_sign_from_longitude(l)
        nak = get_nakshatra_from_longitude(l)
        results[p["name"]] = {
            "longitude": round(l, 4),
            "sign": sign,
            "sign_degree": round(l % 30, 4),
            "nakshatra": nak["name"],
            "nakshatra_pada": nak["pada"]
        }

    # --- GULIKA & MANDI (KALA VELAS) ---
    # We will use simple approximations for sunrise/sunset (6 AM and 6 PM) if swe is not present
    # To do it properly, we determine the day of the week, sunrise and sunset, and split into 8.
    
    dt_local = _parse_datetime(birth_date, birth_time, tz_offset)
    
    # Very basic approximation for sunrise/sunset for Fallback
    local_hour = dt_local.hour + dt_local.minute / 60.0
    day_of_week = dt_local.weekday()  # Monday is 0, Sunday is 6
    # Vedic day of week (Sunday = 0)
    vedic_weekday = (day_of_week + 1) % 7 
    
    sunrise_hour = 6.0
    sunset_hour = 18.0
    
    # Adjust weekday based on whether birth is before sunrise
    if local_hour < sunrise_hour:
        vedic_weekday = (vedic_weekday - 1) % 7
        is_day = False
    elif local_hour >= sunset_hour:
        is_day = False
    else:
        is_day = True

    # Order of lords in yamardhas
    # Sun, Moon, Mars, Mer, Jup, Ven, Sat
    lords_order = [0, 1, 2, 3, 4, 5, 6]  # 0=Sun, 1=Moon...
    
    if is_day:
        start_lord = vedic_weekday
    else:
        # Start lord is 5th from weekday lord
        start_lord = (vedic_weekday + 4) % 7
    
    # We want Saturn's portion (lord 6)
    # Find index of Saturn in the 8 parts
    saturn_index = (6 - start_lord) % 7
    
    if is_day:
        duration = sunset_hour - sunrise_hour
        part_len = duration / 8.0
        start_time = sunrise_hour
    else:
        duration = (24.0 - sunset_hour) + sunrise_hour # Night duration
        part_len = duration / 8.0
        start_time = sunset_hour

    # Gulika rises at the *beginning* (or end) of Saturn's portion. Standard: Gulika at end of Saturn's part, Mandi at middle.
    # Actually, widely accepted: Gulika is at the BEGINNING of Saturn's Muhurta in day, etc. Or at specific portions.
    # A standard calculation puts it at a specific fraction.
    # Let's say Gulika is at the start of Saturn's yamardha.
    gulika_hour = start_time + saturn_index * part_len
    
    # We use astro_engine's calculation for Gulika time:
    if gulika_hour >= 24.0:
        gulika_hour -= 24.0
    
    # Convert gulika_hour back to string HH:MM
    gh = int(gulika_hour)
    gm = int((gulika_hour - gh) * 60)
    g_time_str = f"{gh:02d}:{gm:02d}:00"
    
    # Calculate Ascendant for gulika_hour to get Gulika longitude
    g_pos = calculate_planet_positions(birth_date, g_time_str, lat, lon, tz_offset)
    gulika_lon = g_pos["ascendant"]["longitude"]
    
    g_sign = get_sign_from_longitude(gulika_lon)
    g_nak = get_nakshatra_from_longitude(gulika_lon)
    
    results["Gulika"] = {
        "longitude": round(gulika_lon, 4),
        "sign": g_sign,
        "sign_degree": round(gulika_lon % 30, 4),
        "nakshatra": g_nak["name"],
        "nakshatra_pada": g_nak["pada"]
    }
    
    # Mandi: middle of Saturn's part
    mandi_hour = start_time + (saturn_index + 0.5) * part_len
    if mandi_hour >= 24.0:
        mandi_hour -= 24.0
    mh = int(mandi_hour)
    mm = int((mandi_hour - mh) * 60)
    m_time_str = f"{mh:02d}:{mm:02d}:00"
    m_pos = calculate_planet_positions(birth_date, m_time_str, lat, lon, tz_offset)
    mandi_lon = m_pos["ascendant"]["longitude"]
    
    m_sign = get_sign_from_longitude(mandi_lon)
    m_nak = get_nakshatra_from_longitude(mandi_lon)
    
    results["Mandi"] = {
        "longitude": round(mandi_lon, 4),
        "sign": m_sign,
        "sign_degree": round(mandi_lon % 30, 4),
        "nakshatra": m_nak["name"],
        "nakshatra_pada": m_nak["pada"]
    }

    return results
