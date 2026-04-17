"""
nidhana_engine.py — Nidhana-phala (longevity indicators + karmic transitions)
==============================================================================
Implements Phaladeepika Adhyaya 17 with sensitive, philosophical framing.

IMPORTANT framing policy:
    Adhyaya 17 classically deals with nidhana — end-of-life phalam. This
    engine intentionally reframes the material as "longevity indicators and
    karmic transitions" and does NOT output specific death dates or ages.
    Keep all narrative philosophical and supportive.

Classical rules used:
    * Marakas — lords of 2nd and 7th houses are classical maraka-sthāna lords.
    * 8th house — primary longevity bhava. Its lord's strength + placement
      and any occupants are key indicators.
    * 3rd house — secondary longevity / vitality bhava (upachaya).
    * Saturn — natural significator of longevity and endurance. Its
      placement in the chart is highly relevant.
    * Moon's nakshatra / general strength — reflects vital current.

Main function:
    analyze_longevity_indicators(chart_data) -> dict
"""
from __future__ import annotations
from typing import Any, Dict, List

# ───────────────────────────────────────────────────────────────
# Classical constants (shared vocabulary)
# ───────────────────────────────────────────────────────────────

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn",
    "Aquarius": "Saturn", "Pisces": "Jupiter",
}

EXALTATION: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
    "Rahu": "Taurus", "Ketu": "Scorpio",
}

DEBILITATION: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
    "Rahu": "Scorpio", "Ketu": "Taurus",
}

