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
    tz_offset: float
) -> Dict[str, Any]:
    """
    Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas.
    Each entry includes classical house placement + bilingual interpretation.
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

    results = {}
    for p in aprakasha:
        l = p["longitude"]
        sign = get_sign_from_longitude(l)
        nak = get_nakshatra_from_longitude(l)
        house = _compute_house(l, asc_lon)
        name = p["name"]
        interp_en, interp_hi = _build_interpretation(name, house)
        nature_data = _UPAGRAHA_NATURES.get(name, ("malefic", "", ""))
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
    }

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
    }

    return results
