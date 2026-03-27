"""
muhurat_engine.py -- Advanced Muhurat (Auspicious Timing) Finder Engine
=======================================================================
Calculates auspicious time windows for various life events based on
Vedic panchang elements (tithi, nakshatra, yoga) and inauspicious
periods (Rahu Kaal).

Uses the existing panchang_engine for core astronomical calculations.
"""
from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from app.panchang_engine import (
    TITHIS,
    YOGAS,
    _approx_sunrise_sunset,
    _time_to_minutes,
    _minutes_to_time,
    calculate_panchang,
    calculate_rahu_kaal,
    calculate_choghadiya,
)

# ============================================================
# SUPPORTED EVENT TYPES
# ============================================================

EVENT_TYPES: Dict[str, Dict[str, Any]] = {
    "marriage": {
        "name": "Marriage (Vivah)",
        "description": "Wedding ceremony - requires highly auspicious alignments of tithi, nakshatra, and yoga.",
    },
    "griha_pravesh": {
        "name": "Griha Pravesh (Housewarming)",
        "description": "Entering a new home for the first time - favorable nakshatras and tithis are essential.",
    },
    "business_start": {
        "name": "Business Start",
        "description": "Starting a new business venture or signing important contracts.",
    },
    "travel": {
        "name": "Travel",
        "description": "Beginning an important journey - avoid Rahu Kaal and unfavorable nakshatras.",
    },
    "mundan": {
        "name": "Mundan (First Haircut)",
        "description": "First tonsure ceremony for a child - specific nakshatras and tithis are preferred.",
    },
    "namkaran": {
        "name": "Namkaran (Naming Ceremony)",
        "description": "Naming ceremony for a newborn child.",
    },
    "vehicle_purchase": {
        "name": "Vehicle Purchase",
        "description": "Purchasing a new vehicle - favorable tithis and avoidance of Rahu Kaal recommended.",
    },
    "property_purchase": {
        "name": "Property Purchase",
        "description": "Buying land or property - requires stable nakshatras and auspicious tithis.",
    },
}

# ============================================================
# FAVORABLE / UNFAVORABLE RULES PER EVENT TYPE
# ============================================================
# Tithi names (without paksha) that are favorable for each event.
# Nakshatra names that are favorable.
# Yoga names that are favorable.
# Also list unfavorable elements to explicitly avoid.

