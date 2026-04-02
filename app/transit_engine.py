"""
transit_engine.py -- Gochara (Transit) Prediction Engine
========================================================
Calculates current planetary transits and evaluates their effects
on a natal chart using classical Vedic Gochara rules (transit of
planets counted from the natal Moon sign).

Provides:
  - calculate_transits(natal_chart_data) -> transit results + Sade Sati status
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from app.astro_engine import calculate_planet_positions, _SIGN_NAMES


# ── Zodiac helpers ─────────────────────────────────────────────

ZODIAC_INDEX: Dict[str, int] = {sign: i for i, sign in enumerate(_SIGN_NAMES)}


def _house_from_moon(moon_sign: str, transit_sign: str) -> int:
    """
    Return the house number (1-12) of transit_sign counted from moon_sign.
    House 1 = same sign as Moon.
    """
    moon_idx = ZODIAC_INDEX.get(moon_sign, 0)
    transit_idx = ZODIAC_INDEX.get(transit_sign, 0)
    return ((transit_idx - moon_idx) % 12) + 1


# ── Gochara favourability rules ───────────────────────────────
# Key = planet name, Value = set of house numbers (from Moon) that are favourable.

GOCHARA_FAVORABLE: Dict[str, set] = {
    "Jupiter":  {2, 5, 7, 9, 11},
    "Saturn":   {3, 6, 11},
    "Rahu":     {3, 6, 11},
    "Ketu":     {3, 6, 11},
    "Mars":     {3, 6, 11},
    "Venus":    {1, 2, 3, 4, 5, 8, 9, 11, 12},
    "Sun":      {3, 6, 10, 11},
    "Mercury":  {2, 4, 6, 8, 10, 11},
    "Moon":     {1, 3, 6, 7, 10, 11},
}

# ── Gochara descriptions per planet ───────────────────────────

_FAVORABLE_DESC: Dict[str, str] = {
    "Jupiter":  "Jupiter's benevolent transit brings expansion, wisdom, and opportunities in this area of life.",
    "Saturn":   "Saturn's transit here gives discipline, endurance, and eventual rewards through hard work.",
    "Rahu":     "Rahu's transit here can bring unconventional gains and bold breakthroughs.",
    "Ketu":     "Ketu's transit here supports spiritual detachment and release of old patterns.",
    "Mars":     "Mars transiting here channels energy productively — courage and initiative are favored.",
    "Venus":    "Venus brings harmony, comfort, and pleasurable experiences during this transit.",
    "Sun":      "The Sun's transit here strengthens authority, confidence, and recognition.",
    "Mercury":  "Mercury's transit here sharpens intellect, communication, and business acumen.",
    "Moon":     "The Moon's transit here brings emotional balance and mental peace.",
}

_UNFAVORABLE_DESC: Dict[str, str] = {
    "Jupiter":  "Jupiter's transit through this house may bring overconfidence or misplaced optimism. Practice discernment.",
    "Saturn":   "Saturn's transit here can bring delays, restrictions, and lessons through hardship. Patience is key.",
    "Rahu":     "Rahu's transit here may create confusion, obsessive desires, or unexpected disruptions.",
    "Ketu":     "Ketu's transit here may bring loss, detachment, or spiritual confusion. Inner reflection is advised.",
    "Mars":     "Mars transiting here may cause conflicts, accidents, or impulsive decisions. Exercise caution.",
    "Venus":    "Venus transiting here may bring relationship tensions or overindulgence. Maintain balance.",
    "Sun":      "The Sun's transit here may challenge ego, vitality, or relations with authority figures.",
    "Mercury":  "Mercury's transit here may cause miscommunication, errors in judgment, or mental restlessness.",
    "Moon":     "The Moon's transit here may bring emotional turbulence, anxiety, or domestic unease.",
}


# ── Sade Sati detection ───────────────────────────────────────

def _check_sade_sati(moon_sign: str, saturn_sign: str) -> Dict[str, Any]:
    """
    Determine Sade Sati status from Moon sign and current Saturn sign.

    Sade Sati is active when Saturn transits:
      - 12th from Moon (rising phase)
      - 1st from Moon / same sign (peak phase)
      - 2nd from Moon (setting phase)
    """
    moon_idx = ZODIAC_INDEX.get(moon_sign, 0)
    saturn_idx = ZODIAC_INDEX.get(saturn_sign, 0)

    house = ((saturn_idx - moon_idx) % 12) + 1

    if house == 12:
        return {
            "active": True,
            "phase": "Rising (12th from Moon)",
            "description": (
                "Sade Sati is beginning. Saturn transits the 12th house from your Moon sign. "
                "This phase often brings increased expenses, sleep disturbances, and a period of "
                "introspection. Mental peace may be challenged."
            ),
        }
    elif house == 1:
        return {
            "active": True,
            "phase": "Peak (over natal Moon)",
            "description": (
                "Sade Sati is at its peak. Saturn transits directly over your natal Moon. "
                "This is the most intense phase — expect emotional pressure, career challenges, "
                "and transformation. Persistence and devotion to duty are the remedies."
            ),
        }
    elif house == 2:
        return {
            "active": True,
            "phase": "Setting (2nd from Moon)",
            "description": (
                "Sade Sati is in its final phase. Saturn transits the 2nd house from your Moon. "
                "Financial pressures and family concerns may arise, but the worst is behind you. "
                "This phase brings consolidation of lessons learned."
            ),
        }
    else:
        return {
            "active": False,
            "phase": "Not active",
            "description": "Sade Sati is not currently active for your chart.",
        }


# ── Main transit calculation ──────────────────────────────────

def calculate_transits(natal_chart_data: Dict[str, Any], latitude: float = 0.0, longitude: float = 0.0) -> Dict[str, Any]:
    """
    Calculate current planetary transits and their Gochara effects on a natal chart.

    Args:
        natal_chart_data: The stored chart_data dict from a kundli row,
                          containing planets -> {sign, house, ...} and ascendant.
        latitude:  Observer latitude for ascendant calculation (default 0.0).
        longitude: Observer longitude for ascendant calculation (default 0.0).

    Returns:
        {
            "transits": [
                {
                    "planet": str,
                    "current_sign": str,
                    "natal_house_from_moon": int,
                    "effect": "favorable" | "unfavorable",
                    "description": str,
                }
            ],
            "sade_sati": {
                "active": bool,
                "phase": str,
                "description": str,
            },
            "transit_date": str,  # ISO date of transit calculation
        }
    """
    # Calculate current planetary positions using the birth location for correct ascendant.
    # Planet longitudes are nearly location-independent, but the ascendant (Lagna)
    # depends heavily on the observer's latitude and longitude.
    now_utc = datetime.now(timezone.utc)

    # Approximate timezone offset from longitude (15° per hour)
    tz_offset = round(longitude / 15.0 * 2) / 2  # round to nearest 0.5
    local_now = now_utc + timedelta(hours=tz_offset)
    today_str = local_now.strftime("%Y-%m-%d")
    time_str = local_now.strftime("%H:%M:%S")

    current_positions = calculate_planet_positions(
        birth_date=today_str,
        birth_time=time_str,
        latitude=latitude,
        longitude=longitude,
        tz_offset=tz_offset,
    )

    # Extract natal Moon sign
    natal_planets = natal_chart_data.get("planets", {})
    natal_moon = natal_planets.get("Moon", {})
    natal_moon_sign = natal_moon.get("sign", "Aries")

    # Build transit results
    transits: List[Dict[str, Any]] = []
    current_planets = current_positions.get("planets", {})
    saturn_current_sign = "Capricorn"  # fallback

    for planet_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        planet_info = current_planets.get(planet_name, {})
        current_sign = planet_info.get("sign", "Aries")

        if planet_name == "Saturn":
            saturn_current_sign = current_sign

        house_from_moon = _house_from_moon(natal_moon_sign, current_sign)
        favorable_houses = GOCHARA_FAVORABLE.get(planet_name, set())
        is_favorable = house_from_moon in favorable_houses
        effect = "favorable" if is_favorable else "unfavorable"

        description = (
            _FAVORABLE_DESC.get(planet_name, "")
            if is_favorable
            else _UNFAVORABLE_DESC.get(planet_name, "")
        )
        # Add house context to description
        description += f" (Transiting house {house_from_moon} from Moon in {natal_moon_sign})"

        transits.append({
            "planet": planet_name,
            "current_sign": current_sign,
            "sign_degree": round(planet_info.get("sign_degree", 0.0), 1),
            "house": planet_info.get("house", 1),
            "nakshatra": planet_info.get("nakshatra", ""),
            "is_retrograde": planet_info.get("retrograde", False),
            "natal_house_from_moon": house_from_moon,
            "effect": effect,
            "description": description,
        })

    # Sade Sati check
    sade_sati = _check_sade_sati(natal_moon_sign, saturn_current_sign)

    return {
        "transits": transits,
        "sade_sati": sade_sati,
        "transit_date": today_str,
        "natal_moon_sign": natal_moon_sign,
        "chart_data": {
            "ascendant": current_positions.get("ascendant"),
            "houses": current_positions.get("houses"),
        },
    }
