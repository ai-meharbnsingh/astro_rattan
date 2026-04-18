"""
apatya_engine.py — Apatya (Progeny / Children) Analysis
=======================================================
Implements Phaladeepika Adhyaya 12 — Apatyadhyaya (slokas 2–20).

Classical analysis of progeny/children prospects, grounded in:
  - 5th house (putra-bhava — children, creativity, purva-punya)
  - 5th house lord (placement, dignity, aspects)
  - Jupiter (natural karaka for progeny)
  - Saptamsa (D7) divisional reference (outer caller may supply `d7_planets`)

Eight classical yogas detected (Adh. 12):
  1. PUTRA-YOGA            — blessing of children
  2. APUTRA-YOGA           — denial of children
  3. DATTAKA-YOGA          — adoption only
  4. KANYA-YOGA            — female-only issue
  5. PUTRA-HANI-YOGA       — loss of children
  6. BAHU-PUTRA-YOGA       — many children
  7. JYESHTA-PUTRA-YOGA    — virtuous first-born
  8. DELAYED-PROGENY-YOGA  — late/difficult conception
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

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

# Female (even) signs per classical Vedic scheme
FEMALE_SIGNS = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}
# Male (odd) signs
MALE_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Saturn's own/mulatrikona signs (for DELAYED-PROGENY yoga)
SATURN_SIGNS = {"Capricorn", "Aquarius"}

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

def _is_female_sign(sign: str) -> bool:
    """True if sign is a female (even) sign per Vedic classification."""
    return sign in FEMALE_SIGNS


def _house_of_planet(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> int:
    p = planets.get(planet_name) or {}
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _sign_of_planet(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> str:
    p = planets.get(planet_name) or {}
    return str(p.get("sign", ""))


def _planets_in_house(planets: Dict[str, Dict[str, Any]], house: int) -> List[str]:
    return [name for name, data in planets.items() if (data or {}).get("house") == house]


def _sign_house(sign: str, ascendant_sign: str) -> int:
    """House number (1-12) occupied by a sign given the ascendant."""
    if sign not in ZODIAC or ascendant_sign not in ZODIAC:
        return 0
    asc_idx = ZODIAC.index(ascendant_sign)
    sign_idx = ZODIAC.index(sign)
    return ((sign_idx - asc_idx) % 12) + 1


def _house_sign(house: int, ascendant_sign: str) -> str:
    """Sign occupying the Nth house given ascendant."""
    if ascendant_sign not in ZODIAC or not (1 <= house <= 12):
        return ""
    asc_idx = ZODIAC.index(ascendant_sign)
    return ZODIAC[(asc_idx + house - 1) % 12]


def _houses_aspected_by(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> List[int]:
    """All houses aspected by a planet (7th universal + special aspects)."""
    h = _house_of_planet(planet_name, planets)
    if h < 1 or h > 12:
        return []
    aspects = [((h - 1 + 6) % 12) + 1]  # universal 7th
    for off in SPECIAL_ASPECTS.get(planet_name, []):
        aspects.append(((h - 1 + off - 1) % 12) + 1)
    return aspects


def _aspects_house(source: str, house: int, planets: Dict[str, Dict[str, Any]]) -> bool:
    return house in _houses_aspected_by(source, planets)


def _is_exalted(planet: str, sign: str) -> bool:
    return EXALTATION_SIGN.get(planet) == sign


def _is_debilitated(planet: str, sign: str) -> bool:
    return DEBILITATION_SIGN.get(planet) == sign


def _is_own_sign(planet: str, sign: str) -> bool:
    return SIGN_LORD.get(sign) == planet


def _planet_strength(planet: str, planets: Dict[str, Dict[str, Any]]) -> str:
    """Coarse strength: 'strong' | 'moderate' | 'weak'."""
    p = planets.get(planet) or {}
    sign = str(p.get("sign", ""))
    house = _house_of_planet(planet, planets)
    if _is_exalted(planet, sign) or _is_own_sign(planet, sign):
        return "strong"
    if _is_debilitated(planet, sign):
        return "weak"
    if house in DUSTHANAS:
        return "weak"
    if house in KENDRAS or house in TRIKONAS:
        return "strong"
    return "moderate"


def _malefic_aspects_house(house: int, planets: Dict[str, Dict[str, Any]]) -> List[str]:
    return [m for m in MALEFICS if m in planets and _aspects_house(m, house, planets)]


def _fifth_lord_info(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Return 5th lord's name, placement, sign, strength, aspects."""
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")
    planets = chart.get("planets", {}) or {}
    fifth_sign = _house_sign(5, asc_sign)
    lord = SIGN_LORD.get(fifth_sign, "")
    if not lord or lord not in planets:
        return {
            "lord": lord, "placement": 0, "sign": "",
            "strength": "unknown", "aspected_by_malefics": [],
            "fifth_sign": fifth_sign,
        }
    lord_house = _house_of_planet(lord, planets)
    lord_sign = _sign_of_planet(lord, planets)
    malefic_aspects = [
        m for m in MALEFICS
        if m in planets and lord_house > 0 and _aspects_house(m, lord_house, planets)
    ]
    return {
        "lord": lord,
        "placement": lord_house,
        "sign": lord_sign,
        "strength": _planet_strength(lord, planets),
        "aspected_by_malefics": malefic_aspects,
        "fifth_sign": fifth_sign,
    }


