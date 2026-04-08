"""
festival_engine.py -- Rule-Based Hindu Festival & Vrat Detection Engine
=======================================================================
Detects festivals and vrats for a given date based on Tithi + Nakshatra rules.
NO hardcoded dates -- all festivals are computed from panchang elements.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


# ============================================================
# FESTIVAL RULES -- Tithi + Nakshatra + Paksha based
# ============================================================
# Each rule: {name, name_hindi, type, tithi_name, tithi_number, paksha,
#             nakshatra (optional), month_hint (optional), description}

FESTIVAL_RULES: List[Dict[str, Any]] = [
    # === EKADASHI VRATS (11th Tithi) ===
    {
        "name": "Ekadashi Vrat",
        "name_hindi": "एकादशी व्रत",
        "type": "fasting",
        "tithi_name": "Ekadashi",
        "paksha": None,  # Both Shukla and Krishna
        "description": "Sacred fasting day observed on the 11th Tithi of each Paksha.",
        "rituals": "Full day fast, Vishnu puja, Tulsi worship",
    },
    # === PRADOSH VRAT (13th Tithi evening) ===
    {
        "name": "Pradosh Vrat",
        "name_hindi": "प्रदोष व्रत",
        "type": "fasting",
        "tithi_name": "Trayodashi",
        "paksha": None,
        "description": "Shiva worship during Pradosh Kaal (evening of Trayodashi).",
        "rituals": "Evening Shiva puja, fasting till sunset",
    },
    # === PURNIMA (Full Moon) ===
    {
        "name": "Purnima",
        "name_hindi": "पूर्णिमा",
        "type": "major",
        "tithi_name": "Purnima",
        "paksha": "Shukla",
        "description": "Full Moon day - auspicious for charity, prayers, and rituals.",
        "rituals": "Satyanarayan Katha, charity, river bath",
    },
    # === AMAVASYA (New Moon) ===
    {
        "name": "Amavasya",
        "name_hindi": "अमावस्या",
        "type": "major",
        "tithi_name": "Amavasya",
        "paksha": "Krishna",
        "description": "New Moon day - Pitru Tarpan and ancestor worship.",
        "rituals": "Pitru Tarpan, Shani puja, oil donation",
    },
    # === CHATURTHI (Ganesh) ===
    {
        "name": "Sankashti Chaturthi",
        "name_hindi": "संकष्टी चतुर्थी",
        "type": "fasting",
        "tithi_name": "Chaturthi",
        "paksha": "Krishna",
        "description": "Monthly Ganesh vrat on Krishna Chaturthi.",
        "rituals": "Ganesh puja, moonrise sighting, fast breaking",
    },
    {
        "name": "Vinayaka Chaturthi",
        "name_hindi": "विनायक चतुर्थी",
        "type": "fasting",
        "tithi_name": "Chaturthi",
        "paksha": "Shukla",
        "description": "Monthly Ganesh worship on Shukla Chaturthi.",
        "rituals": "Ganesh puja, modak offering",
    },
    # === SHIVRATRI (Krishna Chaturdashi) ===
    {
        "name": "Masik Shivratri",
        "name_hindi": "मासिक शिवरात्रि",
        "type": "fasting",
        "tithi_name": "Chaturdashi",
        "paksha": "Krishna",
        "description": "Monthly Shivratri on Krishna Chaturdashi night.",
        "rituals": "Night vigil, Shiva abhishek, Rudrabhishek",
    },
    # === NAVAMI ===
    {
        "name": "Ram Navami Day",
        "name_hindi": "राम नवमी",
        "type": "major",
        "tithi_name": "Navami",
        "paksha": "Shukla",
        "maas": "Chaitra",
        "description": "Birthday of Lord Rama on Chaitra Shukla Navami.",
        "rituals": "Ram puja, Ramayana recital, fast",
    },
    # === PANCHAMI ===
    {
        "name": "Basant Panchami",
        "name_hindi": "बसंत पंचमी",
        "type": "major",
        "tithi_name": "Panchami",
        "paksha": "Shukla",
        "maas": "Magha",
        "description": "Saraswati Puja - onset of spring.",
        "rituals": "Saraswati puja, yellow clothes, sweet distribution",
    },
    # === ASHTAMI ===
    {
        "name": "Masik Durga Ashtami",
        "name_hindi": "मासिक दुर्गाष्टमी",
        "type": "fasting",
        "tithi_name": "Ashtami",
        "paksha": "Shukla",
        "description": "Monthly Durga worship on Shukla Ashtami.",
        "rituals": "Durga puja, kanya pujan, havan",
    },
    # === SAPTAMI ===
    {
        "name": "Surya Saptami",
        "name_hindi": "सूर्य सप्तमी",
        "type": "fasting",
        "tithi_name": "Saptami",
        "paksha": "Shukla",
        "description": "Sun worship on Shukla Saptami.",
        "rituals": "Surya Namaskar, Arghya to Sun",
    },
    # === DASHAMI ===
    {
        "name": "Dashami",
        "name_hindi": "दशमी",
        "type": "regional",
        "tithi_name": "Dashami",
        "paksha": "Shukla",
        "maas": "Ashwin",
        "description": "Vijaya Dashami / Dussehra - victory of good over evil.",
        "rituals": "Ravan Dahan, Shastra puja, Shami puja",
    },
    # === DWADASHI ===
    {
        "name": "Dwadashi Vrat",
        "name_hindi": "द्वादशी व्रत",
        "type": "fasting",
        "tithi_name": "Dwadashi",
        "paksha": "Shukla",
        "description": "Post-Ekadashi Parana day. Break fast during Parana window.",
        "rituals": "Parana (breaking Ekadashi fast) in correct window",
    },
    # === TRAYODASHI ===
    {
        "name": "Dhanteras",
        "name_hindi": "धनतेरस",
        "type": "major",
        "tithi_name": "Trayodashi",
        "paksha": "Krishna",
        "maas": "Kartik",
        "description": "Festival of wealth - buying gold and utensils.",
        "rituals": "Dhanvantari puja, buying metals, Lakshmi puja",
    },
    # === CHATURDASHI (Specific) ===
    {
        "name": "Narak Chaturdashi",
        "name_hindi": "नरक चतुर्दशी",
        "type": "major",
        "tithi_name": "Chaturdashi",
        "paksha": "Krishna",
        "maas": "Kartik",
        "description": "Chhoti Diwali - Lord Krishna's victory over Narakasura.",
        "rituals": "Early bath, Yama Deepdan, crackers",
    },
    # === NAKSHATRA-BASED ===
    {
        "name": "Pushya Nakshatra Day",
        "name_hindi": "पुष्य नक्षत्र",
        "type": "auspicious",
        "tithi_name": None,
        "paksha": None,
        "nakshatra": "Pushya",
        "description": "Highly auspicious nakshatra for buying gold, starting ventures.",
        "rituals": "Gold purchase, new ventures, investment",
    },
    {
        "name": "Rohini Vrat",
        "name_hindi": "रोहिणी व्रत",
        "type": "fasting",
        "tithi_name": None,
        "paksha": None,
        "nakshatra": "Rohini",
        "description": "Moon's exalted nakshatra - auspicious for Krishna worship.",
        "rituals": "Krishna puja, moon worship",
    },
]


def detect_festivals(
    tithi_name: str,
    paksha: str,
    nakshatra_name: str,
    maas: str = "",
) -> List[Dict[str, Any]]:
    """
    Detect festivals and vrats for given panchang elements.

    Args:
        tithi_name:     e.g. "Ekadashi", "Chaturthi"
        paksha:         "Shukla" or "Krishna"
        nakshatra_name: e.g. "Pushya", "Rohini"
        maas:           Hindu month name, e.g. "Chaitra" (optional for month-specific festivals)

    Returns:
        List of matching festival dicts with name, type, description, rituals.
    """
    matches: List[Dict[str, Any]] = []

    for rule in FESTIVAL_RULES:
        # Check tithi match
        if rule.get("tithi_name"):
            if rule["tithi_name"] != tithi_name:
                continue

        # Check paksha match (None means any paksha)
        if rule.get("paksha") and rule["paksha"] != paksha:
            continue

        # Check nakshatra match (only for nakshatra-based rules)
        if rule.get("nakshatra"):
            if rule["nakshatra"] != nakshatra_name:
                continue
        elif not rule.get("tithi_name"):
            # Rule has neither tithi nor nakshatra -- skip
            continue

        # Check maas match (only if rule specifies a month)
        if rule.get("maas") and maas:
            if rule["maas"] != maas:
                continue
        elif rule.get("maas") and not maas:
            # Rule needs a specific month but we don't know the month -- skip month-specific
            continue

        matches.append({
            "name": rule["name"],
            "name_hindi": rule.get("name_hindi", ""),
            "type": rule["type"],
            "description": rule["description"],
            "rituals": rule.get("rituals", ""),
        })

    return matches
