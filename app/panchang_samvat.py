"""
panchang_samvat.py -- Samvat Systems & Pushkara Navamsha
=========================================================
Pure calculation functions for:
- Brihaspati Samvatsara (बृहस्पति संवत्सर) — 60-year Jupiter cycle
- Gujarati Samvat (गुजराती संवत्) — Kartikadi variant
- Amanta / Purnimanta month systems (अमान्त / पूर्णिमान्त)
- Pushkara Navamsha (पुष्कर नवांश) — auspicious navamsha degrees

ALL strings include Hindi translations.
"""
from __future__ import annotations

from typing import Any, Dict

# ============================================================
# BRIHASPATI SAMVATSARA — 60-year Jupiter cycle
# ============================================================

SAMVATSARA_NAMES = [
    ("Prabhava", "प्रभव"), ("Vibhava", "विभव"), ("Shukla", "शुक्ल"),
    ("Pramodoota", "प्रमोदूत"), ("Prajothpatti", "प्रजोत्पत्ति"),
    ("Angirasa", "आंगिरस"), ("Shrimukha", "श्रीमुख"), ("Bhava", "भव"),
    ("Yuva", "युवा"), ("Dhaata", "धाता"), ("Eeshvara", "ईश्वर"),
    ("Bahudhanya", "बहुधान्य"), ("Pramaathi", "प्रमाथी"), ("Vikrama", "विक्रम"),
    ("Vrisha", "वृष"), ("Chitrabhanu", "चित्रभानु"), ("Svabhanu", "स्वभानु"),
    ("Taarana", "तारण"), ("Paarthiva", "पार्थिव"), ("Vyaya", "व्यय"),
    ("Sarvajitu", "सर्वजित्"), ("Sarvadhari", "सर्वधारी"), ("Virodhi", "विरोधी"),
    ("Vikruti", "विकृति"), ("Khara", "खर"), ("Nandana", "नन्दन"),
    ("Vijaya", "विजय"), ("Jaya", "जय"), ("Manmatha", "मन्मथ"),
    ("Durmukhi", "दुर्मुखी"), ("Hevilambi", "हेविलम्बी"), ("Vilambi", "विलम्बी"),
    ("Vikari", "विकारी"), ("Sharvari", "शार्वरी"), ("Plava", "प्लव"),
    ("Shubhakrutu", "शुभकृत्"), ("Shobhakrutu", "शोभकृत्"), ("Krodhi", "क्रोधी"),
    ("Vishvavasu", "विश्वावसु"), ("Parabhava", "पराभव"), ("Plavanga", "प्लवंग"),
    ("Keelaka", "कीलक"), ("Saumya", "सौम्य"), ("Sadharana", "साधारण"),
    ("Virodhikrutu", "विरोधिकृत्"), ("Paridhavi", "परिधावी"), ("Pramaadeecha", "प्रमादीच"),
    ("Ananda", "आनन्द"), ("Rakshasa", "राक्षस"), ("Nala", "नल"),
    ("Pingala", "पिंगल"), ("Kalayukti", "कालयुक्ति"), ("Siddharthi", "सिद्धार्थी"),
    ("Raudra", "रौद्र"), ("Durmati", "दुर्मति"), ("Dundubhi", "दुन्दुभि"),
    ("Rudhirodgari", "रुधिरोद्गारी"), ("Raktakshi", "रक्ताक्षी"), ("Krodhana", "क्रोधन"),
    ("Akshaya", "अक्षय"),
]


def get_brihaspati_samvatsara(vikram_samvat: int) -> Dict[str, Any]:
    """
    Return the Brihaspati Samvatsara (बृहस्पति संवत्सर) for a given Vikram Samvat year.

    The 60-year Jupiter cycle repeats: index = (VS - 1) % 60.
    """
    idx = (vikram_samvat - 1) % 60
    name, hindi = SAMVATSARA_NAMES[idx]
    return {
        "name": name,
        "name_hindi": hindi,
        "index": idx + 1,
        "year": vikram_samvat,
    }


# ============================================================
# GUJARATI SAMVAT (गुजराती संवत्) — Kartikadi
# ============================================================

# Months that fall BEFORE Kartik Shukla Pratipada (Gujarati New Year)
_MONTHS_BEFORE_KARTIK = frozenset([
    "Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
    "Shravana", "Bhadrapada", "Ashwin",
])


def get_gujarati_samvat(vikram_samvat: int, month_name: str) -> Dict[str, Any]:
    """
    Gujarati Samvat (गुजराती संवत्).

    Gujarati New Year starts from Kartik Shukla Pratipada (day after Diwali).
    For months before Kartik, Gujarati year = Vikram Samvat - 1.
    From Kartik onwards, Gujarati year = Vikram Samvat.
    """
    if month_name in _MONTHS_BEFORE_KARTIK:
        guj_year = vikram_samvat - 1
    else:
        guj_year = vikram_samvat

    idx = (guj_year - 1) % 60
    name, hindi = SAMVATSARA_NAMES[idx]
    return {
        "year": guj_year,
        "samvatsara": name,
        "samvatsara_hindi": hindi,
    }


# ============================================================
# AMANTA / PURNIMANTA MONTH SYSTEMS
# ============================================================

AMANTA_MONTHS = [
    ("Chaitra", "चैत्र"), ("Vaishakha", "वैशाख"), ("Jyeshtha", "ज्येष्ठ"),
    ("Ashadha", "आषाढ़"), ("Shravana", "श्रावण"), ("Bhadrapada", "भाद्रपद"),
    ("Ashwin", "आश्विन"), ("Kartik", "कार्तिक"), ("Margashirsha", "मार्गशीर्ष"),
    ("Pausha", "पौष"), ("Magha", "माघ"), ("Phalguna", "फाल्गुन"),
]


