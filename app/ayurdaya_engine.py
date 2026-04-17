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


# ═════════════════════════════════════════════════════════════════════
# THREE-METHOD AYURDAYA — Phaladeepika Adhyaya 22
# (Pindayu / Nisargayu / Amsayu + 6 Haranas + selector)
# ═════════════════════════════════════════════════════════════════════

# Classical max years assigned to each planet (Satyacharya scheme)
PINDAYU_MAX_YEARS = {
    "Sun": 19.0,
    "Moon": 25.0,
    "Mars": 15.0,
    "Mercury": 12.0,
    "Jupiter": 15.0,
    "Venus": 21.0,
    "Saturn": 20.0,
}

HUMAN_MAX_LIFESPAN = 108.0

# Navamsa modality starting offsets (movable=0, fixed=8, dual=4)
MOVABLE = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL = {"Gemini", "Virgo", "Sagittarius", "Pisces"}


def _planet_strength_ratio(planet: str, planets: Dict[str, Dict[str, Any]]) -> float:
    """
    Return a 0-1 strength ratio used by Pindayu contributions.

    Exalted/own = 1.0, friendly = 0.75, neutral = 0.5,
    enemy = 0.25, debilitated = 0.1.
    Kendra placement adds +0.1, Dusthana subtracts 0.1 (clamped to [0.1, 1.0]).
    """
    if planet not in planets:
        return 0.5
    sign = _sign_of(planet, planets)
    base = 0.5  # neutral default
    if _is_exalted(planet, sign):
        base = 1.0
    elif _is_own_sign(planet, sign):
        base = 0.9
    elif _is_debilitated(planet, sign):
        base = 0.1

    h = _house_of(planet, planets)
    if h in KENDRAS:
        base = min(1.0, base + 0.1)
    elif h in DUSTHANAS:
        base = max(0.1, base - 0.1)
    return base


