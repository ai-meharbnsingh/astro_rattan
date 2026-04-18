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

# Natural (permanent) planetary friendships — used for Sloka 13 child-count
_NAT_FRIENDS: Dict[str, set] = {
    "Sun":     {"Moon", "Mars", "Jupiter"},
    "Moon":    {"Sun", "Mercury"},
    "Mars":    {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus":   {"Mercury", "Saturn"},
    "Saturn":  {"Mercury", "Venus"},
    "Rahu":    {"Venus", "Saturn", "Mercury"},
    "Ketu":    {"Mars", "Jupiter"},
}
_NAT_ENEMIES: Dict[str, set] = {
    "Sun":     {"Venus", "Saturn"},
    "Moon":    set(),
    "Mars":    {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus":   {"Sun", "Moon"},
    "Saturn":  {"Sun", "Moon", "Mars"},
    "Rahu":    {"Sun", "Moon"},
    "Ketu":    {"Venus", "Saturn"},
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


def _sloka13_weight(planet: str, sign: str) -> tuple:
    """
    Per Phaladeepika Adh. 12 Sloka 13: planet's contribution to child count
    based on its relationship with the sign it occupies.
    Returns (weight: float, label: str).
    Friendly/own/exalted=1.0, neutral=0.5, inimical=0.25, debilitated=0.0.
    """
    if not planet or not sign:
        return 0.5, "neutral"
    if _is_own_sign(planet, sign) or _is_exalted(planet, sign):
        return 1.0, "own/exalted"
    if _is_debilitated(planet, sign):
        return 0.0, "debilitated"
    sign_lord = SIGN_LORD.get(sign, "")
    if not sign_lord or sign_lord == planet:
        return 1.0, "own"
    if sign_lord in _NAT_FRIENDS.get(planet, set()):
        return 0.75, "friendly"
    if sign_lord in _NAT_ENEMIES.get(planet, set()):
        return 0.25, "inimical"
    return 0.5, "neutral"


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

    # Severity balancer: benefic presence in 5th mitigates the yoga
    benefics_in_5 = [p for p in occupants_5 if p in BENEFICS]

    factors: List[str] = []
    if sat_rahu_in_5:
        factors.append("Saturn + Rahu conjoin in 5th house")
    if lord_in_dusthana_with_mars:
        factors.append(
            f"5th lord ({info5['lord']}) in Dusthana (house {info5['placement']}) aspected by Mars"
        )

    if benefics_in_5:
        probability = "moderate"
        mitigation = f" Partially mitigated by benefic(s) in 5th house: {', '.join(benefics_in_5)}."
        factors.append(f"Benefic mitigation — {', '.join(benefics_in_5)} in 5th reduces severity")
        effect_en = f"Elevated risk of grief or difficulty related to children.{mitigation} Remedies advised."
        effect_hi = f"संतान विषयक पीड़ा या विलम्ब का उन्नत खतरा।{' शुभ-ग्रहों की उपस्थिति कुछ शमन करती है।'} उपाय उपयोगी।"
    else:
        probability = "high"
        effect_en = "Loss or grief related to children. Native may experience miscarriage, infant loss, or estrangement."
        effect_hi = "संतान हानि या शोक। जातक को गर्भपात, शिशु-मृत्यु अथवा संतान-वियोग का कष्ट संभव है।"

    return {
        "key": "putra_hani_yoga",
        "name_en": "Putra-Hani Yoga",
        "name_hi": "पुत्र-हानि योग",
        "effect_en": effect_en,
        "effect_hi": effect_hi,
        "probability": probability,
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
# Sprint F — 6 advanced children analysis features (Adh. 12)
# ───────────────────────────────────────────────────────────────

def _detect_adoption_indicators(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 1: Adopted Children Yogas (Phaladeepika Adh. 12).

    Conditions:
      A) 5th lord in 12th house WITH Jupiter in Dusthana → possibility of adoption
      B) Rahu in 5th AND Jupiter is weak (debilitated or enemy sign) → likely to adopt
      C) Sun in 5th WITH Saturn aspect AND no benefic aspect on 5th → biological difficult, adoption indicated

    Returns adoption_indicators: {indicated, strength, reasons, sloka_ref}
    """
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    jup = _jupiter_info(chart)

    reasons: List[Dict[str, str]] = []
    strength_score = 0

    # Condition A: 5th lord in 12th + Jupiter in dusthana
    if info5["placement"] == 12 and jup["placement"] in DUSTHANAS:
        reasons.append({
            "reason_en": f"5th lord ({info5['lord']}) placed in the 12th house (house of loss/liberation) while Jupiter is in a Dusthana (house {jup['placement']}) — classical adoption indicator.",
            "reason_hi": f"पंचमेश ({info5['lord']}) द्वादश भाव (व्यय/मोक्ष भाव) में स्थित है और गुरु दुःस्थान (भाव {jup['placement']}) में हैं — दत्तक संतान का शास्त्रीय संकेत।",
        })
        strength_score += 2

    # Condition B: Rahu in 5th + Jupiter weak/debilitated
    occupants_5 = _planets_in_house(planets, 5)
    jup_weak = (
        jup["strength"] == "weak"
        or (jup["sign"] and _is_debilitated("Jupiter", jup["sign"]))
    )
    if "Rahu" in occupants_5 and jup_weak:
        reasons.append({
            "reason_en": f"Rahu occupies the 5th house and Jupiter is weak/debilitated (house {jup['placement']}, {jup['sign']}) — strongly suggests adoption yoga.",
            "reason_hi": f"राहु पंचम भाव में स्थित है और गुरु दुर्बल/नीच हैं (भाव {jup['placement']}, {jup['sign']}) — दत्तक ग्रहण का प्रबल संकेत।",
        })
        strength_score += 2

    # Condition C: Sun in 5th + Saturn aspects 5th + no benefic aspect on 5th
    sun_in_5 = "Sun" in occupants_5
    sat_aspects_5 = _aspects_house("Saturn", 5, planets)
    benefic_aspect_on_5 = any(_aspects_house(b, 5, planets) for b in BENEFICS if b in planets)
    if sun_in_5 and sat_aspects_5 and not benefic_aspect_on_5:
        reasons.append({
            "reason_en": "Sun in 5th house is aspected by Saturn with no benefic aspect on the 5th — biological progeny faces obstacles; adoption indicated.",
            "reason_hi": "सूर्य पंचम भाव में है, शनि की दृष्टि पड़ रही है और कोई शुभ-ग्रह दृष्टि नहीं — जैविक संतान में बाधा; दत्तक ग्रहण संभव।",
        })
        strength_score += 1

    indicated = len(reasons) > 0
    if strength_score >= 3:
        strength = "strong"
    elif strength_score >= 1:
        strength = "moderate"
    else:
        strength = "none"

    return {
        "indicated": indicated,
        "strength": strength,
        "reasons": reasons,
        "sloka_ref": "Phaladeepika Adh. 12 sloka 8–10",
    }


def _detect_female_child_yogas(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 2: Female-Only Children Yogas (Phaladeepika Adh. 12).

    Conditions:
      A) Moon in 5th (especially in even/female signs)
      B) Venus as 5th lord in female (even) sign
      C) 5th house in even sign + occupied/aspected by female planets (Moon/Venus)

    Returns female_child_yogas: {indicated, reasons, sloka_ref}
    """
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)

    reasons: List[Dict[str, str]] = []
    occupants_5 = _planets_in_house(planets, 5)
    fifth_sign = info5["fifth_sign"]
    fifth_is_female = _is_female_sign(fifth_sign)

    # Saturn-ruled female signs give mixed rather than strong female indication
    SATURN_RULED_FEMALE_SIGNS = {"Capricorn"}  # Capricorn is even/female but Saturn-ruled

    # Condition A: Moon in 5th
    if "Moon" in occupants_5:
        moon_sign = _sign_of_planet("Moon", planets)
        if moon_sign in FEMALE_SIGNS:
            if moon_sign in SATURN_RULED_FEMALE_SIGNS:
                # Saturn-ruled sign moderates the female indication
                reasons.append({
                    "reason_en": (
                        f"Moon in 5th house in {moon_sign} (female/even sign but Saturn-ruled) — "
                        f"slight female tendency; mixed children likely."
                    ),
                    "reason_hi": (
                        f"चन्द्रमा पंचम भाव में {moon_sign} (स्त्री/सम राशि किन्तु शनि-शासित) — "
                        f"हल्का कन्या-संकेत; मिश्रित संतान की सम्भावना।"
                    ),
                })
            else:
                reasons.append({
                    "reason_en": f"Moon in 5th house in the female sign {moon_sign} — favours female children.",
                    "reason_hi": f"चन्द्रमा पंचम भाव में स्त्री राशि {moon_sign} में — कन्या संतान का योग।",
                })
        else:
            reasons.append({
                "reason_en": f"Moon in 5th house (in {moon_sign}) — inclines toward female children.",
                "reason_hi": f"चन्द्रमा पंचम भाव में ({moon_sign} राशि में) — कन्या संतान का संकेत।",
            })

    # Condition B: Venus as 5th lord in female sign
    if info5["lord"] == "Venus" and info5["sign"] in FEMALE_SIGNS:
        reasons.append({
            "reason_en": f"Venus is the 5th lord placed in female sign {info5['sign']} — female children predominate.",
            "reason_hi": f"शुक्र पंचमेश है और स्त्री राशि {info5['sign']} में स्थित है — कन्या संतान की प्रधानता।",
        })

    # Condition C: 5th sign female + female planets in or aspecting 5th
    if fifth_is_female:
        female_in_5 = [p for p in occupants_5 if p in {"Moon", "Venus"}]
        female_aspect_5 = [p for p in {"Moon", "Venus"} if p in planets and _aspects_house(p, 5, planets)]
        if female_in_5 or female_aspect_5:
            active = female_in_5 + female_aspect_5
            reasons.append({
                "reason_en": f"5th house is a female sign ({fifth_sign}) and is occupied/aspected by female planets ({', '.join(active)}) — predominantly female progeny.",
                "reason_hi": f"पंचम भाव स्त्री राशि ({fifth_sign}) में है और स्त्री ग्रहों ({', '.join(active)}) से युक्त/दृष्ट है — कन्या संतान की अधिकता।",
            })

    return {
        "indicated": len(reasons) > 0,
        "reasons": reasons,
        "sloka_ref": "Phaladeepika Adh. 12 sloka 11–12",
    }


def _detect_male_child_yogas(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 3: All-Male Children Yogas (Phaladeepika Adh. 12).

    Conditions:
      A) 5th lord in odd sign + aspected by Jupiter → male children
      B) Sun in 5th with Mars aspect → male children
      C) Jupiter in 5th in odd sign → predominantly male

    Returns male_child_yogas: {indicated, reasons, sloka_ref}
    """
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    occupants_5 = _planets_in_house(planets, 5)

    reasons: List[Dict[str, str]] = []

    # Condition A: 5th lord in odd (male) sign + Jupiter aspects 5th lord house
    if info5["sign"] in MALE_SIGNS:
        lord_house = info5["placement"]
        jup_aspects_lord = lord_house > 0 and _aspects_house("Jupiter", lord_house, planets)
        if jup_aspects_lord:
            reasons.append({
                "reason_en": f"5th lord ({info5['lord']}) in male sign ({info5['sign']}) and aspected by Jupiter — strong indicator of male children.",
                "reason_hi": f"पंचमेश ({info5['lord']}) पुरुष राशि ({info5['sign']}) में है और गुरु की दृष्टि से युक्त है — पुत्र संतान का प्रबल संकेत।",
            })
        else:
            reasons.append({
                "reason_en": f"5th lord ({info5['lord']}) in male sign ({info5['sign']}) — inclines toward male children.",
                "reason_hi": f"पंचमेश ({info5['lord']}) पुरुष राशि ({info5['sign']}) में — पुत्र संतान का संकेत।",
            })

    # Condition B: Sun in 5th + Mars aspects 5th
    if "Sun" in occupants_5 and _aspects_house("Mars", 5, planets):
        reasons.append({
            "reason_en": "Sun in 5th house with Mars aspect — classical yoga for male children.",
            "reason_hi": "सूर्य पंचम भाव में और मंगल की दृष्टि — पुत्र संतान का शास्त्रीय योग।",
        })

    # Condition C: Jupiter in 5th in odd sign
    if "Jupiter" in occupants_5:
        jup_sign = _sign_of_planet("Jupiter", planets)
        if jup_sign in MALE_SIGNS:
            reasons.append({
                "reason_en": f"Jupiter in 5th house in male sign ({jup_sign}) — predominantly male progeny indicated.",
                "reason_hi": f"गुरु पंचम भाव में पुरुष राशि ({jup_sign}) में — पुत्र संतान की प्रधानता।",
            })
        else:
            reasons.append({
                "reason_en": f"Jupiter in 5th house (in {jup_sign}) — karaka for progeny strongly placed, children blessed.",
                "reason_hi": f"गुरु पंचम भाव में ({jup_sign} राशि में) — संतान कारक बलवान, संतान-सुख प्राप्त।",
            })

    return {
        "indicated": len(reasons) > 0,
        "reasons": reasons,
        "sloka_ref": "Phaladeepika Adh. 12 sloka 9–10",
    }


def _get_conception_timing(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 4: Conception Timing Indicators (Phaladeepika Adh. 12 + Gochara).

    Favorable periods:
      - Jupiter transiting 1st, 4th, 5th, 7th, or 9th from natal Moon
      - Jupiter dasha or 5th lord dasha = peak conception window
      - Key Jupiter transit signs to watch

    Returns conception_timing: {favorable_windows, current_favorable, note_en, note_hi, sloka_ref}
    """
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")

    moon_sign = _sign_of_planet("Moon", planets)
    fifth_lord = info5.get("lord", "")
    fifth_sign = info5.get("fifth_sign", "")

    favorable_windows: List[Dict[str, str]] = []

    # Jupiter favorable transit houses from natal Moon: 1, 4, 5, 7, 9
    FAVORABLE_FROM_MOON = [1, 4, 5, 7, 9]
    if moon_sign and moon_sign in ZODIAC:
        moon_idx = ZODIAC.index(moon_sign)
        for offset in FAVORABLE_FROM_MOON:
            watch_sign = ZODIAC[(moon_idx + offset - 1) % 12]
            house_label = {1: "1st (Lagna from Moon)", 4: "4th", 5: "5th (Putra from Moon)", 7: "7th", 9: "9th (Dharma)"}[offset]
            favorable_windows.append({
                "period_en": f"When Jupiter transits {watch_sign} ({house_label} from natal Moon in {moon_sign})",
                "period_hi": f"जब गुरु {watch_sign} में गोचर करे (जन्मकालीन चन्द्र राशि {moon_sign} से {offset}वाँ भाव)",
                "jupiter_position": watch_sign,
                "type": "transit",
            })

    # Jupiter dasha / 5th lord dasha windows
    if fifth_lord:
        favorable_windows.append({
            "period_en": f"Jupiter Mahadasha or Antardasha (primary karaka for progeny)",
            "period_hi": "गुरु की महादशा अथवा अंतर्दशा (संतान का प्राथमिक कारक)",
            "jupiter_position": "Mahadasha/Antardasha",
            "type": "dasha",
        })
        favorable_windows.append({
            "period_en": f"{fifth_lord} Mahadasha or Antardasha (5th lord — Putra Bhava ruler)",
            "period_hi": f"{fifth_lord} की महादशा अथवा अंतर्दशा (पंचमेश — पुत्र भाव स्वामी)",
            "jupiter_position": f"{fifth_lord} period",
            "type": "dasha",
        })

    # Also note the most critical transit: Jupiter over 5th house sign
    if fifth_sign and fifth_sign in ZODIAC:
        favorable_windows.insert(0, {
            "period_en": f"Jupiter transiting {fifth_sign} (natal 5th house — Putra Bhava) — MOST FAVORABLE",
            "period_hi": f"गुरु का {fifth_sign} में गोचर (जन्मकालीन पंचम भाव) — सर्वाधिक अनुकूल",
            "jupiter_position": fifth_sign,
            "type": "transit",
        })

    return {
        "favorable_windows": favorable_windows,
        "current_favorable": False,  # Requires live transit data — not available in static chart
        "note_en": (
            "Conception is most likely when Jupiter transits the 5th house sign from the ascendant "
            "AND the concurrent dasha belongs to Jupiter or the 5th lord. "
            "Favorable Jupiter transits from the natal Moon (1st, 4th, 5th, 7th, 9th) further strengthen the window."
        ),
        "note_hi": (
            "गर्भधारण की सर्वाधिक संभावना तब होती है जब गुरु लग्न के पंचम भाव की राशि में गोचर करे "
            "और समवर्ती दशा गुरु या पंचमेश की हो। "
            "जन्मकालीन चन्द्र राशि से गुरु का 1, 4, 5, 7 या 9वें भाव में गोचर भी इस खिड़की को प्रबल बनाता है।"
        ),
        "sloka_ref": "Phaladeepika Adh. 12 + Adh. 26 (Gochara)",
    }


