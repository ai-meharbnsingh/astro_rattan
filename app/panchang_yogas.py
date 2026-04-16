"""
panchang_yogas.py -- Special Yoga Calculations for Vedic Panchang
=================================================================
Pure calculation functions (no Flask/FastAPI dependencies).
Each function takes panchang data as input and returns a result dict.

Yogas covered:
- Sarvartha Siddhi Yoga (tithi+nakshatra+weekday → auspicious day)
- Amrit Siddhi Yoga (weekday+nakshatra)
- Dwipushkar Yoga (tithi+nakshatra+weekday → doubled results)
- Tripushkar Yoga (tithi+nakshatra+weekday → tripled results)
- Ganda Moola (junction nakshatras)
"""
from __future__ import annotations

from typing import Any, Dict, List

# ============================================================
# SARVARTHA SIDDHI YOGA — Tithi + Weekday combinations
# ============================================================
# weekday: 0=Sunday .. 6=Saturday
# tithi_index: 1-based (1=Pratipada .. 15=Purnima, repeats for Krishna paksha)
# We normalise tithi_index to 1-15 range internally.

SARVARTHA_SIDDHI_TITHI: Dict[int, List[int]] = {
    0: [2, 7, 12],   # Sunday:    Dwitiya, Saptami, Dwadashi
    1: [2, 7, 12],   # Monday:    Dwitiya, Saptami, Dwadashi
    2: [1, 6, 11],   # Tuesday:   Pratipada, Shashthi, Ekadashi
    3: [3, 8, 13],   # Wednesday: Tritiya, Ashtami, Trayodashi
    4: [4, 9, 14],   # Thursday:  Chaturthi, Navami, Chaturdashi
    5: [1, 6, 11],   # Friday:    Pratipada, Shashthi, Ekadashi
    6: [5, 10, 15],  # Saturday:  Panchami, Dashami, Purnima
}

# Sarvartha Siddhi also valid when specific nakshatras fall on specific weekdays
SARVARTHA_SIDDHI_NAKSHATRA: Dict[int, List[str]] = {
    0: ["Pushya", "Hasta", "Ashwini", "Abhijit"],       # Sunday
    1: ["Rohini", "Mrigashira", "Shravana", "Hasta"],    # Monday
    2: ["Ashwini", "Krittika", "Uttara Phalguni"],        # Tuesday
    3: ["Anuradha", "Hasta", "Revati"],                   # Wednesday
    4: ["Punarvasu", "Pushya", "Revati"],                 # Thursday
    5: ["Revati", "Anuradha", "Pushya", "Ashwini"],       # Friday
    6: ["Swati", "Rohini", "Shravana"],                   # Saturday
}

# ============================================================
# AMRIT SIDDHI YOGA — Weekday + Nakshatra
# ============================================================
AMRIT_SIDDHI: Dict[int, str] = {
    0: "Hasta",       # Sunday + Hasta
    1: "Rohini",      # Monday + Rohini
    2: "Ashwini",     # Tuesday + Ashwini
    3: "Anuradha",    # Wednesday + Anuradha
    4: "Punarvasu",   # Thursday + Punarvasu
    5: "Revati",      # Friday + Revati
    6: "Shravana",    # Saturday + Shravana
}

# ============================================================
# DWIPUSHKAR YOGA — Tithi + Nakshatra + Weekday
# ============================================================
DWIPUSHKAR_TITHIS: List[int] = [2, 7, 12]  # Dwitiya, Saptami, Dwadashi
DWIPUSHKAR_WEEKDAYS: List[int] = [0, 2, 6]  # Sunday, Tuesday, Saturday
DWIPUSHKAR_NAKSHATRAS: List[str] = [
    "Chitra", "Mrigashira", "Dhanishta",
    "Purva Ashadha", "Purva Phalguni", "Purva Bhadrapada",
    "Vishakha",
]

# ============================================================
# TRIPUSHKAR YOGA — Tithi + Nakshatra + Weekday
# ============================================================
TRIPUSHKAR_TITHIS: List[int] = [3, 8, 13]  # Tritiya, Ashtami, Trayodashi
TRIPUSHKAR_WEEKDAYS: List[int] = [0, 2, 6]  # Sunday, Tuesday, Saturday
TRIPUSHKAR_NAKSHATRAS: List[str] = [
    "Krittika", "Punarvasu", "Uttara Phalguni",
    "Vishakha", "Uttara Ashadha", "Purva Bhadrapada",
]

# ============================================================
# GANDA MOOLA — Junction nakshatras
# ============================================================
GANDA_MOOLA_NAKSHATRAS: List[str] = [
    "Ashwini",    # First of Aries group
    "Ashlesha",   # Last of Cancer group
    "Magha",      # First of Leo group
    "Jyeshtha",   # Last of Scorpio group
    "Moola",      # First of Sagittarius group
    "Revati",     # Last of Pisces group
]


# ============================================================
# HELPER
# ============================================================

