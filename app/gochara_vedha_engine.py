"""
gochara_vedha_engine.py — Gochara Vedha + Latta Analysis
=========================================================
Implements Adhyaya 26 of Phaladeepika (slokas 29-40).

Two classical modifiers applied on top of basic Gochara:
  1. VEDHA (obstruction) — a good transit is cancelled when another planet
     occupies the "vedha house" from natal Moon for that transit.
  2. LATTA (kick) — when a transiting planet lands at a specific nakshatra
     distance from natal Moon's nakshatra, the transit is strengthened
     (Prishta +25%) or weakened (Pratyak −25%).

Usage:
    from app.gochara_vedha_engine import apply_vedhas, apply_lattas, enrich_transits
    enriched = enrich_transits(transits_list, natal_chart_data)
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional, Tuple

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
ZODIAC_INDEX = {sign: idx for idx, sign in enumerate(ZODIAC)}

# Standard 27-nakshatra sequence — each span 13°20' = 13.3333°
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
NAKSHATRA_INDEX = {name: i for i, name in enumerate(NAKSHATRAS)}
NAKSHATRA_SPAN = 360.0 / 27  # 13.333...

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
_VEDHA_CACHE: Optional[Dict[str, Any]] = None
_LATTA_CACHE: Optional[Dict[str, Any]] = None


def load_vedha_table() -> Dict[str, Any]:
    global _VEDHA_CACHE
    if _VEDHA_CACHE is None:
        with open(os.path.join(_DATA_DIR, "gochara_vedhas.json"), "r", encoding="utf-8") as f:
            _VEDHA_CACHE = json.load(f)
    return _VEDHA_CACHE


def load_latta_table() -> Dict[str, Any]:
    global _LATTA_CACHE
    if _LATTA_CACHE is None:
        with open(os.path.join(_DATA_DIR, "latta_table.json"), "r", encoding="utf-8") as f:
            _LATTA_CACHE = json.load(f)
    return _LATTA_CACHE


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _house_from_moon(moon_sign: str, transit_sign: str) -> int:
    """Return house number (1-12) of transit_sign counted from moon_sign.
    House 1 = same sign as Moon."""
    if moon_sign not in ZODIAC_INDEX or transit_sign not in ZODIAC_INDEX:
        return 0
    moon_idx = ZODIAC_INDEX[moon_sign]
    t_idx = ZODIAC_INDEX[transit_sign]
    return ((t_idx - moon_idx) % 12) + 1


def _nakshatra_from_longitude(longitude: float) -> str:
    """Return nakshatra name for an absolute longitude 0-360."""
    try:
        lon = float(longitude) % 360
    except (TypeError, ValueError):
        return ""
    idx = int(lon // NAKSHATRA_SPAN) % 27
    return NAKSHATRAS[idx]


def _nakshatra_distance(from_nak: str, to_nak: str) -> int:
    """
    Count forward distance in nakshatras (1-based) from `from_nak` to `to_nak`.
    Same nakshatra = 1, next = 2, etc. Wraps around 27.
    """
    if from_nak not in NAKSHATRA_INDEX or to_nak not in NAKSHATRA_INDEX:
        return 0
    return ((NAKSHATRA_INDEX[to_nak] - NAKSHATRA_INDEX[from_nak]) % 27) + 1


def _is_exception_pair(planet_a: str, planet_b: str, vedha_data: Dict[str, Any]) -> bool:
    """Check if these two planets are in the no-vedha exception list."""
    exceptions = vedha_data.get("exceptions", [])
    pair = {planet_a, planet_b}
    return any(pair == set(ex) for ex in exceptions)


# ───────────────────────────────────────────────────────────────
# Vedha
# ───────────────────────────────────────────────────────────────

def apply_vedhas(
    transits: List[Dict[str, Any]],
    natal_chart: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    For each transit entry, check if another transiting planet occupies the
    vedha house from natal Moon → mark cancellation.

    Each input entry needs: planet, current_sign (or sign), effect (optional).
    Adds fields: vedha_active, vedha_by, effect_final.
    """
    if not transits:
        return []
    if not isinstance(natal_chart, dict):
        natal_chart = {}

    vedha_data = load_vedha_table()
    natal_planets = natal_chart.get("planets", {}) or {}
    natal_moon = natal_planets.get("Moon") or {}
    moon_sign = str(natal_moon.get("sign", ""))
    if not moon_sign:
        # Can't compute houses-from-moon without natal Moon → return unchanged
        for t in transits:
            t.setdefault("vedha_active", False)
            t.setdefault("vedha_by", None)
            t.setdefault("effect_final", t.get("effect", ""))
        return transits

    # Precompute each transit planet's house from natal Moon
    occupancy: Dict[int, List[str]] = {}  # house → [planet names]
    for t in transits:
        p = t.get("planet", "")
        sign = t.get("current_sign") or t.get("sign", "")
        if not p or not sign:
            continue
        house = _house_from_moon(moon_sign, sign)
        if house > 0:
            occupancy.setdefault(house, []).append(p)

    enriched: List[Dict[str, Any]] = []
    for t in transits:
        planet = t.get("planet", "")
        sign = t.get("current_sign") or t.get("sign", "")
        house_from_moon = _house_from_moon(moon_sign, sign) if sign else 0

        t_out = dict(t)  # copy
        t_out["natal_house_from_moon"] = house_from_moon

        planet_vedha = vedha_data.get(planet, {})
        good_houses = set(planet_vedha.get("good", []))
        vedha_map = planet_vedha.get("vedhas", {})  # {"3": 9, ...}

        is_good = house_from_moon in good_houses
        vedha_active = False
        vedha_by: Optional[Dict[str, Any]] = None

        if is_good:
            vedha_house = vedha_map.get(str(house_from_moon))
            if vedha_house:
                # Find transit planets occupying the vedha_house (excluding this planet and exception pairs)
                candidates = [
                    p2 for p2 in occupancy.get(int(vedha_house), [])
                    if p2 != planet and not _is_exception_pair(planet, p2, vedha_data)
                ]
                if candidates:
                    vedha_active = True
                    canceller = candidates[0]
                    vedha_by = {
                        "planet": canceller,
                        "house": vedha_house,
                        "description_en": f"{canceller} in house {vedha_house} from natal Moon cancels {planet}'s good transit in house {house_from_moon}",
                        "description_hi": f"जन्म चंद्र से भाव {vedha_house} में स्थित {canceller}, {planet} की {house_from_moon} भाव की शुभ युति को निरस्त करता है",
                        "sloka_ref": "Phaladeepika Adh. 26 sloka 29-33",
                    }

        base_effect = t.get("effect") or ("favorable" if is_good else "unfavorable")
        effect_final = "cancelled" if vedha_active else base_effect

        t_out.update({
            "effect_base": base_effect,
            "effect_final": effect_final,
            "vedha_active": vedha_active,
            "vedha_by": vedha_by,
        })
        enriched.append(t_out)

    return enriched


