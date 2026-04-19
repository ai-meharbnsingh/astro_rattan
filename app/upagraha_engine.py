from typing import Any, Dict, Tuple

from app.astro_engine import (
    calculate_planet_positions,
    get_sign_from_longitude,
    get_nakshatra_from_longitude,
    _parse_datetime,
)

# ── Classical natures (name → (nature, classical_meaning_en, classical_meaning_hi)) ──
_UPAGRAHA_NATURES: Dict[str, Tuple[str, str, str]] = {
    "Dhooma": (
        "malefic",
        "Obstruction, veiling, deceit, inflammatory tendencies; Mars-like in quality.",
        "बाधा, आवरण, छल-कपट, आग्नेय प्रवृत्ति; मंगल-सदृश गुण।",
    ),
    "Vyatipata": (
        "malefic",
        "Sudden reversals, calamities, unexpected defeats; triggers crisis-events.",
        "अचानक विपरीत स्थिति, आपदा, अप्रत्याशित पराजय; संकट-घटनाओं का संकेत।",
    ),
    "Parivesha": (
        "malefic",
        "Jealousy, fear from enemies, a halo of obstacles surrounding the native.",
        "शत्रुओं से भय, जलन, चारों ओर बाधाओं का आवरण।",
    ),
    "Indrachapa": (
        "malefic",
        "Sudden breaks and setbacks; disruption of journeys and long-range plans.",
        "अचानक विराम एवं आघात; यात्राओं और दीर्घकालीन योजनाओं में व्यवधान।",
    ),
    "Upaketu": (
        "malefic",
        "Chronic illness, hidden enemies, karmic debt, and spiritual obstacles.",
        "पुराने रोग, छिपे शत्रु, कर्म-ऋण, आध्यात्मिक विघ्न।",
    ),
    "Gulika": (
        "severe_malefic",
        "Poisons, toxins, evil influences, and chronic destruction; son of Saturn.",
        "विष, विषाक्त प्रभाव, आसुरी शक्तियाँ, पुराना विनाश; शनि-पुत्र।",
    ),
    "Mandi": (
        "severe_malefic",
        "Devastation, death-like suffering, extreme misfortune, and karmic retribution.",
        "विनाश, मृत्युतुल्य कष्ट, अत्यंत दुर्भाग्य, कर्म-दंड।",
    ),
}

_HOUSE_AREAS_EN: Dict[int, str] = {
    1: "self and physical body", 2: "wealth and family", 3: "courage and siblings",
    4: "home and mother", 5: "children and intelligence", 6: "enemies and disease",
    7: "marriage and partnerships", 8: "longevity and hidden matters",
    9: "fortune and dharma", 10: "career and status",
    11: "gains and desires", 12: "losses and liberation",
}
_HOUSE_AREAS_HI: Dict[int, str] = {
    1: "स्वयं एवं शरीर", 2: "धन एवं परिवार", 3: "पराक्रम एवं भाई-बहन",
    4: "गृह एवं माता", 5: "संतान एवं बुद्धि", 6: "शत्रु एवं रोग",
    7: "विवाह एवं साझेदारी", 8: "आयु एवं गुप्त विषय",
    9: "भाग्य एवं धर्म", 10: "कर्म एवं प्रतिष्ठा",
    11: "लाभ एवं इच्छाएं", 12: "व्यय एवं मोक्ष",
}


def _compute_house(lon: float, asc_lon: float) -> int:
    """Whole-sign house from ecliptic longitude and ascendant longitude."""
    asc_sign_idx = int(asc_lon / 30) % 12
    lon_sign_idx = int(lon / 30) % 12
    return ((lon_sign_idx - asc_sign_idx) % 12) + 1


# Sign → Lord mapping (for house-lord strength check)
_SIGN_LORD_U: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
_ZODIAC_U = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
_EXALTATION_U: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
}
_OWN_SIGNS_U: Dict[str, set] = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
}
_SPECIAL_ASPECTS_U: Dict[str, list] = {
    "Mars": [4, 8], "Jupiter": [5, 9], "Saturn": [3, 10],
    "Rahu": [5, 9], "Ketu": [5, 9],
}


def _planet_aspects_house_u(planet: str, planet_house: int, target_house: int) -> bool:
    """Return True if planet in planet_house aspects target_house (Vedic drishti)."""
    if not (1 <= planet_house <= 12) or not (1 <= target_house <= 12):
        return False
    offsets = [7] + list(_SPECIAL_ASPECTS_U.get(planet, []))
    for n in offsets:
        if ((planet_house - 1 + (n - 1)) % 12) + 1 == target_house:
            return True
    return False


