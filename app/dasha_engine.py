"""
dasha_engine.py — Vimshottari Dasha Calculation Engine
=======================================================
Computes Mahadasha, Antardasha, and Pratyantar Dasha periods based on
birth nakshatra. Vimshottari total = 120 years. Order starts from birth
nakshatra lord.
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


def _build_pratyantar_periods(
    antardasha_planet: str,
    antardasha_duration_days: float,
    antardasha_start: datetime,
    now: datetime,
) -> list:
    """Build Pratyantar Dasha periods within an Antardasha."""
    pratyantar_seq = _get_dasha_sequence(antardasha_planet)
    pratyantar_periods = []
    p_start = antardasha_start

    for p_planet in pratyantar_seq:
        p_years = DASHA_YEARS[p_planet]
        # Pratyantar duration = (antardasha_duration_days * p_years / 120)
        p_duration_days = (antardasha_duration_days * p_years) / VIMSHOTTARI_TOTAL
        p_end = p_start + timedelta(days=p_duration_days)

        is_current = (p_start <= now <= p_end)

        pratyantar_periods.append({
            "planet": p_planet,
            "start": p_start.strftime("%Y-%m-%d"),
            "end": p_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        p_start = p_end

    return pratyantar_periods


def _build_antardasha_periods(
    mahadasha_planet: str,
    mahadasha_years: int,
    mahadasha_start: datetime,
    now: datetime,
) -> list:
    """Build Antardasha periods (with nested Pratyantar) within a Mahadasha."""
    antardasha_seq = _get_dasha_sequence(mahadasha_planet)
    antardasha_periods = []
    ad_start = mahadasha_start

    for ad_planet in antardasha_seq:
        ad_years = DASHA_YEARS[ad_planet]
        # Antardasha duration = (mahadasha_years * ad_years / 120) years in days
        ad_duration_days = (mahadasha_years * ad_years / VIMSHOTTARI_TOTAL) * 365.25
        ad_end = ad_start + timedelta(days=ad_duration_days)

        is_current = (ad_start <= now <= ad_end)

        # Build pratyantar only for current antardasha to keep payload reasonable
        pratyantar = []
        if is_current:
            pratyantar = _build_pratyantar_periods(
                ad_planet, ad_duration_days, ad_start, now
            )

        antardasha_periods.append({
            "planet": ad_planet,
            "start": ad_start.strftime("%Y-%m-%d"),
            "end": ad_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
            "pratyantar": pratyantar,
        })
        ad_start = ad_end

    return antardasha_periods


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


def calculate_extended_dasha(birth_nakshatra: str, birth_date: str) -> dict:
    """
    Calculate extended Vimshottari Dasha with Mahadasha -> Antardasha -> Pratyantar.

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini", "Rohini")
        birth_date: Birth date as "YYYY-MM-DD"

    Returns:
        {
            mahadasha: [{planet, start, end, is_current, antardasha: [{...}]}],
            current_dasha: str,
            current_antardasha: str,
            current_pratyantar: str,
        }
    """
    if birth_nakshatra not in NAKSHATRA_LORD:
        return {
            "mahadasha": [],
            "current_dasha": "Unknown",
            "current_antardasha": "Unknown",
            "current_pratyantar": "Unknown",
            "error": f"Unknown nakshatra: {birth_nakshatra}",
        }

    starting_lord = NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date)
    now = datetime.now()

    mahadasha_list = []
    current_start = birth_dt
    current_dasha = "Unknown"
    current_antardasha = "Unknown"
    current_pratyantar = "Unknown"

    for planet in sequence:
        years = DASHA_YEARS[planet]
        end_dt = current_start + timedelta(days=years * 365.25)
        is_current = (current_start <= now <= end_dt)

        if is_current:
            current_dasha = planet

        # Build antardasha for every mahadasha (but pratyantar only for current)
        antardasha = _build_antardasha_periods(
            planet, years, current_start, now
        )

        # Find current antardasha and pratyantar
        if is_current:
            for ad in antardasha:
                if ad["is_current"]:
                    current_antardasha = ad["planet"]
                    for pt in ad.get("pratyantar", []):
                        if pt["is_current"]:
                            current_pratyantar = pt["planet"]
                            break
                    break

        mahadasha_list.append({
            "planet": planet,
            "start": current_start.strftime("%Y-%m-%d"),
            "end": end_dt.strftime("%Y-%m-%d"),
            "years": years,
            "is_current": is_current,
            "antardasha": antardasha,
        })
        current_start = end_dt

    return {
        "mahadasha": mahadasha_list,
        "current_dasha": current_dasha,
        "current_antardasha": current_antardasha,
        "current_pratyantar": current_pratyantar,
    }
