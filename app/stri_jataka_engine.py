"""
stri_jataka_engine.py — Stri-Jataka (Women's Horoscope Analysis)
================================================================
Implements Adhyaya 11 of Phaladeepika (slokas 2–15).

Women's horoscope analysis using the 7th house, its lord, Venus (karaka for
spouse) and Jupiter (karaka for husband in a woman's chart). Seven classical
yogas covering widowhood, multiple marriages, chastity, marital happiness,
progeny and service-oriented life.

Yogas detected:

  1. SAHAGAMANA     — devoted wife (Venus in 7th + Jupiter aspect)
  2. VAIDHAVYA      — widowhood risk (Mars+Saturn in 7th OR 7th-lord in 6/8/12 debilitated + Venus afflicted)
  3. PUNARBHU       — multiple marriages (7th lord in dual sign OR Venus+Rahu in 7th OR multiple malefics in 7th)
  4. BHARTRI-SUKHA  — marital happiness (7th lord exalted/own + Jupiter aspect on 7th + Venus in Kendra)
  5. PUTRAVATI      — blessed with children (5th lord strong + Jupiter in Kendra/Trikona)
  6. PATIVRATA      — virtuous/chaste (Jupiter in 1st or 7th + Moon in own/exalted + no malefic affliction)
  7. SEVAKA         — service-oriented/harder life (Saturn in Lagna + weak Jupiter + Venus in Dusthana)
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

# Dual (dvisvabhava) signs — Gemini, Virgo, Sagittarius, Pisces
DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}
KENDRA_TRIKONA = KENDRAS | TRIKONAS

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
STRICT_MALEFICS = {"Mars", "Saturn", "Rahu", "Ketu"}  # not Sun/Moon ambiguity

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

def _planets_dict(chart: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return (chart or {}).get("planets", {}) or {}


def _ascendant_sign(chart: Dict[str, Any]) -> str:
    return (chart or {}).get("ascendant", {}).get("sign", "") or ""


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


def _sign_at_house(ascendant_sign: str, house: int) -> str:
    """Return the zodiac sign occupying a given house number."""
    if ascendant_sign not in ZODIAC or not (1 <= house <= 12):
        return ""
    asc_idx = ZODIAC.index(ascendant_sign)
    return ZODIAC[(asc_idx + house - 1) % 12]


def _sign_house(sign: str, ascendant_sign: str) -> int:
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


def _houses_aspected_by(planet_name: str, planets: Dict[str, Dict[str, Any]]) -> List[int]:
    h = _house_of_planet(planet_name, planets)
    if h < 1 or h > 12:
        return []
    aspects = [((h - 1 + 6) % 12) + 1]  # universal 7th
    for off in SPECIAL_ASPECTS.get(planet_name, []):
        aspects.append(((h - 1 + off - 1) % 12) + 1)
    return aspects


def _aspects_house(source: str, house: int, planets: Dict[str, Dict[str, Any]]) -> bool:
    return house in _houses_aspected_by(source, planets)


def _aspects_planet(source: str, target: str, planets: Dict[str, Dict[str, Any]]) -> bool:
    target_h = _house_of_planet(target, planets)
    if target_h < 1:
        return False
    return target_h in _houses_aspected_by(source, planets)


def _seventh_lord_info(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Return info about the 7th lord: name, sign, house, dignity, strength label."""
    planets = _planets_dict(chart)
    asc_sign = _ascendant_sign(chart)
    seventh_sign = _sign_at_house(asc_sign, 7)
    lord = SIGN_LORD.get(seventh_sign, "")
    if not lord:
        return {
            "seventh_sign": seventh_sign,
            "seventh_lord": "",
            "seventh_lord_sign": "",
            "seventh_lord_placement": 0,
            "seventh_lord_dignity": "unknown",
            "seventh_lord_strength": "unknown",
        }

    lord_sign = _sign_of_planet(lord, planets)
    lord_house = _house_of_planet(lord, planets)

    dignity = "neutral"
    if _is_exalted(lord, lord_sign):
        dignity = "exalted"
    elif _is_debilitated(lord, lord_sign):
        dignity = "debilitated"
    elif _is_own_sign(lord, lord_sign):
        dignity = "own"

    if dignity in ("exalted", "own"):
        strength = "strong"
    elif dignity == "debilitated" or lord_house in DUSTHANAS:
        strength = "weak"
    else:
        strength = "moderate"

    return {
        "seventh_sign": seventh_sign,
        "seventh_lord": lord,
        "seventh_lord_sign": lord_sign,
        "seventh_lord_placement": lord_house,
        "seventh_lord_dignity": dignity,
        "seventh_lord_strength": strength,
    }


