"""
panchang_directions.py -- Directional & Anandadi Calculations
=============================================================
Pure calculation functions for Vedic panchang directional indicators:
- Disha Shool (inauspicious direction by weekday)
- Baana (elemental direction by tithi)
- Anandadi Yoga (28 yogas from weekday + nakshatra)
- Lucky Day Indicators (color, number, direction by weekday lord)

All strings include English AND Hindi.
No web framework dependencies.
"""
from __future__ import annotations

from typing import Any, Dict

# ============================================================
# DISHA SHOOL (दिशा शूल) -- inauspicious direction by weekday
# ============================================================
DISHA_SHOOL = {
    0: ("East", "पूर्व"),       # Sunday
    1: ("West", "पश्चिम"),      # Monday
    2: ("North", "उत्तर"),      # Tuesday
    3: ("North", "उत्तर"),      # Wednesday
    4: ("South", "दक्षिण"),     # Thursday
    5: ("West", "पश्चिम"),      # Friday
    6: ("East", "पूर्व"),       # Saturday
}

# ============================================================
# BAANA (बाण) -- elemental direction by tithi (5-element cycle)
# Key = (tithi_index - 1) % 5
# Agni (Fire) for tithis 1,6,11 — East
# Vayu (Wind) for tithis 2,7,12 — North-West
# Jala (Water) for tithis 3,8,13 — West
# Prithvi (Earth) for tithis 4,9,14 — South
# Akasha (Ether) for tithis 5,10,15,30 — Overhead
# ============================================================
BAANA_ELEMENTS = {
    0: ("Agni", "अग्नि", "East", "पूर्व"),
    1: ("Vayu", "वायु", "North-West", "वायव्य"),
    2: ("Jala", "जल", "West", "पश्चिम"),
    3: ("Prithvi", "पृथ्वी", "South", "दक्षिण"),
    4: ("Akasha", "आकाश", "Overhead", "ऊपर"),
}

# ============================================================
# ANANDADI YOGAS (आनन्दादि योग) -- 28 yogas
# Formula: (weekday_number * 7 + nakshatra_number) % 28
# ============================================================
ANANDADI_YOGAS = [
    ("Ananda", "आनन्द", True),             # 0  - Auspicious
    ("Kaldanda", "कालदण्ड", False),         # 1  - Inauspicious
    ("Dhvaja", "ध्वज", True),               # 2  - Auspicious
    ("Shrivatsa", "श्रीवत्स", True),        # 3  - Auspicious
    ("Vajra", "वज्र", False),               # 4  - Inauspicious
    ("Mudgara", "मुद्गर", False),           # 5  - Inauspicious
    ("Chhatra", "छत्र", True),              # 6  - Auspicious
    ("Mitra", "मित्र", True),               # 7  - Auspicious
    ("Manasa", "मानस", True),               # 8  - Auspicious
    ("Padma", "पद्म", True),                # 9  - Auspicious
    ("Lamba", "लम्ब", False),               # 10 - Inauspicious
    ("Utpata", "उत्पात", False),            # 11 - Inauspicious
    ("Mrityu", "मृत्यु", False),            # 12 - Inauspicious
    ("Kana", "काण", False),                 # 13 - Inauspicious
    ("Siddhi", "सिद्धि", True),             # 14 - Auspicious
    ("Shubha", "शुभ", True),                # 15 - Auspicious
    ("Amrita", "अमृत", True),               # 16 - Auspicious
    ("Mushala", "मुशल", False),             # 17 - Inauspicious
    ("Gada", "गदा", False),                 # 18 - Inauspicious
    ("Maatanga", "मातंग", True),            # 19 - Auspicious
    ("Rakshasa", "राक्षस", False),          # 20 - Inauspicious
    ("Chara", "चर", False),                 # 21 - Inauspicious
    ("Pravardhini", "प्रवर्धिनी", True),    # 22 - Auspicious
    ("Dhruva", "ध्रुव", True),              # 23 - Auspicious
    ("Shula", "शूल", False),                # 24 - Inauspicious
    ("Ganda", "गण्ड", False),               # 25 - Inauspicious
    ("Vriddhi", "वृद्धि", True),            # 26 - Auspicious
    ("Dhvanksha", "ध्वांक्ष", False),       # 27 - Inauspicious
]

