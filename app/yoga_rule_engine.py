"""
yoga_rule_engine.py — Declarative Yoga Rule Evaluator
======================================================
Evaluates JSON-encoded yoga rules against chart data.

Supported rule types:
  - AND, OR, NOT (combinators)
  - planet_in_houses
  - planet_in_own_or_exaltation
  - planet_in_house_from_moon / planet_in_house_from_sun
  - count_benefics_in_houses_from_moon
  - no_planet_in_houses_from_moon / no_planet_in_kendra_from_moon
  - benefic_in_house / malefic_in_house
  - lord_of_house_in_houses
  - lords_conjunct_or_mutual
  - lord_in_own_or_exaltation_in_houses
  - planet_aspects_planet / planet_aspects_house / planet_aspects_planet (target_lord_of)
  - planet_involved
  - moon_in_strong_sign
  - all_planets_in_sign_category (movable/fixed/dual)
  - all_planets_in_kendras / *_in_2_kendras / *_contiguous_*
  - benefics_only_in_kendras / malefics_only_in_kendras
  - benefics_in_kendras_malefics_in_3_6_9_12
  - benefics_in_1_7_malefics_in_4_10
  - planets_in_odd_houses_only / planets_in_even_houses_only
  - planets_in_kendras_and_trikonas_only
  - all_planets_in_1_7_only / all_planets_in_4_10_only / all_planets_in_1_5_9_only
  - all_planets_in_2_6_10_or_3_7_11_or_4_8_12
  - all_planets_in_contiguous_4_houses_from_lagna / from_4 / from_7 / from_10
  - all_planets_in_panapharas_or_apoklimas
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

EXALTATION_SIGN = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra",
}
DEBILITATION_SIGN = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries",
}

MOVABLE = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
PANAPHARAS = {2, 5, 8, 11}
APOKLIMAS = {3, 6, 9, 12}
UPACHAYAS = {3, 6, 10, 11}

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
# Strict benefics (Mercury and Moon treated as conditional — for "three benefics" checks)
STRICT_BENEFICS = {"Jupiter", "Venus", "Mercury"}
STRICT_MALEFICS = {"Sun", "Mars", "Saturn"}
CLASSICAL_7 = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}

SPECIAL_ASPECTS = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "yogas.json")
_YOGA_CACHE: Optional[List[Dict[str, Any]]] = None


def load_yoga_rules() -> List[Dict[str, Any]]:
    global _YOGA_CACHE
    if _YOGA_CACHE is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _YOGA_CACHE = json.load(f)
    return _YOGA_CACHE


# ───────────────────────────────────────────────────────────────
# Chart helpers
# ───────────────────────────────────────────────────────────────

def _planets(chart: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return chart.get("planets") or {}

def _asc_sign(chart: Dict[str, Any]) -> str:
    return (chart.get("ascendant") or {}).get("sign", "")

def _house_of(planet: str, planets: Dict[str, Dict[str, Any]]) -> int:
    p = planets.get(planet) or {}
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0

def _sign_of(planet: str, planets: Dict[str, Dict[str, Any]]) -> str:
    p = planets.get(planet) or {}
    return str(p.get("sign", ""))

def _houses_aspected_by(planet: str, planets: Dict[str, Dict[str, Any]]) -> List[int]:
    h = _house_of(planet, planets)
    if h < 1 or h > 12:
        return []
    out = [((h - 1 + 6) % 12) + 1]
    for off in SPECIAL_ASPECTS.get(planet, []):
        out.append(((h - 1 + off - 1) % 12) + 1)
    return out

def _lord_of_house(house: int, asc_sign: str) -> str:
    if asc_sign not in ZODIAC or not (1 <= house <= 12):
        return ""
    sign = ZODIAC[(ZODIAC.index(asc_sign) + house - 1) % 12]
    return SIGN_LORD.get(sign, "")

def _is_exalted(planet: str, sign: str) -> bool:
    return EXALTATION_SIGN.get(planet) == sign

def _is_own(planet: str, sign: str) -> bool:
    return SIGN_LORD.get(sign) == planet


# ───────────────────────────────────────────────────────────────
# Rule evaluation
# ───────────────────────────────────────────────────────────────

def evaluate_rule(rule: Dict[str, Any], chart: Dict[str, Any]) -> bool:
    """Evaluate a single rule (possibly composite) against chart data."""
    if not isinstance(rule, dict):
        return False
    rtype = rule.get("type", "")

    # ── Combinators ──
    if rtype == "AND":
        return all(evaluate_rule(r, chart) for r in rule.get("conditions", []))
    if rtype == "OR":
        return any(evaluate_rule(r, chart) for r in rule.get("conditions", []))
    if rtype == "NOT":
        return not evaluate_rule(rule.get("condition", {}), chart)

    planets = _planets(chart)
    asc = _asc_sign(chart)

    # ── Simple placement rules ──
    if rtype == "planet_in_houses":
        p = rule.get("planet", "")
        houses = set(rule.get("houses", []))
        return p in planets and _house_of(p, planets) in houses

    if rtype == "planet_in_own_or_exaltation":
        p = rule.get("planet", "")
        if p not in planets:
            return False
        s = _sign_of(p, planets)
        return _is_own(p, s) or _is_exalted(p, s)

    if rtype == "benefic_in_house":
        h = int(rule.get("house", 0))
        return any(b in planets and _house_of(b, planets) == h for b in BENEFICS)

    if rtype == "malefic_in_house":
        h = int(rule.get("house", 0))
        return any(m in planets and _house_of(m, planets) == h for m in MALEFICS)

    if rtype == "planet_involved":
        # planet is in any of the listed houses
        p = rule.get("planet", "")
        houses = set(rule.get("in_houses", []))
        return p in planets and _house_of(p, planets) in houses

    if rtype == "moon_in_strong_sign":
        s = _sign_of("Moon", planets)
        return _is_exalted("Moon", s) or _is_own("Moon", s)

    # ── Moon-relative rules ──
    if rtype == "planet_in_house_from_moon":
        off = int(rule.get("offset", 0))
        exclude = set(rule.get("exclude", []))
        mh = _house_of("Moon", planets)
        if mh < 1:
            return False
        target = ((mh - 1 + off - 1) % 12) + 1
        return any(
            p not in exclude and _house_of(p, planets) == target
            for p in planets if p != "Moon"
        )

    if rtype == "no_planet_in_houses_from_moon":
        offsets = rule.get("offsets", [])
        mh = _house_of("Moon", planets)
        if mh < 1:
            return True
        targets = {((mh - 1 + o - 1) % 12) + 1 for o in offsets}
        exclude = {"Moon", "Sun", "Rahu", "Ketu"}
        return not any(
            p not in exclude and _house_of(p, planets) in targets
            for p in planets
        )

    if rtype == "no_planet_in_kendra_from_moon":
        mh = _house_of("Moon", planets)
        if mh < 1:
            return True
        kendra_targets = {((mh - 1 + o - 1) % 12) + 1 for o in (1, 4, 7, 10)}
        exclude = {"Moon"}
        return not any(
            p not in exclude and _house_of(p, planets) in kendra_targets
            for p in planets
        )

    if rtype == "count_benefics_in_houses_from_moon":
        offsets = rule.get("offsets", [])
        op = rule.get("operator", ">=")
        want = int(rule.get("count", 1))
        mh = _house_of("Moon", planets)
        if mh < 1:
            return False
        targets = {((mh - 1 + o - 1) % 12) + 1 for o in offsets}
        count = sum(
            1 for b in STRICT_BENEFICS
            if b in planets and _house_of(b, planets) in targets
        )
        if op == ">=":
            return count >= want
        if op == "==":
            return count == want
        if op == ">":
            return count > want
        return False

    # ── Sun-relative rules ──
    if rtype == "planet_in_house_from_sun":
        off = int(rule.get("offset", 0))
        exclude = set(rule.get("exclude", []))
        sh = _house_of("Sun", planets)
        if sh < 1:
            return False
        target = ((sh - 1 + off - 1) % 12) + 1
        return any(
            p not in exclude and _house_of(p, planets) == target
            for p in planets if p != "Sun"
        )

    # ── Lord rules ──
    if rtype == "lord_of_house_in_houses":
        lo = int(rule.get("lord_of", 0))
        houses = set(rule.get("in_houses", []))
        lord = _lord_of_house(lo, asc)
        return lord in planets and _house_of(lord, planets) in houses

    if rtype == "lord_in_own_or_exaltation_in_houses":
        lo = int(rule.get("lord_of", 0))
        houses = set(rule.get("in_houses", []))
        lord = _lord_of_house(lo, asc)
        if lord not in planets:
            return False
        s = _sign_of(lord, planets)
        if not (_is_own(lord, s) or _is_exalted(lord, s)):
            return False
        return _house_of(lord, planets) in houses

    if rtype == "lords_conjunct_or_mutual":
        la = int(rule.get("lord_a", 0))
        lb = int(rule.get("lord_b", 0))
        in_houses = set(rule.get("in_houses", []))
        lord_a = _lord_of_house(la, asc)
        lord_b = _lord_of_house(lb, asc)
        if not (lord_a and lord_b) or lord_a not in planets or lord_b not in planets:
            return False
        ha = _house_of(lord_a, planets)
        hb = _house_of(lord_b, planets)
        # Conjunct (same house) and in allowed set
        if ha == hb and ha in in_houses:
            return True
        # Mutual aspect (opposite houses and both in allowed set)
        if ha in in_houses and hb in in_houses:
            if abs(ha - hb) == 6 or abs(ha - hb) == 0:
                return True
        # Additionally allow: both lords sit in any pair from in_houses (broad interpretation)
        return ha in in_houses and hb in in_houses

    # ── Aspect rules ──
    if rtype == "planet_aspects_planet":
        src = rule.get("source", "")
        tgt = rule.get("target", "")
        if rule.get("target_lord_of"):
            tgt = _lord_of_house(int(rule["target_lord_of"]), asc)
        if not (src in planets and tgt in planets):
            return False
        th = _house_of(tgt, planets)
        return th in _houses_aspected_by(src, planets)

    if rtype == "planet_aspects_house":
        src = rule.get("source", "")
        h = int(rule.get("house", 0))
        return src in planets and h in _houses_aspected_by(src, planets)

    # ── Nabhasa / distribution rules ──
    if rtype == "all_planets_in_sign_category":
        category = rule.get("category", "")
        cat_set = {"movable": MOVABLE, "fixed": FIXED, "dual": DUAL}.get(category)
        if not cat_set:
            return False
        return all(
            p in planets and _sign_of(p, planets) in cat_set
            for p in CLASSICAL_7
        )

    if rtype == "benefics_only_in_kendras":
        # All three strict benefics are in Kendras, and no malefic in Kendras
        in_kendras = [
            b for b in STRICT_BENEFICS
            if b in planets and _house_of(b, planets) in KENDRAS
        ]
        return len(in_kendras) >= 3

    if rtype == "malefics_only_in_kendras":
        in_kendras = [
            m for m in STRICT_MALEFICS
            if m in planets and _house_of(m, planets) in KENDRAS
        ]
        return len(in_kendras) >= 3

    if rtype == "benefics_in_kendras_malefics_in_3_6_9_12":
        benefics_ok = all(
            b in planets and _house_of(b, planets) in KENDRAS
            for b in STRICT_BENEFICS
        )
        malefics_ok = all(
            m in planets and _house_of(m, planets) in {3, 6, 9, 12}
            for m in STRICT_MALEFICS
        )
        return benefics_ok and malefics_ok

    if rtype == "benefics_in_1_7_malefics_in_4_10":
        benefics_ok = all(
            b in planets and _house_of(b, planets) in {1, 7}
            for b in STRICT_BENEFICS
        )
        malefics_ok = all(
            m in planets and _house_of(m, planets) in {4, 10}
            for m in STRICT_MALEFICS
        )
        return benefics_ok and malefics_ok

    if rtype == "all_planets_in_two_kendras":
        # All 7 classical planets fall into exactly 2 Kendras
        houses = {_house_of(p, planets) for p in CLASSICAL_7 if p in planets}
        houses = {h for h in houses if h in KENDRAS}
        return len(houses) == 2 and all(
            p in planets and _house_of(p, planets) in KENDRAS for p in CLASSICAL_7
        )

    if rtype == "all_planets_in_1_7_only":
        return _all_in(planets, {1, 7})

    if rtype == "all_planets_in_4_10_only":
        return _all_in(planets, {4, 10})

    if rtype == "all_planets_in_1_5_9_only":
        return _all_in(planets, {1, 5, 9})

    if rtype == "all_planets_in_2_6_10_or_3_7_11_or_4_8_12":
        return _all_in(planets, {2, 6, 10}) or _all_in(planets, {3, 7, 11}) or _all_in(planets, {4, 8, 12})

    if rtype == "all_planets_in_kendras":
        return _all_in(planets, KENDRAS)

    if rtype == "all_planets_in_panapharas_or_apoklimas":
        return _all_in(planets, PANAPHARAS) or _all_in(planets, APOKLIMAS)

    if rtype == "planets_in_kendras_and_trikonas_only":
        return _all_in(planets, KENDRAS | TRIKONAS)

    if rtype == "planets_in_odd_houses_only":
        return _all_in(planets, {1, 3, 5, 7, 9, 11})

    if rtype == "planets_in_even_houses_only":
        return _all_in(planets, {2, 4, 6, 8, 10, 12})

    if rtype == "all_planets_in_contiguous_4_houses_from_lagna":
        return _all_in(planets, {1, 2, 3, 4})

    if rtype == "all_planets_in_contiguous_4_houses_from_4":
        return _all_in(planets, {4, 5, 6, 7})

    if rtype == "all_planets_in_contiguous_4_houses_from_7":
        return _all_in(planets, {7, 8, 9, 10})

    if rtype == "all_planets_in_contiguous_4_houses_from_10":
        return _all_in(planets, {10, 11, 12, 1})

    # Unknown rule type — conservative false
    return False


def _all_in(planets: Dict[str, Dict[str, Any]], allowed_houses: set) -> bool:
    """True iff all 7 classical planets are in houses within `allowed_houses`."""
    return all(
        p in planets and _house_of(p, planets) in allowed_houses
        for p in CLASSICAL_7
    )


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def detect_all_yogas(
    chart_data: Dict[str, Any],
    category_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Evaluate all declarative yogas against chart. Returns matched yogas with metadata.
    If category_filter is set, only that category is evaluated.
    """
    if not isinstance(chart_data, dict):
        return []
    if not _planets(chart_data):
        return []

    matches: List[Dict[str, Any]] = []
    for yoga in load_yoga_rules():
        if category_filter and yoga.get("category") != category_filter:
            continue
        try:
            if evaluate_rule(yoga.get("rules", {}), chart_data):
                matches.append({
                    "key": yoga["key"],
                    "name_en": yoga.get("name_en", ""),
                    "name_hi": yoga.get("name_hi", ""),
                    "category": yoga.get("category", ""),
                    "category_label_en": yoga.get("category_label_en", ""),
                    "category_label_hi": yoga.get("category_label_hi", ""),
                    "effect_en": yoga.get("effect_en", ""),
                    "effect_hi": yoga.get("effect_hi", ""),
                    "sloka_ref": yoga.get("sloka_ref", ""),
                    "nature": yoga.get("nature", "mixed"),
                })
        except Exception:
            continue
    return matches


def list_categories() -> List[str]:
    """Return sorted unique categories present in the yoga database."""
    return sorted({y.get("category", "") for y in load_yoga_rules() if y.get("category")})