def _normalise_tithi(tithi_index: int) -> int:
    """Normalise a 1-30 tithi index into 1-15 range.

    Tithis 1-15 are Shukla paksha, 16-30 are Krishna paksha.
    The tithi *name* repeats: Krishna Pratipada (16) maps to 1, etc.
    For yoga lookup we only need the 1-15 position.
    """
    if 1 <= tithi_index <= 15:
        return tithi_index
    if 16 <= tithi_index <= 30:
        return tithi_index - 15
    raise ValueError(f"tithi_index must be 1-30, got {tithi_index}")


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def calculate_sarvartha_siddhi(
    weekday: int,
    tithi_index: int,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Calculate Sarvartha Siddhi Yoga.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30 (Shukla 1-15, Krishna 16-30)
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, type, name, name_hindi
    """
    norm_tithi = _normalise_tithi(tithi_index)

    tithi_match = norm_tithi in SARVARTHA_SIDDHI_TITHI.get(weekday, [])
    nakshatra_match = nakshatra_name in SARVARTHA_SIDDHI_NAKSHATRA.get(weekday, [])

    if tithi_match and nakshatra_match:
        yoga_type = "whole_day"
    elif tithi_match or nakshatra_match:
        yoga_type = "partial"
    else:
        yoga_type = "partial"  # not used when inactive

    active = tithi_match or nakshatra_match

    return {
        "active": active,
        "type": yoga_type if active else "partial",
        "name": "Sarvartha Siddhi Yoga",
        "name_hindi": "सर्वार्थ सिद्धि योग",
    }


def calculate_amrit_siddhi(
    weekday: int,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Calculate Amrit Siddhi Yoga.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, name, name_hindi
    """
    required_nakshatra = AMRIT_SIDDHI.get(weekday)
    active = nakshatra_name == required_nakshatra

    return {
        "active": active,
        "name": "Amrit Siddhi Yoga",
        "name_hindi": "अमृत सिद्धि योग",
    }


def calculate_dwipushkar(
    weekday: int,
    tithi_index: int,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Calculate Dwipushkar Yoga.

    Active when Dwitiya/Saptami/Dwadashi tithi falls on
    Sunday/Tuesday/Saturday AND the nakshatra is one of the
    Dwipushkar nakshatras.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, name, name_hindi
    """
    norm_tithi = _normalise_tithi(tithi_index)
    active = (
        norm_tithi in DWIPUSHKAR_TITHIS
        and weekday in DWIPUSHKAR_WEEKDAYS
        and nakshatra_name in DWIPUSHKAR_NAKSHATRAS
    )

    return {
        "active": active,
        "name": "Dwipushkar Yoga",
        "name_hindi": "द्विपुष्कर योग",
    }


def calculate_tripushkar(
    weekday: int,
    tithi_index: int,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Calculate Tripushkar Yoga.

    Active when Tritiya/Ashtami/Trayodashi falls on
    Sunday/Tuesday/Saturday AND the nakshatra is one of the
    Tripushkar nakshatras.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, name, name_hindi
    """
    norm_tithi = _normalise_tithi(tithi_index)
    active = (
        norm_tithi in TRIPUSHKAR_TITHIS
        and weekday in TRIPUSHKAR_WEEKDAYS
        and nakshatra_name in TRIPUSHKAR_NAKSHATRAS
    )

    return {
        "active": active,
        "name": "Tripushkar Yoga",
        "name_hindi": "त्रिपुष्कर योग",
    }


def calculate_ganda_moola(nakshatra_name: str) -> Dict[str, Any]:
    """Calculate Ganda Moola.

    Active when Moon is in a junction nakshatra (first/last of each
    rashi group): Ashwini, Ashlesha, Magha, Jyeshtha, Moola, Revati.

    Args:
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, nakshatra, name, name_hindi
    """
    active = nakshatra_name in GANDA_MOOLA_NAKSHATRAS

    return {
        "active": active,
        "nakshatra": nakshatra_name,
        "name": "Ganda Moola",
        "name_hindi": "गण्ड मूल",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_special_yogas(
    weekday: int,
    tithi_index: int,
    nakshatra_name: str,
) -> Dict[str, Dict[str, Any]]:
    """Calculate all special yogas at once.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30 (Shukla 1-15, Krishna 16-30)
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: sarvartha_siddhi, amrit_siddhi,
        dwipushkar, tripushkar, ganda_moola
    """
    return {
        "sarvartha_siddhi": calculate_sarvartha_siddhi(weekday, tithi_index, nakshatra_name),
        "amrit_siddhi": calculate_amrit_siddhi(weekday, nakshatra_name),
        "dwipushkar": calculate_dwipushkar(weekday, tithi_index, nakshatra_name),
        "tripushkar": calculate_tripushkar(weekday, tithi_index, nakshatra_name),
        "ganda_moola": calculate_ganda_moola(nakshatra_name),
    }
