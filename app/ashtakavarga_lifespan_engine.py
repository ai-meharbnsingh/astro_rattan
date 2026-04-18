"""
ashtakavarga_lifespan_engine.py — Pindayu (Ashtakavarga-based Lifespan)
========================================================================
Implements the Bindu-based Ayurdaya (Pindayu) method from
Phaladeepika Adhyaya 23.

Each of the 7 classical planets contributes years based on:
  contribution = (BAV bindus in planet's own natal sign / 8) × max years

Modifiers:
  - Debilitated planet  : × 0.5
  - Combust planet      : × 0.75  (within 6° of Sun; Moon excluded)
  - Retrograde planet   : × 1.1
  - Exalted planet      : × 1.2
  (Multiple modifiers stack — multiplied together.)

Ayu classification:
  < 32 years  → Alpayu   (short life)
  32–70 years → Madhyayu (medium life)
  > 70 years  → Dirghayu (long life)

Reference: Phaladeepika Adh. 23
"""
from __future__ import annotations

from typing import Any, Dict, List

from app.ashtakvarga_engine import calculate_ashtakvarga

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_HI = {
    "Aries": "मेष", "Taurus": "वृषभ", "Gemini": "मिथुन", "Cancer": "कर्क",
    "Leo": "सिंह", "Virgo": "कन्या", "Libra": "तुला", "Scorpio": "वृश्चिक",
    "Sagittarius": "धनु", "Capricorn": "मकर", "Aquarius": "कुंभ", "Pisces": "मीन",
}

_PLANET_HI = {
    "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि",
}

# Phaladeepika Adh. 23 — maximum years each planet can contribute
_PINDAYU_MAX_YEARS: Dict[str, float] = {
    "Sun":     19.5,
    "Moon":    25.0,
    "Mars":    15.0,
    "Mercury": 12.0,
    "Jupiter": 15.0,
    "Venus":   21.0,
    "Saturn":  20.0,
}

# Debilitation signs (planet loses strength)
_DEBILITATION_SIGN: Dict[str, str] = {
    "Sun":     "Libra",
    "Moon":    "Scorpio",
    "Mars":    "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus":   "Virgo",
    "Saturn":  "Aries",
}

# Exaltation signs (planet gains extra strength)
_EXALTATION_SIGN: Dict[str, str] = {
    "Sun":     "Aries",
    "Moon":    "Taurus",
    "Mars":    "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus":   "Pisces",
    "Saturn":  "Libra",
}

# Modifier values
_MODIFIER_DEBILITATED = 0.5
_MODIFIER_COMBUST     = 0.75
_MODIFIER_RETROGRADE  = 1.1
_MODIFIER_EXALTED     = 1.2

# Maximum possible bindus in one sign (for the contributing denominator)
_MAX_BINDUS_PER_SIGN = 8

# Combust orb for Pindayu method (degrees)
_COMBUST_ORB = 6.0


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _is_debilitated(planet: str, sign: str) -> bool:
    return _DEBILITATION_SIGN.get(planet) == sign


def _is_exalted(planet: str, sign: str) -> bool:
    return _EXALTATION_SIGN.get(planet) == sign


def _is_combust(planet: str, planet_lon: float, sun_lon: float) -> bool:
    """Return True if planet is within _COMBUST_ORB degrees of Sun.

    Moon is never considered combust. Sun itself is excluded.
    """
    if planet in ("Sun", "Moon"):
        return False
    diff = abs(planet_lon - sun_lon)
    if diff > 180:
        diff = 360.0 - diff
    return diff < _COMBUST_ORB


def _is_retrograde(planet_info: Dict[str, Any]) -> bool:
    """Return True if retrograde flag is set (handles both key names)."""
    return bool(
        planet_info.get("retrograde") or planet_info.get("is_retrograde")
    )


