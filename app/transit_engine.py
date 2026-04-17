"""
transit_engine.py -- Core Horoscope Assembly Engine (Transit-Based)
===================================================================
Takes real planetary positions from the Swiss Ephemeris engine and produces
structured, bilingual (en/hi) horoscope content using an interpretation matrix.

Pure functions -- no DB access, no side effects, just computation.

Provides:
  - get_full_transits(target_date)           -> raw planet data
  - calculate_transit_houses(sign, planets)  -> planet-to-house mapping
  - get_planet_dignity(planet, planet_info)  -> dignity classification
  - assemble_section(...)                    -> paragraph for one area
  - compute_scores(...)                      -> numeric scores per area
  - generate_transit_horoscope(sign, period) -> complete horoscope response
  - generate_monthly_extras(sign, date)      -> month phases + key dates
  - generate_yearly_extras(sign, year)       -> quarterly themes + best months
"""
from __future__ import annotations

import calendar
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.astro_engine import calculate_planet_positions

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy imports for interpretation data (modules may not exist yet)
# ---------------------------------------------------------------------------
try:
    from app.transit_interpretations import TRANSIT_FRAGMENTS, DIGNITY_MODIFIERS
except ImportError:
    TRANSIT_FRAGMENTS: Dict[str, Dict[int, Dict[str, Dict[str, str]]]] = {}
    DIGNITY_MODIFIERS: Dict[str, Dict[str, str]] = {}

try:
    from app.transit_lucky import (
        derive_lucky_number,
        derive_lucky_color,
        derive_compatible_sign,
        derive_mood,
        derive_dos,
        derive_donts,
        derive_lucky_time,
        derive_gemstone,
        derive_mantra,
        get_all_lucky_metadata,
        GEMSTONE_DATA,
        PLANET_MANTRAS,
        RULERS,
        ELEMENTS,
    )
except ImportError:
    # Minimal fallbacks so the engine always produces output
    def derive_lucky_number(sign: str, planet_data: dict, **kw) -> int:
        return (SIGNS.index(sign.lower()) + 1) if sign.lower() in SIGNS else 7

    def derive_lucky_color(sign: str, **kw) -> Dict[str, str]:
        return {"en": "Green", "hi": "\u0939\u0930\u093e"}

    def derive_compatible_sign(sign: str, **kw) -> Dict[str, str]:
        return {"en": "Leo", "hi": "\u0938\u093f\u0902\u0939"}

    def derive_mood(sign: str, scores: dict, **kw) -> Dict[str, str]:
        return {"en": "Balanced", "hi": "\u0938\u0902\u0924\u0941\u0932\u093f\u0924"}

    def derive_dos(sign: str, planet_data: dict, **kw) -> List[Dict[str, str]]:
        return [{"en": "Stay positive and focused.", "hi": "\u0938\u0915\u093e\u0930\u093e\u0924\u094d\u092e\u0915 \u0914\u0930 \u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924 \u0930\u0939\u0947\u0902\u0964"}]

    def derive_donts(sign: str, planet_data: dict, **kw) -> List[Dict[str, str]]:
        return [{"en": "Avoid impulsive decisions.", "hi": "\u0906\u0935\u0947\u0917\u092a\u0942\u0930\u094d\u0923 \u0928\u093f\u0930\u094d\u0923\u092f\u094b\u0902 \u0938\u0947 \u092c\u091a\u0947\u0902\u0964"}]

    def derive_lucky_time(sign: str, ruler: str, **kw) -> Dict[str, str]:
        return {"en": "10:00 AM - 11:00 AM", "hi": "सुबह 10:00 - 11:00"}

    def derive_gemstone(ruler: str, **kw) -> Dict[str, Any]:
        return {"gem": {"en": "Pearl (Moti)", "hi": "मोती"}, "metal": {"en": "Silver", "hi": "चांदी"}, "finger": {"en": "Little finger", "hi": "कनिष्ठा"}, "day": {"en": "Monday", "hi": "सोमवार"}}

    def derive_mantra(ruler: str, **kw) -> str:
        return "Om Namah Shivaya"

    def get_all_lucky_metadata(sign: str, **kw) -> Dict[str, Any]:
        return {
            "lucky_number": 7,
            "lucky_color": {"en": "Green", "hi": "हरा"},
            "lucky_time": {"en": "10:00 AM - 11:00 AM", "hi": "सुबह 10:00 - 11:00"},
            "compatible_sign": {"en": "Leo", "hi": "सिंह"},
            "gemstone": {"gem": {"en": "Pearl (Moti)", "hi": "मोती"}},
            "mantra": "Om Namah Shivaya",
            "mood": {"en": "Balanced", "hi": "संतुलित"},
            "dos": [{"en": "Stay positive.", "hi": "सकारात्मक रहें।"}],
            "donts": [{"en": "Avoid impulsive decisions.", "hi": "आवेगपूर्ण निर्णयों से बचें।"}],
        }

    GEMSTONE_DATA: Dict[str, Dict[str, str]] = {}
    PLANET_MANTRAS: Dict[str, str] = {}
    RULERS: Dict[str, str] = {
        "aries": "Mars", "taurus": "Venus", "gemini": "Mercury", "cancer": "Moon",
        "leo": "Sun", "virgo": "Mercury", "libra": "Venus", "scorpio": "Mars",
        "sagittarius": "Jupiter", "capricorn": "Saturn", "aquarius": "Saturn",
        "pisces": "Jupiter",
    }
    ELEMENTS: Dict[str, str] = {
        "aries": "fire", "taurus": "earth", "gemini": "air", "cancer": "water",
        "leo": "fire", "virgo": "earth", "libra": "air", "scorpio": "water",
        "sagittarius": "fire", "capricorn": "earth", "aquarius": "air",
        "pisces": "water",
    }


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIGNS: List[str] = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

SIGN_INDEX: Dict[str, int] = {s: i for i, s in enumerate(SIGNS)}

MAIN_PLANETS: List[str] = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

AREAS: List[str] = ["general", "love", "career", "finance", "health"]

# -- Dignity tables --

EXALTED_SIGNS: Dict[str, str] = {
    "Sun": "aries", "Moon": "taurus", "Mars": "capricorn", "Mercury": "virgo",
    "Jupiter": "cancer", "Venus": "pisces", "Saturn": "libra",
}

DEBILITATED_SIGNS: Dict[str, str] = {
    "Sun": "libra", "Moon": "scorpio", "Mars": "cancer", "Mercury": "pisces",
    "Jupiter": "capricorn", "Venus": "virgo", "Saturn": "aries",
}

OWN_SIGNS: Dict[str, List[str]] = {
    "Sun": ["leo"], "Moon": ["cancer"], "Mars": ["aries", "scorpio"],
    "Mercury": ["gemini", "virgo"], "Jupiter": ["sagittarius", "pisces"],
    "Venus": ["taurus", "libra"], "Saturn": ["capricorn", "aquarius"],
}