def _jupiter_info(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter's placement, sign, and strength (natural karaka for progeny)."""
    planets = chart.get("planets", {}) or {}
    if "Jupiter" not in planets:
        return {"placement": 0, "sign": "", "strength": "unknown"}
    return {
        "placement": _house_of_planet("Jupiter", planets),
        "sign": _sign_of_planet("Jupiter", planets),
        "strength": _planet_strength("Jupiter", planets),
    }


# ───────────────────────────────────────────────────────────────
# Yoga detectors (8 classical — Adh. 12)
# ───────────────────────────────────────────────────────────────

def _detect_putra_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Strong 5th lord + Jupiter in Kendra/Trikona + 5th house unafflicted."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    if info5["strength"] != "strong":
        return None
    if jup["placement"] not in (KENDRAS | TRIKONAS):
        return None
    # 5th house itself: no malefic present and no malefic aspect
    malefics_in_5 = [p for p in _planets_in_house(planets, 5) if p in MALEFICS]
    malefic_aspects_5 = _malefic_aspects_house(5, planets)
    if malefics_in_5 or malefic_aspects_5:
        return None

    factors = [
        f"5th lord ({info5['lord']}) is strong",
        f"Jupiter in house {jup['placement']} (Kendra/Trikona)",
        "5th house unafflicted by malefics",
    ]
    if jup["strength"] == "strong":
        factors.append("Jupiter itself strong")
    return {
        "key": "putra_yoga",
        "name_en": "Putra Yoga",
        "name_hi": "पुत्र योग",
        "effect_en": "Blessing of worthy children. Native obtains virtuous and long-lived offspring.",
        "effect_hi": "श्रेष्ठ संतान का सुख। जातक को सद्गुणी, दीर्घायु संतान प्राप्त होती है।",
        "probability": "high",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 2",
        "supporting_factors": factors,
    }


def _detect_aputra_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """5th house + 5th lord + Jupiter ALL afflicted (denial of children)."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    # 5th house afflicted: malefic present OR malefic aspect
    malefics_in_5 = [p for p in _planets_in_house(planets, 5) if p in MALEFICS]
    malefic_aspects_5 = _malefic_aspects_house(5, planets)
    fifth_afflicted = bool(malefics_in_5) or bool(malefic_aspects_5)

    # 5th lord afflicted: weak OR in Dusthana OR aspected by malefics
    lord_afflicted = (
        info5["strength"] == "weak"
        or info5["placement"] in DUSTHANAS
        or bool(info5["aspected_by_malefics"])
    )

    # Jupiter afflicted: weak OR in Dusthana OR debilitated
    jup_weak = jup["strength"] == "weak" or jup["placement"] in DUSTHANAS
    if jup["sign"] and _is_debilitated("Jupiter", jup["sign"]):
        jup_weak = True

    if not (fifth_afflicted and lord_afflicted and jup_weak):
        return None

    factors: List[str] = []
    if malefics_in_5:
        factors.append(f"Malefic(s) in 5th house: {', '.join(malefics_in_5)}")
    if malefic_aspects_5:
        factors.append(f"5th house aspected by malefics: {', '.join(malefic_aspects_5)}")
    factors.append(f"5th lord ({info5['lord']}) afflicted — placement house {info5['placement']}, strength {info5['strength']}")
    factors.append(f"Jupiter afflicted — house {jup['placement']}, strength {jup['strength']}")
    return {
        "key": "aputra_yoga",
        "name_en": "Aputra Yoga",
        "name_hi": "अपुत्र योग",
        "effect_en": "Denial or obstruction of progeny. Difficulty conceiving or loss of hope of children without remedies.",
        "effect_hi": "संतान का अभाव या बाधा। बिना उपाय के संतति की आशा क्षीण होती है।",
        "probability": "high",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 5",
        "supporting_factors": factors,
    }


def _detect_dattaka_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """5th lord in 6/8/12 + malefic in 5th + Jupiter weak → adoption only."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    if info5["placement"] not in DUSTHANAS:
        return None
    malefics_in_5 = [p for p in _planets_in_house(planets, 5) if p in MALEFICS]
    if not malefics_in_5:
        return None
    if jup["strength"] != "weak" and jup["placement"] not in DUSTHANAS:
        # also weak if debilitated
        if not (jup["sign"] and _is_debilitated("Jupiter", jup["sign"])):
            return None

    factors = [
        f"5th lord ({info5['lord']}) in Dusthana (house {info5['placement']})",
        f"Malefic(s) in 5th house: {', '.join(malefics_in_5)}",
        f"Jupiter weak — house {jup['placement']}, strength {jup['strength']}",
    ]
    return {
        "key": "dattaka_yoga",
        "name_en": "Dattaka Yoga",
        "name_hi": "दत्तक योग",
        "effect_en": "Progeny through adoption. Native may not have biological children but raises an adopted child.",
        "effect_hi": "दत्तक संतान योग। जातक को सम्भवतः जैविक संतान न हो, किन्तु दत्तक पुत्र/पुत्री का पालन करता है।",
        "probability": "moderate",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 8",
        "supporting_factors": factors,
    }


def _detect_kanya_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """5th house sign + 5th lord in female signs + Venus influence → female issue only."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    fifth_sign = info5["fifth_sign"]
    lord_sign = info5["sign"]

    if not fifth_sign or not lord_sign:
        return None
    if not (_is_female_sign(fifth_sign) and _is_female_sign(lord_sign)):
        return None
    # Venus influence: Venus in 5th OR aspects 5th OR conjoins 5th lord
    venus_in_5 = "Venus" in _planets_in_house(planets, 5)
    venus_aspects_5 = _aspects_house("Venus", 5, planets)
    venus_with_lord = (
        "Venus" in planets
        and info5["lord"] in planets
        and _house_of_planet("Venus", planets) == info5["placement"]
        and info5["placement"] > 0
    )
    if not (venus_in_5 or venus_aspects_5 or venus_with_lord):
        return None

    factors = [
        f"5th house in female sign ({fifth_sign})",
        f"5th lord ({info5['lord']}) in female sign ({lord_sign})",
    ]
    if venus_in_5:
        factors.append("Venus in 5th house")
    if venus_aspects_5:
        factors.append("Venus aspects 5th house")
    if venus_with_lord:
        factors.append(f"Venus conjoins 5th lord in house {info5['placement']}")
    return {
        "key": "kanya_yoga",
        "name_en": "Kanya Yoga",
        "name_hi": "कन्या योग",
        "effect_en": "Female issue predominantly. Native is blessed primarily with daughters.",
        "effect_hi": "प्रायः कन्या संतान। जातक को मुख्यतः पुत्रियों का सुख प्राप्त होता है।",
        "probability": "moderate",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 11",
        "supporting_factors": factors,
    }


def _detect_putra_hani_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Saturn+Rahu in 5th OR 5th lord in 6/8/12 with Mars aspect → loss of children."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)

    occupants_5 = _planets_in_house(planets, 5)
    sat_rahu_in_5 = "Saturn" in occupants_5 and "Rahu" in occupants_5

    lord_in_dusthana_with_mars = False
    if info5["placement"] in DUSTHANAS and info5["lord"]:
        if _aspects_house("Mars", info5["placement"], planets):
            lord_in_dusthana_with_mars = True

    if not (sat_rahu_in_5 or lord_in_dusthana_with_mars):
        return None

    factors: List[str] = []
    if sat_rahu_in_5:
        factors.append("Saturn + Rahu conjoin in 5th house")
    if lord_in_dusthana_with_mars:
        factors.append(
            f"5th lord ({info5['lord']}) in Dusthana (house {info5['placement']}) aspected by Mars"
        )
    return {
        "key": "putra_hani_yoga",
        "name_en": "Putra-Hani Yoga",
        "name_hi": "पुत्र-हानि योग",
        "effect_en": "Loss or grief related to children. Native may experience miscarriage, infant loss, or estrangement.",
        "effect_hi": "संतान हानि या शोक। जातक को गर्भपात, शिशु-मृत्यु अथवा संतान-वियोग का कष्ट संभव है।",
        "probability": "high",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 14",
        "supporting_factors": factors,
    }


def _detect_bahu_putra_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Multiple benefics in 5th + Jupiter in Kendra + 5th lord strong → many children."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    benefics_in_5 = [p for p in _planets_in_house(planets, 5) if p in BENEFICS]
    if len(benefics_in_5) < 2:
        return None
    if jup["placement"] not in KENDRAS:
        return None
    if info5["strength"] != "strong":
        return None

    factors = [
        f"{len(benefics_in_5)} benefics in 5th house: {', '.join(benefics_in_5)}",
        f"Jupiter in Kendra (house {jup['placement']})",
        f"5th lord ({info5['lord']}) strong",
    ]
    return {
        "key": "bahu_putra_yoga",
        "name_en": "Bahu-Putra Yoga",
        "name_hi": "बहु-पुत्र योग",
        "effect_en": "Many children. Native is blessed with a large and fortunate progeny.",
        "effect_hi": "बहुसंख्यक संतान। जातक को विशाल एवं सौभाग्यशाली संतति प्राप्त होती है।",
        "probability": "high",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 17",
        "supporting_factors": factors,
    }


def _detect_jyeshta_putra_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Sun in 5th + Jupiter aspects 5th → virtuous first-born."""
    planets = chart.get("planets", {}) or {}
    if "Sun" not in _planets_in_house(planets, 5):
        return None
    if not _aspects_house("Jupiter", 5, planets):
        return None

    factors = [
        "Sun in 5th house",
        "Jupiter aspects 5th house",
    ]
    sun_sign = _sign_of_planet("Sun", planets)
    if _is_exalted("Sun", sun_sign) or _is_own_sign("Sun", sun_sign):
        factors.append(f"Sun strong in {sun_sign}")
    return {
        "key": "jyeshta_putra_yoga",
        "name_en": "Jyeshta-Putra Yoga",
        "name_hi": "ज्येष्ठ-पुत्र योग",
        "effect_en": "Virtuous and illustrious first-born. Eldest child becomes a pillar of the family.",
        "effect_hi": "ज्येष्ठ संतान का उत्कर्ष। प्रथम संतान यशस्वी एवं कुल-आधार बनती है।",
        "probability": "moderate",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 19",
        "supporting_factors": factors,
    }


def _detect_delayed_progeny_yoga(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Saturn in 5th OR 5th lord in Saturn's sign (Capricorn/Aquarius)."""
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)

    saturn_in_5 = "Saturn" in _planets_in_house(planets, 5)
    lord_in_saturn_sign = info5["sign"] in SATURN_SIGNS

    if not (saturn_in_5 or lord_in_saturn_sign):
        return None

    factors: List[str] = []
    if saturn_in_5:
        factors.append("Saturn in 5th house")
    if lord_in_saturn_sign:
        factors.append(f"5th lord ({info5['lord']}) in Saturn's sign ({info5['sign']})")
    return {
        "key": "delayed_progeny_yoga",
        "name_en": "Delayed Progeny Yoga",
        "name_hi": "विलम्बित संतान योग",
        "effect_en": "Late or difficult conception. Children come after delay, effort, or in advanced age.",
        "effect_hi": "विलम्ब से संतान की प्राप्ति। संतति विलम्ब, प्रयास अथवा अधिक आयु में होती है।",
        "probability": "moderate",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 20",
        "supporting_factors": factors,
    }


DETECTORS = (
    _detect_putra_yoga,
    _detect_aputra_yoga,
    _detect_dattaka_yoga,
    _detect_kanya_yoga,
    _detect_putra_hani_yoga,
    _detect_bahu_putra_yoga,
    _detect_jyeshta_putra_yoga,
    _detect_delayed_progeny_yoga,
)


# ───────────────────────────────────────────────────────────────
# Main analyzer
# ───────────────────────────────────────────────────────────────

def _build_fifth_house_analysis(chart: Dict[str, Any]) -> Dict[str, Any]:
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    planets_in_5 = _planets_in_house(planets, 5)
    benefics_in_5 = [p for p in planets_in_5 if p in BENEFICS]
    malefics_in_5 = [p for p in planets_in_5 if p in MALEFICS]

    # Narrative interpretation
    if info5["strength"] == "strong" and jup["strength"] == "strong" and not malefics_in_5:
        interp_en = (
            f"The 5th lord {info5['lord']} is strong in house {info5['placement']}, "
            f"and Jupiter (karaka for progeny) is well-placed in house {jup['placement']}. "
            "The 5th house is clean of malefics — a favorable progeny configuration."
        )
        interp_hi = (
            f"पंचमेश {info5['lord']} {info5['placement']}वें भाव में बलवान है, "
            f"तथा पुत्रकारक गुरु {jup['placement']}वें भाव में शुभ स्थिति में हैं। "
            "पंचम भाव पाप-ग्रहों से शुद्ध है — संतान के लिए अनुकूल योग।"
        )
    elif info5["strength"] == "weak" or jup["strength"] == "weak" or malefics_in_5:
        interp_en = (
            f"The 5th lord {info5['lord']} is in house {info5['placement']} "
            f"({info5['strength']}), Jupiter is in house {jup['placement']} ({jup['strength']}). "
            + (f"Malefics present in 5th: {', '.join(malefics_in_5)}. " if malefics_in_5 else "")
            + "Progeny matters require care and remedial support."
        )
        interp_hi = (
            f"पंचमेश {info5['lord']} {info5['placement']}वें भाव में है ({info5['strength']}), "
            f"गुरु {jup['placement']}वें भाव में हैं ({jup['strength']})। "
            + (f"पंचम में पाप-ग्रह: {', '.join(malefics_in_5)}। " if malefics_in_5 else "")
            + "संतान विषयक मामलों में सावधानी एवं उपाय आवश्यक हैं।"
        )
    else:
        interp_en = (
            f"Mixed indications. 5th lord {info5['lord']} ({info5['strength']}) in house "
            f"{info5['placement']}, Jupiter ({jup['strength']}) in house {jup['placement']}."
        )
        interp_hi = (
            f"मिश्रित संकेत। पंचमेश {info5['lord']} ({info5['strength']}) "
            f"{info5['placement']}वें भाव में, गुरु ({jup['strength']}) "
            f"{jup['placement']}वें भाव में।"
        )

    return {
        "fifth_lord": info5["lord"],
        "fifth_lord_placement": info5["placement"],
        "fifth_lord_sign": info5["sign"],
        "fifth_lord_strength": info5["strength"],
        "fifth_sign": info5["fifth_sign"],
        "jupiter_placement": jup["placement"],
        "jupiter_sign": jup["sign"],
        "jupiter_strength": jup["strength"],
        "planets_in_5th": planets_in_5,
        "benefics_in_5th": benefics_in_5,
        "malefics_in_5th": malefics_in_5,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
    }


def _assess_prospect(yogas: List[Dict[str, Any]], fifth: Dict[str, Any]) -> str:
    """favorable | challenging | mixed."""
    keys = {y["key"] for y in yogas}
    negative = {"aputra_yoga", "putra_hani_yoga", "dattaka_yoga", "delayed_progeny_yoga"}
    positive = {"putra_yoga", "bahu_putra_yoga", "jyeshta_putra_yoga"}

    has_neg = bool(keys & negative)
    has_pos = bool(keys & positive)

    if has_pos and not has_neg:
        return "favorable"
    if has_neg and not has_pos:
        return "challenging"
    if has_pos and has_neg:
        return "mixed"
    # No yogas → fall back to strength
    if fifth.get("fifth_lord_strength") == "strong" and fifth.get("jupiter_strength") == "strong":
        return "favorable"
    if fifth.get("fifth_lord_strength") == "weak" or fifth.get("jupiter_strength") == "weak":
        return "challenging"
    return "mixed"


def _recommendations(prospect: str, yogas: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    keys = {y["key"] for y in yogas}
    en: List[str] = []
    hi: List[str] = []

    if prospect == "favorable":
        en.append("Favorable progeny indications — maintain positive habits and rituals.")
        hi.append("संतान के लिए अनुकूल योग — शुभ आचरण और नियमित पूजा बनाए रखें।")
    if prospect == "challenging":
        en.append("Challenging indications — consult qualified astrologer for timing and remedies.")
        hi.append("कठिन संकेत — योग्य ज्योतिषी से समय एवं उपायों पर परामर्श लें।")
    if prospect == "mixed":
        en.append("Mixed indications — careful timing of conception is advised.")
        hi.append("मिश्रित संकेत — गर्भधारण के समय का विचार आवश्यक।")

    if "delayed_progeny_yoga" in keys:
        en.append("Do not lose patience; progeny matters may simply require time.")
        hi.append("धैर्य रखें; संतान विषय में समय लग सकता है।")
    if "kanya_yoga" in keys:
        en.append("Equal reverence for daughters as for sons is indicated.")
        hi.append("पुत्रियों को पुत्रों के समान आदर एवं स्नेह देने का योग है।")
    if "dattaka_yoga" in keys:
        en.append("Consider adoption as a legitimate spiritual path to parenthood.")
        hi.append("दत्तक ग्रहण को मातृत्व/पितृत्व का धर्म-सम्मत मार्ग मानें।")

    return {"en": en, "hi": hi}


def _remedies(prospect: str, yogas: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    keys = {y["key"] for y in yogas}
    en: List[str] = []
    hi: List[str] = []

    # Default Jupiter/5th-house remedies
    en.append("Recite Santan Gopal Mantra daily (108 times).")
    hi.append("प्रतिदिन संतान गोपाल मंत्र का 108 बार जप करें।")
    en.append("Worship Lord Krishna with yellow flowers on Thursdays.")
    hi.append("गुरुवार को भगवान श्रीकृष्ण को पीले पुष्प अर्पित करें।")
    en.append("Fast on Thursdays and feed Brahmins/cows.")
    hi.append("गुरुवार का व्रत करें तथा ब्राह्मणों एवं गायों को भोजन कराएँ।")

    if "aputra_yoga" in keys or "putra_hani_yoga" in keys:
        en.append("Perform Putrakameshti Yagna under qualified guidance.")
        hi.append("योग्य आचार्य के मार्गदर्शन में पुत्रकामेष्टि यज्ञ कराएँ।")
    if "delayed_progeny_yoga" in keys:
        en.append("Offer water to a Peepal tree daily for Saturn pacification.")
        hi.append("शनि शांति हेतु प्रतिदिन पीपल को जल अर्पित करें।")
    if "dattaka_yoga" in keys:
        en.append("Charity to orphanages and support for destitute children.")
        hi.append("अनाथालयों को दान दें तथा निराश्रित बालकों की सहायता करें।")

    return {"en": en, "hi": hi}


def _children_timing_section(
    chart_data: Dict[str, Any],
    fifth_info: Dict[str, Any],
    yogas: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Classical progeny timing: favorable dasha periods + Jupiter transit triggers.
    Source: Phaladeepika Adh. 12 (dasha rules) + Adh. 26 (Gochara principles).
    """
    asc_sign = (chart_data.get("ascendant") or {}).get("sign", "")

    fifth_lord = fifth_info.get("fifth_lord", "")
    fifth_sign = fifth_info.get("fifth_sign", "")          # 5th house sign
    fifth_lord_natal_sign = fifth_info.get("sign", "")     # where 5th lord sits natally

    ninth_sign = _house_sign(9, asc_sign)
    ninth_lord = SIGN_LORD.get(ninth_sign, "")

    yoga_keys = {y["key"] for y in yogas}
    delayed = "delayed_progeny_yoga" in yoga_keys

    # ── Favorable dasha planets ──────────────────────────────────────────────
    dasha_planets: List[Dict[str, Any]] = []

    # Jupiter — primary karaka for progeny
    dasha_planets.append({
        "planet": "Jupiter",
        "role_en": "Putra Karaka — natural significator of progeny",
        "role_hi": "पुत्र कारक — संतान का नैसर्गिक कारक",
        "favorable": True,
        "reason_en": (
            "Jupiter's Mahadasha or Antardasha is the most auspicious period for children "
            "per Phaladeepika Adh. 12. Even within an otherwise unfavorable Mahadasha, "
            "Jupiter's Antardasha can open a reliable progeny window."
        ),
        "reason_hi": (
            "फलदीपिका अध्याय 12 के अनुसार गुरु की महादशा अथवा अंतर्दशा संतान-प्राप्ति के "
            "लिए सर्वाधिक शुभ काल है। प्रतिकूल महादशा में भी गुरु का अंतर एक शुभ "
            "संतान-खिड़की खोल सकता है।"
        ),
    })

    # 5th lord — Putra Bhava lord
    if fifth_lord and fifth_lord != "Jupiter":
        lord_strength = fifth_info.get("fifth_lord_strength", "moderate")
        favorable = lord_strength != "weak"
        weak_note_en = f" (Note: {fifth_lord} is currently weak — this window benefits from remedies.)" if not favorable else ""
        dasha_planets.append({
            "planet": fifth_lord,
            "role_en": "5th lord — Putra Bhava lord",
            "role_hi": "पंचमेश — पुत्र भाव का स्वामी",
            "favorable": favorable,
            "reason_en": (
                f"{fifth_lord} rules the 5th house (Putra Bhava). Its Mahadasha or Antardasha — "
                f"particularly when Jupiter simultaneously transits the 5th or 9th sign — "
                f"brings progeny events to fruition.{weak_note_en}"
            ),
            "reason_hi": (
                f"{fifth_lord} पंचम भाव (पुत्र भाव) का स्वामी है। इसकी महादशा अथवा अंतर्दशा में — "
                "विशेषतः जब गुरु एक साथ पंचम या नवम राशि में गोचर करे — संतान-प्राप्ति सिद्ध होती है।"
            ),
        })

    # 9th lord — trikona, purva-punya axis
    if ninth_lord and ninth_lord not in ("Jupiter", fifth_lord):
        dasha_planets.append({
            "planet": ninth_lord,
            "role_en": "9th lord — Trikona (Purva Punya)",
            "role_hi": "नवमेश — त्रिकोण (पूर्व पुण्य)",
            "favorable": True,
            "reason_en": (
                f"{ninth_lord} lords the 9th (trikona to 5th). Its Antardasha within Jupiter's "
                "or 5th-lord's Mahadasha creates a double-trikona activation — classically "
                "very auspicious for the manifestation of progeny."
            ),
            "reason_hi": (
                f"{ninth_lord} नवम (पंचम से त्रिकोण) का स्वामी है। गुरु या पंचमेश की महादशा "
                "में इसका अंतर द्विगुण-त्रिकोण सक्रियता बनाता है — शास्त्र-सम्मत अत्यंत शुभ संयोग।"
            ),
        })

    # Saturn — flag as delaying factor when delayed_progeny_yoga present
    if delayed:
        dasha_planets.append({
            "planet": "Saturn",
            "role_en": "Saturn — Delaying factor",
            "role_hi": "शनि — विलम्ब कारक",
            "favorable": False,
            "reason_en": (
                "Saturn's Mahadasha or prominent Antardasha tends to delay progeny. "
                "Children are more likely after age 32–36, or in Saturn's Antar within "
                "a favorable Mahadasha once karmic dues are cleared."
            ),
            "reason_hi": (
                "शनि की महादशा या प्रमुख अंतर्दशा में संतान-प्राप्ति में विलम्ब होता है। "
                "32-36 वर्ष की आयु के पश्चात, शुभ महादशा में शनि के अंतर में, "
                "जब कर्म-ऋण पूर्ण हो, संतान संभव है।"
            ),
        })

    # ── Jupiter transit triggers ─────────────────────────────────────────────
    triggers: List[Dict[str, Any]] = []

    if fifth_sign:
        triggers.append({
            "planet": "Jupiter",
            "watch_sign": fifth_sign,
            "house_ref": 5,
            "trigger_en": f"Jupiter transiting {fifth_sign} (natal 5th house sign)",
            "trigger_hi": f"गुरु का {fifth_sign} में गोचर (जन्मकालीन पंचम भाव)",
            "significance_en": (
                f"Jupiter directly activates the Putra Bhava ({fifth_sign}) — "
                "the single most reliable transit indicator for progeny. "
                "Most effective when concurrent dasha is Jupiter or the 5th lord."
            ),
            "significance_hi": (
                f"गुरु सीधे पुत्र भाव ({fifth_sign}) को सक्रिय करता है — "
                "संतान का सर्वाधिक विश्वसनीय गोचर-संकेत। "
                "जब समवर्ती दशा गुरु या पंचमेश की हो तब सर्वाधिक प्रभावी।"
            ),
        })

    if fifth_lord_natal_sign and fifth_lord_natal_sign != fifth_sign:
        triggers.append({
            "planet": "Jupiter",
            "watch_sign": fifth_lord_natal_sign,
            "house_ref": None,
            "trigger_en": f"Jupiter transiting {fifth_lord_natal_sign} (natal sign of {fifth_lord}, 5th lord)",
            "trigger_hi": f"गुरु का {fifth_lord_natal_sign} में गोचर (पंचमेश {fifth_lord} की जन्मकालीन राशि)",
            "significance_en": (
                f"Jupiter conjoining the natal 5th lord ({fifth_lord}) by transit "
                "energises the progeny significator and can trigger conception events."
            ),
            "significance_hi": (
                f"गुरु का जन्मकालीन पंचमेश {fifth_lord} पर गोचर पुत्र-कारक को "
                "ऊर्जान्वित करता है और गर्भधारण की संभावना को जागृत करता है।"
            ),
        })

    if ninth_sign and ninth_sign not in (fifth_sign, fifth_lord_natal_sign):
        triggers.append({
            "planet": "Jupiter",
            "watch_sign": ninth_sign,
            "house_ref": 9,
            "trigger_en": f"Jupiter transiting {ninth_sign} (9th house — trikona to 5th)",
            "trigger_hi": f"गुरु का {ninth_sign} में गोचर (नवम भाव — पंचम का त्रिकोण)",
            "significance_en": (
                "9th house is trine to the 5th. Jupiter here activates the purva-punya "
                "axis, which classically supports the manifestation of progeny."
            ),
            "significance_hi": (
                "नवम भाव पंचम का त्रिकोण है। यहाँ गुरु का गोचर पूर्व-पुण्य अक्ष को "
                "जागृत करता है — शास्त्रीय रूप से संतान-योग को बल देने वाला।"
            ),
        })

    # ── Summary ──────────────────────────────────────────────────────────────
    if delayed:
        summary_en = (
            "Saturn's influence on the 5th house suggests children may arrive after age 32–36, "
            "or during a favorable Antardasha within Jupiter's or 5th-lord's Mahadasha. "
            "Remedies (Santan Gopal mantra, Putrakameshti Yagna) and patience are key."
        )
        summary_hi = (
            "पंचम भाव पर शनि के प्रभाव से संतान 32-36 वर्ष की आयु के पश्चात अथवा गुरु / "
            "पंचमेश की महादशा में शुभ अंतर में आ सकती है। "
            "उपाय (संतान गोपाल मंत्र, पुत्रकामेष्टि यज्ञ) एवं धैर्य आवश्यक हैं।"
        )
    elif "putra_yoga" in yoga_keys or "bahu_putra_yoga" in yoga_keys:
        summary_en = (
            "Strong progeny yoga present. The optimal window for children is when Jupiter "
            "transits your 5th house sign AND the concurrent dasha belongs to Jupiter or "
            "the 5th lord. Both conditions together are the most reliable classical timing."
        )
        summary_hi = (
            "बलवान पुत्र-योग विद्यमान। संतान-प्राप्ति का सर्वश्रेष्ठ काल वह है जब "
            "गुरु पंचम राशि में गोचर करे और समवर्ती दशा गुरु अथवा पंचमेश की हो — "
            "दोनों संयोगों का मेल सर्वाधिक विश्वसनीय शास्त्रीय काल-खिड़की है।"
        )
    else:
        summary_en = (
            "Watch for periods when Jupiter transits your 5th house sign and the concurrent "
            "Mahadasha or Antardasha belongs to Jupiter or the 5th lord. "
            "The overlap of both conditions is the classical timing window for progeny."
        )
        summary_hi = (
            "वह काल देखें जब गुरु पंचम राशि में गोचर करे और समवर्ती महादशा "
            "या अंतर्दशा गुरु अथवा पंचमेश की हो। "
            "दोनों संयोगों का मेल शास्त्रीय संतान-काल-खिड़की है।"
        )

    return {
        "favorable_dasha_planets": dasha_planets,
        "transit_triggers": triggers,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 12 + Adh. 26 (Gochara)",
    }


def analyze_apatya(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apatyadhyaya — classical progeny analysis per Phaladeepika Adhyaya 12.

    Args:
        chart_data: {
            'planets': {'Jupiter': {'sign': 'Cancer', 'house': 5, 'longitude': 100}, ...},
            'ascendant': {'sign': 'Pisces', 'longitude': 330},
            ...
        }

    Returns:
        {
          'fifth_house_analysis': {...},
          'yogas_detected': [ {key, name_en, name_hi, effect_en, effect_hi,
                               probability, sloka_ref, supporting_factors}, ... ],
          'progeny_prospect': 'favorable' | 'challenging' | 'mixed',
          'recommendations_en': [...], 'recommendations_hi': [...],
          'remedies_en': [...], 'remedies_hi': [...],
          'sloka_ref': 'Phaladeepika Adh. 12',
        }
    """
    if not isinstance(chart_data, dict):
        chart_data = {}

    fifth = _build_fifth_house_analysis(chart_data)

    yogas: List[Dict[str, Any]] = []
    for det in DETECTORS:
        try:
            y = det(chart_data)
        except Exception:
            y = None
        if y:
            yogas.append(y)

    prospect = _assess_prospect(yogas, fifth)
    recs = _recommendations(prospect, yogas)
    rems = _remedies(prospect, yogas)
    timing = _children_timing_section(chart_data, fifth, yogas)

    return {
        "fifth_house_analysis": fifth,
        "yogas_detected": yogas,
        "progeny_prospect": prospect,
        "children_timing": timing,
        "recommendations_en": recs["en"],
        "recommendations_hi": recs["hi"],
        "remedies_en": rems["en"],
        "remedies_hi": rems["hi"],
        "sloka_ref": "Phaladeepika Adh. 12",
    }
