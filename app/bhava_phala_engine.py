"""
bhava_phala_engine.py — Classical Bhava Phala + Bhava-misra-phala
==================================================================
Implements Phaladeepika Adhyaya 8 (Bhava Phala — planet-in-house results)
and Adhyaya 16 (Bhava-misra-phala — general house-wise status).

Data:
  app/data/bhava_phala.json
    - planets.<Planet>.<house> → {effect_en, effect_hi, sloka_ref}
    - bhavas.<house> → {name_en, name_hi, general_en, general_hi, sloka_ref}

Main function:
  analyze_bhava_phala(chart_data) -> dict
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

# ───────────────────────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────────────────────

_PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# Natural benefics and malefics (classical)
NATURAL_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Sign → Lord
_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Exaltation sign for each planet
_EXALTATION: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
    "Rahu": "Taurus", "Ketu": "Scorpio",
}

# Debilitation sign for each planet
_DEBILITATION: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
    "Rahu": "Scorpio", "Ketu": "Taurus",
}

# Own signs (mooltrikona/own)
_OWN_SIGNS: Dict[str, set] = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
    "Rahu": set(), "Ketu": set(),
}

# Special aspects (additional beyond universal 7th) — from aspects_engine
_SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}

DUSTHANAS = {6, 8, 12}

# Mooltrikona sign per planet (Phaladeepika Adh. 1)
_MOOLTRIKONA: Dict[str, str] = {
    "Sun": "Leo", "Moon": "Taurus", "Mars": "Aries",
    "Mercury": "Virgo", "Jupiter": "Sagittarius",
    "Venus": "Libra", "Saturn": "Aquarius",
}

# Planets with two lordships (dual-owned signs)
_DUAL_LORDS: Dict[str, List[str]] = {
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
}

# ───────────────────────────────────────────────────────────────
# Data loading
# ───────────────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "bhava_phala.json")
_DATA_CACHE: Optional[Dict[str, Any]] = None


def load_bhava_phala_data() -> Dict[str, Any]:
    """Load and cache bhava_phala JSON."""
    global _DATA_CACHE
    if _DATA_CACHE is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _DATA_CACHE = json.load(f)
    return _DATA_CACHE


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _house(p: Dict[str, Any]) -> int:
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _sign(p: Dict[str, Any]) -> str:
    return str(p.get("sign", ""))


def _planet_aspects_house(planet: str, planet_house: int, target_house: int) -> bool:
    """Return True if planet in planet_house aspects target_house (Vedic drishti).

    Uses classical Vedic "Nth house from planet" semantics (inclusive).
    A planet in house X aspects house = ((X - 1 + (N - 1)) % 12) + 1.
    Universal 7th aspect for all planets. Special aspects per planet:
      Mars: 4, 8;  Jupiter: 5, 9;  Saturn: 3, 10;  Rahu/Ketu: 5, 9.
    """
    if not (1 <= planet_house <= 12) or not (1 <= target_house <= 12):
        return False
    offsets = [7] + list(_SPECIAL_ASPECTS.get(planet, []))
    for n in offsets:
        target = ((planet_house - 1 + (n - 1)) % 12) + 1
        if target == target_house:
            return True
    return False


def _is_strong_planet(planet: str, sign: str) -> bool:
    """Planet is strong if exalted, in own sign, or mooltrikona."""
    if not sign:
        return False
    if _EXALTATION.get(planet) == sign:
        return True
    if sign in _OWN_SIGNS.get(planet, set()):
        return True
    return False


def _is_weak_planet(planet: str, sign: str) -> bool:
    """Planet is weak if debilitated."""
    return bool(sign) and _DEBILITATION.get(planet) == sign


# ───────────────────────────────────────────────────────────────
# House-strength computation
# ───────────────────────────────────────────────────────────────

def _house_strength(house: int, chart: Dict[str, Any]) -> str:
    """
    Compute classical strength of a bhava.

    strong:  benefic occupant OR benefic aspect, AND lord of house is strong
             (exalted / own sign / mooltrikona)
    weak:    malefic occupant with NO benefic aspect, OR lord in dusthana /
             debilitated
    neutral: otherwise
    """
    if not isinstance(chart, dict) or not (1 <= house <= 12):
        return "neutral"

    planets = chart.get("planets") or {}
    houses = chart.get("houses") or []
    ascendant = chart.get("ascendant") or {}
    asc_sign = str(ascendant.get("sign", ""))

    # Determine sign of the house
    house_sign = ""
    if isinstance(houses, list):
        for h in houses:
            if isinstance(h, dict) and int(h.get("number", 0) or 0) == house:
                house_sign = str(h.get("sign", ""))
                break
    if not house_sign and asc_sign:
        # Derive from ascendant using whole-sign system
        zodiac = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        ]
        if asc_sign in zodiac:
            idx = zodiac.index(asc_sign)
            house_sign = zodiac[(idx + house - 1) % 12]

    house_lord = _SIGN_LORD.get(house_sign, "")

    # Occupant analysis
    has_benefic_occupant = False
    has_malefic_occupant = False
    for planet, pdata in planets.items():
        if not isinstance(pdata, dict):
            continue
        if _house(pdata) != house:
            continue
        if planet in NATURAL_BENEFICS:
            has_benefic_occupant = True
        elif planet in NATURAL_MALEFICS:
            has_malefic_occupant = True

    # Aspect analysis
    has_benefic_aspect = False
    has_malefic_aspect = False
    for planet, pdata in planets.items():
        if not isinstance(pdata, dict):
            continue
        ph = _house(pdata)
        if ph == house or ph == 0:
            continue
        if _planet_aspects_house(planet, ph, house):
            if planet in NATURAL_BENEFICS:
                has_benefic_aspect = True
            elif planet in NATURAL_MALEFICS:
                has_malefic_aspect = True

    # Lord analysis
    lord_strong = False
    lord_weak = False
    lord_in_dusthana = False
    if house_lord and isinstance(planets.get(house_lord), dict):
        lord_data = planets[house_lord]
        lord_sign = _sign(lord_data)
        lord_house = _house(lord_data)
        lord_strong = _is_strong_planet(house_lord, lord_sign)
        lord_weak = _is_weak_planet(house_lord, lord_sign)
        if lord_house in DUSTHANAS:
            lord_in_dusthana = True

    # Strong: benefic occupant/aspect AND lord strong
    if (has_benefic_occupant or has_benefic_aspect) and lord_strong:
        return "strong"

    # Weak: lord in dusthana or debilitated, OR malefic occupant with no benefic help
    if lord_weak or lord_in_dusthana:
        return "weak"
    if has_malefic_occupant and not has_benefic_aspect and not has_benefic_occupant:
        return "weak"

    return "neutral"


# ───────────────────────────────────────────────────────────────
# Main analysis
# ───────────────────────────────────────────────────────────────

def analyze_bhava_phala(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return Bhava Phala + Bhava-misra-phala analysis.

    Output:
    {
      "planet_placements": [
        {planet, house, sign, effect_en, effect_hi, sloka_ref}, ...
      ],
      "bhava_generals": [
        {house, name_en, name_hi, general_en, general_hi, sloka_ref, status}, ...
      ],
      "sloka_ref": "Phaladeepika Adh. 8 + Adh. 16"
    }
    """
    result: Dict[str, Any] = {
        "planet_placements": [],
        "bhava_generals": [],
        "sloka_ref": "Phaladeepika Adh. 8 + Adh. 16",
    }

    if not isinstance(chart_data, dict):
        # Still emit bhava generals with neutral status, even with no chart data
        data = load_bhava_phala_data()
        for h in range(1, 13):
            info = data["bhavas"].get(str(h), {})
            result["bhava_generals"].append({
                "house": h,
                "name_en": info.get("name_en", ""),
                "name_hi": info.get("name_hi", ""),
                "general_en": info.get("general_en", ""),
                "general_hi": info.get("general_hi", ""),
                "sloka_ref": info.get("sloka_ref", ""),
                "status": "neutral",
            })
        return result

    data = load_bhava_phala_data()
    planets_raw = chart_data.get("planets") or {}

    # ── Planet placements ─────────────────────────────────────
    for planet in _PLANET_ORDER:
        pdata = planets_raw.get(planet)
        if not isinstance(pdata, dict):
            continue
        house = _house(pdata)
        sign = _sign(pdata)
        if not (1 <= house <= 12):
            continue
        entry = data["planets"].get(planet, {}).get(str(house), {})
        if not entry:
            continue

        placement: Dict[str, Any] = {
            "planet": planet,
            "house": house,
            "sign": sign,
            "effect_en": entry.get("effect_en", ""),
            "effect_hi": entry.get("effect_hi", ""),
            "sloka_ref": entry.get("sloka_ref", ""),
        }

        # P0-2: Rahu/Ketu results modified by sign lord (Phaladeepika Adh. 8)
        if planet in ("Rahu", "Ketu") and sign:
            base_planet = "Saturn" if planet == "Rahu" else "Mars"
            sign_lord = _SIGN_LORD.get(sign, "")
            if sign_lord and sign_lord != base_planet:
                placement["sign_lord_modifier_en"] = (
                    f"{planet} acts like {base_planet} by nature, but its results in "
                    f"{sign} are further coloured by its sign lord {sign_lord}. "
                    f"The effects of {sign_lord}'s placement and strength modify "
                    f"the house {house} results of {planet}."
                )
                placement["sign_lord_modifier_hi"] = (
                    f"{planet} स्वभाव से {base_planet} जैसा फल देता है, किन्तु "
                    f"{sign} राशि में इसके परिणाम भावेश {sign_lord} से भी प्रभावित होते हैं। "
                    f"{sign_lord} की स्थिति एवं बल भाव {house} में {planet} के फल को संशोधित करते हैं।"
                )

        result["planet_placements"].append(placement)

    # ── Bhava generals (all 12) with mooltrikona note ─────────

    # ── Bhava generals (all 12) ───────────────────────────────
    # Build sign→house lookup for mooltrikona rule
    ascendant = chart_data.get("ascendant") or {}
    asc_sign = str(ascendant.get("sign", ""))
    _zodiac = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]
    sign_to_house: Dict[str, int] = {}
    if asc_sign in _zodiac:
        asc_idx = _zodiac.index(asc_sign)
        for i, s in enumerate(_zodiac):
            sign_to_house[s] = ((i - asc_idx) % 12) + 1

    for h in range(1, 13):
        info = data["bhavas"].get(str(h), {})
        bhava_entry: Dict[str, Any] = {
            "house": h,
            "name_en": info.get("name_en", ""),
            "name_hi": info.get("name_hi", ""),
            "general_en": info.get("general_en", ""),
            "general_hi": info.get("general_hi", ""),
            "sloka_ref": info.get("sloka_ref", ""),
            "status": _house_strength(h, chart_data),
        }

        # P0-3: Mooltrikona gets better effect (Phaladeepika Adh. 15-16)
        # When a planet rules two bhavas, the mooltrikona bhava receives better results.
        house_sign = ""
        if asc_sign in _zodiac:
            house_sign = _zodiac[((_zodiac.index(asc_sign) + h - 1) % 12)]
        if house_sign:
            lord = _SIGN_LORD.get(house_sign, "")
            if lord in _DUAL_LORDS:
                mlt_sign = _MOOLTRIKONA.get(lord, "")
                if mlt_sign and mlt_sign == house_sign:
                    other_sign = [s for s in _DUAL_LORDS[lord] if s != house_sign]
                    other_house = sign_to_house.get(other_sign[0], 0) if other_sign else 0
                    bhava_entry["mooltrikona_note_en"] = (
                        f"{lord} rules both house {h} ({house_sign}) and house {other_house} "
                        f"({other_sign[0] if other_sign else ''}). Since {house_sign} is "
                        f"{lord}'s Mooltrikona sign, house {h} receives the primary and better "
                        f"results of {lord} (Phaladeepika Adh. 15)."
                    )
                    bhava_entry["mooltrikona_note_hi"] = (
                        f"{lord} भाव {h} ({house_sign}) और भाव {other_house} "
                        f"({other_sign[0] if other_sign else ''}) दोनों का स्वामी है। "
                        f"{house_sign} {lord} की मूलत्रिकोण राशि होने से भाव {h} को "
                        f"{lord} के श्रेष्ठ फल प्राप्त होते हैं (फलदीपिका अ. 15)।"
                    )

        result["bhava_generals"].append(bhava_entry)

    return result
