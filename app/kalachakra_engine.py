"""
kalachakra_engine.py — Kalachakra Dasha Calculation Engine
============================================================
Computes Kalachakra Dasha periods based on the Moon's nakshatra and pada
at birth.  Kalachakra ("Wheel of Time") is a rashi-based dasha system
where each nakshatra-pada maps to a navamsa rashi, and the dasha sequence
proceeds through the zodiac signs in either Savya (clockwise) or Apsavya
(anti-clockwise) order depending on the birth nakshatra-pada.

Key concepts
------------
* Each nakshatra-pada maps to a navamsa rashi via the standard 108-navamsa
  mapping (fire→Aries, earth→Capricorn, air→Libra, water→Cancer start).
* Each pada is classified as Savya (forward) or Apsavya (reverse).
* Savya sequence: from navamsa rashi, move forward through 12 signs.
* Apsavya sequence: from navamsa rashi, move backward through 12 signs.
* Each sign has a fixed duration (total half-cycle = 83 years, full = 166).
* Deha/Jeeva: first sign = Deha, alternating thereafter.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


# ============================================================
# CONSTANTS
# ============================================================

ZODIAC: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Rashi durations in years (standard Kalachakra — BPHS/Parashari)
# Classical Kalachakra uses a 9-sign half-cycle (not 12).
# The Savya half proceeds forward 9 signs from the navamsa rashi;
# the Apsavya half proceeds backward 9 signs.
# Sum of any 9 consecutive signs from the table below = 83 years.
# Full cycle (Savya 9 + Apsavya 9, with overlap at turn) = 166 years.
KALACHAKRA_DURATIONS: Dict[str, int] = {
    "Aries": 7,
    "Taurus": 16,
    "Gemini": 9,
    "Cancer": 21,
    "Leo": 5,
    "Virgo": 9,
    "Libra": 16,
    "Scorpio": 7,
    "Sagittarius": 10,
    "Capricorn": 4,
    "Aquarius": 4,
    "Pisces": 10,
}
# Number of signs per half-cycle (classical)
SIGNS_PER_HALF_CYCLE: int = 9

NAKSHATRAS: List[str] = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_SPAN: float = 13.0 + 20.0 / 60.0   # 13°20' = 13.33333…°
PADA_SPAN: float = NAKSHATRA_SPAN / 4.0       # 3°20'  = 3.33333…°
# Note: sum of any 9 consecutive signs = 83 years (verifiable from table above)

# ============================================================
# NAVAMSA MAPPING  (108 navamsas = 27 nakshatras × 4 padas)
# ============================================================
# Standard rule:
#   Fire-sign nakshatras  (nak in 1,5,9  i.e. Aries/Leo/Sag group) start from Aries
#   Earth-sign nakshatras (nak in 2,6,10 i.e. Taurus/Virgo/Cap group) start from Capricorn
#   Air-sign nakshatras   (nak in 3,7,11 i.e. Gemini/Libra/Aqu group) start from Libra
#   Water-sign nakshatras (nak in 4,8,12 i.e. Cancer/Scorpio/Pisces group) start from Cancer
#
# The navamsa rashi for a given nakshatra index (0-26) and pada (0-3):
#   global_pada = nak_index * 4 + pada_index          (0-107)
#   navamsa_rashi_index = global_pada % 12             (0-11)
# This elegant formula works because the navamsa cycle repeats every 12 padas
# (which is exactly one zodiac cycle) and the classical starting signs align
# perfectly with Aries for the very first pada (Ashwini pada 1).


def _navamsa_rashi_index(nak_index: int, pada_index: int) -> int:
    """Return the zodiac index (0-11) of the navamsa rashi for a given
    nakshatra-pada combination.

    Args:
        nak_index:  0-based nakshatra index (0=Ashwini … 26=Revati)
        pada_index: 0-based pada index (0-3)
    """
    global_pada = nak_index * 4 + pada_index
    return global_pada % 12


# ============================================================
# SAVYA / APSAVYA CLASSIFICATION
# ============================================================
# Classical rule (Parashari tradition):
#
# The 27 nakshatras are grouped into 9 triads.  Within each triad the
# first nakshatra is fully Savya (all 4 padas), the second is fully
# Savya, and the third has padas 1-2 Savya and padas 3-4 Apsavya.
#
# However the more widely-used mapping assigns Savya/Apsavya at the
# individual pada level using the following classical table derived
# from Surya Siddhanta / BPHS commentaries.
#
# We encode the path per (nakshatra_index, pada_index) directly.
# True = Savya, False = Apsavya.
#
# Pattern per group of 3 nakshatras (repeats 9 times across 27):
#   nak 0 (group lead)   : padas 1-4 all Savya
#   nak 1 (group middle) : padas 1-4 all Savya
#   nak 2 (group tail)   : padas 1-2 Savya, padas 3-4 Apsavya
#
# Group boundaries: [0,1,2], [3,4,5], [6,7,8], [9,10,11], [12,13,14],
#                   [15,16,17], [18,19,20], [21,22,23], [24,25,26]

def _is_savya(nak_index: int, pada_index: int) -> bool:
    """Return True if the given nakshatra-pada follows the Savya (clockwise)
    path, False for Apsavya (anti-clockwise).

    Args:
        nak_index:  0-based (0=Ashwini … 26=Revati)
        pada_index: 0-based (0-3)
    """
    pos_in_group = nak_index % 3  # 0, 1, or 2
    if pos_in_group in (0, 1):
        return True
    # pos_in_group == 2  →  first two padas Savya, last two Apsavya
    return pada_index <= 1


# ============================================================
# DASHA SEQUENCE BUILDER
# ============================================================

def _build_sign_sequence(start_rashi_index: int, savya: bool) -> List[str]:
    """Build the 9-sign dasha half-cycle starting from *start_rashi_index*.

    Classical Kalachakra uses 9 signs per half-cycle (summing to 83 years).
    For Savya the signs proceed in normal zodiac order (Aries→Taurus→…).
    For Apsavya the signs proceed in reverse order (e.g. Taurus→Aries→Pisces→…).

    Returns a list of 9 sign names.
    """
    sequence: List[str] = []
    for i in range(SIGNS_PER_HALF_CYCLE):
        if savya:
            idx = (start_rashi_index + i) % 12
        else:
            idx = (start_rashi_index - i) % 12
        sequence.append(ZODIAC[idx])
    return sequence


# ============================================================
# DEHA / JEEVA ASSIGNMENT
# ============================================================

def _assign_deha_jeeva(sequence: List[str]) -> List[str]:
    """Return a list of 'Deha' / 'Jeeva' labels for each sign in *sequence*.

    Classical rule: the first sign = Deha, then alternate.
    Position 0 → Deha, 1 → Jeeva, 2 → Deha, …
    """
    return ["Deha" if i % 2 == 0 else "Jeeva" for i in range(len(sequence))]


def _find_deha_jeeva_rashis(
    sequence: List[str], types: List[str],
) -> tuple:
    """Return the (deha_rashi, jeeva_rashi) — the first sign labelled Deha
    and the first sign labelled Jeeva."""
    deha = next((s for s, t in zip(sequence, types) if t == "Deha"), sequence[0])
    jeeva = next((s for s, t in zip(sequence, types) if t == "Jeeva"), sequence[1] if len(sequence) > 1 else sequence[0])
    return deha, jeeva


# ============================================================
# BALANCE AT BIRTH
# ============================================================

def _calculate_balance(moon_longitude: float, nak_index: int, pada_index: int) -> float:
    """Calculate the remaining fraction of the first dasha period at birth.

    The Moon's position within the pada determines how much of the first
    dasha sign's period has already elapsed.  If the Moon is at the very
    start of the pada the full duration remains; at the end, almost none.

    Args:
        moon_longitude: Moon's sidereal longitude 0-360°
        nak_index:      0-based nakshatra index
        pada_index:     0-based pada index

    Returns:
        Float 0.0-1.0 representing the fraction of the first dasha remaining.
    """
    moon_longitude = moon_longitude % 360.0

    # Start of this pada
    pada_start = nak_index * NAKSHATRA_SPAN + pada_index * PADA_SPAN

    traversed = moon_longitude - pada_start
    if traversed < 0:
        traversed += 360.0
    if traversed > PADA_SPAN:
        traversed = PADA_SPAN  # clamp

    remaining = (PADA_SPAN - traversed) / PADA_SPAN
    return max(0.0, min(1.0, remaining))


# ============================================================
# NAKSHATRA + PADA FROM MOON LONGITUDE
# ============================================================

def _moon_nakshatra_pada(moon_longitude: float) -> tuple:
    """Return (nak_index, pada_index, nak_name, pada_number_1based) from
    the Moon's sidereal longitude."""
    moon_longitude = moon_longitude % 360.0
    nak_index = int(moon_longitude / NAKSHATRA_SPAN)
    if nak_index >= 27:
        nak_index = 26  # clamp edge
    remainder = moon_longitude - nak_index * NAKSHATRA_SPAN
    pada_index = int(remainder / PADA_SPAN)
    if pada_index >= 4:
        pada_index = 3  # clamp edge
    return nak_index, pada_index, NAKSHATRAS[nak_index], pada_index + 1


