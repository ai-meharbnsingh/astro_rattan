"""
moola_dasha_engine.py — Moola (Jaimini) Dasha Calculation Engine
================================================================
Computes Moola Dasha periods based on Jaimini's Rashi (sign-based) system.

Unlike nakshatra-based dashas, Moola Dasha uses zodiac signs as periods.
The starting sign is determined by the stronger between Lagna (ascendant)
and the 7th house. Direction of counting (zodiac or reverse) depends on
the nature of the sign (odd/even).

Each sign has a fixed base period in years. The actual period may be
modified based on the sign's lord position (odd/even sign placement).
"""
from datetime import datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

# Zodiac signs in order (1-indexed conceptually, 0-indexed in list)
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_INDEX = {name: i for i, name in enumerate(SIGNS)}

# Base period years for each sign in Moola Dasha
# Odd signs: Aries=8, Gemini=10, Leo=12, Libra=2, Sagittarius=4, Aquarius=6
# Even signs: Taurus=9, Cancer=11, Virgo=1, Scorpio=3, Capricorn=5, Pisces=7
MOOLA_BASE_YEARS = {
    "Aries": 8,
    "Taurus": 9,
    "Gemini": 10,
    "Cancer": 11,
    "Leo": 12,
    "Virgo": 1,
    "Libra": 2,
    "Scorpio": 3,
    "Sagittarius": 4,
    "Capricorn": 5,
    "Aquarius": 6,
    "Pisces": 7,
}

