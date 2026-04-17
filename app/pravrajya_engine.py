"""
pravrajya_engine.py — Pravrajya (Ascetic / Renunciation) Yogas
===============================================================
Implements Adhyaya 27 of Phaladeepika (slokas 1–7).

Detects seven classical yogas indicating inclination toward asceticism,
renunciation, or spiritual withdrawal from worldly life:

  1. PARAMAHAMSA    — supreme ascetic, 4+ planets in one Kendra sign with Jupiter
  2. SANNYASI       — monastic renunciate, Saturn-Moon drekkana link
  3. TRIDANDI       — triple-staff monk, Jupiter in Lagna aspected by Saturn
  4. BHRUGUKACHCHA  — wandering ascetic, Sun+Mars+Saturn in Kendras/Trikonas
  5. VANAPRASTHA    — forest-dweller, 4+ equal-strength planets in Lagna
  6. VRIDDHASRAVAKA — aged listener-monk, Moon+Mars together aspected by Saturn
  7. CHARAKA        — wandering mendicant, weak Moon + Ketu in Lagna
"""
from __future__ import annotations
from typing import Any, Dict, List

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

EXALTATION_SIGN = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra",
}

DEBILITATION_SIGN = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries",
}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Extra (non-universal) aspect offsets from planet's house (1-indexed, +7 always aspected)
SPECIAL_ASPECTS = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _planets_in_sign(planets: Dict[str, Dict[str, Any]], sign: str) -> List[str]:
    """Return list of planet names occupying a given sign."""
    return [name for name, data in planets.items() if (data or {}).get("sign") == sign]


def _planets_in_house(planets: Dict[str, Dict[str, Any]], house: int) -> List[str]:
    """Return list of planet names occupying a given house (1-12)."""
    return [name for name, data in planets.items() if (data or {}).get("house") == house]


def _is_drekkana(planet_longitude: float, drekkana_num: int, sign: str) -> bool:
    """
    Check whether a planet sits in the specified drekkana (1/2/3) of a sign.
    Each sign spans 30°; drekkana 1 = 0-10°, 2 = 10-20°, 3 = 20-30°.
    planet_longitude is absolute (0-360).
    """
    if sign not in ZODIAC:
        return False
    try:
        lon = float(planet_longitude) % 360
    except (TypeError, ValueError):
        return False
    sign_start = ZODIAC.index(sign) * 30
    sign_end = sign_start + 30
    if not (sign_start <= lon < sign_end):
        return False
    pos_in_sign = lon - sign_start
    if drekkana_num == 1:
        return 0 <= pos_in_sign < 10
    if drekkana_num == 2:
        return 10 <= pos_in_sign < 20
    if drekkana_num == 3:
        return 20 <= pos_in_sign < 30
    return False


