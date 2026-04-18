"""
app/lalkitab_remedy_matrix.py

P2.11 — Direction + Colour + Material remedy matrix.

Lal Kitab 1952 references direction (disha), colour (rang), and material
(dhaatu) throughout the remedy chapters but never assembles them into a
single lookup. This module fixes that gap by freezing the canonical
planet-matrix derived from LK Vastu + remedy tables.

Sources
-------
  - LK 1952 Vastu chapter (directions)
  - LK 1952 material tables (donation items, amulets)
  - LK 1952 colour mentions in remedy verses (orange for Sun, white for
    Moon, red for Mars, green for Mercury, yellow for Jupiter, pink/white
    for Venus, black/blue for Saturn, grey for Rahu, brown/multi for Ketu)

The matrix is frozen because these three axes NEVER change per-chart —
they are planet-intrinsic (unlike tithi, which tracks the lunar calendar).
"""
from __future__ import annotations

from typing import Any, Dict, List


# ─────────────────────────────────────────────────────────────
# DIRECTION (disha) per planet — aligned with LK Vastu chapter.
# bearing_deg = compass bearing (0 = North, 90 = East, …).
# ─────────────────────────────────────────────────────────────
PLANET_DIRECTION: Dict[str, Dict[str, Any]] = {
    "Sun":     {"en": "East",       "hi": "पूर्व",       "bearing_deg": 90},
    "Moon":    {"en": "North-West", "hi": "वायव्य",      "bearing_deg": 315},
    "Mars":    {"en": "South",      "hi": "दक्षिण",      "bearing_deg": 180},
    "Mercury": {"en": "North",      "hi": "उत्तर",       "bearing_deg": 0},
    "Jupiter": {"en": "North-East", "hi": "ईशान",        "bearing_deg": 45},
    "Venus":   {"en": "South-East", "hi": "आग्नेय",      "bearing_deg": 135},
    "Saturn":  {"en": "West",       "hi": "पश्चिम",      "bearing_deg": 270},
    "Rahu":    {"en": "South-West", "hi": "नैऋत्य",      "bearing_deg": 225},
    "Ketu":    {"en": "South",      "hi": "दक्षिण",      "bearing_deg": 180},
}


# ─────────────────────────────────────────────────────────────
# COLOURS per planet. `hex` is a UI-ready representative of `primary_en`.
# alt_en / alt_hi list secondary LK-admissible colours.
# ─────────────────────────────────────────────────────────────
PLANET_COLOURS: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "primary_en": "Orange", "primary_hi": "नारंगी", "hex": "#E65100",
        "alt_en": ["Red", "Deep Gold"],   "alt_hi": ["लाल", "गहरा सुनहरा"],
    },
    "Moon": {
        "primary_en": "White", "primary_hi": "श्वेत", "hex": "#F5F5F5",
        "alt_en": ["Silver", "Off-white"], "alt_hi": ["चांदी-रंग", "हल्का श्वेत"],
    },
    "Mars": {
        "primary_en": "Red", "primary_hi": "लाल", "hex": "#C62828",
        "alt_en": ["Blood-red"], "alt_hi": ["रक्त-लाल"],
    },
    "Mercury": {
        "primary_en": "Green", "primary_hi": "हरा", "hex": "#2E7D32",
        "alt_en": ["Emerald"], "alt_hi": ["पन्ना-हरा"],
    },
    "Jupiter": {
        "primary_en": "Yellow", "primary_hi": "पीला", "hex": "#F9A825",
        "alt_en": ["Saffron", "Deep Yellow"], "alt_hi": ["केसरिया", "गहरा पीला"],
    },
    "Venus": {
        "primary_en": "Pink", "primary_hi": "गुलाबी", "hex": "#F48FB1",
        "alt_en": ["White", "Cream"], "alt_hi": ["श्वेत", "क्रीम"],
    },
    "Saturn": {
        "primary_en": "Black", "primary_hi": "काला", "hex": "#212121",
        "alt_en": ["Dark Blue"], "alt_hi": ["गहरा नीला"],
    },
    "Rahu": {
        "primary_en": "Grey", "primary_hi": "धूसर", "hex": "#616161",
        "alt_en": ["Smoky"], "alt_hi": ["धुएँ-सा"],
    },
    "Ketu": {
        "primary_en": "Brown", "primary_hi": "भूरा", "hex": "#6D4C41",
        "alt_en": ["Multi-colour", "Variegated"], "alt_hi": ["बहुरंगी", "चित्रित"],
    },
}


