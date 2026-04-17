"""
festival_engine.py -- Rule-Based Hindu Festival & Vrat Detection Engine
=======================================================================
Detects festivals and vrats for a given date based on three sources:
1. Tithi + Paksha + Maas (specific annual festivals)
2. Recurring monthly festivals (tithi-based, every month)
3. Solar date festivals (Gregorian fixed dates)

NO hardcoded Gregorian-to-festival mapping for Hindu festivals --
all Hindu festivals are computed from panchang elements.
"""
from __future__ import annotations
from datetime import date
from typing import Any, Dict, List, Optional


# ============================================================
# 1. TITHI FESTIVALS -- Specific annual festivals
#    Matched by: maas + paksha + tithi
# ============================================================

TITHI_FESTIVALS: List[Dict[str, Any]] = [
    # ── Chaitra ──────────────────────────────────────────────
    {"maas": "Chaitra", "paksha": "Shukla", "tithi": "Pratipada", "name": "Hindu Nav Varsh", "name_hindi": "हिन्दू नव वर्ष", "type": "major", "description": "Hindu New Year - start of Chaitra Navratri", "description_hindi": "हिंदू नव वर्ष - चैत्र नवरात्रि का प्रारंभ"},
    {"maas": "Chaitra", "paksha": "Shukla", "tithi": "Pratipada", "name": "Chaitra Navratri Begins", "name_hindi": "चैत्र नवरात्रि आरम्भ", "type": "major", "description": "Nine nights of Goddess Durga worship begin", "description_hindi": "मां दुर्गा की नौ रात्रियों की पूजा शुरू"},
    {"maas": "Chaitra", "paksha": "Shukla", "tithi": "Navami", "name": "Ram Navami", "name_hindi": "राम नवमी", "type": "major", "description": "Birthday of Lord Rama", "description_hindi": "भगवान श्री राम का जन्म दिवस"},
    {"maas": "Chaitra", "paksha": "Shukla", "tithi": "Purnima", "name": "Hanuman Jayanti", "name_hindi": "हनुमान जयंती", "type": "major", "description": "Birthday of Lord Hanuman", "description_hindi": "भगवान हनुमान का जन्म दिवस"},
    {"maas": "Chaitra", "paksha": "Shukla", "tithi": "Purnima", "name": "Chaitra Purnima", "name_hindi": "चैत्र पूर्णिमा", "type": "major", "description": "Full moon of Chaitra month", "description_hindi": "चैत्र मास की पूर्णिमा"},

    # ── Vaishakha ────────────────────────────────────────────
    {"maas": "Vaishakha", "paksha": "Shukla", "tithi": "Tritiya", "name": "Akshaya Tritiya", "name_hindi": "अक्षय तृतीया", "type": "major", "description": "Most auspicious day for new beginnings, gold purchase"},
    {"maas": "Vaishakha", "paksha": "Shukla", "tithi": "Tritiya", "name": "Parashurama Jayanti", "name_hindi": "परशुराम जयंती", "type": "major", "description": "Birthday of Lord Parashurama"},
    {"maas": "Vaishakha", "paksha": "Shukla", "tithi": "Navami", "name": "Sita Navami", "name_hindi": "सीता नवमी", "type": "festival", "description": "Birthday of Goddess Sita"},
    {"maas": "Vaishakha", "paksha": "Shukla", "tithi": "Purnima", "name": "Buddha Purnima", "name_hindi": "बुद्ध पूर्णिमा", "type": "major", "description": "Birthday of Lord Buddha"},
    {"maas": "Vaishakha", "paksha": "Krishna", "tithi": "Ekadashi", "name": "Varuthini Ekadashi", "name_hindi": "वरूथिनी एकादशी", "type": "fasting", "description": "Sacred Ekadashi fasting day"},
    {"maas": "Vaishakha", "paksha": "Shukla", "tithi": "Ekadashi", "name": "Mohini Ekadashi", "name_hindi": "मोहिनी एकादशी", "type": "fasting", "description": "Sacred Ekadashi fasting day"},

    # ── Jyeshtha ─────────────────────────────────────────────
    {"maas": "Jyeshtha", "paksha": "Shukla", "tithi": "Purnima", "name": "Vat Savitri Vrat", "name_hindi": "वट सावित्री व्रत", "type": "fasting", "description": "Married women fast for husband's longevity"},
    {"maas": "Jyeshtha", "paksha": "Shukla", "tithi": "Dashami", "name": "Ganga Dussehra", "name_hindi": "गंगा दशहरा", "type": "major", "description": "Descent of Ganga to Earth"},
    {"maas": "Jyeshtha", "paksha": "Shukla", "tithi": "Ekadashi", "name": "Nirjala Ekadashi", "name_hindi": "निर्जला एकादशी", "type": "fasting", "description": "Strictest Ekadashi - no water fast"},

    # ── Ashadha ──────────────────────────────────────────────
    {"maas": "Ashadha", "paksha": "Shukla", "tithi": "Ekadashi", "name": "Devshayani Ekadashi", "name_hindi": "देवशयनी एकादशी", "type": "major", "description": "Lord Vishnu goes to sleep - Chaturmas begins"},
    {"maas": "Ashadha", "paksha": "Shukla", "tithi": "Purnima", "name": "Guru Purnima", "name_hindi": "गुरु पूर्णिमा", "type": "major", "description": "Day to honor the Guru/teacher"},

    # ── Shravana ─────────────────────────────────────────────
    {"maas": "Shravana", "paksha": "Shukla", "tithi": "Panchami", "name": "Nag Panchami", "name_hindi": "नाग पंचमी", "type": "festival", "description": "Worship of serpent deities"},
    {"maas": "Shravana", "paksha": "Shukla", "tithi": "Purnima", "name": "Raksha Bandhan", "name_hindi": "रक्षा बंधन", "type": "major", "description": "Festival of brother-sister bond"},
    {"maas": "Shravana", "paksha": "Krishna", "tithi": "Ashtami", "name": "Krishna Janmashtami", "name_hindi": "कृष्ण जन्माष्टमी", "type": "major", "description": "Birthday of Lord Krishna"},

    # ── Bhadrapada ───────────────────────────────────────────
    {"maas": "Bhadrapada", "paksha": "Shukla", "tithi": "Chaturthi", "name": "Ganesh Chaturthi", "name_hindi": "गणेश चतुर्थी", "type": "major", "description": "Birthday of Lord Ganesha"},
    {"maas": "Bhadrapada", "paksha": "Shukla", "tithi": "Chaturdashi", "name": "Anant Chaturdashi", "name_hindi": "अनंत चतुर्दशी", "type": "festival", "description": "Ganesh Visarjan day"},
    {"maas": "Bhadrapada", "paksha": "Krishna", "tithi": "Amavasya", "name": "Sarva Pitru Amavasya", "name_hindi": "सर्व पितृ अमावस्या", "type": "major", "description": "Last day of Pitru Paksha"},

    # ── Ashwin ───────────────────────────────────────────────
    {"maas": "Ashwin", "paksha": "Shukla", "tithi": "Pratipada", "name": "Sharad Navratri Begins", "name_hindi": "शरद नवरात्रि आरम्भ", "type": "major", "description": "Nine nights of Goddess Durga worship"},
    {"maas": "Ashwin", "paksha": "Shukla", "tithi": "Ashtami", "name": "Durga Ashtami", "name_hindi": "दुर्गा अष्टमी", "type": "major", "description": "Main day of Navratri worship"},
    {"maas": "Ashwin", "paksha": "Shukla", "tithi": "Dashami", "name": "Dussehra / Vijayadashami", "name_hindi": "दशहरा / विजयादशमी", "type": "major", "description": "Victory of good over evil - Ravana Dahan"},
    {"maas": "Ashwin", "paksha": "Shukla", "tithi": "Purnima", "name": "Sharad Purnima", "name_hindi": "शरद पूर्णिमा", "type": "festival", "description": "Full Moon of Ashwin - Kheer Purnima"},
    {"maas": "Ashwin", "paksha": "Krishna", "tithi": "Chaturthi", "name": "Karwa Chauth", "name_hindi": "करवा चौथ", "type": "fasting", "description": "Married women fast for husband's longevity"},

    # ── Kartik ───────────────────────────────────────────────
    {"maas": "Kartik", "paksha": "Krishna", "tithi": "Trayodashi", "name": "Dhanteras", "name_hindi": "धनतेरस", "type": "major", "description": "Festival of wealth - buy gold/silver", "description_hindi": "धन और समृद्धि का उत्सव - सोना/चांदी खरीदना शुभ"},
    {"maas": "Kartik", "paksha": "Krishna", "tithi": "Chaturdashi", "name": "Narak Chaturdashi / Choti Diwali", "name_hindi": "नरक चतुर्दशी / छोटी दिवाली", "type": "major", "description": "Small Diwali", "description_hindi": "छोटी दिवाली"},
    {"maas": "Kartik", "paksha": "Krishna", "tithi": "Amavasya", "name": "Diwali / Deepawali", "name_hindi": "दीपावली", "type": "major", "description": "Festival of Lights - Lakshmi Puja", "description_hindi": "प्रकाश का उत्सव - लक्ष्मी पूजा"},
    {"maas": "Kartik", "paksha": "Shukla", "tithi": "Pratipada", "name": "Govardhan Puja", "name_hindi": "गोवर्धन पूजा", "type": "major", "description": "Worship of Govardhan Hill", "description_hindi": "गोवर्धन पर्वत की पूजा"},
    {"maas": "Kartik", "paksha": "Shukla", "tithi": "Dwitiya", "name": "Bhai Dooj", "name_hindi": "भाई दूज", "type": "major", "description": "Brother-sister festival", "description_hindi": "भाई-बहन के प्रेम का उत्सव"},
    {"maas": "Kartik", "paksha": "Shukla", "tithi": "Ekadashi", "name": "Dev Uthani Ekadashi", "name_hindi": "देव उठनी एकादशी", "type": "major", "description": "Lord Vishnu wakes up - marriages resume"},

    # ── Margashirsha ─────────────────────────────────────────
    {"maas": "Margashirsha", "paksha": "Shukla", "tithi": "Purnima", "name": "Dattatreya Jayanti", "name_hindi": "दत्तात्रेय जयंती", "type": "festival", "description": "Birthday of Lord Dattatreya"},

    # ── Pausha ───────────────────────────────────────────────
    {"maas": "Pausha", "paksha": "Krishna", "tithi": "Ashtami", "name": "Masik Shivaratri", "name_hindi": "मासिक शिवरात्रि", "type": "fasting", "description": "Monthly Shiva worship night"},
    {"maas": "Pausha", "paksha": "Shukla", "tithi": "Purnima", "name": "Pausha Purnima", "name_hindi": "पौष पूर्णिमा", "type": "festival", "description": "Full moon bath in holy rivers"},

    # ── Magha ────────────────────────────────────────────────
    {"maas": "Magha", "paksha": "Shukla", "tithi": "Panchami", "name": "Basant Panchami / Saraswati Puja", "name_hindi": "बसंत पंचमी / सरस्वती पूजा", "type": "major", "description": "Worship of Goddess Saraswati - start of spring"},
    {"maas": "Magha", "paksha": "Krishna", "tithi": "Chaturdashi", "name": "Maha Shivaratri", "name_hindi": "महा शिवरात्रि", "type": "major", "description": "The Great Night of Lord Shiva"},
    {"maas": "Magha", "paksha": "Shukla", "tithi": "Purnima", "name": "Maghi Purnima", "name_hindi": "माघी पूर्णिमा", "type": "festival", "description": "Sacred full moon of Magha"},

    # ── Phalguna ─────────────────────────────────────────────
    {"maas": "Phalguna", "paksha": "Shukla", "tithi": "Purnima", "name": "Holi", "name_hindi": "होली", "type": "major", "description": "Festival of Colors - Holika Dahan night before"},
    {"maas": "Phalguna", "paksha": "Krishna", "tithi": "Chaturdashi", "name": "Holika Dahan", "name_hindi": "होलिका दहन", "type": "major", "description": "Burning of Holika - night before Holi colors"},
]