_EVENT_RULES: Dict[str, Dict[str, Any]] = {
    "marriage": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Ekadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Magha", "Uttara Phalguni",
            "Hasta", "Swati", "Anuradha", "Moola",
            "Uttara Ashadha", "Uttara Bhadrapada", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Vishakha", "Jyeshtha", "Purva Ashadha",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Harshana", "Siddhi",
            "Shiva", "Siddha", "Sadhya", "Shubha",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "griha_pravesh": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Uttara Phalguni", "Hasta",
            "Chitra", "Swati", "Anuradha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Uttara Bhadrapada", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha", "Jyeshtha",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Harshana", "Siddhi",
            "Shiva", "Siddha", "Sadhya", "Shubha", "Brahma", "Indra",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "business_start": {
        "favorable_tithis": [
            "Pratipada", "Dwitiya", "Tritiya", "Panchami",
            "Saptami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Pushya",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati",
            "Anuradha", "Shravana", "Dhanishta", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Purva Phalguni", "Vishakha", "Jyeshtha",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Vriddhi", "Dhruva",
            "Harshana", "Siddhi", "Shiva", "Siddha",
            "Sadhya", "Shubha", "Brahma", "Indra",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "travel": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Ashwini", "Mrigashira", "Punarvasu", "Pushya",
            "Hasta", "Chitra", "Swati", "Anuradha",
            "Shravana", "Dhanishta", "Shatabhisha", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Magha", "Uttara Phalguni", "Vishakha", "Jyeshtha",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Harshana", "Siddhi",
            "Variyan", "Shiva", "Siddha", "Sadhya", "Shubha",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": None,  # Either paksha acceptable
    },
    "mundan": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Shashthi", "Ashtami", "Navami",
            "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Punarvasu",
            "Pushya", "Hasta", "Chitra", "Swati",
            "Shravana", "Dhanishta", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Magha", "Vishakha", "Jyeshtha", "Moola",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Harshana", "Siddhi",
            "Shiva", "Siddha", "Sadhya", "Shubha",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "namkaran": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Punarvasu",
            "Pushya", "Uttara Phalguni", "Hasta", "Chitra",
            "Swati", "Anuradha", "Shravana", "Dhanishta",
            "Uttara Bhadrapada", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Jyeshtha", "Moola",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Harshana", "Siddhi",
            "Shiva", "Siddha", "Sadhya", "Shubha", "Brahma", "Indra",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "vehicle_purchase": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Punarvasu",
            "Pushya", "Uttara Phalguni", "Hasta", "Chitra",
            "Swati", "Anuradha", "Shravana", "Dhanishta", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Vishakha", "Jyeshtha", "Purva Bhadrapada",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Vriddhi", "Harshana",
            "Siddhi", "Shiva", "Siddha", "Sadhya", "Shubha",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
    "property_purchase": {
        "favorable_tithis": [
            "Dwitiya", "Tritiya", "Panchami", "Saptami",
            "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Purnima",
        ],
        "unfavorable_tithis": [
            "Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya",
        ],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Uttara Phalguni", "Hasta",
            "Chitra", "Swati", "Anuradha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Uttara Bhadrapada", "Revati",
        ],
        "unfavorable_nakshatras": [
            "Bharani", "Krittika", "Ardra", "Ashlesha",
            "Purva Phalguni", "Vishakha", "Jyeshtha", "Purva Ashadha",
        ],
        "favorable_yogas": [
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Sukarma", "Dhriti", "Vriddhi", "Dhruva",
            "Harshana", "Siddhi", "Shiva", "Siddha",
            "Sadhya", "Shubha", "Brahma", "Indra",
        ],
        "unfavorable_yogas": [
            "Vishkambha", "Atiganda", "Shoola", "Ganda",
            "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti",
        ],
        "avoid_rahu_kaal": True,
        "preferred_paksha": "Shukla",
    },
}


# ============================================================
# SCORING HELPERS
# ============================================================

def _score_panchang_for_event(
    panchang: Dict[str, Any],
    rules: Dict[str, Any],
) -> Tuple[int, List[str], List[str]]:
    """
    Score a panchang result against event rules.

    Returns:
        (score, positive_factors, negative_factors)
        score range: -100 to +100 approximately
    """
    score = 0
    positives: List[str] = []
    negatives: List[str] = []

    tithi_name = panchang["tithi"]["name"]
    paksha = panchang["tithi"]["paksha"]
    nakshatra_name = panchang["nakshatra"]["name"]
    yoga_name = panchang["yoga"]["name"]

    # -- Tithi scoring --
    if tithi_name in rules.get("favorable_tithis", []):
        score += 25
        positives.append(f"Favorable tithi: {tithi_name}")
    elif tithi_name in rules.get("unfavorable_tithis", []):
        score -= 30
        negatives.append(f"Unfavorable tithi: {tithi_name}")
    else:
        score += 5  # neutral tithi

    # -- Paksha preference --
    preferred = rules.get("preferred_paksha")
    if preferred:
        if paksha == preferred:
            score += 10
            positives.append(f"Preferred paksha: {paksha}")
        else:
            score -= 10
            negatives.append(f"Non-preferred paksha: {paksha}")

    # -- Nakshatra scoring --
    if nakshatra_name in rules.get("favorable_nakshatras", []):
        score += 25
        positives.append(f"Favorable nakshatra: {nakshatra_name}")
    elif nakshatra_name in rules.get("unfavorable_nakshatras", []):
        score -= 30
        negatives.append(f"Unfavorable nakshatra: {nakshatra_name}")
    else:
        score += 5  # neutral nakshatra

    # -- Yoga scoring --
    if yoga_name in rules.get("favorable_yogas", []):
        score += 20
        positives.append(f"Favorable yoga: {yoga_name}")
    elif yoga_name in rules.get("unfavorable_yogas", []):
        score -= 25
        negatives.append(f"Unfavorable yoga: {yoga_name}")
    else:
        score += 5  # neutral yoga

    return score, positives, negatives


