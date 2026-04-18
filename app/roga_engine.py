"""
roga_engine.py — Classical Disease Prediction
==============================================
Implements Adhyaya 14 of Phaladeepika.

Two-layer analysis:
  1. General disease tendencies — planets in 6/8/12 → planet-specific disease set.
  2. Special Disease Yogas — 7 classical combinations with bilingual remedies.

Also returns body parts affected (by house) and timing indicators (dasha/transit hints).
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

DUSTHANAS = {6, 8, 12}
BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

SPECIAL_ASPECTS = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
    "Ketu": [5, 9],
}

# ───────────────────────────────────────────────────────────────
# Data
# ───────────────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "roga_rules.json")
_DATA_CACHE: Optional[Dict[str, Any]] = None


def load_roga_data() -> Dict[str, Any]:
    global _DATA_CACHE
    if _DATA_CACHE is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _DATA_CACHE = json.load(f)
    return _DATA_CACHE


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


def _planets_in_house(planets: Dict[str, Dict[str, Any]], house: int) -> List[str]:
    return [p for p, d in planets.items() if isinstance(d, dict) and d.get("house") == house]


def _is_debilitated(planet: str, sign: str) -> bool:
    return DEBILITATION_SIGN.get(planet) == sign


def _sign_house(sign: str, ascendant_sign: str) -> int:
    if sign not in ZODIAC or ascendant_sign not in ZODIAC:
        return 0
    asc_idx = ZODIAC.index(ascendant_sign)
    sign_idx = ZODIAC.index(sign)
    return ((sign_idx - asc_idx) % 12) + 1


def _lord_of_house(house_number: int, ascendant_sign: str) -> str:
    if ascendant_sign not in ZODIAC or not (1 <= house_number <= 12):
        return ""
    sign_idx = (ZODIAC.index(ascendant_sign) + house_number - 1) % 12
    return SIGN_LORD.get(ZODIAC[sign_idx], "")


# ───────────────────────────────────────────────────────────────
# Special Yoga detectors
# ───────────────────────────────────────────────────────────────

def _detect_leprosy(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Moon + Rahu in Lagna (1st house) without Jupiter aspect."""
    if _house_of("Moon", planets) != 1 or _house_of("Rahu", planets) != 1:
        return False
    # Jupiter aspects Lagna cancels
    if _aspects_house("Jupiter", 1, planets) or _house_of("Jupiter", planets) == 1:
        return False
    return True


