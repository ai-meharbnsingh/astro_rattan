"""
lalkitab_chandra_readings.py — Chandra Kundali (Moon-chart) LK interpretations
===============================================================================
Lal Kitab 1952 treats the Chandra Kundali as an INDEPENDENT predictive framework,
not a Vedic shortcut. The Moon is re-anchored to H1 and the chart is read as a
standalone emotional / mental / maternal chart.

Every reading in THIS file focuses on the MOON'S DOMAIN:
    emotion · memory · mother · public · mental states · habits · nourishment
    — as distinct from the Lagna chart's focus on self / body / dharma / karma.

Readings are intentionally COMPOSED (planet-emotion-quality × house-moon-domain)
and do NOT copy from `lalkitab_interpretations.py` (Lagna table). The compact
template form is canonical — LK 1952 itself gives terse Chandra aphorisms, not
expansive prose.

Source basis:
  - LK 1952 edition — Chandra Kundali prakaran
  - Pt. Roop Chand Joshi — twin-chart doctrine
  - Er. U.C. Mahajan commentaries on Moon-chart rules

Schema (per planet × house):
    {
      "en":           str  (1-2 sentences, Chandra-domain only)
      "hi":           str  (Devanagari, 1-2 sentences)
      "is_favourable": bool (for conflict detection with Lagna table)
    }
"""
from __future__ import annotations

from typing import Dict, Any


# ── Planet → Moon-domain emotional quality ─────────────────────
# Each planet carries a specific mental / emotional vector in LK.
_PLANET_QUALITY_EN: Dict[str, str] = {
    "Sun":     "ego-driven pride and paternal authority",
    "Moon":    "self-nourishing emotional stability",
    "Mars":    "restless emotional heat and impulsive temper",
    "Mercury": "mental chatter and nervous calculation",
    "Jupiter": "emotional wisdom and maternal blessing",
    "Venus":   "sentimental longing and domestic comfort",
    "Saturn":  "cold detachment and mental heaviness",
    "Rahu":    "anxious illusion and smoky intrusive thoughts",
    "Ketu":    "vague memory-loss and spiritual indifference",
}

_PLANET_QUALITY_HI: Dict[str, str] = {
    "Sun":     "अहंकारी आत्म-प्रतिष्ठा व पितृ-अधिकार",
    "Moon":    "आत्म-पोषक भावनात्मक स्थिरता",
    "Mars":    "बेचैन भावनात्मक ताप व तीव्र क्रोध",
    "Mercury": "मानसिक चंचलता व तर्क-गणना",
    "Jupiter": "भावनात्मक ज्ञान व माँ का आशीर्वाद",
    "Venus":   "भावुक चाहत व घरेलू सुख",
    "Saturn":  "ठंडी उदासीनता व मानसिक बोझ",
    "Rahu":    "व्यग्र भ्रम व धुंधले विचार",
    "Ketu":    "अस्पष्ट स्मृति-लोप व आध्यात्मिक उदासीनता",
}


# ── Chandra house → Moon-domain life area ──────────────────────
# LK-Chandra houses differ from Lagna-house meanings.
# Moon = H1 of Chandra Kundali; each subsequent house is Moon's relational field.
_CHANDRA_HOUSE_DOMAIN_EN: Dict[int, str] = {
    1:  "the inner self and moment-to-moment mood",
    2:  "spoken memory, taste, and family nourishment",
    3:  "emotional courage, siblings, and short mental journeys",
    4:  "the mother bond, home-feeling, and deep inner peace",
    5:  "emotional creativity, children of the heart, and mental offspring",
    6:  "mental afflictions, worries, and inner enemies",
    7:  "public mood, spouse-mind, and how crowds receive you",
    8:  "hidden fears, emotional shocks, and inherited grief",
    9:  "inherited faith, mother's dharma, and long soul-travels",
    10: "public reputation, fame of name, and emotional authority",
    11: "gains of affection, social circles, and fulfilled longings",
    12: "emotional retreat, dream-life, and the hidden subconscious",
}

_CHANDRA_HOUSE_DOMAIN_HI: Dict[int, str] = {
    1:  "अंतर्मन व क्षण-भर के मनोभाव",
    2:  "वाणी-स्मृति, स्वाद व पारिवारिक पोषण",
    3:  "भावनात्मक साहस, भाई-बहन व छोटी मानसिक यात्राएं",
    4:  "माँ का बंधन, घर का एहसास व गहरी आंतरिक शांति",
    5:  "भावनात्मक सृजनशीलता, हृदय-संतान व मानसिक उपज",
    6:  "मानसिक पीड़ा, चिंताएं व आंतरिक शत्रु",
    7:  "जन-मानस, जीवनसाथी का मन व भीड़ आपको कैसे स्वीकारती है",
    8:  "छिपे भय, भावनात्मक आघात व विरासती दुख",
    9:  "विरासती आस्था, माँ का धर्म व दीर्घ आत्मिक यात्राएं",
    10: "सार्वजनिक प्रतिष्ठा, नाम की कीर्ति व भावनात्मक प्रभुत्व",
    11: "स्नेह-लाभ, सामाजिक संबंध व पूर्ण चाहतें",
    12: "भावनात्मक एकांत, स्वप्न-जीवन व छिपा अवचेतन",
}