def get_month_systems(maas: str, paksha: str) -> Dict[str, Any]:
    """
    Return both Purnimant and Amant month names for the given lunar month and paksha.

    Purnimant (पूर्णिमान्त): Month ends on Purnima (North Indian).
    Amant (अमान्त): Month ends on Amavasya (South Indian / Gujarati).

    In Purnimant system, Krishna Paksha belongs to the NEXT month name.
    """
    purnimant_month = maas
    amant_month = maas

    # In Purnimant system, Krishna paksha is counted as part of the next month
    if paksha.lower() == "krishna":
        month_idx = next(
            (i for i, (m, _) in enumerate(AMANTA_MONTHS) if m == maas), 0
        )
        next_idx = (month_idx + 1) % 12
        purnimant_month = AMANTA_MONTHS[next_idx][0]

    purnimant_hindi = next(
        (h for m, h in AMANTA_MONTHS if m == purnimant_month), ""
    )
    amant_hindi = next(
        (h for m, h in AMANTA_MONTHS if m == amant_month), ""
    )

    return {
        "purnimant": {
            "month": purnimant_month,
            "month_hindi": purnimant_hindi,
            "system": "Purnimant",
            "system_hindi": "पूर्णिमान्त",
        },
        "amant": {
            "month": amant_month,
            "month_hindi": amant_hindi,
            "system": "Amant",
            "system_hindi": "अमान्त",
        },
    }


# ============================================================
# PUSHKARA NAVAMSHA (पुष्कर नवांश)
# ============================================================

# Each sign has a specific navamsha (3°20' segment) that is Pushkara.
# Key: rashi index (0=Aries .. 11=Pisces)
# Value: (start_degree, end_degree) within that sign (0-30 range)
PUSHKARA_NAVAMSHA = {
    0:  (20.0, 23.333),    # Aries:       Sagittarius navamsha
    1:  (6.667, 10.0),     # Taurus:      Cancer navamsha
    2:  (23.333, 26.667),  # Gemini:      Aquarius navamsha
    3:  (10.0, 13.333),    # Cancer:      Virgo navamsha
    4:  (26.667, 30.0),    # Leo:         Pisces navamsha
    5:  (13.333, 16.667),  # Virgo:       Libra navamsha
    6:  (0.0, 3.333),      # Libra:       Libra navamsha
    7:  (16.667, 20.0),    # Scorpio:     Taurus navamsha
    8:  (3.333, 6.667),    # Sagittarius: Capricorn navamsha
    9:  (20.0, 23.333),    # Capricorn:   Gemini navamsha
    10: (6.667, 10.0),     # Aquarius:    Leo navamsha
    11: (23.333, 26.667),  # Pisces:      Sagittarius navamsha
}

# Rashi name -> index mapping (Sanskrit transliteration)
RASHI_TO_INDEX = {
    "Mesha": 0, "Vrishabha": 1, "Mithuna": 2, "Karka": 3,
    "Simha": 4, "Kanya": 5, "Tula": 6, "Vrishchika": 7,
    "Dhanu": 8, "Makara": 9, "Kumbha": 10, "Meena": 11,
}

RASHI_HINDI = {
    0: "मेष", 1: "वृषभ", 2: "मिथुन", 3: "कर्क",
    4: "सिंह", 5: "कन्या", 6: "तुला", 7: "वृश्चिक",
    8: "धनु", 9: "मकर", 10: "कुम्भ", 11: "मीन",
}


def is_pushkara_navamsha(rashi_index: int, degree_in_sign: float) -> bool:
    """Check if a degree falls within the Pushkara Navamsha of its sign."""
    if rashi_index not in PUSHKARA_NAVAMSHA:
        return False
    start, end = PUSHKARA_NAVAMSHA[rashi_index]
    return start <= degree_in_sign < end


def check_lagna_pushkara(lagna_name: str, lagna_degree: float) -> Dict[str, Any]:
    """
    Check if the current lagna is in Pushkara Navamsha (पुष्कर नवांश).

    Parameters:
        lagna_name:   Rashi name in Sanskrit transliteration (e.g. "Mesha", "Tula")
        lagna_degree: Absolute sidereal longitude (0-360) or degree within sign (0-30)

    Returns dict with active flag, names (English + Hindi), and lagna info.
    """
    idx = RASHI_TO_INDEX.get(lagna_name, -1)
    is_pushkara = False
    if idx >= 0:
        degree_in_sign = lagna_degree % 30
        is_pushkara = is_pushkara_navamsha(idx, degree_in_sign)

    return {
        "active": is_pushkara,
        "name": "Pushkara Navamsha",
        "name_hindi": "पुष्कर नवांश",
        "lagna": lagna_name,
        "lagna_hindi": RASHI_HINDI.get(idx, ""),
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_samvat(
    vikram_samvat: int,
    maas: str,
    paksha: str,
    lagna_name: str = "",
    lagna_degree: float = 0.0,
) -> Dict[str, Any]:
    """
    Calculate all Samvat systems and Pushkara Navamsha in one call.

    Returns dict with keys: brihaspati, gujarati, month_systems, pushkara.
    """
    brihaspati = get_brihaspati_samvatsara(vikram_samvat)
    gujarati = get_gujarati_samvat(vikram_samvat, maas)
    month_systems = get_month_systems(maas, paksha)
    pushkara = check_lagna_pushkara(lagna_name, lagna_degree) if lagna_name else {
        "active": False,
        "name": "Pushkara Navamsha",
        "name_hindi": "पुष्कर नवांश",
        "lagna": "",
        "lagna_hindi": "",
    }

    return {
        "brihaspati": brihaspati,
        "gujarati": gujarati,
        "month_systems": month_systems,
        "pushkara": pushkara,
    }
