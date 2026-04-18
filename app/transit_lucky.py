"""
transit_lucky.py -- Lucky Metadata Derivation Module
=====================================================
Derives deterministic (non-random) lucky numbers, colors, times, gemstones,
mantras, do's/don'ts, mood, and compatible signs from real planetary positions.

All text is bilingual (English + Hindi).
Same date + sign = same output (no randomness).

Provides:
  - derive_lucky_number(moon_nakshatra_index, moon_pada, date_str) -> int
  - derive_lucky_color(sign, moon_pada) -> Dict[str, str]
  - derive_compatible_sign(sign, transit_dignities) -> Dict[str, str]
  - derive_mood(overall_score) -> Dict[str, str]
  - derive_dos(planet_houses, planet_dignities) -> list
  - derive_donts(planet_houses, planet_dignities) -> list
  - derive_lucky_time(sign, ruler) -> Dict[str, str]
  - derive_gemstone(ruler) -> Dict
  - derive_mantra(ruler) -> str
  - get_all_lucky_metadata(sign, moon_nakshatra_index, moon_pada, date_str,
                           overall_score, planet_houses, planet_dignities,
                           transit_dignities) -> Dict
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple


# ---- Zodiac Element & Ruler Mappings ----------------------------------------

ELEMENTS: Dict[str, str] = {
    "aries": "fire", "taurus": "earth", "gemini": "air", "cancer": "water",
    "leo": "fire", "virgo": "earth", "libra": "air", "scorpio": "water",
    "sagittarius": "fire", "capricorn": "earth", "aquarius": "air", "pisces": "water",
}

RULERS: Dict[str, str] = {
    "aries": "Mars", "taurus": "Venus", "gemini": "Mercury", "cancer": "Moon",
    "leo": "Sun", "virgo": "Mercury", "libra": "Venus", "scorpio": "Mars",
    "sagittarius": "Jupiter", "capricorn": "Saturn", "aquarius": "Saturn", "pisces": "Jupiter",
}

SIGN_HINDI: Dict[str, str] = {
    "aries": "\u092e\u0947\u0937", "taurus": "\u0935\u0943\u0937\u092d",
    "gemini": "\u092e\u093f\u0925\u0941\u0928", "cancer": "\u0915\u0930\u094d\u0915",
    "leo": "\u0938\u093f\u0902\u0939", "virgo": "\u0915\u0928\u094d\u092f\u093e",
    "libra": "\u0924\u0941\u0932\u093e", "scorpio": "\u0935\u0943\u0936\u094d\u091a\u093f\u0915",
    "sagittarius": "\u0927\u0928\u0941", "capricorn": "\u092e\u0915\u0930",
    "aquarius": "\u0915\u0941\u0902\u092d", "pisces": "\u092e\u0940\u0928",
}

# Trine groupings (same element)
_TRINES: Dict[str, List[str]] = {
    "fire": ["aries", "leo", "sagittarius"],
    "earth": ["taurus", "virgo", "capricorn"],
    "air": ["gemini", "libra", "aquarius"],
    "water": ["cancer", "scorpio", "pisces"],
}

# ---- House Classification ---------------------------------------------------

BENEFIC_HOUSES: set = {1, 2, 4, 5, 7, 9, 10, 11}
MALEFIC_HOUSES: set = {6, 8, 12}
NEUTRAL_HOUSES: set = {3}

# ---- Lucky Colors (per element, 4 variants for Moon pada selection) ----------

ELEMENT_COLORS: Dict[str, List[Dict[str, str]]] = {
    "fire": [
        {"en": "Red", "hi": "\u0932\u093e\u0932"},
        {"en": "Orange", "hi": "\u0928\u093e\u0930\u0902\u0917\u0940"},
        {"en": "Saffron", "hi": "\u0915\u0947\u0938\u0930\u0940"},
        {"en": "Coral", "hi": "\u092e\u0942\u0902\u0917\u093e \u0930\u0902\u0917"},
    ],
    "earth": [
        {"en": "Green", "hi": "\u0939\u0930\u093e"},
        {"en": "Brown", "hi": "\u092d\u0942\u0930\u093e"},
        {"en": "Olive", "hi": "\u091c\u0948\u0924\u0942\u0928\u0940"},
        {"en": "Khaki", "hi": "\u0916\u093e\u0915\u0940"},
    ],
    "air": [
        {"en": "Yellow", "hi": "\u092a\u0940\u0932\u093e"},
        {"en": "White", "hi": "\u0938\u092b\u0947\u0926"},
        {"en": "Light Blue", "hi": "\u0939\u0932\u094d\u0915\u093e \u0928\u0940\u0932\u093e"},
        {"en": "Cream", "hi": "\u0915\u094d\u0930\u0940\u092e"},
    ],
    "water": [
        {"en": "Blue", "hi": "\u0928\u0940\u0932\u093e"},
        {"en": "Silver", "hi": "\u091a\u093e\u0902\u0926\u0940 \u0930\u0902\u0917"},
        {"en": "Sea Green", "hi": "\u0938\u092e\u0941\u0926\u094d\u0930\u0940 \u0939\u0930\u093e"},
        {"en": "Pearl White", "hi": "\u092e\u094b\u0924\u0940 \u0938\u092b\u0947\u0926"},
    ],
}

# ---- Gemstone Data (per ruling planet) ---------------------------------------

GEMSTONE_DATA: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "gem": {"en": "Ruby (Manik)", "hi": "\u092e\u093e\u0923\u093f\u0915\u094d\u092f"},
        "metal": {"en": "Gold", "hi": "\u0938\u094b\u0928\u093e"},
        "finger": {"en": "Ring finger", "hi": "\u0905\u0928\u093e\u092e\u093f\u0915\u093e"},
        "day": {"en": "Sunday", "hi": "\u0930\u0935\u093f\u0935\u093e\u0930"},
    },
    "Moon": {
        "gem": {"en": "Pearl (Moti)", "hi": "\u092e\u094b\u0924\u0940"},
        "metal": {"en": "Silver", "hi": "\u091a\u093e\u0902\u0926\u0940"},
        "finger": {"en": "Little finger", "hi": "\u0915\u0928\u093f\u0937\u094d\u0920\u093e"},
        "day": {"en": "Monday", "hi": "\u0938\u094b\u092e\u0935\u093e\u0930"},
    },
    "Mars": {
        "gem": {"en": "Red Coral (Moonga)", "hi": "\u092e\u0942\u0902\u0917\u093e"},
        "metal": {"en": "Copper", "hi": "\u0924\u093e\u0902\u092c\u093e"},
        "finger": {"en": "Ring finger", "hi": "\u0905\u0928\u093e\u092e\u093f\u0915\u093e"},
        "day": {"en": "Tuesday", "hi": "\u092e\u0902\u0917\u0932\u0935\u093e\u0930"},
    },
    "Mercury": {
        "gem": {"en": "Emerald (Panna)", "hi": "\u092a\u0928\u094d\u0928\u093e"},
        "metal": {"en": "Gold", "hi": "\u0938\u094b\u0928\u093e"},
        "finger": {"en": "Little finger", "hi": "\u0915\u0928\u093f\u0937\u094d\u0920\u093e"},
        "day": {"en": "Wednesday", "hi": "\u092c\u0941\u0927\u0935\u093e\u0930"},
    },
    "Jupiter": {
        "gem": {"en": "Yellow Sapphire (Pukhraj)", "hi": "\u092a\u0941\u0916\u0930\u093e\u091c"},
        "metal": {"en": "Gold", "hi": "\u0938\u094b\u0928\u093e"},
        "finger": {"en": "Index finger", "hi": "\u0924\u0930\u094d\u091c\u0928\u0940"},
        "day": {"en": "Thursday", "hi": "\u0917\u0941\u0930\u0941\u0935\u093e\u0930"},
    },
    "Venus": {
        "gem": {"en": "Diamond (Heera)", "hi": "\u0939\u0940\u0930\u093e"},
        "metal": {"en": "Silver", "hi": "\u091a\u093e\u0902\u0926\u0940"},
        "finger": {"en": "Middle finger", "hi": "\u092e\u0927\u094d\u092f\u092e\u093e"},
        "day": {"en": "Friday", "hi": "\u0936\u0941\u0915\u094d\u0930\u0935\u093e\u0930"},
    },
    "Saturn": {
        "gem": {"en": "Blue Sapphire (Neelam)", "hi": "\u0928\u0940\u0932\u092e"},
        "metal": {"en": "Iron", "hi": "\u0932\u094b\u0939\u093e"},
        "finger": {"en": "Middle finger", "hi": "\u092e\u0927\u094d\u092f\u092e\u093e"},
        "day": {"en": "Saturday", "hi": "\u0936\u0928\u093f\u0935\u093e\u0930"},
    },
}

# ---- Mantras (per ruling planet) --------------------------------------------

PLANET_MANTRAS: Dict[str, str] = {
    "Sun": "Om Hraam Hreem Hroum Sah Suryaya Namah",
    "Moon": "Om Shraam Shreem Shroum Sah Chandraya Namah",
    "Mars": "Om Kraam Kreem Kroum Sah Bhaumaya Namah",
    "Mercury": "Om Braam Breem Broum Sah Budhaya Namah",
    "Jupiter": "Om Graam Greem Groum Sah Gurave Namah",
    "Venus": "Om Draam Dreem Droum Sah Shukraya Namah",
    "Saturn": "Om Praam Preem Proum Sah Shanaischaraya Namah",
}

# ---- Mood Map (score range -> bilingual label) -------------------------------

MOOD_MAP: List[Tuple[int, int, Dict[str, str]]] = [
    (9, 10, {"en": "Excellent", "hi": "\u0909\u0924\u094d\u0915\u0943\u0937\u094d\u091f"}),
    (7, 8, {"en": "Optimistic", "hi": "\u0906\u0936\u093e\u0935\u093e\u0926\u0940"}),
    (5, 6, {"en": "Steady", "hi": "\u0938\u094d\u0925\u093f\u0930"}),
    (3, 4, {"en": "Cautious", "hi": "\u0938\u0924\u0930\u094d\u0915"}),
    (1, 2, {"en": "Challenging", "hi": "\u091a\u0941\u0928\u094c\u0924\u0940\u092a\u0942\u0930\u094d\u0923"}),
]

# ---- Planetary Hora Time Ranges (24h cycle, each planet rules ~1h) -----------
# Standard planetary hora order: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
# repeats every 7 hours.  We assign time ranges for the sign's ruler.

_HORA_ORDER: List[str] = [
    "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars",
]

_HORA_TIMES: List[Dict[str, str]] = [
    {"en": "6:00 AM - 7:00 AM", "hi": "\u0938\u0941\u092c\u0939 6 - 7 \u092c\u091c\u0947"},
    {"en": "7:00 AM - 8:00 AM", "hi": "\u0938\u0941\u092c\u0939 7 - 8 \u092c\u091c\u0947"},
    {"en": "8:00 AM - 9:00 AM", "hi": "\u0938\u0941\u092c\u0939 8 - 9 \u092c\u091c\u0947"},
    {"en": "9:00 AM - 10:00 AM", "hi": "\u0938\u0941\u092c\u0939 9 - 10 \u092c\u091c\u0947"},
    {"en": "10:00 AM - 11:00 AM", "hi": "\u0938\u0941\u092c\u0939 10 - 11 \u092c\u091c\u0947"},
    {"en": "11:00 AM - 12:00 PM", "hi": "\u0938\u0941\u092c\u0939 11 - \u0926\u094b\u092a\u0939\u0930 12 \u092c\u091c\u0947"},
    {"en": "12:00 PM - 1:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 12 - 1 \u092c\u091c\u0947"},
    {"en": "1:00 PM - 2:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 1 - 2 \u092c\u091c\u0947"},
    {"en": "2:00 PM - 3:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 2 - 3 \u092c\u091c\u0947"},
    {"en": "3:00 PM - 4:00 PM", "hi": "\u0926\u094b\u092a\u0939\u0930 3 - 4 \u092c\u091c\u0947"},
    {"en": "4:00 PM - 5:00 PM", "hi": "\u0936\u093e\u092e 4 - 5 \u092c\u091c\u0947"},
    {"en": "5:00 PM - 6:00 PM", "hi": "\u0936\u093e\u092e 5 - 6 \u092c\u091c\u0947"},
]

# ---- Do's and Don'ts Templates (planet x benefic/malefic) --------------------
# ~6 do's per planet-benefic, ~6 don'ts per planet-malefic = 42 each

DOS_TEMPLATES: Dict[Tuple[str, str], List[Dict[str, str]]] = {
    # -- Sun --
    ("Sun", "benefic"): [
        {"en": "Take initiative on leadership opportunities", "hi": "\u0928\u0947\u0924\u0943\u0924\u094d\u0935 \u0915\u0947 \u0905\u0935\u0938\u0930\u094b\u0902 \u092a\u0930 \u092a\u0939\u0932 \u0915\u0930\u0947\u0902"},
        {"en": "Seek recognition for your achievements", "hi": "\u0905\u092a\u0928\u0940 \u0909\u092a\u0932\u092c\u094d\u0927\u093f\u092f\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u092a\u0939\u091a\u093e\u0928 \u092a\u094d\u0930\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Connect with father or authority figures", "hi": "\u092a\u093f\u0924\u093e \u092f\u093e \u0905\u0927\u093f\u0915\u093e\u0930\u0940 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u092f\u094b\u0902 \u0938\u0947 \u091c\u0941\u0921\u093c\u0947\u0902"},
        {"en": "Focus on self-confidence and vitality", "hi": "\u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938 \u0914\u0930 \u090a\u0930\u094d\u091c\u093e \u092a\u0930 \u0927\u094d\u092f\u093e\u0928 \u0926\u0947\u0902"},
        {"en": "Start new ventures with confidence", "hi": "\u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938 \u0938\u0947 \u0928\u090f \u0915\u093e\u0930\u094d\u092f \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902"},
        {"en": "Spend time outdoors in sunlight", "hi": "\u0927\u0942\u092a \u092e\u0947\u0902 \u092c\u093e\u0939\u0930 \u0938\u092e\u092f \u092c\u093f\u0924\u093e\u090f\u0902"},
    ],
    # -- Moon --
    ("Moon", "benefic"): [
        {"en": "Nurture emotional bonds with loved ones", "hi": "\u092a\u094d\u0930\u093f\u092f\u091c\u0928\u094b\u0902 \u0915\u0947 \u0938\u093e\u0925 \u092d\u093e\u0935\u0928\u093e\u0924\u094d\u092e\u0915 \u0938\u0902\u092c\u0902\u0927\u094b\u0902 \u0915\u094b \u092a\u094b\u0937\u093f\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Trust your intuition in decisions", "hi": "\u0928\u093f\u0930\u094d\u0923\u092f\u094b\u0902 \u092e\u0947\u0902 \u0905\u092a\u0928\u0940 \u0905\u0902\u0924\u0930\u094d\u0926\u0943\u0937\u094d\u091f\u093f \u092a\u0930 \u092d\u0930\u094b\u0938\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Practice meditation for inner peace", "hi": "\u0906\u0902\u0924\u0930\u093f\u0915 \u0936\u093e\u0902\u0924\u093f \u0915\u0947 \u0932\u093f\u090f \u0927\u094d\u092f\u093e\u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Spend quality time with your mother", "hi": "\u0905\u092a\u0928\u0940 \u092e\u093e\u0901 \u0915\u0947 \u0938\u093e\u0925 \u0917\u0941\u0923\u0935\u0924\u094d\u0924\u093e \u0938\u092e\u092f \u092c\u093f\u0924\u093e\u090f\u0902"},
        {"en": "Engage in creative and artistic activities", "hi": "\u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915 \u0914\u0930 \u0915\u0932\u093e\u0924\u094d\u092e\u0915 \u0917\u0924\u093f\u0935\u093f\u0927\u093f\u092f\u094b\u0902 \u092e\u0947\u0902 \u0932\u0917\u0947\u0902"},
        {"en": "Drink plenty of water and stay hydrated", "hi": "\u0916\u0942\u092c \u092a\u093e\u0928\u0940 \u092a\u093f\u090f\u0902 \u0914\u0930 \u0939\u093e\u0907\u0921\u094d\u0930\u0947\u091f\u0947\u0921 \u0930\u0939\u0947\u0902"},
    ],
    # -- Mars --
    ("Mars", "benefic"): [
        {"en": "Channel energy into physical exercise", "hi": "\u090a\u0930\u094d\u091c\u093e \u0915\u094b \u0936\u093e\u0930\u0940\u0930\u093f\u0915 \u0935\u094d\u092f\u093e\u092f\u093e\u092e \u092e\u0947\u0902 \u0932\u0917\u093e\u090f\u0902"},
        {"en": "Take bold action on pending decisions", "hi": "\u0932\u0902\u092c\u093f\u0924 \u0928\u093f\u0930\u094d\u0923\u092f\u094b\u0902 \u092a\u0930 \u0938\u093e\u0939\u0938\u092a\u0942\u0930\u094d\u0923 \u0915\u093e\u0930\u094d\u0930\u0935\u093e\u0908 \u0915\u0930\u0947\u0902"},
        {"en": "Defend your boundaries with assertiveness", "hi": "\u0926\u0943\u0922\u093c\u0924\u093e \u0938\u0947 \u0905\u092a\u0928\u0940 \u0938\u0940\u092e\u093e\u0913\u0902 \u0915\u0940 \u0930\u0915\u094d\u0937\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Pursue competitive goals with full effort", "hi": "\u092a\u0942\u0930\u0947 \u092a\u094d\u0930\u092f\u093e\u0938 \u0938\u0947 \u092a\u094d\u0930\u0924\u093f\u0938\u094d\u092a\u0930\u094d\u0927\u0940 \u0932\u0915\u094d\u0937\u094d\u092f\u094b\u0902 \u0915\u093e \u092a\u0940\u091b\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Start a new fitness routine", "hi": "\u090f\u0915 \u0928\u0908 \u092b\u093f\u091f\u0928\u0947\u0938 \u0926\u093f\u0928\u091a\u0930\u094d\u092f\u093e \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902"},
        {"en": "Address conflicts directly and honestly", "hi": "\u0938\u0902\u0918\u0930\u094d\u0937\u094b\u0902 \u0915\u094b \u0938\u0940\u0927\u0947 \u0914\u0930 \u0908\u092e\u093e\u0928\u0926\u093e\u0930\u0940 \u0938\u0947 \u0938\u0902\u092c\u094b\u0927\u093f\u0924 \u0915\u0930\u0947\u0902"},
    ],
    # -- Mercury --
    ("Mercury", "benefic"): [
        {"en": "Engage in learning and intellectual pursuits", "hi": "\u0936\u093f\u0915\u094d\u0937\u093e \u0914\u0930 \u092c\u094c\u0926\u094d\u0927\u093f\u0915 \u0917\u0924\u093f\u0935\u093f\u0927\u093f\u092f\u094b\u0902 \u092e\u0947\u0902 \u0932\u0917\u0947\u0902"},
        {"en": "Communicate clearly in important matters", "hi": "\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u092e\u093e\u092e\u0932\u094b\u0902 \u092e\u0947\u0902 \u0938\u094d\u092a\u0937\u094d\u091f \u0938\u0902\u0935\u093e\u0926 \u0915\u0930\u0947\u0902"},
        {"en": "Write, journal, or express ideas creatively", "hi": "\u0932\u093f\u0916\u0947\u0902, \u0921\u093e\u092f\u0930\u0940 \u0930\u0916\u0947\u0902 \u092f\u093e \u0935\u093f\u091a\u093e\u0930\u094b\u0902 \u0915\u094b \u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915 \u0930\u0942\u092a \u0938\u0947 \u0935\u094d\u092f\u0915\u094d\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Negotiate deals and sign agreements", "hi": "\u0938\u094c\u0926\u094b\u0902 \u092a\u0930 \u092c\u093e\u0924\u091a\u0940\u0924 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0938\u092e\u091d\u094c\u0924\u0947 \u092a\u0930 \u0939\u0938\u094d\u0924\u093e\u0915\u094d\u0937\u0930 \u0915\u0930\u0947\u0902"},
        {"en": "Plan short trips or social visits", "hi": "\u091b\u094b\u091f\u0940 \u092f\u093e\u0924\u094d\u0930\u093e\u090f\u0902 \u092f\u093e \u0938\u093e\u092e\u093e\u091c\u093f\u0915 \u092e\u0941\u0932\u093e\u0915\u093e\u0924\u0947\u0902 \u092f\u094b\u091c\u0928\u093e \u092c\u0928\u093e\u090f\u0902"},
        {"en": "Update financial records and budgets", "hi": "\u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0930\u093f\u0915\u0949\u0930\u094d\u0921 \u0914\u0930 \u092c\u091c\u091f \u0905\u092a\u0921\u0947\u091f \u0915\u0930\u0947\u0902"},
    ],
    # -- Jupiter --
    ("Jupiter", "benefic"): [
        {"en": "Seek wisdom and guidance from mentors", "hi": "\u0917\u0941\u0930\u0941\u091c\u0928\u094b\u0902 \u0938\u0947 \u091c\u094d\u091e\u093e\u0928 \u0914\u0930 \u092e\u093e\u0930\u094d\u0917\u0926\u0930\u094d\u0936\u0928 \u092a\u094d\u0930\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Invest in education and spiritual growth", "hi": "\u0936\u093f\u0915\u094d\u0937\u093e \u0914\u0930 \u0906\u0927\u094d\u092f\u093e\u0924\u094d\u092e\u093f\u0915 \u0935\u093f\u0915\u093e\u0938 \u092e\u0947\u0902 \u0928\u093f\u0935\u0947\u0936 \u0915\u0930\u0947\u0902"},
        {"en": "Practice generosity and charitable giving", "hi": "\u0909\u0926\u093e\u0930\u0924\u093e \u0914\u0930 \u0926\u093e\u0928 \u0915\u093e \u0905\u092d\u094d\u092f\u093e\u0938 \u0915\u0930\u0947\u0902"},
        {"en": "Expand your professional network", "hi": "\u0905\u092a\u0928\u093e \u092a\u0947\u0936\u0947\u0935\u0930 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u092c\u0922\u093c\u093e\u090f\u0902"},
        {"en": "Visit a temple or sacred place", "hi": "\u092e\u0902\u0926\u093f\u0930 \u092f\u093e \u092a\u0935\u093f\u0924\u094d\u0930 \u0938\u094d\u0925\u093e\u0928 \u0915\u0940 \u092f\u093e\u0924\u094d\u0930\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Study sacred texts or philosophy", "hi": "\u0927\u093e\u0930\u094d\u092e\u093f\u0915 \u0917\u094d\u0930\u0902\u0925\u094b\u0902 \u092f\u093e \u0926\u0930\u094d\u0936\u0928 \u0915\u093e \u0905\u0927\u094d\u092f\u092f\u0928 \u0915\u0930\u0947\u0902"},
    ],
    # -- Venus --
    ("Venus", "benefic"): [
        {"en": "Nurture creativity and artistic pursuits", "hi": "\u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915\u0924\u093e \u0914\u0930 \u0915\u0932\u093e\u0924\u094d\u092e\u0915 \u0917\u0924\u093f\u0935\u093f\u0927\u093f\u092f\u094b\u0902 \u0915\u094b \u092a\u094b\u0937\u093f\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Strengthen romantic and social bonds", "hi": "\u092a\u094d\u0930\u0947\u092e \u0914\u0930 \u0938\u093e\u092e\u093e\u091c\u093f\u0915 \u0938\u0902\u092c\u0902\u0927\u094b\u0902 \u0915\u094b \u092e\u091c\u092c\u0942\u0924 \u0915\u0930\u0947\u0902"},
        {"en": "Indulge in beauty, fashion, or self-care", "hi": "\u0938\u0941\u0902\u0926\u0930\u0924\u093e, \u092b\u0948\u0936\u0928 \u092f\u093e \u0906\u0924\u094d\u092e-\u0926\u0947\u0916\u092d\u093e\u0932 \u092e\u0947\u0902 \u0938\u092e\u092f \u0932\u0917\u093e\u090f\u0902"},
        {"en": "Enjoy music, dance, or cultural events", "hi": "\u0938\u0902\u0917\u0940\u0924, \u0928\u0943\u0924\u094d\u092f \u092f\u093e \u0938\u093e\u0902\u0938\u094d\u0915\u0943\u0924\u093f\u0915 \u0915\u093e\u0930\u094d\u092f\u0915\u094d\u0930\u092e\u094b\u0902 \u0915\u093e \u0906\u0928\u0902\u0926 \u0932\u0947\u0902"},
        {"en": "Buy or gift something beautiful", "hi": "\u0915\u0941\u091b \u0938\u0941\u0902\u0926\u0930 \u0916\u0930\u0940\u0926\u0947\u0902 \u092f\u093e \u0909\u092a\u0939\u093e\u0930 \u0926\u0947\u0902"},
        {"en": "Decorate your home or workspace", "hi": "\u0905\u092a\u0928\u0947 \u0918\u0930 \u092f\u093e \u0915\u093e\u0930\u094d\u092f\u0938\u094d\u0925\u0932 \u0915\u094b \u0938\u091c\u093e\u090f\u0902"},
    ],
    # -- Saturn --
    ("Saturn", "benefic"): [
        {"en": "Focus on discipline and long-term planning", "hi": "\u0905\u0928\u0941\u0936\u093e\u0938\u0928 \u0914\u0930 \u0926\u0940\u0930\u094d\u0918\u0915\u093e\u0932\u093f\u0915 \u092f\u094b\u091c\u0928\u093e \u092a\u0930 \u0927\u094d\u092f\u093e\u0928 \u0926\u0947\u0902"},
        {"en": "Complete pending tasks and responsibilities", "hi": "\u0932\u0902\u092c\u093f\u0924 \u0915\u093e\u0930\u094d\u092f\u094b\u0902 \u0914\u0930 \u091c\u093f\u092e\u094d\u092e\u0947\u0926\u093e\u0930\u093f\u092f\u094b\u0902 \u0915\u094b \u092a\u0942\u0930\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Serve elders and those in need", "hi": "\u092c\u0941\u091c\u0941\u0930\u094d\u0917\u094b\u0902 \u0914\u0930 \u091c\u0930\u0942\u0930\u0924\u092e\u0902\u0926\u094b\u0902 \u0915\u0940 \u0938\u0947\u0935\u093e \u0915\u0930\u0947\u0902"},
        {"en": "Organize finances and reduce unnecessary expenses", "hi": "\u0935\u093f\u0924\u094d\u0924 \u0935\u094d\u092f\u0935\u0938\u094d\u0925\u093f\u0924 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0905\u0928\u093e\u0935\u0936\u094d\u092f\u0915 \u0916\u0930\u094d\u091a \u0915\u092e \u0915\u0930\u0947\u0902"},
        {"en": "Practice patience in difficult situations", "hi": "\u0915\u0920\u093f\u0928 \u092a\u0930\u093f\u0938\u094d\u0925\u093f\u0924\u093f\u092f\u094b\u0902 \u092e\u0947\u0902 \u0927\u0948\u0930\u094d\u092f \u0930\u0916\u0947\u0902"},
        {"en": "Pursue career advancement through hard work", "hi": "\u0915\u0921\u093c\u0940 \u092e\u0947\u0939\u0928\u0924 \u0938\u0947 \u0915\u0930\u093f\u092f\u0930 \u092e\u0947\u0902 \u0906\u0917\u0947 \u092c\u0922\u093c\u0947\u0902"},
    ],
}

DONTS_TEMPLATES: Dict[Tuple[str, str], List[Dict[str, str]]] = {
    # -- Sun --
    ("Sun", "malefic"): [
        {"en": "Avoid ego clashes with superiors", "hi": "\u0935\u0930\u093f\u0937\u094d\u0920\u094b\u0902 \u0915\u0947 \u0938\u093e\u0925 \u0905\u0939\u0902\u0915\u093e\u0930 \u0915\u0947 \u091f\u0915\u0930\u093e\u0935 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not overexert yourself physically", "hi": "\u0936\u093e\u0930\u0940\u0930\u093f\u0915 \u0930\u0942\u092a \u0938\u0947 \u0905\u0924\u094d\u092f\u0927\u093f\u0915 \u092a\u0930\u093f\u0936\u094d\u0930\u092e \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid heated arguments and confrontations", "hi": "\u0917\u0930\u092e\u093e\u0917\u0930\u092e \u092c\u0939\u0938 \u0914\u0930 \u091f\u0915\u0930\u093e\u0935 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not seek attention or validation today", "hi": "\u0906\u091c \u0927\u094d\u092f\u093e\u0928 \u092f\u093e \u092e\u093e\u0928\u094d\u092f\u0924\u093e \u0915\u0940 \u0924\u0932\u093e\u0936 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid starting new government-related matters", "hi": "\u0928\u090f \u0938\u0930\u0915\u093e\u0930\u0940 \u0915\u093e\u092e\u094b\u0902 \u0915\u094b \u0936\u0941\u0930\u0942 \u0915\u0930\u0928\u0947 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not ignore signs of fatigue or burnout", "hi": "\u0925\u0915\u093e\u0928 \u092f\u093e \u092c\u0930\u094d\u0928\u0906\u0909\u091f \u0915\u0947 \u0938\u0902\u0915\u0947\u0924\u094b\u0902 \u0915\u0940 \u0909\u092a\u0947\u0915\u094d\u0937\u093e \u0928 \u0915\u0930\u0947\u0902"},
    ],
    # -- Moon --
    ("Moon", "malefic"): [
        {"en": "Avoid making emotional decisions", "hi": "\u092d\u093e\u0935\u0928\u093e\u0924\u094d\u092e\u0915 \u0928\u093f\u0930\u094d\u0923\u092f \u0932\u0947\u0928\u0947 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not neglect your mental health", "hi": "\u0905\u092a\u0928\u0947 \u092e\u093e\u0928\u0938\u093f\u0915 \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0915\u0940 \u0909\u092a\u0947\u0915\u094d\u0937\u093e \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid travel near water bodies", "hi": "\u091c\u0932 \u0928\u093f\u0915\u093e\u092f\u094b\u0902 \u0915\u0947 \u092a\u093e\u0938 \u092f\u093e\u0924\u094d\u0930\u093e \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not suppress your feelings completely", "hi": "\u0905\u092a\u0928\u0940 \u092d\u093e\u0935\u0928\u093e\u0913\u0902 \u0915\u094b \u092a\u0942\u0930\u0940 \u0924\u0930\u0939 \u0938\u0947 \u0926\u092c\u093e\u090f\u0902 \u0928\u0939\u0940\u0902"},
        {"en": "Avoid consuming stale or cold food", "hi": "\u092c\u093e\u0938\u0940 \u092f\u093e \u0920\u0902\u0921\u093e \u092d\u094b\u091c\u0928 \u0916\u093e\u0928\u0947 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not isolate yourself from close ones", "hi": "\u0915\u0930\u0940\u092c\u0940 \u0932\u094b\u0917\u094b\u0902 \u0938\u0947 \u0905\u0932\u0917-\u0925\u0932\u0917 \u0928 \u0930\u0939\u0947\u0902"},
    ],
    # -- Mars --
    ("Mars", "malefic"): [
        {"en": "Avoid impulsive or aggressive behavior", "hi": "\u0906\u0935\u0947\u0917\u092a\u0942\u0930\u094d\u0923 \u092f\u093e \u0906\u0915\u094d\u0930\u093e\u092e\u0915 \u0935\u094d\u092f\u0935\u0939\u093e\u0930 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not engage in risky physical activities", "hi": "\u091c\u094b\u0916\u093f\u092e \u092d\u0930\u0940 \u0936\u093e\u0930\u0940\u0930\u093f\u0915 \u0917\u0924\u093f\u0935\u093f\u0927\u093f\u092f\u094b\u0902 \u092e\u0947\u0902 \u0928 \u0932\u0917\u0947\u0902"},
        {"en": "Avoid arguments with siblings or neighbors", "hi": "\u092d\u093e\u0908-\u092c\u0939\u0928\u094b\u0902 \u092f\u093e \u092a\u0921\u093c\u094b\u0938\u093f\u092f\u094b\u0902 \u0938\u0947 \u092c\u0939\u0938 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not handle sharp objects carelessly", "hi": "\u0924\u0940\u0916\u0940 \u0935\u0938\u094d\u0924\u0941\u0913\u0902 \u0915\u094b \u0932\u093e\u092a\u0930\u0935\u093e\u0939\u0940 \u0938\u0947 \u0928 \u0938\u0902\u092d\u093e\u0932\u0947\u0902"},
        {"en": "Avoid signing contracts involving land or property", "hi": "\u092d\u0942\u092e\u093f \u092f\u093e \u0938\u0902\u092a\u0924\u094d\u0924\u093f \u0938\u0947 \u091c\u0941\u0921\u093c\u0947 \u0905\u0928\u0941\u092c\u0902\u0927\u094b\u0902 \u092a\u0930 \u0939\u0938\u094d\u0924\u093e\u0915\u094d\u0937\u0930 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Do not start fights or legal battles today", "hi": "\u0906\u091c \u0932\u0921\u093c\u093e\u0908 \u092f\u093e \u0915\u093e\u0928\u0942\u0928\u0940 \u0932\u0921\u093c\u093e\u0908 \u0936\u0941\u0930\u0942 \u0928 \u0915\u0930\u0947\u0902"},
    ],
    # -- Mercury --
    ("Mercury", "malefic"): [
        {"en": "Avoid signing important documents", "hi": "\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u0926\u0938\u094d\u0924\u093e\u0935\u0947\u091c\u093c\u094b\u0902 \u092a\u0930 \u0939\u0938\u094d\u0924\u093e\u0915\u094d\u0937\u0930 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not spread unverified information", "hi": "\u0905\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0928 \u092b\u0948\u0932\u093e\u090f\u0902"},
        {"en": "Avoid multitasking on critical work", "hi": "\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u0915\u093e\u092e \u092e\u0947\u0902 \u092e\u0932\u094d\u091f\u0940\u091f\u093e\u0938\u094d\u0915\u093f\u0902\u0917 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not make hasty financial transactions", "hi": "\u091c\u0932\u094d\u0926\u092c\u093e\u091c\u093c\u0940 \u092e\u0947\u0902 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0932\u0947\u0928\u0926\u0947\u0928 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid gossip and unnecessary chatter", "hi": "\u0917\u092a\u0936\u092a \u0914\u0930 \u0905\u0928\u093e\u0935\u0936\u094d\u092f\u0915 \u092c\u093e\u0924\u091a\u0940\u0924 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not ignore details in written communication", "hi": "\u0932\u093f\u0916\u093f\u0924 \u0938\u0902\u091a\u093e\u0930 \u092e\u0947\u0902 \u0935\u093f\u0935\u0930\u0923\u094b\u0902 \u0915\u0940 \u0909\u092a\u0947\u0915\u094d\u0937\u093e \u0928 \u0915\u0930\u0947\u0902"},
    ],
    # -- Jupiter --
    ("Jupiter", "malefic"): [
        {"en": "Avoid overcommitting or overpromising", "hi": "\u0905\u0924\u094d\u092f\u0927\u093f\u0915 \u092a\u094d\u0930\u0924\u093f\u092c\u0926\u094d\u0927\u0924\u093e \u092f\u093e \u0935\u093e\u0926\u0947 \u0915\u0930\u0928\u0947 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not lend money without clear terms", "hi": "\u0938\u094d\u092a\u0937\u094d\u091f \u0936\u0930\u094d\u0924\u094b\u0902 \u0915\u0947 \u092c\u093f\u0928\u093e \u092a\u0948\u0938\u0947 \u0909\u0927\u093e\u0930 \u0928 \u0926\u0947\u0902"},
        {"en": "Avoid blind faith in unproven schemes", "hi": "\u0905\u092a\u094d\u0930\u092e\u093e\u0923\u093f\u0924 \u092f\u094b\u091c\u0928\u093e\u0913\u0902 \u092e\u0947\u0902 \u0905\u0902\u0927\u0935\u093f\u0936\u094d\u0935\u093e\u0938 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not disrespect teachers or spiritual guides", "hi": "\u0936\u093f\u0915\u094d\u0937\u0915\u094b\u0902 \u092f\u093e \u0906\u0927\u094d\u092f\u093e\u0924\u094d\u092e\u093f\u0915 \u0917\u0941\u0930\u0941\u0913\u0902 \u0915\u093e \u0905\u092a\u092e\u093e\u0928 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid excessive spending on luxuries", "hi": "\u0935\u093f\u0932\u093e\u0938\u093f\u0924\u093e \u092a\u0930 \u0905\u0924\u094d\u092f\u0927\u093f\u0915 \u0916\u0930\u094d\u091a \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not take legal risks without counsel", "hi": "\u0938\u0932\u093e\u0939 \u0915\u0947 \u092c\u093f\u0928\u093e \u0915\u093e\u0928\u0942\u0928\u0940 \u091c\u094b\u0916\u093f\u092e \u0928 \u0932\u0947\u0902"},
    ],
    # -- Venus --
    ("Venus", "malefic"): [
        {"en": "Avoid overindulgence in food or drink", "hi": "\u0916\u093e\u0928\u0947-\u092a\u0940\u0928\u0947 \u092e\u0947\u0902 \u0905\u0924\u094d\u092f\u0927\u093f\u0915 \u092d\u094b\u0917 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not make impulsive purchases", "hi": "\u0906\u0935\u0947\u0917\u092a\u0942\u0930\u094d\u0923 \u0916\u0930\u0940\u0926\u0926\u093e\u0930\u0940 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid romantic entanglements with unclear intentions", "hi": "\u0905\u0938\u094d\u092a\u0937\u094d\u091f \u0907\u0930\u093e\u0926\u094b\u0902 \u0935\u093e\u0932\u0947 \u092a\u094d\u0930\u0947\u092e \u0938\u0902\u092c\u0902\u0927\u094b\u0902 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not neglect your appearance or hygiene", "hi": "\u0905\u092a\u0928\u0940 \u0926\u093f\u0916\u093e\u0935\u091f \u092f\u093e \u0938\u094d\u0935\u091a\u094d\u091b\u0924\u093e \u0915\u0940 \u0909\u092a\u0947\u0915\u094d\u0937\u093e \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid vain flattery or superficial socializing", "hi": "\u0935\u094d\u092f\u0930\u094d\u0925 \u091a\u093e\u092a\u0932\u0942\u0938\u0940 \u092f\u093e \u0938\u0924\u0939\u0940 \u0938\u093e\u092e\u093e\u091c\u093f\u0915\u0924\u093e \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not make relationship decisions under stress", "hi": "\u0924\u0928\u093e\u0935 \u092e\u0947\u0902 \u0930\u093f\u0936\u094d\u0924\u094b\u0902 \u0915\u0947 \u0928\u093f\u0930\u094d\u0923\u092f \u0928 \u0932\u0947\u0902"},
    ],
    # -- Saturn --
    ("Saturn", "malefic"): [
        {"en": "Avoid hasty long-term commitments", "hi": "\u091c\u0932\u094d\u0926\u092c\u093e\u091c\u093c\u0940 \u092e\u0947\u0902 \u0926\u0940\u0930\u094d\u0918\u0915\u093e\u0932\u093f\u0915 \u092a\u094d\u0930\u0924\u093f\u092c\u0926\u094d\u0927\u0924\u093e\u0913\u0902 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not ignore recurring health symptoms", "hi": "\u092c\u093e\u0930-\u092c\u093e\u0930 \u0906\u0928\u0947 \u0935\u093e\u0932\u0947 \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0932\u0915\u094d\u0937\u0923\u094b\u0902 \u0915\u0940 \u0909\u092a\u0947\u0915\u094d\u0937\u093e \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid conflicts with elderly or authority figures", "hi": "\u092c\u0941\u091c\u0941\u0930\u094d\u0917\u094b\u0902 \u092f\u093e \u0905\u0927\u093f\u0915\u093e\u0930\u0940 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u092f\u094b\u0902 \u0938\u0947 \u0938\u0902\u0918\u0930\u094d\u0937 \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not procrastinate on important duties", "hi": "\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u0915\u0930\u094d\u0924\u0935\u094d\u092f\u094b\u0902 \u092e\u0947\u0902 \u091f\u093e\u0932\u092e\u091f\u094b\u0932 \u0928 \u0915\u0930\u0947\u0902"},
        {"en": "Avoid shortcuts in work or studies", "hi": "\u0915\u093e\u092e \u092f\u093e \u092a\u0922\u093c\u093e\u0908 \u092e\u0947\u0902 \u0936\u0949\u0930\u094d\u091f\u0915\u091f \u0938\u0947 \u092c\u091a\u0947\u0902"},
        {"en": "Do not resist necessary change or transformation", "hi": "\u0906\u0935\u0936\u094d\u092f\u0915 \u092a\u0930\u093f\u0935\u0930\u094d\u0924\u0928 \u0915\u093e \u0935\u093f\u0930\u094b\u0927 \u0928 \u0915\u0930\u0947\u0902"},
    ],
}


# ==============================================================================
# DERIVATION FUNCTIONS
# ==============================================================================

def derive_lucky_number(moon_nakshatra_index: int, moon_pada: int, date_str: str) -> int:
    """
    Derive a lucky number (1-9) deterministically from Moon's nakshatra index,
    pada, and date digit sum.

    Parameters
    ----------
    moon_nakshatra_index : int
        0-based nakshatra index (0 = Ashwini, 26 = Revati).
    moon_pada : int
        1-4, the quarter/pada of the nakshatra.
    date_str : str
        ISO date string, e.g. "2026-04-16".

    Returns
    -------
    int
        Lucky number between 1 and 9 (inclusive).
    """
    # Sum all digits of the date string (ignoring hyphens)
    date_digit_sum = sum(int(ch) for ch in date_str if ch.isdigit())
    combined = moon_nakshatra_index + moon_pada + date_digit_sum
    return (combined % 9) + 1


def derive_lucky_color(sign: str, moon_pada: int) -> Dict[str, str]:
    """
    Derive the lucky color from the sign's element and Moon's pada.

    Parameters
    ----------
    sign : str
        Lowercase zodiac sign name (e.g. "aries").
    moon_pada : int
        1-4, the quarter/pada of the Moon's nakshatra.

    Returns
    -------
    dict
        {"en": "...", "hi": "..."} bilingual color name.
    """
    element = ELEMENTS.get(sign, "fire")
    colors = ELEMENT_COLORS.get(element, ELEMENT_COLORS["fire"])
    # pada is 1-4, index is 0-3
    index = (moon_pada - 1) % len(colors)
    return colors[index]


def derive_compatible_sign(sign: str, transit_dignities: Dict[str, str]) -> Dict[str, str]:
    """
    Determine the most compatible sign today from same-element (trine) signs.
    Picks the trine sign whose ruler has the best current dignity.

    Parameters
    ----------
    sign : str
        Lowercase zodiac sign name.
    transit_dignities : dict
        Planet name -> dignity string. e.g. {"Mars": "exalted", "Venus": "own", ...}
        Possible values: "exalted", "own", "neutral", "debilitated".

    Returns
    -------
    dict
        {"en": "Leo", "hi": "..."} bilingual sign name.
    """
    element = ELEMENTS.get(sign, "fire")
    trine_signs = _TRINES.get(element, ["aries", "leo", "sagittarius"])
    # Exclude the queried sign itself
    candidates = [s for s in trine_signs if s != sign]
    if not candidates:
        candidates = trine_signs[:1]

    # Rank by ruler dignity
    dignity_rank = {"exalted": 4, "own": 3, "neutral": 2, "debilitated": 1}

    best_sign = candidates[0]
    best_score = 0
    for candidate in candidates:
        ruler = RULERS.get(candidate, "Sun")
        dignity = transit_dignities.get(ruler, "neutral")
        score = dignity_rank.get(dignity, 2)
        if score > best_score:
            best_score = score
            best_sign = candidate

    return {
        "en": best_sign.title(),
        "hi": SIGN_HINDI.get(best_sign, best_sign),
    }


def derive_mood(overall_score: int) -> Dict[str, str]:
    """
    Map an overall daily score (1-10) to a bilingual mood label.

    Parameters
    ----------
    overall_score : int
        Score between 1 and 10.

    Returns
    -------
    dict
        {"en": "...", "hi": "..."} bilingual mood label.
    """
    clamped = max(1, min(10, overall_score))
    for low, high, label in MOOD_MAP:
        if low <= clamped <= high:
            return label
    # Fallback
    return {"en": "Steady", "hi": "\u0938\u094d\u0925\u093f\u0930"}


def _classify_house(house: int) -> str:
    """Classify a house number as benefic, malefic, or neutral."""
    if house in BENEFIC_HOUSES:
        return "benefic"
    if house in MALEFIC_HOUSES:
        return "malefic"
    return "neutral"


def derive_dos(
    planet_houses: Dict[str, int],
    planet_dignities: Dict[str, str],
) -> List[Dict[str, str]]:
    """
    Pick 3 do's based on which planets are in benefic houses with good dignity.

    Parameters
    ----------
    planet_houses : dict
        Planet name -> house number (1-12). e.g. {"Sun": 10, "Moon": 5, ...}
    planet_dignities : dict
        Planet name -> dignity string. e.g. {"Sun": "exalted", "Moon": "own", ...}

    Returns
    -------
    list
        List of 3 bilingual do's: [{"en": "...", "hi": "..."}, ...]
    """
    dignity_rank = {"exalted": 4, "own": 3, "neutral": 2, "debilitated": 1}
    scored_planets: List[Tuple[str, int]] = []

    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        house = planet_houses.get(planet, 1)
        classification = _classify_house(house)
        if classification == "benefic":
            dignity = planet_dignities.get(planet, "neutral")
            score = dignity_rank.get(dignity, 2) * 10 + (12 - house)
            scored_planets.append((planet, score))

    # Sort by score descending — deterministic since scores are distinct
    scored_planets.sort(key=lambda x: (-x[1], x[0]))

    results: List[Dict[str, str]] = []
    used_planets: set = set()

    for planet, _score in scored_planets:
        if len(results) >= 3:
            break
        if planet in used_planets:
            continue
        templates = DOS_TEMPLATES.get((planet, "benefic"), [])
        if templates:
            # Pick deterministically based on house number
            house = planet_houses.get(planet, 1)
            idx = (house - 1) % len(templates)
            results.append(templates[idx])
            used_planets.add(planet)

    # If fewer than 3 benefic planets found, fill from Jupiter (universal benefic)
    if len(results) < 3:
        templates = DOS_TEMPLATES.get(("Jupiter", "benefic"), [])
        if templates:
            fill_idx = 0
            while len(results) < 3 and fill_idx < len(templates):
                if templates[fill_idx] not in results:
                    results.append(templates[fill_idx])
                fill_idx += 1

    return results[:3]


def derive_donts(
    planet_houses: Dict[str, int],
    planet_dignities: Dict[str, str],
) -> List[Dict[str, str]]:
    """
    Pick 3 don'ts based on which planets are in malefic houses with weak dignity.

    Parameters
    ----------
    planet_houses : dict
        Planet name -> house number (1-12). e.g. {"Saturn": 8, "Mars": 12, ...}
    planet_dignities : dict
        Planet name -> dignity string.

    Returns
    -------
    list
        List of 3 bilingual don'ts: [{"en": "...", "hi": "..."}, ...]
    """
    dignity_rank = {"exalted": 4, "own": 3, "neutral": 2, "debilitated": 1}
    scored_planets: List[Tuple[str, int]] = []

    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        house = planet_houses.get(planet, 1)
        classification = _classify_house(house)
        if classification == "malefic":
            dignity = planet_dignities.get(planet, "neutral")
            # Lower dignity = higher priority for don'ts (invert ranking)
            score = (5 - dignity_rank.get(dignity, 2)) * 10 + house
            scored_planets.append((planet, score))

    # Sort by score descending (worst placements first)
    scored_planets.sort(key=lambda x: (-x[1], x[0]))

    results: List[Dict[str, str]] = []
    used_planets: set = set()

    for planet, _score in scored_planets:
        if len(results) >= 3:
            break
        if planet in used_planets:
            continue
        templates = DONTS_TEMPLATES.get((planet, "malefic"), [])
        if templates:
            house = planet_houses.get(planet, 6)
            idx = (house - 1) % len(templates)
            results.append(templates[idx])
            used_planets.add(planet)

    # If fewer than 3 malefic planets found, fill from Saturn (natural malefic)
    if len(results) < 3:
        templates = DONTS_TEMPLATES.get(("Saturn", "malefic"), [])
        if templates:
            fill_idx = 0
            while len(results) < 3 and fill_idx < len(templates):
                if templates[fill_idx] not in results:
                    results.append(templates[fill_idx])
                fill_idx += 1

    return results[:3]


def derive_lucky_time(sign: str, ruler: str) -> Dict[str, str]:
    """
    Derive the lucky time window as the planetary hora of the sign's ruler.
    Uses the standard hora cycle starting from sunrise (6 AM).

    Parameters
    ----------
    sign : str
        Lowercase zodiac sign name (used for secondary offset).
    ruler : str
        Ruling planet name, e.g. "Mars".

    Returns
    -------
    dict
        {"en": "...", "hi": "..."} bilingual time range.
    """
    # Find the first occurrence of the ruler in the hora order
    if ruler in _HORA_ORDER:
        base_index = _HORA_ORDER.index(ruler)
    else:
        base_index = 0

    # Add a sign-based offset so different signs with the same ruler
    # get slightly different times (e.g. Gemini vs Virgo both ruled by Mercury)
    sign_list = list(ELEMENTS.keys())
    sign_offset = sign_list.index(sign) if sign in sign_list else 0
    # Use modular offset within available hora slots
    hora_index = (base_index + (sign_offset % 2) * 7) % len(_HORA_TIMES)

    return _HORA_TIMES[hora_index]


def derive_gemstone(ruler: str, planet_dignities: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Return gemstone recommendation data based on ruling planet and current transits.

    When planet_dignities is provided, checks if natural benefics (Jupiter, Venus)
    are exalted or in own sign — if so, recommends their gemstone for the transit
    period (secondary gemstone boost) instead of the default sign ruler.

    Parameters
    ----------
    ruler : str
        Planet name, e.g. "Venus".
    planet_dignities : dict, optional
        Current transit dignities per planet, e.g. {"Jupiter": "exalted", ...}.

    Returns
    -------
    dict
        Full gemstone data: gem, metal, finger, day (all bilingual).
    """
    if planet_dignities:
        # Natural benefics in peak dignity override the default ruler's gemstone
        for benefic in ["Jupiter", "Venus"]:
            dignity = planet_dignities.get(benefic, "neutral")
            if dignity in ("exalted", "own_sign") and benefic != ruler:
                return GEMSTONE_DATA.get(benefic, GEMSTONE_DATA.get(ruler, GEMSTONE_DATA["Sun"]))
    return GEMSTONE_DATA.get(ruler, GEMSTONE_DATA["Sun"])