# -- Importance weights by period --

PERIOD_WEIGHTS: Dict[str, Dict[str, int]] = {
    "daily": {"Moon": 5, "Sun": 3, "Mercury": 3, "Venus": 3, "Mars": 2, "Jupiter": 1, "Saturn": 1},
    "weekly": {"Mercury": 4, "Venus": 4, "Mars": 3, "Moon": 3, "Sun": 2, "Jupiter": 2, "Saturn": 1},
    "monthly": {"Saturn": 5, "Jupiter": 5, "Mars": 3, "Venus": 2, "Mercury": 2, "Sun": 2, "Moon": 1},
    "yearly": {"Saturn": 5, "Jupiter": 5, "Mars": 3, "Venus": 2, "Mercury": 1, "Sun": 1, "Moon": 1},
}

# -- Dignity multipliers --

DIGNITY_MULTIPLIER: Dict[str, float] = {
    "exalted": 1.5,
    "own_sign": 1.3,
    "debilitated": 0.7,
    "combust": 0.6,
    "retrograde": 1.1,
    "neutral": 1.0,
}

# -- Fragment pick counts per period --

FRAGMENT_COUNTS: Dict[str, int] = {
    "daily": 3,
    "weekly": 3,
    "monthly": 4,
    "yearly": 5,
}

# -- Scoring tables --

HOUSE_SCORES: Dict[int, int] = {
    1: 2, 2: 1, 3: 1, 4: 1, 5: 3, 6: -1,
    7: 1, 8: -2, 9: 3, 10: 2, 11: 3, 12: -2,
}

PLANET_NATURE: Dict[str, float] = {
    "Jupiter": 1.5, "Venus": 1.0, "Moon": 0.5, "Mercury": 0.5,
    "Sun": 0.0, "Mars": -0.5, "Saturn": -1.0,
}

DIGNITY_BONUS: Dict[str, int] = {
    "exalted": 2, "own_sign": 1, "debilitated": -2,
    "combust": -1, "retrograde": 0, "neutral": 0,
}

AREA_WEIGHTS: Dict[str, Dict[str, float]] = {
    "love": {"Venus": 3, "Moon": 2, "Jupiter": 1.5, "Mars": 1},
    "career": {"Saturn": 3, "Sun": 2.5, "Jupiter": 2, "Mars": 1.5, "Mercury": 1},
    "finance": {"Jupiter": 3, "Venus": 2, "Mercury": 1.5, "Moon": 1},
    "health": {"Sun": 3, "Mars": 2, "Saturn": 1.5, "Moon": 1},
}

# -- Lucky time slots (cycled per sign index) --

_LUCKY_TIMES: List[Dict[str, str]] = [
    {"en": "6:00 AM - 7:00 AM", "hi": "\u0938\u0941\u092c\u0939 6:00 - 7:00"},
    {"en": "7:00 AM - 8:00 AM", "hi": "\u0938\u0941\u092c\u0939 7:00 - 8:00"},
    {"en": "9:00 AM - 10:00 AM", "hi": "\u0938\u0941\u092c\u0939 9:00 - 10:00"},
    {"en": "10:00 AM - 11:00 AM", "hi": "\u0938\u0941\u092c\u0939 10:00 - 11:00"},
    {"en": "11:00 AM - 12:00 PM", "hi": "\u0938\u0941\u092c\u0939 11:00 - \u0926\u094b\u092a\u0939\u0930 12:00"},
    {"en": "12:00 PM - 1:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 12:00 - 1:00"},
    {"en": "2:00 PM - 3:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 2:00 - 3:00"},
    {"en": "3:00 PM - 4:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 3:00 - 4:00"},
    {"en": "4:00 PM - 5:00 PM", "hi": "\u0936\u093e\u092e 4:00 - 5:00"},
    {"en": "5:00 PM - 6:00 PM", "hi": "\u0936\u093e\u092e 5:00 - 6:00"},
    {"en": "6:00 PM - 7:00 PM", "hi": "\u0936\u093e\u092e 6:00 - 7:00"},
    {"en": "7:00 PM - 8:00 PM", "hi": "\u0936\u093e\u092e 7:00 - 8:00"},
]

# -- Default gemstone data (fallback) --

_DEFAULT_GEMSTONES: Dict[str, Dict[str, str]] = {
    "aries":       {"en": "Red Coral (Moonga)", "hi": "\u092e\u0942\u0902\u0917\u093e"},
    "taurus":      {"en": "Diamond (Heera)", "hi": "\u0939\u0940\u0930\u093e"},
    "gemini":      {"en": "Emerald (Panna)", "hi": "\u092a\u0928\u094d\u0928\u093e"},
    "cancer":      {"en": "Pearl (Moti)", "hi": "\u092e\u094b\u0924\u0940"},
    "leo":         {"en": "Ruby (Manik)", "hi": "\u092e\u093e\u0923\u093f\u0915"},
    "virgo":       {"en": "Emerald (Panna)", "hi": "\u092a\u0928\u094d\u0928\u093e"},
    "libra":       {"en": "Diamond (Heera)", "hi": "\u0939\u0940\u0930\u093e"},
    "scorpio":     {"en": "Red Coral (Moonga)", "hi": "\u092e\u0942\u0902\u0917\u093e"},
    "sagittarius": {"en": "Yellow Sapphire (Pukhraj)", "hi": "\u092a\u0941\u0916\u0930\u093e\u091c"},
    "capricorn":   {"en": "Blue Sapphire (Neelam)", "hi": "\u0928\u0940\u0932\u092e"},
    "aquarius":    {"en": "Blue Sapphire (Neelam)", "hi": "\u0928\u0940\u0932\u092e"},
    "pisces":      {"en": "Yellow Sapphire (Pukhraj)", "hi": "\u092a\u0941\u0916\u0930\u093e\u091c"},
}

# -- Default planet mantras (fallback) --

_DEFAULT_MANTRAS: Dict[str, str] = {
    "Sun":     "Om Hraam Hreem Hroum Sah Suryaya Namah",
    "Moon":    "Om Shraam Shreem Shroum Sah Chandraya Namah",
    "Mars":    "Om Kraam Kreem Kroum Sah Bhaumaya Namah",
    "Mercury": "Om Braam Breem Broum Sah Budhaya Namah",
    "Jupiter": "Om Graam Greem Groum Sah Gurave Namah",
    "Venus":   "Om Draam Dreem Droum Sah Shukraya Namah",
    "Saturn":  "Om Praam Preem Proum Sah Shanaishcharaya Namah",
}

# -- Hindi month names --

