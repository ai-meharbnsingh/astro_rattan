"""
family_demise_engine.py — Family Member Demise Timing Indicators
=================================================================
Implements Phaladeepika Adhyaya 17: identifying natal combinations
that indicate timing of demise of father, mother, and children.

Method:
  - Karaka + bhava lord combinations
  - Maraka lords (2nd and 7th from the relevant bhava)
  - Dusthana afflictions (6/8/12 from key bhava)
  - Timing: activated during dasha of maraka lords

API:
  analyze_family_demise_indicators(planets: dict, asc_sign: str) -> dict
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}

_EXALTATION = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
}
_DEBILITATION = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
}
_OWN_SIGNS = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
}


def _house_sign(bhava: int, asc_sign: str) -> str:
    if asc_sign not in _ZODIAC:
        return ""
    idx = (_ZODIAC.index(asc_sign) + bhava - 1) % 12
    return _ZODIAC[idx]


def _lord_of_house(bhava: int, asc_sign: str) -> str:
    sign = _house_sign(bhava, asc_sign)
    return _SIGN_LORD.get(sign, "") if sign else ""


def _planet_house(pname: str, planets: dict) -> int:
    p = planets.get(pname, {})
    if not isinstance(p, dict):
        return 0
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _planet_sign(pname: str, planets: dict) -> str:
    p = planets.get(pname, {})
    return str(p.get("sign", "")) if isinstance(p, dict) else ""


def _is_afflicted(pname: str, planets: dict) -> bool:
    sign = _planet_sign(pname, planets)
    house = _planet_house(pname, planets)
    # Debilitated
    if _DEBILITATION.get(pname) == sign:
        return True
    # In dusthana (6, 8, 12)
    if house in {6, 8, 12}:
        return True
    # Conjunct malefic
    for mal in _MALEFICS:
        if mal != pname and _planet_house(mal, planets) == house and house != 0:
            return True
    return False


def _is_strong(pname: str, planets: dict) -> bool:
    sign = _planet_sign(pname, planets)
    if _EXALTATION.get(pname) == sign:
        return True
    if sign in _OWN_SIGNS.get(pname, set()):
        return True
    return False


def _analyze_member(
    member: str,
    karaka: str,
    bhava: int,
    planets: dict,
    asc_sign: str,
) -> Dict[str, Any]:
    """
    Analyze demise timing indicators for one family member.

    Args:
        member: "Father", "Mother", or "Son/Child"
        karaka: classical karaka planet name
        bhava: primary house (9=father, 4=mother, 5=son)
        planets: full planet dict
        asc_sign: ascendant sign name
    """
    bhava_lord = _lord_of_house(bhava, asc_sign)

    # Maraka houses from bhava (2nd and 7th from bhava)
    maraka1_bhava = ((bhava - 1 + 1) % 12) + 1  # 2nd from bhava
    maraka2_bhava = ((bhava - 1 + 6) % 12) + 1  # 7th from bhava
    # 8th from bhava (direct death indicator)
    ashtama_bhava = ((bhava - 1 + 7) % 12) + 1

    maraka1_lord = _lord_of_house(maraka1_bhava, asc_sign)
    maraka2_lord = _lord_of_house(maraka2_bhava, asc_sign)
    ashtama_lord = _lord_of_house(ashtama_bhava, asc_sign)

    # Assess karaka and bhava lord
    karaka_afflicted = _is_afflicted(karaka, planets)
    karaka_strong = _is_strong(karaka, planets)
    bhava_lord_afflicted = _is_afflicted(bhava_lord, planets) if bhava_lord else False
    bhava_lord_strong = _is_strong(bhava_lord, planets) if bhava_lord else False

    # Check if malefics occupy the bhava
    malefics_in_bhava = [
        m for m in _MALEFICS
        if _planet_house(m, planets) == bhava and isinstance(planets.get(m), dict)
    ]

    # Build affliction indicators list
    indicators: List[str] = []
    indicators_hi: List[str] = []

    if karaka_afflicted:
        sign = _planet_sign(karaka, planets)
        reason = "debilitated" if _DEBILITATION.get(karaka) == sign else (
            "in dusthana" if _planet_house(karaka, planets) in {6, 8, 12} else "with malefics"
        )
        indicators.append(
            f"{karaka} (karaka for {member.lower()}) is {reason} — weakens the {member.lower()}'s longevity signification."
        )
        indicators_hi.append(
            f"{karaka} ({member} का कारक ग्रह) {reason} है — {member.lower()} की आयु-संकेत कमज़ोर।"
        )

    if bhava_lord_afflicted and bhava_lord:
        indicators.append(
            f"Lord of house {bhava} ({bhava_lord}) is afflicted — the {member.lower()}'s Bhava is weakened."
        )
        indicators_hi.append(
            f"भाव {bhava} के स्वामी ({bhava_lord}) पर पीड़ा — {member} के भाव की स्थिति कमज़ोर।"
        )

    if malefics_in_bhava:
        m_str = " and ".join(malefics_in_bhava)
        m_str_hi = " एवं ".join(malefics_in_bhava)
        indicators.append(
            f"Malefic(s) {m_str} occupy house {bhava} — direct affliction to {member.lower()} signification."
        )
        indicators_hi.append(
            f"पापी ग्रह {m_str_hi} भाव {bhava} में — {member} के संकेत पर प्रत्यक्ष पीड़ा।"
        )

    # Timing: dasha of maraka/ashtama lords
    strong_note_en = (
        f"Strong {karaka} and {bhava_lord or 'lord'} without affliction give long life to {member.lower()}."
        if karaka_strong and not karaka_afflicted else ""
    )
    timing_en = (
        f"Phaladeepika Adh. 17: Demise of {member.lower()} is timed during the Mahadasha or Antardasha "
        f"of maraka lords — house {maraka1_bhava} lord ({maraka1_lord or '—'}) "
        f"and house {maraka2_bhava} lord ({maraka2_lord or '—'}) from house {bhava}. "
        f"The 8th lord from house {bhava} (house {ashtama_bhava}, lord {ashtama_lord or '—'}) "
        f"also acts as death-timer. Saturn or Rahu transiting house {bhava} or aspecting its lord "
        f"during such a dasha amplifies the indication. "
        f"{strong_note_en}"
    )
    timing_hi = (
        f"फलदीपिका अ. 17: {member} की आयु-समाप्ति का समय मारक भावों की महादशा/अंतर्दशा में — "
        f"भाव {maraka1_bhava} का स्वामी ({maraka1_lord or '—'}) "
        f"तथा भाव {maraka2_bhava} का स्वामी ({maraka2_lord or '—'}) भाव {bhava} से। "
        f"भाव {bhava} से अष्टम भाव {ashtama_bhava} का स्वामी ({ashtama_lord or '—'}) भी मृत्यु-कारक। "
        f"इस दशा में शनि या राहु का भाव {bhava} पर गोचर संकेत तीव्र करता है।"
    )

    # Overall assessment
    affliction_count = len(indicators)
    if affliction_count == 0:
        outlook_en = f"No strong affliction indicators found. {member}'s longevity appears protected."
        outlook_hi = f"कोई प्रबल पीड़ा संकेत नहीं। {member} की आयु सुरक्षित प्रतीत होती है।"
    elif affliction_count == 1:
        outlook_en = "Mild affliction present. Monitor maraka dasha periods carefully."
        outlook_hi = "हल्की पीड़ा। मारक दशा अवधि में सावधानी रखें।"
    else:
        outlook_en = f"Multiple afflictions ({affliction_count}). Maraka dasha periods are critical for {member.lower()}."
        outlook_hi = f"अनेक पीड़ा संकेत ({affliction_count})। {member} के लिए मारक दशा अत्यंत महत्वपूर्ण।"

    return {
        "member": member,
        "karaka": karaka,
        "primary_house": bhava,
        "bhava_lord": bhava_lord,
        "maraka_lords": {
            f"house_{maraka1_bhava}_lord": maraka1_lord,
            f"house_{maraka2_bhava}_lord": maraka2_lord,
            f"house_{ashtama_bhava}_lord (8th from bhava)": ashtama_lord,
        },
        "affliction_indicators": indicators,
        "affliction_indicators_hi": indicators_hi,
        "timing_en": timing_en,
        "timing_hi": timing_hi,
        "outlook_en": outlook_en,
        "outlook_hi": outlook_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
    }


def analyze_family_demise_indicators(planets: dict, asc_sign: str) -> Dict[str, Any]:
    """
    Analyze demise timing indicators for father, mother, and son/child.

    Returns:
    {
      "father": {...},
      "mother": {...},
      "son_child": {...},
      "disclaimer_en": str,
      "disclaimer_hi": str,
      "sloka_ref": "Phaladeepika Adh. 17"
    }
    """
    father = _analyze_member("Father", "Sun", 9, planets, asc_sign)
    mother = _analyze_member("Mother", "Moon", 4, planets, asc_sign)
    son = _analyze_member("Son/Child", "Jupiter", 5, planets, asc_sign)

    disclaimer_en = (
        "These indicators follow Phaladeepika Adhyaya 17 classical rules for demise timing. "
        "They are not predictions — they identify potentially challenging periods requiring "
        "protective measures (prayers, Ayurvedic health care, family attention). "
        "Consult a qualified Jyotishi for confirmation."
    )
    disclaimer_hi = (
        "ये संकेत फलदीपिका अ. 17 के शास्त्रीय नियमों पर आधारित हैं। "
        "ये भविष्यवाणी नहीं, बल्कि सतर्कता के संकेत हैं — सुरक्षात्मक उपाय (पूजा, स्वास्थ्य ध्यान) लें। "
        "पुष्टि के लिए योग्य ज्योतिषी से परामर्श करें।"
    )

    return {
        "father": father,
        "mother": mother,
        "son_child": son,
        "disclaimer_en": disclaimer_en,
        "disclaimer_hi": disclaimer_hi,
        "sloka_ref": "Phaladeepika Adh. 17",
    }