# Sign lords (traditional Jaimini/Parashari rulership)
SIGN_LORDS = {
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

# Odd signs (fire and air): Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
# Even signs (earth and water): Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces
EVEN_SIGNS = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _is_odd_sign(sign: str) -> bool:
    """Return True if the sign is odd (masculine)."""
    return sign in ODD_SIGNS


def _sign_strength(sign: str, planet_positions: dict) -> int:
    """
    Calculate the strength of a sign for determining the starting sign.

    Strength is computed based on:
    1. Number of planets in the sign (more planets = stronger)
    2. Whether the lord of the sign is in a kendra (1, 4, 7, 10 from the sign)
    3. Whether the sign has its own lord placed in it

    Args:
        sign: Zodiac sign name
        planet_positions: dict mapping planet names to their sign names
            e.g. {"Sun": "Aries", "Moon": "Taurus", ...}

    Returns:
        Integer strength score (higher = stronger)
    """
    strength = 0

    # Count planets in this sign
    for planet, p_sign in planet_positions.items():
        if p_sign == sign:
            strength += 1

    # Bonus if lord is in the sign itself
    lord = SIGN_LORDS[sign]
    lord_sign = planet_positions.get(lord)
    if lord_sign == sign:
        strength += 2

    # Bonus if lord is in a kendra from the sign
    if lord_sign and lord_sign in SIGNS:
        sign_idx = SIGN_INDEX[sign]
        lord_idx = SIGN_INDEX[lord_sign]
        distance = (lord_idx - sign_idx) % 12
        if distance in (0, 3, 6, 9):  # kendras (1st, 4th, 7th, 10th houses)
            strength += 1

    return strength


def _get_dasha_sign_sequence(starting_sign: str) -> list:
    """
    Get the 12-sign sequence for Moola Dasha starting from the given sign.

    For odd signs: count in zodiacal order (forward)
    For even signs: count in reverse zodiacal order (backward)

    Args:
        starting_sign: The sign to start from

    Returns:
        List of 12 sign names in dasha order
    """
    start_idx = SIGN_INDEX[starting_sign]

    if _is_odd_sign(starting_sign):
        # Forward counting
        return [SIGNS[(start_idx + i) % 12] for i in range(12)]
    else:
        # Reverse counting
        return [SIGNS[(start_idx - i) % 12] for i in range(12)]


def _get_effective_years(sign: str) -> int:
    """
    Get effective dasha years for a sign.

    In Moola Dasha, the base years may be modified. The standard approach
    uses the base years directly. Some variants adjust based on the lord's
    position, but we use the classical base years here.

    Args:
        sign: Zodiac sign name

    Returns:
        Years for this sign's dasha period
    """
    return MOOLA_BASE_YEARS[sign]


def _build_sub_periods(
    main_sign: str,
    main_duration_days: float,
    main_start: datetime,
    now: datetime,
    planet_positions: dict,
) -> list:
    """
    Build sub-periods (antardasha equivalent) within a main sign period.

    Sub-periods follow the same sign sequence as the main dasha, starting
    from the main sign itself.

    Args:
        main_sign: The main dasha sign
        main_duration_days: Duration of the main period in days
        main_start: Start datetime of the main period
        now: Current datetime
        planet_positions: Planet positions dict

    Returns:
        List of sub-period dicts
    """
    sub_sequence = _get_dasha_sign_sequence(main_sign)
    total_sub_years = sum(MOOLA_BASE_YEARS[s] for s in sub_sequence)

    sub_periods = []
    s_start = main_start

    for sub_sign in sub_sequence:
        sub_base_years = MOOLA_BASE_YEARS[sub_sign]
        # Sub-period duration is proportional to base years
        s_duration_days = (main_duration_days * sub_base_years) / total_sub_years
        s_end = s_start + timedelta(days=s_duration_days)

        is_current = (s_start <= now <= s_end)

        sub_periods.append({
            "sign": sub_sign,
            "start": s_start.strftime("%Y-%m-%d"),
            "end": s_end.strftime("%Y-%m-%d"),
            "is_current": is_current,
        })
        s_start = s_end

    return sub_periods


# ============================================================
# PUBLIC API
# ============================================================

def calculate_moola_dasha(
    lagna_sign: str,
    seventh_sign: str,
    planet_positions: dict,
    birth_date: str,
) -> dict:
    """
    Calculate Moola (Jaimini) Dasha periods.

    The starting sign is determined by comparing the strength of the Lagna
    and the 7th house. The stronger one starts. Direction of sign sequence
    depends on whether the starting sign is odd (forward) or even (reverse).

    Args:
        lagna_sign: Ascendant sign name (e.g. "Aries", "Taurus")
        seventh_sign: 7th house sign name
        planet_positions: dict mapping planet names to their sign names
            e.g. {"Sun": "Aries", "Moon": "Cancer", "Mars": "Leo", ...}
        birth_date: Birth date as "YYYY-MM-DD"

    Returns:
        {
            mahadasha: [{sign, start, end, years, is_current, sub_periods: [...]}],
            current_dasha: str,
            current_sub_period: str,
            starting_sign: str,
            direction: "forward" | "reverse",
        }
    """
    if lagna_sign not in SIGN_INDEX:
        return {
            "mahadasha": [],
            "current_dasha": "Unknown",
            "current_sub_period": "Unknown",
            "starting_sign": "Unknown",
            "direction": "Unknown",
            "error": f"Unknown lagna sign: {lagna_sign}",
        }

    if seventh_sign not in SIGN_INDEX:
        return {
            "mahadasha": [],
            "current_dasha": "Unknown",
            "current_sub_period": "Unknown",
            "starting_sign": "Unknown",
            "direction": "Unknown",
            "error": f"Unknown seventh sign: {seventh_sign}",
        }

    # Determine starting sign based on strength
    lagna_strength = _sign_strength(lagna_sign, planet_positions)
    seventh_strength = _sign_strength(seventh_sign, planet_positions)

    if lagna_strength >= seventh_strength:
        starting_sign = lagna_sign
    else:
        starting_sign = seventh_sign

    direction = "forward" if _is_odd_sign(starting_sign) else "reverse"
    sign_sequence = _get_dasha_sign_sequence(starting_sign)

    birth_dt = _parse_date(birth_date)
    now = datetime.now(tz=None)

    mahadasha_list = []
    current_start = birth_dt
    current_dasha = "Unknown"
    current_sub_period = "Unknown"

    # Build 2 full cycles to cover sufficient time
    for cycle in range(2):
        for sign in sign_sequence:
            years = _get_effective_years(sign)
            duration_days = years * 365.25
            end_dt = current_start + timedelta(days=duration_days)

            is_current = (current_start <= now <= end_dt)

            if is_current:
                current_dasha = sign

            sub_periods = _build_sub_periods(
                sign, duration_days, current_start, now, planet_positions
            )

            if is_current:
                for sp in sub_periods:
                    if sp["is_current"]:
                        current_sub_period = sp["sign"]
                        break

            mahadasha_list.append({
                "sign": sign,
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "years": years,
                "is_current": is_current,
                "sub_periods": sub_periods,
            })
            current_start = end_dt

    return {
        "mahadasha": mahadasha_list,
        "current_dasha": current_dasha,
        "current_sub_period": current_sub_period,
        "starting_sign": starting_sign,
        "direction": direction,
    }