# ── Favourability grid (planet × chandra-house) ────────────────
# Based on LK 1952 Chandra prakaran — Moon is H1, so planet favourability
# is relative to Moon, NOT to Lagna. This is WHY Chandra chart can disagree
# with Lagna chart even for the same planet placement.
#
# Key LK 1952 rules encoded:
#   - Moon itself is always favourable in its own chart's H1
#   - Jupiter in Chandra H2/5/9/11 is emotionally auspicious
#   - Saturn in Chandra H1/4/7 afflicts mother and public mood
#   - Rahu in Chandra H4/5 = eclipsed mother / anxiety around children
#   - Mars in Chandra H4/7 = emotional volatility at home and with spouse
#   - Venus in Chandra H2/4/11 = domestic comfort and sentimental gains
#   - Sun in Chandra H4 = burnt home-peace (ego vs mother)
_IS_FAVOURABLE: Dict[str, Dict[int, bool]] = {
    "Sun":     {1: True,  2: True,  3: True,  4: False, 5: True,  6: True,  7: False, 8: False, 9: True,  10: True,  11: True,  12: False},
    "Moon":    {1: True,  2: True,  3: True,  4: True,  5: True,  6: False, 7: True,  8: False, 9: True,  10: True,  11: True,  12: True },
    "Mars":    {1: False, 2: False, 3: True,  4: False, 5: False, 6: True,  7: False, 8: False, 9: False, 10: True,  11: True,  12: False},
    "Mercury": {1: True,  2: True,  3: True,  4: True,  5: True,  6: False, 7: True,  8: False, 9: True,  10: True,  11: True,  12: False},
    "Jupiter": {1: True,  2: True,  3: False, 4: True,  5: True,  6: False, 7: True,  8: False, 9: True,  10: False, 11: True,  12: True },
    "Venus":   {1: True,  2: True,  3: True,  4: True,  5: True,  6: False, 7: True,  8: False, 9: True,  10: True,  11: True,  12: True },
    "Saturn":  {1: False, 2: False, 3: True,  4: False, 5: False, 6: True,  7: False, 8: False, 9: False, 10: True,  11: True,  12: False},
    "Rahu":    {1: False, 2: False, 3: True,  4: False, 5: False, 6: True,  7: False, 8: False, 9: False, 10: False, 11: True,  12: False},
    "Ketu":    {1: False, 2: False, 3: True,  4: False, 5: False, 6: True,  7: False, 8: True,  9: True,  10: False, 11: False, 12: True },
}


# ── Reading composer ───────────────────────────────────────────
def _compose_reading(planet: str, chandra_house: int) -> Dict[str, Any]:
    """
    Compose a compact Chandra-domain reading from:
        planet-emotion-quality  ×  chandra-house moon-domain
    Returns {en, hi, is_favourable}.

    Special-case: Moon in Chandra H1 is always fixed as "Moon itself is the
    lagna of this chart — emotional self-foundation."
    """
    if planet == "Moon" and chandra_house == 1:
        return {
            "en": (
                "Moon itself anchors the Chandra Kundali as H1. Emotional "
                "self-foundation is stable; your inner mood IS your life-stage."
            ),
            "hi": (
                "चंद्रमा स्वयं चंद्र कुंडली का लग्न है। भावनात्मक आत्म-आधार "
                "दृढ़ है; आपका आंतरिक मनोभाव ही आपका जीवन-मंच है।"
            ),
            "is_favourable": True,
        }

    q_en = _PLANET_QUALITY_EN.get(planet, "its planetary quality")
    q_hi = _PLANET_QUALITY_HI.get(planet, "अपनी ग्रह-प्रकृति")
    d_en = _CHANDRA_HOUSE_DOMAIN_EN.get(chandra_house, "this area of the mind")
    d_hi = _CHANDRA_HOUSE_DOMAIN_HI.get(chandra_house, "मन के इस क्षेत्र")
    fav = _IS_FAVOURABLE.get(planet, {}).get(chandra_house, False)

    if fav:
        en = (
            f"{planet} in Chandra H{chandra_house} channels {q_en} into "
            f"{d_en} — Moon blesses this placement with emotional ease."
        )
        hi = (
            f"चंद्र कुंडली के H{chandra_house} में {planet} की {q_hi} "
            f"{d_hi} में प्रवाहित होती है — चंद्रमा इस स्थान को "
            f"भावनात्मक सुख देता है।"
        )
    else:
        en = (
            f"{planet} in Chandra H{chandra_house} presses {q_en} onto "
            f"{d_en} — Moon reads this as emotional strain; protect the "
            f"heart through lunar remedies."
        )
        hi = (
            f"चंद्र कुंडली के H{chandra_house} में {planet} की {q_hi} "
            f"{d_hi} पर दबाव डालती है — चंद्रमा इसे भावनात्मक पीड़ा "
            f"मानता है; चंद्र-उपायों से हृदय की रक्षा करें।"
        )

    return {"en": en, "hi": hi, "is_favourable": fav}


# ── 108-entry Chandra readings table ───────────────────────────
# Generated once at import time. 9 planets × 12 houses = 108 readings.
# Keyed as (planet, chandra_house) tuple for O(1) lookup.
CHANDRA_READINGS: Dict[tuple, Dict[str, Any]] = {
    (planet, house): _compose_reading(planet, house)
    for planet in _PLANET_QUALITY_EN
    for house in range(1, 13)
}


def get_chandra_reading(planet: str, chandra_house: int) -> Dict[str, Any]:
    """
    Return the LK Chandra-context reading for a planet in a given Chandra-chart
    house. Returns {} if planet/house not found.

    Args:
        planet:        Planet name (Sun, Moon, Mars, Mercury, Jupiter, Venus,
                       Saturn, Rahu, Ketu)
        chandra_house: House number 1-12 in Chandra Kundali (Moon = H1)

    Returns:
        {en, hi, is_favourable} — empty dict on miss.
    """
    return CHANDRA_READINGS.get((planet, chandra_house), {})


__all__ = [
    "CHANDRA_READINGS",
    "get_chandra_reading",
]
