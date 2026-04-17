"""
vritti_engine.py — Classical Vritti (Livelihood / Career) analysis
===================================================================
Implements Phaladeepika Adhyaya 5 (Vritti — means of livelihood).

Classical method:
  1. Identify the lord of the 10th house from the ascendant.
  2. Compute that lord's navamsa (D9) sign; the lord of that navamsa-sign
     becomes the navamsa-lord → primary vocation indicator.
  3. Among Sun, Moon and Lagna-lord, the strongest contributes a secondary
     signature to the livelihood.

Data file:
  app/data/vritti_rules.json
    - navamsa_vocations.<Planet>           (primary/secondary + examples, bilingual)
    - tenth_lord_placements.<HouseOrdinal> (effect text, bilingual)
    - strongest_luminary_effects.<KEY>     (implication, bilingual)

Public API:
  analyze_vritti(chart_data: dict) -> dict
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────

_SIGN_NAMES: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

# Dignity tables (classical)
_EXALTATION: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
    "Rahu": "Taurus", "Ketu": "Scorpio",
}
_DEBILITATION: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
    "Rahu": "Scorpio", "Ketu": "Taurus",
}
_OWN_SIGNS: Dict[str, set] = {
    "Sun": {"Leo"},
    "Moon": {"Cancer"},
    "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"},
    "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"},
    "Saturn": {"Capricorn", "Aquarius"},
}

_KENDRAS = {1, 4, 7, 10}
_TRIKONAS = {1, 5, 9}
_DUSTHANAS = {6, 8, 12}

_PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                 "Saturn", "Rahu", "Ketu"]

# ─────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "vritti_rules.json")
_DATA_CACHE: Optional[Dict[str, Any]] = None


def load_vritti_data() -> Dict[str, Any]:
    """Load and cache vritti_rules JSON."""
    global _DATA_CACHE
    if _DATA_CACHE is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _DATA_CACHE = json.load(f)
    return _DATA_CACHE


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _sign_index(sign: str) -> int:
    """Return 0-indexed position of a sign name, -1 if unknown."""
    try:
        return _SIGN_NAMES.index(sign)
    except (ValueError, TypeError):
        return -1


def _ordinal(h: int) -> str:
    """Return '1st' / '2nd' / '3rd' / 'Nth' for house number 1..12."""
    if h == 1:
        return "1st"
    if h == 2:
        return "2nd"
    if h == 3:
        return "3rd"
    return f"{h}th"


def _navamsa_sign(longitude: float) -> str:
    """
    Compute the navamsa (D9) sign for a planet's sidereal longitude.

    Fire signs (Aries, Leo, Sagittarius) start from Aries;
    Earth signs (Taurus, Virgo, Capricorn) start from Capricorn;
    Air signs (Gemini, Libra, Aquarius) start from Libra;
    Water signs (Cancer, Scorpio, Pisces) start from Cancer.
    """
    try:
        lon = float(longitude) % 360.0
    except (TypeError, ValueError):
        return ""
    part_size = 30.0 / 9.0
    rasi_index = int(lon / 30.0)
    degree_in_sign = lon - rasi_index * 30.0
    part = min(int(degree_in_sign / part_size), 8)
    element = rasi_index % 4  # 0 Fire, 1 Earth, 2 Air, 3 Water
    start_sign = {0: 0, 1: 9, 2: 6, 3: 3}[element]
    return _SIGN_NAMES[(start_sign + part) % 12]


def _ascendant_sign(chart: Dict[str, Any]) -> str:
    asc = chart.get("ascendant") or {}
    return str(asc.get("sign", "") or "")


def _sign_of_house(chart: Dict[str, Any], house: int) -> str:
    """Return the whole-sign house-sign given an ascendant sign."""
    asc = _ascendant_sign(chart)
    idx = _sign_index(asc)
    if idx < 0 or not (1 <= house <= 12):
        return ""
    return _SIGN_NAMES[(idx + house - 1) % 12]


def _lord_of_tenth(chart: Dict[str, Any]) -> str:
    """Return the planet that lords the 10th house from the ascendant."""
    tenth_sign = _sign_of_house(chart, 10)
    return _SIGN_LORD.get(tenth_sign, "")


def _planet_info(chart: Dict[str, Any], planet: str) -> Dict[str, Any]:
    """Return the chart.planets[planet] dict safely."""
    planets = chart.get("planets") or {}
    if not isinstance(planets, dict):
        return {}
    info = planets.get(planet)
    return info if isinstance(info, dict) else {}


def _planet_longitude(chart: Dict[str, Any], planet: str) -> Optional[float]:
    info = _planet_info(chart, planet)
    lon = info.get("longitude")
    try:
        return float(lon) if lon is not None else None
    except (TypeError, ValueError):
        return None


def _planet_house(chart: Dict[str, Any], planet: str) -> int:
    info = _planet_info(chart, planet)
    try:
        return int(info.get("house", 0) or 0)
    except (TypeError, ValueError):
        return 0


def _planet_sign(chart: Dict[str, Any], planet: str) -> str:
    info = _planet_info(chart, planet)
    return str(info.get("sign", "") or "")


def _dignity_score(planet: str, sign: str) -> int:
    """Score 0..5 for classical dignity."""
    if not sign:
        return 0
    if _EXALTATION.get(planet) == sign:
        return 5
    if sign in _OWN_SIGNS.get(planet, set()):
        return 4
    if _DEBILITATION.get(planet) == sign:
        return 0
    return 2  # neutral


def _house_score(house: int) -> int:
    if house in _KENDRAS:
        return 3
    if house in _TRIKONAS:
        return 2
    if house in _DUSTHANAS:
        return 0
    return 1


def _strongest_luminary(chart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score Sun, Moon and Lagna (via its lord) on dignity + house placement.
    Return {"strongest", "sun_score", "moon_score", "lagna_score",
            "reasoning_en", "reasoning_hi"}.
    """
    # Sun
    sun_sign = _planet_sign(chart, "Sun")
    sun_house = _planet_house(chart, "Sun")
    sun_score = _dignity_score("Sun", sun_sign) + _house_score(sun_house)

    # Moon
    moon_sign = _planet_sign(chart, "Moon")
    moon_house = _planet_house(chart, "Moon")
    moon_score = _dignity_score("Moon", moon_sign) + _house_score(moon_house)

    # Lagna — use Lagna lord
    asc_sign = _ascendant_sign(chart)
    lagna_lord = _SIGN_LORD.get(asc_sign, "")
    if lagna_lord:
        ll_sign = _planet_sign(chart, lagna_lord)
        ll_house = _planet_house(chart, lagna_lord)
        lagna_score = _dignity_score(lagna_lord, ll_sign) + _house_score(ll_house)
    else:
        lagna_score = 0

    ranking = [("sun", sun_score), ("moon", moon_score), ("lagna", lagna_score)]
    strongest = max(ranking, key=lambda x: x[1])[0]

    reasoning_en = (
        f"Sun={sun_score}, Moon={moon_score}, Lagna(lord={lagna_lord or 'n/a'})"
        f"={lagna_score}. Winner: {strongest}."
    )
    reasoning_hi = (
        f"सूर्य={sun_score}, चन्द्र={moon_score}, "
        f"लग्न(लग्नेश={lagna_lord or 'अज्ञात'})={lagna_score}। "
        f"सर्वाधिक बली: {strongest}।"
    )

    return {
        "strongest": strongest,
        "sun_score": sun_score,
        "moon_score": moon_score,
        "lagna_score": lagna_score,
        "lagna_lord": lagna_lord,
        "reasoning_en": reasoning_en,
        "reasoning_hi": reasoning_hi,
    }