# ─────────────────────────────────────────────────────────────
# MATERIALS (dhaatu) per planet. `primary_*` is the single most common
# donation/amulet material; `alt` lists secondary materials + gemstones.
# ─────────────────────────────────────────────────────────────
PLANET_MATERIALS: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "primary_en": "Copper", "primary_hi": "तांबा",
        "alt": ["Ruby gemstone", "Gold"],
        "alt_hi": ["माणिक्य रत्न", "स्वर्ण"],
    },
    "Moon": {
        "primary_en": "Silver", "primary_hi": "चांदी",
        "alt": ["Pearl", "Rice", "Milk"],
        "alt_hi": ["मोती", "चावल", "दूध"],
    },
    "Mars": {
        "primary_en": "Copper", "primary_hi": "तांबा",
        "alt": ["Iron", "Red Coral gemstone"],
        "alt_hi": ["लोहा", "मूंगा रत्न"],
    },
    "Mercury": {
        "primary_en": "Brass", "primary_hi": "पीतल",
        "alt": ["Emerald gemstone", "Green mung dal"],
        "alt_hi": ["पन्ना रत्न", "हरी मूंग दाल"],
    },
    "Jupiter": {
        "primary_en": "Gold", "primary_hi": "स्वर्ण",
        "alt": ["Yellow Sapphire gemstone", "Turmeric", "Chana dal"],
        "alt_hi": ["पुखराज रत्न", "हल्दी", "चने की दाल"],
    },
    "Venus": {
        "primary_en": "Silver", "primary_hi": "चांदी",
        "alt": ["Diamond gemstone", "White cloth"],
        "alt_hi": ["हीरा रत्न", "श्वेत वस्त्र"],
    },
    "Saturn": {
        "primary_en": "Iron", "primary_hi": "लोहा",
        "alt": ["Blue Sapphire gemstone", "Sesame oil (mustard substitute)"],
        "alt_hi": ["नीलम रत्न", "तिल का तेल (सरसों विकल्प)"],
    },
    "Rahu": {
        "primary_en": "Lead", "primary_hi": "सीसा",
        "alt": ["Hessonite (Gomed) gemstone", "Barley"],
        "alt_hi": ["गोमेद रत्न", "जौ"],
    },
    "Ketu": {
        "primary_en": "Bronze", "primary_hi": "कांसा",
        "alt": ["Cat's Eye gemstone", "Variegated cloth"],
        "alt_hi": ["लहसुनिया रत्न", "चित्रित वस्त्र"],
    },
}


def get_remedy_matrix(planet: str) -> Dict[str, Any]:
    """
    Return the frozen direction/colour/material matrix for a planet.

    Args:
        planet: "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                "Saturn", "Rahu", "Ketu".

    Returns:
        {
            direction : {en, hi, bearing_deg},
            colour    : {primary_en, primary_hi, hex, alt_en, alt_hi},
            material  : {primary_en, primary_hi, alt, alt_hi},
            lk_ref    : "Vastu + remedy tables",
            source    : "LK_CANONICAL",
        }

    Unknown planets return a safe empty-but-valid shape so callers don't
    need to null-guard.
    """
    direction = PLANET_DIRECTION.get(planet)
    colour = PLANET_COLOURS.get(planet)
    material = PLANET_MATERIALS.get(planet)

    if not direction or not colour or not material:
        return {
            "direction": {"en": "", "hi": "", "bearing_deg": None},
            "colour": {
                "primary_en": "", "primary_hi": "", "hex": "",
                "alt_en": [], "alt_hi": [],
            },
            "material": {
                "primary_en": "", "primary_hi": "",
                "alt": [], "alt_hi": [],
            },
            "lk_ref": "Vastu + remedy tables",
            "source": "LK_CANONICAL",
        }

    return {
        "direction": dict(direction),
        "colour": dict(colour),
        "material": dict(material),
        "lk_ref": "Vastu + remedy tables",
        "source": "LK_CANONICAL",
    }


def list_supported_planets() -> List[str]:
    """Convenience: enumerate planets with a full matrix entry."""
    return [
        p for p in PLANET_DIRECTION
        if p in PLANET_COLOURS and p in PLANET_MATERIALS
    ]