def _venus_afflicted(chart: Dict[str, Any]) -> bool:
    """Venus afflicted = in Dusthana, or debilitated, or aspected only by malefics."""
    planets = _planets_dict(chart)
    venus = planets.get("Venus") or {}
    if not venus:
        return False
    v_sign = str(venus.get("sign", ""))
    v_house = _house_of_planet("Venus", planets)

    if _is_debilitated("Venus", v_sign):
        return True
    if v_house in DUSTHANAS:
        return True

    # Aspected only by malefics (at least one malefic aspect and zero benefic aspects)
    malefic_aspects = [
        m for m in STRICT_MALEFICS
        if m in planets and _aspects_planet(m, "Venus", planets)
    ]
    benefic_aspects = [
        b for b in ("Jupiter", "Mercury", "Moon")
        if b in planets and _aspects_planet(b, "Venus", planets)
    ]
    if malefic_aspects and not benefic_aspects:
        return True
    return False


# ───────────────────────────────────────────────────────────────
# Yoga detectors
# ───────────────────────────────────────────────────────────────

def _detect_sahagamana(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Venus in 7th + Jupiter aspecting 7th (devoted wife)."""
    planets = _planets_dict(chart)
    if _house_of_planet("Venus", planets) != 7:
        return None
    if not _aspects_house("Jupiter", 7, planets):
        return None

    factors = ["Venus in 7th house", "Jupiter aspects 7th house"]
    venus_sign = _sign_of_planet("Venus", planets)
    if _is_exalted("Venus", venus_sign):
        factors.append("Venus exalted — exceptional devotion")
    if _is_own_sign("Venus", venus_sign):
        factors.append("Venus in own sign")

    return {
        "key": "sahagamana",
        "name_en": "Sahagamana Yoga",
        "name_hi": "सहगमन योग",
        "effect_en": "Devoted and virtuous wife. Native is deeply attached to her husband, embodies feminine grace, and earns lifelong marital loyalty.",
        "effect_hi": "पतिव्रता एवं समर्पित पत्नी। जातिका पति के प्रति अत्यंत समर्पित है, स्त्रीत्व की गरिमा धारण करती है, और आजीवन वैवाहिक निष्ठा प्राप्त करती है।",
        "severity": "auspicious",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 3",
        "supporting_factors": factors,
    }


def _detect_vaidhavya(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Widowhood risk:
       - Mars AND Saturn both in 7th, OR
       - 7th lord in 6/8/12 + debilitated + Venus afflicted.
    """
    planets = _planets_dict(chart)
    factors: List[str] = []

    mars_h = _house_of_planet("Mars", planets)
    saturn_h = _house_of_planet("Saturn", planets)

    combo1 = (mars_h == 7 and saturn_h == 7)
    if combo1:
        factors.append("Mars and Saturn together in 7th house")

    combo2 = False
    info = _seventh_lord_info(chart)
    if info.get("seventh_lord"):
        lord_house = info["seventh_lord_placement"]
        lord_debilitated = info["seventh_lord_dignity"] == "debilitated"
        venus_bad = _venus_afflicted(chart)
        if lord_house in DUSTHANAS and lord_debilitated and venus_bad:
            combo2 = True
            factors.append(f"7th lord {info['seventh_lord']} in house {lord_house} (Dusthana)")
            factors.append(f"7th lord {info['seventh_lord']} debilitated in {info['seventh_lord_sign']}")
            factors.append("Venus afflicted")

    if not (combo1 or combo2):
        return None

    severity = "high" if combo1 and combo2 else "moderate"
    return {
        "key": "vaidhavya",
        "name_en": "Vaidhavya Yoga",
        "name_hi": "वैधव्य योग",
        "effect_en": "Widowhood risk. Classical texts indicate elevated risk to the husband's longevity; remedial measures and harmonising rituals are prescribed.",
        "effect_hi": "वैधव्य का जोखिम। शास्त्रों के अनुसार पति की आयु पर संकट का संकेत; उपाय एवं शांति-कर्म शास्त्र-सम्मत हैं।",
        "severity": severity,
        "sloka_ref": "Phaladeepika Adh. 11 sloka 5",
        "supporting_factors": factors,
    }


def _detect_punarbhu(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Multiple marriages:
       - 7th lord placed in a dual sign, OR
       - Venus AND Rahu together in 7th, OR
       - Two or more malefics in 7th.
    """
    planets = _planets_dict(chart)
    factors: List[str] = []
    triggered = False

    info = _seventh_lord_info(chart)
    if info.get("seventh_lord"):
        lord_sign = info["seventh_lord_sign"]
        if lord_sign in DUAL_SIGNS:
            triggered = True
            factors.append(f"7th lord {info['seventh_lord']} in dual sign {lord_sign}")

    venus_h = _house_of_planet("Venus", planets)
    rahu_h = _house_of_planet("Rahu", planets)
    if venus_h == 7 and rahu_h == 7:
        triggered = True
        factors.append("Venus and Rahu together in 7th house")

    seventh_occ = _planets_in_house(planets, 7)
    malefics_in_7 = [p for p in seventh_occ if p in STRICT_MALEFICS]
    if len(malefics_in_7) >= 2:
        triggered = True
        factors.append(f"Multiple malefics in 7th: {', '.join(malefics_in_7)}")

    if not triggered:
        return None

    return {
        "key": "punarbhu",
        "name_en": "Punarbhu Yoga",
        "name_hi": "पुनर्भू योग",
        "effect_en": "Possibility of more than one marriage or remarriage. Marital life may involve change of partner; counsel and timing rituals help stabilise the bond.",
        "effect_hi": "एक से अधिक विवाह अथवा पुनर्विवाह की सम्भावना। वैवाहिक जीवन में परिवर्तन हो सकता है; परामर्श एवं मुहूर्त-संस्कार सहायक हैं।",
        "severity": "moderate",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 7",
        "supporting_factors": factors,
    }


def _detect_bhartri_sukha(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Marital happiness:
       7th lord exalted OR in own sign,
       AND Jupiter aspects 7th,
       AND Venus in a Kendra.
    """
    planets = _planets_dict(chart)
    info = _seventh_lord_info(chart)
    lord = info.get("seventh_lord")
    if not lord:
        return None
    if info["seventh_lord_dignity"] not in ("exalted", "own"):
        return None
    if not _aspects_house("Jupiter", 7, planets):
        return None
    venus_h = _house_of_planet("Venus", planets)
    if venus_h not in KENDRAS:
        return None

    factors = [
        f"7th lord {lord} {info['seventh_lord_dignity']} in {info['seventh_lord_sign']}",
        "Jupiter aspects 7th house",
        f"Venus in Kendra (house {venus_h})",
    ]

    return {
        "key": "bhartri_sukha",
        "name_en": "Bhartri-Sukha Yoga",
        "name_hi": "भर्तृ-सुख योग",
        "effect_en": "Marital happiness and supportive husband. Native enjoys a loving and prosperous home, harmony with her spouse, and respect in her household.",
        "effect_hi": "वैवाहिक सुख एवं सहयोगी पति। जातिका को प्रेमपूर्ण एवं समृद्ध गृहस्थ जीवन, पति से तालमेल और परिवार में सम्मान प्राप्त होता है।",
        "severity": "auspicious",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 9",
        "supporting_factors": factors,
    }


def _detect_putravati(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Blessed with children:
       5th lord strong (exalted/own/Kendra-Trikona)
       AND Jupiter in a Kendra or Trikona.
    """
    planets = _planets_dict(chart)
    asc_sign = _ascendant_sign(chart)
    fifth_sign = _sign_at_house(asc_sign, 5)
    fifth_lord = SIGN_LORD.get(fifth_sign, "")
    if not fifth_lord:
        return None

    fl_sign = _sign_of_planet(fifth_lord, planets)
    fl_house = _house_of_planet(fifth_lord, planets)

    fl_strong = (
        _is_exalted(fifth_lord, fl_sign)
        or _is_own_sign(fifth_lord, fl_sign)
        or fl_house in KENDRA_TRIKONA
    )
    if not fl_strong:
        return None

    jup_house = _house_of_planet("Jupiter", planets)
    if jup_house not in KENDRA_TRIKONA:
        return None

    factors = [
        f"5th lord {fifth_lord} strong in {fl_sign} (house {fl_house})",
        f"Jupiter in house {jup_house} (Kendra/Trikona)",
    ]
    if _is_exalted(fifth_lord, fl_sign):
        factors.append(f"5th lord {fifth_lord} exalted")
    if _is_own_sign(fifth_lord, fl_sign):
        factors.append(f"5th lord {fifth_lord} in own sign")

    return {
        "key": "putravati",
        "name_en": "Putravati Yoga",
        "name_hi": "पुत्रवती योग",
        "effect_en": "Blessed with progeny. Native is likely to have virtuous, healthy and successful children who bring joy and continue the family legacy.",
        "effect_hi": "संतान-सुख का योग। जातिका को गुणी, स्वस्थ और सफल संतान प्राप्त होने की सम्भावना है जो कुल की परंपरा आगे बढ़ाती है।",
        "severity": "auspicious",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 11",
        "supporting_factors": factors,
    }


def _detect_pativrata(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Virtuous/chaste:
       Jupiter in 1st OR 7th,
       AND Moon in own sign (Cancer) or exalted (Taurus),
       AND no malefic in 7th house.
    """
    planets = _planets_dict(chart)
    jup_h = _house_of_planet("Jupiter", planets)
    if jup_h not in (1, 7):
        return None

    moon_sign = _sign_of_planet("Moon", planets)
    if not (_is_own_sign("Moon", moon_sign) or _is_exalted("Moon", moon_sign)):
        return None

    seventh_occ = _planets_in_house(planets, 7)
    malefics_in_7 = [p for p in seventh_occ if p in STRICT_MALEFICS]
    if malefics_in_7:
        return None

    factors = [
        f"Jupiter in house {jup_h}",
        f"Moon in {moon_sign}" + (" (own sign)" if _is_own_sign("Moon", moon_sign) else " (exalted)"),
        "No malefic in 7th house",
    ]

    return {
        "key": "pativrata",
        "name_en": "Pativrata Yoga",
        "name_hi": "पतिव्रता योग",
        "effect_en": "Virtuous and chaste nature. Native embodies integrity, devotion and dharmic conduct; she is widely respected for her character and inner strength.",
        "effect_hi": "पतिव्रता एवं चारित्रिक शुद्धि का योग। जातिका सदाचार, समर्पण और धर्मनिष्ठा से युक्त है; उसके चरित्र और आंतरिक बल के लिए सर्वत्र आदर प्राप्त होता है।",
        "severity": "auspicious",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 13",
        "supporting_factors": factors,
    }


def _detect_sevaka(chart: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Service-oriented/harder life:
       Saturn in Lagna,
       AND Jupiter weak (debilitated OR in Dusthana),
       AND Venus in a Dusthana.
    """
    planets = _planets_dict(chart)
    if _house_of_planet("Saturn", planets) != 1:
        return None

    jup_sign = _sign_of_planet("Jupiter", planets)
    jup_house = _house_of_planet("Jupiter", planets)
    jup_weak = _is_debilitated("Jupiter", jup_sign) or jup_house in DUSTHANAS
    if not jup_weak:
        return None

    venus_h = _house_of_planet("Venus", planets)
    if venus_h not in DUSTHANAS:
        return None

    factors = [
        "Saturn in Lagna",
        f"Jupiter weak ({'debilitated' if _is_debilitated('Jupiter', jup_sign) else f'in Dusthana house {jup_house}'})",
        f"Venus in Dusthana (house {venus_h})",
    ]

    return {
        "key": "sevaka",
        "name_en": "Sevaka Yoga",
        "name_hi": "सेवक योग",
        "effect_en": "Service-oriented life with hardships. Native may face domestic struggle and a life of toil; spiritual practice and karma-yoga transform the difficulty into merit.",
        "effect_hi": "सेवापरायण किन्तु कष्टमय जीवन। जातिका को गृहस्थ में संघर्ष और परिश्रम का सामना करना पड़ सकता है; साधना एवं कर्मयोग कष्ट को पुण्य में परिणत करते हैं।",
        "severity": "challenging",
        "sloka_ref": "Phaladeepika Adh. 11 sloka 15",
        "supporting_factors": factors,
    }


# ───────────────────────────────────────────────────────────────
# 7th-house overview
# ───────────────────────────────────────────────────────────────

def _seventh_house_analysis(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Structured summary of the 7th house (spouse/marriage bhava)."""
    planets = _planets_dict(chart)
    asc_sign = _ascendant_sign(chart)
    info = _seventh_lord_info(chart)

    seventh_occ = _planets_in_house(planets, 7)
    malefics_in_7th = [p for p in seventh_occ if p in STRICT_MALEFICS]
    benefics_in_7th = [p for p in seventh_occ if p in BENEFICS]

    jupiter_aspects_7th = _aspects_house("Jupiter", 7, planets)
    venus_house = _house_of_planet("Venus", planets)
    venus_position = f"house {venus_house}" if venus_house else "unknown"

    # Interpretation
    if info.get("seventh_lord_strength") == "strong" and jupiter_aspects_7th and not malefics_in_7th:
        interp_en = "7th house is well-fortified — favourable marital prospects."
        interp_hi = "सप्तम भाव सुदृढ़ है — वैवाहिक जीवन अनुकूल है।"
    elif len(malefics_in_7th) >= 2 or info.get("seventh_lord_strength") == "weak":
        interp_en = "7th house is afflicted — marital harmony requires care and remedies."
        interp_hi = "सप्तम भाव पीड़ित है — वैवाहिक सामंजस्य हेतु सावधानी एवं उपाय अपेक्षित हैं।"
    else:
        interp_en = "7th house is mixed — ordinary marital life with ups and downs."
        interp_hi = "सप्तम भाव मिश्र है — सामान्य वैवाहिक जीवन जिसमें सुख-दुख दोनों मिलेंगे।"

    return {
        "seventh_sign": info.get("seventh_sign", ""),
        "seventh_lord": info.get("seventh_lord", ""),
        "seventh_lord_placement": info.get("seventh_lord_placement", 0),
        "seventh_lord_sign": info.get("seventh_lord_sign", ""),
        "seventh_lord_dignity": info.get("seventh_lord_dignity", "unknown"),
        "seventh_lord_strength": info.get("seventh_lord_strength", "unknown"),
        "malefics_in_7th": malefics_in_7th,
        "benefics_in_7th": benefics_in_7th,
        "jupiter_aspects_7th": bool(jupiter_aspects_7th),
        "venus_position": venus_position,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
    }


# ───────────────────────────────────────────────────────────────
# Prospect + recommendations synthesis
# ───────────────────────────────────────────────────────────────

def _score_prospect(yogas: List[Dict[str, Any]], sa: Dict[str, Any]) -> str:
    auspicious = sum(1 for y in yogas if y.get("severity") == "auspicious")
    challenging = sum(1 for y in yogas if y.get("severity") in ("challenging", "high"))
    moderate = sum(1 for y in yogas if y.get("severity") == "moderate")

    if auspicious >= 2 and challenging == 0:
        return "favorable"
    if challenging >= 1 and auspicious == 0:
        return "challenging"
    if auspicious >= 1 and challenging == 0 and sa.get("seventh_lord_strength") != "weak":
        return "favorable"
    if sa.get("seventh_lord_strength") == "weak" and auspicious == 0:
        return "challenging"
    if auspicious == 0 and challenging == 0 and moderate == 0:
        # Nothing special — use 7th house interpretation as fallback
        return "favorable" if sa.get("seventh_lord_strength") == "strong" else "mixed"
    return "mixed"


def _recommendations(yogas: List[Dict[str, Any]], prospect: str) -> tuple[List[str], List[str]]:
    en: List[str] = []
    hi: List[str] = []

    keys = {y["key"] for y in yogas}

    if "vaidhavya" in keys:
        en.append("Perform Mrityunjaya japa and Mangala shanti; include husband's longevity rituals.")
        hi.append("मृत्युंजय जप एवं मंगल शांति कराएँ; पति की दीर्घायु हेतु अनुष्ठान सम्मिलित करें।")
    if "punarbhu" in keys:
        en.append("Delay marriage past mid-twenties; conduct matchmaking with careful 7th-house comparison.")
        hi.append("विवाह मध्य-आयु में करें; कुंडली मिलान में सप्तम भाव का सावधानीपूर्वक विचार करें।")
    if "sevaka" in keys:
        en.append("Strengthen Jupiter — weekly Brihaspati puja, yellow garments on Thursday, service to elders.")
        hi.append("बृहस्पति को प्रबल करें — गुरुवार को बृहस्पति पूजा, पीत वस्त्र, बड़ों की सेवा।")
    if "sahagamana" in keys or "pativrata" in keys or "bhartri_sukha" in keys:
        en.append("Maintain dharmic household conduct; celebrate Tulsi Vivah and Karva Chauth to sustain positive yogas.")
        hi.append("धर्मयुक्त गृहाचरण रखें; सकारात्मक योगों की रक्षा हेतु तुलसी विवाह एवं करवा चौथ मनाएँ।")
    if "putravati" in keys:
        en.append("Observe Santan Gopal japa to reinforce the progeny yoga.")
        hi.append("संतान गोपाल मंत्र जप द्वारा पुत्रवती योग को सुदृढ़ करें।")

    # Baseline recommendations by prospect
    if prospect == "challenging":
        en.append("Consult a qualified jyotishi before fixing marriage muhurta; use gemstone therapy with care.")
        hi.append("विवाह मुहूर्त तय करने से पूर्व योग्य ज्योतिषी से परामर्श लें; रत्न-चिकित्सा सावधानी से करें।")
    elif prospect == "favorable":
        en.append("The chart supports marital happiness — maintain regular Venus and Jupiter remedies.")
        hi.append("कुंडली वैवाहिक सुख के अनुकूल है — नियमित शुक्र एवं गुरु के उपाय जारी रखें।")
    else:
        en.append("Mixed indications — strengthen weak factors and protect strong ones through regular devotional practice.")
        hi.append("मिश्र संकेत — दुर्बल तत्वों को सशक्त करें और प्रबल तत्वों की रक्षा नियमित साधना से करें।")

    # Always include a universal note
    en.append("All remedies supplement, not replace, personal and medical counsel.")
    hi.append("सभी उपाय व्यक्तिगत एवं चिकित्सीय परामर्श के पूरक हैं, विकल्प नहीं।")

    return en, hi


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def analyze_stri_jataka(chart_data: Dict[str, Any], gender: str = "female") -> Dict[str, Any]:
    """
    Analyse a female horoscope per Phaladeepika Adhyaya 11 (Stri-Jataka).

    Args:
        chart_data: {
            'planets':   {'Sun': {'sign': 'Aries', 'house': 1, ...}, ...},
            'ascendant': {'sign': 'Aries'},
            ...
        }
        gender: 'female' (default). Any other value returns {"applicable": False}.

    Returns:
        See module docstring for full schema.
    """
    # Gender filter
    if (gender or "").strip().lower() != "female":
        return {
            "applicable": False,
            "reason": "Stri-Jataka analysis applies only to female horoscopes.",
            "yogas_detected": [],
            "seventh_house_analysis": {},
            "marital_prospect": "n/a",
            "recommendations_en": [],
            "recommendations_hi": [],
            "sloka_ref": "Phaladeepika Adh. 11",
        }

    if not isinstance(chart_data, dict):
        return {
            "applicable": True,
            "yogas_detected": [],
            "seventh_house_analysis": {},
            "marital_prospect": "mixed",
            "recommendations_en": [],
            "recommendations_hi": [],
            "sloka_ref": "Phaladeepika Adh. 11",
        }

    detectors = (
        _detect_sahagamana,
        _detect_vaidhavya,
        _detect_punarbhu,
        _detect_bhartri_sukha,
        _detect_putravati,
        _detect_pativrata,
        _detect_sevaka,
    )

    yogas_detected: List[Dict[str, Any]] = []
    for detector in detectors:
        try:
            result = detector(chart_data)
        except Exception:
            result = None
        if result:
            yogas_detected.append(result)

    sa = _seventh_house_analysis(chart_data)
    prospect = _score_prospect(yogas_detected, sa)
    rec_en, rec_hi = _recommendations(yogas_detected, prospect)

    return {
        "applicable": True,
        "yogas_detected": yogas_detected,
        "seventh_house_analysis": sa,
        "marital_prospect": prospect,
        "recommendations_en": rec_en,
        "recommendations_hi": rec_hi,
        "sloka_ref": "Phaladeepika Adh. 11",
    }
