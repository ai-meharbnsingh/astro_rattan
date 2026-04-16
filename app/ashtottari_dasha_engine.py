"""
ashtottari_dasha_engine.py — Ashtottari Dasha Calculation Engine
=================================================================
Computes Mahadasha, Antardasha, and Pratyantardasha periods based on
the Ashtottari (108-year) Dasha system.

Uses 8 planets (no Ketu): Sun, Moon, Mars, Mercury, Saturn, Jupiter, Rahu, Venus.
Total cycle = 108 years.

Applicable only when Moon's birth nakshatra falls within the 22 nakshatras
of the Ashtottari scheme (Ardra through Revati, skipping 5 nakshatras).

The starting planet is determined by the Moon's birth nakshatra.
Balance of the first dasha is computed from the Moon's position within
the nakshatra at birth.
"""
from datetime import datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

ASHTOTTARI_TOTAL = 108  # years

# Planet -> years in Ashtottari Dasha system (total = 108)
ASHTOTTARI_YEARS = {
    "Sun": 6,
    "Moon": 15,
    "Mars": 8,
    "Mercury": 17,
    "Saturn": 10,
    "Jupiter": 19,
    "Rahu": 12,
    "Venus": 21,
}

# Fixed cyclic order of Ashtottari Dasha
ASHTOTTARI_ORDER = [
    "Sun", "Moon", "Mars", "Mercury",
    "Saturn", "Jupiter", "Rahu", "Venus",
]

# 27 Nakshatras in standard order
NAKSHATRA_ORDER = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

# The 22 nakshatras applicable to Ashtottari system, mapped to their ruling planet.
# Starts from Ardra (6th nakshatra). Every nakshatra except Ashwini, Bharani,
# Krittika, Rohini, Mrigashira is included.
ASHTOTTARI_NAKSHATRA_LORD = {
    "Ardra": "Sun",
    "Punarvasu": "Sun",
    "Pushya": "Sun",
    "Ashlesha": "Moon",
    "Magha": "Moon",
    "Purva Phalguni": "Moon",
    "Uttara Phalguni": "Mars",
    "Hasta": "Mars",
    "Chitra": "Mars",
    "Swati": "Mercury",
    "Vishakha": "Mercury",
    "Anuradha": "Mercury",
    "Jyeshtha": "Saturn",
    "Mula": "Saturn",
    "Purva Ashadha": "Saturn",
    "Uttara Ashadha": "Jupiter",
    "Shravana": "Jupiter",
    "Dhanishta": "Jupiter",
    "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Rahu",
    "Uttara Bhadrapada": "Rahu",
    "Revati": "Venus",
}

# Each planet rules 3 nakshatras in the Ashtottari scheme, except Venus which
# rules only 1 (Revati). The starting point within the planet's nakshatra group
# determines the dasha balance at birth.
# Nakshatra groups per planet, in order:
ASHTOTTARI_PLANET_NAKSHATRAS = {
    "Sun": ["Ardra", "Punarvasu", "Pushya"],
    "Moon": ["Ashlesha", "Magha", "Purva Phalguni"],
    "Mars": ["Uttara Phalguni", "Hasta", "Chitra"],
    "Mercury": ["Swati", "Vishakha", "Anuradha"],
    "Saturn": ["Jyeshtha", "Mula", "Purva Ashadha"],
    "Jupiter": ["Uttara Ashadha", "Shravana", "Dhanishta"],
    "Rahu": ["Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada"],
    "Venus": ["Revati"],
}

NAKSHATRA_SPAN = 13 + 20.0 / 60.0  # 13 degrees 20 minutes = 13.3333 degrees


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _get_dasha_sequence(starting_lord: str) -> list:
    """Return the 8-planet dasha sequence starting from a given lord."""
    start_idx = ASHTOTTARI_ORDER.index(starting_lord)
    return ASHTOTTARI_ORDER[start_idx:] + ASHTOTTARI_ORDER[:start_idx]


def _calculate_balance(birth_nakshatra: str, moon_longitude: float = None) -> float:
    """
    Calculate the balance (remaining fraction) of the first Mahadasha at birth.

    For Ashtottari, each planet rules a group of nakshatras. The balance depends
    on how far through the planet's group the Moon has traversed.

    Args:
        birth_nakshatra: Name of Moon's birth nakshatra
        moon_longitude: Moon's sidereal longitude in degrees (0-360).
                       If None, returns 1.0 (full balance).

    Returns:
        Float between 0.0 and 1.0 representing the remaining fraction.
    """
    if moon_longitude is None:
        return 1.0

    moon_longitude = moon_longitude % 360.0

    lord = ASHTOTTARI_NAKSHATRA_LORD.get(birth_nakshatra)
    if lord is None:
        return 1.0

    group = ASHTOTTARI_PLANET_NAKSHATRAS[lord]
    group_span = len(group) * NAKSHATRA_SPAN  # total degrees this lord covers

    # Find start longitude of the first nakshatra in this lord's group
    first_nak = group[0]
    first_nak_idx = NAKSHATRA_ORDER.index(first_nak)
    group_start_longitude = first_nak_idx * NAKSHATRA_SPAN

    # How far Moon has traversed through this lord's group
    traversed = moon_longitude - group_start_longitude
    if traversed < 0:
        traversed += 360.0
    if traversed > group_span:
        traversed = group_span

    remaining_fraction = (group_span - traversed) / group_span
    return max(0.0, min(1.0, remaining_fraction))