# ============================================================
# 2. RECURRING FESTIVALS -- Generic tithi-based (every month)
# ============================================================

RECURRING_FESTIVALS: List[Dict[str, Any]] = [
    {"tithi": "Ekadashi", "name": "Ekadashi Vrat", "name_hindi": "एकादशी व्रत", "type": "fasting", "description": "Sacred fasting day on 11th Tithi", "rituals": "Full day fast, Vishnu puja"},
    {"tithi": "Purnima", "name": "Purnima", "name_hindi": "पूर्णिमा", "type": "observance", "description": "Full Moon day", "rituals": "Charity, prayers, river bath"},
    {"tithi": "Amavasya", "name": "Amavasya", "name_hindi": "अमावस्या", "type": "observance", "description": "New Moon day", "rituals": "Tarpan for ancestors, oil lamp lighting"},
    {"tithi": "Chaturthi", "paksha": "Krishna", "name": "Sankashti Chaturthi", "name_hindi": "संकष्टी चतुर्थी", "type": "fasting", "description": "Monthly Ganesha fasting day", "rituals": "Fast till moonrise, Ganesha puja"},
    {"tithi": "Chaturdashi", "paksha": "Krishna", "name": "Masik Shivaratri", "name_hindi": "मासिक शिवरात्रि", "type": "fasting", "description": "Monthly Shiva worship night", "rituals": "Night vigil, Shiva abhishek"},
    {"tithi": "Saptami", "paksha": "Shukla", "name": "Vivah Panchami / Surya Saptami", "name_hindi": "सूर्य सप्तमी", "type": "observance", "description": "Sun worship day"},
    {"tithi": "Ashtami", "paksha": "Krishna", "name": "Kalashtami", "name_hindi": "कालाष्टमी", "type": "observance", "description": "Worship of Bhairava"},
    {"tithi": "Trayodashi", "paksha": "Shukla", "name": "Pradosh Vrat", "name_hindi": "प्रदोष व्रत", "type": "fasting", "description": "Shiva worship during twilight"},
    {"tithi": "Trayodashi", "paksha": "Krishna", "name": "Pradosh Vrat", "name_hindi": "प्रदोष व्रत", "type": "fasting", "description": "Shiva worship during twilight"},
]


