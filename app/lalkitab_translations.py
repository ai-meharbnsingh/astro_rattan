"""
lalkitab_translations.py — Lal Kitab bilingual constants
=========================================================
All Hindi translations for Lal Kitab entities.
Hindi text uses Devanagari script, NOT romanized Hindi.
"""

# Planet names in Hindi
PLANET_NAMES_HI: dict[str, str] = {
    "Sun": "सूर्य",
    "Moon": "चंद्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "गुरु",
    "Venus": "शुक्र",
    "Saturn": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
}

# Sign names in Hindi
SIGN_NAMES_HI: dict[str, str] = {
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
    "Aquarius": "कुंभ",
    "Pisces": "मीन",
}

# LK House names in Hindi
HOUSE_NAMES_HI: dict[int, str] = {
    1: "प्रथम भाव",
    2: "द्वितीय भाव",
    3: "तृतीय भाव",
    4: "चतुर्थ भाव",
    5: "पंचम भाव",
    6: "षष्ठ भाव",
    7: "सप्तम भाव",
    8: "अष्टम भाव",
    9: "नवम भाव",
    10: "दशम भाव",
    11: "एकादश भाव",
    12: "द्वादश भाव",
}

# Dignity labels in Hindi
DIGNITY_LABELS_HI: dict[str, str] = {
    "Exalted": "उच्च",
    "Own Sign": "स्वराशि",
    "Friendly": "मित्र राशि",
    "Neutral": "सम राशि",
    "Enemy": "शत्रु राशि",
    "Debilitated": "नीच",
}

# Rin (Debt) types in Hindi
RIN_TYPES_HI: dict[str, str] = {
    "pitru": "पितृ ऋण",
    "matru": "मातृ ऋण",
    "stri": "स्त्री ऋण",
    "dev": "देव ऋण",
    "bhai": "भ्रातृ ऋण",
    "shatru": "शत्रु ऋण",
    "pitamah": "पितामह ऋण",
}

# Activation status in Hindi
ACTIVATION_STATUS_HI: dict[str, str] = {
    "active": "सक्रिय",
    "latent": "सुप्त",
    "passive": "निष्क्रिय",
}