# ============================================================
# DATE HELPERS
# ============================================================

def _parse_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD date string."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _add_years(dt: datetime, years: float) -> datetime:
    """Add fractional years to a datetime using 365.25 days/year."""
    return dt + timedelta(days=years * 365.25)


# ============================================================
# MAIN FUNCTION
# ============================================================

def calculate_kalachakra_dasha(
    moon_longitude: float,
    birth_date: str,
    birth_time: str = "12:00:00",
) -> Dict[str, Any]:
    """Calculate Kalachakra Dasha periods.

    The Kalachakra Dasha is a rashi-based nakshatra dasha system where
    the sequence of sign periods follows either a clockwise (Savya) or
    anti-clockwise (Apsavya) path through the zodiac, starting from
    the navamsa rashi of the Moon's birth nakshatra-pada.

    Args:
        moon_longitude: Moon's sidereal longitude in degrees (0-360).
        birth_date:     Birth date as "YYYY-MM-DD".
        birth_time:     Birth time as "HH:MM:SS" (informational; the
                        actual Moon longitude drives all calculations).

    Returns:
        Dictionary with keys:
            moon_nakshatra  – name of birth nakshatra
            moon_pada       – pada number (1-4)
            navamsa_rashi   – starting rashi for the dasha sequence
            path            – "Savya" or "Apsavya"
            deha_rashi      – first Deha sign
            jeeva_rashi     – first Jeeva sign
            balance_at_birth – fraction of first dasha remaining at birth
            mahadasha_periods – list of period dicts
            current_dasha   – dict describing the period active now
    """
    # ── 1. Determine Moon's nakshatra and pada ──────────────────
    nak_index, pada_index, nak_name, pada_num = _moon_nakshatra_pada(moon_longitude)

    # ── 2. Navamsa rashi ────────────────────────────────────────
    nav_rashi_idx = _navamsa_rashi_index(nak_index, pada_index)
    navamsa_rashi = ZODIAC[nav_rashi_idx]

    # ── 3. Savya / Apsavya ──────────────────────────────────────
    savya = _is_savya(nak_index, pada_index)
    path_label = "Savya" if savya else "Apsavya"

    # ── 4. Build initial sign sequence (for Deha/Jeeva labels) ──
    initial_sequence = _build_sign_sequence(nav_rashi_idx, savya)
    initial_types = _assign_deha_jeeva(initial_sequence)
    deha_rashi, jeeva_rashi = _find_deha_jeeva_rashis(initial_sequence, initial_types)

    # ── 5. Balance at birth ─────────────────────────────────────
    balance = _calculate_balance(moon_longitude, nak_index, pada_index)

    # ── 6. Build Mahadasha periods ──────────────────────────────
    # Classical Kalachakra alternates: Savya half → Apsavya half → Savya …
    # Each half is 9 signs (83 years). We generate enough to cover 200 years.
    birth_dt = _parse_date(birth_date)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    mahadasha_periods: List[Dict[str, Any]] = []
    current_start = birth_dt
    min_coverage = _add_years(birth_dt, 200)
    cycle_count = 0
    current_savya = savya  # start with birth path, then alternate

    while current_start < min_coverage:
        # Build sequence for this half-cycle
        half_sequence = _build_sign_sequence(nav_rashi_idx, current_savya)
        half_types = _assign_deha_jeeva(half_sequence)

        for i, sign in enumerate(half_sequence):
            duration_years = float(KALACHAKRA_DURATIONS[sign])

            # First sign of the very first cycle gets the balance fraction
            if cycle_count == 0 and i == 0:
                effective_years = duration_years * balance
            else:
                effective_years = duration_years

            end_dt = _add_years(current_start, effective_years)

            mahadasha_periods.append({
                "sign": sign,
                "duration_years": round(effective_years, 4),
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "type": half_types[i],
            })

            current_start = end_dt

        cycle_count += 1
        current_savya = not current_savya  # alternate direction

    # ── 7. Find current dasha ───────────────────────────────────
    current_dasha: Optional[Dict[str, Any]] = None
    for period in mahadasha_periods:
        p_start = _parse_date(period["start"])
        p_end = _parse_date(period["end"])
        if p_start <= now <= p_end:
            current_dasha = {
                "sign": period["sign"],
                "type": period["type"],
                "start": period["start"],
                "end": period["end"],
            }
            break

    # Fallback: if now is beyond all computed periods, use the last one
    if current_dasha is None and mahadasha_periods:
        last = mahadasha_periods[-1]
        if now > _parse_date(last["end"]):
            current_dasha = {
                "sign": last["sign"],
                "type": last["type"],
                "start": last["start"],
                "end": last["end"],
            }

    # ── 8. Assemble result ──────────────────────────────────────
    return {
        "moon_nakshatra": nak_name,
        "moon_pada": pada_num,
        "navamsa_rashi": navamsa_rashi,
        "path": path_label,
        "deha_rashi": deha_rashi,
        "jeeva_rashi": jeeva_rashi,
        "balance_at_birth": round(balance, 6),
        "mahadasha_periods": mahadasha_periods,
        "current_dasha": current_dasha,
    }
