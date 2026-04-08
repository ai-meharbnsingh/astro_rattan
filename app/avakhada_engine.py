"""
avakhada_engine.py — Avakhada Chakra Calculation Engine
========================================================
Computes the comprehensive birth summary table (Avakhada Chakra)
from chart data: ascendant, Moon position, Sun position, and planet data.
"""
import math
import traceback
from typing import Any, Dict, List, Optional

# ============================================================
# CONSTANTS
# ============================================================

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Sign lords (traditional Vedic rulerships)
SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# 27 Nakshatras
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13.3333... degrees

# Yoni (animal nature) by nakshatra index — standard Vedic reference
YONI_BY_NAKSHATRA = [
    "Horse (Ashwa)",      # 0  Ashwini
    "Elephant (Gaja)",    # 1  Bharani
    "Sheep (Mesha)",      # 2  Krittika
    "Serpent (Sarpa)",    # 3  Rohini
    "Serpent (Sarpa)",    # 4  Mrigashira
    "Dog (Shwan)",        # 5  Ardra
    "Cat (Marjar)",       # 6  Punarvasu
    "Sheep (Mesha)",      # 7  Pushya
    "Cat (Marjar)",       # 8  Ashlesha
    "Rat (Mushak)",       # 9  Magha
    "Rat (Mushak)",       # 10 Purva Phalguni
    "Cow (Gau)",          # 11 Uttara Phalguni
    "Buffalo (Mahish)",   # 12 Hasta
    "Tiger (Vyaghra)",    # 13 Chitra
    "Buffalo (Mahish)",   # 14 Swati
    "Tiger (Vyaghra)",    # 15 Vishakha
    "Deer (Mrig)",        # 16 Anuradha
    "Deer (Mrig)",        # 17 Jyeshtha
    "Dog (Shwan)",        # 18 Mula
    "Monkey (Vanar)",     # 19 Purva Ashadha
    "Mongoose (Nakul)",   # 20 Uttara Ashadha
    "Monkey (Vanar)",     # 21 Shravana
    "Lion (Simha)",       # 22 Dhanishta
    "Horse (Ashwa)",      # 23 Shatabhisha
    "Lion (Simha)",       # 24 Purva Bhadrapada
    "Cow (Gau)",          # 25 Uttara Bhadrapada
    "Elephant (Gaja)",    # 26 Revati
]

# Gana by nakshatra index
_DEVA_INDICES = {0, 1, 4, 6, 7, 12, 14, 21, 26}
_MANUSHYA_INDICES = {2, 3, 5, 10, 11, 16, 17, 19, 22}
_RAKSHASA_INDICES = {8, 9, 13, 15, 18, 20, 23, 24, 25}

# Nadi by nakshatra index
_AADI_INDICES = {0, 5, 6, 11, 12, 17, 18, 23, 24}
_MADHYA_INDICES = {1, 4, 7, 10, 13, 16, 19, 22, 25}
_ANTYA_INDICES = {2, 3, 8, 9, 14, 15, 20, 21, 26}

# Varna (social class) by Moon sign
# Fire signs (Aries, Leo, Sagittarius) = Kshatriya
# Earth signs (Taurus, Virgo, Capricorn) = Vaishya
# Air signs (Gemini, Libra, Aquarius) = Shudra
# Water signs (Cancer, Scorpio, Pisces) = Brahmin
VARNA_BY_SIGN = {
    "Aries": "Kshatriya", "Taurus": "Vaishya", "Gemini": "Shudra",
    "Cancer": "Brahmin", "Leo": "Kshatriya", "Virgo": "Vaishya",
    "Libra": "Shudra", "Scorpio": "Brahmin", "Sagittarius": "Kshatriya",
    "Capricorn": "Vaishya", "Aquarius": "Shudra", "Pisces": "Brahmin",
}

# 27 Yogas
YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

# 11 Karanas — 7 moveable (Chara) + 4 fixed (Sthira)
MOVEABLE_KARANAS = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",
]
FIXED_KARANAS = ["Shakuni", "Chatushpada", "Nagava", "Kimstughna"]