def _quality_from_score(score: int) -> str:
    """Map a numeric score to a quality label."""
    if score >= 55:
        return "excellent"
    elif score >= 30:
        return "good"
    elif score >= 10:
        return "average"
    else:
        return "poor"


def _compute_auspicious_windows(
    date_str: str,
    latitude: float,
    longitude: float,
    rules: Dict[str, Any],
    panchang: Dict[str, Any],
    base_score: int,
) -> List[Dict[str, Any]]:
    """
    Compute auspicious time windows within a single day by excluding
    Rahu Kaal and inauspicious Choghadiya periods.

    Returns a list of window dicts with start, end, and quality.
    """
    sunrise_str = panchang["sunrise"]
    sunset_str = panchang["sunset"]
    sr_min = _time_to_minutes(sunrise_str)
    ss_min = _time_to_minutes(sunset_str)

    # Parse date for weekday
    parts = date_str.split("-")
    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    weekday = dt.weekday()

    # Collect inauspicious intervals to exclude
    blocked_intervals: List[Tuple[float, float]] = []

    # Rahu Kaal
    if rules.get("avoid_rahu_kaal", True):
        rk = calculate_rahu_kaal(weekday, sunrise_str, sunset_str)
        rk_start = _time_to_minutes(rk["start"])
        rk_end = _time_to_minutes(rk["end"])
        blocked_intervals.append((rk_start, rk_end))

    # Inauspicious Choghadiya periods (Rog, Kaal, Udveg)
    choghadiya = calculate_choghadiya(weekday, sunrise_str, sunset_str)
    for period in choghadiya:
        if period["quality"] == "Inauspicious":
            ch_start = _time_to_minutes(period["start"])
            ch_end = _time_to_minutes(period["end"])
            blocked_intervals.append((ch_start, ch_end))

    # Merge overlapping blocked intervals
    blocked_intervals.sort()
    merged: List[Tuple[float, float]] = []
    for start, end in blocked_intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Build open windows from sunrise to sunset, excluding blocked intervals
    windows: List[Dict[str, Any]] = []
    current = sr_min

    for block_start, block_end in merged:
        if current < block_start:
            # There is an open window before this blocked interval
            window_duration = block_start - current
            if window_duration >= 30:  # minimum 30-minute window
                # Bonus for longer windows
                duration_bonus = min(int(window_duration / 60) * 2, 10)
                window_score = base_score + duration_bonus
                quality = _quality_from_score(window_score)
                if quality != "poor":
                    windows.append({
                        "start": _minutes_to_time(current),
                        "end": _minutes_to_time(block_start),
                        "duration_minutes": int(window_duration),
                        "quality": quality,
                    })
        current = max(current, block_end)

    # Final window from last blocked interval to sunset
    if current < ss_min:
        window_duration = ss_min - current
        if window_duration >= 30:
            duration_bonus = min(int(window_duration / 60) * 2, 10)
            window_score = base_score + duration_bonus
            quality = _quality_from_score(window_score)
            if quality != "poor":
                windows.append({
                    "start": _minutes_to_time(current),
                    "end": _minutes_to_time(ss_min),
                    "duration_minutes": int(window_duration),
                    "quality": quality,
                })

    return windows


# ============================================================
# PUBLIC: find_muhurat
# ============================================================

