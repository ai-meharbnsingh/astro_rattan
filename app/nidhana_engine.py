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
from typing import Any, Dict, List, Optional

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


def _sign_of_house_nidhana(h: int, asc_sign: str) -> str:
    """Return the sign occupying house h from ascendant (whole-sign)."""
    if asc_sign not in ZODIAC or not (1 <= h <= 12):
        return ""
    return ZODIAC[(ZODIAC.index(asc_sign) + h - 1) % 12]


def _transit_timing_section(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns transit-timing indicators for longevity/karmic transitions.
    Classical: maraka activation via Saturn/Jupiter/Mars transits through
    key houses (Phaladeepika Adh. 17 + Adh. 26 transit principles).

    Returns:
    {
        "indicators": [
            {
                "planet_transit": "Saturn",
                "target_sign": "Scorpio",
                "target_house": 8,
                "significance_en": "...",
                "significance_hi": "...",
                "watch_period_en": "When Saturn transits Scorpio (8th house)...",
                "watch_period_hi": "...",
                "intensity": "high"  # high / moderate / low
            },
            ...
        ],
        "summary_en": "...",
        "summary_hi": "...",
        "sloka_ref": "Phaladeepika Adh. 17"
    }
    """
    asc = _asc_sign(chart_data)

    indicators: List[Dict[str, Any]] = []

    # ── 8th house sign ─────────────────────────────────────────
    eighth_sign = _sign_of_house_nidhana(8, asc) if asc else ""
    second_sign = _sign_of_house_nidhana(2, asc) if asc else ""
    seventh_sign = _sign_of_house_nidhana(7, asc) if asc else ""

    # Maraka lords
    maraka_2nd = _lord_of(2, chart_data)
    maraka_7th = _lord_of(7, chart_data)

    # Where do maraka lords sit natally?
    maraka_2nd_sign = _planet_sign(maraka_2nd, chart_data) if maraka_2nd else ""
    maraka_7th_sign = _planet_sign(maraka_7th, chart_data) if maraka_7th else ""

    moon_natal_house = _planet_house("Moon", chart_data)
    moon_natal_sign = _planet_sign("Moon", chart_data)

    # 1. Saturn transiting 8th house sign → highest intensity
    if eighth_sign:
        indicators.append({
            "planet_transit": "Saturn",
            "target_sign": eighth_sign,
            "target_house": 8,
            "significance_en": (
                f"Saturn transiting {eighth_sign} activates the 8th house — the primary longevity bhava. "
                "Classical texts describe this as the most significant karmic review period."
            ),
            "significance_hi": (
                f"शनि का {eighth_sign} में गोचर अष्टम भाव (प्राथमिक आयु-भाव) को सक्रिय करता है। "
                "शास्त्र इसे सर्वाधिक महत्वपूर्ण कर्म-समीक्षा काल मानते हैं।"
            ),
            "watch_period_en": (
                f"When Saturn transits {eighth_sign} (8th house from your ascendant), "
                "a deep karmic review period is activated. This is a time for spiritual deepening, "
                "not to be feared but to be embraced with awareness."
            ),
            "watch_period_hi": (
                f"जब शनि {eighth_sign} (लग्न से अष्टम भाव) में गोचर करे, "
                "तब गहरी कर्म-समीक्षा का काल सक्रिय होता है। यह आध्यात्मिक गहनता का समय है, "
                "भय का नहीं — इसे सचेतन रूप से अपनाएं।"
            ),
            "intensity": "high",
        })

    # 2. Saturn transiting natal 2nd house sign → maraka (2nd house) activation
    if second_sign:
        indicators.append({
            "planet_transit": "Saturn",
            "target_sign": second_sign,
            "target_house": 2,
            "significance_en": (
                f"Saturn transiting {second_sign} activates the 2nd-house maraka theme. "
                "Classical rules treat this as a period requiring mindful resource stewardship."
            ),
            "significance_hi": (
                f"शनि का {second_sign} में गोचर द्वितीय भाव के मारक-विषय को सक्रिय करता है। "
                "शास्त्र इसे संसाधनों के सावधान प्रबंधन का काल मानते हैं।"
            ),
            "watch_period_en": (
                f"When Saturn transits {second_sign} (your natal 2nd house sign), "
                "themes of wealth, speech, and family transitions come into focus. "
                "Disciplined action and spiritual practice are recommended."
            ),
            "watch_period_hi": (
                f"जब शनि {second_sign} (जन्मकालीन द्वितीय भाव की राशि) में गोचर करे, "
                "धन, वाणी एवं पारिवारिक संक्रमण के विषय सक्रिय होते हैं। "
                "अनुशासित कर्म एवं आध्यात्मिक साधना अनुशंसित है।"
            ),
            "intensity": "high",
        })

    # 3. Saturn transiting natal 7th house sign → maraka (7th house) activation
    if seventh_sign:
        indicators.append({
            "planet_transit": "Saturn",
            "target_sign": seventh_sign,
            "target_house": 7,
            "significance_en": (
                f"Saturn transiting {seventh_sign} activates the 7th-house maraka theme. "
                "Partnership and relationship transitions become karmically prominent."
            ),
            "significance_hi": (
                f"शनि का {seventh_sign} में गोचर सप्तम भाव के मारक-विषय को जागृत करता है। "
                "साझेदारी एवं संबंध-संक्रमण कर्म की दृष्टि से महत्वपूर्ण हो जाते हैं।"
            ),
            "watch_period_en": (
                f"When Saturn transits {seventh_sign} (your natal 7th house sign), "
                "key relationship transitions and life-partnership themes are activated. "
                "This is a period for honest self-review and compassionate decision-making."
            ),
            "watch_period_hi": (
                f"जब शनि {seventh_sign} (जन्मकालीन सप्तम भाव की राशि) में गोचर करे, "
                "महत्वपूर्ण संबंध-संक्रमण एवं जीवन-साझेदारी के विषय सक्रिय होते हैं। "
                "यह ईमानदार आत्म-समीक्षा एवं करुणापूर्ण निर्णय का काल है।"
            ),
            "intensity": "high",
        })

    # 4. Jupiter transiting 8th house sign → spiritual support (moderate, supportive)
    if eighth_sign:
        indicators.append({
            "planet_transit": "Jupiter",
            "target_sign": eighth_sign,
            "target_house": 8,
            "significance_en": (
                f"Jupiter transiting {eighth_sign} brings spiritual guidance and wisdom "
                "during the 8th-house transformative period. A protective and illuminating transit."
            ),
            "significance_hi": (
                f"बृहस्पति का {eighth_sign} में गोचर अष्टम भाव के रूपांतरण-काल में "
                "आध्यात्मिक मार्गदर्शन एवं ज्ञान लाता है। यह एक सुरक्षात्मक एवं प्रकाशमान गोचर है।"
            ),
            "watch_period_en": (
                f"When Jupiter transits {eighth_sign} (8th house), spiritual awareness deepens "
                "and the transformative energies of this bhava are guided by wisdom and grace."
            ),
            "watch_period_hi": (
                f"जब बृहस्पति {eighth_sign} (अष्टम भाव) में गोचर करे, "
                "आध्यात्मिक जागरूकता गहरी होती है और इस भाव की रूपांतरणकारी ऊर्जाएं "
                "ज्ञान एवं अनुग्रह द्वारा निर्देशित होती हैं।"
            ),
            "intensity": "moderate",
        })

    # 5. Mars transiting natal 8th house sign → sudden challenges (moderate)
    if eighth_sign:
        indicators.append({
            "planet_transit": "Mars",
            "target_sign": eighth_sign,
            "target_house": 8,
            "significance_en": (
                f"Mars transiting {eighth_sign} can bring sudden health or vitality challenges. "
                "Increased care, rest, and avoidance of unnecessary risks is advised."
            ),
            "significance_hi": (
                f"मंगल का {eighth_sign} में गोचर अचानक स्वास्थ्य या जीवन-शक्ति की चुनौतियां ला सकता है। "
                "अधिक सावधानी, विश्राम एवं अनावश्यक जोखिम से बचने की सलाह है।"
            ),
            "watch_period_en": (
                f"When Mars transits {eighth_sign} (natal 8th house sign), "
                "a period of heightened sensitivity begins. Avoid reckless activity; "
                "prioritise health routines and grounding practices."
            ),
            "watch_period_hi": (
                f"जब मंगल {eighth_sign} (जन्मकालीन अष्टम भाव की राशि) में गोचर करे, "
                "बढ़ी संवेदनशीलता का काल प्रारम्भ होता है। लापरवाह गतिविधि से बचें; "
                "स्वास्थ्य-दिनचर्या एवं स्थिरता की साधनाओं को प्राथमिकता दें।"
            ),
            "intensity": "moderate",
        })

    # 6. Moon transiting natal maraka house each month → recurring monthly sensitivity (low)
    maraka_moon_sign = second_sign  # default to 2nd house sign for Moon sensitivity
    if maraka_moon_sign:
        indicators.append({
            "planet_transit": "Moon",
            "target_sign": maraka_moon_sign,
            "target_house": 2,
            "significance_en": (
                f"Each month when the Moon transits {maraka_moon_sign} (natal 2nd house), "
                "a brief but recurring sensitivity window opens around karmic/health themes."
            ),
            "significance_hi": (
                f"प्रत्येक माह जब चंद्रमा {maraka_moon_sign} (जन्मकालीन द्वितीय भाव) में गोचर करे, "
                "कर्म/स्वास्थ्य विषयों पर एक संक्षिप्त किंतु आवर्ती संवेदनशीलता-विंडो खुलती है।"
            ),
            "watch_period_en": (
                f"Monthly sensitivity: when the Moon transits {maraka_moon_sign}, "
                "pay attention to body signals, emotional states, and karmic patterns. "
                "This is a low-intensity but recurring check-in."
            ),
            "watch_period_hi": (
                f"मासिक संवेदनशीलता: जब चंद्रमा {maraka_moon_sign} में गोचर करे, "
                "शारीरिक संकेतों, भावनात्मक अवस्थाओं एवं कर्म-पैटर्न पर ध्यान दें। "
                "यह कम-तीव्रता वाली किंतु आवर्ती जांच है।"
            ),
            "intensity": "low",
        })

    # Summary
    summary_en = (
        "These transit indicators show WHEN natal longevity themes are activated by moving planets. "
        "High-intensity windows call for heightened spiritual practice; moderate periods ask for mindful "
        "awareness; low-intensity windows are gentle monthly reminders. "
        "No specific date predictions are intended — these are karmic timing windows, not prophecies."
    )
    summary_hi = (
        "ये गोचर-संकेतक दर्शाते हैं कि भ्रमणशील ग्रह जन्मकालीन आयु-विषयों को कब सक्रिय करते हैं। "
        "उच्च-तीव्रता विंडो में आध्यात्मिक साधना बढ़ाएं; मध्यम काल में सचेत जागरूकता रखें; "
        "निम्न-तीव्रता विंडो मासिक स्मरण हैं। "
        "कोई विशिष्ट तिथि-भविष्यवाणी अभिप्रेत नहीं — ये कर्म-काल के संकेत हैं, भविष्यवाणी नहीं।"
    )

    return {
        "indicators": indicators,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
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
# Dasha–Gochara multi-signal timing
# ───────────────────────────────────────────────────────────────

def _compute_triple_confluence(
    dasha_signal_count: int,
    lagna_affliction_count: int,
    natal_saturn_rahu_maraka: bool,
) -> Dict[str, Any]:
    """
    Score the three-way confluence per Phaladeepika Adh. 17.

    Returns: {confluence_level, active_signals, total_score, confluence_en, confluence_hi}
    """
    total: float = 0.0
    active_signals: List[str] = []

    if dasha_signal_count >= 1:
        total += 1
        active_signals.append("Dasha signal")
    if lagna_affliction_count >= 2:
        total += 1
        active_signals.append("Lagna affliction")
    elif lagna_affliction_count == 1:
        total += 0.5
        active_signals.append("Mild lagna affliction")
    if natal_saturn_rahu_maraka:
        total += 1
        active_signals.append("Saturn/Rahu in maraka position")

    if total >= 2.5:
        level = "critical"
        en = (
            "Triple-signal confluence detected (Phaladeepika Adh. 17): "
            f"Active signals: {', '.join(active_signals)}. "
            "When Dasha lord, natal Lagna affliction, AND Saturn/Rahu maraka position align, "
            "this marks the most karmically significant period for longevity themes. "
            "Intensive spiritual practice, health vigilance, and family awareness are advised."
        )
        hi = (
            "त्रि-संकेत संगम (फलदीपिका अ. 17): "
            f"सक्रिय संकेत: {', '.join(active_signals)}। "
            "दशा, लग्न-पीड़ा एवं शनि/राहु-मारक स्थिति का एकत्र संयोग "
            "आयु के दृष्टिकोण से सर्वाधिक महत्वपूर्ण काल को दर्शाता है। "
            "गहन आध्यात्मिक साधना, स्वास्थ्य सतर्कता एवं पारिवारिक जागरूकता अनुशंसित है।"
        )
    elif total >= 1.5:
        level = "elevated"
        en = (
            f"Two-signal alignment (Phaladeepika Adh. 17): {', '.join(active_signals)}. "
            "Partial karmic confluence — longevity themes are active. "
            "Protective practices and mindful living are beneficial."
        )
        hi = (
            f"द्वि-संकेत संरेखण (फलदीपिका अ. 17): {', '.join(active_signals)}। "
            "आंशिक कर्म-संगम — आयु के विषय सक्रिय हैं। "
            "सुरक्षात्मक उपाय एवं सचेत जीवन लाभदायक है।"
        )
    elif total >= 0.5:
        level = "moderate"
        en = (
            f"Single-signal presence: {', '.join(active_signals)}. "
            "One of three Phaladeepika Adh. 17 indicators is active — philosophical reflection is advised."
        )
        hi = (
            f"एकल संकेत उपस्थित: {', '.join(active_signals)}। "
            "तीन में से एक फलदीपिका अ. 17 संकेत सक्रिय है — आत्म-चिन्तन उचित है।"
        )
    else:
        level = "quiescent"
        en = "No strong confluence of longevity signals (Phaladeepika Adh. 17). Indicators are quiet."
        hi = "कोई प्रबल आयु-संकेत संगम नहीं (फलदीपिका अ. 17)। संकेत शान्त हैं।"

    return {
        "confluence_level": level,
        "active_signals": active_signals,
        "total_score": round(total, 1),
        "confluence_en": en,
        "confluence_hi": hi,
    }


def _dasha_gochara_timing(
    chart_data: Dict[str, Any],
    mahadasha_lord: Optional[str],
    antardasha_lord: Optional[str],
) -> Dict[str, Any]:
    """Check whether current dasha lords coincide with maraka/8th/lagna lords.

    Also computes triple-signal confluence (Dasha + Lagna affliction + Saturn/Rahu natal maraka).
    """
    maraka_2nd = _lord_of(2, chart_data)
    maraka_7th = _lord_of(7, chart_data)
    eighth_lord = _lord_of(8, chart_data)
    lagna_lord = _lord_of(1, chart_data)

    signals = []
    for dasha_label, lord in [("Mahadasha", mahadasha_lord), ("Antardasha", antardasha_lord)]:
        if not lord:
            continue
        if lord == maraka_2nd:
            signals.append({
                "dasha": dasha_label, "lord": lord, "role": "maraka_2nd",
                "en": f"{dasha_label} lord {lord} is the 2nd-house maraka — a classical karmic activator.",
                "hi": f"{dasha_label} स्वामी {lord} द्वितीयेश मारक है — शास्त्रीय दृष्टि से कर्म-संक्रमण का सूचक।",
            })
        if lord == maraka_7th:
            signals.append({
                "dasha": dasha_label, "lord": lord, "role": "maraka_7th",
                "en": f"{dasha_label} lord {lord} is the 7th-house maraka — brings transformation themes.",
                "hi": f"{dasha_label} स्वामी {lord} सप्तमेश मारक है — परिवर्तन की आंतरिक यात्रा का सूचक।",
            })
        if lord == eighth_lord:
            signals.append({
                "dasha": dasha_label, "lord": lord, "role": "eighth_lord",
                "en": f"{dasha_label} lord {lord} rules the 8th house — longevity bhava is activated.",
                "hi": f"{dasha_label} स्वामी {lord} अष्टमेश है — दीर्घायु भाव सक्रिय है।",
            })
        if lord == lagna_lord:
            signals.append({
                "dasha": dasha_label, "lord": lord, "role": "lagna_lord",
                "en": f"{dasha_label} lord {lord} is the lagna lord — overall vitality and body are in focus.",
                "hi": f"{dasha_label} स्वामी {lord} लग्नेश है — शरीर एवं जीवन-शक्ति केन्द्र में है।",
            })

    count = len(signals)
    if count >= 3:
        convergence = "high"
        summary_en = "Multiple dasha lords align with maraka/longevity indicators — a period of heightened karmic significance."
        summary_hi = "अनेक दशा-स्वामी मारक/दीर्घायु सूचकों से संरेखित हैं — यह काल कर्म-दृष्टि से अत्यन्त महत्त्वपूर्ण है।"
    elif count >= 1:
        convergence = "moderate"
        summary_en = "Current dasha period shows partial alignment with longevity indicators — philosophical reflection is advised."
        summary_hi = "वर्तमान दशाकाल में आंशिक कर्म-संरेखण दिखता है — आत्म-चिन्तन उचित है।"
    else:
        convergence = "low"
        summary_en = "Current dasha lords are not classical maraka or 8th-house lords — longevity indicators are quiescent."
        summary_hi = "वर्तमान दशा-स्वामी शास्त्रीय मारक या अष्टमेश नहीं हैं — दीर्घायु-सूचक शान्त हैं।"

    # ── Signal 2: Lagna natal affliction ──────────────────────────
    malefics_in_lagna_axis = 0
    for house_check in [1, 7, 8]:
        house_malefics = [
            p for p in ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]
            if _planet_house(p, chart_data) == house_check
        ]
        malefics_in_lagna_axis += len(house_malefics)

    # Lagna lord in dusthana or debilitated?
    if lagna_lord:
        ll_house = _planet_house(lagna_lord, chart_data)
        ll_sign = _planet_sign(lagna_lord, chart_data)
        if ll_house in DUSTHANAS:
            malefics_in_lagna_axis += 1
        _DEBIL = {
            "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
            "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
        }
        if ll_sign and _DEBIL.get(lagna_lord) == ll_sign:
            malefics_in_lagna_axis += 1

    # ── Signal 3: Saturn/Rahu in natal maraka position ────────────
    sat_house = _planet_house("Saturn", chart_data)
    rahu_house = _planet_house("Rahu", chart_data)
    saturn_rahu_maraka = sat_house in {2, 7, 8} or rahu_house in {2, 7, 8}

    # ── Triple confluence ──────────────────────────────────────────
    confluence = _compute_triple_confluence(count, malefics_in_lagna_axis, saturn_rahu_maraka)

    return {
        "signals": signals,
        "convergence": convergence,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "mahadasha_lord": mahadasha_lord,
        "antardasha_lord": antardasha_lord,
        "lagna_affliction_count": malefics_in_lagna_axis,
        "saturn_rahu_in_maraka": saturn_rahu_maraka,
        "confluence": confluence,
    }


# ───────────────────────────────────────────────────────────────
# Month and Lagna of demise — Adh. 17 Nakshatra/Tithi Method
# ───────────────────────────────────────────────────────────────

def _demise_month_lagna_indicators(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phaladeepika Adh. 17 — indicators for the probable month, sign, and
    nakshatra period during which longevity themes peak.

    Method:
      1. Month indicator: Sun transiting the sign of the 8th lord, OR the
         sign of the 2nd/7th maraka lord (classical month-of-transition).
      2. Rising sign at a critical transition: typically the 8th house sign
         from lagna, or the sign where natal Saturn is placed.
      3. Nakshatra period: nakshatra associated with the Moon's 22nd nakshatra
         (Vainashika nakshatra = 22nd from natal Moon nakshatra).
    """
    _SIGN_MONTHS_EN = {
        "Aries": "mid-March to mid-April (Chaitra)",
        "Taurus": "mid-April to mid-May (Vaishakha)",
        "Gemini": "mid-May to mid-June (Jyeshtha)",
        "Cancer": "mid-June to mid-July (Ashadha)",
        "Leo": "mid-July to mid-August (Shravana)",
        "Virgo": "mid-August to mid-September (Bhadrapada)",
        "Libra": "mid-September to mid-October (Ashwina)",
        "Scorpio": "mid-October to mid-November (Kartika)",
        "Sagittarius": "mid-November to mid-December (Margashirsha)",
        "Capricorn": "mid-December to mid-January (Pausha)",
        "Aquarius": "mid-January to mid-February (Magha)",
        "Pisces": "mid-February to mid-March (Phalguna)",
    }
    _SIGN_MONTHS_HI = {
        "Aries": "मध्य-मार्च से मध्य-अप्रैल (चैत्र)",
        "Taurus": "मध्य-अप्रैल से मध्य-मई (वैशाख)",
        "Gemini": "मध्य-मई से मध्य-जून (ज्येष्ठ)",
        "Cancer": "मध्य-जून से मध्य-जुलाई (आषाढ़)",
        "Leo": "मध्य-जुलाई से मध्य-अगस्त (श्रावण)",
        "Virgo": "मध्य-अगस्त से मध्य-सितंबर (भाद्रपद)",
        "Libra": "मध्य-सितंबर से मध्य-अक्टूबर (आश्विन)",
        "Scorpio": "मध्य-अक्टूबर से मध्य-नवंबर (कार्तिक)",
        "Sagittarius": "मध्य-नवंबर से मध्य-दिसंबर (मार्गशीर्ष)",
        "Capricorn": "मध्य-दिसंबर से मध्य-जनवरी (पौष)",
        "Aquarius": "मध्य-जनवरी से मध्य-फरवरी (माघ)",
        "Pisces": "मध्य-फरवरी से मध्य-मार्च (फाल्गुन)",
    }

    asc = _asc_sign(chart_data)

    # 1. Month indicator: Sun transiting 8th lord's sign OR maraka lord signs
    eighth_lord = _lord_of(8, chart_data)
    maraka_2nd_lord = _lord_of(2, chart_data)
    maraka_7th_lord = _lord_of(7, chart_data)

    eighth_lord_sign = _planet_sign(eighth_lord, chart_data) if eighth_lord else ""
    maraka_2nd_sign = _planet_sign(maraka_2nd_lord, chart_data) if maraka_2nd_lord else ""
    maraka_7th_sign = _planet_sign(maraka_7th_lord, chart_data) if maraka_7th_lord else ""

    month_indicators: List[Dict[str, Any]] = []
    if eighth_lord_sign:
        month_en = _SIGN_MONTHS_EN.get(eighth_lord_sign, eighth_lord_sign)
        month_hi = _SIGN_MONTHS_HI.get(eighth_lord_sign, eighth_lord_sign)
        month_indicators.append({
            "trigger": f"Sun transiting {eighth_lord_sign} (natal sign of 8th lord {eighth_lord})",
            "trigger_hi": f"सूर्य का {eighth_lord_sign} में गोचर (अष्टमेश {eighth_lord} की जन्मकालीन राशि)",
            "period_en": month_en,
            "period_hi": month_hi,
            "intensity": "high",
            "note_en": "Phaladeepika Adh. 17: Sun transiting the sign of the 8th lord activates the longevity axis.",
            "note_hi": "फलदीपिका अ. 17: सूर्य का अष्टमेश की राशि में गोचर आयु-अक्ष को सक्रिय करता है।",
        })
    if maraka_2nd_sign and maraka_2nd_sign != eighth_lord_sign:
        month_en2 = _SIGN_MONTHS_EN.get(maraka_2nd_sign, maraka_2nd_sign)
        month_hi2 = _SIGN_MONTHS_HI.get(maraka_2nd_sign, maraka_2nd_sign)
        month_indicators.append({
            "trigger": f"Sun transiting {maraka_2nd_sign} (natal sign of 2nd maraka lord {maraka_2nd_lord})",
            "trigger_hi": f"सूर्य का {maraka_2nd_sign} में गोचर (2nd मारकेश {maraka_2nd_lord} की राशि)",
            "period_en": month_en2,
            "period_hi": month_hi2,
            "intensity": "moderate",
            "note_en": "2nd lord maraka activation.",
            "note_hi": "द्वितीयेश मारक सक्रियण।",
        })
    if maraka_7th_sign and maraka_7th_sign not in {eighth_lord_sign, maraka_2nd_sign}:
        month_en3 = _SIGN_MONTHS_EN.get(maraka_7th_sign, maraka_7th_sign)
        month_hi3 = _SIGN_MONTHS_HI.get(maraka_7th_sign, maraka_7th_sign)
        month_indicators.append({
            "trigger": f"Sun transiting {maraka_7th_sign} (natal sign of 7th maraka lord {maraka_7th_lord})",
            "trigger_hi": f"सूर्य का {maraka_7th_sign} में गोचर (7th मारकेश {maraka_7th_lord} की राशि)",
            "period_en": month_en3,
            "period_hi": month_hi3,
            "intensity": "moderate",
            "note_en": "7th lord maraka activation.",
            "note_hi": "सप्तमेश मारक सक्रियण।",
        })

    # 2. Rising sign at critical transition = 8th house sign from lagna
    eighth_house_sign = _sign_of_house_nidhana(8, asc) if asc else ""
    saturn_sign = _planet_sign("Saturn", chart_data)

    rising_sign_en = ""
    rising_sign_hi = ""
    if eighth_house_sign:
        rising_sign_en = (
            f"The 8th house sign ({eighth_house_sign}) from lagna is classically associated "
            f"with the ascending sign during critical karmic transitions. "
            f"Additionally, Saturn's natal sign ({saturn_sign}) is another traditional indicator. "
            f"Phaladeepika Adh. 17: these signs mark periods of heightened longevity awareness."
        )
        rising_sign_hi = (
            f"लग्न से अष्टम भाव की राशि ({eighth_house_sign}) शास्त्रीय दृष्टि से "
            f"महत्वपूर्ण कर्म-संक्रमण के समय उदित राशि से सम्बद्ध है। "
            f"इसके अतिरिक्त शनि की जन्मकालीन राशि ({saturn_sign}) भी परम्परागत संकेतक है। "
            f"फलदीपिका अ. 17: ये राशियाँ आयु-जागरूकता के ऊँचे काल का संकेत देती हैं।"
        )

    # 3. Vainashika nakshatra (22nd from natal Moon nakshatra)
    _NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
    ]

    # Support both chart_data["moon_nakshatra"] and chart_data["planets"]["Moon"]["nakshatra"]
    moon_nak = ""
    moon_nak_top = chart_data.get("moon_nakshatra")
    if isinstance(moon_nak_top, str):
        moon_nak = moon_nak_top
    elif isinstance(moon_nak_top, dict):
        moon_nak = str(moon_nak_top.get("nakshatra", "") or "")
    else:
        moon_planet = (_planets(chart_data).get("Moon") or {})
        if isinstance(moon_planet, dict):
            moon_nak = str(moon_planet.get("nakshatra", "") or "")

    vainashika_nak = ""
    vainashika_en = ""
    vainashika_hi = ""
    if moon_nak in _NAKSHATRAS:
        moon_idx = _NAKSHATRAS.index(moon_nak)
        vainashika_idx = (moon_idx + 21) % 27  # 22nd from Moon = +21 (0-indexed)
        vainashika_nak = _NAKSHATRAS[vainashika_idx]
        vainashika_en = (
            f"Vainashika (22nd) Nakshatra from natal Moon ({moon_nak}): {vainashika_nak}. "
            f"Phaladeepika Adh. 17: the dasha of the lord of {vainashika_nak} nakshatra "
            f"is considered karmically significant for longevity themes. "
            f"Lord of {vainashika_nak}: used in conjunction with maraka dasha for timing."
        )
        vainashika_hi = (
            f"जन्मकालीन चंद्र नक्षत्र ({moon_nak}) से 22वाँ नक्षत्र (वैनाशिक): {vainashika_nak}। "
            f"फलदीपिका अ. 17: {vainashika_nak} नक्षत्र के स्वामी की दशा "
            f"आयु के दृष्टिकोण से कर्म-महत्वपूर्ण मानी जाती है। "
            f"मारक दशा के साथ {vainashika_nak} के स्वामी की दशा का मेल विशेष ध्यान देने योग्य है।"
        )

    disclaimer_en = (
        "These indicators follow Phaladeepika Adhyaya 17 classical methods. "
        "They identify POTENTIAL periods of heightened karmic significance — NOT specific death predictions. "
        "These are tools for spiritual preparedness and health awareness. "
        "Consult a qualified Jyotishi for confirmation."
    )
    disclaimer_hi = (
        "ये संकेत फलदीपिका अ. 17 की शास्त्रीय पद्धतियों पर आधारित हैं। "
        "ये किसी विशेष मृत्यु-तिथि की भविष्यवाणी नहीं — केवल कर्मिक दृष्टि से महत्वपूर्ण "
        "संभावित कालों के संकेत हैं। पुष्टि के लिए योग्य ज्योतिषी से परामर्श करें।"
    )

    return {
        "month_indicators": month_indicators,
        "rising_sign_indicators": {
            "eighth_house_sign": eighth_house_sign,
            "saturn_natal_sign": saturn_sign,
            "interpretation_en": rising_sign_en,
            "interpretation_hi": rising_sign_hi,
        },
        "vainashika_nakshatra": {
            "moon_nakshatra": moon_nak,
            "vainashika_nak": vainashika_nak,
            "interpretation_en": vainashika_en,
            "interpretation_hi": vainashika_hi,
        },
        "disclaimer_en": disclaimer_en,
        "disclaimer_hi": disclaimer_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


# ───────────────────────────────────────────────────────────────
# Feature 1: Saturn Transit Death Indicator (Adhyaya 17)
# ───────────────────────────────────────────────────────────────

_NAKSHATRA_LORD: Dict[str, str] = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun", "Rohini": "Moon",
    "Mrigashira": "Mars", "Ardra": "Rahu", "Punarvasu": "Jupiter", "Pushya": "Saturn",
    "Ashlesha": "Mercury", "Magha": "Ketu", "Purva Phalguni": "Venus",
    "Uttara Phalguni": "Sun", "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
    "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
    "Mula": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
    "Shravana": "Moon", "Dhanishtha": "Mars", "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury",
}

_NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]


def _saturn_transit_death_indicator(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 1: Saturn transit death timing per Phaladeepika Adhyaya 17.

    Rule: Saturn transiting 8th from natal Moon OR the sign of the 8th lord
    indicates heightened karmic vulnerability when combined with Maraka dasha.
    """
    # Determine Saturn's natal house from Moon
    moon_house = _planet_house("Moon", chart_data)
    saturn_house = _planet_house("Saturn", chart_data)
    saturn_sign = _planet_sign("Saturn", chart_data)

    # 8th from Moon (house counting from Moon's position)
    eighth_from_moon = 0
    if moon_house > 0 and saturn_house > 0:
        eighth_from_moon = ((moon_house - 1 + 7) % 12) + 1  # 8th from Moon

    is_8th_from_moon = (saturn_house == eighth_from_moon) if eighth_from_moon > 0 else False

    # Saturn transiting 8th lord's sign
    eighth_lord = _lord_of(8, chart_data)
    eighth_lord_sign = _planet_sign(eighth_lord, chart_data) if eighth_lord else ""
    saturn_8th_lord_transit = bool(saturn_sign and eighth_lord_sign and saturn_sign == eighth_lord_sign)

    # Current house of Saturn from Moon (gochara approximation using natal)
    current_saturn_house_from_moon = 0
    if moon_house > 0 and saturn_house > 0:
        current_saturn_house_from_moon = ((saturn_house - moon_house) % 12) + 1

    # Severity
    if is_8th_from_moon and saturn_8th_lord_transit:
        severity = "high"
        interp_en = (
            f"Saturn occupies the 8th house from natal Moon (house {eighth_from_moon}) AND "
            f"transits the sign of the 8th lord ({eighth_lord}, {eighth_lord_sign}). "
            "Phaladeepika Adh. 17: double activation — this is the most significant karmic vigilance period. "
            "Combine with Maraka dasha for timing. Spiritual practice and health awareness are strongly advised."
        )
        interp_hi = (
            f"शनि जन्मकालीन चंद्र से अष्टम भाव (भाव {eighth_from_moon}) में है "
            f"और अष्टमेश ({eighth_lord}, {eighth_lord_sign}) की राशि में भी है। "
            "फलदीपिका अ. 17: दोहरा सक्रियण — यह सर्वाधिक कर्म-सतर्कता का काल है। "
            "मारक दशा के साथ मिलाकर देखें। आध्यात्मिक साधना एवं स्वास्थ्य-जागरूकता अत्यंत आवश्यक।"
        )
    elif is_8th_from_moon:
        severity = "high"
        interp_en = (
            f"Saturn is placed in the 8th house from natal Moon (house {eighth_from_moon}). "
            "Phaladeepika Adh. 17: Saturn transiting the 8th from Moon is the primary death-timing indicator. "
            "If you are also in a Maraka dasha, heightened awareness and protective practices are advised."
        )
        interp_hi = (
            f"शनि जन्मकालीन चंद्र से अष्टम भाव (भाव {eighth_from_moon}) में स्थित है। "
            "फलदीपिका अ. 17: चंद्र से 8वें भाव में शनि प्राथमिक निधन-काल संकेत है। "
            "यदि मारक दशा भी चल रही है, तो बढ़ी जागरूकता एवं सुरक्षात्मक उपाय अनुशंसित हैं।"
        )
    elif saturn_8th_lord_transit:
        severity = "moderate"
        interp_en = (
            f"Saturn transits the sign of the 8th lord ({eighth_lord} in {eighth_lord_sign}). "
            "Phaladeepika Adh. 17: this activates the longevity axis via the 8th lord's sign. "
            "A period of philosophical reflection and health mindfulness is appropriate."
        )
        interp_hi = (
            f"शनि अष्टमेश ({eighth_lord}) की राशि ({eighth_lord_sign}) में गोचर कर रहा है। "
            "फलदीपिका अ. 17: यह अष्टमेश की राशि के माध्यम से आयु-अक्ष को सक्रिय करता है। "
            "दार्शनिक चिन्तन एवं स्वास्थ्य-सतर्कता का काल है।"
        )
    else:
        severity = "low"
        interp_en = (
            f"Saturn (house {saturn_house}, {saturn_sign}) is not currently in the 8th from Moon "
            f"(house {eighth_from_moon}) nor in the 8th lord's sign ({eighth_lord_sign or 'unknown'}). "
            "Phaladeepika Adh. 17: Saturn transit death indicators are quiescent at this placement."
        )
        interp_hi = (
            f"शनि (भाव {saturn_house}, {saturn_sign}) वर्तमान में चंद्र से 8वें भाव "
            f"(भाव {eighth_from_moon}) या अष्टमेश की राशि ({eighth_lord_sign or 'अज्ञात'}) में नहीं है। "
            "फलदीपिका अ. 17: इस स्थिति में शनि गोचर निधन-संकेत शान्त हैं।"
        )

    return {
        "current_saturn_house_from_moon": current_saturn_house_from_moon,
        "is_8th_from_moon": is_8th_from_moon,
        "saturn_8th_lord_transit": saturn_8th_lord_transit,
        "eighth_lord": eighth_lord,
        "eighth_lord_sign": eighth_lord_sign,
        "moon_house": moon_house,
        "saturn_house": saturn_house,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
        "severity": severity,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


# ───────────────────────────────────────────────────────────────
# Feature 2: Moon Transit at Death (Adhyaya 17)
# ───────────────────────────────────────────────────────────────

def _moon_death_transit(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 2: Moon transiting Janma Nakshatra during Maraka dasha = critical vulnerability.
    Classical rule per Phaladeepika Adh. 17.
    """
    # Extract Janma Nakshatra
    moon_nak = ""
    moon_nak_top = chart_data.get("moon_nakshatra")
    if isinstance(moon_nak_top, str):
        moon_nak = moon_nak_top
    elif isinstance(moon_nak_top, dict):
        moon_nak = str(moon_nak_top.get("nakshatra", "") or "")
    else:
        moon_planet = (_planets(chart_data).get("Moon") or {})
        if isinstance(moon_planet, dict):
            moon_nak = str(moon_planet.get("nakshatra", "") or "")

    if not moon_nak:
        return {
            "janma_nakshatra": "",
            "watch_for_en": "Janma Nakshatra not available in chart data.",
            "watch_for_hi": "जन्म नक्षत्र कुंडली डेटा में उपलब्ध नहीं है।",
            "note_en": "Provide Moon nakshatra for this analysis.",
            "note_hi": "इस विश्लेषण के लिए चंद्र नक्षत्र प्रदान करें।",
            "sloka_ref": "Phaladeepika Adh. 17",
        }

    # Maraka lords for reference
    maraka_2nd = _lord_of(2, chart_data)
    maraka_7th = _lord_of(7, chart_data)
    maraka_str = f"{maraka_2nd} or {maraka_7th}" if maraka_2nd and maraka_7th else (maraka_2nd or maraka_7th or "Maraka lord")

    watch_en = (
        f"Each month when the Moon returns to {moon_nak} (your Janma Nakshatra), "
        f"watch carefully if you are simultaneously running a Maraka dasha "
        f"({maraka_str} Mahadasha or Antardasha). "
        "Phaladeepika Adh. 17: Moon transiting Janma Nakshatra during Maraka dasha "
        "is the classical critical vulnerability window. "
        "This is a 2–3 day window of heightened spiritual awareness — not a death prediction."
    )
    watch_hi = (
        f"प्रत्येक माह जब चंद्रमा {moon_nak} (आपके जन्म नक्षत्र) में लौटे, "
        f"तब विशेष ध्यान दें यदि आप उसी समय मारक दशा ({maraka_str} महादशा या अन्तर्दशा) में हों। "
        "फलदीपिका अ. 17: मारक दशा के दौरान जन्म नक्षत्र पर चंद्र गोचर "
        "शास्त्रीय दृष्टि से अत्यंत संवेदनशील काल है। "
        "यह 2-3 दिन की आध्यात्मिक जागरूकता की विंडो है — मृत्यु की भविष्यवाणी नहीं।"
    )
    note_en = (
        "Classical guidance: during this window, intensify spiritual practice, avoid risky activities, "
        "and perform protective rituals (mantra, charity). The window recurs monthly but is significant "
        "only during active Maraka dasha periods."
    )
    note_hi = (
        "शास्त्रीय परामर्श: इस विंडो में आध्यात्मिक साधना बढ़ाएं, जोखिम भरी गतिविधियों से बचें "
        "और सुरक्षात्मक अनुष्ठान (मंत्र, दान) करें। यह विंडो मासिक आती है किन्तु सक्रिय "
        "मारक दशाकाल में ही महत्वपूर्ण होती है।"
    )

    return {
        "janma_nakshatra": moon_nak,
        "watch_for_en": watch_en,
        "watch_for_hi": watch_hi,
        "note_en": note_en,
        "note_hi": note_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


# ───────────────────────────────────────────────────────────────
# Feature 3: Month & Lagna of Demise — Classical Estimation (Adh. 17)
# ───────────────────────────────────────────────────────────────

_SIGN_CALENDAR_MONTH_EN = {
    "Aries": "April", "Taurus": "May", "Gemini": "June", "Cancer": "July",
    "Leo": "August", "Virgo": "September", "Libra": "October", "Scorpio": "November",
    "Sagittarius": "December", "Capricorn": "January", "Aquarius": "February", "Pisces": "March",
}
_SIGN_CALENDAR_MONTH_HI = {
    "Aries": "अप्रैल", "Taurus": "मई", "Gemini": "जून", "Cancer": "जुलाई",
    "Leo": "अगस्त", "Virgo": "सितंबर", "Libra": "अक्टूबर", "Scorpio": "नवंबर",
    "Sagittarius": "दिसंबर", "Capricorn": "जनवरी", "Aquarius": "फरवरी", "Pisces": "मार्च",
}


def _demise_timing_classical(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Feature 3: Classical Month & Lagna of Demise estimation (Phaladeepika Adh. 17).

    Month of death: sign of stronger Maraka lord (2nd or 7th lord).
    Lagna at death: sign occupied by the 8th lord natally.
    """
    maraka_2nd = _lord_of(2, chart_data)
    maraka_7th = _lord_of(7, chart_data)
    eighth_lord = _lord_of(8, chart_data)

    # Determine stronger Maraka
    m2_sign = _planet_sign(maraka_2nd, chart_data) if maraka_2nd else ""
    m7_sign = _planet_sign(maraka_7th, chart_data) if maraka_7th else ""
    m2_house = _planet_house(maraka_2nd, chart_data) if maraka_2nd else 0
    m7_house = _planet_house(maraka_7th, chart_data) if maraka_7th else 0

    # Simple strength: Kendra/Trikona > Dusthana
    def _maraka_score(house: int) -> int:
        if house in KENDRAS:
            return 3
        if house in TRIKONAS:
            return 2
        if house in DUSTHANAS:
            return 0
        return 1

    m2_score = _maraka_score(m2_house)
    m7_score = _maraka_score(m7_house)

    if m2_score >= m7_score and m2_sign:
        stronger_sign = m2_sign
        stronger_planet = maraka_2nd
        reason_en = f"2nd lord ({maraka_2nd}) is the stronger Maraka (house {m2_house}, score {m2_score})"
        reason_hi = f"द्वितीयेश ({maraka_2nd}) प्रबल मारक है (भाव {m2_house}, अंक {m2_score})"
    elif m7_sign:
        stronger_sign = m7_sign
        stronger_planet = maraka_7th
        reason_en = f"7th lord ({maraka_7th}) is the stronger Maraka (house {m7_house}, score {m7_score})"
        reason_hi = f"सप्तमेश ({maraka_7th}) प्रबल मारक है (भाव {m7_house}, अंक {m7_score})"
    else:
        stronger_sign = ""
        stronger_planet = ""
        reason_en = "Maraka lords not determinable"
        reason_hi = "मारक स्वामी निर्धारित नहीं"

    month_en = _SIGN_CALENDAR_MONTH_EN.get(stronger_sign, stronger_sign) if stronger_sign else "Unknown"
    month_hi = _SIGN_CALENDAR_MONTH_HI.get(stronger_sign, stronger_sign) if stronger_sign else "अज्ञात"

    # Lagna at death = sign of 8th lord natally
    eighth_lord_sign = _planet_sign(eighth_lord, chart_data) if eighth_lord else ""
    lagna_reason_en = (
        f"The 8th lord ({eighth_lord}) is natally placed in {eighth_lord_sign}. "
        "Phaladeepika Adh. 17: the sign occupied by the 8th lord is the classical indicator "
        "for the rising sign (Lagna) at the time of critical karmic transition."
    ) if eighth_lord_sign else "8th lord sign not determinable."
    lagna_reason_hi = (
        f"अष्टमेश ({eighth_lord}) जन्मकालीन {eighth_lord_sign} में स्थित है। "
        "फलदीपिका अ. 17: अष्टमेश की राशि महत्वपूर्ण कर्म-संक्रमण के समय उदित लग्न का शास्त्रीय संकेतक है।"
    ) if eighth_lord_sign else "अष्टमेश राशि निर्धारित नहीं।"

    disclaimer_en = (
        "IMPORTANT DISCLAIMER: This is a purely classical Phaladeepika Adhyaya 17 estimation method. "
        "It does NOT predict a specific death date or month. These signs indicate general karmic sensitivity "
        "periods — not absolute prophesies. Always consult a qualified Jyotishi for personal guidance."
    )
    disclaimer_hi = (
        "महत्वपूर्ण अस्वीकरण: यह केवल शास्त्रीय फलदीपिका अ. 17 की अनुमान पद्धति है। "
        "यह किसी विशेष मृत्यु-तिथि या माह की भविष्यवाणी नहीं है। ये राशियाँ सामान्य कर्म-संवेदनशीलता "
        "के काल को दर्शाती हैं — निरपेक्ष भविष्यवाणी नहीं। व्यक्तिगत मार्गदर्शन के लिए "
        "योग्य ज्योतिषी से परामर्श करें।"
    )

    return {
        "likely_month_indicator": {
            "sign": stronger_sign,
            "month_name_en": month_en,
            "month_name_hi": month_hi,
            "planet": stronger_planet,
            "reason_en": reason_en,
            "reason_hi": reason_hi,
        },
        "likely_lagna_at_death": {
            "sign": eighth_lord_sign,
            "reason_en": lagna_reason_en,
            "reason_hi": lagna_reason_hi,
        },
        "disclaimer_en": disclaimer_en,
        "disclaimer_hi": disclaimer_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


# ───────────────────────────────────────────────────────────────
# Feature 4: Dasha + Gochara + Lagna Combined Death Score (Adh. 17)
# ───────────────────────────────────────────────────────────────

def _dasha_gochara_lagna_score(
    chart_data: Dict[str, Any],
    mahadasha_lord: Optional[str] = None,
    antardasha_lord: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Feature 4: 5-signal multi-scoring system for death risk per Phaladeepika Adh. 17.

    Signal 1: Maraka dasha/antardasha active (+3)
    Signal 2: Saturn in 8th from Moon (+2)
    Signal 3: Jupiter NOT in good transit houses 2,5,7,9,11 (+1)
    Signal 4: 8th lord active in Gochara — here approximated by 8th lord in maraka/8th house (+1)
    Signal 5: Lagna lord weak in transit — approximated by lagna lord in Dusthana (+1)

    Score 0-2 = low concern, 3-5 = moderate watch, 6+ = high vigilance
    """
    maraka_2nd = _lord_of(2, chart_data)
    maraka_7th = _lord_of(7, chart_data)
    eighth_lord = _lord_of(8, chart_data)
    lagna_lord = _lord_of(1, chart_data)

    signals: List[Dict[str, Any]] = []
    total = 0

    # Signal 1: Maraka dasha/antardasha active
    in_maraka_dasha = bool(
        (mahadasha_lord and mahadasha_lord in {maraka_2nd, maraka_7th}) or
        (antardasha_lord and antardasha_lord in {maraka_2nd, maraka_7th})
    )
    s1_pts = 3 if in_maraka_dasha else 0
    total += s1_pts
    dasha_who = mahadasha_lord or antardasha_lord or "Unknown"
    signals.append({
        "signal_en": f"Maraka dasha/antardasha active ({dasha_who})",
        "signal_hi": f"मारक दशा/अन्तर्दशा सक्रिय ({dasha_who})",
        "points": 3,
        "triggered": in_maraka_dasha,
    })

    # Signal 2: Saturn in 8th from Moon
    moon_house = _planet_house("Moon", chart_data)
    saturn_house = _planet_house("Saturn", chart_data)
    eighth_from_moon = ((moon_house - 1 + 7) % 12) + 1 if moon_house > 0 else 0
    sat_8th_moon = (saturn_house == eighth_from_moon) if (moon_house > 0 and saturn_house > 0) else False
    s2_pts = 2 if sat_8th_moon else 0
    total += s2_pts
    signals.append({
        "signal_en": f"Saturn in 8th from Moon (house {eighth_from_moon})",
        "signal_hi": f"शनि चंद्र से अष्टम भाव में (भाव {eighth_from_moon})",
        "points": 2,
        "triggered": sat_8th_moon,
    })

    # Signal 3: Jupiter NOT in good transit houses (2,5,7,9,11)
    jup_house = _planet_house("Jupiter", chart_data)
    good_jupiter_houses = {2, 5, 7, 9, 11}
    jup_not_good = (jup_house > 0) and (jup_house not in good_jupiter_houses)
    s3_pts = 1 if jup_not_good else 0
    total += s3_pts
    signals.append({
        "signal_en": f"Jupiter not in auspicious transit houses 2/5/7/9/11 (currently house {jup_house})",
        "signal_hi": f"बृहस्पति शुभ गोचर भावों 2/5/7/9/11 में नहीं (वर्तमान भाव {jup_house})",
        "points": 1,
        "triggered": jup_not_good,
    })

    # Signal 4: 8th lord in maraka/8th house (proxy for Gochara activation)
    el_house = _planet_house(eighth_lord, chart_data) if eighth_lord else 0
    eighth_lord_active = el_house in {2, 7, 8} if el_house > 0 else False
    s4_pts = 1 if eighth_lord_active else 0
    total += s4_pts
    signals.append({
        "signal_en": f"8th lord ({eighth_lord}) active in maraka/8th zone (house {el_house})",
        "signal_hi": f"अष्टमेश ({eighth_lord}) मारक/अष्टम क्षेत्र में सक्रिय (भाव {el_house})",
        "points": 1,
        "triggered": eighth_lord_active,
    })

    # Signal 5: Lagna lord weak (Dusthana placement)
    ll_house = _planet_house(lagna_lord, chart_data) if lagna_lord else 0
    ll_sign = _planet_sign(lagna_lord, chart_data) if lagna_lord else ""
    ll_weak = (ll_house in DUSTHANAS) or (DEBILITATION.get(lagna_lord, "") == ll_sign if lagna_lord else False)
    s5_pts = 1 if ll_weak else 0
    total += s5_pts
    signals.append({
        "signal_en": f"Lagna lord ({lagna_lord}) weak — house {ll_house}, sign {ll_sign}",
        "signal_hi": f"लग्नेश ({lagna_lord}) दुर्बल — भाव {ll_house}, राशि {ll_sign}",
        "points": 1,
        "triggered": ll_weak,
    })

    # Verdict
    if total >= 6:
        verdict_en = (
            f"HIGH VIGILANCE PERIOD (score {total}/8): Multiple death-timing signals are simultaneously active. "
            "Phaladeepika Adh. 17: this is the most karmically sensitive configuration. "
            "Intensive spiritual practice, medical check-up, and family awareness are strongly advised. "
            "This is philosophical guidance — NOT a death prediction."
        )
        verdict_hi = (
            f"उच्च सतर्कता काल (अंक {total}/8): अनेक निधन-काल संकेत एक साथ सक्रिय हैं। "
            "फलदीपिका अ. 17: यह सर्वाधिक कर्म-संवेदनशील संरचना है। "
            "गहन आध्यात्मिक साधना, स्वास्थ्य जांच एवं पारिवारिक सतर्कता अत्यंत अनुशंसित। "
            "यह दार्शनिक मार्गदर्शन है — मृत्यु-भविष्यवाणी नहीं।"
        )
    elif total >= 3:
        verdict_en = (
            f"MODERATE WATCH (score {total}/8): Several signals are active. "
            "Phaladeepika Adh. 17 counsels heightened awareness and protective practices. "
            "Philosophical framing: this is a period calling for greater mindfulness. "
            "Not a crisis, but a time for intentional living."
        )
        verdict_hi = (
            f"मध्यम सतर्कता (अंक {total}/8): कई संकेत सक्रिय हैं। "
            "फलदीपिका अ. 17: बढ़ी जागरूकता एवं सुरक्षात्मक उपाय अनुशंसित। "
            "दार्शनिक दृष्टिकोण: यह अधिक सचेत जीवन का काल है। "
            "संकट नहीं, बल्कि सोद्देश्य जीवन जीने का समय।"
        )
    else:
        verdict_en = (
            f"LOW CONCERN (score {total}/8): Most death-timing signals are quiet. "
            "Phaladeepika Adh. 17 indicators are not aligned for heightened vulnerability. "
            "Routine spiritual practice and good health habits are sufficient."
        )
        verdict_hi = (
            f"निम्न चिंता (अंक {total}/8): अधिकांश निधन-काल संकेत शान्त हैं। "
            "फलदीपिका अ. 17 के संकेतक उच्च संवेदनशीलता के लिए संरेखित नहीं हैं। "
            "नियमित आध्यात्मिक साधना एवं स्वास्थ्य-आदतें पर्याप्त हैं।"
        )

    disclaimer_en = (
        "This scoring system follows Phaladeepika Adhyaya 17 classical multi-signal analysis. "
        "It is a philosophical longevity assessment tool — NOT a medical diagnosis or death prediction. "
        "Consult qualified medical and Jyotish practitioners for personal guidance."
    )

    return {
        "total": total,
        "signals": signals,
        "verdict_en": verdict_en,
        "verdict_hi": verdict_hi,
        "disclaimer_en": disclaimer_en,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


# ───────────────────────────────────────────────────────────────
# Feature 6: Best Lucky Time Estimation (Adhyaya 13)
# ───────────────────────────────────────────────────────────────

# Classical Dasha years for each planet (Vimshottari)
_DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
_DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Jupiter's exaltation / own signs (for transit bonus)
_JUPITER_EXCELLENT = {"Cancer", "Sagittarius", "Pisces"}  # exaltation + own signs


def _calculate_lucky_periods(
    chart_data: Dict[str, Any],
    mahadasha_lord: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Feature 6: Best Lucky Time Estimation per Phaladeepika Adhyaya 13.

    Identifies peak fortune periods by combining:
    1. 9th lord dasha/antardasha periods
    2. Jupiter transit in exaltation/own sign periods
    3. Raj yoga fruition dasha (if any Raj yogas exist via well-placed 9th lord)
    """
    asc = _asc_sign(chart_data)
    ninth_lord = _lord_of(9, chart_data)
    fifth_lord = _lord_of(5, chart_data)
    lagna_lord = _lord_of(1, chart_data)
    jupiter_sign = _planet_sign("Jupiter", chart_data)
    jupiter_house = _planet_house("Jupiter", chart_data)

    peak_periods: List[Dict[str, Any]] = []

    # Period 1: 9th lord Mahadasha
    if ninth_lord:
        nl_house = _planet_house(ninth_lord, chart_data)
        nl_sign = _planet_sign(ninth_lord, chart_data)
        nl_strong = _is_exalted(ninth_lord, nl_sign) or _is_own(ninth_lord, nl_sign)
        years = _DASHA_YEARS.get(ninth_lord, 16)
        quality = "excellent" if nl_strong and nl_house in (KENDRAS | TRIKONAS) else "good"
        peak_periods.append({
            "period_type": "dasha",
            "description_en": (
                f"{ninth_lord} Mahadasha ({years} years) — 9th lord period. "
                f"The 9th house governs fortune, dharma, and higher wisdom. "
                f"{'Strong placement (exalted/own sign) amplifies this fortune period.' if nl_strong else 'This is a naturally auspicious dasha for luck and blessings.'}"
            ),
            "description_hi": (
                f"{ninth_lord} महादशा ({years} वर्ष) — नवमेश का काल। "
                f"नवम भाव भाग्य, धर्म एवं उच्च ज्ञान का कारक है। "
                f"{'उच्च/स्वराशि स्थिति इस भाग्य-काल को और प्रबल बनाती है।' if nl_strong else 'यह स्वाभाविक रूप से भाग्य एवं आशीर्वाद के लिए शुभ दशा है।'}"
            ),
            "approximate_age_range": f"During {ninth_lord} Mahadasha",
            "quality": quality,
        })

    # Period 2: 5th lord Mahadasha (Trikona = fortune/intelligence)
    if fifth_lord and fifth_lord != ninth_lord:
        fl_house = _planet_house(fifth_lord, chart_data)
        fl_sign = _planet_sign(fifth_lord, chart_data)
        fl_strong = _is_exalted(fifth_lord, fl_sign) or _is_own(fifth_lord, fl_sign)
        years5 = _DASHA_YEARS.get(fifth_lord, 16)
        quality5 = "excellent" if fl_strong and fl_house in (KENDRAS | TRIKONAS) else "good"
        peak_periods.append({
            "period_type": "dasha",
            "description_en": (
                f"{fifth_lord} Mahadasha ({years5} years) — 5th lord period. "
                "The 5th house governs intelligence, creativity, children, and past-life merit (Purva Punya). "
                f"{'Exceptional placement amplifies intuition, luck, and spiritual intelligence.' if fl_strong else 'A naturally creative and fortunate dasha period.'}"
            ),
            "description_hi": (
                f"{fifth_lord} महादशा ({years5} वर्ष) — पंचमेश का काल। "
                "पंचम भाव बुद्धि, सृजनशीलता, संतान एवं पूर्वपुण्य का कारक है। "
                f"{'असाधारण स्थिति अंतर्ज्ञान, भाग्य एवं आध्यात्मिक बुद्धि को बढ़ाती है।' if fl_strong else 'स्वाभाविक रूप से सृजनशील एवं भाग्यशाली दशाकाल।'}"
            ),
            "approximate_age_range": f"During {fifth_lord} Mahadasha",
            "quality": quality5,
        })

    # Period 3: Lagna lord dasha (overall vitality peak)
    if lagna_lord and lagna_lord not in {ninth_lord, fifth_lord}:
        ll_sign = _planet_sign(lagna_lord, chart_data)
        ll_house = _planet_house(lagna_lord, chart_data)
        ll_strong = _is_exalted(lagna_lord, ll_sign) or _is_own(lagna_lord, ll_sign)
        if ll_strong or ll_house in (KENDRAS | TRIKONAS):
            years_ll = _DASHA_YEARS.get(lagna_lord, 16)
            peak_periods.append({
                "period_type": "dasha",
                "description_en": (
                    f"{lagna_lord} Mahadasha ({years_ll} years) — Lagna lord period. "
                    "The Lagna lord governs the self, vitality, and overall life quality. "
                    "A strong Lagna lord dasha brings physical vitality, renewed purpose, and personal success."
                ),
                "description_hi": (
                    f"{lagna_lord} महादशा ({years_ll} वर्ष) — लग्नेश का काल। "
                    "लग्नेश स्वयं, जीवन-शक्ति एवं समग्र जीवन-गुणवत्ता का कारक है। "
                    "प्रबल लग्नेश दशा शारीरिक ऊर्जा, नवीन उद्देश्य एवं व्यक्तिगत सफलता लाती है।"
                ),
                "approximate_age_range": f"During {lagna_lord} Mahadasha",
                "quality": "excellent" if ll_strong else "good",
            })

    # Period 4: Jupiter in excellent transit (Cancer/Sag/Pisces)
    if jupiter_sign in _JUPITER_EXCELLENT:
        period_quality = "excellent"
        desc_en = (
            f"Jupiter currently in {jupiter_sign} — exaltation/own sign transit. "
            "When Jupiter transits Cancer (exaltation), Sagittarius, or Pisces (own signs), "
            "it amplifies fortune, wisdom, and protective grace for ALL ascendants. "
            "This is the most auspicious Jupiter transit period — lasts approximately 1 year."
        )
        desc_hi = (
            f"बृहस्पति वर्तमान में {jupiter_sign} में — उच्च/स्वराशि गोचर। "
            "जब बृहस्पति कर्क (उच्च), धनु या मीन (स्वराशि) में गोचर करे, "
            "सभी लग्नों के लिए भाग्य, ज्ञान एवं सुरक्षात्मक अनुग्रह बढ़ता है। "
            "यह सर्वाधिक शुभ बृहस्पति गोचर काल है — लगभग 1 वर्ष।"
        )
    else:
        good_jup_houses = {2, 5, 7, 9, 11}
        period_quality = "good" if jupiter_house in good_jup_houses else "neutral"
        desc_en = (
            f"Jupiter currently in house {jupiter_house} ({jupiter_sign}). "
            f"{'In a good transit house (2/5/7/9/11) — fortune and wisdom are supported.' if jupiter_house in good_jup_houses else 'Jupiter transit is not in peak auspicious mode at this time.'} "
            "Peak Jupiter transit fortune occurs when Jupiter is in Cancer, Sagittarius, or Pisces."
        )
        desc_hi = (
            f"बृहस्पति वर्तमान में भाव {jupiter_house} ({jupiter_sign}) में। "
            f"{'शुभ गोचर भाव (2/5/7/9/11) में — भाग्य एवं ज्ञान को समर्थन।' if jupiter_house in good_jup_houses else 'बृहस्पति गोचर अभी सर्वोच्च शुभ स्थिति में नहीं।'} "
            "सर्वोच्च बृहस्पति गोचर भाग्य तब होता है जब वह कर्क, धनु या मीन में हो।"
        )

    peak_periods.append({
        "period_type": "transit",
        "description_en": desc_en,
        "description_hi": desc_hi,
        "approximate_age_range": f"Jupiter in {jupiter_sign} (approx 1 year)",
        "quality": period_quality,
    })

    # Current period quality based on active dasha
    current_quality = "neutral"
    if mahadasha_lord:
        is_ninth = (mahadasha_lord == ninth_lord)
        is_fifth = (mahadasha_lord == fifth_lord)
        is_lagna = (mahadasha_lord == lagna_lord)
        is_jup_good = jupiter_sign in _JUPITER_EXCELLENT or jupiter_house in good_jup_houses
        if (is_ninth or is_fifth) and is_jup_good:
            current_quality = "excellent"
        elif is_ninth or is_fifth or is_lagna:
            current_quality = "good"
        elif mahadasha_lord in {_lord_of(6, chart_data), _lord_of(8, chart_data), _lord_of(12, chart_data)}:
            current_quality = "challenging"
        else:
            current_quality = "neutral"

    return {
        "peak_periods": peak_periods,
        "current_period_quality": current_quality,
        "current_mahadasha": mahadasha_lord or "Unknown",
        "sloka_ref": "Phaladeepika Adh. 13",
    }


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def analyze_longevity_indicators(
    chart_data: Dict[str, Any],
    mahadasha_lord: Optional[str] = None,
    antardasha_lord: Optional[str] = None,
) -> Dict[str, Any]:
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
    transit_timing = _transit_timing_section(chart_data)
    dasha_timing = _dasha_gochara_timing(chart_data, mahadasha_lord, antardasha_lord)
    demise_month_lagna = _demise_month_lagna_indicators(chart_data)

    # New Features (Adhyaya 13 + 17)
    saturn_transit_death = _saturn_transit_death_indicator(chart_data)
    moon_death_transit = _moon_death_transit(chart_data)
    demise_timing_classical = _demise_timing_classical(chart_data)
    dasha_gochara_score = _dasha_gochara_lagna_score(chart_data, mahadasha_lord, antardasha_lord)
    lucky_time = _calculate_lucky_periods(chart_data, mahadasha_lord)

    return {
        "overall_longevity_strength": overall,
        "maraka_planets": marakas,
        "eighth_house_analysis": eighth,
        "saturn_longevity_assessment": saturn,
        "karmic_transitions_en": karmic["karmic_transitions_en"],
        "karmic_transitions_hi": karmic["karmic_transitions_hi"],
        "life_chapters_en": chapters["life_chapters_en"],
        "life_chapters_hi": chapters["life_chapters_hi"],
        "transit_timing_indicators": transit_timing,
        "dasha_gochara_timing": dasha_timing,
        "demise_month_lagna_indicators": demise_month_lagna,
        # New features
        "saturn_transit_death_indicator": saturn_transit_death,
        "moon_death_transit": moon_death_transit,
        "demise_timing_classical": demise_timing_classical,
        "dasha_gochara_lagna_score": dasha_gochara_score,
        "lucky_time_estimate": lucky_time,
        "sloka_ref": "Phaladeepika Adh. 17",
    }
