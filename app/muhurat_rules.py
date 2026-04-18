"""Muhurat rules database for 9 activity-specific muhurats.

Each activity defines favorable/unfavorable tithis, nakshatras, weekdays,
lagnas, months, and conditions to avoid. All names include Hindi translations.
"""
from typing import Any, Dict, List

# ============================================================
# P0 DOSHA TABLES (tests + finder hard/soft blocks)
# ============================================================
# NOTE: These lists use Python weekday numbering: Monday=0 … Sunday=6.
# Values are tithi numbers in Shukla paksha range (1-15). Krishna paksha
# is normalized via normalize_tithi_for_rules().

# Mrityu Yoga (warning) — weekday -> tithi (1-15)
MRITYU_YOGA_TITHI: List[int] = [
    7,   # Monday    + Saptami
    8,   # Tuesday   + Ashtami
    9,   # Wednesday + Navami
    14,  # Thursday  + Chaturdashi
    6,   # Friday    + Shashthi
    4,   # Saturday  + Chaturthi
    1,   # Sunday    + Pratipada
]

# Visha Yoga (hard block) — weekday -> tithi (1-15)
VISHA_YOGA_TITHI: List[int] = [
    6,   # Monday
    7,   # Tuesday
    2,   # Wednesday
    8,   # Thursday
    9,   # Friday
    7,   # Saturday
    4,   # Sunday
]