HINDI_MONTHS: List[str] = [
    "\u091c\u0928\u0935\u0930\u0940",      # January
    "\u092b\u0930\u0935\u0930\u0940",      # February
    "\u092e\u093e\u0930\u094d\u091a",      # March
    "\u0905\u092a\u094d\u0930\u0948\u0932", # April
    "\u092e\u0908",                         # May
    "\u091c\u0942\u0928",                   # June
    "\u091c\u0941\u0932\u093e\u0908",      # July
    "\u0905\u0917\u0938\u094d\u0924",      # August
    "\u0938\u093f\u0924\u0902\u092c\u0930", # September
    "\u0905\u0915\u094d\u091f\u0942\u092c\u0930", # October
    "\u0928\u0935\u0902\u092c\u0930",      # November
    "\u0926\u093f\u0938\u0902\u092c\u0930", # December
]

ENGLISH_MONTHS: List[str] = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# -- Quarter labels --

QUARTER_LABELS: List[Dict[str, str]] = [
    {"en": "Q1 (Jan-Mar)", "hi": "Q1 (\u091c\u0928\u0935\u0930\u0940-\u092e\u093e\u0930\u094d\u091a)"},
    {"en": "Q2 (Apr-Jun)", "hi": "Q2 (\u0905\u092a\u094d\u0930\u0948\u0932-\u091c\u0942\u0928)"},
    {"en": "Q3 (Jul-Sep)", "hi": "Q3 (\u091c\u0941\u0932\u093e\u0908-\u0938\u093f\u0924\u0902\u092c\u0930)"},
    {"en": "Q4 (Oct-Dec)", "hi": "Q4 (\u0905\u0915\u094d\u091f\u0942\u092c\u0930-\u0926\u093f\u0938\u0902\u092c\u0930)"},
]

# -- Sign display names (bilingual) --

SIGN_DISPLAY: Dict[str, Dict[str, str]] = {
    "aries":       {"en": "Aries",       "hi": "\u092e\u0947\u0937"},
    "taurus":      {"en": "Taurus",      "hi": "\u0935\u0943\u0937\u092d"},
    "gemini":      {"en": "Gemini",      "hi": "\u092e\u093f\u0925\u0941\u0928"},
    "cancer":      {"en": "Cancer",      "hi": "\u0915\u0930\u094d\u0915"},
    "leo":         {"en": "Leo",         "hi": "\u0938\u093f\u0902\u0939"},
    "virgo":       {"en": "Virgo",       "hi": "\u0915\u0928\u094d\u092f\u093e"},
    "libra":       {"en": "Libra",       "hi": "\u0924\u0941\u0932\u093e"},
    "scorpio":     {"en": "Scorpio",     "hi": "\u0935\u0943\u0936\u094d\u091a\u093f\u0915"},
    "sagittarius": {"en": "Sagittarius", "hi": "\u0927\u0928\u0941"},
    "capricorn":   {"en": "Capricorn",   "hi": "\u092e\u0915\u0930"},
    "aquarius":    {"en": "Aquarius",    "hi": "\u0915\u0941\u0902\u092d"},
    "pisces":      {"en": "Pisces",      "hi": "\u092e\u0940\u0928"},
}


# ===================================================================
# 1. get_full_transits
# ===================================================================