def _get_delivery_indicators() -> Dict[str, Any]:
    """
    Feature 5: Delivery Date Estimation (classical method).

    Classical Vedic method: count from 5th house sign.
    General estimate from conception month.
    Returns delivery_indicators with method description.
    """
    return {
        "method_en": (
            "Classical Vedic texts estimate delivery by counting from the sign of conception. "
            "The 5th house sign and its lord indicate the gestational sign-count. "
            "Standard Ayurvedic + astrological consensus: full-term delivery occurs in the "
            "9th or 10th month from conception (Garbha period: Phaladeepika Adh. 12)."
        ),
        "method_hi": (
            "शास्त्रीय वैदिक ग्रंथों में गर्भाधान राशि से गणना करके प्रसव का अनुमान लगाया जाता है। "
            "पंचम भाव की राशि एवं उसका स्वामी गर्भावधि के राशि-गणना का संकेत देते हैं। "
            "आयुर्वेद एवं ज्योतिष की सम्मिलित मान्यता: पूर्ण-प्रसव गर्भाधान के 9वें अथवा 10वें मास में होता है।"
        ),
        "estimated_months_range": "9-10",
        "note_en": (
            "This is a general classical estimate based on Phaladeepika tradition. "
            "The 5th house lord's strength and sign influence the exact timing within this range. "
            "A strong 5th lord in a fixed sign suggests closer to 10 months; a movable sign nearer to 9. "
            "Always consult a qualified physician for medical guidance."
        ),
        "note_hi": (
            "यह फलदीपिका परम्परा पर आधारित एक सामान्य शास्त्रीय अनुमान है। "
            "पंचमेश की बल एवं राशि इस सीमा के भीतर सटीक समय को प्रभावित करती है। "
            "स्थिर राशि में बलवान पंचमेश 10 माह के निकट और चर राशि में 9 माह के निकट संकेत देता है। "
            "चिकित्सा मार्गदर्शन के लिए सदैव योग्य चिकित्सक से परामर्श लें।"
        ),
        "sloka_ref": "Phaladeepika Adh. 12 (Garbha Adhyaya) + Ayurvedic Garbha-Sharira",
    }


