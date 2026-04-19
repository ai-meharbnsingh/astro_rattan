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
DWIPUSHKAR_TITHIS: List[int] = [3, 8, 13]  # Tritiya, Ashtami, Trayodashi
DWIPUSHKAR_WEEKDAYS: List[int] = [0, 2, 6]  # Sunday, Tuesday, Saturday
DWIPUSHKAR_NAKSHATRAS: List[str] = [
    "Chitra", "Mrigashira", "Dhanishta",
    "Purva Ashadha", "Purva Phalguni", "Purva Bhadrapada",
    "Vishakha",
]

# ============================================================
# TRIPUSHKAR YOGA — Tithi + Nakshatra + Weekday
# ============================================================
TRIPUSHKAR_TITHIS: List[int] = [2, 7, 12]  # Dwitiya, Saptami, Dwadashi
TRIPUSHKAR_WEEKDAYS: List[int] = [0, 2, 6]  # Sunday, Tuesday, Saturday
TRIPUSHKAR_NAKSHATRAS: List[str] = [
    "Krittika", "Punarvasu", "Uttara Phalguni",
    "Vishakha", "Uttara Ashadha", "Purva Bhadrapada",
]

# ============================================================
# RAVI YOGA — Sun-ruled nakshatra on Sunday
# ============================================================
RAVI_NAKSHATRAS: List[str] = [
    "Krittika", "Uttara Phalguni", "Uttara Ashadha",
]

# ============================================================
# SIDDHI YOGA — Tithi category + Weekday combinations
# (Muhurta Chintamani: Nanda/Bhadra/Jaya/Rikta/Purna tithis
#  on specific weekday lords)
# ============================================================
SIDDHI_YOGA_TITHI_WEEKDAY: Dict[int, List[int]] = {
    # weekday: list of favorable tithis (1-15)
    0: [1, 6, 11],          # Sunday: Nanda tithis
    1: [2, 7, 12],          # Monday: Bhadra tithis
    2: [1, 3, 6, 8, 11, 13], # Tuesday: Nanda + Jaya
    3: [2, 3, 7, 8, 12, 13], # Wednesday: Bhadra + Jaya
    4: [4, 5, 9, 10, 14, 15], # Thursday: Rikta + Purna
    5: [2, 7, 12],          # Friday: Bhadra tithis
    6: [4, 5, 9, 10, 14, 15], # Saturday: Rikta + Purna
}

# ============================================================
# TITHI-VARA DOSHA — Inauspicious tithi + weekday combinations
# (Muhurta Chintamani, Shubhashubha Prakarana)
# ============================================================
# Each entry: weekday -> {dosha_name: tithi_or_list}
TITHI_VARA_DOSHA: Dict[int, Dict[str, Any]] = {
    0: {  # Sunday
        "Dagdha": 12,
        "Visha": 4,
        "Hutasana": 12,
        "Krakacha": 12,
        "Samvartaka": 7,
    },
    1: {  # Monday
        "Dagdha": 11,
        "Visha": 6,
        "Hutasana": 6,
        "Krakacha": 11,
    },
    2: {  # Tuesday
        "Dagdha": 5,
        "Visha": 7,
        "Hutasana": 7,
        "Krakacha": 10,
    },
    3: {  # Wednesday
        "Dagdha": [2, 3],
        "Visha": 2,
        "Hutasana": 8,
        "Krakacha": 9,
        "Samvartaka": 1,
    },
    4: {  # Thursday
        "Dagdha": 6,
        "Visha": 8,
        "Hutasana": 9,
        "Krakacha": 8,
    },
    5: {  # Friday
        "Dagdha": 8,
        "Visha": 9,
        "Hutasana": 10,
        "Krakacha": 7,
    },
    6: {  # Saturday
        "Dagdha": 9,
        "Visha": 7,
        "Hutasana": 11,
        "Krakacha": 6,
    },
}

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
# DAGDHA NAKSHATRA — Burned nakshatra per Hindu month
# ============================================================
DAGDHA_NAKSHATRA_BY_MONTH: Dict[str, List[str]] = {
    "Chaitra": ["Bharani", "Krittika"],
    "Vaishakha": ["Rohini", "Mrigashira"],
    "Jyeshtha": ["Ardra", "Punarvasu"],
    "Ashadha": ["Pushya", "Ashlesha"],
    "Shravana": ["Magha", "Purva Phalguni"],
    "Bhadrapada": ["Uttara Phalguni", "Hasta"],
    "Ashwin": ["Chitra", "Swati"],
    "Kartik": ["Vishakha", "Anuradha"],
    "Margashirsha": ["Jyeshtha", "Mula"],
    "Pausha": ["Purva Ashadha", "Uttara Ashadha"],
    "Magha": ["Shravana", "Dhanishta"],
    "Phalguna": ["Shatabhisha", "Purva Bhadrapada"],
}


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