# Naamakshar (representative first syllable per nakshatra)
NAAMAKSHAR_BY_NAKSHATRA = [
    ["Chu", "Che", "Cho", "La"],     # Ashwini
    ["Li", "Lu", "Le", "Lo"],         # Bharani
    ["A", "I", "U", "E"],             # Krittika
    ["O", "Va", "Vi", "Vu"],          # Rohini
    ["Ve", "Vo", "Ka", "Ki"],         # Mrigashira
    ["Ku", "Gha", "Ng", "Chha"],      # Ardra
    ["Ke", "Ko", "Ha", "Hi"],         # Punarvasu
    ["Hu", "He", "Ho", "Da"],         # Pushya
    ["Di", "Du", "De", "Do"],         # Ashlesha
    ["Ma", "Mi", "Mu", "Me"],         # Magha
    ["Mo", "Ta", "Ti", "Tu"],         # Purva Phalguni
    ["Te", "To", "Pa", "Pi"],         # Uttara Phalguni
    ["Pu", "Sha", "Na", "Tha"],       # Hasta
    ["Pe", "Po", "Ra", "Ri"],         # Chitra
    ["Ru", "Re", "Ro", "Ta"],         # Swati
    ["Ti", "Tu", "Te", "To"],         # Vishakha
    ["Na", "Ni", "Nu", "Ne"],         # Anuradha
    ["No", "Ya", "Yi", "Yu"],         # Jyeshtha
    ["Ye", "Yo", "Bha", "Bhi"],       # Mula
    ["Bhu", "Dha", "Pha", "Dha"],     # Purva Ashadha
    ["Bhe", "Bho", "Ja", "Ji"],       # Uttara Ashadha
    ["Ju/Khi", "Je/Khu", "Jo/Khe", "Gha/Kho"],  # Shravana
    ["Ga", "Gi", "Gu", "Ge"],         # Dhanishta
    ["Go", "Sa", "Si", "Su"],         # Shatabhisha
    ["Se", "So", "Da", "Di"],         # Purva Bhadrapada
    ["Du", "Tha", "Jha", "Da"],       # Uttara Bhadrapada
    ["De", "Do", "Cha", "Chi"],       # Revati
]

# Tithi lords — cycling Sun through Saturn for each of 30 tithis
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

TITHI_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Vaar (weekday) lords — Python weekday: 0=Monday
VAAR_NAMES = {
    0: "Somvar", 1: "Mangalvar", 2: "Budhvar", 3: "Guruvar",
    4: "Shukravar", 5: "Shanivar", 6: "Ravivar",
}
VAAR_LORDS = {
    0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter",
    4: "Venus", 5: "Saturn", 6: "Sun",
}

# Paya by Nakshatra group (0-indexed nakshatra)
# Group of 9: nakshatras 0-8 = Gold, 9-17 = Silver, 18-26 = Copper
PAYA_NAKSHATRA_MAP = {
    "Gold (Swarna)": list(range(0, 9)),
    "Silver (Rajat)": list(range(9, 18)),
    "Copper (Tamra)": list(range(18, 27)),
}

# Paya by Moon sign element
PAYA_CHANDRA_MAP = {
    "Gold (Swarna)": ["Aries", "Leo", "Sagittarius"],       # Fire
    "Silver (Rajat)": ["Taurus", "Virgo", "Capricorn"],     # Earth
    "Copper (Tamra)": ["Gemini", "Libra", "Aquarius"],      # Air
    "Iron (Loha)": ["Cancer", "Scorpio", "Pisces"],         # Water
}