def _navamsa_sign(longitude: float) -> str:
    """Return the navamsa sign (D9) for an absolute longitude 0-360."""
    try:
        lon = float(longitude) % 360
    except (TypeError, ValueError):
        return ""
    sign_idx = int(lon // 30)
    sign = ZODIAC[sign_idx]
    pos_in_sign = lon - sign_idx * 30
    navamsa_idx = int(pos_in_sign // (30.0 / 9.0))  # 0..8

    # Starting navamsa sign by modality of the sign occupied
    if sign in MOVABLE:
        start = sign_idx
    elif sign in FIXED:
        start = (sign_idx + 8) % 12   # 9th from current
    else:  # DUAL
        start = (sign_idx + 4) % 12   # 5th from current
    return ZODIAC[(start + navamsa_idx) % 12]


def _is_combust(planet: str, planets: Dict[str, Dict[str, Any]]) -> bool:
    """Simple combustion: non-Sun, non-node planet within 10° of Sun."""
    if planet in ("Sun", "Rahu", "Ketu") or planet not in planets:
        return False
    sun = planets.get("Sun") or {}
    if not sun:
        return False
    try:
        p_lon = float((planets.get(planet) or {}).get("longitude", -999))
        s_lon = float(sun.get("longitude", -999))
    except (TypeError, ValueError):
        return False
    if p_lon < 0 or s_lon < 0:
        return False
    diff = abs(p_lon - s_lon)
    if diff > 180:
        diff = 360 - diff
    return diff < 10.0


# ────────────────────────────────────────────────────────────────────
# 1. PINDAYU (Satyacharya)
# ────────────────────────────────────────────────────────────────────

def pindayu(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pindayu — Sun-based lifespan calc.
    Each of the 7 classical planets contributes max years × strength ratio.
    """
    breakdown: List[Dict[str, Any]] = []
    if not isinstance(chart_data, dict):
        return {"raw": 0.0, "after_haranas": 0.0, "haranas": [], "breakdown": breakdown}
    planets = chart_data.get("planets", {}) or {}

    raw = 0.0
    for p, max_years in PINDAYU_MAX_YEARS.items():
        ratio = _planet_strength_ratio(p, planets) if p in planets else 0.5
        contribution = round(max_years * ratio, 2)
        raw += contribution
        breakdown.append({
            "planet": p,
            "max_years": max_years,
            "strength_ratio": round(ratio, 2),
            "contribution": contribution,
        })

    raw = round(raw, 2)
    haranas = apply_haranas(raw, chart_data)
    return {
        "raw": raw,
        "after_haranas": haranas["final_years"],
        "haranas": haranas["haranas_applied"],
        "breakdown": breakdown,
    }


# ────────────────────────────────────────────────────────────────────
# 2. NISARGAYU (Jivasarman — Moon-based)
# ────────────────────────────────────────────────────────────────────

def nisargayu(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Natural lifespan assigned from Moon's placement."""
    if not isinstance(chart_data, dict):
        return {"raw": 0.0, "after_haranas": 0.0, "haranas": [], "notes": []}
    planets = chart_data.get("planets", {}) or {}
    moon = planets.get("Moon") or {}
    notes: List[str] = []

    if not moon:
        raw = 60.0
        notes.append("Moon missing — using default 60 years")
    else:
        moon_sign = str(moon.get("sign", ""))
        moon_house = _house_of("Moon", planets)

        if _is_exalted("Moon", moon_sign) or _is_own_sign("Moon", moon_sign):
            if moon_house in KENDRAS:
                raw = 90.0
                notes.append(f"Moon in own/exalted sign ({moon_sign}) in Kendra")
            else:
                raw = 80.0
                notes.append(f"Moon in own/exalted sign ({moon_sign})")
        elif _is_debilitated("Moon", moon_sign):
            raw = 35.0
            notes.append(f"Moon debilitated in {moon_sign}")
        elif moon_house in DUSTHANAS:
            raw = 50.0
            notes.append(f"Moon in Dusthana (house {moon_house})")
        elif moon_house in KENDRAS or moon_house in TRIKONAS:
            raw = 75.0
            notes.append(f"Moon in Kendra/Trikona (house {moon_house})")
        else:
            raw = 65.0
            notes.append(f"Moon in house {moon_house}")

        # Benefic aspect adjusts up, malefic adjusts down
        benefics_on_moon = [
            b for b in BENEFICS if b != "Moon" and b in planets and _aspects_planet(b, "Moon", planets)
        ]
        malefics_on_moon = [
            m for m in MALEFICS if m != "Moon" and m in planets and _aspects_planet(m, "Moon", planets)
        ]
        if benefics_on_moon:
            raw += 5.0 * min(2, len(benefics_on_moon))
            notes.append(f"Benefic aspect on Moon by {', '.join(benefics_on_moon)} (+)")
        if malefics_on_moon and not benefics_on_moon:
            raw -= 8.0 * min(2, len(malefics_on_moon))
            notes.append(f"Malefic aspect on Moon by {', '.join(malefics_on_moon)} (-)")

    raw = max(20.0, min(HUMAN_MAX_LIFESPAN, round(raw, 2)))
    haranas = apply_haranas(raw, chart_data)
    return {
        "raw": raw,
        "after_haranas": haranas["final_years"],
        "haranas": haranas["haranas_applied"],
        "notes": notes,
    }


# ────────────────────────────────────────────────────────────────────
# 3. AMSAYU (Parashara — Navamsa-based)
# ────────────────────────────────────────────────────────────────────

def amsayu(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Amsayu — sum of (100/108) × navamsa strength for each of 7 planets.
    Own navamsa → full, friendly → 0.75, neutral → 0.5, enemy → 0.25, debil → 0.1.
    """
    breakdown: List[Dict[str, Any]] = []
    if not isinstance(chart_data, dict):
        return {"raw": 0.0, "after_haranas": 0.0, "haranas": [], "breakdown": breakdown}
    planets = chart_data.get("planets", {}) or {}

    per_planet_max = HUMAN_MAX_LIFESPAN / 7.0  # ~15.43 years per planet full contribution
    raw = 0.0

    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        if p not in planets:
            continue
        lon = (planets[p] or {}).get("longitude", 0)
        navamsa = _navamsa_sign(lon)
        if not navamsa:
            factor = 0.5
            status = "unknown"
        elif _is_exalted(p, navamsa):
            factor = 1.0
            status = "exalted in navamsa"
        elif _is_own_sign(p, navamsa):
            factor = 1.0
            status = "own navamsa"
        elif _is_debilitated(p, navamsa):
            factor = 0.1
            status = "debilitated in navamsa"
        else:
            # Friendly / neutral — use coarse own-element check
            factor = 0.5
            status = "neutral navamsa"

        contribution = round(per_planet_max * factor, 2)
        raw += contribution
        breakdown.append({
            "planet": p,
            "navamsa": navamsa,
            "status": status,
            "factor": factor,
            "contribution": contribution,
        })

    raw = round(raw, 2)
    haranas = apply_haranas(raw, chart_data)
    return {
        "raw": raw,
        "after_haranas": haranas["final_years"],
        "haranas": haranas["haranas_applied"],
        "breakdown": breakdown,
    }


# ────────────────────────────────────────────────────────────────────
# 6 HARANAS (reductions)
# ────────────────────────────────────────────────────────────────────

def apply_haranas(raw_years: float, chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply six classical Haranas (reductions) to raw lifespan.
    Returns {final_years, haranas_applied: [{name, name_hi, reason, reduction_fraction, reduction_years}, ...]}
    """
    applied: List[Dict[str, Any]] = []
    if not isinstance(chart_data, dict) or raw_years <= 0:
        return {"final_years": round(raw_years or 0.0, 2), "haranas_applied": applied}

    planets = chart_data.get("planets", {}) or {}
    current = raw_years

    # 1. RAJA-HARANA — Lagna lord in Dusthana or debilitated without benefic aspect → 1/3
    ll = _lagna_lord(chart_data)
    if ll and ll in planets:
        ll_sign = _sign_of(ll, planets)
        ll_house = _house_of(ll, planets)
        afflicted = _is_debilitated(ll, ll_sign) or ll_house in DUSTHANAS
        benefic_on_ll = any(
            b != ll and b in planets and _aspects_planet(b, ll, planets) for b in BENEFICS
        )
        if afflicted and not benefic_on_ll:
            red = current / 3.0
            current -= red
            applied.append({
                "name": "Raja Harana",
                "name_hi": "राज हरण",
                "reason": f"Lagna lord ({ll}) severely afflicted without benefic aspect",
                "fraction": "1/3",
                "reduction_years": round(red, 2),
            })

    # 2. BHUPA-HARANA — 10th lord weak → 1/4
    asc_sign = (chart_data.get("ascendant") or {}).get("sign", "")
    if asc_sign in ZODIAC:
        tenth_sign = ZODIAC[(ZODIAC.index(asc_sign) + 9) % 12]
        tenth_lord = SIGN_LORD.get(tenth_sign, "")
        if tenth_lord and tenth_lord in planets:
            tl_sign = _sign_of(tenth_lord, planets)
            tl_house = _house_of(tenth_lord, planets)
            if _is_debilitated(tenth_lord, tl_sign) or tl_house in DUSTHANAS:
                red = current / 4.0
                current -= red
                applied.append({
                    "name": "Bhupa Harana",
                    "name_hi": "भूप हरण",
                    "reason": f"10th lord ({tenth_lord}) weak — in {tl_sign}, house {tl_house}",
                    "fraction": "1/4",
                    "reduction_years": round(red, 2),
                })

    # 3. AYANA-HARANA — Sun/Moon in unfavorable southern ayana (approximate: Sun in signs Cancer-Sagittarius = Dakshinayana)
    # Classical rule: Sun in Dakshinayana (Cancer–Sagittarius) with unfavorable placement (Dusthana) triggers this
    sun = planets.get("Sun") or {}
    sun_sign = str(sun.get("sign", ""))
    sun_house = _house_of("Sun", planets)
    if sun_sign in ("Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius") and sun_house in DUSTHANAS:
        red = current / 6.0
        current -= red
        applied.append({
            "name": "Ayana Harana",
            "name_hi": "अयन हरण",
            "reason": f"Sun in Dakshinayana ({sun_sign}) in Dusthana (house {sun_house})",
            "fraction": "1/6",
            "reduction_years": round(red, 2),
        })

    # 4. ASTANGATA-HARANA — each combust planet → 1/8 per planet (capped at 3 to avoid over-reduction)
    combust_list = [p for p in planets if _is_combust(p, planets)]
    if combust_list:
        count = min(3, len(combust_list))
        red_total = 0.0
        for _ in range(count):
            r = current / 8.0
            current -= r
            red_total += r
        applied.append({
            "name": "Astangata Harana",
            "name_hi": "अस्तंगत हरण",
            "reason": f"Combust planets: {', '.join(combust_list)}",
            "fraction": f"1/8 × {count}",
            "reduction_years": round(red_total, 2),
        })

    # 5. DUSHTA-HARANA — benefics in 6/8/12 → 1/10 per planet (capped at 3)
    benefics_in_dusthana = [b for b in BENEFICS if b in planets and _house_of(b, planets) in DUSTHANAS]
    if benefics_in_dusthana:
        count = min(3, len(benefics_in_dusthana))
        red_total = 0.0
        for _ in range(count):
            r = current / 10.0
            current -= r
            red_total += r
        applied.append({
            "name": "Dushta Harana",
            "name_hi": "दुष्ट हरण",
            "reason": f"Benefics in Dusthanas: {', '.join(benefics_in_dusthana)}",
            "fraction": f"1/10 × {count}",
            "reduction_years": round(red_total, 2),
        })

    # 6. CHAKRAPATA-HARANA — approximation: Saturn + Rahu/Ketu in Lagna or 7th → 1/12
    nodes_in_axis = any(
        n in planets and _house_of(n, planets) in (1, 7) for n in ("Rahu", "Ketu")
    )
    saturn_in_axis = "Saturn" in planets and _house_of("Saturn", planets) in (1, 7)
    if nodes_in_axis and saturn_in_axis:
        red = current / 12.0
        current -= red
        applied.append({
            "name": "Chakrapata Harana",
            "name_hi": "चक्रपात हरण",
            "reason": "Saturn + nodal axis afflicting Lagna/7th (approximation)",
            "fraction": "1/12",
            "reduction_years": round(red, 2),
        })

    return {
        "final_years": round(max(0.0, current), 2),
        "haranas_applied": applied,
    }


# ────────────────────────────────────────────────────────────────────
# SELECTOR (sloka 27)
# ────────────────────────────────────────────────────────────────────

def _strongest_of_sun_moon_lagna(chart_data: Dict[str, Any]) -> str:
    """
    Return 'sun', 'moon', or 'lagna' — whichever is strongest.
    Uses simple scoring: exaltation/own = 3, Kendra = 2, Trikona = 2, etc.
    Lagna strength = Lagna lord strength + ascendant sign as own/exalted for lord.
    """
    planets = chart_data.get("planets", {}) or {}

    def score_planet(p: str) -> float:
        if p not in planets:
            return 0.0
        s = 0.0
        sign = _sign_of(p, planets)
        h = _house_of(p, planets)
        if _is_exalted(p, sign):
            s += 3
        elif _is_own_sign(p, sign):
            s += 2.5
        elif _is_debilitated(p, sign):
            s -= 2
        if h in KENDRAS:
            s += 1.5
        elif h in TRIKONAS:
            s += 1
        elif h in DUSTHANAS:
            s -= 1
        return s

    sun = score_planet("Sun")
    moon = score_planet("Moon")
    ll = _lagna_lord(chart_data)
    lagna = score_planet(ll) if ll else 0.0
    # Prefer lagna on exact ties (classical convention)
    best = max(sun, moon, lagna)
    if lagna == best:
        return "lagna"
    if moon == best:
        return "moon"
    return "sun"


def calculate_lifespan(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full three-method Ayurdaya with selector.
    Returns all three methods + selected + final years + classification.
    """
    if not isinstance(chart_data, dict):
        chart_data = {}

    pi = pindayu(chart_data)
    ni = nisargayu(chart_data)
    am = amsayu(chart_data)

    selector = _strongest_of_sun_moon_lagna(chart_data)
    if selector == "sun":
        method_key = "pindayu"
        selection_en = "Sun strongest among Sun/Moon/Lagna → Pindayu method"
        selection_hi = "सूर्य/चंद्र/लग्न में से सूर्य सबसे बलवान → पिंडायु विधि"
    elif selector == "moon":
        method_key = "nisargayu"
        selection_en = "Moon strongest among Sun/Moon/Lagna → Nisargayu method"
        selection_hi = "सूर्य/चंद्र/लग्न में से चंद्र सबसे बलवान → निसर्गायु विधि"
    else:
        method_key = "amsayu"
        selection_en = "Lagna strongest among Sun/Moon/Lagna → Amsayu method"
        selection_hi = "सूर्य/चंद्र/लग्न में से लग्न सबसे बलवान → अंशायु विधि"

    selected = {"pindayu": pi, "nisargayu": ni, "amsayu": am}[method_key]
    final = min(HUMAN_MAX_LIFESPAN, selected["after_haranas"])

    # Classification based on final years
    if final <= 32:
        classification = "Alpayu"
    elif final <= 64:
        classification = "Madhyayu"
    elif final < 100:
        classification = "Dirghayu"
    else:
        classification = "Purnayu"

    return {
        "pindayu": pi,
        "nisargayu": ni,
        "amsayu": am,
        "selected_method": method_key,
        "selection_reason_en": selection_en,
        "selection_reason_hi": selection_hi,
        "final_years": final,
        "classification": classification,
        "sloka_ref": "Phaladeepika Adh. 22 sloka 27",
    }