def _detect_child_loss_yogas_complete(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 6: Complete Child Loss Yogas (upgrade from partial Putra-Hani Yoga).

    Conditions with severity levels:
      A) 5th lord debilitated in 8th or 12th → child loss risk (HIGH)
      B) Mars in 5th + Saturn aspect → surgical delivery risk, child risk (HIGH)
      C) Rahu in 5th + no benefic aspect → child loss yoga (MODERATE-HIGH)
      D) 5th lord in dusthana aspected by Mars → loss/grief (existing, MODERATE)
      E) Saturn + Rahu both in 5th → combined affliction (HIGH)

    Returns child_loss_yogas: {present, overall_risk, yogas, sloka_ref}
    """
    planets = chart.get("planets", {}) or {}
    info5 = _fifth_lord_info(chart)
    occupants_5 = _planets_in_house(planets, 5)

    yogas: List[Dict[str, str]] = []

    # A) 5th lord debilitated in 8th or 12th
    if (info5["lord"] and info5["placement"] in {8, 12}
            and info5["sign"] and _is_debilitated(info5["lord"], info5["sign"])):
        yogas.append({
            "key": "lord_debilitated_in_dusthana",
            "name_en": "5th Lord Debilitated in 8th/12th",
            "name_hi": "पंचमेश की नीच स्थिति 8/12 में",
            "description_en": f"5th lord {info5['lord']} is debilitated in {info5['sign']} placed in house {info5['placement']} — serious child loss risk per Phaladeepika.",
            "description_hi": f"पंचमेश {info5['lord']} नीच स्थिति में {info5['sign']} में, भाव {info5['placement']} में — फलदीपिका अनुसार संतान-हानि का गंभीर खतरा।",
            "severity": "high",
        })

    # B) Mars in 5th + Saturn aspects 5th
    if "Mars" in occupants_5 and _aspects_house("Saturn", 5, planets):
        yogas.append({
            "key": "mars_5th_saturn_aspect",
            "name_en": "Mars in 5th with Saturn Aspect",
            "name_hi": "पंचम में मंगल, शनि की दृष्टि",
            "description_en": "Mars in 5th house with Saturn's aspect — indicates risk of surgical delivery complications or child loss.",
            "description_hi": "पंचम भाव में मंगल और शनि की दृष्टि — शल्य-प्रसव संबंधी जटिलता या संतान-हानि का खतरा।",
            "severity": "high",
        })

    # C) Rahu in 5th + no benefic protection (aspect OR presence)
    # Skip if Saturn also in 5th — condition E handles the combined Saturn+Rahu yoga
    benefic_in_5 = any(p in BENEFICS for p in occupants_5)
    benefic_aspect_on_5 = any(_aspects_house(b, 5, planets) for b in BENEFICS if b in planets)
    benefic_protected = benefic_in_5 or benefic_aspect_on_5
    sat_also_in_5 = "Saturn" in occupants_5
    if "Rahu" in occupants_5 and not sat_also_in_5:
        if benefic_protected:
            benefics_present = [p for p in occupants_5 if p in BENEFICS]
            benefics_aspecting = [b for b in BENEFICS if b in planets and b not in occupants_5 and _aspects_house(b, 5, planets)]
            all_benefics = benefics_present + benefics_aspecting
            yogas.append({
                "key": "rahu_5th_mitigated",
                "name_en": "Rahu in 5th (Mitigated by Benefic)",
                "name_hi": "पंचम में राहु (शुभ-ग्रह से शमन)",
                "description_en": (
                    f"Rahu in 5th house — child grief possible, but benefic(s) "
                    f"{', '.join(all_benefics)} {'in the same house' if benefics_present else 'aspecting the 5th'} "
                    f"reduce severity. Care and remedies advised."
                ),
                "description_hi": (
                    f"राहु पंचम भाव में — संतान-पीड़ा संभव, किन्तु शुभ-ग्रह "
                    f"{', '.join(all_benefics)} की उपस्थिति/दृष्टि गंभीरता घटाती है। सावधानी एवं उपाय।"
                ),
                "severity": "moderate",
            })
        else:
            yogas.append({
                "key": "rahu_5th_no_benefic",
                "name_en": "Rahu in 5th — No Benefic Protection",
                "name_hi": "पंचम में राहु, शुभ-ग्रह का अभाव",
                "description_en": "Rahu in 5th house with no benefic present or aspecting — child loss yoga. Remedies strongly advised.",
                "description_hi": "राहु पंचम भाव में, कोई शुभ-ग्रह न स्थित न दृष्ट — संतान-हानि योग। उपाय अत्यावश्यक।",
                "severity": "moderate_high",
            })

    # D) 5th lord in dusthana aspected by Mars
    if info5["placement"] in DUSTHANAS and info5["lord"] and _aspects_house("Mars", info5["placement"], planets):
        yogas.append({
            "key": "lord_dusthana_mars_aspect",
            "name_en": "5th Lord in Dusthana with Mars Aspect",
            "name_hi": "पंचमेश दुःस्थान में, मंगल की दृष्टि",
            "description_en": f"5th lord ({info5['lord']}) in Dusthana (house {info5['placement']}) with Mars aspect — grief or loss related to children.",
            "description_hi": f"पंचमेश ({info5['lord']}) दुःस्थान (भाव {info5['placement']}) में, मंगल की दृष्टि — संतान संबंधी पीड़ा या हानि।",
            "severity": "moderate",
        })

    # E) Saturn + Rahu both in 5th (combined affliction)
    # benefic_in_5 already computed in condition C above
    if "Saturn" in occupants_5 and "Rahu" in occupants_5:
        if benefic_in_5:
            benefics_present = [p for p in occupants_5 if p in BENEFICS]
            yogas.append({
                "key": "saturn_rahu_5th",
                "name_en": "Saturn + Rahu in 5th (Partially Mitigated)",
                "name_hi": "पंचम में शनि + राहु (आंशिक शमन)",
                "description_en": (
                    f"Saturn and Rahu together in 5th house — Putra-Hani yoga present. "
                    f"Elevated risk, partially mitigated by benefic(s) {', '.join(benefics_present)} "
                    f"in the same house. Remedies advised."
                ),
                "description_hi": (
                    f"शनि और राहु दोनों पंचम भाव में — पुत्र-हानि योग। "
                    f"उन्नत खतरा, किन्तु शुभ-ग्रह {', '.join(benefics_present)} की उपस्थिति से "
                    f"आंशिक शमन। उपाय उपयोगी।"
                ),
                "severity": "moderate",
            })
        else:
            yogas.append({
                "key": "saturn_rahu_5th",
                "name_en": "Saturn + Rahu in 5th (Combined Affliction)",
                "name_hi": "पंचम में शनि + राहु (संयुक्त पीड़ा)",
                "description_en": "Saturn and Rahu together in the 5th house — Putra-Hani yoga. Severe affliction of the 5th house. Remedies essential.",
                "description_hi": "शनि और राहु दोनों पंचम भाव में — पुत्र-हानि योग। पंचम भाव की गंभीर पीड़ा। उपाय अनिवार्य।",
                "severity": "high",
            })

    # Overall risk assessment
    high_count = sum(1 for y in yogas if y.get("severity") == "high")
    mod_high_count = sum(1 for y in yogas if y.get("severity") == "moderate_high")

    if high_count >= 2:
        overall_risk = "very_high"
    elif high_count == 1 or (high_count == 0 and mod_high_count >= 1):
        overall_risk = "high"
    elif yogas:
        overall_risk = "moderate"
    else:
        overall_risk = "none"

    return {
        "present": len(yogas) > 0,
        "overall_risk": overall_risk,
        "yogas": yogas,
        "note_en": "Presence of child loss yogas indicates risk, not certainty. Remedial measures (Putrakameshti Yagna, Santan Gopal mantra, Rahu pacification) can mitigate these yogas." if yogas else "",
        "note_hi": "संतान-हानि योगों की उपस्थिति खतरे का संकेत है, निश्चितता नहीं। पुत्रकामेष्टि यज्ञ, संतान गोपाल मंत्र और राहु-शांति उपाय इन योगों को शमन कर सकते हैं।" if yogas else "",
        "sloka_ref": "Phaladeepika Adh. 12 sloka 13–16",
    }


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
                "Children typically come in the late 20s to mid-30s, or in Saturn's Antar within "
                "a favorable Mahadasha once karmic dues are cleared. Exact timing varies by chart."
            ),
            "reason_hi": (
                "शनि की महादशा या प्रमुख अंतर्दशा में संतान-प्राप्ति में विलम्ब होता है। "
                "20 के दशक के अंत से 30 के मध्य तक, शुभ महादशा में शनि के अंतर में, "
                "जब कर्म-ऋण पूर्ण हो, संतान संभव है। सटीक समय कुंडली-विशेष पर निर्भर है।"
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
            "Saturn's influence on the 5th house suggests children may arrive in the late 20s "
            "to mid-30s, or during a favorable Antardasha within Jupiter's or 5th-lord's Mahadasha. "
            "Remedies (Santan Gopal mantra, Putrakameshti Yagna) and patience are key."
        )
        summary_hi = (
            "पंचम भाव पर शनि के प्रभाव से संतान 20 के दशक के अंत से 30 के मध्य तक "
            "अथवा गुरु / पंचमेश की महादशा में शुभ अंतर में आ सकती है। "
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


def estimate_child_count(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Child count per Phaladeepika Adhyaya 12, Sloka 13.

    Classical method (literal):
      "The number of issues should be determined by the consideration of
       the planets in the 5th house or those posted along with the lord of
       the 5th, as to how many of them are in friendly, depressed, or
       inimical [Navamsas / sign positions]."

    Implementation:
      relevant = planets in 5th house ∪ planets conjunct 5th lord ∪ {5th lord}
      For each relevant planet, apply _sloka13_weight() based on its sign:
        own/exalted  → 1.00 (full contribution)
        friendly     → 0.75
        neutral      → 0.50
        inimical     → 0.25
        debilitated  → 0.00
      score = sum of weights
      Jupiter own/exalted (Sloka 10 bonus) → +0.5 if not already counted

    Score → count mapping (classical "few/some/many" buckets):
      score >= 3.0  → 4 children (many)
      score >= 2.0  → 3
      score >= 1.25 → 2
      score >= 0.5  → 1
      score <  0.5  → uncertain/difficult
    """
    planets = chart_data.get("planets", {}) or {}
    fl = _fifth_lord_info(chart_data)
    ju = _jupiter_info(chart_data)

    fifth_lord = fl.get("lord", "")
    fifth_lord_house = fl.get("placement", 0)

    # Relevant planets per Sloka 13
    in5: set = set(_planets_in_house(planets, 5))
    lord_group: set = set()
    if fifth_lord:
        lord_group.add(fifth_lord)
    if fifth_lord_house > 0:
        lord_group.update(_planets_in_house(planets, fifth_lord_house))
    relevant = list(in5 | lord_group) or ([fifth_lord] if fifth_lord else [])

    # Score each planet
    score = 0.0
    factors: List[str] = []
    for p in relevant:
        p_sign = _sign_of_planet(p, planets)
        weight, label = _sloka13_weight(p, p_sign)
        score += weight
        factors.append(f"{p} in {p_sign} ({label}) → {weight:.2f}")

    # Jupiter own/exalted bonus (Sloka 10: male Navamsa of 5th lord + Sun
    # leads to good number of children; Jupiter in own sign amplifies this)
    ju_sign = ju.get("sign", "")
    if (_is_exalted("Jupiter", ju_sign) or _is_own_sign("Jupiter", ju_sign)) and "Jupiter" not in relevant:
        score += 0.5
        factors.append(f"Jupiter in own/exalted ({ju_sign}) +0.5 (Sloka 10 bonus)")

    # Score → count (classical bucket mapping)
    if score >= 3.0:
        point = 4
    elif score >= 2.0:
        point = 3
    elif score >= 1.25:
        point = 2
    elif score >= 0.5:
        point = 1
    else:
        point = 0

    # Malefic cap: Saturn+Rahu in 5th classically reduce count (karmic obstruction).
    # Strong malefic presence overrides the raw score — cap point at 2 (range 1–2).
    in5_set = set(_planets_in_house(planets, 5))
    heavy_malefics_in_5 = in5_set & {"Saturn", "Rahu", "Ketu"}
    if len(heavy_malefics_in_5) >= 2 and point > 2:
        point = 2
    elif heavy_malefics_in_5 and point > 3:
        point = 3

    low = max(0, point - 1)
    high = point + 1 if point > 0 else 0

    if point == 0:
        label_en = "Progeny uncertain — classical indicators suggest significant challenge"
        label_hi = "संतान अनिश्चित — शास्त्रीय संकेत गंभीर बाधा बताते हैं"
    else:
        label_en = f"Approximately {low}–{high} children indicated"
        label_hi = f"लगभग {low}–{high} संतान का संकेत"

    return {
        "point_estimate": point,
        "count_low": low,
        "count_high": high,
        "label_en": label_en,
        "label_hi": label_hi,
        "method_en": (
            "Per Phaladeepika Adh. 12, Sloka 13: relevant planets are those in "
            "the 5th house and those conjunct the 5th lord. Each is weighted by "
            "its sign relationship — own/exalted=1.0, friendly=0.75, neutral=0.5, "
            "inimical=0.25, debilitated=0. Jupiter in own/exalted adds 0.5 bonus "
            "(Sloka 10). Score maps to count; heavy malefics (2+ of Saturn/Rahu/Ketu) "
            "in 5th cap the count at 1–2 per classical karmic-obstruction principle."
        ),
        "method_hi": (
            "फलदीपिका अध्याय 12, श्लोक 13: पंचम भाव के ग्रह एवं पंचमेश के साथ "
            "स्थित ग्रहों को उनकी राशि-सम्बन्ध से भारित करके संतान-संख्या का निर्धारण। "
            "स्वगृह/उच्च=1.0, मित्र=0.75, सम=0.5, शत्रु=0.25, नीच=0। "
            "गुरु स्वगृह/उच्च हो तो 0.5 अतिरिक्त (श्लोक 10)। "
            "पंचम में 2+ भारी पाप-ग्रह (शनि/राहु/केतु) हों तो अधिकतम 1–2 संतान।"
        ),
        "supporting_factors": factors,
        "sloka_ref": "Phaladeepika Adh. 12 sloka 13",
        "source": "PHALADEEPIKA_SLOKA13",
    }


