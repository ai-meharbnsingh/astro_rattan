"""
ayurdaya_engine.py — Balarishta & Ayu Classification
======================================================
Implements Adhyaya 13 of Phaladeepika (slokas 1–8 + 21).

Two entry points:
  - check_balarishta(chart_data)     → infant mortality risk (birth-to-age-12)
  - classify_ayu(chart_data)         → lifespan category (Alpayu/Madhyayu/Dirghayu/Purnayu)
  - is_balarishta_cancelled(chart)   → benefic aspect nullification (sloka 21)

Ayu categories (classical year ranges):
  - Alpayu     ≤ 32 years
  - Madhyayu    32 – 64 years
  - Dirghayu    64 – 108 years
  - Purnayu   100+ years (special case of Dirghayu with extra qualifiers)
"""
from __future__ import annotations
from typing import Any, Dict, List

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

KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Special aspects (offset from planet house, additional to the universal 7th)
SPECIAL_ASPECTS = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

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
    """Vedic aspect — 'Nth from H' counts H as 1st, so offset = N-1."""
    h = _house_of(planet, planets)
    if h < 1 or h > 12:
        return []
    aspects = [((h - 1 + 6) % 12) + 1]  # 7th (opposite)
    for off in SPECIAL_ASPECTS.get(planet, []):
        aspects.append(((h - 1 + off - 1) % 12) + 1)
    return aspects


def _aspects_house(source: str, house: int, planets: Dict[str, Dict[str, Any]]) -> bool:
    return house in _houses_aspected_by(source, planets)


def _aspects_planet(source: str, target: str, planets: Dict[str, Dict[str, Any]]) -> bool:
    th = _house_of(target, planets)
    return th > 0 and th in _houses_aspected_by(source, planets)


def _planets_aspecting_house(house: int, planets: Dict[str, Dict[str, Any]]) -> List[str]:
    return [p for p in planets if _aspects_house(p, house, planets)]


def _is_exalted(planet: str, sign: str) -> bool:
    return EXALTATION_SIGN.get(planet) == sign


def _is_debilitated(planet: str, sign: str) -> bool:
    return DEBILITATION_SIGN.get(planet) == sign


def _is_own_sign(planet: str, sign: str) -> bool:
    return SIGN_LORD.get(sign) == planet


def _lagna_lord(chart: Dict[str, Any]) -> str:
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")
    return SIGN_LORD.get(asc_sign, "")


def _planet_strength(planet: str, planets: Dict[str, Dict[str, Any]]) -> str:
    """Coarse strength label: strong / moderate / weak / missing."""
    if planet not in planets:
        return "missing"
    sign = _sign_of(planet, planets)
    house = _house_of(planet, planets)
    if _is_exalted(planet, sign):
        return "strong"
    if _is_own_sign(planet, sign):
        return "strong"
    if _is_debilitated(planet, sign):
        return "weak"
    if house in DUSTHANAS:
        return "weak"
    if house in KENDRAS or house in TRIKONAS:
        return "moderate"
    return "moderate"


def _moon_is_weak(chart: Dict[str, Any]) -> bool:
    planets = chart.get("planets", {}) or {}
    moon = planets.get("Moon") or {}
    if not moon:
        return True
    sign = str(moon.get("sign", ""))
    if _is_debilitated("Moon", sign):
        return True
    house = _house_of("Moon", planets)
    if house in DUSTHANAS:
        return True
    # Aspected by malefics with no benefic aspect
    malefic_aspects = [m for m in MALEFICS if m != "Moon" and _aspects_planet(m, "Moon", planets)]
    benefic_aspects = [b for b in BENEFICS if b != "Moon" and _aspects_planet(b, "Moon", planets)]
    if malefic_aspects and not benefic_aspects:
        return True
    return False


# ───────────────────────────────────────────────────────────────
# BALARISHTA (sloka 21 cancellation)
# ───────────────────────────────────────────────────────────────