def _build_mitigating_factors(
    house: int,
    asc_sign: str,
    planet_houses: dict | None,
    planet_signs: dict | None,
) -> Tuple[list, str, str]:
    """
    Compute mitigating factors for an upagraha in `house`.

    Returns:
        (factors_list, mitigated_en, mitigated_hi)
        factors_list: list of dicts describing each mitigant
        mitigated_en / mitigated_hi: non-empty if any mitigant found
    """
    factors = []
    ph = planet_houses or {}
    ps = planet_signs or {}

    # Factor 1: Jupiter aspects the house
    jup_house = ph.get("Jupiter", 0)
    if jup_house and _planet_aspects_house_u("Jupiter", jup_house, house):
        factors.append({
            "factor": "Jupiter aspect",
            "detail_en": f"Jupiter (natural benefic) in house {jup_house} aspects house {house}, reducing severity.",
            "detail_hi": f"बृहस्पति (शुभ ग्रह) भाव {jup_house} से भाव {house} को दृष्टि दे रहे हैं, तीव्रता घट जाती है।",
        })

    # Factor 2: House lord is strong (exalted or own sign)
    house_sign = ""
    if asc_sign in _ZODIAC_U:
        asc_idx = _ZODIAC_U.index(asc_sign)
        house_sign = _ZODIAC_U[(asc_idx + house - 1) % 12]
    house_lord = _SIGN_LORD_U.get(house_sign, "")
    if house_lord:
        lord_sign = ps.get(house_lord, "")
        if lord_sign:
            lord_is_exalted = _EXALTATION_U.get(house_lord) == lord_sign
            lord_in_own = lord_sign in _OWN_SIGNS_U.get(house_lord, set())
            if lord_is_exalted:
                factors.append({
                    "factor": "House lord exalted",
                    "detail_en": f"{house_lord} (lord of house {house}) is exalted in {lord_sign} — strong house lord counters the upagraha's malefic effect.",
                    "detail_hi": f"{house_lord} (भाव {house} का स्वामी) {lord_sign} में उच्च — बलवान भावेश उपग्रह के पापी प्रभाव को प्रतिरोधित करता है।",
                })
            elif lord_in_own:
                factors.append({
                    "factor": "House lord in own sign",
                    "detail_en": f"{house_lord} (lord of house {house}) is in its own sign {lord_sign} — protects house significations from the upagraha's full malefic impact.",
                    "detail_hi": f"{house_lord} (भाव {house} का स्वामी) अपनी राशि {lord_sign} में — भाव के विषयों को उपग्रह के पूर्ण पापी प्रभाव से बचाता है।",
                })

    if not factors:
        return [], "", ""

    factor_labels_en = "; ".join(f["detail_en"] for f in factors)
    factor_labels_hi = "; ".join(f["detail_hi"] for f in factors)
    mitigated_en = (
        f"Classical indication of adversity — however, {factor_labels_en} "
        f"These factors reduce the severity of the classical indication."
    )
    mitigated_hi = (
        f"शास्त्रोक्त प्रतिकूलता का संकेत — परन्तु {factor_labels_hi} "
        f"ये कारक शास्त्रोक्त संकेत की तीव्रता को कम करते हैं।"
    )
    return factors, mitigated_en, mitigated_hi


def _build_interpretation(name: str, house: int) -> Tuple[str, str]:
    """Return (en, hi) interpretation for an upagraha in a given house."""
    data = _UPAGRAHA_NATURES.get(name)
    if not data:
        return (f"{name} in house {house}: malefic sub-planet influence.",
                f"{name} भाव {house} में: पापी उपग्रह प्रभाव।")
    nature, classical_en, classical_hi = data
    severity_en = "serious" if nature == "severe_malefic" else "adverse"
    severity_hi = "गंभीर" if nature == "severe_malefic" else "प्रतिकूल"
    area_en = _HOUSE_AREAS_EN.get(house, f"house {house}")
    area_hi = _HOUSE_AREAS_HI.get(house, f"भाव {house}")
    en = (
        f"{name} in house {house} ({area_en}): casts {severity_en} influence over "
        f"{area_en} significations. {classical_en}"
    )
    hi = (
        f"{name} भाव {house} ({area_hi}) में: {area_hi} के विषयों पर {severity_hi} "
        f"प्रभाव डालता है। {classical_hi}"
    )
    return en, hi