def detect_gender_yogas(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sprint E item 11 — gender-specific child yogas per Phaladeepika Adh. 12.

    Classical correlations:
      - Male-children yoga:
          5th lord is a male planet (Sun / Mars / Jupiter)
          AND in a male sign (Aries / Gemini / Leo / Libra / Sagittarius / Aquarius)
          AND Jupiter aspects 5th (or sits in 5th).

      - Female-children yoga:
          5th lord is a female planet (Moon / Venus)
          AND in a female sign (Taurus / Cancer / Virgo / Scorpio / Capricorn / Pisces)
          AND Venus / Moon aspects 5th (or sits in 5th).

      - Mixed / neutral:
          5th lord is Mercury or Saturn (neutral),
          OR only one criterion meets — return "mixed".

    Returns {dominant_gender, male_score, female_score, yogas, rationale_en/hi}.
    """
    planets = chart_data.get("planets", {}) or {}
    fl = _fifth_lord_info(chart_data)

    MALE_PLANETS = {"Sun", "Mars", "Jupiter"}
    FEMALE_PLANETS = {"Moon", "Venus"}
    MALE_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}

    male_score = 0
    female_score = 0
    yogas: list[dict] = []
    rationale: list[str] = []

    lord = fl.get("lord", "")
    lord_sign = fl.get("sign", "")

    if lord in MALE_PLANETS:
        male_score += 2
        rationale.append(f"5th lord {lord} is a male planet (+2 male)")
    if lord in FEMALE_PLANETS:
        female_score += 2
        rationale.append(f"5th lord {lord} is a female planet (+2 female)")
    if lord_sign in MALE_SIGNS:
        male_score += 1
        rationale.append(f"5th lord in male sign {lord_sign} (+1 male)")
    elif lord_sign:
        female_score += 1
        rationale.append(f"5th lord in female sign {lord_sign} (+1 female)")

    # Jupiter / Venus influence on 5th
    jup_house = _house_of_planet("Jupiter", planets)
    ven_house = _house_of_planet("Venus", planets)
    moon_house = _house_of_planet("Moon", planets)
    if jup_house == 5 or _aspects_house("Jupiter", 5, planets):
        male_score += 1
        rationale.append("Jupiter in/aspects 5th (+1 male)")
    if ven_house == 5 or _aspects_house("Venus", 5, planets):
        female_score += 1
        rationale.append("Venus in/aspects 5th (+1 female)")
    if moon_house == 5 or _aspects_house("Moon", 5, planets):
        female_score += 1
        rationale.append("Moon in/aspects 5th (+1 female)")

    if male_score >= 3 and male_score > female_score + 1:
        dominant = "male_predominant"
        yogas.append({
            "key": "putra_pradhana",
            "name_en": "Putra-Pradhana Yoga (Male-children dominant)",
            "name_hi": "पुत्र-प्रधान योग",
            "effect_en": "Male children predominate; sons are favoured by the configuration.",
            "effect_hi": "पुत्र-पक्ष की प्रबलता; पुत्रों का योग अधिक।",
            "severity": "auspicious",
            "sloka_ref": "Phaladeepika Adh. 12",
        })
    elif female_score >= 3 and female_score > male_score + 1:
        dominant = "female_predominant"
        yogas.append({
            "key": "kanya_pradhana",
            "name_en": "Kanya-Pradhana Yoga (Female-children dominant)",
            "name_hi": "कन्या-प्रधान योग",
            "effect_en": "Female children predominate; daughters are favoured by the configuration.",
            "effect_hi": "कन्या-पक्ष की प्रबलता; पुत्रियों का योग अधिक।",
            "severity": "auspicious",
            "sloka_ref": "Phaladeepika Adh. 12",
        })
    else:
        dominant = "mixed"
        yogas.append({
            "key": "ubhaya",
            "name_en": "Mixed gender indication",
            "name_hi": "मिश्रित लिंग योग",
            "effect_en": "Balanced indicators — children of both genders likely.",
            "effect_hi": "संतुलित योग — दोनों लिंग की संतान सम्भव।",
            "severity": "neutral",
            "sloka_ref": "Phaladeepika Adh. 12",
        })

    return {
        "dominant_gender": dominant,
        "male_score": male_score,
        "female_score": female_score,
        "yogas": yogas,
        "rationale_en": " · ".join(rationale) if rationale else "Insufficient data for gender inference.",
        "rationale_hi": " · ".join(rationale) if rationale else "लिंग-निर्धारण हेतु पर्याप्त संकेत नहीं।",
        "sloka_ref": "Phaladeepika Adh. 12",
        "source": "PHALADEEPIKA",
    }


def score_fecundity(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sprint E item 12 — 0-100 fecundity score.

    Components (weights sum to 100):
      5th lord strength:               30 pts
      Jupiter strength:                25 pts
      5th house condition:             25 pts   (benefic/malefic occupancy + aspects)
      Panchama (5th from Moon):        10 pts
      Beeja-Sphuta surrogate:          10 pts   (Jupiter + 5th lord dignity combined)

    Returns {score, band, components, sloka_ref, source}.
    """
    planets = chart_data.get("planets", {}) or {}
    fl = _fifth_lord_info(chart_data)
    ju = _jupiter_info(chart_data)

    # Component 1 — 5th lord strength (30)
    c1 = {"strong": 30, "moderate": 18, "weak": 6}.get(fl.get("strength", "moderate"), 15)

    # Component 2 — Jupiter strength (25)
    c2 = {"strong": 25, "moderate": 15, "weak": 5}.get(ju.get("strength", "moderate"), 12)

    # Component 3 — 5th house condition (25)
    in5 = _planets_in_house(planets, 5)
    benefics_in_5 = [p for p in in5 if p in BENEFICS]
    malefics_in_5 = [p for p in in5 if p in MALEFICS]
    c3 = 12  # baseline
    c3 += 5 * len(benefics_in_5)
    c3 -= 5 * len(malefics_in_5)
    # Benefic aspect on 5th
    for b in ("Jupiter", "Venus", "Mercury"):
        if _aspects_house(b, 5, planets):
            c3 += 2
    c3 = max(0, min(25, c3))

    # Component 4 — Panchama from Moon (10)
    moon_house = _house_of_planet("Moon", planets)
    panchama_from_moon = ((moon_house + 3) % 12) + 1 if moon_house else 0
    p5_occupants = _planets_in_house(planets, panchama_from_moon) if panchama_from_moon else []
    c4 = 5
    for p in p5_occupants:
        if p in BENEFICS:
            c4 += 2
        elif p in MALEFICS:
            c4 -= 2
    c4 = max(0, min(10, c4))

    # Component 5 — Beeja-Sphuta surrogate (10)
    # Combined dignity of Jupiter + 5th lord.
    ju_sign = ju.get("sign", "")
    fl_sign = fl.get("sign", "")
    fl_lord = fl.get("lord", "")
    c5 = 5
    if _is_exalted("Jupiter", ju_sign) or _is_own_sign("Jupiter", ju_sign):
        c5 += 3
    if _is_debilitated("Jupiter", ju_sign):
        c5 -= 2
    if fl_lord and (_is_exalted(fl_lord, fl_sign) or _is_own_sign(fl_lord, fl_sign)):
        c5 += 2
    if fl_lord and _is_debilitated(fl_lord, fl_sign):
        c5 -= 2
    c5 = max(0, min(10, c5))

    total = c1 + c2 + c3 + c4 + c5
    if total >= 75:
        band = "excellent"
        band_hi = "उत्तम"
    elif total >= 55:
        band = "good"
        band_hi = "अच्छा"
    elif total >= 35:
        band = "moderate"
        band_hi = "मध्यम"
    elif total >= 20:
        band = "weak"
        band_hi = "दुर्बल"
    else:
        band = "very_weak"
        band_hi = "अत्यंत दुर्बल"

    return {
        "score": total,
        "band": band,
        "band_hi": band_hi,
        "components": {
            "fifth_lord_strength": c1,
            "jupiter_strength": c2,
            "fifth_house_condition": c3,
            "panchama_from_moon": c4,
            "beeja_sphuta_surrogate": c5,
        },
        "max_score": 100,
        "sloka_ref": "Phaladeepika Adh. 12 — composite fecundity scoring",
        "source": "PHALADEEPIKA",
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

    # Sprint E — deeper progeny metrics per Phaladeepika Adh. 12.
    try:
        child_count = estimate_child_count(chart_data)
    except Exception:
        child_count = None
    try:
        gender_analysis = detect_gender_yogas(chart_data)
    except Exception:
        gender_analysis = None
    try:
        fecundity = score_fecundity(chart_data)
    except Exception:
        fecundity = None

    # Sprint F — advanced children analysis (Adh. 12 complete coverage)
    try:
        adoption_indicators = _detect_adoption_indicators(chart_data)
    except Exception:
        adoption_indicators = None
    try:
        female_child_yogas = _detect_female_child_yogas(chart_data)
    except Exception:
        female_child_yogas = None
    try:
        male_child_yogas = _detect_male_child_yogas(chart_data)
    except Exception:
        male_child_yogas = None
    try:
        conception_timing = _get_conception_timing(chart_data)
    except Exception:
        conception_timing = None
    try:
        delivery_indicators = _get_delivery_indicators()
    except Exception:
        delivery_indicators = None
    try:
        child_loss_yogas = _detect_child_loss_yogas_complete(chart_data)
    except Exception:
        child_loss_yogas = None

    return {
        "fifth_house_analysis": fifth,
        "yogas_detected": yogas,
        "progeny_prospect": prospect,
        "children_timing": timing,
        # Sprint E additions:
        "child_count_estimate": child_count,
        "gender_analysis": gender_analysis,
        "fecundity_score": fecundity,
        # Sprint F additions:
        "adoption_indicators": adoption_indicators,
        "female_child_yogas": female_child_yogas,
        "male_child_yogas": male_child_yogas,
        "conception_timing": conception_timing,
        "delivery_indicators": delivery_indicators,
        "child_loss_yogas": child_loss_yogas,
        "recommendations_en": recs["en"],
        "recommendations_hi": recs["hi"],
        "remedies_en": rems["en"],
        "remedies_hi": rems["hi"],
        "sloka_ref": "Phaladeepika Adh. 12",
    }