OWN_SIGNS: Dict[str, set] = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
    "Rahu": set(), "Ketu": set(),
}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _planets(chart: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return chart.get("planets", {}) or {}


def _asc_sign(chart: Dict[str, Any]) -> str:
    return str((chart.get("ascendant") or {}).get("sign", ""))


def _int_house(pdata: Dict[str, Any]) -> int:
    try:
        return int(pdata.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _lord_of(house: int, chart: Dict[str, Any]) -> str:
    """Return the sign-lord of the Nth house from ascendant (whole-sign)."""
    asc = _asc_sign(chart)
    if asc not in ZODIAC or not (1 <= house <= 12):
        return ""
    idx = (ZODIAC.index(asc) + house - 1) % 12
    return SIGN_LORD.get(ZODIAC[idx], "")


def _planet_house(planet: str, chart: Dict[str, Any]) -> int:
    p = _planets(chart).get(planet)
    if not isinstance(p, dict):
        return 0
    return _int_house(p)


def _planet_sign(planet: str, chart: Dict[str, Any]) -> str:
    p = _planets(chart).get(planet)
    if not isinstance(p, dict):
        return ""
    return str(p.get("sign", ""))


def _is_exalted(planet: str, sign: str) -> bool:
    return bool(sign) and EXALTATION.get(planet) == sign


def _is_own(planet: str, sign: str) -> bool:
    return bool(sign) and sign in OWN_SIGNS.get(planet, set())


def _is_debilitated(planet: str, sign: str) -> bool:
    return bool(sign) and DEBILITATION.get(planet) == sign


def _planet_strength(planet: str, chart: Dict[str, Any]) -> str:
    """Return strong / moderate / weak / missing for a planet in the chart."""
    if planet not in _planets(chart):
        return "missing"
    sign = _planet_sign(planet, chart)
    house = _planet_house(planet, chart)
    if _is_exalted(planet, sign) or _is_own(planet, sign):
        return "strong"
    if _is_debilitated(planet, sign):
        return "weak"
    if house in DUSTHANAS:
        return "weak"
    if house in (KENDRAS | TRIKONAS):
        return "moderate"
    return "moderate"


def _maraka_assessment(lord_house: int, chart: Dict[str, Any]) -> str:
    """Qualitative strength label for a maraka planet's influence."""
    if lord_house in (KENDRAS | TRIKONAS):
        # Well-placed maraka — classical texts treat this as stronger influence
        return "strong"
    if lord_house in DUSTHANAS:
        # In a Dusthana — its maraka influence is considered less effective
        return "weak"
    if lord_house == 0:
        return "unknown"
    return "moderate"


# ───────────────────────────────────────────────────────────────
# Sections
# ───────────────────────────────────────────────────────────────

def _maraka_planets_section(chart: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return [{planet, role, placement, strength, notes_en, notes_hi}, ...]."""
    out: List[Dict[str, Any]] = []
    for house_num, role_en, role_hi in (
        (2, "2nd lord", "द्वितीयेश"),
        (7, "7th lord", "सप्तमेश"),
    ):
        planet = _lord_of(house_num, chart)
        if not planet:
            continue
        placement = _planet_house(planet, chart)
        strength = _maraka_assessment(placement, chart)
        placement_str = str(placement) if placement > 0 else "unknown"

        if strength == "strong":
            notes_en = (
                f"{planet} as {role_en} is placed in house {placement_str}, a supportive position. "
                "Classical texts treat such maraka placements as informational indicators, not fateful predictions."
            )
            notes_hi = (
                f"{planet} ({role_hi}) भाव {placement_str} में स्थित है — एक सहायक स्थिति। "
                "शास्त्र ऐसे मारक संकेतों को केवल सूचनात्मक मानते हैं, नियति-सूचक नहीं।"
            )
        elif strength == "weak":
            notes_en = (
                f"{planet} as {role_en} is placed in a Dusthana (house {placement_str}); "
                "its maraka influence is considered diluted."
            )
            notes_hi = (
                f"{planet} ({role_hi}) दुःस्थान (भाव {placement_str}) में है; "
                "इसका मारक प्रभाव शिथिल माना गया है।"
            )
        else:
            notes_en = (
                f"{planet} as {role_en} is in house {placement_str}. "
                "Classical notes consider this a neutral karmic indicator."
            )
            notes_hi = (
                f"{planet} ({role_hi}) भाव {placement_str} में है। "
                "शास्त्रानुसार यह तटस्थ कर्म-सूचक है।"
            )

        out.append({
            "planet": planet,
            "role": role_en,
            "role_hi": role_hi,
            "placement": placement,
            "strength": strength,
            "notes_en": notes_en,
            "notes_hi": notes_hi,
        })
    return out


def _eighth_house_section(chart: Dict[str, Any]) -> Dict[str, Any]:
    eighth_lord = _lord_of(8, chart)
    placement = _planet_house(eighth_lord, chart) if eighth_lord else 0
    strength = _planet_strength(eighth_lord, chart) if eighth_lord else "missing"

    planets_in_8 = [
        p for p, pd in _planets(chart).items()
        if isinstance(pd, dict) and _int_house(pd) == 8
    ]

    if strength == "strong":
        interp_en = (
            f"The 8th lord ({eighth_lord}) is strong and placed in house "
            f"{placement}. Classical rules treat this as a positive longevity indicator."
        )
        interp_hi = (
            f"अष्टमेश ({eighth_lord}) बलवान है तथा भाव {placement} में स्थित है। "
            "शास्त्र इसे दीर्घायु का शुभ संकेत मानते हैं।"
        )
    elif strength == "weak":
        interp_en = (
            f"The 8th lord ({eighth_lord}) is in a weak condition — house {placement}. "
            "Classical texts advise pursuing a disciplined lifestyle and spiritual practices."
        )
        interp_hi = (
            f"अष्टमेश ({eighth_lord}) दुर्बल स्थिति में है (भाव {placement})। "
            "शास्त्र संयमित जीवन एवं आध्यात्मिक साधना की अनुशंसा करते हैं।"
        )
    elif strength == "missing":
        interp_en = (
            "The 8th lord is not present in the chart — classical longevity indicators "
            "cannot be drawn from this single factor alone."
        )
        interp_hi = (
            "अष्टमेश कुंडली में उपस्थित नहीं है — केवल इस एक कारक से दीर्घायु-निर्णय सम्भव नहीं।"
        )
    else:
        interp_en = (
            f"The 8th lord ({eighth_lord}) is in a neutral condition (house {placement}). "
            "Longevity indicators from this factor are balanced."
        )
        interp_hi = (
            f"अष्टमेश ({eighth_lord}) तटस्थ स्थिति में है (भाव {placement})। "
            "इस कारक से आयु-संकेत संतुलित हैं।"
        )

    return {
        "eighth_lord": eighth_lord,
        "eighth_lord_placement": placement,
        "eighth_lord_strength": strength,
        "planets_in_8th": planets_in_8,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
    }


def _saturn_section(chart: Dict[str, Any]) -> Dict[str, Any]:
    saturn_house = _planet_house("Saturn", chart)
    saturn_sign = _planet_sign("Saturn", chart)
    saturn_strength = _planet_strength("Saturn", chart)

    if saturn_strength == "strong":
        interp_en = (
            f"Saturn is well placed ({saturn_sign}, house {saturn_house}). "
            "As the natural significator of longevity and endurance, this strengthens vitality and resilience."
        )
        interp_hi = (
            f"शनि उत्तम स्थिति में है ({saturn_sign}, भाव {saturn_house})। "
            "शनि आयुकारक है; यह स्थिरता एवं सहनशीलता को सुदृढ़ करता है।"
        )
    elif saturn_strength == "weak":
        interp_en = (
            f"Saturn is in a weak condition ({saturn_sign or 'unknown sign'}, house {saturn_house}). "
            "Classical guidance: cultivate discipline, regular routines, and Saturn's remedies to strengthen this area."
        )
        interp_hi = (
            f"शनि दुर्बल स्थिति में है ({saturn_sign or 'अज्ञात राशि'}, भाव {saturn_house})। "
            "शास्त्रीय परामर्श: अनुशासन, नियमित दिनचर्या एवं शनि-संबंधी उपाय इस क्षेत्र को बल देते हैं।"
        )
    elif saturn_strength == "missing":
        interp_en = "Saturn is not present in the chart data."
        interp_hi = "कुंडली आंकड़ों में शनि उपस्थित नहीं है।"
    else:
        interp_en = (
            f"Saturn is placed in house {saturn_house} ({saturn_sign}). "
            "Its longevity-significator role reads as balanced here."
        )
        interp_hi = (
            f"शनि भाव {saturn_house} ({saturn_sign}) में स्थित है। "
            "आयुकारक की भूमिका यहाँ संतुलित प्रतीत होती है।"
        )

    return {
        "saturn_placement": saturn_house,
        "saturn_sign": saturn_sign,
        "saturn_strength": saturn_strength,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
    }


def _overall_strength(
    marakas: List[Dict[str, Any]],
    eighth: Dict[str, Any],
    saturn: Dict[str, Any],
) -> str:
    """Synthesise a 3-bucket label from the sub-analyses."""
    score = 0
    # 8th lord
    if eighth["eighth_lord_strength"] == "strong":
        score += 2
    elif eighth["eighth_lord_strength"] == "weak":
        score -= 2

    # Saturn
    if saturn["saturn_strength"] == "strong":
        score += 2
    elif saturn["saturn_strength"] == "weak":
        score -= 2

    # Marakas — strong marakas are classical challenge; weak marakas ease
    for m in marakas:
        if m["strength"] == "strong":
            score -= 1
        elif m["strength"] == "weak":
            score += 1

    if score >= 2:
        return "strong"
    if score <= -2:
        return "weak"
    return "moderate"


def _karmic_transitions_narrative(overall: str) -> Dict[str, str]:
    if overall == "strong":
        return {
            "karmic_transitions_en": (
                "The chart suggests resilience through major life transitions. "
                "Periods of inner change and transformation are likely to be navigated with strength. "
                "Classical texts emphasise that every life chapter carries its own dharma — "
                "this analysis is not a prediction of specific events, only a philosophical lens."
            ),
            "karmic_transitions_hi": (
                "कुंडली जीवन के प्रमुख मोड़ों में दृढ़ता का संकेत देती है। "
                "परिवर्तन एवं आंतरिक रूपांतरण के कालखंड बल के साथ पार किए जाते हैं। "
                "शास्त्रानुसार प्रत्येक जीवन-अध्याय का अपना धर्म है — "
                "यह विश्लेषण किसी विशेष घटना की भविष्यवाणी नहीं, केवल दार्शनिक दृष्टिकोण है।"
            ),
        }
    if overall == "weak":
        return {
            "karmic_transitions_en": (
                "The chart indicates that inner discipline, steady routines, and spiritual practice "
                "can soften the intensity of karmic transitions. Classical wisdom offers remedies — "
                "mantra, charity, and mindful living — as means of strengthening vitality. "
                "This is guidance, not prophecy."
            ),
            "karmic_transitions_hi": (
                "कुंडली बताती है कि आंतरिक अनुशासन, स्थिर दिनचर्या एवं आध्यात्मिक साधना "
                "कर्म-संक्रमण की तीव्रता को कम कर सकती है। शास्त्र मंत्र, दान एवं "
                "संतुलित जीवन को जीवन-शक्ति बढ़ाने का उपाय मानते हैं। "
                "यह मार्गदर्शन है, भविष्यवाणी नहीं।"
            ),
        }
    return {
        "karmic_transitions_en": (
            "Life transitions are shown as balanced — neither overwhelming nor effortless. "
            "Classical texts teach that consciousness shapes the quality of every chapter. "
            "This narrative is philosophical; it is not a prediction of specific events."
        ),
        "karmic_transitions_hi": (
            "जीवन के मोड़ संतुलित दिखाई देते हैं — न अत्यधिक कठिन, न पूर्णतः सहज। "
            "शास्त्रानुसार चेतना ही प्रत्येक अध्याय के गुणधर्म को गढ़ती है। "
            "यह कथन दार्शनिक है; किसी विशेष घटना की भविष्यवाणी नहीं।"
        ),
    }


def _life_chapters(overall: str) -> Dict[str, List[str]]:
    if overall == "strong":
        en = [
            "Early chapter — foundational learning and the unfolding of personal dharma.",
            "Middle chapter — expression through work, family, and mature relationships.",
            "Later chapter — wisdom, contemplation, and the refinement of inner life.",
        ]
        hi = [
            "प्रारम्भिक अध्याय — आधारभूत शिक्षण एवं व्यक्तिगत धर्म का उद्घाटन।",
            "मध्य अध्याय — कर्म, परिवार एवं परिपक्व सम्बन्धों के माध्यम से अभिव्यक्ति।",
            "उत्तर अध्याय — ज्ञान, चिन्तन एवं आंतरिक जीवन की परिशुद्धि।",
        ]
    elif overall == "weak":
        en = [
            "Early chapter — growth through learning and careful habits; guidance from elders matters.",
            "Middle chapter — balance through service and steady routines; remedies are supportive.",
            "Later chapter — gradual turn inward; contemplation and dharma practices soften transitions.",
        ]
        hi = [
            "प्रारम्भिक अध्याय — सीखने एवं सुगठित आदतों से विकास; वरिष्ठजनों का मार्गदर्शन महत्वपूर्ण।",
            "मध्य अध्याय — सेवा एवं नियमित दिनचर्या से संतुलन; उपाय सहायक हैं।",
            "उत्तर अध्याय — क्रमशः अन्तर्मुखता; चिन्तन एवं धर्म-साधना संक्रमण को सहज बनाती है।",
        ]
    else:
        en = [
            "Early chapter — formation of character through varied experiences.",
            "Middle chapter — the active phase of karma and relationship.",
            "Later chapter — reflection, integration, and the inward turn.",
        ]
        hi = [
            "प्रारम्भिक अध्याय — विविध अनुभवों से चरित्र-निर्माण।",
            "मध्य अध्याय — कर्म एवं सम्बन्धों का सक्रिय काल।",
            "उत्तर अध्याय — चिन्तन, समन्वय एवं अन्तर्यात्रा।",
        ]
    return {"life_chapters_en": en, "life_chapters_hi": hi}


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def analyze_longevity_indicators(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Philosophical longevity analysis per Phaladeepika Adh. 17.

    Does NOT output specific ages or death-year predictions.
    """
    if not isinstance(chart_data, dict):
        chart_data = {}

    marakas = _maraka_planets_section(chart_data)
    eighth = _eighth_house_section(chart_data)
    saturn = _saturn_section(chart_data)
    overall = _overall_strength(marakas, eighth, saturn)
    karmic = _karmic_transitions_narrative(overall)
    chapters = _life_chapters(overall)

    return {
        "overall_longevity_strength": overall,
        "maraka_planets": marakas,
        "eighth_house_analysis": eighth,
        "saturn_longevity_assessment": saturn,
        "karmic_transitions_en": karmic["karmic_transitions_en"],
        "karmic_transitions_hi": karmic["karmic_transitions_hi"],
        "life_chapters_en": chapters["life_chapters_en"],
        "life_chapters_hi": chapters["life_chapters_hi"],
        "sloka_ref": "Phaladeepika Adh. 17",
    }
