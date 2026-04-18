"""
planet_properties_engine.py — Phaladeepika Adh. 1–2 Planet Properties
======================================================================

Implements classical Vedic astrology classification systems from
Phaladeepika Adhyayas 1 and 2 (Mantreshvara):

  Feature #18 — Stage of Life (graha svabhava / Baladi Avastha)
    Each planet has a fixed natural stage (Youth / Child / Mature / Old)
    AND a degree-based dynamic stage per sign position (Bala → Mrita).

  Feature #20 — Sattvika / Rajasa / Tamasa guna classification
    Each planet is assigned one of the three Prakritic gunas.

  Feature #21 — Shirodaya / Prusthodaya / Ubhaodaya rising mode
    Each sign has a classical "rising mode" that characterises when in
    life the Lagna delivers its strongest results.

  Feature #22 — Sun/Moon Parent Rule (Adhyaya 2)
    Day chart (Sun in houses 7-12): Sun=father, Moon=mother.
    Night chart (Sun in houses 1-6): Saturn=father, Venus=mother.

  Feature #23 — Mercury Hermaphrodite Gender Rule (Adhyaya 2)
    Mercury adopts the gender of conjunct planets.

  Feature #24 — Planet Metals, Grains, Trees (Adhyaya 2)
    Each planet rules a classical metal, grain, and sacred tree.

Public API:
    get_planet_properties(chart_data)   → per-planet stage + guna + avastha + metals/grains/trees
    get_lagna_rising_analysis(chart_data) → lagna rising mode details

Data source:
    app/data/planet_properties.json
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, Tuple

# ── Data Loading ─────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "planet_properties.json")

_DATA: Optional[Dict[str, Any]] = None


def _load_data() -> Dict[str, Any]:
    global _DATA
    if _DATA is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as fh:
            _DATA = json.load(fh)
    return _DATA


# ── Sign Constants ───────────────────────────────────────────────────

_SIGN_NAMES = [
    "Aries",       # 1  — odd
    "Taurus",      # 2  — even
    "Gemini",      # 3  — odd
    "Cancer",      # 4  — even
    "Leo",         # 5  — odd
    "Virgo",       # 6  — even
    "Libra",       # 7  — odd
    "Scorpio",     # 8  — even
    "Sagittarius", # 9  — odd
    "Capricorn",   # 10 — even
    "Aquarius",    # 11 — odd
    "Pisces",      # 12 — even
]

# Sign number (1-based) -> True if odd
_ODD_SIGN: Dict[int, bool] = {i + 1: (i + 1) % 2 == 1 for i in range(12)}

# Name to 1-based sign number
_SIGN_NUMBER: Dict[str, int] = {name: i + 1 for i, name in enumerate(_SIGN_NAMES)}

ALL_PLANETS = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
)

# ── Feature 24 — Planet Metals, Grains, Trees (Phaladeepika Adh. 2) ──
_PLANET_MATERIALS: Dict[str, Dict[str, str]] = {
    "Sun": {
        "metal_en": "Gold",
        "metal_hi": "सोना",
        "grain_en": "Wheat",
        "grain_hi": "गेहूँ",
        "tree_en": "Bel Tree (Aegle marmelos)",
        "tree_hi": "बेल (श्रीफल)",
    },
    "Moon": {
        "metal_en": "Silver",
        "metal_hi": "चाँदी",
        "grain_en": "Rice",
        "grain_hi": "चावल",
        "tree_en": "Palash Tree (Butea monosperma)",
        "tree_hi": "पलाश (ढाक)",
    },
    "Mars": {
        "metal_en": "Copper / Brass",
        "metal_hi": "ताँबा / पीतल",
        "grain_en": "Red Lentils (Masoor)",
        "grain_hi": "मसूर",
        "tree_en": "Khadira Tree (Acacia catechu)",
        "tree_hi": "खदिर (कत्था)",
    },
    "Mercury": {
        "metal_en": "Bronze / Mixed Alloys",
        "metal_hi": "काँसा / मिश्र-धातु",
        "grain_en": "Green Gram (Moong)",
        "grain_hi": "मूँग",
        "tree_en": "Apamarga Tree (Achyranthes aspera)",
        "tree_hi": "अपामार्ग (चिरचिटा)",
    },
    "Jupiter": {
        "metal_en": "Gold / Yellow Metals",
        "metal_hi": "सोना / पीत-धातु",
        "grain_en": "Chickpeas (Chana)",
        "grain_hi": "चना",
        "tree_en": "Peepal Tree (Ficus religiosa)",
        "tree_hi": "पीपल",
    },
    "Venus": {
        "metal_en": "Silver / White Metals",
        "metal_hi": "चाँदी / श्वेत-धातु",
        "grain_en": "White Beans",
        "grain_hi": "सफ़ेद लोबिया",
        "tree_en": "Oudumbara / Cluster Fig (Ficus racemosa)",
        "tree_hi": "उदुम्बर (गूलर)",
    },
    "Saturn": {
        "metal_en": "Iron / Lead",
        "metal_hi": "लोहा / सीसा",
        "grain_en": "Sesame (Til)",
        "grain_hi": "तिल",
        "tree_en": "Shami Tree (Prosopis cineraria)",
        "tree_hi": "शमी",
    },
}

# ── Feature 22 — Day/Night Chart (Phaladeepika Adh. 2) ───────────────
# Sun in houses 7-12 = Day chart; houses 1-6 = Night chart
_DAY_CHART_HOUSES = {7, 8, 9, 10, 11, 12}


def _get_day_night_indicator(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determine day/night chart and parent indicators.
    Day chart (Sun above horizon, houses 7-12): Sun=father, Moon=mother.
    Night chart (Sun below horizon, houses 1-6): Saturn=father, Venus=mother.
    """
    planets = chart_data.get("planets", {})
    sun_data = planets.get("Sun", {})
    sun_house = int(sun_data.get("house", 0) or 0)

    is_day_chart = sun_house in _DAY_CHART_HOUSES

    if is_day_chart:
        chart_type = "day"
        chart_type_hi = "दिन-कुण्डली"
        father = "Sun"
        father_hi = "सूर्य"
        mother = "Moon"
        mother_hi = "चन्द्र"
        reason_en = "Sun is above the horizon (houses 7–12) — Day chart rule applies."
        reason_hi = "सूर्य क्षितिज के ऊपर है (भाव 7–12) — दिन-कुण्डली का नियम लागू।"
    else:
        chart_type = "night"
        chart_type_hi = "रात्रि-कुण्डली"
        father = "Saturn"
        father_hi = "शनि"
        mother = "Venus"
        mother_hi = "शुक्र"
        reason_en = "Sun is below the horizon (houses 1–6) — Night chart rule applies."
        reason_hi = "सूर्य क्षितिज के नीचे है (भाव 1–6) — रात्रि-कुण्डली का नियम लागू।"

    return {
        "day_night_chart": chart_type,
        "day_night_chart_hi": chart_type_hi,
        "sun_house": sun_house,
        "father_indicator": {
            "planet": father,
            "planet_hi": father_hi,
            "reason_en": reason_en,
            "reason_hi": reason_hi,
        },
        "mother_indicator": {
            "planet": mother,
            "planet_hi": mother_hi,
            "reason_en": reason_en,
            "reason_hi": reason_hi,
        },
        "sloka_ref": "Phaladeepika Adh. 2",
    }


