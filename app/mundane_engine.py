"""
mundane_engine.py -- Mundane Astrology Engine
==============================================
Analyses national/country charts using Vedic mundane astrology principles.
Uses independence/foundation chart data for countries and evaluates current
transits, eclipses, ingresses, and planetary combinations for geopolitical,
economic, and social predictions.

Provides:
  - COUNTRY_CHARTS          — foundation data for 13 countries
  - MUNDANE_HOUSES           — mundane meanings for each house (en + hi)
  - calculate_mundane_analysis(country_key, year)
  - calculate_eclipses(year)
  - calculate_ingress(year)
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.astro_engine import (
    calculate_planet_positions,
    _SIGN_NAMES,
)


# ============================================================
# 1. COUNTRY CHARTS — independence / foundation data
# ============================================================

COUNTRY_CHARTS: Dict[str, Dict[str, Any]] = {
    "india": {
        "name": "India",
        "name_hi": "\u092d\u093e\u0930\u0924",
        "date": "1947-08-15",
        "time": "00:00:00",
        "lat": 28.6139,
        "lon": 77.2090,
        "tz": 5.5,
        "capital": "New Delhi",
        "capital_hi": "\u0928\u0908 \u0926\u093f\u0932\u094d\u0932\u0940",
        "description": {
            "en": "Independence from British rule",
            "hi": "\u092c\u094d\u0930\u093f\u091f\u093f\u0936 \u0936\u093e\u0938\u0928 \u0938\u0947 \u0938\u094d\u0935\u0924\u0902\u0924\u094d\u0930\u0924\u093e",
        },
    },
    "usa": {
        "name": "United States",
        "name_hi": "\u0938\u0902\u092f\u0941\u0915\u094d\u0924 \u0930\u093e\u091c\u094d\u092f \u0905\u092e\u0947\u0930\u093f\u0915\u093e",
        "date": "1776-07-04",
        "time": "17:10:00",
        "lat": 39.9526,
        "lon": -75.1652,
        "tz": -5.0,
        "capital": "Washington D.C.",
        "capital_hi": "\u0935\u093e\u0936\u093f\u0902\u0917\u091f\u0928 \u0921\u0940.\u0938\u0940.",
        "description": {
            "en": "Declaration of Independence",
            "hi": "\u0938\u094d\u0935\u0924\u0902\u0924\u094d\u0930\u0924\u093e \u0915\u0940 \u0918\u094b\u0937\u0923\u093e",
        },
    },
    "uk": {
        "name": "United Kingdom",
        "name_hi": "\u092f\u0942\u0928\u093e\u0907\u091f\u0947\u0921 \u0915\u093f\u0902\u0917\u0921\u092e",
        "date": "1801-01-01",
        "time": "00:00:00",
        "lat": 51.5074,
        "lon": -0.1278,
        "tz": 0.0,
        "capital": "London",
        "capital_hi": "\u0932\u0902\u0926\u0928",
        "description": {
            "en": "Act of Union — United Kingdom of Great Britain and Ireland",
            "hi": "\u0938\u0902\u0918 \u0905\u0927\u093f\u0928\u093f\u092f\u092e \u2014 \u0917\u094d\u0930\u0947\u091f \u092c\u094d\u0930\u093f\u091f\u0947\u0928 \u0914\u0930 \u0906\u092f\u0930\u0932\u0948\u0902\u0921",
        },
    },
    "china": {
        "name": "China",
        "name_hi": "\u091a\u0940\u0928",
        "date": "1949-10-01",
        "time": "15:00:00",
        "lat": 39.9042,
        "lon": 116.4074,
        "tz": 8.0,
        "capital": "Beijing",
        "capital_hi": "\u092c\u0940\u091c\u093f\u0902\u0917",
        "description": {
            "en": "Proclamation of the People's Republic of China",
            "hi": "\u091a\u0940\u0928 \u091c\u0928\u0935\u093e\u0926\u0940 \u0917\u0923\u0930\u093e\u091c\u094d\u092f \u0915\u0940 \u0918\u094b\u0937\u0923\u093e",
        },
    },
    "russia": {
        "name": "Russia",
        "name_hi": "\u0930\u0942\u0938",
        "date": "1991-12-25",
        "time": "19:38:00",
        "lat": 55.7558,
        "lon": 37.6173,
        "tz": 3.0,
        "capital": "Moscow",
        "capital_hi": "\u092e\u0949\u0938\u094d\u0915\u094b",
        "description": {
            "en": "Dissolution of the Soviet Union — Russian Federation",
            "hi": "\u0938\u094b\u0935\u093f\u092f\u0924 \u0938\u0902\u0918 \u0915\u093e \u0935\u093f\u0918\u091f\u0928 \u2014 \u0930\u0942\u0938\u0940 \u0938\u0902\u0918",
        },
    },
    "pakistan": {
        "name": "Pakistan",
        "name_hi": "\u092a\u093e\u0915\u093f\u0938\u094d\u0924\u093e\u0928",
        "date": "1947-08-14",
        "time": "00:00:00",
        "lat": 33.6844,
        "lon": 73.0479,
        "tz": 5.0,
        "capital": "Islamabad",
        "capital_hi": "\u0907\u0938\u094d\u0932\u093e\u092e\u093e\u092c\u093e\u0926",
        "description": {
            "en": "Independence from British rule",
            "hi": "\u092c\u094d\u0930\u093f\u091f\u093f\u0936 \u0936\u093e\u0938\u0928 \u0938\u0947 \u0938\u094d\u0935\u0924\u0902\u0924\u094d\u0930\u0924\u093e",
        },
    },
    "japan": {
        "name": "Japan",
        "name_hi": "\u091c\u093e\u092a\u093e\u0928",
        "date": "1952-04-28",
        "time": "00:00:00",
        "lat": 35.6762,
        "lon": 139.6503,
        "tz": 9.0,
        "capital": "Tokyo",
        "capital_hi": "\u091f\u094b\u0915\u094d\u092f\u094b",
        "description": {
            "en": "Treaty of San Francisco — sovereignty restored",
            "hi": "\u0938\u0948\u0928 \u092b\u094d\u0930\u093e\u0902\u0938\u093f\u0938\u094d\u0915\u094b \u0938\u0902\u0927\u093f \u2014 \u0938\u0902\u092a\u094d\u0930\u092d\u0941\u0924\u093e \u092c\u0939\u093e\u0932",
        },
    },
    "france": {
        "name": "France",
        "name_hi": "\u092b\u094d\u0930\u093e\u0902\u0938",
        "date": "1958-10-04",
        "time": "00:00:00",
        "lat": 48.8566,
        "lon": 2.3522,
        "tz": 1.0,
        "capital": "Paris",
        "capital_hi": "\u092a\u0947\u0930\u093f\u0938",
        "description": {
            "en": "Fifth Republic — Constitution of the French Fifth Republic",
            "hi": "\u092a\u093e\u0901\u091a\u0935\u093e\u0901 \u0917\u0923\u0930\u093e\u091c\u094d\u092f \u2014 \u092b\u094d\u0930\u093e\u0902\u0938\u0940\u0938\u0940 \u0938\u0902\u0935\u093f\u0927\u093e\u0928",
        },
    },
    "germany": {
        "name": "Germany",
        "name_hi": "\u091c\u0930\u094d\u092e\u0928\u0940",
        "date": "1990-10-03",
        "time": "00:00:00",
        "lat": 52.5200,
        "lon": 13.4050,
        "tz": 1.0,
        "capital": "Berlin",
        "capital_hi": "\u092c\u0930\u094d\u0932\u093f\u0928",
        "description": {
            "en": "German Reunification",
            "hi": "\u091c\u0930\u094d\u092e\u0928 \u092a\u0941\u0928\u0930\u094d\u0947\u0915\u0940\u0915\u0930\u0923",
        },
    },
    "australia": {
        "name": "Australia",
        "name_hi": "\u0911\u0938\u094d\u091f\u094d\u0930\u0947\u0932\u093f\u092f\u093e",
        "date": "1901-01-01",
        "time": "00:00:00",
        "lat": -35.2809,
        "lon": 149.1300,
        "tz": 10.0,
        "capital": "Canberra",
        "capital_hi": "\u0915\u0948\u0928\u092c\u0930\u093e",
        "description": {
            "en": "Federation of Australia",
            "hi": "\u0911\u0938\u094d\u091f\u094d\u0930\u0947\u0932\u093f\u092f\u093e \u0938\u0902\u0918",
        },
    },
    "brazil": {
        "name": "Brazil",
        "name_hi": "\u092c\u094d\u0930\u093e\u091c\u093c\u0940\u0932",
        "date": "1822-09-07",
        "time": "16:00:00",
        "lat": -15.7975,
        "lon": -47.8919,
        "tz": -3.0,
        "capital": "Brasilia",
        "capital_hi": "\u092c\u094d\u0930\u093e\u0938\u0940\u0932\u093f\u092f\u093e",
        "description": {
            "en": "Independence from Portugal",
            "hi": "\u092a\u0941\u0930\u094d\u0924\u0917\u093e\u0932 \u0938\u0947 \u0938\u094d\u0935\u0924\u0902\u0924\u094d\u0930\u0924\u093e",
        },
    },
    "canada": {
        "name": "Canada",
        "name_hi": "\u0915\u0928\u093e\u0921\u093e",
        "date": "1867-07-01",
        "time": "00:00:00",
        "lat": 45.4215,
        "lon": -75.6972,
        "tz": -5.0,
        "capital": "Ottawa",
        "capital_hi": "\u0913\u091f\u093e\u0935\u093e",
        "description": {
            "en": "Confederation — Dominion of Canada",
            "hi": "\u0915\u0928\u093e\u0921\u093e \u0938\u0902\u0918 \u0915\u0940 \u0938\u094d\u0925\u093e\u092a\u0928\u093e",
        },
    },
    "israel": {
        "name": "Israel",
        "name_hi": "\u0907\u091c\u093c\u0930\u093e\u092f\u0932",
        "date": "1948-05-14",
        "time": "16:00:00",
        "lat": 31.7683,
        "lon": 35.2137,
        "tz": 2.0,
        "capital": "Jerusalem",
        "capital_hi": "\u092f\u0947\u0930\u0941\u0936\u0932\u092e",
        "description": {
            "en": "Declaration of the State of Israel",
            "hi": "\u0907\u091c\u093c\u0930\u093e\u092f\u0932 \u0930\u093e\u091c\u094d\u092f \u0915\u0940 \u0918\u094b\u0937\u0923\u093e",
        },
    },
}


# ============================================================
# 2. MUNDANE HOUSE MEANINGS (en + hi)
# ============================================================

MUNDANE_HOUSES: Dict[int, Dict[str, str]] = {
    1: {
        "en": "People, national mood, general condition",
        "hi": "\u091c\u0928\u0924\u093e, \u0930\u093e\u0937\u094d\u091f\u094d\u0930\u0940\u092f \u092e\u0928\u094b\u0926\u0936\u093e, \u0938\u093e\u092e\u093e\u0928\u094d\u092f \u0938\u094d\u0925\u093f\u0924\u093f",
    },
    2: {
        "en": "National wealth, economy, reserves",
        "hi": "\u0930\u093e\u0937\u094d\u091f\u094d\u0930\u0940\u092f \u0927\u0928, \u0905\u0930\u094d\u0925\u0935\u094d\u092f\u0935\u0938\u094d\u0925\u093e, \u092d\u0902\u0921\u093e\u0930",
    },
    3: {
        "en": "Communication, media, neighbors",
        "hi": "\u0938\u0902\u091a\u093e\u0930, \u092e\u0940\u0921\u093f\u092f\u093e, \u092a\u0921\u093c\u094b\u0938\u0940 \u0926\u0947\u0936",
    },
    4: {
        "en": "Land, agriculture, opposition party",
        "hi": "\u092d\u0942\u092e\u093f, \u0915\u0943\u0937\u093f, \u0935\u093f\u092a\u0915\u094d\u0937",
    },
    5: {
        "en": "Speculation, entertainment, children",
        "hi": "\u0938\u091f\u094d\u091f\u093e, \u092e\u0928\u094b\u0930\u0902\u091c\u0928, \u092c\u091a\u094d\u091a\u0947",
    },
    6: {
        "en": "Military, health, service sector",
        "hi": "\u0938\u0947\u0928\u093e, \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f, \u0938\u0947\u0935\u093e \u0915\u094d\u0937\u0947\u0924\u094d\u0930",
    },
    7: {
        "en": "Foreign relations, war & peace, treaties",
        "hi": "\u0935\u093f\u0926\u0947\u0936 \u0938\u0902\u092c\u0902\u0927, \u092f\u0941\u0926\u094d\u0927 \u090f\u0935\u0902 \u0936\u093e\u0902\u0924\u093f, \u0938\u0902\u0927\u093f",
    },
    8: {
        "en": "Death toll, disasters, hidden enemies",
        "hi": "\u092e\u0943\u0924\u094d\u092f\u0941 \u0926\u0930, \u0906\u092a\u0926\u093e\u090f\u0901, \u091b\u093f\u092a\u0947 \u0936\u0924\u094d\u0930\u0941",
    },
    9: {
        "en": "Religion, judiciary, higher education",
        "hi": "\u0927\u0930\u094d\u092e, \u0928\u094d\u092f\u093e\u092f\u092a\u093e\u0932\u093f\u0915\u093e, \u0909\u091a\u094d\u091a \u0936\u093f\u0915\u094d\u0937\u093e",
    },
    10: {
        "en": "Government, PM/President, authority",
        "hi": "\u0938\u0930\u0915\u093e\u0930, \u092a\u094d\u0930\u0927\u093e\u0928\u092e\u0902\u0924\u094d\u0930\u0940/\u0930\u093e\u0937\u094d\u091f\u094d\u0930\u092a\u0924\u093f, \u0938\u0924\u094d\u0924\u093e",
    },
    11: {
        "en": "Parliament, alliances, income",
        "hi": "\u0938\u0902\u0938\u0926, \u0917\u0920\u092c\u0902\u0927\u0928, \u0906\u092f",
    },
    12: {
        "en": "Foreign affairs, losses, secret enemies",
        "hi": "\u0935\u093f\u0926\u0947\u0936 \u092e\u093e\u092e\u0932\u0947, \u0939\u093e\u0928\u093f, \u0917\u0941\u092a\u094d\u0924 \u0936\u0924\u094d\u0930\u0941",
    },
}


# ============================================================
# ZODIAC HELPERS
# ============================================================

_SIGN_INDEX: Dict[str, int] = {name: i for i, name in enumerate(_SIGN_NAMES)}

_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}


def _angular_distance(lon_a: float, lon_b: float) -> float:
    """Smallest angular distance between two ecliptic longitudes (0-180)."""
    diff = abs(lon_a - lon_b) % 360.0
    return diff if diff <= 180.0 else 360.0 - diff


def _house_number(planet_sign: str, asc_sign: str) -> int:
    """House number (1-12) of planet_sign counted from asc_sign."""
    asc_idx = _SIGN_INDEX.get(asc_sign, 0)
    planet_idx = _SIGN_INDEX.get(planet_sign, 0)
    return ((planet_idx - asc_idx) % 12) + 1


# ============================================================
# 3. CURRENT TRANSIT POSITIONS
# ============================================================

def _get_current_planet_positions() -> Dict[str, Dict[str, Any]]:
    """
    Calculate current planet positions using the same approach as astro_engine:
    call calculate_planet_positions with current UTC datetime and a neutral location.
    Returns a dict of planet name -> {longitude, sign, sign_degree, house, ...}.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    # Use 0,0 coords and tz=0 for a pure transit snapshot (houses not meaningful
    # in transit-only context — we re-derive house from country ascendant).
    result = calculate_planet_positions(date_str, time_str, 0.0, 0.0, 0.0)
    return result.get("planets", {})