def derive_mantra(ruler: str) -> str:
    """
    Return the Vedic beej mantra for the given ruling planet.

    Parameters
    ----------
    ruler : str
        Planet name, e.g. "Saturn".

    Returns
    -------
    str
        The mantra text.
    """
    return PLANET_MANTRAS.get(ruler, PLANET_MANTRAS["Sun"])


# ==============================================================================
# AGGREGATE FUNCTION
# ==============================================================================

def get_all_lucky_metadata(
    sign: str,
    moon_nakshatra_index: int,
    moon_pada: int,
    date_str: str,
    overall_score: int,
    planet_houses: Dict[str, int],
    planet_dignities: Dict[str, str],
    transit_dignities: Dict[str, str],
) -> Dict[str, Any]:
    """
    Compute all lucky metadata for a sign on a given date.
    Deterministic: same inputs always produce the same outputs.

    Parameters
    ----------
    sign : str
        Lowercase zodiac sign name (e.g. "aries").
    moon_nakshatra_index : int
        0-based Moon nakshatra index (0-26).
    moon_pada : int
        Moon's nakshatra pada (1-4).
    date_str : str
        ISO date string, e.g. "2026-04-16".
    overall_score : int
        Computed overall daily score (1-10).
    planet_houses : dict
        Planet name -> house number (1-12) from Moon sign.
    planet_dignities : dict
        Planet name -> dignity string for each transit planet.
    transit_dignities : dict
        Planet name -> dignity string for compatible sign derivation.

    Returns
    -------
    dict
        Complete lucky metadata with keys:
        lucky_number, lucky_color, lucky_time, compatible_sign,
        mood, gemstone, mantra, dos, donts
    """
    ruler = RULERS.get(sign, "Sun")

    return {
        "lucky_number": derive_lucky_number(moon_nakshatra_index, moon_pada, date_str),
        "lucky_color": derive_lucky_color(sign, moon_pada),
        "lucky_time": derive_lucky_time(sign, ruler),
        "compatible_sign": derive_compatible_sign(sign, transit_dignities),
        "mood": derive_mood(overall_score),
        "gemstone": derive_gemstone(ruler, planet_dignities),
        "mantra": derive_mantra(ruler),
        "dos": derive_dos(planet_houses, planet_dignities),
        "donts": derive_donts(planet_houses, planet_dignities),
    }