def _parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _build_pratyantar_periods(
    antardasha_planet: str,
    antardasha_duration_days: float,
    antardasha_start: datetime,
    now: datetime,
) -> list:
    """Build Pratyantardasha periods within an Antardasha."""
    pratyantar_seq = _get_dasha_sequence(antardasha_planet)
    pratyantar_periods = []
    p_start = antardasha_start

    for p_planet in pratyantar_seq:
        p_years = ASHTOTTARI_YEARS[p_planet]
        p_duration_days = (antardasha_duration_days * p_years) / ASHTOTTARI_TOTAL
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
    mahadasha_years: float,
    mahadasha_start: datetime,
    now: datetime,
) -> list:
    """Build Antardasha periods (with nested Pratyantardasha) within a Mahadasha."""
    antardasha_seq = _get_dasha_sequence(mahadasha_planet)
    antardasha_periods = []
    ad_start = mahadasha_start

    for ad_planet in antardasha_seq:
        ad_years = ASHTOTTARI_YEARS[ad_planet]
        ad_duration_days = (mahadasha_years * ad_years / ASHTOTTARI_TOTAL) * 365.25
        ad_end = ad_start + timedelta(days=ad_duration_days)

        is_current = (ad_start <= now <= ad_end)

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


# ============================================================
# PUBLIC API
# ============================================================

def calculate_ashtottari_dasha(
    birth_nakshatra: str,
    birth_date: str,
    moon_longitude: float = None,
) -> dict:
    """
    Calculate Ashtottari Dasha periods from birth nakshatra and birth date.

    The Ashtottari Dasha uses 8 planets (no Ketu) with a total cycle of 108 years.
    It is applicable only when the birth nakshatra falls within the 22 nakshatras
    of the Ashtottari scheme.

    Args:
        birth_nakshatra: One of the 22 applicable nakshatras (Ardra through Revati)
        birth_date: Birth date as "YYYY-MM-DD"
        moon_longitude: Moon's sidereal longitude in degrees (0-360).
                       If None, full first dasha is used.

    Returns:
        {
            mahadasha: [{planet, start, end, years, is_current, antardasha: [...]}],
            current_dasha: str,
            current_antardasha: str,
            current_pratyantar: str,
            applicable: bool,
        }
    """
    # Check if nakshatra is in the Ashtottari scheme
    if birth_nakshatra not in ASHTOTTARI_NAKSHATRA_LORD:
        return {
            "mahadasha": [],
            "current_dasha": "N/A",
            "current_antardasha": "N/A",
            "current_pratyantar": "N/A",
            "applicable": False,
            "error": (
                f"Nakshatra '{birth_nakshatra}' is not in the Ashtottari scheme. "
                "Ashtottari applies to: Ardra through Revati (22 nakshatras)."
            ),
        }

    starting_lord = ASHTOTTARI_NAKSHATRA_LORD[birth_nakshatra]
    sequence = _get_dasha_sequence(starting_lord)
    birth_dt = _parse_date(birth_date)
    now = datetime.now(tz=None)

    balance = _calculate_balance(birth_nakshatra, moon_longitude)

    mahadasha_list = []
    current_start = birth_dt
    current_dasha = "Unknown"
    current_antardasha = "Unknown"
    current_pratyantar = "Unknown"

    def _append_mahadasha(planet, effective_years, start):
        nonlocal current_dasha, current_antardasha, current_pratyantar
        end_dt = start + timedelta(days=effective_years * 365.25)
        is_current = (start <= now <= end_dt)

        if is_current:
            current_dasha = planet

        antardasha = _build_antardasha_periods(planet, effective_years, start, now)

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
            "start": start.strftime("%Y-%m-%d"),
            "end": end_dt.strftime("%Y-%m-%d"),
            "years": round(effective_years, 4),
            "is_current": is_current,
            "antardasha": antardasha,
        })
        return end_dt

    # First cycle (8 periods, first one gets balance)
    for i, planet in enumerate(sequence):
        full_years = ASHTOTTARI_YEARS[planet]
        effective_years = full_years * balance if i == 0 else full_years
        current_start = _append_mahadasha(planet, effective_years, current_start)

    # Extend with additional cycles until we cover at least 216 years (2 full cycles)
    min_coverage = birth_dt + timedelta(days=216 * 365.25)
    while current_start < min_coverage:
        for planet in sequence:
            full_years = ASHTOTTARI_YEARS[planet]
            current_start = _append_mahadasha(planet, full_years, current_start)

    return {
        "mahadasha": mahadasha_list,
        "current_dasha": current_dasha,
        "current_antardasha": current_antardasha,
        "current_pratyantar": current_pratyantar,
        "applicable": True,
    }