def calculate_ravi_yoga(
    weekday: int,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Calculate Ravi Yoga.

    Active when a Sun-ruled nakshatra (Krittika, Uttara Phalguni,
    Uttara Ashadha) falls on Sunday.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, name, name_hindi
    """
    active = weekday == 0 and nakshatra_name in RAVI_NAKSHATRAS
    return {
        "active": active,
        "name": "Ravi Yoga",
        "name_hindi": "रवि योग",
    }


def calculate_siddhi_yoga(
    weekday: int,
    tithi_index: int,
) -> Dict[str, Any]:
    """Calculate Siddhi Yoga (auspicious tithi + weekday combination).

    Based on Muhurta Chintamani: specific tithi categories on
    specific weekdays.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30

    Returns:
        dict with keys: active, name, name_hindi
    """
    norm_tithi = _normalise_tithi(tithi_index)
    favorable = SIDDHI_YOGA_TITHI_WEEKDAY.get(weekday, [])
    active = norm_tithi in favorable
    return {
        "active": active,
        "name": "Siddhi Yoga",
        "name_hindi": "सिद्धि योग",
    }


def calculate_tithi_vara_dosha(
    weekday: int,
    tithi_index: int,
) -> Dict[str, Any]:
    """Calculate all Tithi-Vara doshas for the day.

    Returns a list of active inauspicious combinations
    (Dagdha, Visha, Hutasana, Krakacha, Samvartaka).

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30

    Returns:
        dict with keys: active_doshas (list), all_doshas (dict)
    """
    norm_tithi = _normalise_tithi(tithi_index)
    dosha_map = TITHI_VARA_DOSHA.get(weekday, {})

    active_doshas: List[Dict[str, Any]] = []
    for name, tithis in dosha_map.items():
        if isinstance(tithis, int):
            tithis = [tithis]
        if norm_tithi in tithis:
            active_doshas.append({
                "name": name,
                "name_hindi": {
                    "Dagdha": "दग्ध",
                    "Visha": "विष",
                    "Hutasana": "हुताशन",
                    "Krakacha": "क्रकच",
                    "Samvartaka": "संवर्तक",
                }.get(name, name),
                "tithi": norm_tithi,
            })

    return {
        "active": len(active_doshas) > 0,
        "active_doshas": active_doshas,
        "name": "Tithi-Vara Dosha",
        "name_hindi": "तिथि-वार दोष",
    }


def calculate_dagdha_nakshatra(hindu_month: str, nakshatra_name: str) -> Dict[str, Any]:
    """Calculate Dagdha Nakshatra (burned nakshatra for the month).

    Args:
        hindu_month: English Hindu month name (e.g. "Chaitra")
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: active, nakshatra, month, dagdha_list, name, name_hindi
    """
    dagdha_list = DAGDHA_NAKSHATRA_BY_MONTH.get(hindu_month, [])

    return {
        "active": nakshatra_name in dagdha_list,
        "nakshatra": nakshatra_name,
        "month": hindu_month,
        "dagdha_list": dagdha_list,
        "name": "Dagdha Nakshatra",
        "name_hindi": "दग्ध नक्षत्र",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_special_yogas(
    weekday: int,
    tithi_index: int,
    nakshatra_name: str,
    include_extended: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Calculate all special yogas at once.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30 (Shukla 1-15, Krishna 16-30)
        nakshatra_name: English nakshatra name

    Returns:
        dict with keys: sarvartha_siddhi, amrit_siddhi,
        dwipushkar, tripushkar, ganda_moola.

        If include_extended=True, also includes: ravi_yoga,
        siddhi_yoga, tithi_vara_dosha.
    """
    result: Dict[str, Dict[str, Any]] = {
        "sarvartha_siddhi": calculate_sarvartha_siddhi(weekday, tithi_index, nakshatra_name),
        "amrit_siddhi": calculate_amrit_siddhi(weekday, nakshatra_name),
        "dwipushkar": calculate_dwipushkar(weekday, tithi_index, nakshatra_name),
        "tripushkar": calculate_tripushkar(weekday, tithi_index, nakshatra_name),
        "ganda_moola": calculate_ganda_moola(nakshatra_name),
    }
    if include_extended:
        result["ravi_yoga"] = calculate_ravi_yoga(weekday, nakshatra_name)
        result["siddhi_yoga"] = calculate_siddhi_yoga(weekday, tithi_index)
        result["tithi_vara_dosha"] = calculate_tithi_vara_dosha(weekday, tithi_index)
    return result