def get_full_transits(target_date: str = None) -> Dict[str, Dict]:
    """
    Compute planetary positions for Delhi 12:00 IST on the given date.

    Args:
        target_date: ISO date string "YYYY-MM-DD". Defaults to today (UTC).

    Returns:
        The full ``planets`` dict from :func:`calculate_planet_positions`.
    """
    if target_date is None:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Delhi coordinates: 28.6139 N, 77.2090 E, IST = UTC+5.5
    try:
        positions = calculate_planet_positions(
            birth_date=target_date,
            birth_time="12:00:00",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        return positions.get("planets", {})
    except Exception:
        logger.exception("Failed to calculate planet positions for %s", target_date)
        return _fallback_planet_data()


# ===================================================================
# 2. calculate_transit_houses
# ===================================================================

def calculate_transit_houses(sign: str, planet_data: Dict[str, Dict]) -> Dict[str, int]:
    """
    For a given native sign (treated as 1st house), compute which house each
    planet occupies based on the planet's current sign.

    Args:
        sign: The native's sign (lowercase, e.g. "aries").
        planet_data: Dict of planet name -> planet info dict (must have "sign" key).

    Returns:
        Dict mapping planet name -> house number (1-12).
    """
    sign_lower = sign.lower()
    native_idx = SIGN_INDEX.get(sign_lower, 0)

    houses: Dict[str, int] = {}
    for planet_name, info in planet_data.items():
        planet_sign = info.get("sign", "Aries").lower()
        planet_idx = SIGN_INDEX.get(planet_sign, 0)
        house = ((planet_idx - native_idx) % 12) + 1
        houses[planet_name] = house

    return houses


# ===================================================================
# 3. get_planet_dignity
# ===================================================================

def get_planet_dignity(planet: str, planet_info: Dict) -> str:
    """
    Return the dignity classification for a planet.

    Priority order: combust > retrograde > exalted > debilitated > own_sign > neutral.
    Uses the ``status`` field from astro_engine if available, otherwise checks manually.

    Returns one of: "exalted", "debilitated", "own_sign", "retrograde", "combust", "neutral".
    """
    # Check combust first (highest priority negative condition)
    if planet_info.get("is_combust", False):
        return "combust"

    # Check retrograde
    is_retro = planet_info.get("retrograde", False)

    # Get the planet's current sign (lowercase for comparison)
    current_sign = planet_info.get("sign", "").lower()

    # Check status field from astro_engine (may contain combined strings like "Exalted, Retrograde")
    status = planet_info.get("status", "").lower()

    if "exalted" in status:
        return "exalted"
    if "debilitated" in status:
        return "debilitated"
    if "own sign" in status:
        return "own_sign"

    # Manual check against tables
    if current_sign and planet in EXALTED_SIGNS:
        if current_sign == EXALTED_SIGNS[planet]:
            return "exalted"
    if current_sign and planet in DEBILITATED_SIGNS:
        if current_sign == DEBILITATED_SIGNS[planet]:
            return "debilitated"
    if current_sign and planet in OWN_SIGNS:
        if current_sign in OWN_SIGNS[planet]:
            return "own_sign"

    if is_retro:
        return "retrograde"

    return "neutral"


# ===================================================================
# 4. assemble_section
# ===================================================================

def assemble_section(
    sign: str,
    area: str,
    planet_houses: Dict[str, int],
    planet_data: Dict[str, Dict],
    period: str,
    language: str,
) -> str:
    """
    Combine relevant interpretation fragments into a coherent 3-5 sentence paragraph
    for the given sign, area, and period.

    Algorithm:
      1. For each of 7 main planets, look up TRANSIT_FRAGMENTS[planet][house][area][language].
      2. Assign importance weights based on period.
      3. Apply dignity multiplier.
      4. Sort by (weight * dignity_mult) descending.
      5. Pick top N fragments (daily=3, weekly=3, monthly=4, yearly=5).
      6. For top-1 planet, if it has a special dignity, prepend DIGNITY_MODIFIERS prefix.
      7. Join fragments with space.

    Args:
        sign: Native sign (lowercase).
        area: One of "general", "love", "career", "finance", "health".
        planet_houses: Mapping of planet -> house (from calculate_transit_houses).
        planet_data: Raw planet info dict.
        period: "daily", "weekly", "monthly", or "yearly".
        language: "en" or "hi".

    Returns:
        A single string paragraph.
    """
    weights = PERIOD_WEIGHTS.get(period, PERIOD_WEIGHTS["daily"])
    pick_count = FRAGMENT_COUNTS.get(period, 3)

    scored_fragments: List[Tuple[float, str, str, str]] = []
    # (score, fragment_text, planet_name, dignity)

    for planet in MAIN_PLANETS:
        house = planet_houses.get(planet)
        if house is None:
            continue

        # Look up fragment text
        fragment = _lookup_fragment(planet, house, area, language)
        if not fragment:
            continue

        # Weight from period
        base_weight = weights.get(planet, 1)

        # Dignity multiplier
        pinfo = planet_data.get(planet, {})
        dignity = get_planet_dignity(planet, pinfo)
        multiplier = DIGNITY_MULTIPLIER.get(dignity, 1.0)

        score = base_weight * multiplier
        scored_fragments.append((score, fragment, planet, dignity))

    # Sort descending by score
    scored_fragments.sort(key=lambda x: x[0], reverse=True)

    # Pick top N
    selected = scored_fragments[:pick_count]
    if not selected:
        return _default_section_text(sign, area, language)

    # Build the paragraph
    parts: List[str] = []
    for idx, (score, fragment, planet, dignity) in enumerate(selected):
        text = fragment
        # For the top-1 planet, prepend dignity modifier if applicable
        if idx == 0 and dignity != "neutral":
            modifier = _get_dignity_modifier(dignity, language)
            if modifier:
                text = modifier + " " + text
        parts.append(text)

    return " ".join(parts)


# ===================================================================
# 5. compute_scores
# ===================================================================

def compute_scores(
    sign: str,
    planet_houses: Dict[str, int],
    planet_data: Dict[str, Dict],
) -> Dict[str, int]:
    """
    Compute numeric scores (1-10) for overall and each area.

    Scoring algorithm:
      - Overall: sum(house_score + planet_nature + dignity_bonus) for all 7 planets,
        then normalize to 1-10.
      - Area scores: use AREA_WEIGHTS to compute weighted sub-scores.

    Returns:
        {"overall": 7, "love": 8, "career": 6, "finance": 7, "health": 5}
    """
    # -- Overall score --
    raw_total = 0.0
    for planet in MAIN_PLANETS:
        house = planet_houses.get(planet, 1)
        pinfo = planet_data.get(planet, {})
        dignity = get_planet_dignity(planet, pinfo)

        h_score = HOUSE_SCORES.get(house, 0)
        nature = PLANET_NATURE.get(planet, 0.0)
        d_bonus = DIGNITY_BONUS.get(dignity, 0)

        raw_total += h_score + nature + d_bonus

    # Theoretical range: 7 planets * (worst: -5) to (best: +6.5) = -35 to +45.5
    # Real-world range clusters around -5 to +15. Use tighter bounds for better spread.
    overall = _normalize_score(raw_total, min_val=-8.0, max_val=18.0)

    # -- Area scores --
    area_scores: Dict[str, int] = {}
    for area, area_planet_weights in AREA_WEIGHTS.items():
        raw_area = 0.0
        total_weight = 0.0
        for planet, weight in area_planet_weights.items():
            house = planet_houses.get(planet, 1)
            pinfo = planet_data.get(planet, {})
            dignity = get_planet_dignity(planet, pinfo)

            h_score = HOUSE_SCORES.get(house, 0)
            nature = PLANET_NATURE.get(planet, 0.0)
            d_bonus = DIGNITY_BONUS.get(dignity, 0)

            planet_score = h_score + nature + d_bonus
            raw_area += planet_score * weight
            total_weight += weight

        # Weighted average, then normalize
        if total_weight > 0:
            avg = raw_area / total_weight
        else:
            avg = 0.0
        # Per-planet weighted avg typically ranges -3 to +5. Tighter bounds for better spread.
        area_scores[area] = _normalize_score(avg, min_val=-3.0, max_val=5.0)

    return {
        "overall": overall,
        "love": area_scores.get("love", 5),
        "career": area_scores.get("career", 5),
        "finance": area_scores.get("finance", 5),
        "health": area_scores.get("health", 5),
    }


# ===================================================================
# 6. generate_transit_horoscope (main entry point)
# ===================================================================

def generate_transit_horoscope(
    sign: str,
    period: str,
    target_date: str = None,
) -> Dict[str, Any]:
    """
    Generate a complete bilingual horoscope response for a given sign and period.

    Args:
        sign: Zodiac sign (lowercase, e.g. "aries").
        period: "daily", "weekly", "monthly", or "yearly".
        target_date: ISO date string. Defaults to today.

    Returns:
        Complete horoscope dict with sections, scores, mood, lucky info, dos/donts.
    """
    sign_lower = sign.lower()
    period_lower = period.lower()

    # Get planet positions
    planet_data = get_full_transits(target_date)
    if not planet_data:
        return _fallback_horoscope(sign_lower, period_lower)

    # Calculate houses from native sign
    planet_houses = calculate_transit_houses(sign_lower, planet_data)

    # Assemble sections (bilingual)
    sections: Dict[str, Dict[str, str]] = {}
    for area in AREAS:
        sections[area] = {
            "en": assemble_section(sign_lower, area, planet_houses, planet_data, period_lower, "en"),
            "hi": assemble_section(sign_lower, area, planet_houses, planet_data, period_lower, "hi"),
        }

    # Compute scores
    scores = compute_scores(sign_lower, planet_houses, planet_data)

    # Extract Moon nakshatra data for lucky derivations
    moon_info = planet_data.get("Moon", {})
    moon_nak_idx = _nakshatra_name_to_index(moon_info.get("nakshatra", "Ashwini"))
    moon_pada = moon_info.get("nakshatra_pada", 1)

    # Build dignity map for all planets
    planet_dignities = {p: get_planet_dignity(p, planet_data.get(p, {})) for p in MAIN_PLANETS}

    # Use target_date or today's date
    date_str = target_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Derive ALL lucky elements using the lucky module - Centralized Source of Truth
    lucky_meta = get_all_lucky_metadata(
        sign=sign_lower,
        moon_nakshatra_index=moon_nak_idx,
        moon_pada=moon_pada,
        date_str=date_str,
        overall_score=int(scores.get("overall", 5)),
        planet_houses=planet_houses,
        planet_dignities=planet_dignities,
        transit_dignities=planet_dignities
    )

    # Extract clean gemstone name for frontend
    gem_data = lucky_meta.get("gemstone", {})
    gem_name = gem_data.get("gem", {"en": "Pearl (Moti)", "hi": "\u092e\u094b\u0924\u0940"})

    return {
        "sign": sign_lower,
        "period": period_lower,
        "date": date_str,
        "sections": sections,
        "scores": scores,
        "mood": lucky_meta["mood"],
        "lucky": {
            "number": lucky_meta["lucky_number"],
            "color": lucky_meta["lucky_color"],
            "time": lucky_meta["lucky_time"],
            "compatible_sign": lucky_meta["compatible_sign"],
            "gemstone": gem_name,
            "mantra": lucky_meta["mantra"],
        },
        "dos": lucky_meta["dos"],
        "donts": lucky_meta["donts"],
        "source": "transit_engine",
    }


# ===================================================================
# 7. generate_monthly_extras
# ===================================================================

def generate_monthly_extras(sign: str, target_date: str = None) -> Dict[str, Any]:
    """
    Compute transit engine data at 3 dates (5th, 15th, 25th of the month) to
    produce monthly phases and detect key dates when planets change signs.

    Args:
        sign: Zodiac sign (lowercase).
        target_date: ISO date string within the target month. Defaults to today.

    Returns:
        Dict with "phases" (3 ten-day ranges) and "key_dates" (sign-change events).
    """
    sign_lower = sign.lower()

    if target_date:
        year, month, _ = _parse_date_parts(target_date)
    else:
        now = datetime.now(timezone.utc)
        year, month = now.year, now.month

    last_day = calendar.monthrange(year, month)[1]

    # Sample dates: 5th, 15th, 25th
    sample_days = [5, 15, 25]
    phase_ranges = [
        ("1st - 10th", "\u0967 - \u0967\u0966"),
        ("11th - 20th", "\u0967\u0967 - \u0968\u0966"),
        ("21st - end", "\u0968\u0967 - \u0905\u0902\u0924"),
    ]

    phases: List[Dict[str, Any]] = []
    for i, day in enumerate(sample_days):
        date_str = f"{year}-{month:02d}-{min(day, last_day):02d}"
        try:
            planet_data = get_full_transits(date_str)
            planet_houses = calculate_transit_houses(sign_lower, planet_data)
            scores = compute_scores(sign_lower, planet_houses, planet_data)

            summary_en = assemble_section(sign_lower, "general", planet_houses, planet_data, "monthly", "en")
            summary_hi = assemble_section(sign_lower, "general", planet_houses, planet_data, "monthly", "hi")
        except Exception:
            logger.exception("Monthly extras: failed for %s", date_str)
            scores = {"overall": 5}
            summary_en = "A period of mixed influences. Stay balanced."
            summary_hi = "\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u092a\u094d\u0930\u092d\u093e\u0935\u094b\u0902 \u0915\u093e \u0938\u092e\u092f\u0964 \u0938\u0902\u0924\u0941\u0932\u093f\u0924 \u0930\u0939\u0947\u0902\u0964"

        en_range, hi_range = phase_ranges[i]
        phases.append({
            "range": en_range,
            "summary": {"en": summary_en, "hi": summary_hi},
            "score": scores.get("overall", 5),
        })

    # Key dates: detect sign changes between 1st and last day
    key_dates = _detect_sign_changes(year, month, last_day)

    return {
        "phases": phases,
        "key_dates": key_dates,
    }


# ===================================================================
# 8. generate_yearly_extras
# ===================================================================

def generate_yearly_extras(sign: str, year: int = None) -> Dict[str, Any]:
    """
    Compute transit engine at quarterly and monthly mid-points to produce
    yearly overview data including quarter themes, best months, and annual theme.

    Args:
        sign: Zodiac sign (lowercase).
        year: Target year. Defaults to current year.

    Returns:
        Dict with "quarters", "best_months", and "annual_theme".
    """
    sign_lower = sign.lower()
    if year is None:
        year = datetime.now(timezone.utc).year

    # -- Quarterly analysis (mid-points: Feb 15, May 15, Aug 15, Nov 15) --
    quarter_dates = [
        f"{year}-02-15",
        f"{year}-05-15",
        f"{year}-08-15",
        f"{year}-11-15",
    ]

    quarters: List[Dict[str, Any]] = []
    for q_idx, q_date in enumerate(quarter_dates):
        try:
            planet_data = get_full_transits(q_date)
            planet_houses = calculate_transit_houses(sign_lower, planet_data)
            scores = compute_scores(sign_lower, planet_houses, planet_data)
            theme_en = assemble_section(sign_lower, "general", planet_houses, planet_data, "yearly", "en")
            theme_hi = assemble_section(sign_lower, "general", planet_houses, planet_data, "yearly", "hi")

            # Find the best area for this quarter
            area_scores = {a: scores.get(a, 5) for a in ["love", "career", "finance", "health"]}
            best_area = max(area_scores, key=area_scores.get)  # type: ignore[arg-type]
        except Exception:
            logger.exception("Yearly extras: failed quarter %d", q_idx + 1)
            theme_en = "A quarter of growth and change."
            theme_hi = "\u0935\u093f\u0915\u093e\u0938 \u0914\u0930 \u092a\u0930\u093f\u0935\u0930\u094d\u0924\u0928 \u0915\u0940 \u0924\u093f\u092e\u093e\u0939\u0940\u0964"
            best_area = "career"
            scores = {"overall": 5}

        quarters.append({
            "label": QUARTER_LABELS[q_idx],
            "theme": {"en": theme_en, "hi": theme_hi},
            "best_area": best_area,
            "score": scores.get("overall", 5),
        })

    # -- Monthly analysis (15th of each month) for best months --
    monthly_scores: Dict[int, Dict[str, int]] = {}  # month -> area -> score
    for m in range(1, 13):
        date_str = f"{year}-{m:02d}-15"
        try:
            planet_data = get_full_transits(date_str)
            planet_houses = calculate_transit_houses(sign_lower, planet_data)
            scores = compute_scores(sign_lower, planet_houses, planet_data)
            monthly_scores[m] = scores
        except Exception:
            logger.exception("Yearly extras: failed month %d", m)
            monthly_scores[m] = {"overall": 5, "love": 5, "career": 5, "finance": 5, "health": 5}

    # Find best 2 months per area
    best_months: Dict[str, Dict[str, str]] = {}
    for area in ["career", "love", "finance", "health"]:
        scored_months = [(m, monthly_scores[m].get(area, 5)) for m in range(1, 13)]
        scored_months.sort(key=lambda x: x[1], reverse=True)
        top2 = scored_months[:2]
        top2_sorted = sorted(top2, key=lambda x: x[0])  # sort by month order

        en_names = ", ".join(ENGLISH_MONTHS[m - 1] for m, _ in top2_sorted)
        hi_names = ", ".join(HINDI_MONTHS[m - 1] for m, _ in top2_sorted)
        best_months[area] = {"en": en_names, "hi": hi_names}

    # Annual theme: general section from mid-year (July 15)
    try:
        mid_year_data = get_full_transits(f"{year}-07-15")
        mid_houses = calculate_transit_houses(sign_lower, mid_year_data)
        annual_en = assemble_section(sign_lower, "general", mid_houses, mid_year_data, "yearly", "en")
        annual_hi = assemble_section(sign_lower, "general", mid_houses, mid_year_data, "yearly", "hi")
    except Exception:
        logger.exception("Yearly extras: failed annual theme")
        annual_en = "A year of transformation and growth awaits you."
        annual_hi = "\u092a\u0930\u093f\u0935\u0930\u094d\u0924\u0928 \u0914\u0930 \u0935\u093f\u0915\u093e\u0938 \u0915\u093e \u0935\u0930\u094d\u0937 \u0906\u092a\u0915\u093e \u0907\u0902\u0924\u091c\u093e\u0930 \u0915\u0930 \u0930\u0939\u093e \u0939\u0948\u0964"

    return {
        "quarters": quarters,
        "best_months": best_months,
        "annual_theme": {"en": annual_en, "hi": annual_hi},
    }


# ===================================================================
# Internal helpers
# ===================================================================

# 27 Nakshatra names (same order as astro_engine._NAKSHATRA_DATA)
_NAKSHATRA_NAMES: List[str] = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]