def _house_of_planet(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> int:
    """Return house of planet or 0 if missing."""
    p = planets.get(planet_name) or {}
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _sign_of_planet(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> str:
    p = planets.get(planet_name) or {}
    return str(p.get("sign", ""))


def _houses_aspected_by(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> List[int]:
    """All houses aspected by a planet (7th universal + special).
    "Nth from H" in Vedic astrology counts H as 1st, so offset = N-1."""
    h = _house_of_planet(planet_name, planets)
    if h < 1 or h > 12:
        return []
    aspects = [((h - 1 + 6) % 12) + 1]  # universal 7th (opposite house)
    for off in SPECIAL_ASPECTS.get(planet_name, []):
        aspects.append(((h - 1 + off - 1) % 12) + 1)
    return aspects


def _aspects_planet(source: str, target: str, planets: Dict[str, Dict[str, Any]]) -> bool:
    """True if `source` planet aspects the house occupied by `target` planet."""
    target_h = _house_of_planet(target, planets)
    if target_h < 1:
        return False
    return target_h in _houses_aspected_by(source, planets)


def _aspects_house(source: str, house: int, planets: Dict[str, Dict[str, Any]]) -> bool:
    """True if `source` planet aspects the given house number."""
    return house in _houses_aspected_by(source, planets)


def _sign_house(sign: str, ascendant_sign: str) -> int:
    """Return the house number (1-12) occupied by a sign given the ascendant."""
    if sign not in ZODIAC or ascendant_sign not in ZODIAC:
        return 0
    asc_idx = ZODIAC.index(ascendant_sign)
    sign_idx = ZODIAC.index(sign)
    return ((sign_idx - asc_idx) % 12) + 1


def _is_exalted(planet_name: str, sign: str) -> bool:
    return EXALTATION_SIGN.get(planet_name) == sign


def _is_debilitated(planet_name: str, sign: str) -> bool:
    return DEBILITATION_SIGN.get(planet_name) == sign


def _is_own_sign(planet_name: str, sign: str) -> bool:
    return SIGN_LORD.get(sign) == planet_name


# ───────────────────────────────────────────────────────────────
# Yoga detectors
# ───────────────────────────────────────────────────────────────

def _detect_paramahamsa(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    4+ planets (excluding Moon) in ONE sign, Jupiter among them,
    and that sign sits in a Kendra (1, 4, 7, 10).
    """
    planets = chart.get("planets", {}) or {}
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")
    factors: List[str] = []

    for sign in ZODIAC:
        occupants = _planets_in_sign(planets, sign)
        non_moon = [p for p in occupants if p != "Moon"]
        if len(non_moon) < 4 or "Jupiter" not in non_moon:
            continue
        h = _sign_house(sign, asc_sign)
        if h not in KENDRAS:
            continue

        factors.append(f"{len(non_moon)} planets in {sign}")
        factors.append(f"Jupiter present in {sign}")
        factors.append(f"{sign} is in Kendra (house {h})")

        jup_sign = _sign_of_planet("Jupiter", planets)
        if _is_exalted("Jupiter", jup_sign):
            factors.append("Jupiter exalted")
        if _is_own_sign("Jupiter", jup_sign):
            factors.append("Jupiter in own sign")
        if h == 1:
            factors.append("Cluster in Lagna (strongest Kendra)")

        strength = min(10, 5 + len(non_moon) - 4 + (1 if _is_exalted("Jupiter", jup_sign) else 0))
        return {
            "key": "paramahamsa",
            "name_en": "Paramahamsa",
            "name_hi": "परमहंस",
            "strength": strength,
            "effect_en": "Supreme ascetic yoga. Native renounces all worldly attachments and attains the highest spiritual realization.",
            "effect_hi": "परम संन्यास योग। जातक सभी सांसारिक आसक्तियों का त्याग करके सर्वोच्च आध्यात्मिक अनुभूति प्राप्त करता है।",
            "sloka_ref": "Phaladeepika Adh. 27 sloka 1",
            "supporting_factors": factors,
        }
    return None


def _detect_sannyasi(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Saturn aspects Moon, AND Moon sits in Saturn's drekkana
    (2nd or 3rd drekkana of Capricorn/Aquarius).
    """
    planets = chart.get("planets", {}) or {}
    moon = planets.get("Moon") or {}
    if not planets.get("Saturn") or not moon:
        return None

    if not _aspects_planet("Saturn", "Moon", planets):
        return None

    moon_sign = str(moon.get("sign", ""))
    moon_lon = moon.get("longitude", moon.get("sign_degree", 0))
    # Moon in Saturn's drekkana — 2nd/3rd decan of Capricorn or Aquarius
    in_saturn_dk = False
    for sign in ("Capricorn", "Aquarius"):
        if moon_sign == sign and (_is_drekkana(moon_lon, 2, sign) or _is_drekkana(moon_lon, 3, sign)):
            in_saturn_dk = True
            break
    if not in_saturn_dk:
        return None

    factors = [
        "Saturn aspects Moon",
        f"Moon in Saturn's drekkana of {moon_sign}",
    ]
    sat_sign = _sign_of_planet("Saturn", planets)
    if _is_exalted("Saturn", sat_sign):
        factors.append("Saturn exalted")
    if _is_own_sign("Saturn", sat_sign):
        factors.append("Saturn in own sign")

    strength = min(10, 6 + (1 if _is_exalted("Saturn", sat_sign) else 0) + (1 if _is_own_sign("Saturn", sat_sign) else 0))
    return {
        "key": "sannyasi",
        "name_en": "Sannyasi",
        "name_hi": "संन्यासी",
        "strength": strength,
        "effect_en": "Monastic renunciate yoga. Native takes formal sannyasa and devotes life to disciplined spiritual practice.",
        "effect_hi": "संन्यास योग। जातक विधिवत संन्यास लेकर अनुशासित आध्यात्मिक साधना में जीवन समर्पित करता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 2",
        "supporting_factors": factors,
    }


def _detect_tridandi(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """Jupiter in Lagna (1st house), aspected by Saturn."""
    planets = chart.get("planets", {}) or {}
    if _house_of_planet("Jupiter", planets) != 1:
        return None
    if not _aspects_house("Saturn", 1, planets):
        return None

    factors = ["Jupiter in Lagna (1st house)", "Saturn aspects 1st house"]
    jup_sign = _sign_of_planet("Jupiter", planets)
    if _is_exalted("Jupiter", jup_sign):
        factors.append("Jupiter exalted in Lagna")
    if _is_own_sign("Jupiter", jup_sign):
        factors.append("Jupiter in own sign in Lagna")

    strength = min(10, 6 + (2 if _is_exalted("Jupiter", jup_sign) else 0) + (1 if _is_own_sign("Jupiter", jup_sign) else 0))
    return {
        "key": "tridandi",
        "name_en": "Tridandi",
        "name_hi": "त्रिदण्डी",
        "strength": strength,
        "effect_en": "Triple-staff monk yoga. Native takes up the tridanda sannyasa (Vaishnava order) and lives a life of teaching and detachment.",
        "effect_hi": "त्रिदण्डी संन्यास योग। जातक त्रिदण्ड संन्यास (वैष्णव परम्परा) ग्रहण कर शिक्षण और वैराग्य का जीवन जीता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 3",
        "supporting_factors": factors,
    }


def _detect_bhrugukachcha(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Sun, Mars, AND Saturn all occupy either Kendras (1,4,7,10)
    or Trikonas (1,5,9).
    """
    planets = chart.get("planets", {}) or {}
    good_houses = KENDRAS | TRIKONAS
    positions = {}
    for p in ("Sun", "Mars", "Saturn"):
        h = _house_of_planet(p, planets)
        if h not in good_houses:
            return None
        positions[p] = h

    factors = [f"{p} in house {h}" for p, h in positions.items()]
    # Count how many are in Kendra specifically (stronger than plain Trikona for ascetic yoga)
    kendra_count = sum(1 for h in positions.values() if h in KENDRAS)
    if kendra_count >= 2:
        factors.append(f"{kendra_count} of 3 planets in Kendras")

    strength = min(10, 5 + kendra_count)
    return {
        "key": "bhrugukachcha",
        "name_en": "Bhrugukachcha",
        "name_hi": "भृगुकच्छ",
        "strength": strength,
        "effect_en": "Wandering ascetic yoga. Native travels to holy places, lives on alms, and gains spiritual merit through pilgrimage.",
        "effect_hi": "भ्रमणशील संन्यास योग। जातक तीर्थाटन करता है, भिक्षा पर जीवन व्यतीत करता है और तीर्थयात्रा द्वारा पुण्य अर्जित करता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 4",
        "supporting_factors": factors,
    }


def _detect_vanaprastha(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """4 or more planets in Lagna (1st house)."""
    planets = chart.get("planets", {}) or {}
    lagna_planets = _planets_in_house(planets, 1)
    if len(lagna_planets) < 4:
        return None

    factors = [f"{len(lagna_planets)} planets in Lagna: {', '.join(lagna_planets)}"]
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")
    benefic_count = sum(1 for p in lagna_planets if p in BENEFICS)
    if benefic_count >= 2:
        factors.append(f"{benefic_count} benefics among Lagna cluster")
    if any(_is_exalted(p, asc_sign) for p in lagna_planets):
        factors.append("At least one exalted planet in Lagna")

    strength = min(10, 5 + (len(lagna_planets) - 4) + (1 if benefic_count >= 2 else 0))
    return {
        "key": "vanaprastha",
        "name_en": "Vanaprastha",
        "name_hi": "वानप्रस्थ",
        "strength": strength,
        "effect_en": "Forest-dweller yoga. Native gradually withdraws from household life and retires to contemplative solitude in later years.",
        "effect_hi": "वानप्रस्थ योग। जातक धीरे-धीरे गृहस्थ जीवन से विमुख होकर वृद्धावस्था में चिंतन एवं एकांत में रहता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 5",
        "supporting_factors": factors,
    }


def _detect_vriddhasravaka(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """Moon and Mars in the same house, aspected by Saturn."""
    planets = chart.get("planets", {}) or {}
    mh = _house_of_planet("Moon", planets)
    mah = _house_of_planet("Mars", planets)
    if mh < 1 or mh != mah:
        return None
    if not _aspects_house("Saturn", mh, planets):
        return None

    factors = [
        f"Moon + Mars together in house {mh}",
        f"Saturn aspects house {mh}",
    ]
    moon_sign = _sign_of_planet("Moon", planets)
    if _is_debilitated("Moon", moon_sign):
        factors.append("Moon debilitated (intensifies detachment)")

    strength = min(10, 6 + (1 if _is_debilitated("Moon", moon_sign) else 0))
    return {
        "key": "vriddhasravaka",
        "name_en": "Vriddhasravaka",
        "name_hi": "वृद्धश्रावक",
        "strength": strength,
        "effect_en": "Aged listener-monk yoga. Native embraces renunciation in advanced years and studies sacred scriptures as a lay disciple.",
        "effect_hi": "वृद्धश्रावक योग। जातक वृद्धावस्था में संन्यास लेता है और साधक-शिष्य के रूप में धर्मग्रंथों का अध्ययन करता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 6",
        "supporting_factors": factors,
    }


def _detect_charaka(chart: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Moon is weak (debilitated, in 6/8/12, or aspected by malefics)
    AND Ketu in Lagna.
    """
    planets = chart.get("planets", {}) or {}
    if _house_of_planet("Ketu", planets) != 1:
        return None
    moon = planets.get("Moon") or {}
    if not moon:
        return None

    moon_house = _house_of_planet("Moon", planets)
    moon_sign = str(moon.get("sign", ""))

    weaknesses = []
    if _is_debilitated("Moon", moon_sign):
        weaknesses.append("Moon debilitated")
    if moon_house in DUSTHANAS:
        weaknesses.append(f"Moon in Dusthana (house {moon_house})")
    # Aspected by malefic (excluding Moon itself)
    malefic_aspects = [
        m for m in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
        if m in planets and _aspects_planet(m, "Moon", planets)
    ]
    if malefic_aspects:
        weaknesses.append(f"Moon aspected by malefics: {', '.join(malefic_aspects)}")

    if not weaknesses:
        return None

    factors = ["Ketu in Lagna"] + weaknesses
    strength = min(10, 5 + len(weaknesses))
    return {
        "key": "charaka",
        "name_en": "Charaka",
        "name_hi": "चरक",
        "strength": strength,
        "effect_en": "Wandering mendicant yoga. Native renounces a fixed home, travels constantly as a beggar-ascetic, and is supported by strangers.",
        "effect_hi": "चरक (भ्रमणशील भिक्षुक) योग। जातक स्थायी निवास त्यागकर भिक्षुक संन्यासी के रूप में भ्रमण करता है और अजनबियों से सहायता प्राप्त करता है।",
        "sloka_ref": "Phaladeepika Adh. 27 sloka 7",
        "supporting_factors": factors,
    }


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def detect_pravrajya(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect all Pravrajya (ascetic) yogas from Phaladeepika Adhyaya 27.

    Args:
        chart_data: {
            'planets': {'Sun': {'sign': 'Aries', 'house': 1, 'longitude': 12.3, ...}, ...},
            'ascendant': {'sign': 'Aries', 'longitude': 0},
            ...
        }

    Returns:
        {
            'yogas_found': [ {key, name_en, name_hi, strength, effect_en, effect_hi,
                              sloka_ref, supporting_factors}, ... ],
            'count': int,
            'has_ascetic_tendency': bool,
        }
    """
    if not isinstance(chart_data, dict):
        return {"yogas_found": [], "count": 0, "has_ascetic_tendency": False}

    detectors = (
        _detect_paramahamsa,
        _detect_sannyasi,
        _detect_tridandi,
        _detect_bhrugukachcha,
        _detect_vanaprastha,
        _detect_vriddhasravaka,
        _detect_charaka,
    )

    found: List[Dict[str, Any]] = []
    for detector in detectors:
        try:
            result = detector(chart_data)
        except Exception:
            result = None
        if result:
            found.append(result)

    return {
        "yogas_found": found,
        "count": len(found),
        "has_ascetic_tendency": len(found) > 0,
    }