# ============================================================
# Activity metadata with translations
# ============================================================
MUHURAT_ACTIVITIES: Dict[str, Dict[str, str]] = {
    "marriage": {
        "name": "Vivah Muhurat", "name_hindi": "विवाह मुहूर्त", "icon": "💍",
        "description": "Auspicious time for marriage ceremony",
        "description_hindi": "विवाह संस्कार के लिए शुभ समय",
    },
    "griha_pravesh": {
        "name": "Griha Pravesh", "name_hindi": "गृह प्रवेश", "icon": "🏠",
        "description": "Auspicious time for entering a new home",
        "description_hindi": "नए घर में प्रवेश के लिए शुभ समय",
    },
    "vehicle_purchase": {
        "name": "Vehicle Purchase", "name_hindi": "वाहन खरीद", "icon": "🚗",
        "description": "Auspicious time for buying a vehicle",
        "description_hindi": "वाहन खरीदने के लिए शुभ समय",
    },
    "property_purchase": {
        "name": "Property Purchase", "name_hindi": "भूमि/सम्पत्ति खरीद", "icon": "🏗️",
        "description": "Auspicious time for buying property",
        "description_hindi": "भूमि/सम्पत्ति खरीदने के लिए शुभ समय",
    },
    "mundan": {
        "name": "Mundan", "name_hindi": "मुण्डन संस्कार", "icon": "✂️",
        "description": "Auspicious time for first head shaving",
        "description_hindi": "प्रथम मुण्डन के लिए शुभ समय",
    },
    "annaprashan": {
        "name": "Annaprashan", "name_hindi": "अन्नप्राशन", "icon": "🍚",
        "description": "Auspicious time for first feeding ceremony",
        "description_hindi": "प्रथम अन्न भोजन के लिए शुभ समय",
    },
    "upanayana": {
        "name": "Upanayana", "name_hindi": "उपनयन संस्कार", "icon": "📿",
        "description": "Auspicious time for sacred thread ceremony",
        "description_hindi": "यज्ञोपवीत संस्कार के लिए शुभ समय",
    },
    "nama_karana": {
        "name": "Nama Karana", "name_hindi": "नामकरण", "icon": "📝",
        "description": "Auspicious time for naming ceremony",
        "description_hindi": "नामकरण संस्कार के लिए शुभ समय",
    },
    "business_start": {
        "name": "Business Start", "name_hindi": "व्यापार प्रारम्भ", "icon": "💼",
        "description": "Auspicious time for starting a new business",
        "description_hindi": "नया व्यापार शुरू करने के लिए शुभ समय",
    },
    "bhoomi_puja": {
        "name": "Bhoomi Puja", "name_hindi": "भूमि पूजन", "icon": "🪔",
        "description": "Auspicious time for land worship before construction",
        "description_hindi": "निर्माण से पहले भूमि पूजन के लिए शुभ समय",
    },
    "shilanyas": {
        "name": "Shilanyas", "name_hindi": "शिलान्यास", "icon": "🧱",
        "description": "Auspicious time for foundation stone laying",
        "description_hindi": "शिलान्यास (आधार शिला) के लिए शुभ समय",
    },
    "vastu_shanti": {
        "name": "Vastu Shanti", "name_hindi": "वास्तु शान्ति", "icon": "🕉️",
        "description": "Auspicious time for Vastu Shanti ritual",
        "description_hindi": "वास्तु शान्ति अनुष्ठान के लिए शुभ समय",
    },
    "shop_opening": {
        "name": "Shop Opening", "name_hindi": "दुकान उद्घाटन", "icon": "🏪",
        "description": "Auspicious time for opening a shop / commercial establishment",
        "description_hindi": "दुकान/व्यावसायिक प्रतिष्ठान उद्घाटन के लिए शुभ समय",
    },
    "vidyarambha": {
        "name": "Vidyarambha", "name_hindi": "विद्यारम्भ", "icon": "📚",
        "description": "Auspicious time for starting education / school admission",
        "description_hindi": "शिक्षा आरम्भ / विद्यालय प्रवेश हेतु शुभ समय",
    },
    "shraddha": {
        "name": "Shraddha", "name_hindi": "श्राद्ध", "icon": "🕯️",
        "description": "Auspicious time for Pitru Tarpan / Shraddha rituals",
        "description_hindi": "पितृ तर्पण / श्राद्ध अनुष्ठान हेतु शुभ समय",
    },
    "antyeshti": {
        "name": "Antyeshti", "name_hindi": "अंत्येष्टि", "icon": "🪦",
        "description": "Guidance for funeral timings (avoid major doshas)",
        "description_hindi": "अंत्येष्टि समय-निर्धारण (मुख्य दोषों से बचें)",
    },
    "medical_treatment": {
        "name": "Medical Treatment / Surgery", "name_hindi": "चिकित्सा / शल्य चिकित्सा", "icon": "⚕️",
        "description": "Auspicious time for medical treatment or surgery",
        "description_hindi": "चिकित्सा / शल्य चिकित्सा के लिए शुभ समय",
    },
    "puja_havan": {
        "name": "Puja / Havan / Yagna", "name_hindi": "पूजा / हवन / यज्ञ", "icon": "🪔",
        "description": "Auspicious time for puja, havan, or yagna",
        "description_hindi": "पूजा / हवन / यज्ञ के लिए शुभ समय",
    },
    "legal_court": {
        "name": "Legal / Court Proceedings", "name_hindi": "कानूनी / न्यायालय कार्य", "icon": "⚖️",
        "description": "Auspicious time for legal or court matters",
        "description_hindi": "कानूनी / न्यायालय कार्य के लिए शुभ समय",
    },
    "loan_debt": {
        "name": "Loan / Debt Repayment", "name_hindi": "ऋण / उधार चुकाना", "icon": "💰",
        "description": "Auspicious time for taking or repaying loans",
        "description_hindi": "ऋण / उधार चुकाने के लिए शुभ समय",
    },
    "garbha_dhana": {
        "name": "Garbha Dhana (Conception Ceremony)", "name_hindi": "गर्भाधान संस्कार", "icon": "🌱",
        "description": "Auspicious time for Garbha Dhana samskara",
        "description_hindi": "गर्भाधान संस्कार के लिए शुभ समय",
    },
    "jatakarma": {
        "name": "Jatakarma (Birth Ceremony)", "name_hindi": "जातकर्म संस्कार", "icon": "👶",
        "description": "Auspicious time for birth ceremony",
        "description_hindi": "जातकर्म संस्कार के लिए शुभ समय",
    },
    "nishkramana": {
        "name": "Nishkramana (First Outdoor Outing)", "name_hindi": "निष्क्रमण संस्कार", "icon": "🌞",
        "description": "Auspicious time for first outdoor outing of infant",
        "description_hindi": "निष्क्रमण संस्कार के लिए शुभ समय",
    },
    "karnavedha": {
        "name": "Karnavedha (Ear Piercing)", "name_hindi": "कर्णवेध संस्कार", "icon": "💎",
        "description": "Auspicious time for ear piercing ceremony",
        "description_hindi": "कर्णवेध संस्कार के लिए शुभ समय",
    },
    "kupa_baoli": {
        "name": "Well / Water Body Construction", "name_hindi": "कुआँ / बावली निर्माण", "icon": "💧",
        "description": "Auspicious time for constructing a well or water body",
        "description_hindi": "कुआँ / बावली निर्माण के लिए शुभ समय",
    },
    "door_gate": {
        "name": "Door / Gate Installation", "name_hindi": "दरवाज़ा / द्वार स्थापना", "icon": "🚪",
        "description": "Auspicious time for door or gate installation",
        "description_hindi": "दरवाज़ा / द्वार स्थापना के लिए शुभ समय",
    },
    "vehicle_purchase_ext": {
        "name": "Vehicle Purchase (Extended)", "name_hindi": "वाहन खरीद (विस्तृत)", "icon": "🚙",
        "description": "Extended auspicious time for vehicle purchase with additional checks",
        "description_hindi": "वाहन खरीद (विस्तृत नियमों सहित) के लिए शुभ समय",
    },
    "construction_start": {
        "name": "Construction Start", "name_hindi": "निर्माण प्रारंभ", "icon": "🏗️",
        "description": "Auspicious time for starting construction",
        "description_hindi": "निर्माण प्रारंभ के लिए शुभ समय",
    },
}

