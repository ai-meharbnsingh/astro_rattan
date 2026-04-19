"""
avakhada_engine.py — Avakhada Chakra Calculation Engine
========================================================
Computes the comprehensive birth summary table (Avakhada Chakra)
from chart data: ascendant, Moon position, Sun position, and planet data.
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

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
_DEVA_INDICES = {0, 4, 6, 7, 12, 14, 16, 21, 26}
_MANUSHYA_INDICES = {1, 3, 5, 10, 11, 19, 20, 24, 25}
_RAKSHASA_INDICES = {2, 8, 9, 13, 15, 17, 18, 22, 23}

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

# Nakshatra lords by index (Vimshottari sequence)
NAKSHATRA_LORD_BY_INDEX = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury",
]

# Lucky Metal by nakshatra lord
LUCKY_METAL = {
    "Sun": "Gold", "Moon": "Silver", "Mars": "Copper",
    "Mercury": "Bronze", "Jupiter": "Gold", "Venus": "Silver",
    "Saturn": "Iron", "Rahu": "Lead", "Ketu": "Iron",
}

# Evil Numbers by nakshatra lord (classical reference — lord's enemy numbers)
EVIL_NUMBERS_BY_NAK_LORD = {
    "Sun": [8], "Moon": [4], "Mars": [6, 5],
    "Mercury": [9, 1], "Jupiter": [6, 8], "Venus": [1, 8],
    "Saturn": [1, 4], "Rahu": [9, 1], "Ketu": [6, 5],
}

# Good Numbers by nakshatra lord
GOOD_NUMBERS_BY_NAK_LORD = {
    "Sun": [1, 4, 5], "Moon": [2, 7, 9], "Mars": [3, 9, 1],
    "Mercury": [5, 4, 6], "Jupiter": [3, 1, 9], "Venus": [6, 2, 7],
    "Saturn": [8, 5, 6], "Rahu": [4, 7, 8], "Ketu": [7, 9, 3],
}

# Lucky Number (primary) = nakshatra lord's number
LUCKY_NUMBER_BY_NAK_LORD = {
    "Sun": 1, "Moon": 2, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 6, "Saturn": 8, "Rahu": 4, "Ketu": 7,
}

# Friendly Signs per lagna sign
FRIENDLY_SIGNS = {
    "Aries": ["Leo", "Sagittarius", "Scorpio"],
    "Taurus": ["Virgo", "Capricorn", "Libra"],
    "Gemini": ["Libra", "Aquarius", "Virgo"],
    "Cancer": ["Scorpio", "Pisces", "Sagittarius"],
    "Leo": ["Aries", "Sagittarius", "Scorpio"],
    "Virgo": ["Taurus", "Capricorn", "Gemini"],
    "Libra": ["Gemini", "Aquarius", "Taurus"],
    "Scorpio": ["Cancer", "Pisces", "Aries"],
    "Sagittarius": ["Aries", "Leo", "Cancer"],
    "Capricorn": ["Taurus", "Virgo", "Aquarius"],
    "Aquarius": ["Gemini", "Libra", "Capricorn"],
    "Pisces": ["Cancer", "Scorpio", "Sagittarius"],
}

# Good Lagna (auspicious lagna for important tasks)
GOOD_LAGNA = {
    "Aries": ["Sagittarius", "Leo"],
    "Taurus": ["Capricorn", "Virgo"],
    "Gemini": ["Aquarius", "Libra"],
    "Cancer": ["Pisces", "Scorpio"],
    "Leo": ["Aries", "Sagittarius"],
    "Virgo": ["Taurus", "Capricorn"],
    "Libra": ["Gemini", "Aquarius"],
    "Scorpio": ["Cancer", "Pisces"],
    "Sagittarius": ["Leo", "Aries"],
    "Capricorn": ["Virgo", "Taurus"],
    "Aquarius": ["Libra", "Gemini"],
    "Pisces": ["Scorpio", "Cancer"],
}

# Lucky Days by nakshatra lord
LUCKY_DAYS = {
    "Sun": ["Sunday"], "Moon": ["Monday"], "Mars": ["Tuesday", "Thursday"],
    "Mercury": ["Wednesday", "Thursday"], "Jupiter": ["Thursday", "Tuesday"],
    "Venus": ["Friday", "Wednesday"], "Saturn": ["Saturday", "Thursday"],
    "Rahu": ["Saturday", "Wednesday"], "Ketu": ["Tuesday", "Thursday"],
}

# Good Planets (friendly planets for the nakshatra lord)
GOOD_PLANETS = {
    "Sun": ["Jupiter", "Mars", "Moon"], "Moon": ["Sun", "Mercury", "Jupiter"],
    "Mars": ["Sun", "Moon", "Jupiter"], "Mercury": ["Venus", "Saturn", "Rahu"],
    "Jupiter": ["Sun", "Moon", "Mars"], "Venus": ["Mercury", "Saturn", "Rahu"],
    "Saturn": ["Mercury", "Venus", "Rahu"], "Rahu": ["Venus", "Saturn", "Mercury"],
    "Ketu": ["Mars", "Jupiter", "Sun"],
}

# ============================================================
# GHATAK (MALEFICS) TABLE
# ============================================================
# 9 groups of 3 nakshatras each. Group index = nakshatra_index // 3.
# Each group shares the same Ghatak (inauspicious) indicators.

GHATAK_TABLE = {
    # Group 0: Ashwini / Bharani / Krittika
    0: {
        "bad_day": "Saturday", "bad_karan": "Vishti",
        "bad_lagna": "Aquarius", "bad_month": "Magha",
        "bad_nakshatra": "Dhanishta", "bad_prahar": 1,
        "bad_rasi": "Aquarius",
        "bad_tithi": [4, 9, 14], "bad_yoga": "Vishkambha",
        "bad_planets": ["Saturn"],
    },
    # Group 1: Rohini / Mrigashira / Ardra
    1: {
        "bad_day": "Friday", "bad_karan": "Garaja",
        "bad_lagna": "Capricorn", "bad_month": "Paush",
        "bad_nakshatra": "Shravana", "bad_prahar": 2,
        "bad_rasi": "Capricorn",
        "bad_tithi": [2, 7, 12], "bad_yoga": "Harshana",
        "bad_planets": ["Saturn"],
    },
    # Group 2: Punarvasu / Pushya / Ashlesha
    2: {
        "bad_day": "Wednesday", "bad_karan": "Balava",
        "bad_lagna": "Sagittarius", "bad_month": "Ashwin",
        "bad_nakshatra": "Mula", "bad_prahar": 3,
        "bad_rasi": "Sagittarius",
        "bad_tithi": [3, 8, 13], "bad_yoga": "Vajra",
        "bad_planets": ["Jupiter"],
    },
    # Group 3: Magha / Purva Phalguni / Uttara Phalguni
    3: {
        "bad_day": "Tuesday", "bad_karan": "Kaulava",
        "bad_lagna": "Scorpio", "bad_month": "Bhadrapada",
        "bad_nakshatra": "Jyeshtha", "bad_prahar": 4,
        "bad_rasi": "Scorpio",
        "bad_tithi": [1, 6, 11], "bad_yoga": "Parigha",
        "bad_planets": ["Mars"],
    },
    # Group 4: Hasta / Chitra / Swati
    4: {
        "bad_day": "Monday", "bad_karan": "Taitila",
        "bad_lagna": "Libra", "bad_month": "Shravana",
        "bad_nakshatra": "Vishakha", "bad_prahar": 1,
        "bad_rasi": "Libra",
        "bad_tithi": [5, 10, 15], "bad_yoga": "Siddhi",
        "bad_planets": ["Venus"],
    },
    # Group 5: Vishakha / Anuradha / Jyeshtha
    5: {
        "bad_day": "Sunday", "bad_karan": "Vanija",
        "bad_lagna": "Virgo", "bad_month": "Ashadha",
        "bad_nakshatra": "Hasta", "bad_prahar": 2,
        "bad_rasi": "Virgo",
        "bad_tithi": [4, 9, 14], "bad_yoga": "Shula",
        "bad_planets": ["Mercury"],
    },
    # Group 6: Mula / Purva Ashadha / Uttara Ashadha
    6: {
        "bad_day": "Friday", "bad_karan": "Garaja",
        "bad_lagna": "Leo", "bad_month": "Jyeshtha",
        "bad_nakshatra": "Magha", "bad_prahar": 3,
        "bad_rasi": "Cancer",
        "bad_tithi": [2, 7, 12], "bad_yoga": "Atiganda",
        "bad_planets": ["Sun"],
    },
    # Group 7: Shravana / Dhanishta / Shatabhisha
    7: {
        "bad_day": "Thursday", "bad_karan": "Bava",
        "bad_lagna": "Cancer", "bad_month": "Vaishakha",
        "bad_nakshatra": "Pushya", "bad_prahar": 4,
        "bad_rasi": "Gemini",
        "bad_tithi": [3, 8, 13], "bad_yoga": "Vyatipata",
        "bad_planets": ["Moon"],
    },
    # Group 8: Purva Bhadrapada / Uttara Bhadrapada / Revati
    8: {
        "bad_day": "Wednesday", "bad_karan": "Vishti",
        "bad_lagna": "Aries", "bad_month": "Chaitra",
        "bad_nakshatra": "Ashwini", "bad_prahar": 1,
        "bad_rasi": "Pisces",
        "bad_tithi": [1, 6, 11], "bad_yoga": "Brahma",
        "bad_planets": ["Mercury"],
    },
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


def _get_nakshatra_lord(nakshatra_idx: int) -> str:
    """Get the Vimshottari lord for a nakshatra index (0-26)."""
    if 0 <= nakshatra_idx < 27:
        return NAKSHATRA_LORD_BY_INDEX[nakshatra_idx]
    return "Unknown"


def _compute_good_years(lucky_number: int) -> list:
    """
    Compute significant life years based on lucky number.
    Formula: multiples of lucky number that are common life milestones
    (up to age 100), plus nearby milestone markers.
    """
    if lucky_number < 1 or lucky_number > 9:
        return []
    years = sorted(set(
        n for n in range(lucky_number, 101, lucky_number)
        if n > 0
    ))
    return years


def _calculate_ghatak(nakshatra_index: int) -> dict:
    """
    Calculate Ghatak (malefic/inauspicious) indicators from birth nakshatra.

    The 27 nakshatras are divided into 9 groups of 3.
    Each group shares the same Ghatak data: bad day, karan, lagna,
    month, nakshatra, prahar, rasi, tithis, yoga, and planets.

    Args:
        nakshatra_index: Birth nakshatra index (0-26).

    Returns:
        Dict with all Ghatak fields, or empty dict if index is invalid.
    """
    if not (0 <= nakshatra_index < 27):
        logger.warning("Invalid nakshatra index %s for Ghatak calculation", nakshatra_index)
        return {}
    group = nakshatra_index // 3
    return GHATAK_TABLE.get(group, {})


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
            logger.error("Error in calculate_avakhada (vaar calculation): %s", e, exc_info=True)

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

    # --- Nakshatra Lord derived fields ---
    nak_lord = _get_nakshatra_lord(nakshatra_idx)
    lucky_metal = LUCKY_METAL.get(nak_lord, "Unknown")
    evil_numbers = EVIL_NUMBERS_BY_NAK_LORD.get(nak_lord, [])
    good_numbers = GOOD_NUMBERS_BY_NAK_LORD.get(nak_lord, [])
    lucky_number = LUCKY_NUMBER_BY_NAK_LORD.get(nak_lord, 0)
    good_years = _compute_good_years(lucky_number)
    lucky_days = LUCKY_DAYS.get(nak_lord, [])
    good_planets = GOOD_PLANETS.get(nak_lord, [])

    # --- Lagna-based fields ---
    friendly_signs = FRIENDLY_SIGNS.get(asc_sign, [])
    good_lagna = GOOD_LAGNA.get(asc_sign, [])

    # --- Ghatak (malefics) ---
    ghatak = _calculate_ghatak(nakshatra_idx)

    # Planets appearing in both good_planets and ghatak.bad_planets — classical ambiguity
    # (two independent systems: nakshatra-lord friendship vs nakshatra-group malefics)
    conflict_planets = [p for p in good_planets if p in ghatak.get("bad_planets", [])]

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
        # Nakshatra lord derived fields
        "nakshatra_lord": nak_lord,
        "lucky_metal": lucky_metal,
        "evil_numbers": evil_numbers,
        "good_numbers": good_numbers,
        "lucky_number": lucky_number,
        "good_years": good_years,
        "lucky_days": lucky_days,
        "good_planets": good_planets,
        "conflict_planets": conflict_planets,
        # Lagna-based fields
        "friendly_signs": friendly_signs,
        "good_lagna": good_lagna,
        # Ghatak (malefics)
        "ghatak": ghatak,
    }
