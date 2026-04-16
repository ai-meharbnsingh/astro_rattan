"""
tara_dasha_engine.py — Tara Dasha Calculation Engine
=====================================================
Computes Tara Dasha periods based on the birth nakshatra.

Tara Dasha divides the 27 nakshatras into 9 Tara groups of 3 nakshatras
each, cycling from the birth nakshatra. Each Tara group has a specific
nature (Janma, Sampat, Vipat, etc.) and is assigned years matching the
Vimshottari dasha lords for the corresponding group.

The 9 Tara groups:
  1. Janma (Birth)       — Ketu lord    — 7 years
  2. Sampat (Wealth)     — Venus lord   — 20 years
  3. Vipat (Danger)      — Sun lord     — 6 years
  4. Kshema (Well-being) — Moon lord    — 10 years
  5. Pratyari (Obstacle) — Mars lord    — 7 years
  6. Sadhaka (Success)   — Rahu lord    — 18 years
  7. Vadha (Death)       — Jupiter lord — 16 years
  8. Mitra (Friend)      — Saturn lord  — 19 years
  9. Ati-Mitra (Great Friend) — Mercury lord — 17 years

Total = 120 years (same as Vimshottari).

Balance of the first dasha is computed from the Moon's position within
the birth nakshatra.
"""
from datetime import datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

TARA_TOTAL = 120  # years (same as Vimshottari)

# 27 Nakshatras in standard order
NAKSHATRA_ORDER = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_INDEX = {name: i for i, name in enumerate(NAKSHATRA_ORDER)}

# 9 Tara groups with their names, Vimshottari lord, and period years
TARA_GROUPS = [
    {"name": "Janma", "lord": "Ketu", "years": 7},
    {"name": "Sampat", "lord": "Venus", "years": 20},
    {"name": "Vipat", "lord": "Sun", "years": 6},
    {"name": "Kshema", "lord": "Moon", "years": 10},
    {"name": "Pratyari", "lord": "Mars", "years": 7},
    {"name": "Sadhaka", "lord": "Rahu", "years": 18},
    {"name": "Vadha", "lord": "Jupiter", "years": 16},
    {"name": "Mitra", "lord": "Saturn", "years": 19},
    {"name": "Ati-Mitra", "lord": "Mercury", "years": 17},
]

