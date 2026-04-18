"""
family_timing_engine.py — Cross-Chart Family Timing Analysis
============================================================
Implements Phaladeepika Adhyaya 15: using the native's natal chart to time
events in the lives of close family members via planetary transits through
the key bhavas (houses) and their lords.

Bhavas (classical assignment):
  9th house  → Father  (Pitru bhava)
  4th house  → Mother  (Matru bhava)
  3rd house  → Siblings / Brothers (Sahaja bhava)
  7th house  → Spouse  (Kalatra bhava)

Public API:
  analyze_family_timing(chart_data: dict) -> dict
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

_SIGN_NAMES: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_NAMES_HI: List[str] = [
    "मेष", "वृष", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
]

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_FAMILY_MEMBERS: List[Dict[str, Any]] = [
    {"member": "Father",   "member_hi": "पिता",       "bhava": 9},
    {"member": "Mother",   "member_hi": "माता",        "bhava": 4},
    {"member": "Siblings", "member_hi": "भाई-बहन",    "bhava": 3},
    {"member": "Spouse",   "member_hi": "जीवनसाथी",   "bhava": 7},
]

_TRANSIT_RULES: Dict[int, List[Dict[str, Any]]] = {
    9: [
        {
            "planet_transit": "Saturn",
            "intensity": "high",
            "effect_en": (
                "Saturn transiting the 9th house — Father faces hardship, health challenges, "
                "or career obstacles. A period of discipline and endurance for the father."
            ),
            "effect_hi": (
                "शनि का नवम भाव में गोचर — पिता को कठिनाई, स्वास्थ्य-चुनौती अथवा जीविका में बाधा "
                "का सामना करना पड़ सकता है। पिता के लिए अनुशासन और धैर्य का काल।"
            ),
            "also_lord_effect_en": (
                "Saturn transiting the natal 9th lord's sign — Father's fortunes are tested; "
                "karmic delays and authority challenges are likely."
            ),
            "also_lord_effect_hi": (
                "शनि का नवम भावेश की राशि में गोचर — पिता की भाग्य-शक्ति परीक्षा में होती है; "
                "कर्मिक विलम्ब और अधिकार-बाधाएँ सम्भव।"
            ),
        },
        {
            "planet_transit": "Rahu",
            "intensity": "moderate",
            "effect_en": (
                "Rahu transiting the 9th house — Father may face reputation challenges, foreign "
                "travel, or a period of separation. Unconventional events enter the father's life."
            ),
            "effect_hi": (
                "राहु का नवम भाव में गोचर — पिता की प्रतिष्ठा पर प्रश्न उठ सकते हैं, विदेश-यात्रा "
                "अथवा वियोग का काल सम्भव। पिता के जीवन में अप्रत्याशित घटनाएँ आती हैं।"
            ),
        },
        {
            "planet_transit": "Mars",
            "intensity": "moderate",
            "effect_en": (
                "Mars transiting the 9th house — Sudden conflict with or concerning the father. "
                "Risk of accidents or aggressive confrontations affecting him."
            ),
            "effect_hi": (
                "मंगल का नवम भाव में गोचर — पिता के साथ या उनसे सम्बन्धित अचानक विवाद। "
                "उन्हें दुर्घटना या आक्रामक टकराव का जोखिम।"
            ),
        },
        {
            "planet_transit": "Jupiter",
            "intensity": "supportive",
            "effect_en": (
                "Jupiter transiting the 9th house — Father is blessed; spiritual growth, "
                "recognition and good health for the father. Auspicious phase."
            ),
            "effect_hi": (
                "बृहस्पति का नवम भाव में गोचर — पिता के लिए शुभकाल; आध्यात्मिक उन्नति, "
                "सम्मान तथा स्वास्थ्य-लाभ। मांगलिक चरण।"
            ),
        },
    ],
    4: [
        {
            "planet_transit": "Saturn",
            "intensity": "high",
            "effect_en": (
                "Saturn transiting the 4th house — Mother's health may be strained; domestic "
                "difficulties and emotional heaviness. Burdens within the home."
            ),
            "effect_hi": (
                "शनि का चतुर्थ भाव में गोचर — माता के स्वास्थ्य पर दबाव सम्भव; घरेलू कठिनाइयाँ "
                "और मानसिक भार। गृह में कष्ट।"
            ),
            "also_lord_effect_en": (
                "Saturn transiting the natal 4th lord's sign — Domestic security is tested; "
                "mother faces delays and restrictions in comfort and property matters."
            ),
            "also_lord_effect_hi": (
                "शनि का चतुर्थ भावेश की राशि में गोचर — गृह-सुरक्षा की परीक्षा; "
                "माता को सुख-सम्पत्ति के मामलों में विलम्ब और बाधाएँ।"
            ),
            "moon_sign_effect_en": (
                "Moon afflicted and Saturn transiting natal Moon's sign — A critical period "
                "for mother's health and emotional wellbeing."
            ),
            "moon_sign_effect_hi": (
                "पीड़ित चन्द्र और शनि का जन्मकालीन चन्द्र-राशि में गोचर — माता के स्वास्थ्य "
                "और भावनात्मक कल्याण का संकटकाल।"
            ),
        },
        {
            "planet_transit": "Mars",
            "intensity": "moderate",
            "effect_en": (
                "Mars transiting the 4th house — Sudden upheaval in the home; mother may face "
                "aggression, accidents or surgical procedures. Domestic turbulence."
            ),
            "effect_hi": (
                "मंगल का चतुर्थ भाव में गोचर — घर में अचानक उथल-पुथल; माता को आक्रामकता, "
                "दुर्घटना अथवा शल्य-चिकित्सा का सामना करना पड़ सकता है।"
            ),
        },
        {
            "planet_transit": "Jupiter",
            "intensity": "supportive",
            "effect_en": (
                "Jupiter transiting the 4th house — Mother is blessed; domestic peace and "
                "prosperity. Harmony and happiness within the home."
            ),
            "effect_hi": (
                "बृहस्पति का चतुर्थ भाव में गोचर — माता के लिए शुभकाल; गृह में शान्ति व "
                "समृद्धि। परिवार में सुख और स्नेह।"
            ),
        },
    ],
    3: [
        {
            "planet_transit": "Saturn",
            "intensity": "high",
            "effect_en": (
                "Saturn transiting the 3rd house — Siblings face struggles, career delays or "
                "a period of hard work without immediate reward."
            ),
            "effect_hi": (
                "शनि का तृतीय भाव में गोचर — भाई-बहन को संघर्ष, जीविका में विलम्ब अथवा "
                "परिश्रम के तत्काल फल न मिलने का काल।"
            ),
            "also_lord_effect_en": (
                "Saturn transiting the natal 3rd lord's sign — Sibling's endeavors are slowed; "
                "communication and short journeys face hurdles."
            ),
            "also_lord_effect_hi": (
                "शनि का तृतीय भावेश की राशि में गोचर — भाई-बहन के प्रयासों में शिथिलता; "
                "संचार और लघु-यात्राओं में बाधा।"
            ),
        },
        {
            "planet_transit": "Mars",
            "intensity": "moderate",
            "effect_en": (
                "Mars transiting the 3rd house — Sibling faces conflicts or accidents; "
                "alternatively, gains in military, sports or competitive fields."
            ),
            "effect_hi": (
                "मंगल का तृतीय भाव में गोचर — भाई-बहन को विवाद या दुर्घटना; अथवा सेना, "
                "खेल या प्रतिस्पर्धी क्षेत्रों में सफलता।"
            ),
        },
        {
            "planet_transit": "Rahu",
            "intensity": "moderate",
            "effect_en": (
                "Rahu transiting the 3rd house — Sibling may pursue foreign travel, an unusual "
                "career path, or unconventional ambitions."
            ),
            "effect_hi": (
                "राहु का तृतीय भाव में गोचर — भाई-बहन विदेश-यात्रा, असामान्य व्यवसाय-मार्ग "
                "अथवा अपारम्परिक महत्त्वाकांक्षाओं की ओर जा सकते हैं।"
            ),
        },
        {
            "planet_transit": "Jupiter",
            "intensity": "supportive",
            "effect_en": (
                "Jupiter transiting the 3rd house — Sibling benefits from education, promotion "
                "or marriage. Good fortune in creative endeavors."
            ),
            "effect_hi": (
                "बृहस्पति का तृतीय भाव में गोचर — भाई-बहन को शिक्षा, पदोन्नति अथवा विवाह "
                "का लाभ। सृजनात्मक प्रयासों में सौभाग्य।"
            ),
        },
    ],
    7: [
        {
            "planet_transit": "Saturn",
            "intensity": "high",
            "effect_en": (
                "Saturn transiting the 7th house — Marital strain or spouse's health challenges. "
                "A period of patience and karmic testing in partnership."
            ),
            "effect_hi": (
                "शनि का सप्तम भाव में गोचर — वैवाहिक तनाव अथवा जीवनसाथी के स्वास्थ्य पर संकट। "
                "साझेदारी में धैर्य और कर्मिक परीक्षा का काल।"
            ),
            "also_lord_effect_en": (
                "Saturn transiting the natal 7th lord's sign — Spouse faces delays and "
                "responsibilities; marital harmony requires extra effort."
            ),
            "also_lord_effect_hi": (
                "शनि का सप्तम भावेश की राशि में गोचर — जीवनसाथी को विलम्ब और दायित्व; "
                "वैवाहिक सामंजस्य के लिए अतिरिक्त प्रयास आवश्यक।"
            ),
        },
        {
            "planet_transit": "Venus",
            "intensity": "moderate",
            "effect_en": (
                "Venus debilitated or combust in transit — Spouse's happiness is reduced; "
                "romantic and material comforts for the spouse are diminished."
            ),
            "effect_hi": (
                "शुक्र का नीच अथवा अस्त होना — जीवनसाथी के सुख में कमी; उनके रोमांटिक "
                "और भौतिक सुखों में न्यूनता।"
            ),
        },
        {
            "planet_transit": "Mars",
            "intensity": "moderate",
            "effect_en": (
                "Mars transiting the 7th house — Conflict or aggressive energy in marriage. "
                "Spouse may face sudden challenges or impulsive decisions."
            ),
            "effect_hi": (
                "मंगल का सप्तम भाव में गोचर — विवाह में विवाद या आक्रामक ऊर्जा। "
                "जीवनसाथी को अचानक चुनौती या आवेगी निर्णय का सामना।"
            ),
        },
        {
            "planet_transit": "Jupiter",
            "intensity": "supportive",
            "effect_en": (
                "Jupiter transiting the 7th house — Spouse is blessed; marriage becomes "
                "harmonious. Prospects for spiritual growth and material prosperity together."
            ),
            "effect_hi": (
                "बृहस्पति का सप्तम भाव में गोचर — जीवनसाथी के लिए शुभकाल; विवाह में सामंजस्य। "
                "साथ में आध्यात्मिक उन्नति और भौतिक समृद्धि।"
            ),
        },
    ],
}


def _sign_index(sign: str) -> int:
    """Return 0-indexed position of sign name, -1 if unknown."""
    try:
        return _SIGN_NAMES.index(sign)
    except ValueError:
        return -1


def _house_sign(house: int, asc_sign: str) -> str:
    """Return the whole-sign sign for a given house number (1-12) from the ascendant sign."""
    idx = _sign_index(asc_sign)
    if idx == -1:
        return asc_sign
    return _SIGN_NAMES[(idx + house - 1) % 12]


def _house_sign_hi(house: int, asc_sign: str) -> str:
    """Hindi name of the whole-sign for a given house from ascendant."""
    idx = _sign_index(asc_sign)
    if idx == -1:
        return ""
    return _SIGN_NAMES_HI[(idx + house - 1) % 12]


def _house_lord(house: int, asc_sign: str) -> str:
    """Return the lord of the given house from ascendant (whole-sign system)."""
    sign = _house_sign(house, asc_sign)
    return _SIGN_LORD.get(sign, "")


def _natal_sign(chart_data: Dict[str, Any], planet: str) -> str:
    """Extract the natal sign of a planet from chart_data."""
    planets = chart_data.get("planets", {})
    pdata = planets.get(planet, {})
    if isinstance(pdata, dict):
        return pdata.get("sign", "")
    return ""


def _sign_hi(sign: str) -> str:
    idx = _sign_index(sign)
    if idx == -1:
        return sign
    return _SIGN_NAMES_HI[idx]


def _build_indicator(
    rule: Dict[str, Any],
    through_sign: str,
    through_sign_hi: str,
    is_lord_transit: bool,
    sloka_ref: str = "Phaladeepika Adh. 15",
) -> Dict[str, Any]:
    """Build a single transit_indicator dict from a rule entry, substituting the actual sign name into effect strings."""
    if is_lord_transit:
        effect_en = rule.get("also_lord_effect_en", rule.get("effect_en", ""))
        effect_hi = rule.get("also_lord_effect_hi", rule.get("effect_hi", ""))
    else:
        effect_en = rule.get("effect_en", "")
        effect_hi = rule.get("effect_hi", "")

    for house_phrase in [
        "the 9th house", "the 4th house", "the 3rd house", "the 7th house",
    ]:
        if house_phrase in effect_en:
            effect_en = effect_en.replace(
                house_phrase, f"{house_phrase} ({through_sign})"
            )
            break

    return {
        "planet_transit": rule["planet_transit"],
        "through_sign": through_sign,
        "through_sign_hi": through_sign_hi,
        "intensity": rule["intensity"],
        "effect_en": effect_en,
        "effect_hi": effect_hi,
        "sloka_ref": sloka_ref,
    }


def _make_summary(members_out: List[Dict[str, Any]]) -> Tuple[str, str]:
    """Produce a short bilingual narrative summary from computed members."""
    watch_en: List[str] = []
    watch_hi: List[str] = []
    support_en: List[str] = []
    support_hi: List[str] = []

    for m in members_out:
        high_indicators = [
            i for i in m.get("transit_indicators", []) if i["intensity"] == "high"
        ]
        protective = m.get("protective_indicators", [])
        member = m["member"]
        member_hi = m["member_hi"]
        bhava = m["bhava"]
        bhava_sign = m.get("bhava_sign", "")
        bhava_sign_hi = m.get("bhava_sign_hi", "")

        if high_indicators:
            watch_en.append(
                f"{member} (house {bhava} — {bhava_sign})"
                " — watch for Saturn/Mars transits"
            )
            watch_hi.append(
                f"{member_hi} (भाव {bhava} — {bhava_sign_hi})"
                " — शनि/मंगल गोचर पर ध्यान दें"
            )
        if protective:
            support_en.append(
                f"{member} benefits when Jupiter transits house {bhava}"
            )
            support_hi.append(
                f"{member_hi} को बृहस्पति के भाव {bhava} में गोचर से लाभ"
            )

    parts_en = []
    parts_hi = []
    if watch_en:
        parts_en.append("Key periods to watch for family members: " + "; ".join(watch_en))
        parts_hi.append("परिवार के सदस्यों के लिए ध्यान देने योग्य मुख्य काल: " + "; ".join(watch_hi))
    if support_en:
        parts_en.append("Supportive periods: " + "; ".join(support_en))
        parts_hi.append("अनुकूल काल: " + "; ".join(support_hi))

    if not parts_en:
        return (
            "Your natal chart's family houses indicate standard transit patterns for "
            "timing events in family members' lives per Phaladeepika Adh. 15.",
            "आपकी जन्मकुंडली के पारिवारिक भाव फलदीपिका अध्याय 15 के अनुसार परिजनों के "
            "जीवन की घटनाओं के लिए सामान्य गोचर-संकेत देते हैं।",
        )
    return " ".join(parts_en), " ".join(parts_hi)


def analyze_family_timing(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cross-chart timing indicators for family members per Phaladeepika Adh. 15.

    Shows which planetary transits (through the relevant natal bhava sign and
    through the natal bhava-lord's sign) affect each family member.

    Args:
        chart_data: Standard chart dict with keys:
            {
                "ascendant": {"sign": "Leo", ...},
                "planets": {
                    "Sun": {"sign": "Aries", "house": 9, ...},
                    ...
                }
            }

    Returns:
        {
            "family_members": [...],
            "summary_en": "...",
            "summary_hi": "...",
            "sloka_ref": "Phaladeepika Adh. 15"
        }
    """
    asc_sign = (chart_data.get("ascendant") or {}).get("sign", "Aries")
    moon_natal_sign = _natal_sign(chart_data, "Moon")
    moon_hi = _sign_hi(moon_natal_sign)

    members_out: List[Dict[str, Any]] = []

    for fm in _FAMILY_MEMBERS:
        member = fm["member"]
        member_hi = fm["member_hi"]
        bhava = fm["bhava"]

        bhava_sign = _house_sign(bhava, asc_sign)
        bhava_sign_hi = _house_sign_hi(bhava, asc_sign)
        bhava_lord = _house_lord(bhava, asc_sign)
        bhava_lord_natal_sign = _natal_sign(chart_data, bhava_lord)
        bhava_lord_natal_sign_hi = _sign_hi(bhava_lord_natal_sign)

        transit_indicators: List[Dict[str, Any]] = []
        protective_indicators: List[Dict[str, Any]] = []

        rules = _TRANSIT_RULES.get(bhava, [])
        for rule in rules:
            planet = rule["planet_transit"]
            intensity = rule["intensity"]

            if intensity == "supportive":
                ind = _build_indicator(rule, bhava_sign, bhava_sign_hi, False)
                protective_indicators.append(ind)
                continue

            # Primary: planet transiting the bhava sign
            ind = _build_indicator(rule, bhava_sign, bhava_sign_hi, False)
            transit_indicators.append(ind)

            # Secondary: Saturn also transiting the bhava lord's natal sign
            if planet == "Saturn" and "also_lord_effect_en" in rule and bhava_lord_natal_sign:
                lord_ind = _build_indicator(
                    rule, bhava_lord_natal_sign, bhava_lord_natal_sign_hi, True
                )
                transit_indicators.append(lord_ind)

                # Extra: Saturn transiting natal Moon's sign (especially for 4th house)
                if bhava == 4 and moon_natal_sign and moon_natal_sign != bhava_lord_natal_sign:
                    moon_rule = {
                        "planet_transit": "Saturn",
                        "intensity": "high",
                        "effect_en": rule.get(
                            "moon_sign_effect_en",
                            f"Moon afflicted and Saturn transiting natal Moon's sign ({moon_natal_sign})"
                            " — A critical period for mother's health and emotional wellbeing.",
                        ),
                        "effect_hi": rule.get(
                            "moon_sign_effect_hi",
                            f"पीड़ित चन्द्र और शनि का जन्मकालीन चन्द्र-राशि ({moon_hi}) में गोचर"
                            " — माता के स्वास्थ्य और भावनात्मक कल्याण का संकटकाल।",
                        ),
                    }
                    moon_ind = _build_indicator(moon_rule, moon_natal_sign, moon_hi, False)
                    transit_indicators.append(moon_ind)

        members_out.append(
            {
                "member": member,
                "member_hi": member_hi,
                "bhava": bhava,
                "bhava_sign": bhava_sign,
                "bhava_sign_hi": bhava_sign_hi,
                "bhava_lord": bhava_lord,
                "bhava_lord_natal_sign": bhava_lord_natal_sign,
                "transit_indicators": transit_indicators,
                "protective_indicators": protective_indicators,
            }
        )

    summary_en, summary_hi = _make_summary(members_out)
    return {
        "family_members": members_out,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 15",
    }