def is_balarishta_cancelled(chart_data: Dict[str, Any]) -> bool:
    """
    Per Phaladeepika Adh. 13 sloka 21: benefic aspect on Moon or Lagna
    (especially Jupiter) cancels balarishta, or strong Lagna lord in own/exaltation.
    """
    if not isinstance(chart_data, dict):
        return False
    planets = chart_data.get("planets", {}) or {}
    if not planets:
        return False

    # 1. Strong Jupiter aspecting Moon or Lagna
    jup_sign = _sign_of("Jupiter", planets)
    jup_strong = _is_exalted("Jupiter", jup_sign) or _is_own_sign("Jupiter", jup_sign)
    jup_h = _house_of("Jupiter", planets)
    if jup_h > 0 and jup_strong:
        if _aspects_house("Jupiter", 1, planets) or _aspects_planet("Jupiter", "Moon", planets):
            return True

    # 2. Strong Lagna lord in own sign or exaltation in Kendra AND benefic aspects Moon
    #    (sloka 21 wants multiple supports, not just a strong lord)
    ll = _lagna_lord(chart_data)
    if ll and ll in planets:
        ll_sign = _sign_of(ll, planets)
        if _is_exalted(ll, ll_sign) or _is_own_sign(ll, ll_sign):
            ll_house = _house_of(ll, planets)
            if ll_house in KENDRAS or ll_house in TRIKONAS:
                # Also need a benefic aspect on Moon
                benefic_on_moon = any(
                    b != "Moon" and b in planets and _aspects_planet(b, "Moon", planets)
                    for b in BENEFICS
                )
                if benefic_on_moon:
                    return True

    # 3. Benefic (Jupiter or Venus) IN a Kendra AND no malefic aspects Lagna
    #    (stricter than earlier — only the two strongest benefics count)
    strong_benefic_in_kendra = any(
        b in planets and _house_of(b, planets) in KENDRAS
        for b in ("Jupiter", "Venus")
    )
    malefic_in_or_aspecting_lagna = (
        any(_house_of(m, planets) == 1 for m in MALEFICS if m in planets)
        or any(_aspects_house(m, 1, planets) for m in MALEFICS if m in planets)
    )
    if strong_benefic_in_kendra and not malefic_in_or_aspecting_lagna:
        return True

    return False