def calculate_upagrahas(
    birth_date: str,
    birth_time: str,
    lat: float,
    lon: float,
    tz_offset: float,
    planet_houses: dict | None = None,
    planet_signs: dict | None = None,
    asc_sign: str = "",
) -> Dict[str, Any]:
    """
    Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas.
    Each entry includes classical house placement + bilingual interpretation,
    plus mitigating_factors when Jupiter aspects the house or the house lord is strong.

    planet_houses: {planet_name: house_number}  (optional — enhances mitigant detection)
    planet_signs:  {planet_name: sign_name}     (optional — enables house-lord strength check)
    asc_sign:      ascendant sign name           (optional — needed for house-lord derivation)
    """
    # 1. Get Sun and ascendant positions
    pos_data = calculate_planet_positions(birth_date, birth_time, lat, lon, tz_offset)
    sun_lon = pos_data["planets"]["Sun"]["longitude"]
    asc_lon = pos_data["ascendant"]["longitude"]

    # --- APRAKASHA GRAHAS ---
    dhooma = (sun_lon + 133.3333333) % 360
    vyatipata = (360 - dhooma) % 360
    parivesha = (vyatipata + 180) % 360
    indrachapa = (360 - parivesha) % 360
    upaketu = (indrachapa + 16.6666666) % 360

    aprakasha = [
        {"name": "Dhooma",    "longitude": dhooma},
        {"name": "Vyatipata", "longitude": vyatipata},
        {"name": "Parivesha", "longitude": parivesha},
        {"name": "Indrachapa","longitude": indrachapa},
        {"name": "Upaketu",   "longitude": upaketu},
    ]

    # Derive asc_sign from computed asc_lon if not provided
    _asc_sign = asc_sign
    if not _asc_sign:
        _asc_sign = _ZODIAC_U[int(asc_lon / 30) % 12]

    results = {}
    for p in aprakasha:
        l = p["longitude"]
        sign = get_sign_from_longitude(l)
        nak = get_nakshatra_from_longitude(l)
        house = _compute_house(l, asc_lon)
        name = p["name"]
        interp_en, interp_hi = _build_interpretation(name, house)
        nature_data = _UPAGRAHA_NATURES.get(name, ("malefic", "", ""))
        mit_factors, mit_en, mit_hi = _build_mitigating_factors(
            house, _asc_sign, planet_houses, planet_signs
        )
        results[name] = {
            "longitude": round(l, 4),
            "sign": sign,
            "sign_degree": round(l % 30, 4),
            "nakshatra": nak["name"],
            "nakshatra_pada": nak["pada"],
            "house": house,
            "nature": nature_data[0],
            "classical_meaning_en": nature_data[1],
            "classical_meaning_hi": nature_data[2],
            "interpretation_en": interp_en,
            "interpretation_hi": interp_hi,
            "mitigating_factors": mit_factors,
            "mitigating_effect_en": mit_en or None,
            "mitigating_effect_hi": mit_hi or None,
        }

    # --- GULIKA & MANDI (KALA VELAS) ---
    dt_local = _parse_datetime(birth_date, birth_time, tz_offset)
    local_hour = dt_local.hour + dt_local.minute / 60.0
    day_of_week = dt_local.weekday()
    vedic_weekday = (day_of_week + 1) % 7

    sunrise_hour = 6.0
    sunset_hour = 18.0

    if local_hour < sunrise_hour:
        vedic_weekday = (vedic_weekday - 1) % 7
        is_day = False
    elif local_hour >= sunset_hour:
        is_day = False
    else:
        is_day = True

    if is_day:
        start_lord = vedic_weekday
    else:
        start_lord = (vedic_weekday + 4) % 7

    saturn_index = (6 - start_lord) % 7

    if is_day:
        duration = sunset_hour - sunrise_hour
        part_len = duration / 8.0
        start_time = sunrise_hour
    else:
        duration = (24.0 - sunset_hour) + sunrise_hour
        part_len = duration / 8.0
        start_time = sunset_hour

    gulika_hour = start_time + saturn_index * part_len
    if gulika_hour >= 24.0:
        gulika_hour -= 24.0

    gh = int(gulika_hour)
    gm = int((gulika_hour - gh) * 60)
    g_time_str = f"{gh:02d}:{gm:02d}:00"
    g_pos = calculate_planet_positions(birth_date, g_time_str, lat, lon, tz_offset)
    gulika_lon = g_pos["ascendant"]["longitude"]
    g_sign = get_sign_from_longitude(gulika_lon)
    g_nak = get_nakshatra_from_longitude(gulika_lon)
    gulika_house = _compute_house(gulika_lon, asc_lon)
    g_interp_en, g_interp_hi = _build_interpretation("Gulika", gulika_house)
    g_nature = _UPAGRAHA_NATURES["Gulika"]
    g_mit_factors, g_mit_en, g_mit_hi = _build_mitigating_factors(
        gulika_house, _asc_sign, planet_houses, planet_signs
    )
    results["Gulika"] = {
        "longitude": round(gulika_lon, 4),
        "sign": g_sign,
        "sign_degree": round(gulika_lon % 30, 4),
        "nakshatra": g_nak["name"],
        "nakshatra_pada": g_nak["pada"],
        "house": gulika_house,
        "nature": g_nature[0],
        "classical_meaning_en": g_nature[1],
        "classical_meaning_hi": g_nature[2],
        "interpretation_en": g_interp_en,
        "interpretation_hi": g_interp_hi,
        "mitigating_factors": g_mit_factors,
        "mitigating_effect_en": g_mit_en or None,
        "mitigating_effect_hi": g_mit_hi or None,
    }

    # Rule: Gulika in 8th/12th intensifies Mrita effect
    if gulika_house in (8, 12):
        area = "longevity and sudden adversity" if gulika_house == 8 else "losses, hospitalization, and isolation"
        results["Gulika"]["special_rule_en"] = (
            f"Gulika in house {gulika_house} activates Mrita Yoga — significantly intensifies malefic "
            f"influence over {area}. Affliction to lifespan and well-being is heightened. "
            f"Phaladeepika Adh. 22 warns of serious obstacles in the significations of this house."
        )
        results["Gulika"]["special_rule_hi"] = (
            f"गुलिक भाव {gulika_house} में मृत योग सक्रिय करता है — {area} पर पापी "
            f"प्रभाव तीव्र। आयु एवं कल्याण पर पीड़ा बढ़ी। "
            f"फलदीपिका अध्याय 22 के अनुसार इस भाव के विषयों में गंभीर बाधाएं।"
        )
    else:
        results["Gulika"]["special_rule_en"] = None
        results["Gulika"]["special_rule_hi"] = None

    # Rule: Gulika conjunct a benefic (Jupiter or Venus in same house)
    benefics_in_gulika_house = []
    if planet_houses:
        for ben in ("Jupiter", "Venus"):
            if planet_houses.get(ben) == gulika_house:
                benefics_in_gulika_house.append(ben)
    if benefics_in_gulika_house:
        ben_str = " and ".join(benefics_in_gulika_house)
        ben_str_hi = " एवं ".join(
            ("बृहस्पति" if b == "Jupiter" else "शुक्र") for b in benefics_in_gulika_house
        )
        results["Gulika"]["benefic_conjunction_en"] = (
            f"Gulika is conjoined by {ben_str} in house {gulika_house}. "
            f"The benefic presence partially counters Gulika's malefic influence, "
            f"reducing adversity and offering protection from sudden calamities. "
            f"Classical texts (Phaladeepika Adh. 22) note that benefic association mitigates Gulika's harm."
        )
        results["Gulika"]["benefic_conjunction_hi"] = (
            f"गुलिक भाव {gulika_house} में {ben_str_hi} से युक्त है। "
            f"शुभ ग्रह की उपस्थिति गुलिक के पापी प्रभाव को आंशिक रूप से नियंत्रित करती है, "
            f"विपत्ति को कम करती और आकस्मिक आपदाओं से सुरक्षा देती है। "
            f"फलदीपिका अध्याय 22 के अनुसार शुभ-युति गुलिक की पीड़ा कम करती है।"
        )
    else:
        results["Gulika"]["benefic_conjunction_en"] = None
        results["Gulika"]["benefic_conjunction_hi"] = None

    mandi_hour = start_time + (saturn_index + 0.5) * part_len
    if mandi_hour >= 24.0:
        mandi_hour -= 24.0
    mh = int(mandi_hour)
    mm = int((mandi_hour - mh) * 60)
    m_time_str = f"{mh:02d}:{mm:02d}:00"
    m_pos = calculate_planet_positions(birth_date, m_time_str, lat, lon, tz_offset)
    mandi_lon = m_pos["ascendant"]["longitude"]
    m_sign = get_sign_from_longitude(mandi_lon)
    m_nak = get_nakshatra_from_longitude(mandi_lon)
    mandi_house = _compute_house(mandi_lon, asc_lon)
    m_interp_en, m_interp_hi = _build_interpretation("Mandi", mandi_house)
    m_nature = _UPAGRAHA_NATURES["Mandi"]
    m_mit_factors, m_mit_en, m_mit_hi = _build_mitigating_factors(
        mandi_house, _asc_sign, planet_houses, planet_signs
    )
    results["Mandi"] = {
        "longitude": round(mandi_lon, 4),
        "sign": m_sign,
        "sign_degree": round(mandi_lon % 30, 4),
        "nakshatra": m_nak["name"],
        "nakshatra_pada": m_nak["pada"],
        "house": mandi_house,
        "nature": m_nature[0],
        "classical_meaning_en": m_nature[1],
        "classical_meaning_hi": m_nature[2],
        "interpretation_en": m_interp_en,
        "interpretation_hi": m_interp_hi,
        "mitigating_factors": m_mit_factors,
        "mitigating_effect_en": m_mit_en or None,
        "mitigating_effect_hi": m_mit_hi or None,
    }

    return results