def _compute_modifier(
    planet: str,
    natal_sign: str,
    planet_info: Dict[str, Any],
    sun_longitude: float,
) -> tuple[float, List[str], List[str]]:
    """
    Compute the combined modifier for a planet.

    Returns:
        (modifier, reasons_en, reasons_hi)

    Multiple conditions stack (multiply together).
    """
    modifier = 1.0
    reasons_en: List[str] = []
    reasons_hi: List[str] = []

    p_lon = float(planet_info.get("longitude", 0.0))
    sign_hi = _SIGN_HI.get(natal_sign, natal_sign)
    p_hi = _PLANET_HI.get(planet, planet)

    # Exaltation (checked first — exclusive with debilitation)
    if _is_exalted(planet, natal_sign):
        modifier *= _MODIFIER_EXALTED
        reasons_en.append(f"Exalted in {natal_sign} — strength bonus applied")
        reasons_hi.append(f"{sign_hi} राशि में उच्च — बल-वृद्धि लागू")

    # Debilitation (exclusive with exaltation — can't be both)
    elif _is_debilitated(planet, natal_sign):
        modifier *= _MODIFIER_DEBILITATED
        reasons_en.append(f"Debilitated in {natal_sign} — strength halved")
        reasons_hi.append(f"{sign_hi} राशि में नीच — बल अर्ध")

    # Combust
    if _is_combust(planet, p_lon, sun_longitude):
        modifier *= _MODIFIER_COMBUST
        reasons_en.append("Combust (within 6° of Sun) — reduced contribution")
        reasons_hi.append("अस्त (सूर्य से 6° के भीतर) — बल ह्रास")

    # Retrograde
    if _is_retrograde(planet_info):
        modifier *= _MODIFIER_RETROGRADE
        reasons_en.append("Retrograde — slight increase in contribution")
        reasons_hi.append("वक्री — अंशदान में सामान्य वृद्धि")

    # No modifier
    if not reasons_en:
        reasons_en.append("No special modification")
        reasons_hi.append("कोई विशेष संशोधन नहीं")

    return round(modifier, 4), reasons_en, reasons_hi


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def calculate_pindayu(chart_data: dict) -> dict:
    """
    Pindayu (Ashtakavarga-based lifespan) per Phaladeepika Adh. 23.

    Args:
        chart_data: standard chart dict with 'planets' and 'ascendant'.
                    Each planet entry must have at minimum:
                      - 'sign'      (str) — natal sign name
                      - 'longitude' (float) — absolute ecliptic longitude 0-360

    Returns:
        {
            "planet_contributions": [...],  # one entry per classical planet
            "total_pindayu": float,
            "ayu_class": str,               # Alpayu / Madhyayu / Dirghayu
            "ayu_class_hi": str,
            "ayu_range_en": str,
            "ayu_range_hi": str,
            "interpretation_en": str,
            "interpretation_hi": str,
            "note_en": str,
            "note_hi": str,
            "sloka_ref": str,
        }

    Gracefully returns a skeleton with total_pindayu=0.0 if chart data is
    incomplete or an internal error occurs.
    """
    _sloka_ref = "Phaladeepika Adh. 23"

    # ── Empty skeleton for graceful degradation ──
    _empty = {
        "planet_contributions": [],
        "total_pindayu": 0.0,
        "ayu_class": "unknown",
        "ayu_class_hi": "अज्ञात",
        "ayu_range_en": "Insufficient data",
        "ayu_range_hi": "अपर्याप्त डेटा",
        "interpretation_en": "Chart data is incomplete. Please provide all 7 classical planets.",
        "interpretation_hi": "कुंडली डेटा अपूर्ण है। कृपया सातों शास्त्रीय ग्रह प्रदान करें।",
        "note_en": (
            "Pindayu is one of several classical longevity methods. "
            "It should be read alongside Vimshottari dasha, 8th house strength, "
            "and maraka analysis for a complete picture."
        ),
        "note_hi": (
            "पिण्डायु — आयुर्दाय की कई शास्त्रीय पद्धतियों में से एक है। "
            "पूर्ण चित्र के लिए विंशोत्तरी दशा, अष्टम भाव बल तथा मारकेश "
            "विश्लेषण के साथ पढ़ें।"
        ),
        "sloka_ref": _sloka_ref,
    }

    if not isinstance(chart_data, dict):
        return _empty

    planets_raw: Dict[str, Any] = chart_data.get("planets") or {}
    asc_raw: Any = chart_data.get("ascendant") or {}
    ascendant_sign: str = (
        asc_raw.get("sign", "") if isinstance(asc_raw, dict) else ""
    )

    # Validate required planets
    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    if not required.issubset(set(planets_raw.keys())):
        missing = required - set(planets_raw.keys())
        _empty["interpretation_en"] = (
            f"Missing planet data: {', '.join(sorted(missing))}. "
            "Please provide all 7 classical planets."
        )
        return _empty

    # Build planet_signs dict for calculate_ashtakvarga
    planet_signs: Dict[str, str] = {}
    for p_name, info in planets_raw.items():
        if isinstance(info, dict) and info.get("sign") in _SIGN_NAMES:
            planet_signs[p_name] = info["sign"]
    if ascendant_sign in _SIGN_NAMES:
        planet_signs["Ascendant"] = ascendant_sign
    elif ascendant_sign:
        # Ascendant present but sign not recognised — proceed without it
        planet_signs.setdefault("Ascendant", "Aries")

    # Ensure all required planets have valid signs in _SIGN_NAMES
    for p in required:
        if planet_signs.get(p) not in _SIGN_NAMES:
            _empty["interpretation_en"] = (
                f"Planet {p} has an unrecognised sign: "
                f"'{planets_raw.get(p, {}).get('sign', 'unknown')}'"
            )
            return _empty

    # Run Ashtakvarga
    try:
        av_result = calculate_ashtakvarga(planet_signs)
    except Exception as exc:  # pragma: no cover
        _empty["interpretation_en"] = f"Ashtakvarga calculation failed: {exc}"
        return _empty

    planet_details: Dict[str, Any] = av_result.get("planet_details", {})

    # Sun longitude (needed for combust check)
    sun_info: Dict[str, Any] = planets_raw.get("Sun") or {}
    try:
        sun_longitude = float(sun_info.get("longitude", 0.0))
    except (TypeError, ValueError):
        sun_longitude = 0.0

    # ── Per-planet contributions ──
    planet_contributions: List[Dict[str, Any]] = []
    total_pindayu = 0.0

    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        p_info: Dict[str, Any] = planets_raw.get(planet) or {}
        natal_sign: str = planet_signs.get(planet, "Aries")
        max_years: float = _PINDAYU_MAX_YEARS[planet]

        # BAV bindus for this planet in its own natal sign
        p_detail: Dict[str, Any] = planet_details.get(planet, {})
        totals: Dict[str, int] = p_detail.get("totals", {})
        bindus: int = int(totals.get(natal_sign, 0))

        # Raw contribution: (bindus / 8) × max years
        raw_contribution = round((bindus / _MAX_BINDUS_PER_SIGN) * max_years, 4)

        # Modifier
        try:
            p_lon = float(p_info.get("longitude", 0.0))
        except (TypeError, ValueError):
            p_lon = 0.0

        modifier, reasons_en, reasons_hi = _compute_modifier(
            planet, natal_sign, p_info, sun_longitude
        )

        final_contribution = round(raw_contribution * modifier, 4)
        total_pindayu += final_contribution

        planet_contributions.append({
            "planet": planet,
            "planet_hi": _PLANET_HI.get(planet, planet),
            "natal_sign": natal_sign,
            "natal_sign_hi": _SIGN_HI.get(natal_sign, natal_sign),
            "bindus_in_sign": bindus,
            "max_years": max_years,
            "raw_contribution": round(raw_contribution, 2),
            "modifier": round(modifier, 4),
            "final_contribution": round(final_contribution, 2),
            "modifier_reason_en": "; ".join(reasons_en),
            "modifier_reason_hi": "; ".join(reasons_hi),
            "sloka_ref": _sloka_ref,
        })

    total_pindayu = round(total_pindayu, 2)

    # ── Ayu classification ──
    if total_pindayu < 32:
        ayu_class    = "Alpayu"
        ayu_class_hi = "अल्पायु"
        ayu_range_en = "< 32 years (short lifespan)"
        ayu_range_hi = "32 वर्ष से कम (अल्प आयु)"
        interp_en = (
            f"Your Pindayu score of {total_pindayu} years places you in Alpayu "
            f"(short lifespan, < 32 years). This indicates challenges related to "
            f"longevity; classical texts advise examining 8th house, maraka lords, "
            f"and Balarishta factors for a complete assessment."
        )
        interp_hi = (
            f"आपका पिण्डायु अंक {total_pindayu} वर्ष है, जो अल्पायु "
            f"(32 वर्ष से कम) श्रेणी में आता है। शास्त्रीय ग्रंथों के अनुसार "
            f"अष्टम भाव, मारकेश एवं बलारिष्ट का भी परीक्षण करना चाहिए।"
        )
    elif total_pindayu <= 70:
        ayu_class    = "Madhyayu"
        ayu_class_hi = "मध्यायु"
        ayu_range_en = "32–70 years (medium lifespan)"
        ayu_range_hi = "32–70 वर्ष (मध्यम आयु)"
        interp_en = (
            f"Your Pindayu score of {total_pindayu} years places you in Madhyayu "
            f"(medium lifespan, 32–70 years). This is the most common category; "
            f"planetary periods (dashas) and transits will further refine the "
            f"timing of health-related events."
        )
        interp_hi = (
            f"आपका पिण्डायु अंक {total_pindayu} वर्ष है, जो मध्यायु "
            f"(32–70 वर्ष) श्रेणी में आता है। यह सर्वाधिक सामान्य वर्ग है। "
            f"ग्रह-दशाएँ एवं गोचर स्वास्थ्य-घटनाओं का समय और स्पष्ट करेंगे।"
        )
    else:
        ayu_class    = "Dirghayu"
        ayu_class_hi = "दीर्घायु"
        ayu_range_en = "> 70 years (long lifespan)"
        ayu_range_hi = "70 वर्ष से अधिक (दीर्घ आयु)"
        interp_en = (
            f"Your Pindayu score of {total_pindayu} years places you in Dirghayu "
            f"(long lifespan, > 70 years). Strong Ashtakavarga bindus across "
            f"planetary positions indicate robust vitality and longevity potential."
        )
        interp_hi = (
            f"आपका पिण्डायु अंक {total_pindayu} वर्ष है, जो दीर्घायु "
            f"(70 वर्ष से अधिक) श्रेणी में आता है। ग्रहों की स्थिति में "
            f"प्रबल अष्टकवर्ग बिंदु दीर्घ जीवन-शक्ति के द्योतक हैं।"
        )

    return {
        "planet_contributions": planet_contributions,
        "total_pindayu": total_pindayu,
        "ayu_class": ayu_class,
        "ayu_class_hi": ayu_class_hi,
        "ayu_range_en": ayu_range_en,
        "ayu_range_hi": ayu_range_hi,
        "interpretation_en": interp_en,
        "interpretation_hi": interp_hi,
        "note_en": (
            "Pindayu is one of several classical longevity methods. "
            "It should be read alongside Vimshottari dasha, 8th house strength, "
            "and maraka analysis for a complete picture."
        ),
        "note_hi": (
            "पिण्डायु — आयुर्दाय की कई शास्त्रीय पद्धतियों में से एक है। "
            "पूर्ण चित्र के लिए विंशोत्तरी दशा, अष्टम भाव बल तथा मारकेश "
            "विश्लेषण के साथ पढ़ें।"
        ),
        "sloka_ref": _sloka_ref,
    }
