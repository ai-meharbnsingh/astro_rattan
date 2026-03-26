"""
dasha_engine.py — Vimshottari Dasha Calculation Engine
=======================================================
Computes Mahadasha and Antardasha periods based on birth nakshatra.
Vimshottari total = 120 years. Order starts from birth nakshatra lord.
"""
from datetime import datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

# Planet -> years in Vimshottari Dasha system (total = 120)
DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# Fixed cyclic order of Vimshottari Dasha
DASHA_ORDER = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury",
]

# 27 Nakshatras mapped to their ruling planet
NAKSHATRA_LORD = {
    "Ashwini": "Ketu",
    "Bharani": "Venus",
    "Krittika": "Sun",
    "Rohini": "Moon",
    "Mrigashira": "Mars",
    "Ardra": "Rahu",
    "Punarvasu": "Jupiter",
    "Pushya": "Saturn",
    "Ashlesha": "Mercury",
    "Magha": "Ketu",
    "Purva Phalguni": "Venus",
    "Uttara Phalguni": "Sun",
    "Hasta": "Moon",
    "Chitra": "Mars",
    "Swati": "Rahu",
    "Vishakha": "Jupiter",
    "Anuradha": "Saturn",
    "Jyeshtha": "Mercury",
    "Mula": "Ketu",
    "Purva Ashadha": "Venus",
    "Uttara Ashadha": "Sun",
    "Shravana": "Moon",
    "Dhanishta": "Mars",
    "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter",
    "Uttara Bhadrapada": "Saturn",
    "Revati": "Mercury",
}

VIMSHOTTARI_TOTAL = 120  # years


def _get_dasha_sequence(starting_lord: str) -> list:
    """Return the 9-planet dasha sequence starting from a given lord."""
    start_idx = DASHA_ORDER.index(starting_lord)
    return DASHA_ORDER[start_idx:] + DASHA_ORDER[:start_idx]


def _parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def calculate_dasha(birth_nakshatra: str, birth_date: str) -> dict:
    """
    Calculate Vimshottari Dasha periods from birth nakshatra and birth date.

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini", "Rohini")
        birth_date: Birth date as "YYYY-MM-DD"

    Returns:
        {
            mahadasha_periods: [{planet, start_date, end_date, years}],
            current_dasha: str,
            current_antardasha: str,
        }
    """
    if birth_nakshatra not in NAKSHATRA_LORD:
        return {
            "mahadasha_periods": [],
            "current_dasha": "Unknown",
            "current_antardasha": "Unknown",
            "error": f"Unknown nakshatra: {birth_nakshatra}",
        }

    starting_lord = NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date)
    now = datetime.now()

    # Build mahadasha periods
    mahadasha_periods = []
    current_start = birth_dt

    for planet in sequence:
        years = DASHA_YEARS[planet]
        end_dt = current_start + timedelta(days=years * 365.25)
        mahadasha_periods.append({
            "planet": planet,
            "start_date": current_start.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "years": years,
        })
        current_start = end_dt

    # Determine current mahadasha
    current_dasha = "Unknown"
    current_dasha_start = None
    current_dasha_years = 0
    for period in mahadasha_periods:
        start_dt = _parse_date(period["start_date"])
        end_dt = _parse_date(period["end_date"])
        if start_dt <= now <= end_dt:
            current_dasha = period["planet"]
            current_dasha_start = start_dt
            current_dasha_years = period["years"]
            break

    # If now is beyond all periods (past 120 years), cycle back
    if current_dasha == "Unknown" and now > _parse_date(mahadasha_periods[-1]["end_date"]):
        current_dasha = mahadasha_periods[-1]["planet"]
        current_dasha_start = _parse_date(mahadasha_periods[-1]["start_date"])
        current_dasha_years = mahadasha_periods[-1]["years"]

    # Determine current antardasha within the mahadasha
    current_antardasha = "Unknown"
    if current_dasha != "Unknown" and current_dasha_start is not None:
        antardasha_seq = _get_dasha_sequence(current_dasha)
        antardasha_start = current_dasha_start
        mahadasha_total_days = current_dasha_years * 365.25

        for sub_planet in antardasha_seq:
            # Antardasha duration = (mahadasha_years * sub_planet_years / 120) years
            sub_years = DASHA_YEARS[sub_planet]
            sub_duration_days = (current_dasha_years * sub_years / VIMSHOTTARI_TOTAL) * 365.25
            sub_end = antardasha_start + timedelta(days=sub_duration_days)

            if antardasha_start <= now <= sub_end:
                current_antardasha = sub_planet
                break
            antardasha_start = sub_end

    return {
        "mahadasha_periods": mahadasha_periods,
        "current_dasha": current_dasha,
        "current_antardasha": current_antardasha,
    }