# ============================================================
# 3. SOLAR FESTIVALS -- Fixed Gregorian date festivals
# ============================================================

SOLAR_FESTIVALS: List[Dict[str, Any]] = [
    {"month": 1, "day": 1, "name": "New Year", "name_hindi": "नया साल", "type": "observance", "description": "New Year's Day"},
    {"month": 1, "day": 14, "name": "Makar Sankranti / Pongal", "name_hindi": "मकर संक्रांति / पोंगल", "type": "major", "description": "Sun enters Capricorn - harvest festival"},
    {"month": 1, "day": 26, "name": "Republic Day", "name_hindi": "गणतंत्र दिवस", "type": "national", "description": "Republic Day of India"},
    {"month": 4, "day": 14, "name": "Mesha Sankranti / Baisakhi", "name_hindi": "मेष संक्रांति / बैसाखी", "type": "major", "description": "Sun enters Aries - Solar New Year"},
    {"month": 4, "day": 14, "name": "Dr. Ambedkar Jayanti", "name_hindi": "डॉ. अम्बेडकर जयंती", "type": "national", "description": "Birthday of Dr. B.R. Ambedkar"},
    {"month": 8, "day": 15, "name": "Independence Day", "name_hindi": "स्वतंत्रता दिवस", "type": "national", "description": "Independence Day of India"},
    {"month": 10, "day": 2, "name": "Gandhi Jayanti", "name_hindi": "गांधी जयंती", "type": "national", "description": "Birthday of Mahatma Gandhi"},
]


