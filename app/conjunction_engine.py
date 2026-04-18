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
from typing import Any, Dict, List, Optional, Tuple

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
# Effect strength helpers
# ───────────────────────────────────────────────────────────────

TRIKONAS = {1, 5, 9}

DEBILITATION_SIGN: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries",
}


def _is_debilitated(planet: str, sign: str) -> bool:
    return DEBILITATION_SIGN.get(planet) == sign


def _calc_effect_strength(
    p1: str, d1: Dict[str, Any],
    p2: str, d2: Dict[str, Any],
    house: int,
) -> Tuple[str, str, str]:
    """
    Return (effect_strength, reason_en, reason_hi).
    Rules (Phaladeepika Adh. 18):
      - REVERSED: both planets debilitated OR conjunction in 8th with both malefics
      - PARTIAL:  one planet debilitated/combust OR conjunction in dusthana (6/8/12)
      - FULL:     conjunction in kendra (1/4/7/10) or trikona (1/5/9) with no weakness
    """
    sign1 = str(d1.get("sign", ""))
    sign2 = str(d2.get("sign", ""))

    both_debi = _is_debilitated(p1, sign1) and _is_debilitated(p2, sign2)
    malefics = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
    both_malefic_8th = (house == 8 and p1 in malefics and p2 in malefics)

    if both_debi or both_malefic_8th:
        if both_debi:
            reason_en = f"Both {p1} and {p2} are debilitated — conjunction gives reversed results."
            reason_hi = f"{p1} और {p2} दोनों नीच राशि में — युति विपरीत फल देती है।"
        else:
            reason_en = f"Two malefics ({p1}, {p2}) conjunct in 8th house — reversed results."
            reason_hi = f"दो पाप ग्रह ({p1}, {p2}) अष्टम भाव में — विपरीत फल।"
        return "reversed", reason_en, reason_hi

    one_debi = _is_debilitated(p1, sign1) or _is_debilitated(p2, sign2)
    # Combust check: a planet is combust when status contains 'combust'
    def _is_combust(d: Dict[str, Any]) -> bool:
        return "combust" in str(d.get("status", "")).lower()

    one_combust = _is_combust(d1) or _is_combust(d2)
    in_dusthana = house in {6, 8, 12}

    if one_debi or one_combust or in_dusthana:
        if one_debi:
            weak = p1 if _is_debilitated(p1, sign1) else p2
            reason_en = f"{weak} is debilitated — conjunction gives partial (50%) results."
            reason_hi = f"{weak} नीच राशि में — युति आंशिक (50%) फल देती है।"
        elif one_combust:
            reason_en = "One planet is combust — conjunction gives partial results."
            reason_hi = "एक ग्रह अस्त है — युति आंशिक फल देती है।"
        else:
            reason_en = f"Conjunction in dusthana (house {house}) — partial results."
            reason_hi = f"युति दुःस्थान (भाव {house}) में — आंशिक फल।"
        return "partial", reason_en, reason_hi

    kendra_or_trikona = house in (KENDRAS | TRIKONAS)
    if kendra_or_trikona:
        reason_en = f"Both planets strong, conjunction in house {house} (kendra/trikona) — full results."
        reason_hi = f"दोनों ग्रह बलवान, भाव {house} (केंद्र/त्रिकोण) में युति — पूर्ण फल।"
    else:
        reason_en = f"Conjunction in house {house} — full results."
        reason_hi = f"भाव {house} में युति — पूर्ण फल।"
    return "full", reason_en, reason_hi


def _check_d12_conjunction(
    p1: str, p2: str,
    planet_longitudes: Dict[str, float],
    orb_degrees: float = DEFAULT_ORB_DEGREES,
) -> bool:
    """
    Check if the same planet pair is also conjunct in D12 (Dwadasamsa).
    D12: each sign (30°) is divided into 12 parts of 2.5° each.
    """
    if p1 not in planet_longitudes or p2 not in planet_longitudes:
        return False
    lon1 = planet_longitudes[p1]
    lon2 = planet_longitudes[p2]

    def _d12_sign_index(lon: float) -> int:
        sign_idx = int(lon / 30.0) % 12
        deg_in_sign = lon % 30.0
        part = int(deg_in_sign / 2.5)  # 0-11
        return (sign_idx + part) % 12

    return _d12_sign_index(lon1) == _d12_sign_index(lon2)


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
        "effect_strength": "full"|"partial"|"reversed",
        "effect_strength_reason_en": str,
        "effect_strength_reason_hi": str,
        "d12_also_conjunct": bool,
        "d12_amplified_en": str | None,
        "d12_amplified_hi": str | None,
    }
    """
    if not isinstance(chart_data, dict):
        return []
    planets_raw = chart_data.get("planets") or {}
    if not planets_raw:
        return []

    # Build planet_longitudes for D12 check
    planet_longitudes: Dict[str, float] = {}
    for pn, pi in planets_raw.items():
        if isinstance(pi, dict):
            try:
                planet_longitudes[pn] = float(pi.get("longitude", pi.get("sign_degree", 0)))
            except (TypeError, ValueError):
                pass

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

            effect_strength, reason_en, reason_hi = _calc_effect_strength(
                p1, d1, p2, d2, house
            )
            d12_conj = _check_d12_conjunction(p1, p2, planet_longitudes, orb_degrees)
            if d12_conj:
                d12_amp_en = (
                    f"{p1} and {p2} are also conjunct in D12 (Dwadasamsa) — "
                    "their effects on parents and ancestry are amplified."
                )
                d12_amp_hi = (
                    f"{p1} और {p2} D12 (द्वादशांश) में भी युत हैं — "
                    "माता-पिता और पूर्वजों पर प्रभाव प्रबल होता है।"
                )
            else:
                d12_amp_en = None
                d12_amp_hi = None

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
                "effect_strength": effect_strength,
                "effect_strength_reason_en": reason_en,
                "effect_strength_reason_hi": reason_hi,
                "d12_also_conjunct": d12_conj,
                "d12_amplified_en": d12_amp_en,
                "d12_amplified_hi": d12_amp_hi,
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

            pdata = planets_raw[planet]
            # Lagna is always in house 1 (kendra) — treat as "full" by default
            lagna_strength, lagna_reason_en, lagna_reason_hi = _calc_effect_strength(
                planet, pdata, "Lagna", {"sign": asc_sign}, 1
            )

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
                "effect_strength": lagna_strength,
                "effect_strength_reason_en": lagna_reason_en,
                "effect_strength_reason_hi": lagna_reason_hi,
                "d12_also_conjunct": False,
                "d12_amplified_en": None,
                "d12_amplified_hi": None,
            })

    # Stable sort: by house, then by orb (tightest first)
    results.sort(key=lambda r: (r["house"], r["orb"]))
    return results
