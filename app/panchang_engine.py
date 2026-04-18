"""
panchang_engine.py -- Production-Grade Vedic Panchang Engine
=============================================================
Swiss Ephemeris-powered panchang with accurate calculations for:
- Tithi, Nakshatra, Yoga, Karana with end times (binary search)
- Sunrise/Sunset/Moonrise/Moonset via Swiss Ephemeris
- Planetary positions (Navgraha) with Rashi
- Rahu Kaal, Gulika Kaal, Yamaganda Kaal
- Auspicious timings (Abhijit Muhurat, Brahma Muhurat)
- Hindu calendar (Vikram/Shaka Samvat, Maas, Ritu, Ayana)
- Choghadiya periods
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------- Try swisseph ----------
try:
    import swisseph as swe
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

from app.astro_engine import (
    _approx_sun_longitude,
    _approx_moon_longitude,
    _approx_ayanamsa,
    _datetime_to_jd,
    _parse_datetime,
    get_nakshatra_from_longitude,
    get_sign_from_longitude,
    PLANETS as PLANET_IDS,
    NAKSHATRAS as ASTRO_NAKSHATRAS,
    NAKSHATRA_SPAN as ASTRO_NAKSHATRA_SPAN,
    SE_SUN,
    SE_MOON,
    SE_MEAN_NODE,
)

# ============================================================
# HINDI NAME MAPPINGS
# ============================================================

NAKSHATRA_HINDI: Dict[str, str] = {
    "Ashwini": "अश्विनी",
    "Bharani": "भरणी",
    "Krittika": "कृत्तिका",
    "Rohini": "रोहिणी",
    "Mrigashira": "मृगशिरा",
    "Ardra": "आर्द्रा",
    "Punarvasu": "पुनर्वसु",
    "Pushya": "पुष्य",
    "Ashlesha": "आश्लेषा",
    "Magha": "मघा",
    "Purva Phalguni": "पूर्व फाल्गुनी",
    "Uttara Phalguni": "उत्तर फाल्गुनी",
    "Hasta": "हस्त",
    "Chitra": "चित्रा",
    "Swati": "स्वाती",
    "Vishakha": "विशाखा",
    "Anuradha": "अनुराधा",
    "Jyeshtha": "ज्येष्ठा",
    "Mula": "मूल",
    "Purva Ashadha": "पूर्वाषाढ़ा",
    "Uttara Ashadha": "उत्तराषाढ़ा",
    "Shravana": "श्रवण",
    "Dhanishta": "धनिष्ठा",
    "Shatabhisha": "शतभिषा",
    "Purva Bhadrapada": "पूर्व भाद्रपद",
    "Uttara Bhadrapada": "उत्तर भाद्रपद",
    "Revati": "रेवती",
}

# ============================================================
# NAKSHATRA CATEGORY (Muhurta Chintamani, Ch. 2)
# 7 types: Sthira, Chara, Ugra, Mishra, Laghu, Mridu, Tikshna
# ============================================================
NAKSHATRA_CATEGORY: Dict[str, str] = {
    # Sthira (Fixed) — permanent works, building, marriage, planting
    "Rohini": "sthira", "Uttara Phalguni": "sthira",
    "Uttara Ashadha": "sthira", "Uttara Bhadrapada": "sthira",
    # Chara (Movable) — travel, journeys, vehicles
    "Punarvasu": "chara", "Swati": "chara",
    "Shravana": "chara", "Dhanishta": "chara", "Shatabhisha": "chara",
    # Ugra (Fierce) — legal battles, aggressive acts, warfare
    "Bharani": "ugra", "Magha": "ugra",
    "Purva Phalguni": "ugra", "Purva Ashadha": "ugra", "Purva Bhadrapada": "ugra",
    # Mishra (Mixed) — moderate activities, mixed outcomes
    "Krittika": "mishra", "Vishakha": "mishra",
    # Laghu (Light/Swift) — medicine, crafts, quick tasks, commerce
    "Ashwini": "laghu", "Pushya": "laghu", "Hasta": "laghu",
    # Mridu (Soft/Tender) — arts, music, romance, friendship
    "Mrigashira": "mridu", "Chitra": "mridu",
    "Anuradha": "mridu", "Revati": "mridu",
    # Tikshna (Sharp/Fierce) — surgery, separation, enemies
    "Ardra": "tikshna", "Ashlesha": "tikshna",
    "Jyeshtha": "tikshna", "Mula": "tikshna",
}

NAKSHATRA_CATEGORY_DATA: Dict[str, Dict[str, str]] = {
    "sthira": {
        "en": "Sthira", "hi": "स्थिर",
        "good_for_en": "Building, marriage, permanent works",
        "good_for_hi": "निर्माण, विवाह, स्थायी कार्य",
        "color": "blue",
    },
    "chara": {
        "en": "Chara", "hi": "चर",
        "good_for_en": "Travel, vehicles, journeys",
        "good_for_hi": "यात्रा, वाहन, प्रवास",
        "color": "green",
    },
    "ugra": {
        "en": "Ugra", "hi": "उग्र",
        "good_for_en": "Legal, warfare, aggressive acts",
        "good_for_hi": "विवाद, युद्ध, उग्र कार्य",
        "color": "red",
    },
    "mishra": {
        "en": "Mishra", "hi": "मिश्र",
        "good_for_en": "Moderate activities, mixed outcomes",
        "good_for_hi": "सामान्य कार्य, मिश्रित फल",
        "color": "purple",
    },
    "laghu": {
        "en": "Laghu", "hi": "लघु",
        "good_for_en": "Medicine, crafts, commerce, quick tasks",
        "good_for_hi": "चिकित्सा, शिल्प, व्यापार, शीघ्र कार्य",
        "color": "teal",
    },
    "mridu": {
        "en": "Mridu", "hi": "मृदु",
        "good_for_en": "Arts, music, romance, friendship",
        "good_for_hi": "कला, संगीत, प्रेम, मित्रता",
        "color": "pink",
    },
    "tikshna": {
        "en": "Tikshna", "hi": "तीक्ष्ण",
        "good_for_en": "Surgery, separation, enemy work",
        "good_for_hi": "शल्य, विच्छेद, शत्रु कार्य",
        "color": "orange",
    },
}

RASHI_HINDI: Dict[str, str] = {
    "Aries": "मेष",
    "Taurus": "वृषभ",
    "Gemini": "मिथुन",
    "Cancer": "कर्क",
    "Leo": "सिंह",
    "Virgo": "कन्या",
    "Libra": "तुला",
    "Scorpio": "वृश्चिक",
    "Sagittarius": "धनु",
    "Capricorn": "मकर",
    "Aquarius": "कुम्भ",
    "Pisces": "मीन",
}

PLANET_HINDI: Dict[str, str] = {
    "Sun": "सूर्य",
    "Moon": "चन्द्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "बृहस्पति",
    "Venus": "शुक्र",
    "Saturn": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
}

# Combustion orbs (degrees from Sun)
COMBUSTION_ORBS: Dict[str, float] = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,
    "Jupiter": 11.0,
    "Venus": 10.0,
    "Saturn": 15.0,
}

# Reduced combustion orbs when planet is retrograde
COMBUSTION_ORBS_RETROGRADE: Dict[str, float] = {
    "Mercury": 12.0,
    "Venus": 8.0,
}

# ============================================================
# TITHIS -- 30 tithis in a lunar month
# ============================================================
TITHIS: List[Dict[str, Any]] = [
    {"number": 1,  "name": "Pratipada",    "paksha": "Shukla"},
    {"number": 2,  "name": "Dwitiya",      "paksha": "Shukla"},
    {"number": 3,  "name": "Tritiya",      "paksha": "Shukla"},
    {"number": 4,  "name": "Chaturthi",    "paksha": "Shukla"},
    {"number": 5,  "name": "Panchami",     "paksha": "Shukla"},
    {"number": 6,  "name": "Shashthi",     "paksha": "Shukla"},
    {"number": 7,  "name": "Saptami",      "paksha": "Shukla"},
    {"number": 8,  "name": "Ashtami",      "paksha": "Shukla"},
    {"number": 9,  "name": "Navami",       "paksha": "Shukla"},
    {"number": 10, "name": "Dashami",      "paksha": "Shukla"},
    {"number": 11, "name": "Ekadashi",     "paksha": "Shukla"},
    {"number": 12, "name": "Dwadashi",     "paksha": "Shukla"},
    {"number": 13, "name": "Trayodashi",   "paksha": "Shukla"},
    {"number": 14, "name": "Chaturdashi",  "paksha": "Shukla"},
    {"number": 15, "name": "Purnima",      "paksha": "Shukla"},
    {"number": 16, "name": "Pratipada",    "paksha": "Krishna"},
    {"number": 17, "name": "Dwitiya",      "paksha": "Krishna"},
    {"number": 18, "name": "Tritiya",      "paksha": "Krishna"},
    {"number": 19, "name": "Chaturthi",    "paksha": "Krishna"},
    {"number": 20, "name": "Panchami",     "paksha": "Krishna"},
    {"number": 21, "name": "Shashthi",     "paksha": "Krishna"},
    {"number": 22, "name": "Saptami",      "paksha": "Krishna"},
    {"number": 23, "name": "Ashtami",      "paksha": "Krishna"},
    {"number": 24, "name": "Navami",       "paksha": "Krishna"},
    {"number": 25, "name": "Dashami",      "paksha": "Krishna"},
    {"number": 26, "name": "Ekadashi",     "paksha": "Krishna"},
    {"number": 27, "name": "Dwadashi",     "paksha": "Krishna"},
    {"number": 28, "name": "Trayodashi",   "paksha": "Krishna"},
    {"number": 29, "name": "Chaturdashi",  "paksha": "Krishna"},
    {"number": 30, "name": "Amavasya",     "paksha": "Krishna"},
]

# ============================================================
# YOGAS -- 27 yogas
# ============================================================
YOGAS: List[str] = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

YOGA_INTERPRETATIONS: List[Dict[str, str]] = [
    {"en": "Obstacle-causing, avoid new starts. Inauspicious.", "hi": "बाधाएँ उत्पन्न करने वाला, नए कार्यों से बचें। अशुभ।"},
    {"en": "Love and affection, good for social ceremonies.", "hi": "प्रेम और स्नेह, सामाजिक समारोहों के लिए उत्तम।"},
    {"en": "Longevity, good for health and longevity rites.", "hi": "दीर्घायु, स्वास्थ्य और आयुष्य कर्मों के लिए शुभ।"},
    {"en": "Good fortune, excellent for auspicious work.", "hi": "सौभाग्य, शुभ कार्यों के लिए उत्तम।"},
    {"en": "Splendor, very auspicious for all ceremonies.", "hi": "तेज, सभी समारोहों के लिए अत्यंत शुभ।"},
    {"en": "Great danger, avoid important beginnings.", "hi": "महान खतरा, महत्वपूर्ण प्रारंभ से बचें।"},
    {"en": "Good deeds, auspicious for virtuous acts.", "hi": "शुभ कर्म, पुण्य कार्यों के लिए शुभ।"},
    {"en": "Steadfastness, good for fixed/immovable works.", "hi": "दृढ़ता, स्थिर और अचल कार्यों के लिए शुभ।"},
    {"en": "Pain/thorn, inauspicious, avoid travel and new starts.", "hi": "पीड़ा/कांटा, अशुभ, यात्रा और नए प्रारंभ से बचें।"},
    {"en": "Danger, inauspicious for all ceremonies.", "hi": "खतरा, सभी समारोहों के लिए अशुभ।"},
    {"en": "Growth, good for business and expansion.", "hi": "वृद्धि, व्यापार और विस्तार के लिए शुभ।"},
    {"en": "Fixed/constant, excellent for permanent works.", "hi": "स्थिर/निश्चल, स्थायी कार्यों के लिए उत्तम।"},
    {"en": "Obstruction, avoid new beginnings.", "hi": "बाधा, नए प्रारंभ से बचें।"},
    {"en": "Joy, auspicious for celebrations and social events.", "hi": "आनंद, उत्सवों और सामाजिक कार्यक्रमों के लिए शुभ।"},
    {"en": "Thunderbolt, mixed — good for aggressive acts, bad for gentle ceremonies.", "hi": "वज्र, मिश्र — आक्रामक कार्यों के लिए शुभ, कोमल समारोहों के लिए अशुभ।"},
    {"en": "Success, very auspicious for all work.", "hi": "सफलता, सभी कार्यों के लिए अत्यंत शुभ।"},
    {"en": "Calamity, EXTREMELY inauspicious — blocks ALL activity.", "hi": "आपदा, अत्यंत अशुभ — सभी गतिविधियाँ रुक जाती हैं।"},
    {"en": "Luxury/comfort, good for enjoyment, not for austerity.", "hi": "विलास/आराम, भोग के लिए शुभ, तपस्या के लिए नहीं।"},
    {"en": "Obstacle, inauspicious for new beginnings.", "hi": "बाधा, नए प्रारंभ के लिए अशुभ।"},
    {"en": "Auspicious, excellent for spiritual and auspicious work.", "hi": "शुभ, आध्यात्मिक और शुभ कार्यों के लिए उत्तम।"},
    {"en": "Accomplished, very favorable for all activities.", "hi": "सिद्ध, सभी गतिविधियों के लिए अत्यंत अनुकूल।"},
    {"en": "Achievable, good for efforts and endeavors.", "hi": "साध्य, प्रयासों और उद्यमों के लिए शुभ।"},
    {"en": "Auspicious, favorable for all ceremonies.", "hi": "शुभ, सभी समारोहों के लिए अनुकूल।"},
    {"en": "Bright/pure, excellent for all auspicious work.", "hi": "शुद्ध/स्वच्छ, सभी शुभ कार्यों के लिए उत्तम।"},
    {"en": "Creator, very auspicious for sacred ceremonies.", "hi": "सृष्टिकर्ता, पवित्र समारोहों के लिए अत्यंत शुभ।"},
    {"en": "Lord of gods, highly auspicious for all work.", "hi": "देवताओं के स्वामी, सभी कार्यों के लिए अत्यंत शुभ।"},
    {"en": "Unsupported, EXTREMELY inauspicious — blocks ALL activity.", "hi": "असहाय/अनावृत, अत्यंत अशुभ — सभी गतिविधियाँ रुक जाती हैं।"},
]

YOGA_SPAN = 360.0 / 27.0  # ~13.3333 degrees

# ============================================================
# CHANDRABALAM — Classical fruit per house from birth Moon
# ============================================================
_CHANDRABALAM_TEXT: List[Dict[str, str]] = [
    # Index 0 = House 1
    {"en": "Indifferent — neither strong gain nor loss. Maintain status quo.", "hi": "उदासीन — न लाभ न हानि। स्थिति बनाए रखें।"},
    {"en": "Wealth loss possible — avoid major financial decisions.", "hi": "धन हानि संभव — बड़े वित्तीय निर्णय टालें।"},
    {"en": "Gain and courage — good for enterprise and effort.", "hi": "लाभ और साहस — उद्यम और परिश्रम के लिए शुभ।"},
    {"en": "Anxiety and discomfort — mental stress, postpone important work.", "hi": "चिंता और असुविधा — मानसिक तनाव, महत्वपूर्ण कार्य टालें।"},
    {"en": "Mixed results — some pleasure but instability.", "hi": "मिश्र परिणाम — कुछ सुख पर अस्थिरता।"},
    {"en": "Victory over enemies — good for competition and health recovery.", "hi": "शत्रु पर विजय — प्रतिस्पर्धा और स्वास्थ्य लाभ के लिए शुभ।"},
    {"en": "Good for relationships and partnerships — auspicious.", "hi": "संबंधों और साझेदारी के लिए अच्छा — शुभ।"},
    {"en": "Danger and physical weakness — worst position. Avoid all new starts.", "hi": "खतरा और शारीरिक कमजोरी — सबसे खराब स्थिति। नए कार्य वर्जित।"},
    {"en": "Mixed — spiritual growth good, material matters uncertain.", "hi": "मिश्र — आध्यात्मिक विकास अच्छा, भौतिक मामले अनिश्चित।"},
    {"en": "Success in work and career — excellent for professional efforts.", "hi": "कार्य और करियर में सफलता — पेशेवर प्रयासों के लिए उत्तम।"},
    {"en": "Gain of wealth and fulfillment — best position for gains.", "hi": "धन लाभ और पूर्ति — लाभ के लिए सर्वोत्तम स्थिति।"},
    {"en": "Loss and expenses — avoid commitments, rest instead.", "hi": "हानि और व्यय — प्रतिबद्धताएँ टालें, विश्राम करें।"},
]

# ============================================================
# TARA BALAM — Classical interpretation per tara position
# ============================================================
_TARA_BALAM_TEXT: Dict[str, Dict[str, str]] = {
    "Janma": {
        "en": "Danger to body, worry, mental stress. Avoid major beginnings.",
        "hi": "शरीर को खतरा, चिंता, मानसिक तनाव। बड़े प्रारंभ से बचें।",
    },
    "Sampat": {
        "en": "Wealth and prosperity. Excellent for financial activities.",
        "hi": "धन और समृद्धि। वित्तीय गतिविधियों के लिए उत्तम।",
    },
    "Vipat": {
        "en": "Dangers, losses, accidents, disputes. Highly inauspicious.",
        "hi": "खतरे, हानि, दुर्घटना, विवाद। अत्यंत अशुभ।",
    },
    "Kshema": {
        "en": "Prosperity, well-being, gains in business. Very favorable.",
        "hi": "समृद्धि, कल्याण, व्यापार में लाभ। अत्यंत अनुकूल।",
    },
    "Pratyari": {
        "en": "Obstacles, harm to work, opposition. Proceed with caution.",
        "hi": "बाधाएँ, कार्य को हानि, विरोध। सावधानी से आगे बढ़ें।",
    },
    "Sadhaka": {
        "en": "Realization of ambitions, happiness, achievement. Auspicious.",
        "hi": "महत्वाकांक्षाओं की पूर्ति, सुख, सफलता। शुभ।",
    },
    "Vadha": {
        "en": "Destruction, monetary loss, dangers. Avoid all new work.",
        "hi": "विनाश, धन हानि, खतरे। सभी नए कार्य वर्जित।",
    },
    "Mitra": {
        "en": "Friendship, good happiness, harmony. Favorable for all.",
        "hi": "मित्रता, सुख, सामंजस्य। सभी के लिए अनुकूल।",
    },
    "Ati-Mitra": {
        "en": "Great friend, very favorable, excellent for all beginnings.",
        "hi": "परम मित्र, अत्यंत अनुकूल, सभी प्रारंभों के लिए उत्तम।",
    },
}

# ============================================================
# KARANAS -- 11 karana types (cycle: 7 repeating + 4 fixed)
# ============================================================
_REPEATING_KARANAS: List[str] = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",
]
_FIXED_KARANAS: List[str] = [
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]

KARANAS: List[str] = _REPEATING_KARANAS + _FIXED_KARANAS

# Yoga quality classification (Muhurta Chintamani — Yoga Dosha list)
_BAD_YOGA_NUMBERS: set = {1, 8, 17, 24, 27}  # Vishkambha, Shoola(?), Vyatipata, Vajra, Vaidhriti

# Karana quality classification
_VISHTI_NAMES: set = {"Vishti", "Bhadra"}
# Chara (moveable) karanas cycle repeatedly; Sthira (fixed) karanas are the 4 fixed ones
_CHARA_KARANA_NAMES: set = {"Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"}


# ============================================================
# RAHU KAAL / GULIKA / YAMAGANDA timing by weekday
# ============================================================
# Slot number (1-8) for each weekday (0=Monday ... 6=Sunday)
_RAHU_KAAL_SLOT = {
    0: 2,  # Monday
    1: 7,  # Tuesday
    2: 5,  # Wednesday
    3: 6,  # Thursday
    4: 4,  # Friday
    5: 3,  # Saturday
    6: 8,  # Sunday
}

_GULIKA_KAAL_SLOT = {
    0: 6,  # Monday
    1: 5,  # Tuesday
    2: 4,  # Wednesday
    3: 3,  # Thursday
    4: 2,  # Friday
    5: 1,  # Saturday
    6: 7,  # Sunday
}

_YAMAGANDA_SLOT = {
    0: 4,  # Monday
    1: 3,  # Tuesday
    2: 2,  # Wednesday
    3: 1,  # Thursday
    4: 6,  # Friday
    5: 5,  # Saturday
    6: 8,  # Sunday (some traditions say 5)
}

# ============================================================
# CHOGHADIYA -- Planetary periods
# ============================================================
_DAY_CHOGHADIYA_NAMES = {
    0: ["Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit"],   # Monday
    1: ["Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],     # Tuesday
    2: ["Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh"],    # Wednesday
    3: ["Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh"],   # Thursday
    4: ["Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char"],    # Friday
    5: ["Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal"],    # Saturday
    6: ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],   # Sunday
}

_CHOGHADIYA_QUALITY = {
    "Amrit": "Best",
    "Shubh": "Good",
    "Labh": "Good",
    "Char": "Neutral",
    "Rog": "Inauspicious",
    "Kaal": "Inauspicious",
    "Udveg": "Inauspicious",
}

# Night Choghadiya sequence per weekday (sunset to next sunrise)
_NIGHT_CHOGHADIYA_NAMES = {
    0: ["Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char"],      # Monday
    1: ["Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal"],      # Tuesday
    2: ["Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh"],      # Wednesday
    3: ["Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit"],     # Thursday
    4: ["Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog"],       # Friday
    5: ["Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg"],     # Saturday
    6: ["Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh"],     # Sunday
}

# Vaar Vela / Kaal Vela / Kaal Ratri — 1-based period index per weekday (0=Mon..6=Sun)
_VAAR_VELA_PERIOD = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 7}  # Mon=6th, Tue=5th...Sun=7th
_KAAL_VELA_PERIOD = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}  # Mon=2nd, Tue=3rd...Sun=1st
# Kaal Ratri follows a DIFFERENT sequence from Kaal Vela (traditional night mapping)
_KAAL_RATRI_PERIOD = {0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3, 6: 8}  # Mon=2, Tue=7, Wed=5, Thu=6, Fri=4, Sat=3, Sun=8

# ============================================================
# HINDU MONTH NAMES
# ============================================================
_HINDU_MONTHS = [
    "Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
    "Shravana", "Bhadrapada", "Ashwin", "Kartik",
    "Margashirsha", "Pausha", "Magha", "Phalguna",
]

_RITU = [
    ("Vasanta", "Spring"),    # Chaitra-Vaishakha
    ("Grishma", "Summer"),    # Jyeshtha-Ashadha
    ("Varsha", "Monsoon"),    # Shravana-Bhadrapada
    ("Sharad", "Autumn"),     # Ashwin-Kartik
    ("Hemanta", "Pre-winter"), # Margashirsha-Pausha
    ("Shishira", "Winter"),   # Magha-Phalguna
]

_AYANA = ["Uttarayana", "Dakshinayana"]

# ============================================================
# VAAR (Weekday) NAMES
# ============================================================
_VAAR_NAMES = [
    "Somvar",   # Monday
    "Mangalvar", # Tuesday
    "Budhvar",   # Wednesday
    "Guruvar",   # Thursday
    "Shukravar", # Friday
    "Shanivar",  # Saturday
    "Ravivar",   # Sunday
]

_VAAR_ENGLISH = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


# ============================================================
# SUNRISE / SUNSET via Swiss Ephemeris or NOAA fallback
# ============================================================

def _swe_sunrise_sunset(date_str: str, latitude: float, longitude: float) -> Tuple[float, float, float, float]:
    """
    Compute sunrise, sunset, moonrise, moonset using Swiss Ephemeris.
    Returns (sunrise_jd, sunset_jd, moonrise_jd, moonset_jd).
    """
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    jd_start = swe.julday(year, month, day, 0.0)

    # Sunrise (upper limb, atmospheric refraction)
    try:
        sunrise_jd = swe.rise_trans(
            jd_start, swe.SUN, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        sunrise_jd = jd_start + 0.25  # fallback ~6 AM

    try:
        sunset_jd = swe.rise_trans(
            jd_start, swe.SUN, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        sunset_jd = jd_start + 0.75  # fallback ~6 PM

    try:
        moonrise_jd = swe.rise_trans(
            jd_start, swe.MOON, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        moonrise_jd = 0.0

    try:
        moonset_jd = swe.rise_trans(
            jd_start, swe.MOON, geopos=(longitude, latitude, 0),
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER,
        )[1][0]
    except Exception:
        moonset_jd = 0.0

    return sunrise_jd, sunset_jd, moonrise_jd, moonset_jd


def _jd_to_local_time_str(jd: float, tz_hours: float) -> str:
    """Convert JD to local HH:MM string."""
    if jd == 0.0:
        return "--:--"
    # Convert JD to UTC components
    ut_hours = (jd - int(jd) - 0.5) * 24.0
    if ut_hours < 0:
        ut_hours += 24.0
    local_hours = ut_hours + tz_hours
    if local_hours >= 24:
        local_hours -= 24
    elif local_hours < 0:
        local_hours += 24
    h = int(local_hours)
    m = int((local_hours - h) * 60)
    return f"{h:02d}:{m:02d}"


def _approx_sunrise_sunset(
    date_str: str, latitude: float, longitude: float,
) -> Tuple[str, str]:
    """
    Approximate sunrise and sunset times for a given date and location.
    Returns (sunrise_str, sunset_str) in "HH:MM" local solar time.
    """
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

    dt = datetime(year, month, day)
    doy = dt.timetuple().tm_yday

    declination = 23.45 * math.sin(math.radians(360.0 / 365.0 * (doy - 81)))
    dec_rad = math.radians(declination)
    lat_rad = math.radians(latitude)

    cos_ha = -math.tan(lat_rad) * math.tan(dec_rad)
    cos_ha = max(-1.0, min(1.0, cos_ha))
    ha = math.degrees(math.acos(cos_ha))

    b_val = math.radians(360.0 / 365.0 * (doy - 81))
    eot = 9.87 * math.sin(2 * b_val) - 7.53 * math.cos(b_val) - 1.5 * math.sin(b_val)

    solar_noon_minutes = 720
    sunrise_minutes = solar_noon_minutes - (ha / 360.0) * 24 * 60
    sunset_minutes = solar_noon_minutes + (ha / 360.0) * 24 * 60

    sunrise_h = int(sunrise_minutes // 60)
    sunrise_m = int(sunrise_minutes % 60)
    sunset_h = int(sunset_minutes // 60)
    sunset_m = int(sunset_minutes % 60)

    return f"{sunrise_h:02d}:{sunrise_m:02d}", f"{sunset_h:02d}:{sunset_m:02d}"


def _compute_sun_times(date_str: str, latitude: float, longitude: float, tz_offset: float = None) -> Dict[str, str]:
    """
    Compute sunrise, sunset, moonrise, moonset.
    Uses Swiss Ephemeris if available, otherwise NOAA approximation.
    Returns dict with sunrise, sunset, moonrise, moonset as HH:MM strings.
    """
    if tz_offset is None:
        tz_offset = 5.5 if 68.0 <= longitude <= 97.5 else round(longitude / 15.0 * 2) / 2

    if _HAS_SWE:
        try:
            sr_jd, ss_jd, mr_jd, ms_jd = _swe_sunrise_sunset(date_str, latitude, longitude)
            return {
                "sunrise": _jd_to_local_time_str(sr_jd, tz_offset),
                "sunset": _jd_to_local_time_str(ss_jd, tz_offset),
                "moonrise": _jd_to_local_time_str(mr_jd, tz_offset),
                "moonset": _jd_to_local_time_str(ms_jd, tz_offset),
            }
        except Exception:
            pass

    sr, ss = _approx_sunrise_sunset(date_str, latitude, longitude)
    # Approximate moonrise/moonset
    sr_min = _time_to_minutes(sr)
    return {
        "sunrise": sr,
        "sunset": ss,
        "moonrise": _minutes_to_time(sr_min + 50),
        "moonset": _minutes_to_time(_time_to_minutes(ss) + 50),
    }


# ============================================================
# ASTRONOMICAL COMPUTATIONS -- Sun/Moon longitudes at a given JD
# ============================================================

def _get_sun_moon_swe(jd: float) -> Tuple[float, float]:
    """Get tropical Sun and Moon longitudes via swisseph."""
    sun_pos, _ = swe.calc_ut(jd, 0)  # SE_SUN
    moon_pos, _ = swe.calc_ut(jd, 1)  # SE_MOON
    return sun_pos[0], moon_pos[0]


def _get_sidereal_longitudes(jd: float) -> Tuple[float, float, float]:
    """Return (sun_sid, moon_sid, ayanamsa) at given JD."""
    if _HAS_SWE:
        sun_lon, moon_lon = _get_sun_moon_swe(jd)
        ayanamsa = swe.get_ayanamsa(jd)
    else:
        sun_lon = _approx_sun_longitude(jd)
        moon_lon = _approx_moon_longitude(jd)
        ayanamsa = _approx_ayanamsa(jd)
    sun_sid = (sun_lon - ayanamsa) % 360.0
    moon_sid = (moon_lon - ayanamsa) % 360.0
    return sun_sid, moon_sid, ayanamsa


def _get_elongation(jd: float) -> float:
    """Get Moon-Sun elongation (0-360) at given JD. Used for tithi/karana."""
    if _HAS_SWE:
        sun_lon, moon_lon = _get_sun_moon_swe(jd)
    else:
        sun_lon = _approx_sun_longitude(jd)
        moon_lon = _approx_moon_longitude(jd)
    return (moon_lon - sun_lon) % 360.0


def _get_moon_longitude_sidereal(jd: float) -> float:
    """Get sidereal Moon longitude. Used for nakshatra boundary detection."""
    if _HAS_SWE:
        moon_pos, _ = swe.calc_ut(jd, 1)
        ayanamsa = swe.get_ayanamsa(jd)
        return (moon_pos[0] - ayanamsa) % 360.0
    else:
        moon_lon = _approx_moon_longitude(jd)
        ayanamsa = _approx_ayanamsa(jd)
        return (moon_lon - ayanamsa) % 360.0


def _get_yoga_angle(jd: float) -> float:
    """Get (Sun_sid + Moon_sid) % 360. Used for yoga boundary detection."""
    sun_sid, moon_sid, _ = _get_sidereal_longitudes(jd)
    return (sun_sid + moon_sid) % 360.0


# ============================================================
# END TIME CALCULATIONS -- Binary search for boundary crossings
# ============================================================

def _find_boundary_time(
    jd_start: float,
    angle_func,
    boundary_degree: float,
    span: float,
    max_hours: float = 30.0,
    tolerance_minutes: float = 0.5,
) -> Optional[float]:
    """
    Binary search to find when angle_func(jd) crosses boundary_degree.
    Returns JD of crossing, or None if not found within max_hours.

    angle_func: callable(jd) -> float (0-360)
    boundary_degree: the target boundary value
    span: the span of one unit (12 for tithi, 13.333 for nakshatra, etc.)
    """
    jd_end = jd_start + max_hours / 24.0
    step = 1.0 / 24.0  # 1 hour steps for coarse scan

    # Determine which unit we are in at start
    start_val = angle_func(jd_start)
    start_index = int(start_val / span)

    # Coarse scan to find the hour bracket where the boundary is crossed
    jd_a = jd_start
    prev_index = start_index
    found = False

    t = jd_start + step
    while t <= jd_end:
        cur_val = angle_func(t)
        cur_index = int(cur_val / span)
        # Handle wraparound
        if cur_index != prev_index:
            jd_a = t - step
            found = True
            break
        prev_index = cur_index
        t += step

    if not found:
        return None

    # Binary search within [jd_a, jd_a + step]
    jd_lo = jd_a
    jd_hi = jd_a + step
    tol = tolerance_minutes / (24.0 * 60.0)  # convert to JD units

    for _ in range(50):  # max iterations
        if (jd_hi - jd_lo) < tol:
            break
        jd_mid = (jd_lo + jd_hi) / 2.0
        mid_index = int(angle_func(jd_mid) / span)
        if mid_index == start_index:
            jd_lo = jd_mid
        else:
            jd_hi = jd_mid

    return (jd_lo + jd_hi) / 2.0


def _compute_tithi_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current tithi after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_elongation, 0.0, 12.0)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_nakshatra_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current nakshatra after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_moon_longitude_sidereal, 0.0, NAKSHATRA_SPAN)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_yoga_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current yoga after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_yoga_angle, 0.0, YOGA_SPAN)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_karana_end(jd_sunrise: float, tz_offset: float) -> str:
    """Find the end time of the current karana (half-tithi) after sunrise."""
    jd = _find_boundary_time(jd_sunrise, _get_elongation, 0.0, 6.0)
    if jd is None:
        return "--:--"
    return _jd_to_local_time_str(jd, tz_offset)


def _compute_second_karana_end(jd_sunrise: float, tz_offset: float, tithi_end_str: str) -> str:
    """
    Calculate the end time of the second karana.
    The second karana ends when the tithi ends (at the tithi boundary).
    We estimate this as halfway between first karana end and tithi end,
    or more precisely, the tithi end time itself since second karana ends with the tithi.
    """
    # The second karana ends at the tithi boundary
    # First, find when the current tithi ends (same as _compute_tithi_end)
    jd_tithi_end = _find_boundary_time(jd_sunrise, _get_elongation, 0.0, 12.0)
    if jd_tithi_end is None:
        return "--:--"
    return _jd_to_local_time_str(jd_tithi_end, tz_offset)


NAKSHATRA_SPAN = 360.0 / 27.0  # 13.3333 degrees


# ============================================================
# PLANETARY POSITIONS (NAVGRAHA) — helpers
# ============================================================

def _nakshatra_for_longitude(sid_lon: float) -> Tuple[str, str, int]:
    """Return (nakshatra_name, nakshatra_hindi, pada) for a sidereal longitude."""
    lon = sid_lon % 360.0
    nak_span = ASTRO_NAKSHATRA_SPAN  # 13.3333...
    nak_index = int(lon / nak_span)
    if nak_index >= 27:
        nak_index = 26
    nak_name = ASTRO_NAKSHATRAS[nak_index]["name"]
    nak_hindi = NAKSHATRA_HINDI.get(nak_name, nak_name)
    pada = int((lon % nak_span) / (nak_span / 4.0)) + 1
    if pada > 4:
        pada = 4
    return nak_name, nak_hindi, pada


def _is_combust(planet_name: str, planet_lon: float, sun_lon: float,
                is_retrograde: bool) -> bool:
    """Check if a planet is combust (too close to Sun)."""
    if planet_name not in COMBUSTION_ORBS:
        return False
    orb = COMBUSTION_ORBS[planet_name]
    # Reduced orb for Mercury and Venus when retrograde
    if is_retrograde and planet_name in COMBUSTION_ORBS_RETROGRADE:
        orb = COMBUSTION_ORBS_RETROGRADE[planet_name]
    # Angular distance (shortest arc)
    diff = abs(planet_lon - sun_lon)
    if diff > 180.0:
        diff = 360.0 - diff
    return diff <= orb


def _enrich_planet_dict(entry: Dict[str, Any], sun_lon: float) -> None:
    """Add nakshatra, rashi_hindi, name_hindi, combustion fields in-place."""
    name = entry["name"]
    sid_lon = entry["longitude"]
    rashi = entry["rashi"]
    is_retro = entry.get("retrograde", False)

    # Nakshatra & Pada
    nak_name, nak_hindi, pada = _nakshatra_for_longitude(sid_lon)
    entry["nakshatra"] = nak_name
    entry["nakshatra_hindi"] = nak_hindi
    entry["nakshatra_pada"] = pada

    # Rashi Hindi
    entry["rashi_hindi"] = RASHI_HINDI.get(rashi, rashi)

    # Planet Hindi name
    entry["name_hindi"] = PLANET_HINDI.get(name, name)

    # Combustion (only physical planets Moon–Saturn, not nodes)
    if name in COMBUSTION_ORBS:
        entry["combusted"] = _is_combust(name, sid_lon, sun_lon, is_retro)
    else:
        entry["combusted"] = False


# ============================================================
# PLANETARY POSITIONS (NAVGRAHA)
# ============================================================

def calculate_planetary_positions(jd: float) -> List[Dict[str, Any]]:
    """
    Calculate sidereal positions for all 9 Vedic planets (Navgraha).

    Returns list of dicts, each containing:
      name, longitude, degree, rashi, rashi_index,
      retrograde, nakshatra, nakshatra_hindi, nakshatra_pada,
      rashi_hindi, name_hindi, combusted
    """
    planets = []
    if _HAS_SWE:
        ayanamsa = swe.get_ayanamsa(jd)
        ayanamsa_next = swe.get_ayanamsa(jd + 1.0)
        planet_list = [
            ("Sun", 0), ("Moon", 1), ("Mars", 4), ("Mercury", 2),
            ("Jupiter", 5), ("Venus", 3), ("Saturn", 6), ("Rahu", 10),
        ]
        for name, pid in planet_list:
            pos, _ = swe.calc_ut(jd, pid)
            sid_lon = (pos[0] - ayanamsa) % 360.0
            rashi = get_sign_from_longitude(sid_lon)

            # --- Retrograde detection ---
            if name == "Sun":
                retrograde = False  # Sun never retrogrades
            elif name == "Rahu":
                retrograde = True  # Rahu always retrograde by convention
            else:
                pos_next, _ = swe.calc_ut(jd + 1.0, pid)
                sid_lon_next = (pos_next[0] - ayanamsa_next) % 360.0
                # If longitude decreases over 1 day -> retrograde
                delta = sid_lon_next - sid_lon
                # Handle wrap-around (e.g., 359 -> 1 is +2 not -358)
                if delta > 180.0:
                    delta -= 360.0
                elif delta < -180.0:
                    delta += 360.0
                retrograde = delta < 0.0

            planets.append({
                "name": name,
                "longitude": round(sid_lon, 4),
                "degree": round(sid_lon % 30.0, 2),
                "rashi": rashi,
                "rashi_index": int(sid_lon / 30.0),
                "retrograde": retrograde,
            })

        # Ketu = Rahu + 180 (always retrograde by convention)
        rahu_lon = next(p["longitude"] for p in planets if p["name"] == "Rahu")
        ketu_lon = (rahu_lon + 180.0) % 360.0
        planets.append({
            "name": "Ketu",
            "longitude": round(ketu_lon, 4),
            "degree": round(ketu_lon % 30.0, 2),
            "rashi": get_sign_from_longitude(ketu_lon),
            "rashi_index": int(ketu_lon / 30.0),
            "retrograde": True,
        })
    else:
        # Fallback -- use approximations from astro_engine
        from app.astro_engine import _approx_planet_longitude, _approx_rahu_longitude
        ayanamsa = _approx_ayanamsa(jd)
        ayanamsa_next = _approx_ayanamsa(jd + 1.0)
        approx_funcs = {
            "Sun": lambda _jd=jd: _approx_sun_longitude(_jd),
            "Moon": lambda _jd=jd: _approx_moon_longitude(_jd),
            "Mars": lambda _jd=jd: _approx_planet_longitude(_jd, "Mars"),
            "Mercury": lambda _jd=jd: _approx_planet_longitude(_jd, "Mercury"),
            "Jupiter": lambda _jd=jd: _approx_planet_longitude(_jd, "Jupiter"),
            "Venus": lambda _jd=jd: _approx_planet_longitude(_jd, "Venus"),
            "Saturn": lambda _jd=jd: _approx_planet_longitude(_jd, "Saturn"),
            "Rahu": lambda _jd=jd: _approx_rahu_longitude(_jd),
        }
        approx_funcs_next = {
            "Sun": lambda _jd=jd: _approx_sun_longitude(_jd + 1.0),
            "Moon": lambda _jd=jd: _approx_moon_longitude(_jd + 1.0),
            "Mars": lambda _jd=jd: _approx_planet_longitude(_jd + 1.0, "Mars"),
            "Mercury": lambda _jd=jd: _approx_planet_longitude(_jd + 1.0, "Mercury"),
            "Jupiter": lambda _jd=jd: _approx_planet_longitude(_jd + 1.0, "Jupiter"),
            "Venus": lambda _jd=jd: _approx_planet_longitude(_jd + 1.0, "Venus"),
            "Saturn": lambda _jd=jd: _approx_planet_longitude(_jd + 1.0, "Saturn"),
            "Rahu": lambda _jd=jd: _approx_rahu_longitude(_jd + 1.0),
        }
        for name, func in approx_funcs.items():
            trop = func()
            sid_lon = (trop - ayanamsa) % 360.0
            rashi = get_sign_from_longitude(sid_lon)

            # --- Retrograde detection ---
            if name == "Sun":
                retrograde = False
            elif name == "Rahu":
                retrograde = True
            else:
                trop_next = approx_funcs_next[name]()
                sid_lon_next = (trop_next - ayanamsa_next) % 360.0
                delta = sid_lon_next - sid_lon
                if delta > 180.0:
                    delta -= 360.0
                elif delta < -180.0:
                    delta += 360.0
                retrograde = delta < 0.0

            planets.append({
                "name": name,
                "longitude": round(sid_lon, 4),
                "degree": round(sid_lon % 30.0, 2),
                "rashi": rashi,
                "rashi_index": int(sid_lon / 30.0),
                "retrograde": retrograde,
            })

        rahu_lon = next(p["longitude"] for p in planets if p["name"] == "Rahu")
        ketu_lon = (rahu_lon + 180.0) % 360.0
        planets.append({
            "name": "Ketu",
            "longitude": round(ketu_lon, 4),
            "degree": round(ketu_lon % 30.0, 2),
            "rashi": get_sign_from_longitude(ketu_lon),
            "rashi_index": int(ketu_lon / 30.0),
            "retrograde": True,
        })

    # --- Enrich all planets with nakshatra, Hindi names, combustion ---
    sun_lon = next(p["longitude"] for p in planets if p["name"] == "Sun")
    for p in planets:
        _enrich_planet_dict(p, sun_lon)

    return planets


# ============================================================
# RAHU KAAL / GULIKA KAAL / YAMAGANDA KAAL
# ============================================================

def _compute_kaal_period(weekday: int, sunrise: str, sunset: str, slot_map: dict) -> Dict[str, str]:
    """Divide daytime into 8 equal parts and return the slot for the weekday."""
    sr_min = _time_to_minutes(sunrise)
    ss_min = _time_to_minutes(sunset)
    day_duration = ss_min - sr_min
    slot = slot_map.get(weekday, 1)
    slot_duration = day_duration / 8.0
    start_min = sr_min + (slot - 1) * slot_duration
    end_min = start_min + slot_duration
    return {
        "start": _minutes_to_time(start_min),
        "end": _minutes_to_time(end_min),
    }


def calculate_rahu_kaal(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Rahu Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _RAHU_KAAL_SLOT)


def calculate_gulika_kaal(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Gulika Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _GULIKA_KAAL_SLOT)


def calculate_yamaganda(weekday: int, sunrise: str, sunset: str) -> Dict[str, str]:
    """Calculate Yamaganda Kaal period for a given weekday."""
    return _compute_kaal_period(weekday, sunrise, sunset, _YAMAGANDA_SLOT)


# ============================================================
# AUSPICIOUS TIMINGS
# ============================================================

def calculate_abhijit_muhurat(sunrise: str, sunset: str) -> Dict[str, str]:
    """
    Abhijit Muhurat: the 8th muhurat of the day (midday window).
    Divide daytime into 15 muhurats; the 8th is Abhijit.
    """
    sr_min = _time_to_minutes(sunrise)
    ss_min = _time_to_minutes(sunset)
    day_duration = ss_min - sr_min
    muhurat_duration = day_duration / 15.0
    start = sr_min + 7 * muhurat_duration
    end = start + muhurat_duration
    return {
        "start": _minutes_to_time(start),
        "end": _minutes_to_time(end),
    }


def calculate_brahma_muhurat(sunrise: str, ratrimana_mins: float = 672.0) -> Dict[str, str]:
    """
    Brahma Muhurat: 2 night-muhurats before sunrise.
    One night muhurta = ratrimana / 15. Brahma Muhurat spans the
    penultimate night muhurta (2nd-to-last before sunrise).
    Default ratrimana 672 min (= 11h 12m) gives ~44.8 min muhurta.
    """
    sr_min = _time_to_minutes(sunrise)
    muhurta_night = ratrimana_mins / 15.0
    start = sr_min - 2 * muhurta_night
    end = sr_min - muhurta_night
    if start < 0:
        start += 1440
    if end < 0:
        end += 1440
    return {
        "start": _minutes_to_time(start),
        "end": _minutes_to_time(end),
    }


# ============================================================
# HINDU CALENDAR SYSTEM (Vikram Samvat, Shaka Samvat)
# ============================================================

def _compute_hindu_calendar(date_str: str, tithi_index: int, sun_sid: float) -> Dict[str, Any]:
    """
    Compute Hindu calendar elements.
    - Vikram Samvat = Gregorian year + 57 (approx, adjusted for Chaitra)
    - Shaka Samvat = Gregorian year - 78 (approx)
    - Maas from Sun sidereal longitude (solar month)
    - Paksha from tithi
    - Ritu and Ayana from solar position
    """
    parts = date_str.split("-")
    year = int(parts[0])
    month = int(parts[1])

    # Lunar month (Purnimant system, North Indian tradition).
    # The lunar month is named after the solar month in which the
    # full moon (Purnima) falls.  A practical mapping from the
    # Sun's sidereal sign:
    #   Mesha  (0)  -> Vaishakha     Tula   (6)  -> Kartik
    #   Vrishabha(1)-> Jyeshtha      Vrischika(7)-> Margashirsha
    #   Mithuna(2)  -> Ashadha       Dhanu  (8)  -> Pausha
    #   Karka  (3)  -> Shravana      Makara (9)  -> Magha
    #   Simha  (4)  -> Bhadrapada    Kumbha(10)  -> Phalguna
    #   Kanya  (5)  -> Ashwin        Meena (11)  -> Chaitra
    #
    # For Krishna paksha (dark fortnight, 2nd half of lunar month)
    # the month has ALREADY advanced by one from the full moon,
    # so we add +1.
    solar_sign_idx = int(sun_sid / 30.0) % 12
    base_maas = (solar_sign_idx + 1) % 12          # Mesha->Vaishakha

    paksha = "Shukla" if tithi_index < 15 else "Krishna"

    # Purnimant (North Indian): month runs Krishna-then-Shukla.
    # Krishna paksha is the FIRST half of the month, so no +1 needed.
    maas_index = base_maas
    maas_name = _HINDU_MONTHS[maas_index]

    # Vikram Samvat (starts ~March/April, Chaitra Shukla Pratipada)
    vikram_samvat = year + 57
    if month < 4:  # Before April
        vikram_samvat -= 1

    # Shaka Samvat
    shaka_samvat = year - 78
    if month < 4:
        shaka_samvat -= 1

    # Ritu (season) -- 2 months per ritu
    ritu_index = maas_index // 2
    ritu_name, ritu_english = _RITU[ritu_index]

    # Ayana -- Uttarayana (Capricorn to Gemini = signs 9-2), Dakshinayana (Cancer to Sagittarius = 3-8)
    if solar_sign_idx >= 9 or solar_sign_idx <= 2:
        ayana = _AYANA[0]  # Uttarayana
    else:
        ayana = _AYANA[1]  # Dakshinayana

    return {
        "vikram_samvat": vikram_samvat,
        "shaka_samvat": shaka_samvat,
        "maas": maas_name,
        "paksha": paksha,
        "ritu": ritu_name,
        "ritu_english": ritu_english,
        "ayana": ayana,
    }


# ============================================================
# KARANA HELPERS
# ============================================================

def _get_karana_index(tithi_index: int, elongation: float = None) -> int:
    """Get karana number (0-59).

    When *elongation* (Moon - Sun mod 360) is provided, the index is computed
    directly from ``floor(elongation / 6.0)``, which correctly distinguishes
    the first and second half of each tithi.  Falls back to the tithi-based
    approximation only when elongation is unavailable.
    """
    if elongation is not None:
        idx = int(elongation / 6.0)
        return min(idx, 59)  # clamp to valid range
    # Legacy fallback (first half only — kept for backward compat)
    half_tithi = tithi_index * 2
    return half_tithi % 60


def _get_karana_name(karana_index: int) -> str:
    """Map a karana index (0-59) to its name."""
    if karana_index == 0:
        return "Kimstughna"
    if karana_index >= 57:
        fixed_map = {57: "Shakuni", 58: "Chatushpada", 59: "Naga"}
        return fixed_map.get(karana_index, "Kimstughna")
    return _REPEATING_KARANAS[(karana_index - 1) % 7]


# ============================================================
# CHOGHADIYA
# ============================================================

def calculate_choghadiya(
    weekday: int, sunrise: str, sunset: str,
) -> List[Dict[str, Any]]:
    """Calculate Choghadiya (auspicious time periods) for daytime."""
    sr_minutes = _time_to_minutes(sunrise)
    ss_minutes = _time_to_minutes(sunset)
    day_duration = ss_minutes - sr_minutes
    slot_duration = day_duration / 8.0

    names = _DAY_CHOGHADIYA_NAMES.get(weekday, _DAY_CHOGHADIYA_NAMES[0])
    vaar_vela_idx = _VAAR_VELA_PERIOD.get(weekday, 0) - 1  # convert to 0-based
    kaal_vela_idx = _KAAL_VELA_PERIOD.get(weekday, 0) - 1
    result = []
    for i, name in enumerate(names):
        start = sr_minutes + i * slot_duration
        end = start + slot_duration
        period = {
            "name": name,
            "quality": _CHOGHADIYA_QUALITY.get(name, "Unknown"),
            "start": _minutes_to_time(start),
            "end": _minutes_to_time(end),
        }
        if i == vaar_vela_idx:
            period["vaar_vela"] = True
        if i == kaal_vela_idx:
            period["kaal_vela"] = True
        result.append(period)
    return result


def calculate_night_choghadiya(
    weekday: int, sunset: str, next_sunrise: str,
) -> List[Dict[str, Any]]:
    """Calculate Night Choghadiya (sunset to next sunrise)."""
    ss_minutes = _time_to_minutes(sunset)
    nsr_minutes = _time_to_minutes(next_sunrise)
    # Handle overnight wrap: if next_sunrise appears earlier, add 24h
    if nsr_minutes <= ss_minutes:
        nsr_minutes += 1440
    night_duration = nsr_minutes - ss_minutes
    slot_duration = night_duration / 8.0

    names = _NIGHT_CHOGHADIYA_NAMES.get(weekday, _NIGHT_CHOGHADIYA_NAMES[0])
    kaal_ratri_idx = _KAAL_RATRI_PERIOD.get(weekday, 0) - 1  # convert to 0-based
    result = []
    for i, name in enumerate(names):
        start = ss_minutes + i * slot_duration
        end = start + slot_duration
        period = {
            "name": name,
            "quality": _CHOGHADIYA_QUALITY.get(name, "Unknown"),
            "start": _minutes_to_time(start % 1440),
            "end": _minutes_to_time(end % 1440),
        }
        if i == kaal_ratri_idx:
            period["kaal_ratri"] = True
        result.append(period)
    return result


# ============================================================
# TIME HELPERS
# ============================================================

def _time_to_minutes(time_str: str) -> float:
    """Convert "HH:MM" to minutes from midnight."""
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(minutes: float) -> str:
    """Convert minutes from midnight to "HH:MM"."""
    h = int(minutes // 60) % 24
    m = int(minutes % 60)
    return f"{h:02d}:{m:02d}"


# ============================================================
# ============================================================
# NAKSHATRA CATEGORY HELPER
# ============================================================

def _nakshatra_category_fields(nak_name: str) -> Dict[str, str]:
    """Return category fields for a nakshatra name."""
    cat_key = NAKSHATRA_CATEGORY.get(nak_name, "mishra")
    cat = NAKSHATRA_CATEGORY_DATA.get(cat_key, NAKSHATRA_CATEGORY_DATA["mishra"])
    return {
        "category": cat_key,
        "category_en": cat["en"],
        "category_hi": cat["hi"],
        "category_good_for_en": cat["good_for_en"],
        "category_good_for_hi": cat["good_for_hi"],
        "category_color": cat["color"],
    }


# ============================================================
# PANCHANGA SHUDDHI — Composite day-quality score
# ============================================================

_GOOD_TITHIS = {2, 3, 5, 7, 10, 11, 12, 13}
_BAD_TITHIS = {4, 6, 8, 9, 14}
_BAD_NAKSHATRAS = {"Bharani", "Krittika", "Ardra", "Ashlesha", "Jyeshtha", "Mula", "Purva Ashadha", "Purva Bhadrapada"}
_GOOD_NAKSHATRAS = {"Rohini", "Pushya", "Uttara Phalguni", "Hasta", "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Revati", "Uttara Bhadrapada"}
_BAD_KARANAS = {"Vishti", "Shakuni", "Chatushpada", "Naga"}


def _compute_panchanga_shuddhi(
    tithi_index: int,
    paksha: str,
    weekday: int,
    yoga_number: int,
    karana_name: str,
    nakshatra_name: str,
) -> Dict[str, Any]:
    """Compute Panchanga Shuddhi — composite score of day quality.

    Scores each of the 5 limbs (tithi, vara, nakshatra, yoga, karana)
    and returns a composite 0-100 score with a qualitative label.
    """
    # 1. Tithi score (0-20)
    norm_t = tithi_index if tithi_index <= 15 else tithi_index - 15
    if norm_t in _GOOD_TITHIS:
        tithi_score = 20
    elif norm_t in _BAD_TITHIS:
        tithi_score = 0
    elif norm_t == 15:
        tithi_score = 10  # Purnima — mixed
    else:
        tithi_score = 5  # Pratipada/amavasya — weak
    if paksha.lower() == "krishna" and norm_t in _BAD_TITHIS:
        tithi_score = max(0, tithi_score - 5)

    # 2. Vara score (0-20)
    if weekday in {3, 4}:  # Wed, Thu
        vara_score = 20
    elif weekday in {0, 1, 5}:  # Sun, Mon, Fri
        vara_score = 15
    elif weekday == 6:  # Sat
        vara_score = 5
    else:  # Tue
        vara_score = 0

    # 3. Nakshatra score (0-20)
    if nakshatra_name in _GOOD_NAKSHATRAS:
        nak_score = 20
    elif nakshatra_name in _BAD_NAKSHATRAS:
        nak_score = 0
    else:
        nak_score = 10

    # 4. Yoga score (0-20)
    if yoga_number in {17, 27}:  # Vyatipata, Vaidhriti
        yoga_score = 0
    elif yoga_number in {1, 6, 9, 10, 13, 19, 24}:  # Other bad yogas
        yoga_score = 5
    elif yoga_number in {16, 20, 21, 22, 23, 25, 26}:  # Excellent yogas
        yoga_score = 20
    else:
        yoga_score = 15

    # 5. Karana score (0-20)
    if karana_name in _BAD_KARANAS:
        karana_score = 0
    elif karana_name == "Kimstughna":
        karana_score = 5
    else:
        karana_score = 20

    total = tithi_score + vara_score + nak_score + yoga_score + karana_score

    if total >= 85:
        label, label_hindi = "Excellent", "उत्तम"
    elif total >= 70:
        label, label_hindi = "Good", "शुभ"
    elif total >= 50:
        label, label_hindi = "Average", "सामान्य"
    elif total >= 30:
        label, label_hindi = "Weak", "कमज़ोर"
    else:
        label, label_hindi = "Inauspicious", "अशुभ"

    return {
        "score": total,
        "label": label,
        "label_hindi": label_hindi,
        "breakdown": {
            "tithi": tithi_score,
            "vara": vara_score,
            "nakshatra": nak_score,
            "yoga": yoga_score,
            "karana": karana_score,
        },
    }


# PUBLIC: calculate_panchang (ENHANCED)
# ============================================================

def calculate_panchang(
    date: str, latitude: float, longitude: float, tz_offset: float = None,
) -> Dict[str, Any]:
    """
    Calculate complete Panchang for a given date and location.

    Returns the original contract keys (tithi, nakshatra, yoga, karana, sunrise, sunset)
    plus extended data for the enhanced UI.
    """
    # CRITICAL: Reset to Lahiri ayanamsa. Other engines (KP) may have
    # switched swe to Krishnamurti mode in the same worker process.
    if _HAS_SWE:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    if tz_offset is None:
        # Default to IST for India, otherwise approximate from longitude
        if 68.0 <= longitude <= 97.5:
            tz_offset = 5.5  # IST
        else:
            tz_offset = round(longitude / 15.0 * 2) / 2  # round to nearest 0.5h

    # 1. Sunrise/Sunset/Moonrise/Moonset
    sun_times = _compute_sun_times(date, latitude, longitude, tz_offset)
    sunrise_str = sun_times["sunrise"]
    sunset_str = sun_times["sunset"]

    # 2. Julian Day at sunrise for panchang calculations
    dt_utc = _parse_datetime(date, sunrise_str, tz_offset)
    jd_sunrise = _datetime_to_jd(dt_utc)

    # 3. Sidereal longitudes at sunrise
    sun_sid, moon_sid, ayanamsa = _get_sidereal_longitudes(jd_sunrise)

    # 4. Elongation for Tithi
    elongation = _get_elongation(jd_sunrise)
    tithi_index = int(elongation / 12.0)
    if tithi_index >= 30:
        tithi_index = 29
    tithi = TITHIS[tithi_index]

    # 5. Nakshatra
    nakshatra = get_nakshatra_from_longitude(moon_sid)

    # 6. Yoga
    yoga_sum = (sun_sid + moon_sid) % 360.0
    yoga_index = int(yoga_sum / YOGA_SPAN)
    if yoga_index >= 27:
        yoga_index = 26
    yoga_name = YOGAS[yoga_index]

    # 7. Karana (use elongation for correct half-tithi distinction)
    karana_index = _get_karana_index(tithi_index, elongation)
    karana_name = _get_karana_name(karana_index)

    # 8. End times via binary search
    tithi_end = _compute_tithi_end(jd_sunrise, tz_offset)
    nakshatra_end = _compute_nakshatra_end(jd_sunrise, tz_offset)
    yoga_end = _compute_yoga_end(jd_sunrise, tz_offset)
    karana_end = _compute_karana_end(jd_sunrise, tz_offset)

    # 9. Weekday / Vaar
    parts = date.split("-")
    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    weekday = dt.weekday()

    # 10. Rahu Kaal, Gulika Kaal, Yamaganda
    rahu_kaal = calculate_rahu_kaal(weekday, sunrise_str, sunset_str)
    gulika_kaal = calculate_gulika_kaal(weekday, sunrise_str, sunset_str)
    yamaganda = calculate_yamaganda(weekday, sunrise_str, sunset_str)

    # 11. Auspicious timings
    abhijit = calculate_abhijit_muhurat(sunrise_str, sunset_str)
    _sr_m = _time_to_minutes(sunrise_str)
    _ss_m = _time_to_minutes(sunset_str)
    ratrimana_mins = 1440 - (_ss_m - _sr_m)
    brahma = calculate_brahma_muhurat(sunrise_str, ratrimana_mins=ratrimana_mins)

    # 12. Planetary positions
    planetary_positions = calculate_planetary_positions(jd_sunrise)

    # 13. Hindu calendar
    hindu_calendar = _compute_hindu_calendar(date, tithi_index, sun_sid)

    # 14. Choghadiya (Day + Night)
    choghadiya = calculate_choghadiya(weekday, sunrise_str, sunset_str)
    # Night: sunset to next sunrise (approximate next sunrise = same sunrise + 24h)
    # For a more accurate calculation we'd compute tomorrow's sunrise,
    # but using today's sunrise as proxy is standard practice.
    night_choghadiya = calculate_night_choghadiya(weekday, sunset_str, sunrise_str)

    # 15. Next Tithi, Nakshatra, Yoga
    next_tithi_idx = (tithi_index + 1) % 30
    next_tithi = TITHIS[next_tithi_idx]
    next_nakshatra_idx = (nakshatra.get("index", 0) + 1) % 27
    from app.astro_engine import NAKSHATRAS
    next_nak_name = NAKSHATRAS[next_nakshatra_idx]["name"] if next_nakshatra_idx < len(NAKSHATRAS) else ""
    next_yoga_idx = (yoga_index + 1) % 27
    next_yoga_name = YOGAS[next_yoga_idx] if next_yoga_idx < len(YOGAS) else ""

    # 16. Second Karana
    second_karana_idx = _get_karana_index(tithi_index, elongation) + 1
    if second_karana_idx >= 60:
        second_karana_idx = 0
    second_karana_name = _get_karana_name(second_karana_idx)
    # Calculate second karana end time (approximately halfway between first karana end and tithi end)
    second_karana_end = _compute_second_karana_end(jd_sunrise, tz_offset, tithi_end)

    # 17. Sun sign + Moon sign
    sun_sign = get_sign_from_longitude(sun_sid)
    moon_sign = get_sign_from_longitude(moon_sid)

    # 18. Dinamana / Ratrimana / Madhyahna
    sunrise_mins = _time_to_minutes(sunrise_str)
    sunset_mins = _time_to_minutes(sunset_str)
    dinamana_mins = sunset_mins - sunrise_mins
    ratrimana_mins = 1440 - dinamana_mins
    madhyahna_mins = sunrise_mins + dinamana_mins / 2
    dinamana_str = f"{int(dinamana_mins // 60)} Hours {int(dinamana_mins % 60)} Mins"
    ratrimana_str = f"{int(ratrimana_mins // 60)} Hours {int(ratrimana_mins % 60)} Mins"
    madhyahna_str = _minutes_to_time(madhyahna_mins)

    # 19. Additional Muhurtas
    day_duration_mins = dinamana_mins
    muhurta_duration = day_duration_mins / 15  # each muhurta = 1/15th of day

    # Godhuli Muhurta: ~24 min around sunset
    godhuli = {"start": _minutes_to_time(sunset_mins - 24), "end": _minutes_to_time(sunset_mins)}
    # Sayahna Sandhya: sunset to sunset+48min
    sayahna = {"start": sunset_str, "end": _minutes_to_time(sunset_mins + 48)}
    # Nishita Muhurta: midnight ± 24min
    midnight_mins = sunset_mins + ratrimana_mins / 2
    nishita = {"start": _minutes_to_time(midnight_mins - 24), "end": _minutes_to_time(midnight_mins + 24)}
    # Pratah Sandhya: sunrise-48min to sunrise
    pratah = {"start": _minutes_to_time(sunrise_mins - 48), "end": sunrise_str}
    # Ravi Yoga: sunrise to sunrise + 1/5 of day (first 1/5 of daytime on Sunday)
    ravi_yoga_end = sunrise_mins + day_duration_mins * 3 / 15
    ravi_yoga = {"start": sunrise_str, "end": _minutes_to_time(ravi_yoga_end)}
    # Vijaya Muhurta: 7th muhurta of the day
    vijaya_start = sunrise_mins + muhurta_duration * 6
    vijaya = {"start": _minutes_to_time(vijaya_start), "end": _minutes_to_time(vijaya_start + muhurta_duration)}

    # 20. Dur Muhurtam (8th muhurta on most days)
    dur_start = sunrise_mins + muhurta_duration * 7
    dur_muhurtam = {"start": _minutes_to_time(dur_start), "end": _minutes_to_time(dur_start + muhurta_duration)}

    # 21. Varjyam (inauspicious period based on nakshatra)
    # Simplified: ~1.5 hours, position depends on nakshatra number
    nak_num = nakshatra.get("index", 0) % 9
    varjyam_offset = (nak_num * 2 + 1) * 60  # rough calculation
    varjyam_start = sunrise_mins + varjyam_offset % (dinamana_mins * 0.8)
    varjyam = {"start": _minutes_to_time(varjyam_start), "end": _minutes_to_time(varjyam_start + 90)}

    # 22. Hora Table (planetary hours — 24 horas, day + night)
    hora_sequence_day = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    # Day lord based on weekday — dt.weekday() gives 0=Mon..6=Sun
    # Mon=Moon(3), Tue=Mars(6), Wed=Mercury(2), Thu=Jupiter(5), Fri=Venus(1), Sat=Saturn(4), Sun=Sun(0)
    day_lord_idx = [3, 6, 2, 5, 1, 4, 0][weekday]
    hora_duration_day = dinamana_mins / 12
    hora_duration_night = ratrimana_mins / 12
    HORA_GUIDE = {
        "Sun": {"best_for": ["Government work", "Authority matters"], "best_for_hindi": "सरकारी कार्य, अधिकार संबंधी"},
        "Moon": {"best_for": ["Travel", "Agriculture", "Art"], "best_for_hindi": "यात्रा, कृषि, कला"},
        "Mars": {"best_for": ["Surgery", "Property", "Competition"], "best_for_hindi": "शल्य चिकित्सा, संपत्ति, प्रतिस्पर्धा"},
        "Mercury": {"best_for": ["Business", "Education", "Commerce"], "best_for_hindi": "व्यापार, शिक्षा, वाणिज्य"},
        "Jupiter": {"best_for": ["Marriage", "Spiritual", "Teaching"], "best_for_hindi": "विवाह, आध्यात्मिक, शिक्षण"},
        "Venus": {"best_for": ["Marriage", "Art", "Luxury purchases"], "best_for_hindi": "विवाह, कला, विलासी खरीदारी"},
        "Saturn": {"best_for": ["Property dealing", "Iron/oil work"], "best_for_hindi": "संपत्ति, लोहा/तेल कार्य", "avoid_for": ["New beginnings", "Marriage"]},
    }
    hora_table = []
    for i in range(12):
        lord = hora_sequence_day[(day_lord_idx + i) % 7]
        start = _minutes_to_time(sunrise_mins + i * hora_duration_day)
        end = _minutes_to_time(sunrise_mins + (i + 1) * hora_duration_day)
        guide = HORA_GUIDE.get(lord, {})
        activity_guide = {
            "best_for": guide.get("best_for", []),
            "best_for_hindi": guide.get("best_for_hindi", ""),
        }
        if "avoid_for" in guide:
            activity_guide["avoid_for"] = guide["avoid_for"]
        hora_table.append({"hora": i + 1, "lord": lord, "start": start, "end": end, "type": "day", "activity_guide": activity_guide})
    for i in range(12):
        lord = hora_sequence_day[(day_lord_idx + 12 + i) % 7]
        start = _minutes_to_time(sunset_mins + i * hora_duration_night)
        end = _minutes_to_time(sunset_mins + (i + 1) * hora_duration_night)
        guide = HORA_GUIDE.get(lord, {})
        activity_guide = {
            "best_for": guide.get("best_for", []),
            "best_for_hindi": guide.get("best_for_hindi", ""),
        }
        if "avoid_for" in guide:
            activity_guide["avoid_for"] = guide["avoid_for"]
        hora_table.append({"hora": i + 13, "lord": lord, "start": start, "end": end, "type": "night", "activity_guide": activity_guide})

    # 23. Lagna Table (Udaya Lagna — rising sign changes through the day)
    # Calculate proper Ascendant using sidereal time (NOT Sun position)
    # Lagna = rising sign on eastern horizon, changes every ~2 hours
    lagna_table = []
    _RASHI_NAMES = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    _RASHI_NAMES_HINDI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
                          "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
    
    def _calculate_ascendant(jd, lat, lon):
        """
        Calculate Ascendant (Lagna) using sidereal time.
        Returns sign index (0-11) and exact longitude.
        """
        # Julian centuries from J2000.0
        T = (jd - 2451545.0) / 36525.0
        
        # Greenwich Mean Sidereal Time at 0h UT (in degrees)
        # Formula: GMST = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + ...
        gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545.0)
        
        # Add higher order terms for better accuracy
        gmst_deg += 0.000387933 * T * T - T * T * T / 38710000.0
        
        # Normalize to 0-360
        gmst_deg = gmst_deg % 360.0
        
        # Local Sidereal Time (add longitude, positive east)
        lst_deg = (gmst_deg + lon) % 360.0
        
        # Convert LST to radians for calculation
        lst_rad = math.radians(lst_deg)
        lat_rad = math.radians(lat)
        
        # Obliquity of ecliptic (approximate, in radians)
        # Mean obliquity: ε = 23°26'21.448" - 46.815"*T - 0.00059"*T² + 0.001813"*T³
        eps_deg = 23.439291111 - 0.013004167 * T - 1.6389e-7 * T * T + 5.0361e-7 * T * T * T
        eps_rad = math.radians(eps_deg)
        
        # Calculate Ascendant using standard formula
        # tan(ASC) = cos(LST) / -(sin(LST) * cos(ε) + tan(φ) * sin(ε))
        # where φ = latitude, ε = obliquity, LST = local sidereal time
        
        denom = -(math.sin(lst_rad) * math.cos(eps_rad) + math.tan(lat_rad) * math.sin(eps_rad))
        numer = math.cos(lst_rad)
        
        # Handle special cases to avoid division issues
        if abs(denom) < 1e-10:
            asc_rad = math.pi / 2 if numer > 0 else -math.pi / 2
        else:
            asc_rad = math.atan2(numer, denom)
        
        # Convert to degrees and normalize
        asc_deg = math.degrees(asc_rad) % 360.0
        
        # Apply ayanamsa correction for sidereal zodiac
        asc_sid = (asc_deg - ayanamsa) % 360.0
        
        sign_idx = int(asc_sid / 30) % 12
        return {"sign": sign_idx, "longitude": asc_sid}
    
    # Calculate lagna boundaries by sampling ascendant every 5 minutes for 24h
    # This gives accurate durations that vary by latitude and season
    _SAMPLE_INTERVAL = 5  # minutes
    _TOTAL_SAMPLES = (24 * 60) // _SAMPLE_INTERVAL + 1  # 289 samples for 24h
    _jd_per_min = 1.0 / 1440.0

    samples = []
    for s in range(_TOTAL_SAMPLES):
        t_mins = s * _SAMPLE_INTERVAL
        jd_t = jd_sunrise + t_mins * _jd_per_min
        asc = _calculate_ascendant(jd_t, latitude, longitude)
        samples.append((t_mins, asc["sign"]))

    # Detect sign boundaries
    boundaries = [(0, samples[0][1])]  # (minutes_from_sunrise, sign_idx)
    for i in range(1, len(samples)):
        if samples[i][1] != samples[i - 1][1]:
            boundaries.append((samples[i][0], samples[i][1]))

    # Build lagna table from boundaries
    for i, (start_offset, sign_idx) in enumerate(boundaries):
        if i + 1 < len(boundaries):
            end_offset = boundaries[i + 1][0]
        else:
            end_offset = 24 * 60  # full 24h
        start_str = _minutes_to_time((sunrise_mins + start_offset) % 1440)
        end_str = _minutes_to_time((sunrise_mins + end_offset) % 1440)

        # Compute ascendant degree at midpoint for Ganda/Sandhi warning
        mid_offset = (start_offset + end_offset) / 2
        mid_jd = jd_sunrise + (mid_offset / 1440.0)
        try:
            mid_asc = _compute_ascendant(mid_jd, latitude, longitude)
            mid_degree = round(mid_asc.get("longitude", 0) % 30, 1)
        except Exception:
            mid_degree = 15.0  # fallback: middle of sign

        # Ganda = first 3°20' (3.333°), Sandhi = last 3°20' (26.667°)
        ganda_sandhi = None
        if mid_degree < 3.333:
            ganda_sandhi = "ganda"
        elif mid_degree > 26.667:
            ganda_sandhi = "sandhi"

        lagna_table.append({
            "lagna": _RASHI_NAMES[sign_idx],
            "lagna_hindi": _RASHI_NAMES_HINDI[sign_idx],
            "start": start_str,
            "end": end_str,
            "degree": mid_degree,
            "ganda_sandhi": ganda_sandhi,
        })

    # 24. Chandrabalam (Moon strength for each Rashi)
    moon_rashi_idx = int(moon_sid / 30)
    chandrabalam = []
    for i in range(12):
        house_from_moon = ((i - moon_rashi_idx) % 12) + 1
        good = house_from_moon in [1, 3, 6, 7, 10, 11]
        cb_text = _CHANDRABALAM_TEXT[house_from_moon - 1]
        chandrabalam.append({
            "rashi": _RASHI_NAMES[i],
            "house_from_moon": house_from_moon,
            "balam": "Shubh" if good else "Ashubh",
            "good": good,
            "interpretation": cb_text,
        })

    # 25. Tarabalam (Star strength for each Nakshatra)
    from app.astro_engine import NAKSHATRAS as _ALL_NAKS
    moon_nak_idx = nakshatra.get("index", 0)
    tarabalam = []
    tara_names = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyari", "Sadhaka", "Vadha", "Mitra", "Ati-Mitra"]
    for i in range(27):
        tara_num = ((i - moon_nak_idx) % 9)
        tara_name = tara_names[tara_num]
        good = tara_name in ["Sampat", "Kshema", "Sadhaka", "Mitra", "Ati-Mitra"]
        tara_text = _TARA_BALAM_TEXT.get(tara_name, {"en": "", "hi": ""})
        tarabalam.append({
            "nakshatra": _ALL_NAKS[i]["name"] if i < len(_ALL_NAKS) else f"Nak-{i+1}",
            "tara": tara_name,
            "tara_number": tara_num + 1,
            "good": good,
            "interpretation": tara_text,
        })

    # 26. Gowri Panchangam (8 periods, day + night)
    gowri_names_day = ["Udvega", "Chara", "Labha", "Amruta", "Kaala", "Shubha", "Roga", "Dhanada"]
    gowri_names_night = ["Kaala", "Shubha", "Roga", "Dhanada", "Udvega", "Chara", "Labha", "Amruta"]
    gowri_day_dur = dinamana_mins / 8
    gowri_night_dur = ratrimana_mins / 8
    gowri_panchang = []
    for i in range(8):
        gowri_panchang.append({
            "name": gowri_names_day[(day_lord_idx + i) % 8],
            "start": _minutes_to_time(sunrise_mins + i * gowri_day_dur),
            "end": _minutes_to_time(sunrise_mins + (i + 1) * gowri_day_dur),
            "type": "day",
            "quality": "good" if gowri_names_day[(day_lord_idx + i) % 8] in ["Labha", "Amruta", "Shubha", "Dhanada"] else "bad",
        })
    for i in range(8):
        gowri_panchang.append({
            "name": gowri_names_night[(day_lord_idx + i) % 8],
            "start": _minutes_to_time(sunset_mins + i * gowri_night_dur),
            "end": _minutes_to_time(sunset_mins + (i + 1) * gowri_night_dur),
            "type": "night",
            "quality": "good" if gowri_names_night[(day_lord_idx + i) % 8] in ["Labha", "Amruta", "Shubha", "Dhanada"] else "bad",
        })

    # 27. Do Ghati Muhurta (30 muhurtas in a day)
    total_day_mins = 1440
    ghati_duration = total_day_mins / 30
    do_ghati = []
    muhurta_names_30 = ["Rudra", "Ahi", "Mitra", "Pitru", "Vasu", "Varah", "Vishwadeva", "Vidhi",
                        "Satamukhi", "Puruhuta", "Vahini", "Naktanchara", "Varuna", "Aryaman", "Bhaga",
                        "Girisha", "Ajapada", "Ahirbudhnya", "Pushan", "Ashwini", "Yama", "Agni",
                        "Vidhata", "Chanda", "Aditi", "Jeeva", "Vishnu", "Dyumadgadyuti", "Brahma", "Samudra"]
    for i in range(30):
        start_min = sunrise_mins + i * ghati_duration
        do_ghati.append({
            "muhurta": i + 1,
            "name": muhurta_names_30[i] if i < len(muhurta_names_30) else f"M-{i+1}",
            "start": _minutes_to_time(start_min % 1440),
            "end": _minutes_to_time((start_min + ghati_duration) % 1440),
            "quality": "good" if i in [0, 2, 3, 4, 6, 7, 10, 13, 14, 19, 25, 26, 28] else "neutral",
        })

    # 28. Panchaka check (5 elements — inauspicious when Moon in certain nakshatras)
    # 0-based: Dhanishta=22, Shatabhisha=23, P.Bhadrapada=24, U.Bhadrapada=25, Revati=26
    panchaka_nakshatras = [22, 23, 24, 25, 26]  # Dhanishta, Shatabhisha, P.Bhadrapada, U.Bhadrapada, Revati
    is_panchaka = moon_nak_idx in panchaka_nakshatras
    panchaka = {"active": is_panchaka, "rahita": not is_panchaka}

    # 29. Panchanga Shuddhi — composite day-quality score (0-100)
    panchanga_shuddhi = _compute_panchanga_shuddhi(
        tithi_index, tithi["paksha"], weekday, yoga_index + 1, karana_name, nakshatra.get("name", "")
    )

    return {
        # Original contract keys
        "tithi": {
            "name": tithi["name"],
            "number": tithi["number"],
            "paksha": tithi["paksha"],
            "end_time": tithi_end,
            "next": next_tithi["name"],
        },
        "nakshatra": {
            **nakshatra,
            "name_hindi": NAKSHATRA_HINDI.get(nakshatra.get("name", ""), nakshatra.get("name", "")),
            "end_time": nakshatra_end,
            "next": next_nak_name,
            **_nakshatra_category_fields(nakshatra.get("name", "")),
        },
        "yoga": {
            "name": yoga_name,
            "number": yoga_index + 1,
            "end_time": yoga_end,
            "next": next_yoga_name,
            "auspicious": (yoga_index + 1) not in _BAD_YOGA_NUMBERS,
            "quality": "bad" if (yoga_index + 1) in _BAD_YOGA_NUMBERS else "good",
            "interpretation": YOGA_INTERPRETATIONS[yoga_index],
            "interpretation_en": (YOGA_INTERPRETATIONS[yoga_index] or {}).get("en", ""),
            "interpretation_hi": (YOGA_INTERPRETATIONS[yoga_index] or {}).get("hi", ""),
        },
        "karana": {
            "name": karana_name,
            "number": karana_index + 1,
            "end_time": karana_end,
            "second_karana": second_karana_name,
            "second_karana_end_time": second_karana_end,
            "is_vishti": karana_name in _VISHTI_NAMES,
            "type": "chara" if karana_name in _CHARA_KARANA_NAMES else "sthira",
            "auspicious": karana_name not in _VISHTI_NAMES,
        },
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        # Extended data
        "moonrise": sun_times["moonrise"],
        "moonset": sun_times["moonset"],
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "vaar": {
            "name": _VAAR_NAMES[weekday],
            "english": _VAAR_ENGLISH[weekday],
            "number": weekday,
        },
        "dinamana": dinamana_str,
        "ratrimana": ratrimana_str,
        "madhyahna": madhyahna_str,
        "rahu_kaal": rahu_kaal,
        "gulika_kaal": gulika_kaal,
        "yamaganda": yamaganda,
        "abhijit_muhurat": abhijit,
        "brahma_muhurat": brahma,
        "ravi_yoga": ravi_yoga,
        "vijaya_muhurta": vijaya,
        "godhuli_muhurta": godhuli,
        "sayahna_sandhya": sayahna,
        "nishita_muhurta": nishita,
        "pratah_sandhya": pratah,
        "dur_muhurtam": dur_muhurtam,
        "varjyam": varjyam,
        "planetary_positions": planetary_positions,
        "hindu_calendar": hindu_calendar,
        "choghadiya": choghadiya,
        "night_choghadiya": night_choghadiya,
        "ayanamsa": round(ayanamsa, 4),
        "sun_longitude": round(sun_sid, 4),
        "moon_longitude": round(moon_sid, 4),
        # Advanced Panchang
        "hora_table": hora_table,
        "lagna_table": lagna_table,
        "chandrabalam": chandrabalam,
        "tarabalam": tarabalam,
        "gowri_panchang": gowri_panchang,
        "do_ghati_muhurta": do_ghati,
        "panchaka": panchaka,
        "panchanga_shuddhi": panchanga_shuddhi,
        # --- New modules (Wave 1) ---
        **_calculate_wave1_extras(weekday, tithi_index, tithi["name"],
                                  nakshatra.get("name", ""), nakshatra.get("index", 0),
                                  nakshatra_end, tithi_end, date, sunrise_str, sunset_str,
                                  hindu_calendar.get("vikram_samvat", 0),
                                  jd_sunrise, ayanamsa,
                                  hindu_calendar.get("maas", ""),
                                  hindu_calendar.get("paksha", "")),
    }


def _calculate_wave1_extras(
    weekday, tithi_index, tithi_name, nakshatra_name, nakshatra_index,
    nakshatra_end_time, tithi_end_time, date_str, sunrise, sunset, vikram_samvat, jd, ayanamsa,
    hindu_month, paksha,
):
    """Integrate all new Wave 1 modules into panchang output."""
    result = {}
    # panchang_yogas and panchang_directions use 0=Sunday convention.
    # dt.weekday() returns 0=Monday, so convert: Sun=0 → (Mon_idx + 1) % 7
    weekday_sun = (weekday + 1) % 7
    try:
        from app.panchang_yogas import calculate_all_special_yogas, calculate_dagdha_nakshatra
        result["special_yogas"] = calculate_all_special_yogas(weekday_sun, tithi_index, nakshatra_name)
        result["special_yogas"]["dagdha_nakshatra"] = calculate_dagdha_nakshatra(hindu_month, nakshatra_name)
    except Exception:
        result["special_yogas"] = {}
    try:
        from app.panchang_directions import calculate_all_directions
        result["directions"] = calculate_all_directions(weekday_sun, tithi_index, nakshatra_index)
    except Exception:
        result["directions"] = {}
    try:
        from app.panchang_misc import calculate_all_misc
        result["misc"] = calculate_all_misc(
            date_str=date_str, vikram_samvat=vikram_samvat,
            jd=jd, ayanamsha=ayanamsa,
            nakshatra_name=nakshatra_name, nakshatra_end_time=nakshatra_end_time or "",
            sunrise=sunrise, sunset=sunset,
        )
    except Exception:
        result["misc"] = {}
    try:
        from app.panchang_ekadashi import calculate_ekadashi_parana
        result["ekadashi_parana"] = calculate_ekadashi_parana(
            tithi_name=tithi_name,
            tithi_end_time=tithi_end_time or "",
            next_sunrise=sunrise,
        )
    except Exception:
        result["ekadashi_parana"] = None
    try:
        from app.panchang_nivas import calculate_all_nivas
        result["nivas"] = calculate_all_nivas(weekday, tithi_index, nakshatra_index)
    except Exception:
        result["nivas"] = {}
    try:
        from app.panchang_tamil import calculate_all_tamil
        result["tamil"] = calculate_all_tamil(weekday, tithi_index, nakshatra_index)
    except Exception:
        result["tamil"] = {}
    try:
        from app.panchang_samvat import calculate_all_samvat
        _vs = vikram_samvat if vikram_samvat else 2083
        result["samvat"] = calculate_all_samvat(
            vikram_samvat=_vs, maas="", paksha="",
        )
    except Exception:
        result["samvat"] = {}
    try:
        from app.panchang_misc import calculate_chaturmasa
        result["chaturmasa"] = calculate_chaturmasa(hindu_month, tithi_index, paksha)
    except Exception:
        result["chaturmasa"] = {}
    return result