# ───────────────────────────────────────────────────────────────
# Latta
# ───────────────────────────────────────────────────────────────

def apply_lattas(
    transits: List[Dict[str, Any]],
    natal_chart: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    For each transit entry, compute nakshatra distance from natal Moon nakshatra.
    If distance matches planet's Prishta → +25% strength.
    If distance matches planet's Pratyak → −25% strength.

    Adds fields: latta_modifier (float), latta_type ("prishta"|"pratyak"|None).
    """
    if not transits:
        return []
    if not isinstance(natal_chart, dict):
        natal_chart = {}

    latta_table = load_latta_table()
    natal_planets = natal_chart.get("planets", {}) or {}
    natal_moon = natal_planets.get("Moon") or {}
    # Natal Moon nakshatra — either explicit or derived from longitude
    moon_nak = natal_moon.get("nakshatra", "")
    if not moon_nak:
        moon_nak = _nakshatra_from_longitude(natal_moon.get("longitude", 0))

    enriched: List[Dict[str, Any]] = []
    for t in transits:
        t_out = dict(t)
        planet = t.get("planet", "")
        distances = latta_table.get(planet)

        if not moon_nak or not distances:
            t_out.setdefault("latta_modifier", 1.0)
            t_out.setdefault("latta_type", None)
            enriched.append(t_out)
            continue

        # Transit planet's current nakshatra
        transit_nak = t.get("nakshatra", "") or _nakshatra_from_longitude(
            (t.get("planet_info") or {}).get("longitude", t.get("longitude", 0))
        )

        if not transit_nak:
            t_out.setdefault("latta_modifier", 1.0)
            t_out.setdefault("latta_type", None)
            enriched.append(t_out)
            continue

        distance = _nakshatra_distance(moon_nak, transit_nak)
        modifier = 1.0
        latta_type: Optional[str] = None
        description_en: Optional[str] = None
        description_hi: Optional[str] = None

        if distance == distances.get("prishta"):
            modifier = 1.25
            latta_type = "prishta"
            description_en = f"Prishta Latta: {planet} strengthens transit (+25%) — at nakshatra {distance} from natal Moon"
            description_hi = f"प्रिष्ठ लत्ता: {planet} युति को बलवान (+25%) — जन्म चंद्र से {distance} नक्षत्र पर"
        elif distance == distances.get("pratyak"):
            modifier = 0.75
            latta_type = "pratyak"
            description_en = f"Pratyak Latta: {planet} weakens transit (−25%) — at nakshatra {distance} from natal Moon"
            description_hi = f"प्रत्यक् लत्ता: {planet} युति को दुर्बल (−25%) — जन्म चंद्र से {distance} नक्षत्र पर"

        t_out.update({
            "latta_modifier": modifier,
            "latta_type": latta_type,
            "latta_nakshatra_distance": distance,
            "latta_description_en": description_en,
            "latta_description_hi": description_hi,
        })
        enriched.append(t_out)

    return enriched


# ───────────────────────────────────────────────────────────────
# Combined enrichment
# ───────────────────────────────────────────────────────────────

def enrich_transits(
    transits: List[Dict[str, Any]],
    natal_chart: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Apply Vedha + Latta classical modifiers in sequence.
    Returns the enriched transit list (new entries, original dicts preserved).
    """
    with_vedhas = apply_vedhas(transits, natal_chart)
    with_lattas = apply_lattas(with_vedhas, natal_chart)
    # Add sloka reference to each entry for traceability
    for t in with_lattas:
        t.setdefault("sloka_ref", "Phaladeepika Adh. 26")
    return with_lattas