def _nakshatra_name_to_index(name: str) -> int:
    """Convert a nakshatra name to its 0-based index (0-26)."""
    try:
        return _NAKSHATRA_NAMES.index(name)
    except ValueError:
        return 0


def _lookup_fragment(planet: str, house: int, area: str, language: str) -> str:
    """Look up a text fragment from the interpretation matrix, returning empty string if missing."""
    try:
        return TRANSIT_FRAGMENTS[planet][house][area][language]
    except (KeyError, TypeError):
        return ""


def _get_dignity_modifier(dignity: str, language: str) -> str:
    """Get a prefix phrase for a given dignity from the DIGNITY_MODIFIERS data."""
    try:
        mod = DIGNITY_MODIFIERS.get(dignity, {})
        # DIGNITY_MODIFIERS uses nested structure: {prefix: {en, hi}, suffix: {en, hi}}
        prefix = mod.get("prefix", {}).get(language, "")
        return prefix
    except (AttributeError, TypeError):
        return ""


def _normalize_score(raw: float, min_val: float, max_val: float) -> int:
    """Normalize a raw score to 1-10 integer range."""
    if max_val == min_val:
        return 5
    ratio = (raw - min_val) / (max_val - min_val)
    # Clamp to 0-1
    ratio = max(0.0, min(1.0, ratio))
    # Map to 1-10
    return max(1, min(10, round(ratio * 9 + 1)))