def find_muhurat(
    event_type: str,
    date_str: str,
    latitude: float,
    longitude: float,
) -> Dict[str, Any]:
    """
    Find auspicious muhurat windows for a specific event on a given date.

    Args:
        event_type:  One of the keys in EVENT_TYPES
        date_str:    ISO date "YYYY-MM-DD"
        latitude:    Location latitude
        longitude:   Location longitude

    Returns:
        {
            date: str,
            event_type: str,
            event_name: str,
            panchang: { tithi, nakshatra, yoga, karana, sunrise, sunset },
            rahu_kaal: { start, end },
            score: int,
            quality: str,
            positive_factors: [str],
            negative_factors: [str],
            auspicious_windows: [{ start, end, duration_minutes, quality }],
            is_auspicious: bool,
        }
    """
    if event_type not in _EVENT_RULES:
        raise ValueError(f"Unsupported event type: '{event_type}'. Supported: {list(EVENT_TYPES.keys())}")

    rules = _EVENT_RULES[event_type]
    event_info = EVENT_TYPES[event_type]

    # Calculate panchang for the date
    panchang = calculate_panchang(date_str, latitude, longitude)

    # Score the day
    score, positives, negatives = _score_panchang_for_event(panchang, rules)
    quality = _quality_from_score(score)

    # Get Rahu Kaal
    parts = date_str.split("-")
    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    weekday = dt.weekday()
    rahu_kaal = calculate_rahu_kaal(weekday, panchang["sunrise"], panchang["sunset"])

    # Find auspicious time windows within the day
    auspicious_windows = _compute_auspicious_windows(
        date_str, latitude, longitude, rules, panchang, score,
    )

    # A day is considered auspicious if score >= 10 and there is at least one window
    is_auspicious = score >= 10 and len(auspicious_windows) > 0

    return {
        "date": date_str,
        "event_type": event_type,
        "event_name": event_info["name"],
        "panchang": panchang,
        "rahu_kaal": rahu_kaal,
        "score": score,
        "quality": quality,
        "positive_factors": positives,
        "negative_factors": negatives,
        "auspicious_windows": auspicious_windows,
        "is_auspicious": is_auspicious,
    }


# ============================================================
# PUBLIC: get_monthly_muhurats
# ============================================================

def get_monthly_muhurats(
    event_type: str,
    month: int,
    year: int,
    latitude: float,
    longitude: float,
) -> Dict[str, Any]:
    """
    Find all auspicious dates in a month for a given event type.

    Args:
        event_type:  One of the keys in EVENT_TYPES
        month:       Month number (1-12)
        year:        Year (YYYY)
        latitude:    Location latitude
        longitude:   Location longitude

    Returns:
        {
            event_type: str,
            event_name: str,
            month: int,
            year: int,
            latitude: float,
            longitude: float,
            auspicious_dates: [
                {
                    date: str,
                    quality: str,
                    score: int,
                    tithi: str,
                    nakshatra: str,
                    yoga: str,
                    best_window: { start, end, duration_minutes, quality } | None,
                    positive_factors: [str],
                    negative_factors: [str],
                }
            ],
            total_auspicious_days: int,
        }
    """
    if event_type not in _EVENT_RULES:
        raise ValueError(f"Unsupported event type: '{event_type}'. Supported: {list(EVENT_TYPES.keys())}")

    event_info = EVENT_TYPES[event_type]
    days_in_month = calendar.monthrange(year, month)[1]

    auspicious_dates: List[Dict[str, Any]] = []

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        d_str = d.isoformat()

        result = find_muhurat(event_type, d_str, latitude, longitude)

        if result["is_auspicious"]:
            # Pick the best window (longest with highest quality)
            best_window = None
            if result["auspicious_windows"]:
                # Sort by quality then duration
                quality_order = {"excellent": 3, "good": 2, "average": 1, "poor": 0}
                sorted_windows = sorted(
                    result["auspicious_windows"],
                    key=lambda w: (quality_order.get(w["quality"], 0), w["duration_minutes"]),
                    reverse=True,
                )
                best_window = sorted_windows[0]

            auspicious_dates.append({
                "date": d_str,
                "quality": result["quality"],
                "score": result["score"],
                "tithi": f"{result['panchang']['tithi']['paksha']} {result['panchang']['tithi']['name']}",
                "nakshatra": result["panchang"]["nakshatra"]["name"],
                "yoga": result["panchang"]["yoga"]["name"],
                "best_window": best_window,
                "positive_factors": result["positive_factors"],
                "negative_factors": result["negative_factors"],
            })

    # Sort by score descending so best dates appear first
    auspicious_dates.sort(key=lambda x: x["score"], reverse=True)

    return {
        "event_type": event_type,
        "event_name": event_info["name"],
        "month": month,
        "year": year,
        "latitude": latitude,
        "longitude": longitude,
        "auspicious_dates": auspicious_dates,
        "total_auspicious_days": len(auspicious_dates),
    }