# ── Feature 23 — Mercury Gender Rule (Phaladeepika Adh. 2) ───────────
_MALE_PLANETS = {"Sun", "Mars", "Jupiter"}
_FEMALE_PLANETS = {"Moon", "Venus"}

# Vedic aspect offsets (house-based) per planet
_PLANET_ASPECT_OFFSETS: Dict[str, List[int]] = {
    "Sun": [7],
    "Moon": [7],
    "Mars": [4, 7, 8],
    "Mercury": [7],
    "Jupiter": [5, 7, 9],
    "Venus": [7],
    "Saturn": [3, 7, 10],
    "Rahu": [5, 7, 9],
    "Ketu": [5, 7, 9],
}

_NATURAL_BENEFICS = {"Moon", "Jupiter", "Venus", "Mercury"}
_NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


def _get_mercury_gender_state(chart_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Mercury adopts the gender of planets conjunct with it.
    Conjunct = same house as Mercury.
    Male planets: Sun, Mars, Jupiter → Mercury becomes male.
    Female planets: Moon, Venus → Mercury becomes female.
    Both or none → neutral.
    """
    planets = chart_data.get("planets", {})
    mercury_data = planets.get("Mercury")
    if mercury_data is None:
        return None

    mercury_house = int(mercury_data.get("house", 0) or 0)
    conjunct_planets = []

    for pname, pdata in planets.items():
        if pname == "Mercury":
            continue
        if isinstance(pdata, dict):
            ph = int(pdata.get("house", 0) or 0)
            if ph and ph == mercury_house:
                conjunct_planets.append(pname)

    male_conjuncts = [p for p in conjunct_planets if p in _MALE_PLANETS]
    female_conjuncts = [p for p in conjunct_planets if p in _FEMALE_PLANETS]

    if male_conjuncts and not female_conjuncts:
        effective_gender = "male"
        gender_hi = "पुरुष"
        reason_en = (
            f"Mercury is conjunct with male planet(s) {', '.join(male_conjuncts)} "
            f"— adopts masculine gender."
        )
        reason_hi = (
            f"बुध पुरुष ग्रह {', '.join(male_conjuncts)} के साथ युत है — पुरुष लिंग धारण करता है।"
        )
    elif female_conjuncts and not male_conjuncts:
        effective_gender = "female"
        gender_hi = "स्त्री"
        reason_en = (
            f"Mercury is conjunct with female planet(s) {', '.join(female_conjuncts)} "
            f"— adopts feminine gender."
        )
        reason_hi = (
            f"बुध स्त्री ग्रह {', '.join(female_conjuncts)} के साथ युत है — स्त्री लिंग धारण करता है।"
        )
    elif male_conjuncts and female_conjuncts:
        effective_gender = "neutral"
        gender_hi = "नपुंसक"
        reason_en = (
            f"Mercury conjuncts both male ({', '.join(male_conjuncts)}) "
            f"and female ({', '.join(female_conjuncts)}) planets — remains neutral/hermaphrodite."
        )
        reason_hi = (
            f"बुध पुरुष ({', '.join(male_conjuncts)}) और स्त्री ({', '.join(female_conjuncts)}) "
            f"दोनों ग्रहों के साथ युत है — नपुंसक (उभयलिंगी) रहता है।"
        )
    else:
        effective_gender = "neutral"
        gender_hi = "नपुंसक"
        reason_en = "Mercury has no conjunctions — remains neutral/hermaphrodite."
        reason_hi = "बुध के साथ कोई ग्रह युत नहीं — नपुंसक (उभयलिंगी) रहता है।"

    return {
        "effective_gender": effective_gender,
        "effective_gender_hi": gender_hi,
        "reason_en": reason_en,
        "reason_hi": reason_hi,
        "conjunct_planets": conjunct_planets,
        "sloka_ref": "Phaladeepika Adh. 2",
    }


def _get_mercury_hermaphrodite_note(
    chart_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Mercury hermaphrodite nature rule (Phaladeepika Adh. 2).
    Mercury adopts the nature of planets it is conjunct with or aspected by.
    - Conjunct / aspected by malefics  → malefic-leaning
    - Conjunct / aspected by benefics  → benefic-leaning
    - Alone / mixed / neutral          → neutral
    """
    planets = chart_data.get("planets", {})
    mercury_data = planets.get("Mercury")
    if mercury_data is None:
        return None

    mercury_house = int(mercury_data.get("house", 0) or 0)
    if not mercury_house:
        return None

    # Build house -> planets mapping
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for pname, pdata in planets.items():
        if isinstance(pdata, dict):
            ph = int(pdata.get("house", 0) or 0)
            if ph:
                house_planets[ph].append(pname)

    conjunct = [p for p in house_planets.get(mercury_house, []) if p != "Mercury"]

    # Find planets that aspect Mercury's house
    aspected_by: List[str] = []
    for pname, pdata in planets.items():
        if pname == "Mercury":
            continue
        if not isinstance(pdata, dict):
            continue
        ph = int(pdata.get("house", 0) or 0)
        if not ph:
            continue
        for offset in _PLANET_ASPECT_OFFSETS.get(pname, [7]):
            target = ((ph - 1 + offset) % 12) + 1
            if target == mercury_house:
                aspected_by.append(pname)
                break

    # Remove duplicates while preserving order
    seen = set()
    all_influences: List[str] = []
    for p in conjunct + aspected_by:
        if p not in seen:
            seen.add(p)
            all_influences.append(p)

    benefic_influences = [p for p in all_influences if p in _NATURAL_BENEFICS]
    malefic_influences = [p for p in all_influences if p in _NATURAL_MALEFICS]

    if malefic_influences and not benefic_influences:
        nature = "malefic-leaning"
        nature_hi = "पाप-प्रधान"
        reason_en = (
            f"Mercury is influenced by malefic(s) {', '.join(malefic_influences)} "
            f"— adopts malefic tendencies."
        )
        reason_hi = (
            f"बुध पाप ग्रह {', '.join(malefic_influences)} के प्रभाव में है — "
            f"पाप प्रवृत्ति धारण करता है।"
        )
    elif benefic_influences and not malefic_influences:
        nature = "benefic-leaning"
        nature_hi = "शुभ-प्रधान"
        reason_en = (
            f"Mercury is influenced by benefic(s) {', '.join(benefic_influences)} "
            f"— adopts benefic tendencies."
        )
        reason_hi = (
            f"बुध शुभ ग्रह {', '.join(benefic_influences)} के प्रभाव में है — "
            f"शुभ प्रवृत्ति धारण करता है।"
        )
    else:
        nature = "neutral"
        nature_hi = "मध्यम"
        if all_influences:
            reason_en = (
                f"Mercury receives mixed influences ({', '.join(all_influences)}) "
                f"— remains neutral."
            )
            reason_hi = (
                f"बुध पर मिश्रित प्रभाव हैं ({', '.join(all_influences)}) — "
                f"मध्यम रहता है।"
            )
        else:
            reason_en = "Mercury is unaspected and unconjoined — remains neutral."
            reason_hi = "बुध पर कोई ग्रह-दृष्टि या युति नहीं — मध्यम रहता है।"

    return {
        "mercury_nature": nature,
        "mercury_nature_hi": nature_hi,
        "reason_en": reason_en,
        "reason_hi": reason_hi,
        "conjunct_planets": conjunct,
        "aspected_by": list(dict.fromkeys(aspected_by)),
        "influencing_planets": all_influences,
        "sloka_ref": "Phaladeepika Adh. 2",
    }


# ── Baladi Avastha Calculation ───────────────────────────────────────

# Stage sequence for ODD signs (degree 0 → 30):
#   0-6  = Bala, 6-12 = Kumara, 12-18 = Yuva, 18-24 = Vriddha, 24-30 = Mrita
_ODD_SEQUENCE = ["Bala", "Kumara", "Yuva", "Vriddha", "Mrita"]

# Stage sequence for EVEN signs (reversed):
#   0-6  = Mrita, 6-12 = Vriddha, 12-18 = Yuva, 18-24 = Kumara, 24-30 = Bala
_EVEN_SEQUENCE = ["Mrita", "Vriddha", "Yuva", "Kumara", "Bala"]


def _compute_baladi_avastha(
    sign_name: str,
    sign_degree: float,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Determine Baladi Avastha for a planet at `sign_degree` degrees (0-30)
    within `sign_name`.

    Returns a dict merging the stage key and stage-level data.
    """
    sign_num = _SIGN_NUMBER.get(sign_name)
    if sign_num is None:
        return {"stage": "Unknown", "name_hi": "अज्ञात", "strength_fraction": 0.0,
                "description_en": "Sign not recognised.", "description_hi": "राशि अज्ञात।"}

    deg = max(0.0, min(float(sign_degree), 29.9999))
    bucket = int(deg / 6)           # 0..4
    bucket = min(bucket, 4)

    is_odd = _ODD_SIGN[sign_num]
    sequence = _ODD_SEQUENCE if is_odd else _EVEN_SEQUENCE
    stage_key = sequence[bucket]

    stage_data = data["baladi_avastha_stages"].get(stage_key, {})
    result = {"stage": stage_key}
    result.update(stage_data)
    return result


# ── Public API ───────────────────────────────────────────────────────

def get_planet_properties(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns stage-of-life, Baladi Avastha, guna, metals/grains/trees,
    parent indicators, and Mercury gender state for each planet in the chart.

    Args:
        chart_data: must contain a "planets" key, each entry having at least:
            - "sign" (str)     — sign name, e.g. "Aries"
            - "sign_degree" (float) — degree within sign (0-30)
            - "longitude" (float, optional) — ecliptic longitude (degrees)
            - "house" (int, optional) — house number (1-12)

    Returns:
    {
      "planets": {
        "<Planet>": {
          "stage_of_life": { stage, stage_hi, description_en, description_hi },
          "guna": { guna, guna_hi, description_en, description_hi },
          "baladi_avastha": { stage, name_hi, strength_fraction, description_en, description_hi },
          "metal_en": str, "metal_hi": str,
          "grain_en": str, "grain_hi": str,
          "tree_en": str, "tree_hi": str,
          "sign_degree": float,
          "sign": str,
        },
        ...
      },
      "day_night_indicator": { day_night_chart, father_indicator, mother_indicator, ... },
      "mercury_gender_state": { effective_gender, reason_en, reason_hi, conjunct_planets } | null,
      "sloka_ref": "Phaladeepika Adh. 2"
    }
    """
    data = _load_data()
    planets_in = chart_data.get("planets", {})
    planets_out: Dict[str, Any] = {}

    for planet_name, planet_data in planets_in.items():
        sign = planet_data.get("sign", "")
        sign_degree = float(planet_data.get("sign_degree", 0.0))

        # --- Stage of Life (fixed, by planet identity) ---
        stage_of_life = data["stage_of_life"].get(planet_name)
        if stage_of_life is None:
            stage_of_life = {
                "stage": "Unknown",
                "stage_hi": "अज्ञात",
                "description_en": "No classical stage defined for this body.",
                "description_hi": "इस ग्रह के लिए कोई शास्त्रीय अवस्था परिभाषित नहीं।",
            }

        # --- Guna (fixed, by planet identity) ---
        guna = data["gunas"].get(planet_name)
        if guna is None:
            guna = {
                "guna": "Unknown",
                "guna_hi": "अज्ञात",
                "description_en": "No classical guna defined for this body.",
                "description_hi": "इस ग्रह के लिए कोई शास्त्रीय गुण परिभाषित नहीं।",
            }

        # --- Baladi Avastha (dynamic, by degree in sign) ---
        baladi = _compute_baladi_avastha(sign, sign_degree, data)

        # --- Metals, Grains, Trees (Feature 24 — Phaladeepika Adh. 2) ---
        materials = _PLANET_MATERIALS.get(planet_name, {})

        entry: Dict[str, Any] = {
            "stage_of_life": dict(stage_of_life),
            "guna": dict(guna),
            "baladi_avastha": baladi,
            "sign_degree": sign_degree,
            "sign": sign,
        }
        entry.update(materials)  # adds metal_en/hi, grain_en/hi, tree_en/hi
        planets_out[planet_name] = entry

    # --- Day/Night Chart Parent Indicators (Feature 22) ---
    day_night_indicator = _get_day_night_indicator(chart_data)

    # --- Mercury Gender State (Feature 23) ---
    mercury_gender_state = _get_mercury_gender_state(chart_data)

    # --- Mercury Hermaphrodite Nature Note (Feature 23 extended) ---
    mercury_note = _get_mercury_hermaphrodite_note(chart_data)
    if mercury_note and "Mercury" in planets_out:
        planets_out["Mercury"]["hermaphrodite_note"] = mercury_note

    return {
        "planets": planets_out,
        "day_night_indicator": day_night_indicator,
        "mercury_gender_state": mercury_gender_state,
        "sloka_ref": (
            data["sloka_refs"]["stage_of_life"]
            + " | "
            + data["sloka_refs"]["gunas"]
            + " | "
            + data["sloka_refs"]["baladi_avastha"]
        ),
    }


def get_lagna_rising_analysis(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns Shirodaya / Prusthodaya / Ubhaodaya analysis for the Lagna sign.

    Args:
        chart_data: must contain an "ascendant" key with:
            - "sign" (str)      — sign name, e.g. "Leo"
            - "longitude" (float, optional) — ecliptic longitude

    Returns:
    {
      "lagna_sign": str,
      "rising_mode": str,          # "Shirodaya" | "Prusthodaya" | "Ubhaodaya"
      "rising_mode_hi": str,
      "effect_en": str,
      "effect_hi": str,
      "sloka_ref": str
    }
    """
    data = _load_data()
    ascendant = chart_data.get("ascendant", {})
    lagna_sign = ascendant.get("sign", "")

    rising = data["rising_signs"].get(lagna_sign)
    if rising is None:
        return {
            "lagna_sign": lagna_sign,
            "rising_mode": "Unknown",
            "rising_mode_hi": "अज्ञात",
            "effect_en": f"Rising mode not defined for sign '{lagna_sign}'.",
            "effect_hi": f"'{lagna_sign}' राशि के लिए उदय-प्रकार परिभाषित नहीं।",
            "sloka_ref": data["sloka_refs"]["rising_signs"],
        }

    return {
        "lagna_sign": lagna_sign,
        "rising_mode": rising["mode"],
        "rising_mode_hi": rising["mode_hi"],
        "effect_en": rising["effect_en"],
        "effect_hi": rising["effect_hi"],
        "sloka_ref": data["sloka_refs"]["rising_signs"],
    }