# ============================================================
# Localized Reasons
# ============================================================
MUHURAT_REASONS = {
    "favorable_tithi": {"en": "Favorable tithi", "hi": "शुभ तिथि"},
    "unfavorable_tithi": {"en": "Unfavorable tithi", "hi": "अशुभ तिथि"},
    "favorable_nakshatra": {"en": "Favorable nakshatra", "hi": "शुभ नक्षत्र"},
    "unfavorable_nakshatra": {"en": "Unfavorable nakshatra", "hi": "अशुभ नक्षत्र"},
    "favorable_weekday": {"en": "Favorable weekday", "hi": "शुभ वार"},
    "unfavorable_weekday": {"en": "Unfavorable weekday", "hi": "अशुभ वार"},
    "favorable_month": {"en": "Favorable month", "hi": "शुभ मास"},
    "unfavorable_month": {"en": "Unfavorable month", "hi": "अशुभ मास"},
    "krishna_paksha_avoided": {"en": "Krishna Paksha avoided", "hi": "कृष्ण पक्ष वर्जित"},
    "amavasya": {"en": "Amavasya (New Moon)", "hi": "अमावस्या"},
    "ekadashi": {"en": "Ekadashi", "hi": "एकादशी"},
    "bhadra": {"en": "Bhadra Kaal (Earth realm)", "hi": "भद्रा काल (भू-लोक)"},
    "rahu_kaal": {"en": "Rahu Kaal", "hi": "राहु काल"},
    "panchaka": {"en": "Panchaka", "hi": "पंचक"},
    "ganda_moola": {"en": "Ganda Moola", "hi": "गण्ड मूल"},
    "pushya_direction":  {"en": "Pushya Nakshatra — best for travel in all directions", "hi": "पुष्य नक्षत्र — सभी दिशाओं में यात्रा के लिए सर्वोत्तम"},
    "dagdha_tithi":      {"en": "Dagdha Tithi (burned day)", "hi": "दग्ध तिथि"},
    "guru_asta":         {"en": "Jupiter combust (Guru Asta) — marriage forbidden", "hi": "गुरु अस्त — विवाह वर्जित"},
    "shukra_asta":       {"en": "Venus combust (Shukra Asta) — marriage forbidden", "hi": "शुक्र अस्त — विवाह वर्जित"},
    "kula_kanthaka":     {"en": "Kula Kanthaka Dosha (Mars afflicts Moon)", "hi": "कुल कण्टक दोष (मंगल चंद्र से अशुभ भाव में)"},
    "sankranti":         {"en": "Sankranti (Sun sign ingress) — inauspicious", "hi": "संक्रान्ति — अशुभ काल"},
    "retrograde_jupiter":{"en": "Jupiter retrograde (Guru Vakri) — samskaras forbidden", "hi": "गुरु वक्री — संस्कार वर्जित"},
    "retrograde_saturn": {"en": "Saturn retrograde (Shani Vakri) — griha/property inauspicious", "hi": "शनि वक्री — गृह/सम्पत्ति कार्य अशुभ"},
    "simha_surya":       {"en": "Sun in Leo (Simha Surya) — marriage inauspicious", "hi": "सूर्य सिंह राशि — विवाह अशुभ"},
    "chandra_balam_weak":{"en": "Chandra Balam weak for your birth Moon", "hi": "जन्म चंद्र से चंद्रबल कमज़ोर"},
    "chandra_balam_good":{"en": "Chandra Balam strong for your birth Moon", "hi": "जन्म चंद्र से चंद्रबल शुभ"},
    "tara_balam_bad":    {"en": "Tara Balam unfavorable for your birth nakshatra", "hi": "जन्म नक्षत्र से तारा बल अशुभ"},
    "tara_balam_good":   {"en": "Tara Balam favorable for your birth nakshatra", "hi": "जन्म नक्षत्र से तारा बल शुभ"},
}

