"""Muhurat rules database for 9 activity-specific muhurats.

Each activity defines favorable/unfavorable tithis, nakshatras, weekdays,
lagnas, months, and conditions to avoid. All names include Hindi translations.
"""
from typing import Any, Dict, List

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
            "Ashwini", "Rohini", "Pushya", "Uttara Phalguni", "Hasta",
            "Chitra", "Swati", "Anuradha", "Uttara Ashadha", "Shravana",
            "Dhanishta", "Shatabhisha", "Uttara Bhadrapada", "Revati",
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