# Western Sun signs by degree range
WESTERN_SIGNS = [
    (0, 30, "Aries"), (30, 60, "Taurus"), (60, 90, "Gemini"),
    (90, 120, "Cancer"), (120, 150, "Leo"), (150, 180, "Virgo"),
    (180, 210, "Libra"), (210, 240, "Scorpio"), (240, 270, "Sagittarius"),
    (270, 300, "Capricorn"), (300, 330, "Aquarius"), (330, 360, "Pisces"),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _get_nakshatra_index(longitude: float) -> int:
    """Get nakshatra index (0-26) from sidereal longitude."""
    return int((longitude % 360.0) / NAKSHATRA_SPAN)


def _get_pada(longitude: float) -> int:
    """Get pada (1-4) from sidereal longitude."""
    within_nakshatra = (longitude % 360.0) % NAKSHATRA_SPAN
    pada_span = NAKSHATRA_SPAN / 4.0
    return int(within_nakshatra / pada_span) + 1


def _get_gana(nakshatra_idx: int) -> str:
    """Get Gana from nakshatra index."""
    if nakshatra_idx in _DEVA_INDICES:
        return "Deva"
    elif nakshatra_idx in _MANUSHYA_INDICES:
        return "Manushya"
    else:
        return "Rakshasa"


def _get_nadi(nakshatra_idx: int) -> str:
    """Get Nadi from nakshatra index."""
    if nakshatra_idx in _AADI_INDICES:
        return "Aadi"
    elif nakshatra_idx in _MADHYA_INDICES:
        return "Madhya"
    else:
        return "Antya"


def _get_western_sign(longitude: float) -> str:
    """Get western zodiac sign from tropical longitude."""
    # Use the sidereal longitude as approximation (Ayanamsa ~24 degrees)
    # For simplicity, we map based on degree ranges
    deg = longitude % 360.0
    for start, end, sign in WESTERN_SIGNS:
        if start <= deg < end:
            return sign
    return "Pisces"


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def calculate_avakhada(chart_data: dict, birth_date: str = "") -> dict:
    """
    Calculate Avakhada Chakra from chart_data.

    Args:
        chart_data: The full chart_data dict with 'planets' and 'ascendant' keys.
        birth_date: Birth date string "YYYY-MM-DD" for Vaar calculation.

    Returns:
        Dict with all Avakhada Chakra components.
    """
    planets = chart_data.get("planets", {})
    ascendant = chart_data.get("ascendant", {})

    # Get Moon data
    moon = planets.get("Moon", {})
    moon_longitude = moon.get("longitude", 0.0)
    moon_sign = moon.get("sign", "Aries")

    # Get Sun data
    sun = planets.get("Sun", {})
    sun_longitude = sun.get("longitude", 0.0)
    sun_sign = sun.get("sign", "Aries")

    # Ascendant
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    asc_lord = SIGN_LORD.get(asc_sign, "Unknown")

    # Moon sign lord
    moon_sign_lord = SIGN_LORD.get(moon_sign, "Unknown")

    # Nakshatra and Pada from Moon
    nakshatra_idx = _get_nakshatra_index(moon_longitude)
    nakshatra_name = NAKSHATRAS[nakshatra_idx] if 0 <= nakshatra_idx < 27 else "Unknown"
    pada = _get_pada(moon_longitude)

    # Yoga: index = floor((sun_long + moon_long) / 13.333) % 27
    yoga_index = int((sun_longitude + moon_longitude) / NAKSHATRA_SPAN) % 27
    yoga_name = YOGA_NAMES[yoga_index]

    # Karana: each karana = 6 degrees of Moon-Sun elongation, 60 karanas per cycle
    # Index 0 = Kimstughna, indices 1-56 = 7 moveable karanas cycling, 57-59 = fixed
    diff = (moon_longitude - sun_longitude) % 360.0
    karana_index = int(diff / 6.0) % 60
    if karana_index == 0:
        karana_name = "Kimstughna"
    elif karana_index <= 56:
        karana_name = MOVEABLE_KARANAS[(karana_index - 1) % 7]
    else:
        karana_name = FIXED_KARANAS[karana_index - 57]

    # Yoni
    yoni = YONI_BY_NAKSHATRA[nakshatra_idx] if 0 <= nakshatra_idx < 27 else "Unknown"

    # Gana
    gana = _get_gana(nakshatra_idx)

    # Nadi
    nadi = _get_nadi(nakshatra_idx)

    # Varna
    varna = VARNA_BY_SIGN.get(moon_sign, "Unknown")

    # Naamakshar
    if 0 <= nakshatra_idx < 27 and 1 <= pada <= 4:
        syllables = NAAMAKSHAR_BY_NAKSHATRA[nakshatra_idx]
        naamakshar = syllables[pada - 1]
    else:
        naamakshar = "N/A"

    # Sun Sign (Western)
    sun_western_sign = _get_western_sign(sun_longitude)

    # --- NEW: Tithi + Tithi Lord ---
    tithi_index = int(diff / 12.0) % 30  # diff already = (moon - sun) % 360
    tithi_name = TITHI_NAMES[tithi_index] if 0 <= tithi_index < 30 else "Unknown"
    tithi_paksha = "Shukla" if tithi_index < 15 else "Krishna"
    tithi_lord = TITHI_LORDS[tithi_index % 7]

    # --- NEW: Vaar (day of week + lord) ---
    vaar_name = ""
    vaar_lord = ""
    if birth_date:
        try:
            from datetime import datetime as _dt
            bd = _dt.strptime(str(birth_date).split("T")[0].split(" ")[0], "%Y-%m-%d")
            weekday = bd.weekday()  # 0=Monday
            vaar_name = VAAR_NAMES.get(weekday, "")
            vaar_lord = VAAR_LORDS.get(weekday, "")
        except Exception as e:
            print(f"ERROR in calculate_avakhada (vaar calculation): {e}")
            print(traceback.format_exc())

    # --- NEW: Paya (Nakshatra-based) ---
    paya_nakshatra = "Unknown"
    for paya_label, indices in PAYA_NAKSHATRA_MAP.items():
        if nakshatra_idx in indices:
            paya_nakshatra = paya_label
            break

    # --- NEW: Paya (Chandra / Moon sign element) ---
    paya_chandra = "Unknown"
    for paya_label, signs in PAYA_CHANDRA_MAP.items():
        if moon_sign in signs:
            paya_chandra = paya_label
            break

    return {
        "ascendant": asc_sign,
        "ascendant_lord": asc_lord,
        "rashi": moon_sign,
        "rashi_lord": moon_sign_lord,
        "nakshatra": nakshatra_name,
        "nakshatra_pada": pada,
        "yoga": yoga_name,
        "karana": karana_name,
        "yoni": yoni,
        "gana": gana,
        "nadi": nadi,
        "varna": varna,
        "naamakshar": naamakshar,
        "sun_sign": sun_western_sign,
        "moon_degree": round(moon_longitude % 360.0, 2),
        "sun_degree": round(sun_longitude % 360.0, 2),
        # New Avakhada fields
        "tithi": tithi_name,
        "tithi_paksha": tithi_paksha,
        "tithi_lord": tithi_lord,
        "vaar": vaar_name,
        "vaar_lord": vaar_lord,
        "paya_nakshatra": paya_nakshatra,
        "paya_chandra": paya_chandra,
    }