NAKSHATRA_SPAN = 13 + 20.0 / 60.0  # 13 degrees 20 minutes = 13.3333 degrees


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _calculate_balance(birth_nakshatra: str, moon_longitude: float = None) -> float:
    """
    Calculate the balance (remaining fraction) of the first Tara dasha at birth.

    Depends on how far the Moon has traversed through its birth nakshatra.

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

    nak_index = NAKSHATRA_INDEX.get(birth_nakshatra)
    if nak_index is None:
        return 1.0

    nak_start = nak_index * NAKSHATRA_SPAN

    traversed = moon_longitude - nak_start
    if traversed < 0:
        traversed += 360.0
    if traversed > NAKSHATRA_SPAN:
        traversed = NAKSHATRA_SPAN

    remaining_fraction = (NAKSHATRA_SPAN - traversed) / NAKSHATRA_SPAN
    return max(0.0, min(1.0, remaining_fraction))


def _build_tara_nakshatras(birth_nakshatra: str) -> list:
    """
    Build the 9 Tara groups starting from the birth nakshatra.

    Each group contains 3 consecutive nakshatras (cycling through 27).
    Group 1 starts with the birth nakshatra itself.

    Args:
        birth_nakshatra: Name of Moon's birth nakshatra

    Returns:
        List of 9 dicts, each with:
          - name: Tara group name
          - lord: Vimshottari lord
          - years: Period years
          - nakshatras: list of 3 nakshatra names in this group
    """
    start_idx = NAKSHATRA_INDEX[birth_nakshatra]
    groups = []

    for i, tara in enumerate(TARA_GROUPS):
        naks = []
        for j in range(3):
            nak_idx = (start_idx + i * 3 + j) % 27
            naks.append(NAKSHATRA_ORDER[nak_idx])
        groups.append({
            "name": tara["name"],
            "lord": tara["lord"],
            "years": tara["years"],
            "nakshatras": naks,
        })

    return groups


def _build_sub_periods(
    tara_group: dict,
    main_duration_days: float,
    main_start: datetime,
    now: datetime,
    all_groups: list,
) -> list:
    """
    Build sub-periods (antardasha equivalent) within a Tara main period.

    Sub-periods follow the same 9 Tara groups in order, starting from the
    main period's group. Duration is proportional to each sub-group's years.

    Args:
        tara_group: The main period's Tara group dict
        main_duration_days: Duration of the main period in days
        main_start: Start datetime
        now: Current datetime
        all_groups: All 9 Tara groups

    Returns:
        List of sub-period dicts
    """
    # Find starting index in the all_groups list
    main_idx = next(
        i for i, g in enumerate(all_groups) if g["name"] == tara_group["name"]
    )

    sub_periods = []
    s_start = main_start

    for i in range(9):
        sub_group = all_groups[(main_idx + i) % 9]
        sub_years = sub_group["years"]
        s_duration_days = (main_duration_days * sub_years) / TARA_TOTAL
        s_end = s_start + timedelta(days=s_duration_days)

        is_current = (s_start <= now <= s_end)

        sub_periods.append({
            "tara": sub_group["name"],
            "lord": sub_group["lord"],
            "start": s_start.strftime("%Y-%m-%d"),
            "end": s_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        s_start = s_end

    return sub_periods


# ============================================================
# PUBLIC API
# ============================================================

def calculate_tara_dasha(
    birth_nakshatra: str,
    birth_date: str,
    moon_longitude: float = None,
) -> dict:
    """
    Calculate Tara Dasha periods from birth nakshatra and birth date.

    The Tara Dasha divides 27 nakshatras into 9 groups of 3, cycling from
    the birth nakshatra. Each group is assigned years matching Vimshottari
    lords (total = 120 years). Sub-periods follow the same 9-group cycle.

    Args:
        birth_nakshatra: One of 27 nakshatras (e.g. "Ashwini", "Rohini")
        birth_date: Birth date as "YYYY-MM-DD"
        moon_longitude: Moon's sidereal longitude in degrees (0-360).
                       If None, full first dasha is used.

    Returns:
        {
            mahadasha: [{tara, lord, nakshatras, start, end, years, is_current,
                         sub_periods: [...]}],
            tara_groups: [{name, lord, years, nakshatras}],
            current_dasha: str,
            current_sub_period: str,
        }
    """
    if birth_nakshatra not in NAKSHATRA_INDEX:
        return {
            "mahadasha": [],
            "tara_groups": [],
            "current_dasha": "Unknown",
            "current_sub_period": "Unknown",
            "error": f"Unknown nakshatra: {birth_nakshatra}",
        }

    tara_groups = _build_tara_nakshatras(birth_nakshatra)
    birth_dt = _parse_date(birth_date)
    now = datetime.now(tz=None)

    balance = _calculate_balance(birth_nakshatra, moon_longitude)

    mahadasha_list = []
    current_start = birth_dt
    current_dasha = "Unknown"
    current_sub_period = "Unknown"

    # Build 2 full cycles to cover at least 240 years
    for cycle in range(2):
        for i, group in enumerate(tara_groups):
            full_years = group["years"]

            if cycle == 0 and i == 0:
                effective_years = full_years * balance
            else:
                effective_years = full_years

            duration_days = effective_years * 365.25
            end_dt = current_start + timedelta(days=duration_days)

            is_current = (current_start <= now <= end_dt)

            if is_current:
                current_dasha = group["name"]

            sub_periods = _build_sub_periods(
                group, duration_days, current_start, now, tara_groups
            )

            if is_current:
                for sp in sub_periods:
                    if sp["is_current"]:
                        current_sub_period = sp["tara"]
                        break

            mahadasha_list.append({
                "tara": group["name"],
                "lord": group["lord"],
                "nakshatras": group["nakshatras"],
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "years": round(effective_years, 4),
                "is_current": is_current,
                "sub_periods": sub_periods,
            })
            current_start = end_dt

    return {
        "mahadasha": mahadasha_list,
        "tara_groups": tara_groups,
        "current_dasha": current_dasha,
        "current_sub_period": current_sub_period,
    }