def _default_section_text(sign: str, area: str, language: str) -> str:
    """Return a generic fallback paragraph when no fragments are available."""
    sign_display = SIGN_DISPLAY.get(sign, {}).get(language, sign.title())

    defaults_en = {
        "general": f"The planetary alignment brings a period of reflection for {sign_display}. Stay mindful of opportunities and challenges alike. Balance is key.",
        "love": f"Relationships require patience and understanding for {sign_display}. Open communication strengthens bonds. Trust the process.",
        "career": f"Professional matters demand focus and determination for {sign_display}. Strategic thinking leads to progress. Stay committed to goals.",
        "finance": f"Financial decisions should be made carefully for {sign_display}. Avoid impulsive spending and focus on long-term stability.",
        "health": f"Health requires attention for {sign_display}. Prioritize rest, nutrition, and regular exercise. Mental well-being is equally important.",
    }

    defaults_hi = {
        "general": f"{sign_display} \u0915\u0947 \u0932\u093f\u090f \u0917\u094d\u0930\u0939\u094b\u0902 \u0915\u0940 \u0938\u094d\u0925\u093f\u0924\u093f \u091a\u093f\u0902\u0924\u0928 \u0915\u093e \u0938\u092e\u092f \u0932\u093e\u0924\u0940 \u0939\u0948\u0964 \u0905\u0935\u0938\u0930\u094b\u0902 \u0914\u0930 \u091a\u0941\u0928\u094c\u0924\u093f\u092f\u094b\u0902 \u0926\u094b\u0928\u094b\u0902 \u0915\u093e \u0927\u094d\u092f\u093e\u0928 \u0930\u0916\u0947\u0902\u0964 \u0938\u0902\u0924\u0941\u0932\u0928 \u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u0939\u0948\u0964",
        "love": f"{sign_display} \u0915\u0947 \u0932\u093f\u090f \u0930\u093f\u0936\u094d\u0924\u094b\u0902 \u092e\u0947\u0902 \u0927\u0948\u0930\u094d\u092f \u0914\u0930 \u0938\u092e\u091d \u0915\u0940 \u0906\u0935\u0936\u094d\u092f\u0915\u0924\u093e \u0939\u0948\u0964 \u0916\u0941\u0932\u093e \u0938\u0902\u0935\u093e\u0926 \u0938\u0902\u092c\u0902\u0927\u094b\u0902 \u0915\u094b \u092e\u091c\u092c\u0942\u0924 \u0915\u0930\u0924\u093e \u0939\u0948\u0964",
        "career": f"{sign_display} \u0915\u0947 \u0932\u093f\u090f \u092a\u0947\u0936\u0947\u0935\u0930 \u092e\u093e\u092e\u0932\u094b\u0902 \u092e\u0947\u0902 \u0927\u094d\u092f\u093e\u0928 \u0914\u0930 \u0926\u0943\u0922\u093c\u0924\u093e \u0915\u0940 \u091c\u0930\u0942\u0930\u0924 \u0939\u0948\u0964 \u0930\u0923\u0928\u0940\u0924\u093f\u0915 \u0938\u094b\u091a \u092a\u094d\u0930\u0917\u0924\u093f \u0915\u0940 \u0913\u0930 \u0932\u0947 \u091c\u093e\u0924\u0940 \u0939\u0948\u0964",
        "finance": f"{sign_display} \u0915\u0947 \u0932\u093f\u090f \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0928\u093f\u0930\u094d\u0923\u092f \u0938\u093e\u0935\u0927\u093e\u0928\u0940 \u0938\u0947 \u0932\u0947\u0928\u0947 \u091a\u093e\u0939\u093f\u090f\u0964 \u0906\u0935\u0947\u0917\u092a\u0942\u0930\u094d\u0923 \u0916\u0930\u094d\u091a \u0938\u0947 \u092c\u091a\u0947\u0902\u0964",
        "health": f"{sign_display} \u0915\u0947 \u0932\u093f\u090f \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u092a\u0930 \u0927\u094d\u092f\u093e\u0928 \u0926\u0947\u0928\u093e \u091c\u0930\u0942\u0930\u0940 \u0939\u0948\u0964 \u0906\u0930\u093e\u092e, \u092a\u094b\u0937\u0923 \u0914\u0930 \u0935\u094d\u092f\u093e\u092f\u093e\u092e \u0915\u094b \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0926\u0947\u0902\u0964",
    }

    if language == "hi":
        return defaults_hi.get(area, defaults_hi["general"])
    return defaults_en.get(area, defaults_en["general"])


