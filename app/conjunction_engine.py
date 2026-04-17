"""
conjunction_engine.py — Pair-wise Planetary Conjunctions
=========================================================
Implements Adhyaya 18 of Phaladeepika.

Detection: two planets within a given orb (default 8°) in the SAME sign.
Also detects planet-with-Lagna conjunctions (planet in 1st house).

Special Yogas surfaced:
  - Budhaditya (Sun + Mercury)
  - Gaja-Kesari (Moon + Jupiter in Kendra from Lagna)
  - Chandra-Mangal (Moon + Mars)
  - Guru-Mangal (Jupiter + Mars)
  - Guru-Chandal (Jupiter + Rahu)
  - Angarak (Mars + Rahu)
  - Shrapit (Saturn + Rahu)
  - Vish (Moon + Saturn)
  - Grahan Dosha (Sun/Moon + Rahu/Ketu)
  - Mahapurusha candidates (planet + Lagna in own/exalted sign)
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

# ───────────────────────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────────────────────

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

KENDRAS = {1, 4, 7, 10}
DUSTHANAS = {6, 8, 12}

DEFAULT_ORB_DEGREES = 8.0


# ───────────────────────────────────────────────────────────────
# Data loading
# ───────────────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "conjunction_effects.json")
_DATA_CACHE: Optional[List[Dict[str, Any]]] = None


def load_conjunction_data() -> List[Dict[str, Any]]:
    """Load and cache conjunction effects JSON."""
    global _DATA_CACHE
    if _DATA_CACHE is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _DATA_CACHE = json.load(f)
    return _DATA_CACHE


def _build_pair_index() -> Dict[frozenset, Dict[str, Any]]:
    """Index conjunction entries by frozenset(planets) for O(1) lookup."""
    index: Dict[frozenset, Dict[str, Any]] = {}
    for entry in load_conjunction_data():
        key = frozenset(entry.get("planets") or [])
        if len(key) == 2:
            index[key] = entry
    return index


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _longitude(p: Dict[str, Any]) -> float:
    try:
        return float(p.get("longitude", p.get("sign_degree", 0))) % 360
    except (TypeError, ValueError):
        return 0.0


def _degree_separation(a: float, b: float) -> float:
    """Angular distance 0-180 between two longitudes."""
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _sign(p: Dict[str, Any]) -> str:
    return str(p.get("sign", ""))


def _house(p: Dict[str, Any]) -> int:
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


# ───────────────────────────────────────────────────────────────
# Main detection
# ───────────────────────────────────────────────────────────────

def detect_conjunctions(
    chart_data: Dict[str, Any],
    orb_degrees: float = DEFAULT_ORB_DEGREES,
) -> List[Dict[str, Any]]:
    """
    Return list of detected conjunctions.

    Each entry:
    {
        "planets": [...], "house": int, "sign": str, "orb": float,
        "key": str, "name_en": str, "name_hi": str, "nature": str,
        "effect_en": str, "effect_hi": str,
        "enhanced": bool, "enhanced_en": ... | None, "enhanced_hi": ... | None,
        "weakened": bool, "weakened_en": ... | None, "weakened_hi": ... | None,
        "special_yoga": str | None,
        "sloka_ref": str,
    }
    """
    if not isinstance(chart_data, dict):
        return []
    planets_raw = chart_data.get("planets") or {}
    if not planets_raw:
        return []

    index = _build_pair_index()
    results: List[Dict[str, Any]] = []

    # Filter to planets with sign data
    planet_names = [n for n in planets_raw if isinstance(planets_raw.get(n), dict)]

    # ── Planet-planet conjunctions ─────────────────────────────
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1, p2 = planet_names[i], planet_names[j]
            d1, d2 = planets_raw[p1], planets_raw[p2]
            if _sign(d1) != _sign(d2) or not _sign(d1):
                continue
            orb = _degree_separation(_longitude(d1), _longitude(d2))
            if orb > orb_degrees:
                continue

            entry = index.get(frozenset([p1, p2]))
            if not entry:
                continue  # unknown pair — skip silently

            house = _house(d1)
            enhanced = house in KENDRAS and entry.get("enhanced_en") is not None
            # Weakened marker currently used only to flag that a softening rule exists.
            # We don't auto-detect weakening aspects here (would need aspect engine).
            weakened = False

            results.append({
                "key": entry["key"],
                "planets": list(entry["planets"]),
                "house": house,
                "sign": _sign(d1),
                "orb": round(orb, 2),
                "name_en": entry.get("name_en", ""),
                "name_hi": entry.get("name_hi", ""),
                "nature": entry.get("nature", "mixed"),
                "effect_en": entry.get("effect_en", ""),
                "effect_hi": entry.get("effect_hi", ""),
                "enhanced": enhanced,
                "enhanced_en": entry.get("enhanced_en"),
                "enhanced_hi": entry.get("enhanced_hi"),
                "weakened": weakened,
                "weakened_en": entry.get("weakened_en"),
                "weakened_hi": entry.get("weakened_hi"),
                "special_yoga": entry.get("special_yoga"),
                "sloka_ref": entry.get("sloka_ref", ""),
            })

    # ── Planet-Lagna conjunctions ──────────────────────────────
    # A planet is "with Lagna" when it sits in the 1st house (sign match with ascendant).
    asc = chart_data.get("ascendant") or {}
    asc_sign = str(asc.get("sign", ""))
    if asc_sign:
        for planet in planet_names:
            pdata = planets_raw[planet]
            if _house(pdata) != 1:
                continue
            if _sign(pdata) != asc_sign:
                # Require same sign as ascendant for a true Lagna conjunction
                continue
            entry = index.get(frozenset([planet, "Lagna"]))
            if not entry:
                continue

            # Orb measured against ascendant longitude when available
            asc_lon = 0.0
            try:
                asc_lon = float(asc.get("longitude", 0))
            except (TypeError, ValueError):
                asc_lon = 0.0
            orb = _degree_separation(_longitude(pdata), asc_lon)

            results.append({
                "key": entry["key"],
                "planets": list(entry["planets"]),
                "house": 1,
                "sign": asc_sign,
                "orb": round(orb, 2),
                "name_en": entry.get("name_en", ""),
                "name_hi": entry.get("name_hi", ""),
                "nature": entry.get("nature", "mixed"),
                "effect_en": entry.get("effect_en", ""),
                "effect_hi": entry.get("effect_hi", ""),
                "enhanced": False,
                "enhanced_en": entry.get("enhanced_en"),
                "enhanced_hi": entry.get("enhanced_hi"),
                "weakened": False,
                "weakened_en": entry.get("weakened_en"),
                "weakened_hi": entry.get("weakened_hi"),
                "special_yoga": entry.get("special_yoga"),
                "sloka_ref": entry.get("sloka_ref", ""),
            })

    # Stable sort: by house, then by orb (tightest first)
    results.sort(key=lambda r: (r["house"], r["orb"]))
    return results