def check_balarishta(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check for Balarishta (infant mortality risk — death before age 12).
    Phaladeepika Adh. 13 slokas 1–4.
    """
    result = {
        "has_risk": False,
        "risk_level": "low",
        "factors": [],
        "remedies_recommended": False,
        "sloka_ref": "Phaladeepika Adh. 13 slokas 1–4",
        "cancelled": False,
    }

    if not isinstance(chart_data, dict):
        return result
    planets = chart_data.get("planets", {}) or {}
    if not planets:
        return result

    factors: List[str] = []

    # Rule 1: Moon in 6/8/12 aspected by malefic with no benefic aspect
    moon_house = _house_of("Moon", planets)
    if moon_house in DUSTHANAS:
        malefic_on_moon = [
            m for m in MALEFICS if m != "Moon" and _aspects_planet(m, "Moon", planets)
        ]
        benefic_on_moon = [
            b for b in BENEFICS if b != "Moon" and _aspects_planet(b, "Moon", planets)
        ]
        if malefic_on_moon and not benefic_on_moon:
            factors.append(
                f"Moon in Dusthana (house {moon_house}) aspected by malefic(s) "
                f"{', '.join(malefic_on_moon)} with no benefic aspect"
            )

    # Rule 2: Weak Moon in Lagna + weak Lagna lord
    if moon_house == 1 and _moon_is_weak(chart_data):
        ll = _lagna_lord(chart_data)
        if ll in planets and _planet_strength(ll, planets) == "weak":
            factors.append(f"Weak Moon in Lagna with weak Lagna lord ({ll})")

    # Rule 3: Malefic in Lagna + Moon in 7th or 8th aspected by malefic
    malefic_in_lagna = [m for m in MALEFICS if m in planets and _house_of(m, planets) == 1]
    if malefic_in_lagna and moon_house in (7, 8):
        malefic_on_moon = [
            m for m in MALEFICS if m != "Moon" and _aspects_planet(m, "Moon", planets)
        ]
        if malefic_on_moon:
            factors.append(
                f"Malefic(s) {', '.join(malefic_in_lagna)} in Lagna + Moon in "
                f"{moon_house}th aspected by malefic"
            )

    # Rule 4: Sun in 7/8 + Moon in 6/12
    sun_house = _house_of("Sun", planets)
    if sun_house in (7, 8) and moon_house in (6, 12):
        factors.append(f"Sun in {sun_house}th house + Moon in {moon_house}th house")

    if not factors:
        return result

    # Compute severity from raw signal count
    n = len(factors)
    if n >= 3:
        level = "severe"
    elif n == 2:
        level = "high"
    else:
        level = "moderate"

    # Cancellation check (sloka 21)
    cancelled = is_balarishta_cancelled(chart_data)
    if cancelled:
        # Cancellation demotes severity by one level (but does not remove signals)
        demotion = {"severe": "moderate", "high": "low", "moderate": "low"}
        level = demotion.get(level, "low")

    result.update({
        "has_risk": (not cancelled) and n >= 1,
        "risk_level": level if not cancelled else "low",
        "factors": factors,
        "remedies_recommended": (not cancelled) and n >= 2,
        "cancelled": cancelled,
    })
    return result


# ───────────────────────────────────────────────────────────────
# AYU CLASSIFICATION
# ───────────────────────────────────────────────────────────────

def _score_dirghayu(chart: Dict[str, Any]) -> tuple[int, List[str]]:
    """Count long-life indicators. Returns (score, matched_rules)."""
    planets = chart.get("planets", {}) or {}
    score = 0
    rules: List[str] = []

    # Strong Jupiter in Kendra or Trikona
    jup_h = _house_of("Jupiter", planets)
    jup_sign = _sign_of("Jupiter", planets)
    jup_strong = _is_exalted("Jupiter", jup_sign) or _is_own_sign("Jupiter", jup_sign)
    if jup_h in (KENDRAS | TRIKONAS) and jup_strong:
        score += 2
        rules.append(f"Strong Jupiter ({jup_sign}) in Kendra/Trikona (house {jup_h})")
    elif jup_h in (KENDRAS | TRIKONAS):
        score += 1
        rules.append(f"Jupiter in Kendra/Trikona (house {jup_h})")

    # Strong Lagna lord with benefic aspect
    ll = _lagna_lord(chart)
    if ll and ll in planets:
        ll_strength = _planet_strength(ll, planets)
        if ll_strength == "strong":
            score += 2
            rules.append(f"Strong Lagna lord ({ll}) in {_sign_of(ll, planets)}")
        benefic_on_ll = [
            b for b in BENEFICS if b != ll and _aspects_planet(b, ll, planets)
        ]
        if benefic_on_ll:
            score += 1
            rules.append(f"Benefic aspect on Lagna lord by {', '.join(benefic_on_ll)}")

    # 8th lord in own sign or exaltation
    asc_sign = (chart.get("ascendant") or {}).get("sign", "")
    if asc_sign in ZODIAC:
        eighth_sign_idx = (ZODIAC.index(asc_sign) + 7) % 12
        eighth_sign = ZODIAC[eighth_sign_idx]
        eighth_lord = SIGN_LORD.get(eighth_sign, "")
        if eighth_lord and eighth_lord in planets:
            el_sign = _sign_of(eighth_lord, planets)
            if _is_exalted(eighth_lord, el_sign) or _is_own_sign(eighth_lord, el_sign):
                score += 2
                rules.append(f"8th lord ({eighth_lord}) in own/exalted sign ({el_sign})")

    # Benefics in Kendras
    benefic_in_kendra = [
        b for b in BENEFICS if b in planets and _house_of(b, planets) in KENDRAS
    ]
    if len(benefic_in_kendra) >= 2:
        score += 1
        rules.append(f"Multiple benefics in Kendras: {', '.join(benefic_in_kendra)}")

    return score, rules


def _score_alpayu(chart: Dict[str, Any]) -> tuple[int, List[str]]:
    """Count short-life indicators. Returns (score, matched_rules)."""
    planets = chart.get("planets", {}) or {}
    score = 0
    rules: List[str] = []

    # Malefic in Lagna with no benefic aspect
    malefic_in_lagna = [m for m in MALEFICS if m in planets and _house_of(m, planets) == 1]
    if malefic_in_lagna:
        benefic_aspecting_lagna = [
            b for b in BENEFICS if b in planets and _aspects_house(b, 1, planets)
        ]
        if not benefic_aspecting_lagna:
            score += 2
            rules.append(
                f"Malefic(s) {', '.join(malefic_in_lagna)} in Lagna with no benefic aspect"
            )

    # Lagna lord in 6/8/12
    ll = _lagna_lord(chart)
    if ll and ll in planets:
        ll_h = _house_of(ll, planets)
        if ll_h in DUSTHANAS:
            score += 2
            rules.append(f"Lagna lord ({ll}) in Dusthana (house {ll_h})")

    # Moon + Saturn + Mars together in Lagna
    lagna_planets = [p for p in planets if _house_of(p, planets) == 1]
    if all(p in lagna_planets for p in ("Moon", "Saturn", "Mars")):
        score += 3
        rules.append("Moon + Saturn + Mars all in Lagna")

    # Many malefics in Kendras, benefics in dusthanas
    benefic_in_dusthana = [
        b for b in BENEFICS if b in planets and _house_of(b, planets) in DUSTHANAS
    ]
    if len(benefic_in_dusthana) >= 2:
        score += 1
        rules.append(f"Multiple benefics in Dusthanas: {', '.join(benefic_in_dusthana)}")

    return score, rules


def classify_ayu(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify lifespan into Alpayu / Madhyayu / Dirghayu / Purnayu.

    Method: Score dirghayu vs alpayu indicators and classify by balance.
    Purnayu requires dirghayu conditions PLUS special qualifiers.
    """
    base = {
        "category": "Madhyayu",
        "category_en": "Madhyayu",
        "category_hi": "मध्यायु",
        "years_range": "32–64",
        "reasoning_en": "Mixed influences, balanced benefic and malefic strength.",
        "reasoning_hi": "मिश्रित प्रभाव, शुभ एवं अशुभ ग्रहों का संतुलन।",
        "matched_rules": [],
        "dirghayu_score": 0,
        "alpayu_score": 0,
        "sloka_ref": "Phaladeepika Adh. 13 slokas 5–8",
    }

    if not isinstance(chart_data, dict):
        return base
    planets = chart_data.get("planets", {}) or {}
    if not planets:
        return base

    dscore, drules = _score_dirghayu(chart_data)
    ascore, arules = _score_alpayu(chart_data)

    base["dirghayu_score"] = dscore
    base["alpayu_score"] = ascore

    # Purnayu: strong Dirghayu + exalted Lagna lord + Jupiter in 1/5/9/10
    purnayu = False
    purnayu_rules: List[str] = []
    ll = _lagna_lord(chart_data)
    if ll and ll in planets:
        ll_sign = _sign_of(ll, planets)
        if _is_exalted(ll, ll_sign):
            jup_h = _house_of("Jupiter", planets)
            if jup_h in (KENDRAS | TRIKONAS):
                purnayu_rules.append(f"Exalted Lagna lord ({ll}) in {ll_sign}")
                purnayu_rules.append(f"Jupiter in house {jup_h} (Kendra/Trikona)")
                if dscore >= 4:
                    purnayu = True

    if purnayu:
        base.update({
            "category": "Purnayu",
            "category_en": "Purnayu",
            "category_hi": "पूर्णायु",
            "years_range": "100+",
            "reasoning_en": "Exceptional longevity indicated: strong Dirghayu conditions with exalted Lagna lord and Jupiter in Kendra/Trikona.",
            "reasoning_hi": "असाधारण दीर्घायु: प्रबल दीर्घायु योग, उच्च लग्नेश, एवं केंद्र/त्रिकोण में बृहस्पति।",
            "matched_rules": drules + purnayu_rules,
        })
    elif dscore >= 4 and dscore > ascore:
        base.update({
            "category": "Dirghayu",
            "category_en": "Dirghayu",
            "category_hi": "दीर्घायु",
            "years_range": "64–108",
            "reasoning_en": "Strong longevity indicators: " + "; ".join(drules),
            "reasoning_hi": "प्रबल दीर्घायु संकेतक कुंडली में उपस्थित हैं।",
            "matched_rules": drules,
        })
    elif ascore >= 3 and ascore > dscore:
        base.update({
            "category": "Alpayu",
            "category_en": "Alpayu",
            "category_hi": "अल्पायु",
            "years_range": "0–32",
            "reasoning_en": "Short-life indicators dominate: " + "; ".join(arules),
            "reasoning_hi": "अल्पायु के संकेतक प्रबल हैं।",
            "matched_rules": arules,
        })
    else:
        combined = drules + arules
        base["matched_rules"] = combined
        if combined:
            base["reasoning_en"] = (
                "Balanced factors — both positive and negative influences: "
                + "; ".join(combined)
            )
            base["reasoning_hi"] = "संतुलित योग — दोनों प्रकार के प्रभाव उपस्थित हैं।"

    return base