def _empty_result() -> Dict[str, Any]:
    """Return a minimal, safe default structure."""
    return {
        "primary_vocation": {
            "vocation_en": "",
            "vocation_hi": "",
            "derivation": "",
            "sloka_ref": "Phaladeepika Adh. 5",
        },
        "tenth_lord_info": {
            "planet": "",
            "navamsa_sign": "",
            "navamsa_lord": "",
            "placement_house": 0,
            "placement_sign": "",
            "placement_effect_en": "",
            "placement_effect_hi": "",
        },
        "luminary_strength": {
            "strongest": "",
            "sun_score": 0,
            "moon_score": 0,
            "lagna_score": 0,
            "lagna_lord": "",
            "reasoning_en": "",
            "reasoning_hi": "",
            "implication_en": "",
            "implication_hi": "",
        },
        "recommended_fields_en": [],
        "recommended_fields_hi": [],
        "avoid_fields_en": [],
        "avoid_fields_hi": [],
        "sloka_ref": "Phaladeepika Adh. 5",
    }


# ─────────────────────────────────────────────────────────────
# Main analysis
# ─────────────────────────────────────────────────────────────

def analyze_vritti(chart_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Run classical Adh. 5 Vritti analysis on a chart.

    The chart is expected to match the output of
    app.astro_engine.calculate_planet_positions:
      {
        "planets": { "Sun": {"longitude", "sign", "house", ...}, ... },
        "ascendant": {"sign": "...", "longitude": ...}, ...
      }
    """
    result = _empty_result()

    if not isinstance(chart_data, dict):
        return result

    data = load_vritti_data()
    navamsa_map = data.get("navamsa_vocations", {})
    tenth_map = data.get("tenth_lord_placements", {})
    luminary_map = data.get("strongest_luminary_effects", {})

    # ── 10th lord + navamsa ─────────────────────────────────
    tenth_lord = _lord_of_tenth(chart_data)
    tenth_lord_long = _planet_longitude(chart_data, tenth_lord) if tenth_lord else None
    nav_sign = _navamsa_sign(tenth_lord_long) if tenth_lord_long is not None else ""
    nav_lord = _SIGN_LORD.get(nav_sign, "") if nav_sign else ""

    # If the 10th lord is Rahu or Ketu (cannot happen classically, but chart can
    # place a rasi-lord that is also a node; keep guard), we still use nav_lord
    # of the navamsa sign. If nav_lord cannot be computed, fall back to
    # the 10th lord itself to produce a meaningful vocation key.
    vocation_key = nav_lord or tenth_lord

    # Placement house of the 10th lord
    placement_house = _planet_house(chart_data, tenth_lord) if tenth_lord else 0
    placement_sign = _planet_sign(chart_data, tenth_lord) if tenth_lord else ""

    # ── Luminary strength ────────────────────────────────────
    lum = _strongest_luminary(chart_data)
    lum_key = f"{lum['strongest'].capitalize()}_strongest"
    lum_entry = luminary_map.get(lum_key, {})
    lum["implication_en"] = lum_entry.get("implication_en", "")
    lum["implication_hi"] = lum_entry.get("implication_hi", "")
    lum["sloka_ref"] = lum_entry.get("sloka_ref", "")

    # ── Primary vocation text ────────────────────────────────
    nav_entry = navamsa_map.get(vocation_key, {})
    primary_en = nav_entry.get("primary_en", "")
    primary_hi = nav_entry.get("primary_hi", "")
    sloka_primary = nav_entry.get("sloka_ref", "Phaladeepika Adh. 5")

    derivation_bits: List[str] = []
    if tenth_lord:
        derivation_bits.append(f"10th lord = {tenth_lord}")
    if nav_sign:
        derivation_bits.append(f"navamsa sign = {nav_sign}")
    if nav_lord:
        derivation_bits.append(f"navamsa lord = {nav_lord}")
    if vocation_key:
        derivation_bits.append(f"vocation key = {vocation_key}")
    derivation = "; ".join(derivation_bits)

    result["primary_vocation"] = {
        "vocation_en": primary_en,
        "vocation_hi": primary_hi,
        "derivation": derivation,
        "sloka_ref": sloka_primary,
    }

    # ── 10th lord info ──────────────────────────────────────
    tenth_entry = tenth_map.get(_ordinal(placement_house), {}) if placement_house else {}
    result["tenth_lord_info"] = {
        "planet": tenth_lord,
        "navamsa_sign": nav_sign,
        "navamsa_lord": nav_lord,
        "placement_house": placement_house,
        "placement_sign": placement_sign,
        "placement_effect_en": tenth_entry.get("effect_en", ""),
        "placement_effect_hi": tenth_entry.get("effect_hi", ""),
        "sloka_ref": tenth_entry.get("sloka_ref", ""),
    }

    # ── Luminary strength (fill) ────────────────────────────
    result["luminary_strength"] = lum

    # ── Recommended + avoid fields ──────────────────────────
    # Only emit recommended / avoid lists when we have a real vocation match.
    rec_en: List[str] = []
    rec_hi: List[str] = []
    avoid_en_set: List[str] = []
    avoid_hi_set: List[str] = []

    if vocation_key and vocation_key in navamsa_map:
        rec_en = list(nav_entry.get("examples_en", []) or [])
        rec_hi = list(nav_entry.get("examples_hi", []) or [])

        # Avoid = union of examples from OTHER planets (complement),
        # deduplicated and capped to keep the UI tidy.
        seen_en = set(rec_en)
        seen_hi = set(rec_hi)
        for planet in _PLANET_ORDER:
            if planet == vocation_key:
                continue
            entry = navamsa_map.get(planet, {})
            for e in entry.get("examples_en", []) or []:
                if e not in seen_en:
                    avoid_en_set.append(e)
                    seen_en.add(e)
            for e in entry.get("examples_hi", []) or []:
                if e not in seen_hi:
                    avoid_hi_set.append(e)
                    seen_hi.add(e)

    # Cap avoid list to 10 representative items per language
    result["recommended_fields_en"] = rec_en
    result["recommended_fields_hi"] = rec_hi
    result["avoid_fields_en"] = avoid_en_set[:10]
    result["avoid_fields_hi"] = avoid_hi_set[:10]

    result["sloka_ref"] = "Phaladeepika Adh. 5"
    return result