# ============================================================
# DETECTION FUNCTION
# ============================================================

def detect_festivals(
    tithi_name: str,
    paksha: str,
    nakshatra_name: str,
    maas: str = "",
    gregorian_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Detect festivals and vrats for given panchang elements.

    Checks all three sources:
    1. Specific annual festivals (tithi + paksha + maas)
    2. Recurring monthly festivals (tithi + optional paksha)
    3. Solar date festivals (Gregorian month + day)

    Args:
        tithi_name:      e.g. "Ekadashi", "Chaturthi"
        paksha:          "Shukla" or "Krishna"
        nakshatra_name:  e.g. "Pushya", "Rohini"
        maas:            Hindu month name, e.g. "Chaitra" (optional)
        gregorian_date:  YYYY-MM-DD string for solar date matching (optional)

    Returns:
        List of matching festival dicts with name, name_hindi, type, description.
    """
    matches: List[Dict[str, Any]] = []
    seen_names: set = set()

    def _add(entry: Dict[str, Any]) -> None:
        """Add a festival if not already present (deduplicate by name)."""
        name = entry.get("name", "")
        if name and name not in seen_names:
            seen_names.add(name)
            matches.append(entry)

    # ── 1. Specific annual tithi festivals ───────────────────
    for fest in TITHI_FESTIVALS:
        # Must match maas
        if not maas or fest["maas"] != maas:
            continue
        # Must match paksha
        if fest["paksha"] != paksha:
            continue
        # Must match tithi
        if fest["tithi"] != tithi_name:
            continue

        _add({
            "name": fest["name"],
            "name_hindi": fest.get("name_hindi", ""),
            "type": fest["type"],
            "description": fest.get("description", ""),
        })

    # ── 2. Recurring monthly festivals ───────────────────────
    for fest in RECURRING_FESTIVALS:
        # Must match tithi
        if fest["tithi"] != tithi_name:
            continue
        # If paksha specified, must match
        if fest.get("paksha") and fest["paksha"] != paksha:
            continue

        # Skip generic recurring if a specific annual festival already matched
        # for the same tithi (e.g., don't show "Ekadashi Vrat" when "Nirjala Ekadashi" matches)
        generic_name = fest["name"]
        _add({
            "name": generic_name,
            "name_hindi": fest.get("name_hindi", ""),
            "type": fest["type"],
            "description": fest.get("description", ""),
            "rituals": fest.get("rituals", ""),
        })

    # ── 3. Solar date festivals ──────────────────────────────
    if gregorian_date:
        try:
            dt = date.fromisoformat(gregorian_date)
            g_month = dt.month
            g_day = dt.day
            for fest in SOLAR_FESTIVALS:
                if fest["month"] == g_month and fest["day"] == g_day:
                    _add({
                        "name": fest["name"],
                        "name_hindi": fest.get("name_hindi", ""),
                        "type": fest["type"],
                        "description": fest.get("description", ""),
                    })
        except (ValueError, TypeError):
            pass  # Invalid date string -- skip solar matching

    return matches
