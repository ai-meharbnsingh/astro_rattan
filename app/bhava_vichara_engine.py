"""
bhava_vichara_engine.py — Bhava-phala-vichara (house flourish/destruction)
============================================================================
Implements Phaladeepika Adhyaya 15 — classical rules for when a bhava
flourishes vs is destroyed, including the **karaka-as-Lagna** technique
(treat a house's karaka as Lagna and re-evaluate the topic from there).

Main function:
    analyze_bhava_vichara(chart_data) -> dict

Rules (classical):
  Bhava DESTROYED if any of:
    * Its lord is in 6/8/12
    * Multiple malefics aspect it with no benefic support
    * Its karaka is combust AND afflicted
  Bhava FLOURISHES if:
    * Its lord exalted / own-sign AND placed in Kendra/Trikona
    * Benefic aspect on the house OR benefic occupant

NOTE: classical rules are probabilistic. Output is purely informational.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

# ───────────────────────────────────────────────────────────────
# Classical constants
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

SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}

NATURAL_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}

BHAVA_NAMES_EN = {
    1: "Tanu", 2: "Dhana", 3: "Sahaja", 4: "Sukha",
    5: "Putra", 6: "Ari", 7: "Yuvati", 8: "Randhra",
    9: "Bhagya", 10: "Karma", 11: "Labha", 12: "Vyaya",
}

BHAVA_NAMES_HI = {
    1: "तनु", 2: "धन", 3: "सहज", 4: "सुख",
    5: "पुत्र", 6: "अरि", 7: "युवति", 8: "रन्ध्र",
    9: "भाग्य", 10: "कर्म", 11: "लाभ", 12: "व्यय",
}

BHAVA_TOPIC_EN = {
    1: "body and self", 2: "wealth and speech", 3: "siblings and courage",
    4: "happiness and mother", 5: "children and intellect", 6: "enemies and disease",
    7: "spouse and partnerships", 8: "longevity and hidden matters",
    9: "fortune and dharma", 10: "career and action",
    11: "gains and friendships", 12: "losses and liberation",
}

BHAVA_TOPIC_HI = {
    1: "शरीर एवं स्व", 2: "धन एवं वाणी", 3: "भाई-बहन एवं पराक्रम",
    4: "सुख एवं माता", 5: "सन्तान एवं बुद्धि", 6: "शत्रु एवं रोग",
    7: "जीवनसाथी एवं साझेदारी", 8: "आयु एवं गूढ़ विषय",
    9: "भाग्य एवं धर्म", 10: "कर्म एवं वृत्ति",
    11: "लाभ एवं मित्र", 12: "व्यय एवं मोक्ष",
}


# ───────────────────────────────────────────────────────────────
# Karakas per house (classical Phaladeepika list)
# ───────────────────────────────────────────────────────────────

def _bhava_karakas() -> Dict[int, str]:
    """Primary karakas for each of the 12 houses.

    Some houses (6, 10) have dual karakas. We return the primary; the full
    dual where relevant is preserved in the human-readable name.
    """
    return {
        1: "Sun",
        2: "Jupiter",
        3: "Mars",
        4: "Moon",
        5: "Jupiter",
        6: "Mars/Saturn",
        7: "Venus",
        8: "Saturn",
        9: "Jupiter",
        10: "Sun/Saturn",
        11: "Jupiter",
        12: "Saturn",
    }


def _primary_karaka(house: int) -> str:
    """Return the primary (first) karaka when multiple are listed."""
    karakas = _bhava_karakas()
    raw = karakas.get(house, "")
    if "/" in raw:
        return raw.split("/")[0].strip()
    return raw


# ───────────────────────────────────────────────────────────────
# Chart helpers
# ───────────────────────────────────────────────────────────────

def _int_house(p: Dict[str, Any]) -> int:
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _sign(p: Dict[str, Any]) -> str:
    return str(p.get("sign", ""))


def _planets(chart: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return chart.get("planets", {}) or {}


def _asc_sign(chart: Dict[str, Any]) -> str:
    return str((chart.get("ascendant") or {}).get("sign", ""))


def _house_sign(house: int, chart: Dict[str, Any]) -> str:
    """Sign occupying the given house (whole-sign system)."""
    asc = _asc_sign(chart)
    if asc not in ZODIAC or not (1 <= house <= 12):
        # Try explicit houses[] if present
        for h in chart.get("houses") or []:
            if isinstance(h, dict) and int(h.get("number", 0) or 0) == house:
                return str(h.get("sign", ""))
        return ""
    idx = (ZODIAC.index(asc) + house - 1) % 12
    return ZODIAC[idx]


def _house_lord(house: int, chart: Dict[str, Any]) -> str:
    return SIGN_LORD.get(_house_sign(house, chart), "")


def _planet_house(planet: str, chart: Dict[str, Any]) -> int:
    p = _planets(chart).get(planet)
    if not isinstance(p, dict):
        return 0
    return _int_house(p)


def _planet_sign(planet: str, chart: Dict[str, Any]) -> str:
    p = _planets(chart).get(planet)
    if not isinstance(p, dict):
        return ""
    return _sign(p)


def _is_exalted(planet: str, sign: str) -> bool:
    return bool(sign) and EXALTATION.get(planet) == sign


def _is_own(planet: str, sign: str) -> bool:
    return bool(sign) and sign in OWN_SIGNS.get(planet, set())


def _is_debilitated(planet: str, sign: str) -> bool:
    return bool(sign) and DEBILITATION.get(planet) == sign


def _planet_aspects_house(planet: str, planet_house: int, target_house: int) -> bool:
    """Return True if planet in planet_house aspects target_house (Vedic drishti)."""
    if not (1 <= planet_house <= 12) or not (1 <= target_house <= 12):
        return False
    offsets = [7] + list(SPECIAL_ASPECTS.get(planet, []))
    for n in offsets:
        target = ((planet_house - 1 + (n - 1)) % 12) + 1
        if target == target_house:
            return True
    return False


def _is_combust(planet: str, chart: Dict[str, Any]) -> bool:
    """Simple combustion: non-Sun, non-node planet within 10 of Sun."""
    if planet in ("Sun", "Rahu", "Ketu"):
        return False
    planets = _planets(chart)
    p = planets.get(planet) or {}
    sun = planets.get("Sun") or {}
    if not p or not sun:
        return False
    try:
        p_lon = float(p.get("longitude", -999))
        s_lon = float(sun.get("longitude", -999))
    except (TypeError, ValueError):
        return False
    if p_lon < 0 or s_lon < 0:
        return False
    diff = abs(p_lon - s_lon)
    if diff > 180:
        diff = 360 - diff
    return diff < 10.0


# ───────────────────────────────────────────────────────────────
# Karaka-as-Lagna technique
# ───────────────────────────────────────────────────────────────

def _analyze_karaka_as_lagna(
    karaka: str, house_topic_en: str, house_topic_hi: str, chart: Dict[str, Any]
) -> Tuple[str, str]:
    """
    Treat the karaka planet's position as Lagna and re-evaluate the topic.

    We check the karaka's own house placement, sign, and whether benefics or
    malefics aspect it. This provides a secondary lens on the topic ruled by
    the house.
    """
    planets = _planets(chart)
    if karaka not in planets:
        return (
            f"Karaka {karaka} not present in chart; {house_topic_en} cannot be re-evaluated via karaka-as-Lagna.",
            f"कारक {karaka} कुंडली में उपस्थित नहीं है; {house_topic_hi} का कारक-से-लग्न विश्लेषण सम्भव नहीं।",
        )

    k_house = _planet_house(karaka, chart)
    k_sign = _planet_sign(karaka, chart)

    # Strength of karaka itself
    if _is_exalted(karaka, k_sign):
        strength_en = f"{karaka} is exalted in {k_sign}"
        strength_hi = f"{karaka} {k_sign} में उच्च राशि में है"
    elif _is_own(karaka, k_sign):
        strength_en = f"{karaka} is in own sign ({k_sign})"
        strength_hi = f"{karaka} स्वराशि ({k_sign}) में है"
    elif _is_debilitated(karaka, k_sign):
        strength_en = f"{karaka} is debilitated in {k_sign}"
        strength_hi = f"{karaka} {k_sign} में नीच राशि में है"
    elif k_house in DUSTHANAS:
        strength_en = f"{karaka} is placed in a Dusthana (house {k_house})"
        strength_hi = f"{karaka} दुःस्थान (भाव {k_house}) में स्थित है"
    elif k_house in KENDRAS or k_house in TRIKONAS:
        strength_en = f"{karaka} is placed in Kendra/Trikona (house {k_house})"
        strength_hi = f"{karaka} केंद्र/त्रिकोण (भाव {k_house}) में स्थित है"
    else:
        strength_en = f"{karaka} is placed in house {k_house}"
        strength_hi = f"{karaka} भाव {k_house} में स्थित है"

    # Aspects on karaka (from other planets)
    benefic_support = []
    malefic_pressure = []
    for other, pdata in planets.items():
        if other == karaka or not isinstance(pdata, dict):
            continue
        oh = _int_house(pdata)
        if oh <= 0:
            continue
        if _planet_aspects_house(other, oh, k_house):
            if other in NATURAL_BENEFICS:
                benefic_support.append(other)
            elif other in NATURAL_MALEFICS:
                malefic_pressure.append(other)

    aspect_en = ""
    aspect_hi = ""
    if benefic_support and not malefic_pressure:
        aspect_en = f" Benefic aspect by {', '.join(benefic_support)} supports {house_topic_en}."
        aspect_hi = f" {', '.join(benefic_support)} की शुभ दृष्टि {house_topic_hi} का समर्थन करती है।"
    elif malefic_pressure and not benefic_support:
        aspect_en = f" Malefic aspect by {', '.join(malefic_pressure)} may challenge {house_topic_en}."
        aspect_hi = f" {', '.join(malefic_pressure)} की अशुभ दृष्टि {house_topic_hi} के लिए चुनौती बन सकती है।"
    elif benefic_support and malefic_pressure:
        aspect_en = (
            f" Mixed influences on karaka: benefics {', '.join(benefic_support)} vs "
            f"malefics {', '.join(malefic_pressure)}."
        )
        aspect_hi = (
            f" कारक पर मिश्रित प्रभाव: शुभ ({', '.join(benefic_support)}) बनाम "
            f"अशुभ ({', '.join(malefic_pressure)})।"
        )

    en = f"Karaka-as-Lagna ({karaka}): {strength_en}.{aspect_en}"
    hi = f"कारक-से-लग्न ({karaka}): {strength_hi}।{aspect_hi}"
    return en, hi


# ───────────────────────────────────────────────────────────────
# Per-bhava assessment
# ───────────────────────────────────────────────────────────────

def _occupants(house: int, chart: Dict[str, Any]) -> List[str]:
    out: List[str] = []
    for p, pdata in _planets(chart).items():
        if isinstance(pdata, dict) and _int_house(pdata) == house:
            out.append(p)
    return out


def _aspects_on_house(house: int, chart: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Return (benefic_aspects, malefic_aspects) on the given house."""
    benefics: List[str] = []
    malefics: List[str] = []
    for p, pdata in _planets(chart).items():
        if not isinstance(pdata, dict):
            continue
        ph = _int_house(pdata)
        if ph <= 0 or ph == house:
            continue
        if _planet_aspects_house(p, ph, house):
            if p in NATURAL_BENEFICS:
                benefics.append(p)
            elif p in NATURAL_MALEFICS:
                malefics.append(p)
    return benefics, malefics