# ============================================================
# DAGDHA TITHI — Burned day: specific Tithi + Weekday combos
# (Muhurta Chintamani, Shubhashubha Prakarana)
# Weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
# Tithi: normalised 1-15
# ============================================================
DAGDHA_TITHIS: Dict[int, int] = {
    6: 2,   # Sunday  + Dwitiya (2)
    0: 7,   # Monday  + Saptami (7)
    1: 12,  # Tuesday + Dwadashi (12)
    2: 3,   # Wednesday + Tritiya (3)
    3: 11,  # Thursday + Ekadashi (11)
    4: 6,   # Friday  + Shashthi (6)
    5: 9,   # Saturday + Navami (9)
}

# ============================================================
# Rules per activity
# ============================================================
# Weekdays: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun (Python convention)
# Tithis: 1-15 Shukla (Pratipada-Purnima), mapped from 1-30 engine index
# Nakshatras: English names matching astro_engine.py NAKSHATRAS list

MUHURAT_RULES: Dict[str, Dict[str, Any]] = {
    "marriage": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Magha", "Uttara Phalguni", "Hasta",
            "Swati", "Anuradha", "Moola", "Uttara Ashadha", "Shravana",
            "Dhanishta", "Uttara Bhadrapada", "Revati",
        ],
        "favorable_weekdays": [0, 1, 2, 3, 4],  # Mon-Fri
        "favorable_lagnas": ["Tula", "Dhanu", "Mithuna", "Kanya", "Meena"],  # Simha excluded
        "favorable_months": ["Magha", "Phalguna", "Vaishakha", "Jyeshtha"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_jupiter",
        ],
        "samskara": True,  # flag: apply Guru-Vakri + Chandra/Tara Balam checks
    },
    "griha_pravesh": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni", "Hasta",
            "Anuradha", "Uttara Ashadha", "Uttara Bhadrapada", "Revati",
            # also retained from original for backward compat
            "Ashwini", "Chitra", "Swati", "Shravana",
            "Dhanishta", "Shatabhisha",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Simha", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_jupiter", "retrograde_saturn",
        ],
        "samskara": True,
        # Extended Griha Pravesh rules
        "uttarayan_preferred": True,   # Makar Sankranti → Karka Sankranti (roughly Jan–Jul)
        "notes_extended": (
            "Uttarayan (Jan–Jul, Sun in Capricorn→Gemini) is strongly preferred. "
            "Pushya and Rohini nakshatras are especially auspicious — Pushya is ruled by "
            "Brihaspati (Jupiter) ensuring divine blessing, and Rohini by the Moon ensuring "
            "prosperity and comfort in the new home. "
            "Best lagnas: Vrishabha (stability), Simha (strength), Dhanu (expansion)."
        ),
    },
    "vehicle_purchase": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Anuradha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": ["Chaitra", "Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
    },
    "property_purchase": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Pushya", "Uttara Phalguni", "Hasta",
            "Chitra", "Swati", "Anuradha", "Uttara Ashadha", "Shravana",
            "Dhanishta", "Shatabhisha", "Uttara Bhadrapada", "Revati",
        ],
        "favorable_weekdays": [0, 1, 2, 3, 4],  # Mon-Fri (Tue ok for aggressive deals)
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Simha", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_saturn",
        ],
        "samskara": False,
    },
    "mundan": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Mrigashira", "Pushya", "Punarvasu", "Hasta",
            "Chitra", "Swati", "Shravana", "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Chaitra", "Vaishakha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": True,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_jupiter",
        ],
        "samskara": True,
    },
    "annaprashan": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Pushya", "Punarvasu",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Shravana",
            "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": True,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "sankranti", "retrograde_jupiter",
        ],
        "samskara": True,
    },
    "upanayana": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Hasta", "Chitra", "Swati", "Pushya", "Dhanishta", "Ashwini",
            "Punarvasu", "Shravana", "Revati", "Uttara Phalguni",
            "Uttara Ashadha", "Uttara Bhadrapada",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Chaitra", "Phalguna", "Magha", "Vaishakha"],
        "avoid_krishna_paksha": True,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_jupiter",
        ],
        "samskara": True,
    },
    "nama_karana": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Punarvasu", "Pushya",
            "Magha", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
            "Vishakha", "Anuradha", "Uttara Ashadha", "Shravana",
            "Dhanishta", "Shatabhisha", "Uttara Bhadrapada", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": [],  # naming can happen any month (11th day from birth)
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti", "retrograde_jupiter",
        ],
        "samskara": True,
    },
    "business_start": {
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Anuradha", "Shravana",
            "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Chaitra", "Vaishakha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
    },
    "bhoomi_puja": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Hasta", "Uttara Phalguni",
            "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Revati",
            "Uttara Bhadrapada",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_saturn",
        ],
        "samskara": False,
    },
    "shilanyas": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Pushya", "Hasta", "Uttara Phalguni",
            "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Revati",
        ],
        "favorable_weekdays": [2, 3, 4],  # Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_saturn",
        ],
        "samskara": False,
    },
    "vastu_shanti": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Pushya", "Hasta", "Swati", "Anuradha",
            "Shravana", "Revati", "Uttara Bhadrapada",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Vaishakha", "Jyeshtha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti",
        ],
        "samskara": False,
    },
    "shop_opening": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Anuradha", "Shravana",
            "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": ["Chaitra", "Vaishakha", "Magha", "Phalguna"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
    },
    "vidyarambha": {
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Punarvasu", "Pushya", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Anuradha", "Shravana",
            "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],  # Mon, Wed, Thu, Fri
        "favorable_lagnas": ["Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": True,
        "avoid_conditions": ["bhadra", "panchaka", "ganda_moola", "amavasya", "sankranti", "retrograde_jupiter"],
        "samskara": True,
    },
    "shraddha": {
        "favorable_tithis": [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15],
        "favorable_nakshatras": [
            "Rohini", "Pushya", "Hasta", "Swati", "Anuradha",
            "Shravana", "Revati", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada",
        ],
        "favorable_weekdays": [0, 1, 2, 3, 4, 5, 6],
        "favorable_lagnas": ["Karka", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": ["Bhadrapada", "Ashwin"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["bhadra", "panchaka", "ganda_moola", "sankranti"],
        "samskara": True,
    },
    "antyeshti": {
        "favorable_tithis": [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 15],
        "favorable_nakshatras": [
            "Ashwini", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
            "Pushya", "Uttara Phalguni", "Hasta", "Swati", "Anuradha",
            "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Uttara Bhadrapada", "Revati",
        ],
        "favorable_weekdays": [0, 1, 2, 3, 4, 5, 6],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["bhadra", "panchaka", "ganda_moola", "sankranti"],
        "samskara": True,
    },
    # ── New activities (Sprint II) ────────────────────────────────────────
    "medical_treatment": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Ashwini", "Pushya", "Hasta", "Shravana", "Mrigashira",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Ashwini nakshatra (deity: Ashwini Kumaras — celestial physicians) is especially auspicious. Avoid Rahu Kaal.",
        "dosha_free": True,
    },
    "puja_havan": {
        # good_vara: Sunday=6, Monday=0, Wednesday=2, Thursday=3, Friday=4
        "favorable_tithis": [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 15],
        "favorable_nakshatras": [
            "Rohini", "Pushya", "Uttara Phalguni", "Hasta", "Shravana",
            "Uttara Ashadha", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4, 6],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Full moon (Purnima) and Ekadashi are especially auspicious for puja.",
        "dosha_free": False,
    },
    "legal_court": {
        # good_vara: Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Saturday=5, Tuesday=1
        "favorable_tithis": [2, 3, 5, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Punarvasu", "Pushya", "Hasta", "Uttara Phalguni",
        ],
        "favorable_weekdays": [2, 3, 4],
        "favorable_lagnas": ["Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Mercury-ruled days (Wednesday) are best for legal matters.",
        "dosha_free": True,
    },
    "loan_debt": {
        # good_vara: Wednesday=2, Thursday=3, Friday=4, Monday=0
        # avoid_vara: Saturday=5
        "favorable_tithis": [2, 5, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Pushya", "Hasta", "Shravana", "Uttara Phalguni",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Avoid borrowing on Amavasya. Repayment is best on waxing moon days.",
        "dosha_free": False,
    },
    "garbha_dhana": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5, Sunday=6
        "favorable_tithis": [4, 6, 8, 10, 12, 14],  # even tithis for son
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Uttara Phalguni", "Uttara Ashadha",
            "Uttara Bhadrapada", "Anuradha", "Dhanishta",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti", "retrograde_jupiter"],
        "samskara": True,
        "notes": "Even tithis in Shukla Paksha preferred. Avoid Vishti Karana.",
        "dosha_free": True,
    },
    "jatakarma": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [1, 2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni", "Uttara Ashadha",
            "Uttara Bhadrapada", "Shravana", "Dhanishta", "Revati",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": True,
        "notes": "Performed within 10 days of birth. Time of birth nakshatra is primary consideration.",
        "dosha_free": False,
    },
    "nishkramana": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4, Sunday=6
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Hasta", "Shravana", "Revati", "Punarvasu",
        ],
        "favorable_weekdays": [0, 2, 3, 4, 6],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": True,
        "notes": "Performed in 4th month. Sun or Moon nakshatra at time is auspicious.",
        "dosha_free": False,
    },
    "karnavedha": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Hasta", "Shravana", "Uttara Phalguni",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": True,
        "notes": "6th or 12th month after birth. Avoid Rahu Kaal.",
        "dosha_free": False,
    },
    "kupa_baoli": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
            "Hasta", "Shravana", "Shatabhisha",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Karka", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Water-related nakshatras (Ardra, Shatabhisha, Purva Ashadha) are especially good.",
        "dosha_free": False,
    },
    "door_gate": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Hasta", "Uttara Phalguni",
            "Uttara Ashadha", "Uttara Bhadrapada",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Uttara nakshatras (Uttara Phalguni, Uttara Ashadha, Uttara Bhadrapada) are most auspicious.",
        "dosha_free": False,
    },
    "vehicle_purchase_ext": {
        # good_vara: Monday=0, Wednesday=2, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Hasta", "Uttara Phalguni",
            "Anuradha", "Shravana",
        ],
        "favorable_weekdays": [0, 2, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu", "Meena"],
        "favorable_months": [],
        "avoid_krishna_paksha": False,
        "avoid_conditions": ["rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya", "sankranti"],
        "samskara": False,
        "notes": "Avoid Ashtami and Chaturdashi. Saturn hora during purchase is unfavourable.",
        "dosha_free": True,
    },
    "construction_start": {
        # good_vara: Monday=0, Wednesday=2, Thursday=3, Friday=4
        # avoid_vara: Tuesday=1, Saturday=5
        "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "favorable_nakshatras": [
            "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni", "Uttara Ashadha",
            "Uttara Bhadrapada", "Hasta", "Anuradha",
        ],
        "favorable_weekdays": [0, 2, 3, 4],
        "favorable_lagnas": ["Vrishabha", "Mithuna", "Kanya", "Tula", "Dhanu"],
        "favorable_months": ["Margashirsha", "Pausha", "Magha", "Phalguna", "Chaitra", "Vaishakha", "Jyeshtha"],
        "avoid_krishna_paksha": False,
        "avoid_conditions": [
            "rahu_kaal", "bhadra", "panchaka", "ganda_moola", "amavasya",
            "ekadashi", "sankranti", "retrograde_saturn",
        ],
        "samskara": False,
        "notes": "Month-based rule: Margashirsha to Jyeshtha months are preferred. Avoid Ashadha and Shraavana.",
        "dosha_free": True,
    },
}


