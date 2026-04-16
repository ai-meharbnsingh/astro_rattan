"""
panchang_nivas.py -- Nivas, Shool, Homahuti & Kumbha Chakra Calculations
=========================================================================
Pure calculation functions (no Flask/FastAPI dependencies).
All strings carry both English AND Hindi labels.

Calculations covered:
- Chandra Vasa (Moon's directional residence by nakshatra)
- Agnivasa (Fire god's residence by tithi)
- Rahu Vasa (Rahu's directional residence by weekday)
- Shivavasa (Shiva's residence by tithi)
- Homahuti (planet for homa fire offering by nakshatra)
- Kumbha Chakra (body part auspiciousness by weekday)
"""
from __future__ import annotations

from typing import Any, Dict, List

# ============================================================
# CHANDRA VASA (चन्द्र वास) -- Moon's directional residence
# ============================================================
# Nakshatras 0-6: East, 7-13: South, 14-20: West, 21-26: North
CHANDRA_VASA_RANGES: List[tuple[range, str, str]] = [
    (range(0, 7),   "East",  "पूर्व"),
    (range(7, 14),  "South", "दक्षिण"),
    (range(14, 21), "West",  "पश्चिम"),
    (range(21, 27), "North", "उत्तर"),
]


def calculate_chandra_vasa(nakshatra_index: int) -> Dict[str, Any]:
    """
    Return Moon's directional residence (Chandra Vasa) for a nakshatra.

    Parameters
    ----------
    nakshatra_index : int
        0-based nakshatra index (0 = Ashwini, ... 26 = Revati)

    Returns
    -------
    dict with keys: direction, direction_hindi, name, name_hindi
    """
    idx = nakshatra_index % 27
    direction = "East"
    direction_hindi = "पूर्व"
    for rng, d_en, d_hi in CHANDRA_VASA_RANGES:
        if idx in rng:
            direction = d_en
            direction_hindi = d_hi
            break
    return {
        "direction": direction,
        "direction_hindi": direction_hindi,
        "name": "Chandra Vasa",
        "name_hindi": "चन्द्र वास",
    }


# ============================================================
# AGNIVASA (अग्नि वास) -- Fire god's residence by tithi
# ============================================================
# 5-tithi cycle: Prithvi → Jala → Akasha
# Tithis 1-5: Prithvi, 6-10: Jala, 11-15: Akasha
# Krishna: 16-20: Prithvi, 21-25: Jala, 26-30: Akasha
AGNIVASA_ELEMENTS: Dict[int, tuple[str, str]] = {
    0: ("Prithvi", "पृथ्वी"),   # tithis 1-5, 16-20
    1: ("Jala", "जल"),          # tithis 6-10, 21-25
    2: ("Akasha", "आकाश"),      # tithis 11-15, 26-30
}