def _assess_bhava(house: int, chart: Dict[str, Any]) -> Dict[str, Any]:
    """Assess a single bhava: flourishing vs destruction per Adh. 15 rules."""
    lord = _house_lord(house, chart)
    lord_house = _planet_house(lord, chart) if lord else 0
    lord_sign = _planet_sign(lord, chart) if lord else ""
    karaka_raw = _bhava_karakas().get(house, "")
    karaka = _primary_karaka(house)

    occupants = _occupants(house, chart)
    benefic_aspects, malefic_aspects = _aspects_on_house(house, chart)
    has_benefic_occupant = any(o in NATURAL_BENEFICS for o in occupants)
    has_malefic_occupant = any(o in NATURAL_MALEFICS for o in occupants)

    reasons_en: List[str] = []
    reasons_hi: List[str] = []

    destruction_risk = False
    flourishing = False

    # ── Destruction checks ────────────────────────────────────
    if lord and lord_house in DUSTHANAS:
        destruction_risk = True
        reasons_en.append(
            f"Lord {lord} is placed in Dusthana (house {lord_house}) — classical destruction indicator."
        )
        reasons_hi.append(
            f"भावेश {lord} दुःस्थान (भाव {lord_house}) में स्थित है — शास्त्रीय भाव नाश का संकेत।"
        )

    if len(malefic_aspects) >= 2 and not benefic_aspects and not has_benefic_occupant:
        destruction_risk = True
        reasons_en.append(
            f"Multiple malefics ({', '.join(malefic_aspects)}) aspect the house with no benefic support."
        )
        reasons_hi.append(
            f"एकाधिक अशुभ ग्रह ({', '.join(malefic_aspects)}) इस भाव को देखते हैं; कोई शुभ सहायता नहीं।"
        )

    if karaka and _is_combust(karaka, chart):
        karaka_sign = _planet_sign(karaka, chart)
        afflicted = (
            _is_debilitated(karaka, karaka_sign)
            or _planet_house(karaka, chart) in DUSTHANAS
        )
        if afflicted:
            destruction_risk = True
            reasons_en.append(
                f"Karaka {karaka} is combust AND afflicted — weakens the significations of this bhava."
            )
            reasons_hi.append(
                f"कारक {karaka} अस्त एवं पीड़ित है — भाव के फल क्षीण होते हैं।"
            )

    # ── Flourishing checks ────────────────────────────────────
    lord_strong = lord and (_is_exalted(lord, lord_sign) or _is_own(lord, lord_sign))
    lord_placed_well = lord_house in (KENDRAS | TRIKONAS)
    if lord_strong and lord_placed_well:
        flourishing = True
        reasons_en.append(
            f"Lord {lord} is strong (in {lord_sign}) and placed in Kendra/Trikona (house {lord_house})."
        )
        reasons_hi.append(
            f"भावेश {lord} बलवान है ({lord_sign}) तथा केंद्र/त्रिकोण (भाव {lord_house}) में स्थित है।"
        )

    if has_benefic_occupant or benefic_aspects:
        # Supplementary flourish support; ensures flag even without strong lord
        if not flourishing and not destruction_risk:
            flourishing = True
        detail_en = []
        detail_hi = []
        if has_benefic_occupant:
            bens = [o for o in occupants if o in NATURAL_BENEFICS]
            detail_en.append(f"benefic occupant(s) {', '.join(bens)}")
            detail_hi.append(f"शुभ ग्रह ({', '.join(bens)}) उपस्थित")
        if benefic_aspects:
            detail_en.append(f"benefic aspect by {', '.join(benefic_aspects)}")
            detail_hi.append(f"{', '.join(benefic_aspects)} की शुभ दृष्टि")
        if detail_en:
            reasons_en.append("Benefic support: " + "; ".join(detail_en) + ".")
            reasons_hi.append("शुभ सहायता: " + "; ".join(detail_hi) + "।")

    # P0-4: Malefic in 6/8/12 (Dusthana) STRENGTHENS that bhava's significations.
    # Counter-intuitive classical rule (Phaladeepika Adh. 15-16):
    # A natural malefic in its own dusthana energises the house's core purpose
    # (6th → defeats enemies; 8th → fortifies longevity; 12th → aids liberation/foreign).
    if house in DUSTHANAS and has_malefic_occupant:
        malefics_in_house = [o for o in occupants if o in NATURAL_MALEFICS]
        dusthana_names = {6: "6th (Ari)", 8: "8th (Randhra)", 12: "12th (Vyaya)"}
        dusthana_benefits = {
            6: "strengthens the ability to defeat enemies and overcome disease",
            8: "fortifies longevity and occult knowledge",
            12: "supports spiritual liberation, foreign travel, and moksha",
        }
        dusthana_benefits_hi = {
            6: "शत्रुनाश एवं रोग-निवारण की क्षमता बढ़ती है",
            8: "आयु एवं गूढ़ ज्ञान को बल मिलता है",
            12: "मोक्ष, विदेश-यात्रा, एवं आध्यात्मिक उन्नति को बल मिलता है",
        }
        if not destruction_risk:
            flourishing = True
        reasons_en.append(
            f"Natural malefic(s) {', '.join(malefics_in_house)} in the {dusthana_names.get(house, str(house))} house "
            f"{dusthana_benefits.get(house, 'strengthens this dusthana')} "
            f"(Phaladeepika Adh. 15 — malefic in dusthana energises its significations)."
        )
        reasons_hi.append(
            f"प्राकृतिक अशुभ ग्रह {', '.join(malefics_in_house)} {house}वें भाव में स्थित है — "
            f"{dusthana_benefits_hi.get(house, 'यह दुःस्थान को बलवान बनाता है')} "
            f"(फलदीपिका अ. 15 — दुःस्थान में पापग्रह उस भाव के फल को बलवान बनाता है)।"
        )

    # If conflicting: destruction takes precedence
    if destruction_risk:
        flourishing = False

    # ── Karaka-as-Lagna narrative ─────────────────────────────
    k_en, k_hi = _analyze_karaka_as_lagna(
        karaka, BHAVA_TOPIC_EN[house], BHAVA_TOPIC_HI[house], chart
    )

    return {
        "house": house,
        "name_en": BHAVA_NAMES_EN[house],
        "name_hi": BHAVA_NAMES_HI[house],
        "lord": lord,
        "lord_placement": lord_house,
        "karaka": karaka_raw,
        "flourishing": flourishing,
        "destruction_risk": destruction_risk,
        "reasons_en": reasons_en,
        "reasons_hi": reasons_hi,
        "karaka_as_lagna_analysis_en": k_en,
        "karaka_as_lagna_analysis_hi": k_hi,
        "sloka_ref": f"Phaladeepika Adh. 15 (bhava {house})",
    }


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def analyze_bhava_vichara(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyse all 12 bhavas per Phaladeepika Adhyaya 15.

    Returns dict with bhava_assessments (12 entries), overall_strongest
    and overall_weakest house numbers, plus sloka_ref.
    """
    if not isinstance(chart_data, dict):
        chart_data = {}

    assessments: List[Dict[str, Any]] = []
    for h in range(1, 13):
        assessments.append(_assess_bhava(h, chart_data))

    strongest = [a["house"] for a in assessments if a["flourishing"]]
    weakest = [a["house"] for a in assessments if a["destruction_risk"]]

    return {
        "bhava_assessments": assessments,
        "overall_strongest": strongest,
        "overall_weakest": weakest,
        "sloka_ref": "Phaladeepika Adh. 15",
    }