def _parse_date_parts(date_str: str) -> Tuple[int, int, int]:
    """Parse 'YYYY-MM-DD' into (year, month, day) integers."""
    parts = date_str.split("-")
    return int(parts[0]), int(parts[1]), int(parts[2])


def _detect_sign_changes(year: int, month: int, last_day: int) -> List[Dict[str, Any]]:
    """
    Detect when any planet changes sign between the 1st and last day of a month.

    Compares planet signs on the 1st vs. last day. Returns key date events.
    """
    first_date = f"{year}-{month:02d}-01"
    last_date = f"{year}-{month:02d}-{last_day:02d}"

    try:
        first_data = get_full_transits(first_date)
        last_data = get_full_transits(last_date)
    except Exception:
        return []

    key_dates: List[Dict[str, Any]] = []

    for planet in MAIN_PLANETS:
        first_info = first_data.get(planet, {})
        last_info = last_data.get(planet, {})

        first_sign = first_info.get("sign", "")
        last_sign = last_info.get("sign", "")

        if first_sign and last_sign and first_sign != last_sign:
            # Binary search for the approximate change date
            change_date = _find_sign_change_date(planet, year, month, 1, last_day, first_sign)

            last_sign_display_en = last_sign
            last_sign_display_hi = SIGN_DISPLAY.get(last_sign.lower(), {}).get("hi", last_sign)
            planet_hi = _planet_hindi_name(planet)

            key_dates.append({
                "date": change_date,
                "event": {
                    "en": f"{planet} enters {last_sign_display_en} \u2014 {_sign_change_meaning_en(planet)}",
                    "hi": f"{planet_hi} {last_sign_display_hi} \u092e\u0947\u0902 \u2014 {_sign_change_meaning_hi(planet)}",
                },
            })

    return key_dates


def _find_sign_change_date(
    planet: str, year: int, month: int, start_day: int, end_day: int, start_sign: str
) -> str:
    """Binary search for the approximate date a planet changes sign within a month."""
    lo, hi = start_day, end_day
    while lo < hi:
        mid = (lo + hi) // 2
        date_str = f"{year}-{month:02d}-{mid:02d}"
        try:
            data = get_full_transits(date_str)
            mid_sign = data.get(planet, {}).get("sign", start_sign)
        except Exception:
            mid_sign = start_sign

        if mid_sign == start_sign:
            lo = mid + 1
        else:
            hi = mid

    return f"{year}-{month:02d}-{lo:02d}"


def _planet_hindi_name(planet: str) -> str:
    """Return Hindi name for a planet."""
    names = {
        "Sun": "\u0938\u0942\u0930\u094d\u092f",
        "Moon": "\u091a\u0902\u0926\u094d\u0930",
        "Mars": "\u092e\u0902\u0917\u0932",
        "Mercury": "\u092c\u0941\u0927",
        "Jupiter": "\u092c\u0943\u0939\u0938\u094d\u092a\u0924\u093f",
        "Venus": "\u0936\u0941\u0915\u094d\u0930",
        "Saturn": "\u0936\u0928\u093f",
    }
    return names.get(planet, planet)


def _sign_change_meaning_en(planet: str) -> str:
    """Short English phrase describing the effect of a planet changing sign."""
    meanings = {
        "Sun": "vitality and focus shift",
        "Moon": "emotional tone changes",
        "Mars": "energy and drive redirect",
        "Mercury": "communication shifts",
        "Jupiter": "expansion enters new territory",
        "Venus": "love and values transform",
        "Saturn": "discipline takes new form",
    }
    return meanings.get(planet, "influence shifts")


def _sign_change_meaning_hi(planet: str) -> str:
    """Short Hindi phrase describing the effect of a planet changing sign."""
    meanings = {
        "Sun": "\u090a\u0930\u094d\u091c\u093e \u0914\u0930 \u0927\u094d\u092f\u093e\u0928 \u092e\u0947\u0902 \u092c\u0926\u0932\u093e\u0935",
        "Moon": "\u092d\u093e\u0935\u0928\u093e\u0924\u094d\u092e\u0915 \u0938\u094d\u0935\u0930 \u092e\u0947\u0902 \u092c\u0926\u0932\u093e\u0935",
        "Mars": "\u090a\u0930\u094d\u091c\u093e \u0914\u0930 \u092a\u094d\u0930\u0947\u0930\u0923\u093e \u0928\u0908 \u0926\u093f\u0936\u093e \u092e\u0947\u0902",
        "Mercury": "\u0938\u0902\u0935\u093e\u0926 \u092e\u0947\u0902 \u092c\u0926\u0932\u093e\u0935",
        "Jupiter": "\u0935\u093f\u0938\u094d\u0924\u093e\u0930 \u0928\u090f \u0915\u094d\u0937\u0947\u0924\u094d\u0930 \u092e\u0947\u0902",
        "Venus": "\u092a\u094d\u0930\u0947\u092e \u0914\u0930 \u092e\u0942\u0932\u094d\u092f\u094b\u0902 \u092e\u0947\u0902 \u092a\u0930\u093f\u0935\u0930\u094d\u0924\u0928",
        "Saturn": "\u0905\u0928\u0941\u0936\u093e\u0938\u0928 \u0928\u092f\u093e \u0930\u0942\u092a \u0932\u0947\u0924\u093e \u0939\u0948",
    }
    return meanings.get(planet, "\u092a\u094d\u0930\u092d\u093e\u0935 \u092e\u0947\u0902 \u092c\u0926\u0932\u093e\u0935")


def _fallback_planet_data() -> Dict[str, Dict]:
    """Return a minimal fallback planet data dict when calculation fails."""
    default_signs = {
        "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
        "Mercury": "Gemini", "Jupiter": "Sagittarius", "Venus": "Taurus",
        "Saturn": "Aquarius", "Rahu": "Pisces", "Ketu": "Virgo",
    }
    result = {}
    for planet, sign in default_signs.items():
        result[planet] = {
            "sign": sign,
            "sign_degree": 15.0,
            "nakshatra": "Ashwini",
            "nakshatra_pada": 1,
            "house": 1,
            "retrograde": False,
            "is_combust": False,
            "status": "",
        }
    return result