def calculate_agnivasa(tithi_index: int) -> Dict[str, Any]:
    """
    Return Agnivasa (fire god's residence element) for a tithi.

    Parameters
    ----------
    tithi_index : int
        1-based tithi number (1-30).

    Returns
    -------
    dict with keys: location, location_hindi, name, name_hindi
    """
    # Map 1-30 into groups of 5: (tithi-1)//5 gives 0..5, mod 3 gives cycle
    group = ((tithi_index - 1) // 5) % 3
    location, location_hindi = AGNIVASA_ELEMENTS[group]
    return {
        "location": location,
        "location_hindi": location_hindi,
        "name": "Agnivasa",
        "name_hindi": "अग्नि वास",
    }


# ============================================================
# RAHU VASA (राहु वास) -- Rahu's residence by weekday
# ============================================================
RAHU_VASA: Dict[int, tuple[str, str]] = {
    0: ("South", "दक्षिण"),          # Sunday
    1: ("South-West", "नैऋत्य"),     # Monday
    2: ("South-East", "आग्नेय"),     # Tuesday
    3: ("North-West", "वायव्य"),     # Wednesday
    4: ("North-East", "ईशान"),       # Thursday
    5: ("West", "पश्चिम"),          # Friday
    6: ("East", "पूर्व"),           # Saturday
}


def calculate_rahu_vasa(weekday: int) -> Dict[str, Any]:
    """
    Return Rahu's directional residence for a weekday.

    Parameters
    ----------
    weekday : int
        0 = Sunday, 1 = Monday, ... 6 = Saturday

    Returns
    -------
    dict with keys: direction, direction_hindi, name, name_hindi
    """
    direction, direction_hindi = RAHU_VASA[weekday % 7]
    return {
        "direction": direction,
        "direction_hindi": direction_hindi,
        "name": "Rahu Vasa",
        "name_hindi": "राहु वास",
    }


# ============================================================
# SHIVAVASA (शिव वास) -- Shiva's residence by tithi
# ============================================================
# 5-tithi cycle within each paksha:
# tithis 1-5 / 16-20: with Gowri
# tithis 6-10 / 21-25: in Kailasha
# tithis 11-15 / 26-30: in Shmashana
SHIVAVASA_LOCATIONS: Dict[int, tuple[str, str]] = {
    0: ("with Gowri", "गौरी के साथ"),
    1: ("in Kailasha", "कैलाश में"),
    2: ("in Shmashana", "श्मशान में"),
}


def calculate_shivavasa(tithi_index: int) -> Dict[str, Any]:
    """
    Return Shiva's residence for a tithi.

    Parameters
    ----------
    tithi_index : int
        1-based tithi number (1-30).

    Returns
    -------
    dict with keys: location, location_hindi, name, name_hindi
    """
    group = ((tithi_index - 1) // 5) % 3
    location, location_hindi = SHIVAVASA_LOCATIONS[group]
    return {
        "location": location,
        "location_hindi": location_hindi,
        "name": "Shivavasa",
        "name_hindi": "शिव वास",
    }


# ============================================================
# HOMAHUTI (होमाहुति) -- Planet for homa by nakshatra
# ============================================================
HOMAHUTI_PLANETS: List[str] = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter",
    "Venus", "Saturn", "Rahu", "Ketu",
]
HOMAHUTI_HINDI: List[str] = [
    "सूर्य", "चन्द्र", "मंगल", "बुध", "बृहस्पति",
    "शुक्र", "शनि", "राहु", "केतु",
]


def calculate_homahuti(nakshatra_index: int) -> Dict[str, Any]:
    """
    Return the planet for homa (fire offering) based on nakshatra.

    Parameters
    ----------
    nakshatra_index : int
        0-based nakshatra index (0 = Ashwini, ... 26 = Revati)

    Returns
    -------
    dict with keys: planet, planet_hindi, name, name_hindi
    """
    idx = nakshatra_index % 9
    return {
        "planet": HOMAHUTI_PLANETS[idx],
        "planet_hindi": HOMAHUTI_HINDI[idx],
        "name": "Homahuti",
        "name_hindi": "होमाहुति",
    }


# ============================================================
# KUMBHA CHAKRA (कुम्भ चक्र) -- Body part by weekday
# ============================================================
KUMBHA_CHAKRA: Dict[int, tuple[str, str, bool]] = {
    0: ("Feet", "पैर", False),        # Sunday - Inauspicious
    1: ("Head", "सिर", True),         # Monday - Auspicious
    2: ("Face", "मुख", False),        # Tuesday - Inauspicious
    3: ("Chest", "छाती", True),       # Wednesday - Auspicious
    4: ("Navel", "नाभि", True),      # Thursday - Auspicious
    5: ("Throat", "कण्ठ", True),      # Friday - Auspicious
    6: ("Waist", "कमर", False),       # Saturday - Inauspicious
}


def calculate_kumbha_chakra(weekday: int) -> Dict[str, Any]:
    """
    Return Kumbha Chakra body part and auspiciousness for a weekday.

    Parameters
    ----------
    weekday : int
        0 = Sunday, 1 = Monday, ... 6 = Saturday

    Returns
    -------
    dict with keys: body_part, body_part_hindi, auspicious, name, name_hindi
    """
    body_part, body_part_hindi, auspicious = KUMBHA_CHAKRA[weekday % 7]
    return {
        "body_part": body_part,
        "body_part_hindi": body_part_hindi,
        "auspicious": auspicious,
        "name": "Kumbha Chakra",
        "name_hindi": "कुम्भ चक्र",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_nivas(
    weekday: int,
    tithi_index: int,
    nakshatra_index: int,
) -> Dict[str, Any]:
    """
    Master function -- returns all Nivas, Homahuti & Kumbha Chakra calculations.

    Parameters
    ----------
    weekday : int
        0 = Sunday ... 6 = Saturday
    tithi_index : int
        1-based tithi number (1-30)
    nakshatra_index : int
        0-based nakshatra index (0-26)

    Returns
    -------
    dict with keys: chandra_vasa, agnivasa, rahu_vasa, shivavasa, homahuti,
                    kumbha_chakra
    """
    return {
        "chandra_vasa": calculate_chandra_vasa(nakshatra_index),
        "agnivasa": calculate_agnivasa(tithi_index),
        "rahu_vasa": calculate_rahu_vasa(weekday),
        "shivavasa": calculate_shivavasa(tithi_index),
        "homahuti": calculate_homahuti(nakshatra_index),
        "kumbha_chakra": calculate_kumbha_chakra(weekday),
    }