def _current_transits_in_country_chart(
    country_chart: Dict[str, Any],
    birth_chart: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Build transit list: current planet positions with house placement relative
    to the country's natal ascendant.
    """
    transit_planets = _get_current_planet_positions()
    asc_sign = birth_chart.get("ascendant", {}).get("sign", "Aries")

    transits: List[Dict[str, Any]] = []
    for pname, pdata in transit_planets.items():
        transit_sign = pdata.get("sign", "Aries")
        house = _house_number(transit_sign, asc_sign)
        mundane_meaning = MUNDANE_HOUSES.get(house, {"en": "", "hi": ""})
        transits.append({
            "planet": pname,
            "longitude": pdata.get("longitude"),
            "sign": transit_sign,
            "sign_degree": pdata.get("sign_degree"),
            "nakshatra": pdata.get("nakshatra"),
            "retrograde": pdata.get("retrograde", False),
            "house_in_country_chart": house,
            "house_meaning": mundane_meaning,
        })
    return transits


# ============================================================
# 4. HOUSE ANALYSIS
# ============================================================

def _analyze_houses(
    birth_chart: Dict[str, Any],
    transit_planets: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Produce 12-house analysis combining mundane meaning with current transits.
    """
    asc_sign = birth_chart.get("ascendant", {}).get("sign", "Aries")

    # Natal planets per house
    natal_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for pname, pdata in birth_chart.get("planets", {}).items():
        natal_planets[pdata.get("house", 1)].append(pname)

    # Transit planets per house
    transit_in_house: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for t in transit_planets:
        transit_in_house[t["house_in_country_chart"]].append(t["planet"])

    houses: List[Dict[str, Any]] = []
    for h in range(1, 13):
        malefic_count = sum(1 for p in transit_in_house[h] if p in _MALEFICS)
        benefic_count = sum(1 for p in transit_in_house[h] if p in _BENEFICS)

        if benefic_count > malefic_count:
            condition = {
                "en": "Positive — benefic transits supporting this domain",
                "hi": "\u0938\u0915\u093e\u0930\u093e\u0924\u094d\u092e\u0915 \u2014 \u0936\u0941\u092d \u0917\u094d\u0930\u0939\u094b\u0902 \u0915\u093e \u0938\u0939\u092f\u094b\u0917",
            }
        elif malefic_count > benefic_count:
            condition = {
                "en": "Pressured — malefic transits creating challenges",
                "hi": "\u0926\u092c\u093e\u0935 \u092e\u0947\u0902 \u2014 \u092a\u093e\u092a \u0917\u094d\u0930\u0939\u094b\u0902 \u0938\u0947 \u091a\u0941\u0928\u094c\u0924\u093f\u092f\u093e\u0901",
            }
        else:
            condition = {
                "en": "Neutral — balanced planetary influence",
                "hi": "\u0924\u091f\u0938\u094d\u0925 \u2014 \u0938\u0902\u0924\u0941\u0932\u093f\u0924 \u0917\u094d\u0930\u0939 \u092a\u094d\u0930\u092d\u093e\u0935",
            }

        asc_idx = _SIGN_INDEX.get(asc_sign, 0)
        house_sign = _SIGN_NAMES[(asc_idx + h - 1) % 12]

        houses.append({
            "house": h,
            "sign": house_sign,
            "mundane_meaning": MUNDANE_HOUSES[h],
            "natal_planets": natal_planets[h],
            "transit_planets": transit_in_house[h],
            "condition": condition,
        })
    return houses


# ============================================================
# 5. CONFLICT / DISASTER RISK INDICATORS
# ============================================================

def _conflict_indicators(
    transit_planets: List[Dict[str, Any]],
    asc_sign: str,
) -> List[Dict[str, Any]]:
    """
    Check for dangerous planetary combinations in current transits.
    """
    # Build lookup
    planet_data: Dict[str, Dict[str, Any]] = {}
    for t in transit_planets:
        planet_data[t["planet"]] = t

    indicators: List[Dict[str, Any]] = []

    # Mars-Saturn conjunction (within 15 degrees)
    mars = planet_data.get("Mars")
    saturn = planet_data.get("Saturn")
    if mars and saturn:
        dist = _angular_distance(mars["longitude"], saturn["longitude"])
        if dist <= 15.0:
            indicators.append({
                "combination": "Mars-Saturn",
                "distance_deg": round(dist, 2),
                "severity": "high" if dist <= 8.0 else "medium",
                "description": {
                    "en": "Mars-Saturn conjunction indicates political instability, industrial disputes, and potential for accidents or structural failures",
                    "hi": "\u092e\u0902\u0917\u0932-\u0936\u0928\u093f \u092f\u0941\u0924\u093f \u0930\u093e\u091c\u0928\u0940\u0924\u093f\u0915 \u0905\u0938\u094d\u0925\u093f\u0930\u0924\u093e, \u0914\u0926\u094d\u092f\u094b\u0917\u093f\u0915 \u0935\u093f\u0935\u093e\u0926 \u0914\u0930 \u0926\u0941\u0930\u094d\u0918\u091f\u0928\u093e\u0913\u0902 \u0915\u0940 \u0938\u0902\u092d\u093e\u0935\u0928\u093e \u0926\u0930\u094d\u0936\u093e\u0924\u0940 \u0939\u0948",
                },
            })

    # Mars-Rahu conjunction (within 15 degrees)
    rahu = planet_data.get("Rahu")
    if mars and rahu:
        dist = _angular_distance(mars["longitude"], rahu["longitude"])
        if dist <= 15.0:
            indicators.append({
                "combination": "Mars-Rahu",
                "distance_deg": round(dist, 2),
                "severity": "high" if dist <= 8.0 else "medium",
                "description": {
                    "en": "Mars-Rahu conjunction (Angarak Yoga) indicates aggression, violence, terrorism risk, and sudden explosive events",
                    "hi": "\u092e\u0902\u0917\u0932-\u0930\u093e\u0939\u0941 \u092f\u0941\u0924\u093f (\u0905\u0902\u0917\u093e\u0930\u0915 \u092f\u094b\u0917) \u0906\u0915\u094d\u0930\u093e\u092e\u0915\u0924\u093e, \u0939\u093f\u0902\u0938\u093e, \u0906\u0924\u0902\u0915\u0935\u093e\u0926 \u0914\u0930 \u0905\u091a\u093e\u0928\u0915 \u0935\u093f\u0938\u094d\u092b\u094b\u091f\u0915 \u0918\u091f\u0928\u093e\u0913\u0902 \u0915\u093e \u0938\u0902\u0915\u0947\u0924 \u0926\u0947\u0924\u0940 \u0939\u0948",
                },
            })

    # Saturn in 8th from country lagna
    if saturn:
        saturn_house = _house_number(saturn["sign"], asc_sign)
        if saturn_house == 8:
            indicators.append({
                "combination": "Saturn-in-8th",
                "distance_deg": 0,
                "severity": "high",
                "description": {
                    "en": "Saturn transiting the 8th house of the national chart signals disaster risk, mass casualties, and national grief",
                    "hi": "\u0936\u0928\u093f \u0915\u093e \u0930\u093e\u0937\u094d\u091f\u094d\u0930\u0940\u092f \u0915\u0941\u0902\u0921\u0932\u0940 \u0915\u0947 \u0906\u0920\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0917\u094b\u091a\u0930 \u0906\u092a\u0926\u093e, \u091c\u0928\u0939\u093e\u0928\u093f \u0914\u0930 \u0930\u093e\u0937\u094d\u091f\u094d\u0930\u0940\u092f \u0936\u094b\u0915 \u0915\u093e \u0938\u0902\u0915\u0947\u0924 \u0926\u0947\u0924\u093e \u0939\u0948",
                },
            })

    # Malefics in 6th house — military/health alerts
    for pname in _MALEFICS:
        p = planet_data.get(pname)
        if p:
            h = _house_number(p["sign"], asc_sign)
            if h == 6:
                indicators.append({
                    "combination": f"{pname}-in-6th",
                    "distance_deg": 0,
                    "severity": "medium",
                    "description": {
                        "en": f"{pname} transiting the 6th house signals military tensions, health epidemics, or labour unrest",
                        "hi": f"{pname} \u0915\u093e \u091b\u0920\u0947 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0917\u094b\u091a\u0930 \u0938\u0948\u0928\u094d\u092f \u0924\u0928\u093e\u0935, \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u092e\u0939\u093e\u092e\u093e\u0930\u0940 \u092f\u093e \u0936\u094d\u0930\u092e \u0905\u0936\u093e\u0902\u0924\u093f \u0915\u093e \u0938\u0902\u0915\u0947\u0924 \u0926\u0947\u0924\u093e \u0939\u0948",
                    },
                })

    # Malefics in 8th house — death/disaster
    for pname in _MALEFICS - {"Saturn"}:  # Saturn-in-8th already handled above
        p = planet_data.get(pname)
        if p:
            h = _house_number(p["sign"], asc_sign)
            if h == 8:
                indicators.append({
                    "combination": f"{pname}-in-8th",
                    "distance_deg": 0,
                    "severity": "medium",
                    "description": {
                        "en": f"{pname} transiting the 8th house warns of hidden crises, natural disasters, or covert threats",
                        "hi": f"{pname} \u0915\u093e \u0906\u0920\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0917\u094b\u091a\u0930 \u091b\u093f\u092a\u0947 \u0938\u0902\u0915\u091f, \u092a\u094d\u0930\u093e\u0915\u0943\u0924\u093f\u0915 \u0906\u092a\u0926\u093e \u092f\u093e \u0917\u0941\u092a\u094d\u0924 \u0916\u0924\u0930\u094b\u0902 \u0915\u0940 \u091a\u0947\u0924\u093e\u0935\u0928\u0940 \u0926\u0947\u0924\u093e \u0939\u0948",
                    },
                })

    return indicators


# ============================================================
# 6. ECONOMIC INDICATORS
# ============================================================

def _economic_indicators(
    transit_planets: List[Dict[str, Any]],
    asc_sign: str,
) -> Dict[str, Any]:
    """Analyse Jupiter, Saturn, Mercury positions for economic outlook."""
    planet_data: Dict[str, Dict[str, Any]] = {}
    for t in transit_planets:
        planet_data[t["planet"]] = t

    factors: List[Dict[str, Any]] = []
    positive = 0
    negative = 0

    # Jupiter in 2nd or 11th → growth
    jupiter = planet_data.get("Jupiter")
    if jupiter:
        h = _house_number(jupiter["sign"], asc_sign)
        if h in (2, 11):
            positive += 2
            factors.append({
                "planet": "Jupiter",
                "house": h,
                "effect": {
                    "en": f"Jupiter in the {h}{'nd' if h == 2 else 'th'} house promotes economic expansion, trade growth, and increased revenue",
                    "hi": f"\u092c\u0943\u0939\u0938\u094d\u092a\u0924\u093f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0906\u0930\u094d\u0925\u093f\u0915 \u0935\u093f\u0938\u094d\u0924\u093e\u0930, \u0935\u094d\u092f\u093e\u092a\u093e\u0930 \u0935\u0943\u0926\u094d\u0927\u093f \u0914\u0930 \u0930\u093e\u091c\u0938\u094d\u0935 \u0935\u0943\u0926\u094d\u0927\u093f \u0915\u094b \u092c\u0922\u093c\u093e\u0935\u093e \u0926\u0947\u0924\u093e \u0939\u0948",
                },
            })
        elif h in (6, 8, 12):
            negative += 1
            factors.append({
                "planet": "Jupiter",
                "house": h,
                "effect": {
                    "en": f"Jupiter in the {h}th house may reduce economic benefits — growth slows or gets diverted",
                    "hi": f"\u092c\u0943\u0939\u0938\u094d\u092a\u0924\u093f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0906\u0930\u094d\u0925\u093f\u0915 \u0932\u093e\u092d \u0915\u092e \u0939\u094b \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
                },
            })

    # Saturn in 2nd or 8th → economic pressure
    saturn = planet_data.get("Saturn")
    if saturn:
        h = _house_number(saturn["sign"], asc_sign)
        if h in (2, 8):
            negative += 2
            factors.append({
                "planet": "Saturn",
                "house": h,
                "effect": {
                    "en": f"Saturn in the {h}{'nd' if h == 2 else 'th'} house creates economic pressure — austerity, slowdown, or financial restructuring",
                    "hi": f"\u0936\u0928\u093f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0906\u0930\u094d\u0925\u093f\u0915 \u0926\u092c\u093e\u0935 \u2014 \u092e\u093f\u0924\u0935\u094d\u092f\u092f\u093f\u0924\u093e, \u092e\u0902\u0926\u0940 \u092f\u093e \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u092a\u0941\u0928\u0930\u094d\u0917\u0920\u0928",
                },
            })
        elif h in (3, 6, 11):
            positive += 1
            factors.append({
                "planet": "Saturn",
                "house": h,
                "effect": {
                    "en": f"Saturn in the {h}{'rd' if h == 3 else 'th'} house supports disciplined economic planning and structural reforms",
                    "hi": f"\u0936\u0928\u093f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0905\u0928\u0941\u0936\u093e\u0938\u093f\u0924 \u0906\u0930\u094d\u0925\u093f\u0915 \u092f\u094b\u091c\u0928\u093e \u0914\u0930 \u0938\u0902\u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915 \u0938\u0941\u0927\u093e\u0930\u094b\u0902 \u0915\u093e \u0938\u092e\u0930\u094d\u0925\u0928 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })

    # Mercury strong → trade growth
    mercury = planet_data.get("Mercury")
    if mercury:
        h = _house_number(mercury["sign"], asc_sign)
        is_retro = mercury.get("retrograde", False)
        if h in (1, 2, 4, 7, 10, 11) and not is_retro:
            positive += 1
            factors.append({
                "planet": "Mercury",
                "house": h,
                "effect": {
                    "en": f"Mercury direct in the {h}{'st' if h == 1 else 'nd' if h == 2 else 'th'} house supports trade, commerce, and diplomatic communication",
                    "hi": f"\u092c\u0941\u0927 \u092e\u093e\u0930\u094d\u0917\u0940 {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0935\u094d\u092f\u093e\u092a\u093e\u0930, \u0935\u093e\u0923\u093f\u091c\u094d\u092f \u0914\u0930 \u0930\u093e\u091c\u0928\u092f\u093f\u0915 \u0938\u0902\u0935\u093e\u0926 \u0915\u093e \u0938\u092e\u0930\u094d\u0925\u0928 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })
        elif is_retro:
            negative += 1
            factors.append({
                "planet": "Mercury",
                "house": h,
                "effect": {
                    "en": "Mercury retrograde disrupts trade agreements, communication systems, and market stability",
                    "hi": "\u092c\u0941\u0927 \u0935\u0915\u094d\u0930\u0940 \u0935\u094d\u092f\u093e\u092a\u093e\u0930 \u0938\u092e\u091d\u094c\u0924\u094b\u0902, \u0938\u0902\u091a\u093e\u0930 \u092a\u094d\u0930\u0923\u093e\u0932\u093f\u092f\u094b\u0902 \u0914\u0930 \u092c\u093e\u091c\u093c\u093e\u0930 \u0938\u094d\u0925\u093f\u0930\u0924\u093e \u0915\u094b \u092c\u093e\u0927\u093f\u0924 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })

    # Determine trend
    if positive > negative:
        trend = "growth"
        trend_hi = "\u0935\u0943\u0926\u094d\u0927\u093f"
    elif negative > positive:
        trend = "pressure"
        trend_hi = "\u0926\u092c\u093e\u0935"
    else:
        trend = "neutral"
        trend_hi = "\u0924\u091f\u0938\u094d\u0925"

    return {
        "trend": {"en": trend, "hi": trend_hi},
        "positive_score": positive,
        "negative_score": negative,
        "factors": factors,
    }


# ============================================================
# 7. POLITICAL INDICATORS (10th house + Sun/Saturn)
# ============================================================

def _political_indicators(
    transit_planets: List[Dict[str, Any]],
    asc_sign: str,
) -> Dict[str, Any]:
    """10th house analysis + Sun and Saturn positions for governance outlook."""
    planet_data: Dict[str, Dict[str, Any]] = {}
    for t in transit_planets:
        planet_data[t["planet"]] = t

    factors: List[Dict[str, Any]] = []
    stability_score = 0  # positive = stable, negative = unstable

    sun = planet_data.get("Sun")
    if sun:
        h = _house_number(sun["sign"], asc_sign)
        if h == 10:
            stability_score += 2
            factors.append({
                "planet": "Sun",
                "house": h,
                "effect": {
                    "en": "Sun in the 10th house strengthens government authority and leadership visibility",
                    "hi": "\u0938\u0942\u0930\u094d\u092f \u0926\u0938\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0938\u0930\u0915\u093e\u0930\u0940 \u0938\u0924\u094d\u0924\u093e \u0914\u0930 \u0928\u0947\u0924\u0943\u0924\u094d\u0935 \u0926\u0943\u0936\u094d\u092f\u0924\u093e \u0915\u094b \u092e\u091c\u093c\u092c\u0942\u0924 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })
        elif h in (6, 8, 12):
            stability_score -= 1
            factors.append({
                "planet": "Sun",
                "house": h,
                "effect": {
                    "en": f"Sun in the {h}th house weakens government image — leadership faces criticism or health concerns",
                    "hi": f"\u0938\u0942\u0930\u094d\u092f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0938\u0930\u0915\u093e\u0930\u0940 \u091b\u0935\u093f \u0915\u092e\u091c\u093c\u094b\u0930 \u2014 \u0928\u0947\u0924\u0943\u0924\u094d\u0935 \u0906\u0932\u094b\u091a\u0928\u093e \u092f\u093e \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u091a\u093f\u0902\u0924\u093e\u0913\u0902 \u0915\u093e \u0938\u093e\u092e\u0928\u093e \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })

    saturn = planet_data.get("Saturn")
    if saturn:
        h = _house_number(saturn["sign"], asc_sign)
        if h == 10:
            stability_score -= 2
            factors.append({
                "planet": "Saturn",
                "house": h,
                "effect": {
                    "en": "Saturn in the 10th house brings heavy pressure on government — restructuring, public discontent, leadership challenges",
                    "hi": "\u0936\u0928\u093f \u0926\u0938\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0938\u0930\u0915\u093e\u0930 \u092a\u0930 \u092d\u093e\u0930\u0940 \u0926\u092c\u093e\u0935 \u2014 \u092a\u0941\u0928\u0930\u094d\u0917\u0920\u0928, \u091c\u0928 \u0905\u0938\u0902\u0924\u094b\u0937, \u0928\u0947\u0924\u0943\u0924\u094d\u0935 \u091a\u0941\u0928\u094c\u0924\u093f\u092f\u093e\u0901",
                },
            })
        elif h in (3, 6, 11):
            stability_score += 1
            factors.append({
                "planet": "Saturn",
                "house": h,
                "effect": {
                    "en": f"Saturn in the {h}{'rd' if h == 3 else 'th'} house supports governmental discipline and policy execution",
                    "hi": f"\u0936\u0928\u093f {h}\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0938\u0930\u0915\u093e\u0930\u0940 \u0905\u0928\u0941\u0936\u093e\u0938\u0928 \u0914\u0930 \u0928\u0940\u0924\u093f \u0915\u093e\u0930\u094d\u092f\u093e\u0928\u094d\u0935\u092f\u0928 \u0915\u093e \u0938\u092e\u0930\u094d\u0925\u0928 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })

    # Rahu in 10th — unconventional leadership
    rahu = planet_data.get("Rahu")
    if rahu:
        h = _house_number(rahu["sign"], asc_sign)
        if h == 10:
            stability_score -= 1
            factors.append({
                "planet": "Rahu",
                "house": h,
                "effect": {
                    "en": "Rahu in the 10th house brings unconventional governance, scandals, or deceptive leadership",
                    "hi": "\u0930\u093e\u0939\u0941 \u0926\u0938\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0905\u092a\u0930\u0902\u092a\u0930\u093e\u0917\u0924 \u0936\u093e\u0938\u0928, \u0918\u094b\u091f\u093e\u0932\u0947 \u092f\u093e \u092d\u094d\u0930\u093e\u092e\u0915 \u0928\u0947\u0924\u0943\u0924\u094d\u0935 \u0932\u093e\u0924\u093e \u0939\u0948",
                },
            })

    if stability_score >= 2:
        status = "stable"
        status_hi = "\u0938\u094d\u0925\u093f\u0930"
    elif stability_score <= -2:
        status = "unstable"
        status_hi = "\u0905\u0938\u094d\u0925\u093f\u0930"
    else:
        status = "pressured"
        status_hi = "\u0926\u092c\u093e\u0935 \u092e\u0947\u0902"

    return {
        "government_stability": {"en": status, "hi": status_hi},
        "stability_score": stability_score,
        "factors": factors,
    }


# ============================================================
# 8. HEALTH INDICATORS (6th house + malefics)
# ============================================================

def _health_indicators(
    transit_planets: List[Dict[str, Any]],
    asc_sign: str,
) -> Dict[str, Any]:
    """Assess public health outlook from 6th house transits."""
    planet_data: Dict[str, Dict[str, Any]] = {}
    for t in transit_planets:
        planet_data[t["planet"]] = t

    factors: List[Dict[str, Any]] = []
    risk_score = 0

    for pname in _MALEFICS:
        p = planet_data.get(pname)
        if not p:
            continue
        h = _house_number(p["sign"], asc_sign)
        if h == 6:
            risk_score += 1
            factors.append({
                "planet": pname,
                "house": h,
                "effect": {
                    "en": f"{pname} in the 6th house raises public health concerns — epidemics, workplace injuries, or healthcare strain",
                    "hi": f"{pname} \u091b\u0920\u0947 \u092d\u093e\u0935 \u092e\u0947\u0902 \u091c\u0928 \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u091a\u093f\u0902\u0924\u093e\u090f\u0901 \u092c\u0922\u093c\u093e\u0924\u093e \u0939\u0948 \u2014 \u092e\u0939\u093e\u092e\u093e\u0930\u0940, \u0915\u093e\u0930\u094d\u092f\u0938\u094d\u0925\u0932 \u0926\u0941\u0930\u094d\u0918\u091f\u0928\u093e\u090f\u0901 \u092f\u093e \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0938\u0947\u0935\u093e \u092a\u0930 \u0926\u092c\u093e\u0935",
                },
            })
        elif h == 1:
            risk_score += 1
            factors.append({
                "planet": pname,
                "house": h,
                "effect": {
                    "en": f"{pname} in the 1st house affects general public well-being and national vitality",
                    "hi": f"{pname} \u092a\u0939\u0932\u0947 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0938\u093e\u092e\u093e\u0928\u094d\u092f \u091c\u0928 \u0915\u0932\u094d\u092f\u093e\u0923 \u0914\u0930 \u0930\u093e\u0937\u094d\u091f\u094d\u0930\u0940\u092f \u091c\u0940\u0935\u0928\u0936\u0915\u094d\u0924\u093f \u0915\u094b \u092a\u094d\u0930\u092d\u093e\u0935\u093f\u0924 \u0915\u0930\u0924\u093e \u0939\u0948",
                },
            })

    # Benefics in 6th can mitigate
    for pname in _BENEFICS:
        p = planet_data.get(pname)
        if p:
            h = _house_number(p["sign"], asc_sign)
            if h == 6:
                risk_score -= 1
                factors.append({
                    "planet": pname,
                    "house": h,
                    "effect": {
                        "en": f"{pname} in the 6th house provides healing energy and improved health services",
                        "hi": f"{pname} \u091b\u0920\u0947 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0909\u092a\u091a\u093e\u0930 \u090a\u0930\u094d\u091c\u093e \u0914\u0930 \u092c\u0947\u0939\u0924\u0930 \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0938\u0947\u0935\u093e\u090f\u0901 \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u0930\u0924\u093e \u0939\u0948",
                    },
                })

    if risk_score <= 0:
        level = "low"
        level_hi = "\u0915\u092e"
    elif risk_score <= 2:
        level = "medium"
        level_hi = "\u092e\u0927\u094d\u092f\u092e"
    else:
        level = "high"
        level_hi = "\u0909\u091a\u094d\u091a"

    return {
        "risk_level": {"en": level, "hi": level_hi},
        "risk_score": risk_score,
        "factors": factors,
    }


# ============================================================
# 9. INTERNATIONAL RELATIONS (7th house analysis)
# ============================================================

def _international_relations(
    transit_planets: List[Dict[str, Any]],
    asc_sign: str,
) -> Dict[str, Any]:
    """Assess foreign relations from the 7th house and its transiting planets."""
    planet_data: Dict[str, Dict[str, Any]] = {}
    for t in transit_planets:
        planet_data[t["planet"]] = t

    factors: List[Dict[str, Any]] = []
    harmony_score = 0

    for pname, p in planet_data.items():
        h = _house_number(p["sign"], asc_sign)
        if h == 7:
            if pname in _BENEFICS:
                harmony_score += 1
                factors.append({
                    "planet": pname,
                    "house": 7,
                    "effect": {
                        "en": f"{pname} in the 7th house promotes diplomatic success, treaty progress, and foreign goodwill",
                        "hi": f"{pname} \u0938\u093e\u0924\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0930\u093e\u091c\u0928\u092f\u093f\u0915 \u0938\u092b\u0932\u0924\u093e, \u0938\u0902\u0927\u093f \u092a\u094d\u0930\u0917\u0924\u093f \u0914\u0930 \u0935\u093f\u0926\u0947\u0936\u0940 \u0938\u0926\u094d\u092d\u093e\u0935\u0928\u093e \u0915\u094b \u092c\u0922\u093c\u093e\u0935\u093e \u0926\u0947\u0924\u093e \u0939\u0948",
                    },
                })
            elif pname in _MALEFICS:
                harmony_score -= 1
                factors.append({
                    "planet": pname,
                    "house": 7,
                    "effect": {
                        "en": f"{pname} in the 7th house heightens foreign tensions, border disputes, or war rhetoric",
                        "hi": f"{pname} \u0938\u093e\u0924\u0935\u0947\u0902 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0935\u093f\u0926\u0947\u0936\u0940 \u0924\u0928\u093e\u0935, \u0938\u0940\u092e\u093e \u0935\u093f\u0935\u093e\u0926 \u092f\u093e \u092f\u0941\u0926\u094d\u0927 \u0915\u0940 \u092c\u092f\u093e\u0928\u092c\u093e\u091c\u093c\u0940 \u092c\u0922\u093c\u093e\u0924\u093e \u0939\u0948",
                    },
                })

    if harmony_score >= 1:
        outlook = "peaceful"
        outlook_hi = "\u0936\u093e\u0902\u0924\u093f\u092a\u0942\u0930\u094d\u0923"
    elif harmony_score <= -1:
        outlook = "tense"
        outlook_hi = "\u0924\u0928\u093e\u0935\u092a\u0942\u0930\u094d\u0923"
    else:
        outlook = "neutral"
        outlook_hi = "\u0924\u091f\u0938\u094d\u0925"

    return {
        "outlook": {"en": outlook, "hi": outlook_hi},
        "harmony_score": harmony_score,
        "factors": factors,
    }


# ============================================================
# 10. ECLIPSE CALCULATOR
# ============================================================

# Hardcoded known eclipses 2024-2027 (type, date, visibility, kind)
_KNOWN_ECLIPSES: List[Dict[str, Any]] = [
    # 2024
    {"date": "2024-03-25", "type": "lunar", "kind": "penumbral",
     "visibility": {"en": "Americas, Europe, Africa", "hi": "\u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092f\u0942\u0930\u094b\u092a, \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2024-04-08", "type": "solar", "kind": "total",
     "visibility": {"en": "North America, Mexico", "hi": "\u0909\u0924\u094d\u0924\u0930\u0940 \u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092e\u0947\u0915\u094d\u0938\u093f\u0915\u094b"}},
    {"date": "2024-09-18", "type": "lunar", "kind": "partial",
     "visibility": {"en": "Americas, Europe, Africa", "hi": "\u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092f\u0942\u0930\u094b\u092a, \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2024-10-02", "type": "solar", "kind": "annular",
     "visibility": {"en": "South America, Pacific", "hi": "\u0926\u0915\u094d\u0937\u093f\u0923 \u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092a\u094d\u0930\u0936\u093e\u0902\u0924 \u092e\u0939\u093e\u0938\u093e\u0917\u0930"}},
    # 2025
    {"date": "2025-03-14", "type": "lunar", "kind": "total",
     "visibility": {"en": "Americas, Europe, Africa", "hi": "\u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092f\u0942\u0930\u094b\u092a, \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2025-03-29", "type": "solar", "kind": "partial",
     "visibility": {"en": "Europe, North Africa, West Asia", "hi": "\u092f\u0942\u0930\u094b\u092a, \u0909\u0924\u094d\u0924\u0930 \u0905\u092b\u094d\u0930\u0940\u0915\u093e, \u092a\u0936\u094d\u091a\u093f\u092e \u090f\u0936\u093f\u092f\u093e"}},
    {"date": "2025-09-07", "type": "lunar", "kind": "total",
     "visibility": {"en": "Europe, Africa, Asia, Australia", "hi": "\u092f\u0942\u0930\u094b\u092a, \u0905\u092b\u094d\u0930\u0940\u0915\u093e, \u090f\u0936\u093f\u092f\u093e, \u0911\u0938\u094d\u091f\u094d\u0930\u0947\u0932\u093f\u092f\u093e"}},
    {"date": "2025-09-21", "type": "solar", "kind": "partial",
     "visibility": {"en": "South Pacific, Antarctica, New Zealand", "hi": "\u0926\u0915\u094d\u0937\u093f\u0923 \u092a\u094d\u0930\u0936\u093e\u0902\u0924 \u092e\u0939\u093e\u0938\u093e\u0917\u0930, \u0905\u0902\u091f\u093e\u0930\u094d\u0915\u091f\u093f\u0915\u093e, \u0928\u094d\u092f\u0942\u091c\u0940\u0932\u0948\u0902\u0921"}},
    # 2026
    {"date": "2026-02-17", "type": "solar", "kind": "annular",
     "visibility": {"en": "Antarctica, South America, Africa", "hi": "\u0905\u0902\u091f\u093e\u0930\u094d\u0915\u091f\u093f\u0915\u093e, \u0926\u0915\u094d\u0937\u093f\u0923 \u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2026-03-03", "type": "lunar", "kind": "total",
     "visibility": {"en": "East Asia, Australia, Pacific, Americas", "hi": "\u092a\u0942\u0930\u094d\u0935 \u090f\u0936\u093f\u092f\u093e, \u0911\u0938\u094d\u091f\u094d\u0930\u0947\u0932\u093f\u092f\u093e, \u092a\u094d\u0930\u0936\u093e\u0902\u0924 \u092e\u0939\u093e\u0938\u093e\u0917\u0930, \u0905\u092e\u0947\u0930\u093f\u0915\u093e"}},
    {"date": "2026-08-12", "type": "solar", "kind": "total",
     "visibility": {"en": "Arctic, Europe, North Africa", "hi": "\u0906\u0930\u094d\u0915\u091f\u093f\u0915, \u092f\u0942\u0930\u094b\u092a, \u0909\u0924\u094d\u0924\u0930 \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2026-08-28", "type": "lunar", "kind": "partial",
     "visibility": {"en": "East Asia, Pacific, Americas", "hi": "\u092a\u0942\u0930\u094d\u0935 \u090f\u0936\u093f\u092f\u093e, \u092a\u094d\u0930\u0936\u093e\u0902\u0924 \u092e\u0939\u093e\u0938\u093e\u0917\u0930, \u0905\u092e\u0947\u0930\u093f\u0915\u093e"}},
    # 2027
    {"date": "2027-02-06", "type": "solar", "kind": "annular",
     "visibility": {"en": "South America, Antarctica, Africa", "hi": "\u0926\u0915\u094d\u0937\u093f\u0923 \u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u0905\u0902\u091f\u093e\u0930\u094d\u0915\u091f\u093f\u0915\u093e, \u0905\u092b\u094d\u0930\u0940\u0915\u093e"}},
    {"date": "2027-02-20", "type": "lunar", "kind": "penumbral",
     "visibility": {"en": "Americas, Europe, Africa, West Asia", "hi": "\u0905\u092e\u0947\u0930\u093f\u0915\u093e, \u092f\u0942\u0930\u094b\u092a, \u0905\u092b\u094d\u0930\u0940\u0915\u093e, \u092a\u0936\u094d\u091a\u093f\u092e \u090f\u0936\u093f\u092f\u093e"}},
    {"date": "2027-07-18", "type": "lunar", "kind": "penumbral",
     "visibility": {"en": "Asia, Australia, Pacific, Americas", "hi": "\u090f\u0936\u093f\u092f\u093e, \u0911\u0938\u094d\u091f\u094d\u0930\u0947\u0932\u093f\u092f\u093e, \u092a\u094d\u0930\u0936\u093e\u0902\u0924 \u092e\u0939\u093e\u0938\u093e\u0917\u0930, \u0905\u092e\u0947\u0930\u093f\u0915\u093e"}},
    {"date": "2027-08-02", "type": "solar", "kind": "total",
     "visibility": {"en": "North Africa, Europe, Middle East", "hi": "\u0909\u0924\u094d\u0924\u0930 \u0905\u092b\u094d\u0930\u0940\u0915\u093e, \u092f\u0942\u0930\u094b\u092a, \u092e\u0927\u094d\u092f \u092a\u0942\u0930\u094d\u0935"}},
]


def _eclipse_house_in_chart(eclipse_date: str, asc_sign: str, eclipse_type: str) -> int:
    """
    Determine which house of a country chart an eclipse affects.
    Solar eclipse = Sun's sign, Lunar eclipse = Moon's sign at that date.
    """
    result = calculate_planet_positions(eclipse_date, "12:00:00", 0.0, 0.0, 0.0)
    planets = result.get("planets", {})
    if eclipse_type == "solar":
        sun_sign = planets.get("Sun", {}).get("sign", "Aries")
        return _house_number(sun_sign, asc_sign)
    else:
        moon_sign = planets.get("Moon", {}).get("sign", "Aries")
        return _house_number(moon_sign, asc_sign)


def calculate_eclipses(
    year: int,
    country_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Return eclipse data for a given year. If country_key is provided, also
    compute which house of the country chart each eclipse falls in.
    """
    eclipses = [e for e in _KNOWN_ECLIPSES if e["date"].startswith(str(year))]

    asc_sign: Optional[str] = None
    if country_key:
        chart_info = COUNTRY_CHARTS.get(country_key)
        if chart_info:
            birth = calculate_planet_positions(
                chart_info["date"], chart_info["time"],
                chart_info["lat"], chart_info["lon"], chart_info["tz"],
            )
            asc_sign = birth.get("ascendant", {}).get("sign")

    result: List[Dict[str, Any]] = []
    for e in eclipses:
        entry: Dict[str, Any] = {
            "date": e["date"],
            "type": {"en": e["type"], "hi": "\u0938\u0942\u0930\u094d\u092f \u0917\u094d\u0930\u0939\u0923" if e["type"] == "solar" else "\u091a\u0902\u0926\u094d\u0930 \u0917\u094d\u0930\u0939\u0923"},
            "kind": {"en": e["kind"], "hi": _eclipse_kind_hi(e["kind"])},
            "visibility": e["visibility"],
        }
        if asc_sign:
            house = _eclipse_house_in_chart(e["date"], asc_sign, e["type"])
            entry["affected_house"] = house
            entry["affected_domain"] = MUNDANE_HOUSES.get(house, {"en": "", "hi": ""})
        result.append(entry)

    return result


def _eclipse_kind_hi(kind: str) -> str:
    """Hindi label for eclipse kind."""
    return {
        "total": "\u092a\u0942\u0930\u094d\u0923",
        "partial": "\u0906\u0902\u0936\u093f\u0915",
        "annular": "\u0935\u0932\u092f\u093e\u0915\u093e\u0930",
        "penumbral": "\u091b\u093e\u092f\u093e",
    }.get(kind, kind)


# ============================================================
# 11. INGRESS / SANKRANTI CALCULATOR
# ============================================================

def calculate_ingress(year: int) -> List[Dict[str, Any]]:
    """
    Find approximate dates when the Sun enters each of the 12 sidereal signs
    (Sankranti dates) for a given year.

    Uses a binary search on Sun's sidereal longitude to find sign boundaries.
    """
    results: List[Dict[str, Any]] = []
    _SIGN_NAMES_HI = [
        "\u092e\u0947\u0937", "\u0935\u0943\u0937\u092d", "\u092e\u093f\u0925\u0941\u0928",
        "\u0915\u0930\u094d\u0915", "\u0938\u093f\u0902\u0939", "\u0915\u0928\u094d\u092f\u093e",
        "\u0924\u0941\u0932\u093e", "\u0935\u0943\u0936\u094d\u091a\u093f\u0915",
        "\u0927\u0928\u0941", "\u092e\u0915\u0930", "\u0915\u0941\u092e\u094d\u092d",
        "\u092e\u0940\u0928",
    ]
    _SANKRANTI_NAMES = [
        "Mesha Sankranti", "Vrishabha Sankranti", "Mithuna Sankranti",
        "Karka Sankranti", "Simha Sankranti", "Kanya Sankranti",
        "Tula Sankranti", "Vrischika Sankranti", "Dhanu Sankranti",
        "Makara Sankranti", "Kumbha Sankranti", "Meena Sankranti",
    ]
    _SANKRANTI_NAMES_HI = [
        "\u092e\u0947\u0937 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0935\u0943\u0937\u092d \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u092e\u093f\u0925\u0941\u0928 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0915\u0930\u094d\u0915 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0938\u093f\u0902\u0939 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0915\u0928\u094d\u092f\u093e \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0924\u0941\u0932\u093e \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0935\u0943\u0936\u094d\u091a\u093f\u0915 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0927\u0928\u0941 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u092e\u0915\u0930 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u0915\u0941\u092e\u094d\u092d \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
        "\u092e\u0940\u0928 \u0938\u0902\u0915\u094d\u0930\u093e\u0902\u0924\u093f",
    ]

    for sign_idx in range(12):
        target_lon = sign_idx * 30.0  # sidereal boundary
        date_str = _find_sun_ingress_date(year, target_lon)
        results.append({
            "sign": {"en": _SIGN_NAMES[sign_idx], "hi": _SIGN_NAMES_HI[sign_idx]},
            "sankranti": {"en": _SANKRANTI_NAMES[sign_idx], "hi": _SANKRANTI_NAMES_HI[sign_idx]},
            "date": date_str,
            "degree": target_lon,
        })

    return results


def _get_sidereal_sun_longitude(date_str: str) -> float:
    """Get sidereal Sun longitude for a date at noon UTC."""
    result = calculate_planet_positions(date_str, "12:00:00", 0.0, 0.0, 0.0)
    return result.get("planets", {}).get("Sun", {}).get("longitude", 0.0)


def _find_sun_ingress_date(year: int, target_lon: float) -> str:
    """
    Binary search to find the date when sidereal Sun crosses target_lon.
    Returns ISO date string.
    """
    from datetime import date as date_type, timedelta

    # Approximate month when Sun enters each sign (sidereal, ~23 days behind tropical)
    # Aries~Apr14, Taurus~May15, Gemini~Jun15, Cancer~Jul17, Leo~Aug17, Virgo~Sep17
    # Libra~Oct18, Scorpio~Nov16, Sag~Dec16, Capricorn~Jan14, Aquarius~Feb13, Pisces~Mar14
    _APPROX_MONTHS = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    _APPROX_DAYS = [14, 15, 15, 17, 17, 17, 18, 16, 16, 14, 13, 14]

    sign_idx = int(target_lon / 30.0) % 12
    m = _APPROX_MONTHS[sign_idx]
    d = _APPROX_DAYS[sign_idx]

    # For Capricorn/Aquarius/Pisces, the year is the same calendar year (Jan-Mar)
    search_year = year if m >= 4 else year
    try:
        start = date_type(search_year, m, d) - timedelta(days=20)
    except ValueError:
        start = date_type(search_year, m, 1)
    end = start + timedelta(days=40)

    # Binary search for the crossing
    for _ in range(30):  # ~30 iterations gives sub-hour precision
        if (end - start).days <= 0:
            break
        mid = start + (end - start) / 2
        mid_str = mid.isoformat() if hasattr(mid, 'isoformat') else str(mid)

        sun_lon = _get_sidereal_sun_longitude(mid_str)

        # Handle wrap-around at 0/360
        diff = (sun_lon - target_lon) % 360.0
        if diff > 180.0:
            diff -= 360.0

        if diff < 0:
            # Sun hasn't reached target yet — search later
            start = mid + timedelta(days=1) if (end - mid).days > 1 else mid
        else:
            end = mid

    return start.isoformat()


# ============================================================
# 12. SUMMARY BUILDER
# ============================================================

def _build_summary(
    house_analysis: List[Dict[str, Any]],
    political: Dict[str, Any],
    economic: Dict[str, Any],
    health: Dict[str, Any],
    conflict: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build the top-level summary object from sub-analyses."""
    # National mood from 1st house
    first_house = house_analysis[0] if house_analysis else {}
    first_condition = first_house.get("condition", {}).get("en", "neutral")
    if "Positive" in first_condition:
        mood = "positive"
        mood_hi = "\u0938\u0915\u093e\u0930\u093e\u0924\u094d\u092e\u0915"
    elif "Pressured" in first_condition:
        mood = "negative"
        mood_hi = "\u0928\u0915\u093e\u0930\u093e\u0924\u094d\u092e\u0915"
    else:
        mood = "neutral"
        mood_hi = "\u0924\u091f\u0938\u094d\u0925"

    # Risk level from conflict indicators
    high_count = sum(1 for c in conflict if c.get("severity") == "high")
    medium_count = sum(1 for c in conflict if c.get("severity") == "medium")
    if high_count >= 2:
        risk = "high"
        risk_hi = "\u0909\u091a\u094d\u091a"
    elif high_count >= 1 or medium_count >= 3:
        risk = "medium"
        risk_hi = "\u092e\u0927\u094d\u092f\u092e"
    else:
        risk = "low"
        risk_hi = "\u0915\u092e"

    return {
        "national_mood": {"en": mood, "hi": mood_hi},
        "government_stability": political.get("government_stability", {"en": "unknown", "hi": "\u0905\u091c\u094d\u091e\u093e\u0924"}),
        "economy_trend": economic.get("trend", {"en": "neutral", "hi": "\u0924\u091f\u0938\u094d\u0925"}),
        "risk_level": {"en": risk, "hi": risk_hi},
    }


# ============================================================
# 13. MAIN ANALYSIS FUNCTION
# ============================================================

def calculate_mundane_analysis(
    country_key: str,
    year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Full mundane astrology analysis for a country.

    Args:
        country_key: lowercase key into COUNTRY_CHARTS (e.g. "india")
        year: optional year for eclipse/ingress data (defaults to current year)

    Returns:
        Complete analysis dict with birth chart, transits, house analysis,
        conflict/economic/political/health/international indicators, eclipses,
        ingress data, and a top-level summary.
    """
    chart_info = COUNTRY_CHARTS.get(country_key)
    if not chart_info:
        return {"error": {"en": f"Country '{country_key}' not found", "hi": f"'\u0926\u0947\u0936 '{country_key}' \u0928\u0939\u0940\u0902 \u092e\u093f\u0932\u093e"}}

    if year is None:
        year = datetime.now(timezone.utc).year

    # 1. Country birth chart
    birth_chart = calculate_planet_positions(
        chart_info["date"], chart_info["time"],
        chart_info["lat"], chart_info["lon"], chart_info["tz"],
    )
    asc_sign = birth_chart.get("ascendant", {}).get("sign", "Aries")

    # 2. Current transits in country chart
    transits = _current_transits_in_country_chart(chart_info, birth_chart)

    # 3. House analysis
    house_analysis = _analyze_houses(birth_chart, transits)

    # 4. Indicators
    conflict = _conflict_indicators(transits, asc_sign)
    economic = _economic_indicators(transits, asc_sign)
    political = _political_indicators(transits, asc_sign)
    health = _health_indicators(transits, asc_sign)
    international = _international_relations(transits, asc_sign)

    # 5. Summary
    summary = _build_summary(house_analysis, political, economic, health, conflict)

    # 6. Country info (bilingual)
    country_info = {
        "key": country_key,
        "name": {"en": chart_info["name"], "hi": chart_info["name_hi"]},
        "capital": {"en": chart_info["capital"], "hi": chart_info["capital_hi"]},
        "independence_date": chart_info["date"],
        "independence_time": chart_info["time"],
        "description": chart_info["description"],
    }

    return {
        "country": country_info,
        "birth_chart": birth_chart,
        "current_transits": transits,
        "house_analysis": house_analysis,
        "summary": summary,
        "conflict_indicators": conflict,
        "economic_indicators": economic,
        "political_indicators": political,
        "health_indicators": health,
        "international_relations": international,
    }