# ============================================================
# LUCKY INDICATORS (शुभ संकेत) -- by weekday lord
# ============================================================
LUCKY_INDICATORS = {
    0: {  # Sunday - Sun
        "color": "Copper", "color_hindi": "ताम्र",
        "number": 1,
        "direction": "East", "direction_hindi": "पूर्व",
    },
    1: {  # Monday - Moon
        "color": "White", "color_hindi": "सफ़ेद",
        "number": 2,
        "direction": "North-West", "direction_hindi": "वायव्य",
    },
    2: {  # Tuesday - Mars
        "color": "Red", "color_hindi": "लाल",
        "number": 9,
        "direction": "South", "direction_hindi": "दक्षिण",
    },
    3: {  # Wednesday - Mercury
        "color": "Green", "color_hindi": "हरा",
        "number": 5,
        "direction": "North", "direction_hindi": "उत्तर",
    },
    4: {  # Thursday - Jupiter
        "color": "Yellow", "color_hindi": "पीला",
        "number": 3,
        "direction": "North-East", "direction_hindi": "ईशान",
    },
    5: {  # Friday - Venus
        "color": "White", "color_hindi": "सफ़ेद",
        "number": 6,
        "direction": "South-East", "direction_hindi": "आग्नेय",
    },
    6: {  # Saturday - Saturn
        "color": "Black", "color_hindi": "काला",
        "number": 8,
        "direction": "West", "direction_hindi": "पश्चिम",
    },
}


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def calculate_disha_shool(weekday: int) -> Dict[str, Any]:
    """
    Return the inauspicious direction (Disha Shool) for a weekday.

    Parameters
    ----------
    weekday : int
        0 = Sunday, 1 = Monday, ... 6 = Saturday

    Returns
    -------
    dict with keys: direction, direction_hindi, name, name_hindi
    """
    direction, direction_hindi = DISHA_SHOOL[weekday % 7]
    return {
        "direction": direction,
        "direction_hindi": direction_hindi,
        "name": "Disha Shool",
        "name_hindi": "दिशा शूल",
    }


def calculate_baana(tithi_index: int) -> Dict[str, Any]:
    """
    Return the Baana (elemental arrow direction) for a tithi.

    Parameters
    ----------
    tithi_index : int
        1-based tithi number (1-30). Internally mapped via (tithi_index - 1) % 5.

    Returns
    -------
    dict with keys: element, element_hindi, direction, direction_hindi, name, name_hindi
    """
    key = (tithi_index - 1) % 5
    element, element_hindi, direction, direction_hindi = BAANA_ELEMENTS[key]
    return {
        "element": element,
        "element_hindi": element_hindi,
        "direction": direction,
        "direction_hindi": direction_hindi,
        "name": "Baana",
        "name_hindi": "बाण",
    }


def calculate_anandadi_yoga(weekday: int, nakshatra_index: int) -> Dict[str, Any]:
    """
    Return the Anandadi Yoga for a weekday + nakshatra combination.

    Parameters
    ----------
    weekday : int
        0 = Sunday, 1 = Monday, ... 6 = Saturday
    nakshatra_index : int
        0-based nakshatra index (0 = Ashwini, ... 26 = Revati)

    Returns
    -------
    dict with keys: name, name_hindi, auspicious, index
    """
    idx = (weekday * 7 + nakshatra_index) % 28
    name, name_hindi, auspicious = ANANDADI_YOGAS[idx]
    return {
        "name": name,
        "name_hindi": name_hindi,
        "auspicious": auspicious,
        "index": idx,
    }


def calculate_lucky_indicators(weekday: int) -> Dict[str, Any]:
    """
    Return lucky-day indicators (color, number, direction) for a weekday.

    Parameters
    ----------
    weekday : int
        0 = Sunday, 1 = Monday, ... 6 = Saturday

    Returns
    -------
    dict with keys: color, color_hindi, number, direction, direction_hindi,
                    name, name_hindi
    """
    info = LUCKY_INDICATORS[weekday % 7]
    return {
        "color": info["color"],
        "color_hindi": info["color_hindi"],
        "number": info["number"],
        "direction": info["direction"],
        "direction_hindi": info["direction_hindi"],
        "name": "Lucky Indicators",
        "name_hindi": "शुभ संकेत",
    }


def calculate_all_directions(
    weekday: int,
    tithi_index: int,
    nakshatra_index: int,
) -> Dict[str, Any]:
    """
    Master function -- returns all directional and Anandadi calculations.

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
    dict with keys: disha_shool, baana, anandadi_yoga, lucky
    """
    return {
        "disha_shool": calculate_disha_shool(weekday),
        "baana": calculate_baana(tithi_index),
        "anandadi_yoga": calculate_anandadi_yoga(weekday, nakshatra_index),
        "lucky": calculate_lucky_indicators(weekday),
    }
