"""
birth_rectification_engine.py — Birth Time Rectification Engine
================================================================
Tests multiple birth times within a user-defined window and scores each
candidate by how well Vimshottari Dasha periods + planetary transits
explain known life events. Returns the top candidates ranked by score.

Provides:
  - calculate_rectification(birth_date, time_window_start, time_window_end,
        birth_place, life_events, step_minutes=1)
  - _score_event_match(event, dasha_at_event, transit_at_event, birth_chart)
  - _get_event_signatures(event_type)
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from app.astro_engine import (
    calculate_planet_positions,
    get_nakshatra_from_longitude,
    _SIGN_NAMES,
)
from app.dasha_engine import (
    calculate_dasha,
    DASHA_YEARS,
    NAKSHATRA_LORD,
    _get_dasha_sequence,
)

# ============================================================
# EVENT SIGNATURES
# ============================================================

# Each event type maps to:
#   dasha_lords:       planets whose Mahadasha/Antardasha is a positive signal
#   houses:            houses that should be activated (planet transiting OR lord active)
#   transit_planets:   planets whose transit over the relevant houses is meaningful
#   malefic:           if True, the event is a hardship (affliction, not activation)

EVENT_SIGNATURES: Dict[str, Dict[str, Any]] = {
    "marriage": {
        "dasha_lords": {"Venus", "Jupiter", "Moon"},
        "houses": {7, 2, 11},
        "transit_planets": {"Jupiter", "Venus"},
        "malefic": False,
    },
    "child_birth": {
        "dasha_lords": {"Jupiter", "Venus", "Moon"},
        "houses": {5, 9, 2},
        "transit_planets": {"Jupiter"},
        "malefic": False,
    },
    "job_start": {
        "dasha_lords": {"Saturn", "Sun", "Mercury", "Jupiter"},
        "houses": {10, 6, 2, 11},
        "transit_planets": {"Jupiter", "Saturn", "Sun"},
        "malefic": False,
    },
    "job_loss": {
        "dasha_lords": {"Saturn", "Rahu", "Ketu", "Mars"},
        "houses": {10, 6, 8},
        "transit_planets": {"Saturn", "Rahu"},
        "malefic": True,
    },
    "accident": {
        "dasha_lords": {"Mars", "Rahu", "Ketu", "Saturn"},
        "houses": {6, 8, 12},
        "transit_planets": {"Mars", "Rahu", "Ketu"},
        "malefic": True,
    },
    "education": {
        "dasha_lords": {"Mercury", "Jupiter", "Venus"},
        "houses": {4, 5, 9},
        "transit_planets": {"Jupiter", "Mercury"},
        "malefic": False,
    },
    "foreign_travel": {
        "dasha_lords": {"Rahu", "Ketu", "Jupiter", "Moon"},
        "houses": {9, 12, 3},
        "transit_planets": {"Rahu", "Ketu", "Jupiter"},
        "malefic": False,
    },
    "property": {
        "dasha_lords": {"Mars", "Venus", "Saturn", "Jupiter"},
        "houses": {4, 2, 11},
        "transit_planets": {"Mars", "Jupiter", "Venus"},
        "malefic": False,
    },
    "father_death": {
        "dasha_lords": {"Sun", "Saturn", "Rahu", "Ketu"},
        "houses": {9, 10, 8},
        "transit_planets": {"Saturn", "Sun"},
        "malefic": True,
    },
    "mother_death": {
        "dasha_lords": {"Moon", "Saturn", "Rahu", "Ketu"},
        "houses": {4, 10, 8},
        "transit_planets": {"Saturn", "Moon"},
        "malefic": True,
    },
    "health_issue": {
        "dasha_lords": {"Saturn", "Mars", "Rahu", "Ketu"},
        "houses": {6, 8, 12},
        "transit_planets": {"Saturn", "Mars", "Rahu"},
        "malefic": True,
    },
}

# ============================================================
# HOUSE LORD MAPPING
# ============================================================

# Sign -> natural lord (for determining house lords from Whole-Sign houses)
SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}


def _get_house_lord(birth_chart: Dict[str, Any], house_number: int) -> Optional[str]:
    """Return the lord of a house based on the sign occupying that house."""
    houses = birth_chart.get("houses", [])
    for h in houses:
        if h.get("number") == house_number:
            sign = h.get("sign", "")
            return SIGN_LORD.get(sign)
    return None


def _get_planets_in_house(birth_chart: Dict[str, Any], house_number: int) -> List[str]:
    """Return list of planets occupying a given house."""
    planets = birth_chart.get("planets", {})
    return [p for p, info in planets.items() if info.get("house") == house_number]


# ============================================================
# DASHA AT EVENT DATE
# ============================================================

def _get_dasha_at_date(
    birth_nakshatra: str,
    birth_date: str,
    moon_longitude: float,
    event_date: str,
) -> Dict[str, str]:
    """
    Determine the Mahadasha and Antardasha lords active on a given event date.

    Returns: {"mahadasha": "Venus", "antardasha": "Jupiter"}
    """
    dasha_data = calculate_dasha(birth_nakshatra, birth_date, moon_longitude)
    event_dt = datetime.strptime(event_date, "%Y-%m-%d")

    mahadasha_lord = "Unknown"
    antardasha_lord = "Unknown"

    for period in dasha_data.get("mahadasha_periods", []):
        start_dt = datetime.strptime(period["start_date"], "%Y-%m-%d")
        end_dt = datetime.strptime(period["end_date"], "%Y-%m-%d")
        if start_dt <= event_dt <= end_dt:
            mahadasha_lord = period["planet"]
            # Calculate antardasha within this mahadasha
            md_years = period["years"]
            ad_seq = _get_dasha_sequence(mahadasha_lord)
            ad_start = start_dt
            for ad_planet in ad_seq:
                ad_years = DASHA_YEARS[ad_planet]
                ad_duration_days = (md_years * ad_years / 120) * 365.25
                ad_end = ad_start + timedelta(days=ad_duration_days)
                if ad_start <= event_dt <= ad_end:
                    antardasha_lord = ad_planet
                    break
                ad_start = ad_end
            break

    return {"mahadasha": mahadasha_lord, "antardasha": antardasha_lord}


# ============================================================
# TRANSIT AT EVENT DATE
# ============================================================

def _get_transit_at_date(
    event_date: str,
    birth_place: Dict[str, float],
    tz_offset: float = 5.5,
) -> Dict[str, Any]:
    """
    Calculate planetary positions on a specific date (at noon) from the
    event location. Returns the same structure as calculate_planet_positions.
    """
    return calculate_planet_positions(
        birth_date=event_date,
        birth_time="12:00",
        latitude=birth_place.get("lat", 0.0),
        longitude=birth_place.get("lon", 0.0),
        tz_offset=tz_offset,
    )


# ============================================================
# SCORING
# ============================================================

def _get_event_signatures(event_type: str) -> Dict[str, Any]:
    """
    Return expected dasha lords, houses, and transit planets for an event type.
    Falls back to a generic signature if type is unknown.
    """
    return EVENT_SIGNATURES.get(event_type, {
        "dasha_lords": set(),
        "houses": set(),
        "transit_planets": set(),
        "malefic": False,
    })


def _score_event_match(
    event: Dict[str, Any],
    dasha_at_event: Dict[str, str],
    transit_at_event: Dict[str, Any],
    birth_chart: Dict[str, Any],
) -> float:
    """
    Score 0-100 how well the dasha + transit configuration explains the event.

    Scoring components (total = 100):
      - Mahadasha lord match:  0-30 points
      - Antardasha lord match: 0-20 points
      - Transit activation:    0-30 points
      - House lord activation: 0-20 points
    """
    event_type = event.get("type", "")
    sig = _get_event_signatures(event_type)
    if not sig.get("dasha_lords"):
        return 0.0

    score = 0.0
    explanation_parts: List[str] = []

    md_lord = dasha_at_event.get("mahadasha", "")
    ad_lord = dasha_at_event.get("antardasha", "")
    expected_dasha = sig["dasha_lords"]
    expected_houses = sig["houses"]
    expected_transit = sig["transit_planets"]

    # 1. Mahadasha lord match (0-30)
    if md_lord in expected_dasha:
        score += 30.0
        explanation_parts.append(f"{md_lord} Mahadasha")
    elif ad_lord in expected_dasha and md_lord != "Unknown":
        # Partial credit if mahadasha doesn't match but antardasha does
        score += 10.0

    # 2. Antardasha lord match (0-20)
    if ad_lord in expected_dasha:
        score += 20.0
        explanation_parts.append(f"{ad_lord} Antardasha")
    elif md_lord in expected_dasha and ad_lord != "Unknown":
        score += 5.0

    # 3. Transit activation (0-30)
    # Check if transit planets are transiting relevant houses from ascendant
    transit_planets = transit_at_event.get("planets", {})
    asc_sign = birth_chart.get("ascendant", {}).get("sign", "Aries")
    asc_index = _SIGN_NAMES.index(asc_sign) if asc_sign in _SIGN_NAMES else 0

    transit_score = 0.0
    transit_hits = 0
    for t_planet in expected_transit:
        t_info = transit_planets.get(t_planet, {})
        t_sign = t_info.get("sign", "")
        if t_sign and t_sign in _SIGN_NAMES:
            t_sign_index = _SIGN_NAMES.index(t_sign)
            t_house = ((t_sign_index - asc_index) % 12) + 1
            if t_house in expected_houses:
                transit_hits += 1
                explanation_parts.append(f"{t_planet} transit {_ordinal(t_house)} house")

    if expected_transit:
        transit_score = (transit_hits / len(expected_transit)) * 30.0
    score += transit_score

    # 4. House lord activation (0-20)
    # Check if the dasha lords rule any of the expected houses
    house_lord_score = 0.0
    house_hits = 0
    for h_num in expected_houses:
        h_lord = _get_house_lord(birth_chart, h_num)
        if h_lord and (h_lord == md_lord or h_lord == ad_lord):
            house_hits += 1
            explanation_parts.append(f"{_ordinal(h_num)} lord {h_lord} in dasha")

    if expected_houses:
        house_lord_score = (house_hits / len(expected_houses)) * 20.0
    score += house_lord_score

    return round(min(score, 100.0), 1)


def _ordinal(n: int) -> str:
    """Return ordinal string for a number: 1st, 2nd, 3rd, etc."""
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _build_explanation(
    event: Dict[str, Any],
    dasha_at_event: Dict[str, str],
    transit_at_event: Dict[str, Any],
    birth_chart: Dict[str, Any],
) -> str:
    """Build a human-readable explanation for an event match."""
    event_type = event.get("type", "")
    sig = _get_event_signatures(event_type)
    md_lord = dasha_at_event.get("mahadasha", "Unknown")
    ad_lord = dasha_at_event.get("antardasha", "Unknown")

    parts = [f"{md_lord} Mahadasha"]
    if ad_lord != "Unknown":
        parts.append(f"{ad_lord} Antardasha")

    # Transit info
    transit_planets = transit_at_event.get("planets", {})
    asc_sign = birth_chart.get("ascendant", {}).get("sign", "Aries")
    asc_index = _SIGN_NAMES.index(asc_sign) if asc_sign in _SIGN_NAMES else 0

    for t_planet in sig.get("transit_planets", set()):
        t_info = transit_planets.get(t_planet, {})
        t_sign = t_info.get("sign", "")
        if t_sign and t_sign in _SIGN_NAMES:
            t_sign_index = _SIGN_NAMES.index(t_sign)
            t_house = ((t_sign_index - asc_index) % 12) + 1
            if t_house in sig.get("houses", set()):
                parts.append(f"{t_planet} transit {_ordinal(t_house)}")

    return ", ".join(parts)


# ============================================================
# MAIN RECTIFICATION
# ============================================================

def calculate_rectification(
    birth_date: str,
    time_window_start: str,
    time_window_end: str,
    birth_place: Dict[str, float],
    life_events: List[Dict[str, str]],
    step_minutes: int = 1,
    tz_offset: float = 5.5,
) -> Dict[str, Any]:
    """
    Test multiple birth times within a window and score each candidate
    by how well Vimshottari Dasha + transits explain known life events.

    Args:
        birth_date:        "YYYY-MM-DD"
        time_window_start: "HH:MM" start of search window
        time_window_end:   "HH:MM" end of search window
        birth_place:       {"lat": float, "lon": float}
        life_events:       [{"date": "YYYY-MM-DD", "type": "marriage"}, ...]
        step_minutes:      minutes between candidate times (default 1)
        tz_offset:         timezone offset in hours (default 5.5 for IST)

    Returns:
        {
            "candidates": [...],
            "best_time": "HH:MM",
            "confidence": "high" | "medium" | "low",
            "analysis_summary": "..."
        }
    """
    if not life_events:
        return {
            "candidates": [],
            "best_time": None,
            "confidence": "low",
            "analysis_summary": "No life events provided for rectification.",
        }

    # Parse time window into minutes from midnight
    start_h, start_m = map(int, time_window_start.split(":"))
    end_h, end_m = map(int, time_window_end.split(":"))
    start_total_min = start_h * 60 + start_m
    end_total_min = end_h * 60 + end_m

    # Support midnight-crossing windows (e.g., 23:00 → 01:00)
    if end_total_min < start_total_min:
        end_total_min += 24 * 60  # wrap to next day

    # Cap max candidates to prevent DoS (300 candidates max)
    MAX_CANDIDATES = 300
    total_candidates = (end_total_min - start_total_min) // step_minutes + 1
    if total_candidates > MAX_CANDIDATES:
        step_minutes = max(step_minutes, (end_total_min - start_total_min) // MAX_CANDIDATES + 1)

    # Pre-compute transit positions for each event date (shared across candidates)
    event_transits: Dict[str, Dict[str, Any]] = {}
    for ev in life_events:
        ev_date = ev.get("date", "")
        if ev_date and ev_date not in event_transits:
            event_transits[ev_date] = _get_transit_at_date(
                ev_date, birth_place, tz_offset
            )

    # Test each candidate time
    candidates: List[Dict[str, Any]] = []

    current_min = start_total_min
    while current_min <= end_total_min:
        h = (current_min // 60) % 24
        m = current_min % 60
        candidate_time = f"{h:02d}:{m:02d}"

        # Calculate birth chart for this candidate time
        try:
            chart = calculate_planet_positions(
                birth_date=birth_date,
                birth_time=candidate_time,
                latitude=birth_place.get("lat", 0.0),
                longitude=birth_place.get("lon", 0.0),
                tz_offset=tz_offset,
            )
        except Exception:
            current_min += step_minutes
            continue

        # Get Moon nakshatra for dasha calculation
        moon_info = chart.get("planets", {}).get("Moon", {})
        moon_lon = moon_info.get("longitude", 0.0)
        moon_nak = get_nakshatra_from_longitude(moon_lon)
        birth_nakshatra = moon_nak["name"]

        # Ascendant info
        asc_info = chart.get("ascendant", {})
        asc_sign = asc_info.get("sign", "Unknown")
        asc_lon = asc_info.get("longitude", 0.0)

        # Score each life event
        event_matches: List[Dict[str, Any]] = []
        total_score = 0.0

        for ev in life_events:
            ev_date = ev.get("date", "")
            ev_type = ev.get("type", "")

            if not ev_date:
                continue

            # Get dasha at event date for this candidate birth time
            dasha_at = _get_dasha_at_date(
                birth_nakshatra, birth_date, moon_lon, ev_date
            )

            # Get pre-computed transit
            transit_at = event_transits.get(ev_date, {})

            # Score
            ev_score = _score_event_match(ev, dasha_at, transit_at, chart)
            explanation = _build_explanation(ev, dasha_at, transit_at, chart)

            event_matches.append({
                "event": ev_type,
                "date": ev_date,
                "score": ev_score,
                "explanation": explanation,
                "dasha": f"{dasha_at['mahadasha']}/{dasha_at['antardasha']}",
            })
            total_score += ev_score

        # Average score across events
        avg_score = total_score / len(life_events) if life_events else 0.0

        candidates.append({
            "birth_time": candidate_time,
            "score": round(avg_score, 1),
            "lagna": asc_sign,
            "lagna_degree": round(asc_lon, 1),
            "nakshatra": birth_nakshatra,
            "event_matches": event_matches,
        })

        current_min += step_minutes

    # Sort by score descending
    candidates.sort(key=lambda c: c["score"], reverse=True)

    # Take top 5
    top_candidates = candidates[:5]

    # Determine confidence based on score gap
    if len(top_candidates) >= 2:
        gap = top_candidates[0]["score"] - top_candidates[1]["score"]
        if gap >= 15:
            confidence = "high"
        elif gap >= 5:
            confidence = "medium"
        else:
            confidence = "low"
    elif len(top_candidates) == 1:
        confidence = "medium"
    else:
        confidence = "low"

    best_time = top_candidates[0]["birth_time"] if top_candidates else None
    best_score = top_candidates[0]["score"] if top_candidates else 0

    # Build summary
    summary_parts = []
    if best_time:
        summary_parts.append(
            f"Best candidate birth time: {best_time} "
            f"(Lagna: {top_candidates[0]['lagna']}) "
            f"with score {best_score}/100."
        )
    summary_parts.append(
        f"Analyzed {len(candidates)} candidate times "
        f"with {len(life_events)} life events."
    )
    summary_parts.append(f"Confidence: {confidence}.")

    if confidence == "low" and len(top_candidates) >= 2:
        summary_parts.append(
            "Multiple birth times score similarly. "
            "Adding more life events may improve accuracy."
        )

    return {
        "candidates": top_candidates,
        "best_time": best_time,
        "confidence": confidence,
        "analysis_summary": " ".join(summary_parts),
    }