def _detect_epilepsy(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Saturn + Moon in Lagna, afflicted by malefic (another malefic aspects them)."""
    if _house_of("Saturn", planets) != 1 or _house_of("Moon", planets) != 1:
        return False
    afflictor = any(
        m in planets and _aspects_house(m, 1, planets) and _house_of(m, planets) != 1
        for m in ("Mars", "Rahu", "Ketu", "Sun")
    )
    return afflictor


def _detect_diabetes(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Jupiter in 6th OR Venus + Saturn in 6th."""
    if _house_of("Jupiter", planets) == 6:
        return True
    if _house_of("Venus", planets) == 6 and _house_of("Saturn", planets) == 6:
        return True
    return False


def _detect_jaundice(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Sun + Mars in 6th house."""
    return _house_of("Sun", planets) == 6 and _house_of("Mars", planets) == 6


def _detect_tuberculosis(
    planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]
) -> bool:
    """Moon in 8th afflicted by malefic (conjunct or aspecting) + weak Lagna lord."""
    moon_h = _house_of("Moon", planets)
    if moon_h != 8:
        return False
    # Afflicted: a malefic either sits in 8th with Moon OR aspects it
    afflicted = any(
        m in planets and (
            _house_of(m, planets) == moon_h or _aspects_planet(m, "Moon", planets)
        )
        for m in ("Mars", "Saturn", "Rahu", "Ketu")
    )
    if not afflicted:
        return False
    # Weak Lagna lord: debilitated or in Dusthana
    asc = (chart.get("ascendant") or {}).get("sign", "")
    ll = SIGN_LORD.get(asc, "")
    if not ll or ll not in planets:
        return False
    ll_sign = _sign_of(ll, planets)
    ll_h = _house_of(ll, planets)
    return _is_debilitated(ll, ll_sign) or ll_h in DUSTHANAS


def _detect_insanity(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Moon + Saturn + Rahu conjunct in Dusthana (6/8/12)."""
    mh = _house_of("Moon", planets)
    if mh not in DUSTHANAS:
        return False
    return _house_of("Saturn", planets) == mh and _house_of("Rahu", planets) == mh


def _detect_blindness(planets: Dict[str, Dict[str, Any]]) -> bool:
    """Sun and Moon both debilitated with no benefic aspect on either."""
    sun_sign = _sign_of("Sun", planets)
    moon_sign = _sign_of("Moon", planets)
    if not (_is_debilitated("Sun", sun_sign) and _is_debilitated("Moon", moon_sign)):
        return False
    benefic_on_sun = any(
        b in planets and _aspects_planet(b, "Sun", planets)
        for b in ("Jupiter", "Venus", "Mercury")
    )
    benefic_on_moon = any(
        b in planets and _aspects_planet(b, "Moon", planets)
        for b in ("Jupiter", "Venus", "Mercury")
    )
    return not (benefic_on_sun or benefic_on_moon)


def _detect_eye_ear_disease(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """
    Eye: Sun or Moon in 2nd/12th afflicted by malefic (2nd=right eye, 12th=left eye).
    Ear: Saturn or Rahu in 3rd (3rd house rules ears/hearing), or 3rd lord debilitated.
    """
    # Eye: Sun afflicted in 2nd or 12th
    sun_h = _house_of("Sun", planets)
    if sun_h in (2, 12) and any(
        _aspects_planet(m, "Sun", planets) or _house_of(m, planets) == sun_h
        for m in ("Saturn", "Rahu", "Mars") if m in planets
    ):
        return True
    # Eye: Moon afflicted in 2nd or 12th
    moon_h = _house_of("Moon", planets)
    if moon_h in (2, 12) and any(
        _aspects_planet(m, "Moon", planets) or _house_of(m, planets) == moon_h
        for m in ("Saturn", "Rahu", "Mars") if m in planets
    ):
        return True
    # Ear: Saturn or Rahu in 3rd house
    if _house_of("Saturn", planets) == 3 or _house_of("Rahu", planets) == 3:
        return True
    # Ear: 3rd lord debilitated
    asc = (chart.get("ascendant") or {}).get("sign", "")
    third_lord = _lord_of_house(3, asc)
    if third_lord:
        return _is_debilitated(third_lord, _sign_of(third_lord, planets))
    return False


def _detect_cancer_tumor(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Rahu in 5th/8th + Saturn aspect on that house, OR two+ malefics in 8th."""
    rahu_h = _house_of("Rahu", planets)
    if rahu_h in (5, 8) and _aspects_house("Saturn", rahu_h, planets):
        return True
    malefics_in_8 = [p for p in ("Rahu", "Saturn", "Mars") if _house_of(p, planets) == 8]
    return len(malefics_in_8) >= 2


def _detect_heart_disease(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Sun in 4th afflicted by malefic, OR Sun debilitated in 4th or 5th house."""
    sun_h = _house_of("Sun", planets)
    sun_sign = _sign_of("Sun", planets)
    if sun_h == 4 and any(
        (_house_of(m, planets) == 4 or _aspects_house(m, 4, planets))
        for m in ("Saturn", "Rahu", "Mars") if m in planets
    ):
        return True
    return _is_debilitated("Sun", sun_sign) and sun_h in (4, 5)


def _detect_liver_disease(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Jupiter debilitated, OR Jupiter in dusthana with Saturn's aspect."""
    jup_sign = _sign_of("Jupiter", planets)
    jup_h = _house_of("Jupiter", planets)
    if _is_debilitated("Jupiter", jup_sign):
        return True
    return jup_h in DUSTHANAS and _aspects_planet("Saturn", "Jupiter", planets)


def _detect_kidney_disease(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Venus debilitated in dusthana, OR Venus in dusthana aspected by Saturn or Rahu."""
    ven_sign = _sign_of("Venus", planets)
    ven_h = _house_of("Venus", planets)
    if _is_debilitated("Venus", ven_sign) and ven_h in DUSTHANAS:
        return True
    return ven_h in DUSTHANAS and any(
        _aspects_planet(m, "Venus", planets) for m in ("Saturn", "Rahu")
    )


def _detect_accidents_wounds(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Mars in 8th with Saturn aspect, OR Mars + Rahu both in 8th/12th."""
    mars_h = _house_of("Mars", planets)
    rahu_h = _house_of("Rahu", planets)
    if mars_h == 8 and _aspects_planet("Saturn", "Mars", planets):
        return True
    return mars_h in (8, 12) and rahu_h in (8, 12)


def _detect_paralysis(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Saturn + Rahu conjunct in 2nd/3rd/12th, OR Saturn debilitated in 3rd house."""
    sat_h = _house_of("Saturn", planets)
    rahu_h = _house_of("Rahu", planets)
    sat_sign = _sign_of("Saturn", planets)
    if sat_h == rahu_h and sat_h in (2, 3, 12):
        return True
    return sat_h == 3 and _is_debilitated("Saturn", sat_sign)


def _detect_venereal_disease(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """Venus + Rahu conjunct in 7th/8th, OR Venus debilitated in 8th with Mars aspect."""
    ven_h = _house_of("Venus", planets)
    rahu_h = _house_of("Rahu", planets)
    ven_sign = _sign_of("Venus", planets)
    if ven_h == rahu_h and ven_h in (7, 8):
        return True
    return _is_debilitated("Venus", ven_sign) and ven_h == 8 and _aspects_planet("Mars", "Venus", planets)


def _detect_manner_of_death(planets: Dict[str, Dict[str, Any]], chart: Dict[str, Any]) -> bool:
    """8th lord debilitated in 12th, OR Saturn + Rahu both in 8th house."""
    asc = (chart.get("ascendant") or {}).get("sign", "")
    eighth_lord = _lord_of_house(8, asc)
    if eighth_lord:
        el_h = _house_of(eighth_lord, planets)
        el_sign = _sign_of(eighth_lord, planets)
        if _is_debilitated(eighth_lord, el_sign) and el_h == 12:
            return True
    return _house_of("Saturn", planets) == 8 and _house_of("Rahu", planets) == 8


_SPECIAL_DETECTORS = {
    "leprosy":          lambda p, c: _detect_leprosy(p),
    "epilepsy":         lambda p, c: _detect_epilepsy(p),
    "diabetes":         lambda p, c: _detect_diabetes(p),
    "jaundice":         lambda p, c: _detect_jaundice(p),
    "tuberculosis":     lambda p, c: _detect_tuberculosis(p, c),
    "insanity":         lambda p, c: _detect_insanity(p),
    "blindness":        lambda p, c: _detect_blindness(p),
    "eye_ear_disease":  _detect_eye_ear_disease,
    "cancer_tumor":     _detect_cancer_tumor,
    "heart_disease":    _detect_heart_disease,
    "liver_disease":    _detect_liver_disease,
    "kidney_disease":   _detect_kidney_disease,
    "accidents_wounds": _detect_accidents_wounds,
    "paralysis":        _detect_paralysis,
    "venereal_disease": _detect_venereal_disease,
    "manner_of_death":  _detect_manner_of_death,
}


# ───────────────────────────────────────────────────────────────
# Main entry
# ───────────────────────────────────────────────────────────────

def analyze_diseases(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze disease tendencies + special disease yogas.

    Returns:
      {
        "general_tendencies": [{planet, house, severity, diseases_en, diseases_hi, ...}, ...],
        "special_yogas_detected": [{key, name_en, name_hi, trigger_en, ..., severity, remedy_en, remedy_hi, sloka_ref}, ...],
        "timing_indicators": [...],
        "body_parts_affected": [...],
        "remedy_suggestions": [...],
        "sloka_ref": "Phaladeepika Adh. 14",
      }
    """
    result = {
        "general_tendencies": [],
        "special_yogas_detected": [],
        "timing_indicators": [],
        "body_parts_affected": [],
        "remedy_suggestions": [],
        "sloka_ref": "Phaladeepika Adh. 14",
    }

    if not isinstance(chart_data, dict):
        return result
    planets = chart_data.get("planets", {}) or {}
    if not planets:
        return result

    data = load_roga_data()
    planet_diseases = data.get("planet_diseases", {})
    body_parts = data.get("body_part_by_house", {})
    special_yogas = data.get("special_yogas", [])

    asc_sign = (chart_data.get("ascendant") or {}).get("sign", "")

    # ── 1. General tendencies: planets in 6/8/12 ──
    seen_planets: set = set()
    for house in (6, 8, 12):
        occupants = _planets_in_house(planets, house)
        house_info = body_parts.get(str(house), {})
        for planet in occupants:
            if planet not in planet_diseases or planet in seen_planets:
                continue
            seen_planets.add(planet)
            severity = {6: "moderate", 8: "severe", 12: "chronic"}[house]
            # Benefic in 6/8/12 partially cancels (reduces severity by one level)
            if planet in BENEFICS:
                severity = {"moderate": "low", "severe": "moderate", "chronic": "moderate"}[severity]
            entry = {
                "planet": planet,
                "house": house,
                "severity": severity,
                "diseases_en": planet_diseases[planet].get("en", []),
                "diseases_hi": planet_diseases[planet].get("hi", []),
                "body_part_en": house_info.get("en", ""),
                "body_part_hi": house_info.get("hi", ""),
                "reason_en": f"{planet} in house {house} — {severity} susceptibility.",
                "reason_hi": f"{planet} भाव {house} में — {severity} प्रवृत्ति।",
            }
            result["general_tendencies"].append(entry)
            result["body_parts_affected"].append({
                "house": house,
                "part_en": house_info.get("en", ""),
                "part_hi": house_info.get("hi", ""),
                "due_to_en": f"{planet} in {house}",
                "due_to_hi": f"{planet} भाव {house} में",
            })

    # ── 2. Special disease yogas ──
    for yoga in special_yogas:
        key = yoga.get("key")
        detector = _SPECIAL_DETECTORS.get(key)
        if detector is None:
            continue
        try:
            triggered = detector(planets, chart_data)
        except Exception:
            triggered = False
        if triggered:
            entry = {
                "key": key,
                "name_en": yoga.get("name_en", ""),
                "name_hi": yoga.get("name_hi", ""),
                "trigger_en": yoga.get("trigger_en", ""),
                "trigger_hi": yoga.get("trigger_hi", ""),
                "severity": yoga.get("severity", "moderate"),
                "remedy_en": yoga.get("remedy_en", ""),
                "remedy_hi": yoga.get("remedy_hi", ""),
                "sloka_ref": yoga.get("sloka_ref", ""),
            }
            result["special_yogas_detected"].append(entry)
            result["remedy_suggestions"].append({
                "for_en": yoga.get("name_en", ""),
                "for_hi": yoga.get("name_hi", ""),
                "remedy_en": yoga.get("remedy_en", ""),
                "remedy_hi": yoga.get("remedy_hi", ""),
            })

    # ── 3. Timing indicators (dasha + transit hints) ──
    afflicting_planets = [e["planet"] for e in result["general_tendencies"]]
    sixth_lord = _lord_of_house(6, asc_sign)
    eighth_lord = _lord_of_house(8, asc_sign)
    for p in afflicting_planets:
        result["timing_indicators"].append({
            "en": f"Watch during Mahadasha / Antardasha of {p}",
            "hi": f"{p} की महादशा / अंतर्दशा में सावधानी",
        })
    if sixth_lord:
        result["timing_indicators"].append({
            "en": f"Watch during Antardasha of 6th lord ({sixth_lord})",
            "hi": f"षष्ठेश ({sixth_lord}) की अंतर्दशा में सावधानी",
        })
    if eighth_lord:
        result["timing_indicators"].append({
            "en": f"Watch during Antardasha of 8th lord ({eighth_lord})",
            "hi": f"अष्टमेश ({eighth_lord}) की अंतर्दशा में सावधानी",
        })
    # Sade Sati hint: always applicable when Saturn transits natal Moon area
    if "Moon" in planets:
        result["timing_indicators"].append({
            "en": "Monitor during Saturn transit over natal Moon (Sade Sati phases)",
            "hi": "शनि का जन्म-चंद्र पर गोचर (साढ़े साती) में ध्यान रखें",
        })

    return result