# ============================================================
# DOSHA CANCELLATION RULES
# ============================================================
DOSHA_CANCELLATIONS: Dict[str, Dict[str, Any]] = {
    "vishti": {
        "cancelled_by": ["pushya_nakshatra", "abhijit_muhurat", "guru_pushya_yoga"],
        "description": "Vishti/Bhadra Karana dosha is cancelled if Pushya nakshatra is active, or during Abhijit Muhurat",
        "description_hi": "पुष्य नक्षत्र या अभिजित मुहूर्त में भद्रा/विष्टि दोष समाप्त हो जाता है",
    },
    "rahu_kaal": {
        "cancelled_by": ["abhijit_muhurat"],
        "description": "Rahu Kaal dosha is partially cancelled during Abhijit Muhurat (midday)",
        "description_hi": "अभिजित मुहूर्त में राहु काल का प्रभाव कम होता है",
    },
    "ashtami_chaturdashi": {
        "cancelled_by": ["special_yoga_active", "guru_hora"],
        "description": "8th and 14th tithi dosha is reduced when special yogas (Sarvartha Siddhi, Amrit Siddhi) are active",
        "description_hi": "अष्टमी/चतुर्दशी दोष विशेष योग (सर्वार्थ सिद्धि, अमृत सिद्धि) में कम होता है",
    },
}