def _fallback_horoscope(sign: str, period: str) -> Dict[str, Any]:
    """Return a complete fallback horoscope when transit calculation fails entirely."""
    sections = {}
    for area in AREAS:
        sections[area] = {
            "en": _default_section_text(sign, area, "en"),
            "hi": _default_section_text(sign, area, "hi"),
        }

    return {
        "sign": sign,
        "period": period,
        "sections": sections,
        "scores": {"overall": 5, "love": 5, "career": 5, "finance": 5, "health": 5},
        "mood": {"en": "Balanced", "hi": "\u0938\u0902\u0924\u0941\u0932\u093f\u0924"},
        "lucky": {
            "number": (SIGN_INDEX.get(sign, 0) + 1),
            "color": {"en": "Green", "hi": "\u0939\u0930\u093e"},
            "time": _LUCKY_TIMES[SIGN_INDEX.get(sign, 0) % len(_LUCKY_TIMES)],
            "compatible_sign": {"en": "Leo", "hi": "\u0938\u093f\u0902\u0939"},
            "gemstone": _DEFAULT_GEMSTONES.get(sign, {"en": "Pearl (Moti)", "hi": "\u092e\u094b\u0924\u0940"}),
            "mantra": _DEFAULT_MANTRAS.get(RULERS.get(sign, "Sun"), ""),
        },
        "dos": [{"en": "Stay positive and focused.", "hi": "\u0938\u0915\u093e\u0930\u093e\u0924\u094d\u092e\u0915 \u0914\u0930 \u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924 \u0930\u0939\u0947\u0902\u0964"}],
        "donts": [{"en": "Avoid impulsive decisions.", "hi": "\u0906\u0935\u0947\u0917\u092a\u0942\u0930\u094d\u0923 \u0928\u093f\u0930\u094d\u0923\u092f\u094b\u0902 \u0938\u0947 \u092c\u091a\u0947\u0902\u0964"}],
        "source": "transit_engine",
    }


# ===================================================================
# Backward-compatible exports from original transit_engine.py
# ===================================================================
# The original module provided Gochara-based transit analysis.
# These are re-exported to avoid breaking existing callers.

# Zodiac helpers (used by original callers)
from app.astro_engine import _SIGN_NAMES

ZODIAC_INDEX: Dict[str, int] = {sign: i for i, sign in enumerate(_SIGN_NAMES)}


def _house_from_moon(moon_sign: str, transit_sign: str) -> int:
    """
    Return the house number (1-12) of transit_sign counted from moon_sign.
    House 1 = same sign as Moon.
    """
    moon_idx = ZODIAC_INDEX.get(moon_sign, 0)
    transit_idx = ZODIAC_INDEX.get(transit_sign, 0)
    return ((transit_idx - moon_idx) % 12) + 1


# Gochara favourability rules
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

_FAVORABLE_DESC: Dict[str, str] = {
    "Jupiter":  "Jupiter's benevolent transit brings expansion, wisdom, and opportunities in this area of life.",
    "Saturn":   "Saturn's transit here gives discipline, endurance, and eventual rewards through hard work.",
    "Rahu":     "Rahu's transit here can bring unconventional gains and bold breakthroughs.",
    "Ketu":     "Ketu's transit here supports spiritual detachment and release of old patterns.",
    "Mars":     "Mars transiting here channels energy productively -- courage and initiative are favored.",
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
                "This is the most intense phase -- expect emotional pressure, career challenges, "
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


def calculate_transits(
    natal_chart_data: Dict[str, Any],
    latitude: float = 0.0,
    longitude: float = 0.0,
    transit_date: str = None,
    transit_time: str = None,
) -> Dict[str, Any]:
    """
    Calculate planetary transits and their Gochara effects on a natal chart.

    This is the original transit_engine entry point, preserved for backward compatibility.
    """
    from datetime import timedelta

    tz_offset = longitude / 15.0

    if transit_date and transit_time:
        today_str = transit_date
        time_str = transit_time
    elif transit_date:
        today_str = transit_date
        time_str = "12:00:00"
    else:
        now_utc = datetime.now(timezone.utc)
        today_str = now_utc.strftime("%Y-%m-%d")
        time_str = now_utc.strftime("%H:%M:%S")
        tz_offset = 0.0

    current_positions = calculate_planet_positions(
        birth_date=today_str,
        birth_time=time_str,
        latitude=latitude,
        longitude=longitude,
        tz_offset=tz_offset,
    )

    natal_planets = natal_chart_data.get("planets", {})
    natal_moon = natal_planets.get("Moon", {})
    natal_moon_sign = natal_moon.get("sign", "Aries")

    transits: List[Dict[str, Any]] = []
    current_planets = current_positions.get("planets", {})
    saturn_current_sign = "Capricorn"

    favorable_count = 0
    total_planets = 0

    for planet_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        planet_info = current_planets.get(planet_name, {})
        current_sign = planet_info.get("sign", "Aries")

        if planet_name == "Saturn":
            saturn_current_sign = current_sign

        house_from_moon = _house_from_moon(natal_moon_sign, current_sign)
        favorable_houses = GOCHARA_FAVORABLE.get(planet_name, set())
        is_favorable = house_from_moon in favorable_houses

        weight = 3 if planet_name in ["Jupiter", "Saturn", "Rahu", "Ketu"] else 1
        if is_favorable:
            favorable_count += weight
        total_planets += weight

        effect = "favorable" if is_favorable else "unfavorable"

        description = (
            _FAVORABLE_DESC.get(planet_name, "")
            if is_favorable
            else _UNFAVORABLE_DESC.get(planet_name, "")
        )
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

    score = int((favorable_count / total_planets) * 100) if total_planets > 0 else 50

    sade_sati = _check_sade_sati(natal_moon_sign, saturn_current_sign)

    return {
        "transits": transits,
        "sade_sati": sade_sati,
        "transit_date": today_str,
        "daily_score": score,
        "natal_moon_sign": natal_moon_sign,
        "chart_data": {
            "ascendant": current_positions.get("ascendant"),
            "houses": current_positions.get("houses"),
        },
    }


def calculate_transit_forecast(
    natal_chart_data: Dict[str, Any],
    latitude: float = 0.0,
    longitude: float = 0.0,
    days: int = 30,
) -> List[Dict[str, Any]]:
    """
    Calculate transit intensity scores for the next N days.

    Preserved from original transit_engine for backward compatibility.
    """
    from datetime import timedelta

    forecast = []
    now = datetime.now(timezone.utc)

    for i in range(days):
        target_date = now + timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")

        res = calculate_transits(natal_chart_data, latitude, longitude, transit_date=date_str, transit_time="12:00:00")

        forecast.append({
            "date": date_str,
            "score": res["daily_score"],
            "summary": "Good" if res["daily_score"] >= 70 else "Average" if res["daily_score"] >= 40 else "Challenging",
        })

    return forecast