# ============================================================
# Helper functions
# ============================================================

def get_activity_info(activity_key: str) -> Dict[str, str]:
    """Get activity name, Hindi name, icon, description."""
    return MUHURAT_ACTIVITIES.get(activity_key, {})


def get_activity_rules(activity_key: str) -> Dict[str, Any]:
    """Get the full rule set for an activity."""
    return MUHURAT_RULES.get(activity_key, {})


def get_all_activities() -> List[Dict[str, str]]:
    """Return list of all activity keys with metadata."""
    return [{"key": k, **v} for k, v in MUHURAT_ACTIVITIES.items()]


def normalize_tithi_for_rules(tithi_index: int) -> int:
    """Convert engine tithi index (1-30) to rule tithi (1-15).
    Krishna paksha tithis 16-29 map to 1-14, Amavasya 30 stays 30.
    """
    if tithi_index <= 15:
        return tithi_index
    if tithi_index == 30:
        return 30  # Amavasya
    return tithi_index - 15


def check_day_favorable(
    activity_key: str,
    tithi_index: int,
    paksha: str,
    nakshatra_name: str,
    weekday: int,
    hindu_month: str = "",
) -> Dict[str, Any]:
    """Check if a day is favorable for a given activity.
    Returns dict with: favorable (bool), reasons (list of str), score (0-100).
    """
    rules = MUHURAT_RULES.get(activity_key)
    if not rules:
        return {"favorable": False, "reasons": ["Unknown activity"], "score": 0}

    reasons_good: List[str] = []
    reasons_bad: List[str] = []
    reasons_good_hindi: List[str] = []
    reasons_bad_hindi: List[str] = []
    norm_tithi = normalize_tithi_for_rules(tithi_index)

    def _add_good(key: str):
        reasons_good.append(MUHURAT_REASONS[key]["en"])
        reasons_good_hindi.append(MUHURAT_REASONS[key]["hi"])

    def _add_bad(key: str):
        reasons_bad.append(MUHURAT_REASONS[key]["en"])
        reasons_bad_hindi.append(MUHURAT_REASONS[key]["hi"])

    # Check Krishna Paksha avoidance
    if rules["avoid_krishna_paksha"] and paksha.lower() == "krishna":
        _add_bad("krishna_paksha_avoided")

    # Tithi check
    if norm_tithi in rules["favorable_tithis"]:
        _add_good("favorable_tithi")
    elif norm_tithi == 30:
        _add_bad("amavasya")
    else:
        _add_bad("unfavorable_tithi")

    # Nakshatra check
    if nakshatra_name in rules["favorable_nakshatras"]:
        _add_good("favorable_nakshatra")
    else:
        _add_bad("unfavorable_nakshatra")

    # Weekday check
    if weekday in rules["favorable_weekdays"]:
        _add_good("favorable_weekday")
    else:
        _add_bad("unfavorable_weekday")

    # Month check (empty = all months ok)
    if rules["favorable_months"]:
        if hindu_month in rules["favorable_months"]:
            _add_good("favorable_month")
        else:
            _add_bad("unfavorable_month")

    # Avoid conditions (checked externally, but flag if tithi is Ekadashi/Amavasya)
    if "ekadashi" in rules["avoid_conditions"] and norm_tithi == 11:
        _add_bad("ekadashi")
    if "amavasya" in rules["avoid_conditions"] and norm_tithi == 30:
        _add_bad("amavasya")

    # Score: good reasons add points, bad reasons subtract
    score = max(0, min(100, len(reasons_good) * 25 - len(reasons_bad) * 25 + 50))
    favorable = len(reasons_bad) == 0 and len(reasons_good) >= 2

    return {
        "favorable": favorable,
        "score": score,
        "reasons_good": reasons_good,
        "reasons_bad": reasons_bad,
        "reasons_good_hindi": reasons_good_hindi,
        "reasons_bad_hindi": reasons_bad_hindi,
    }
