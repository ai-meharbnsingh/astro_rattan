"""
lalkitab_chakar.py — 35-Sala vs 36-Sala Chakar auto-determination
==================================================================
Reference: Lal Kitab 1952 (Pandit Roop Chand Joshi) — chapter on
           Saala Grah / annual cycles.

LK recognises TWO annual-cycle variants:

  • 35-Sala Chakar — applies when the ascendant lord is one of the
    seven visible planets (Sun, Moon, Mars, Mercury, Jupiter, Venus,
    Saturn). The Saala Grah cycle repeats every 35 years across the
    three 35-year life phases.

  • 36-Sala Chakar — applies when the ascendant lord is a shadow
    planet (Rahu or Ketu). Because the shadow planets are not
    visible, LK canon adds ONE extra "shadow year" before the cycle
    resets, making it 36 years instead of 35.

Vedic lord mapping (used by LK):
    Aries/Scorpio      → Mars
    Taurus/Libra       → Venus
    Gemini/Virgo       → Mercury
    Cancer             → Moon
    Leo                → Sun
    Sagittarius/Pisces → Jupiter
    Capricorn/Aquarius → Saturn

Rahu / Ketu are NEVER rashi lords in classical Vedic. Some LK
variants ascribe Rahu co-lordship to Aquarius and Ketu co-lordship
to Scorpio, but this function does NOT treat those co-lordships as
triggering 36-Sala on their own — it would over-apply the shadow
cycle to a large fraction of charts. Instead we only emit 36-Sala
when the ascendant (1st house) physically contains Rahu or Ketu —
i.e. the ascendant lord is effectively replaced by a shadow planet
sitting in H1.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


# ── Sign → ascendant lord (Vedic / LK canon) ──────────────────────
_SIGN_LORD: Dict[str, str] = {
    "Aries":       "Mars",
    "Taurus":      "Venus",
    "Gemini":      "Mercury",
    "Cancer":      "Moon",
    "Leo":         "Sun",
    "Virgo":       "Mercury",
    "Libra":       "Venus",
    "Scorpio":     "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn":   "Saturn",
    "Aquarius":    "Saturn",
    "Pisces":      "Jupiter",
}

# ── Hindi planet names ────────────────────────────────────────────
_PLANET_HI: Dict[str, str] = {
    "Sun":     "सूर्य",
    "Moon":    "चन्द्र",
    "Mars":    "मंगल",
    "Mercury": "बुध",
    "Jupiter": "गुरु",
    "Venus":   "शुक्र",
    "Saturn":  "शनि",
    "Rahu":    "राहु",
    "Ketu":    "केतु",
}

# ── Hindi sign names ──────────────────────────────────────────────
_SIGN_HI: Dict[str, str] = {
    "Aries":       "मेष",
    "Taurus":      "वृषभ",
    "Gemini":      "मिथुन",
    "Cancer":      "कर्क",
    "Leo":         "सिंह",
    "Virgo":       "कन्या",
    "Libra":       "तुला",
    "Scorpio":     "वृश्चिक",
    "Sagittarius": "धनु",
    "Capricorn":   "मकर",
    "Aquarius":    "कुम्भ",
    "Pisces":      "मीन",
}

_SHADOW_PLANETS = {"Rahu", "Ketu"}
_VISIBLE_PLANETS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}


def _normalize_sign(sign: str) -> str:
    """Capitalise first letter so 'aries', 'ARIES' and 'Aries' all map."""
    if not sign or not isinstance(sign, str):
        return ""
    s = sign.strip()
    if not s:
        return ""
    return s[0].upper() + s[1:].lower()


def _normalize_planet(planet: str) -> str:
    if not planet or not isinstance(planet, str):
        return ""
    p = planet.strip()
    if not p:
        return ""
    return p[0].upper() + p[1:].lower()


def detect_chakar_cycle(
    ascendant_sign: str,
    planets_in_h1: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Decide whether the native follows the 35-Sala or 36-Sala Chakar.

    Args:
        ascendant_sign:  Zodiac sign of the ascendant (e.g. "Leo", "Scorpio").
                         Must be a str or None — passing a list/dict/int raises TypeError.
        planets_in_h1:   Planets occupying the 1st house (LK-style). If Rahu
                         or Ketu sits in H1 the shadow cycle (36-Sala) fires
                         even though Rahu/Ketu are not formal sign lords.

    Returns:
        {
          cycle_length:     35 | 36,
          ascendant_lord:   str,        # English planet name
          ascendant_lord_hi: str,       # Devanagari
          ascendant_sign:   str,        # echoed (normalised)
          ascendant_sign_hi: str,
          trigger:          "visible_lord" | "shadow_in_h1",
          reason_en:        str,
          reason_hi:        str,
          shadow_year_en:   str | None, # only populated for 36-Sala
          shadow_year_hi:   str | None,
          source:           "LK_CANONICAL",
          lk_ref:           "3.04",      # LK 1952 Saala Grah section
        }

    Raises:
        TypeError: when ascendant_sign is not a str or None.
    """
    if ascendant_sign is not None and not isinstance(ascendant_sign, str):
        raise TypeError(
            f"ascendant_sign must be a str (e.g. 'Taurus'), got {type(ascendant_sign).__name__}. "
            "Pass the zodiac sign name, not a position list or house dict."
        )
    sign = _normalize_sign(ascendant_sign)
    h1_planets = [_normalize_planet(p) for p in (planets_in_h1 or []) if p]
    h1_planets = [p for p in h1_planets if p]  # drop empties

    # ── Step 1: determine ascendant lord from sign ──────────────
    asc_lord = _SIGN_LORD.get(sign, "")
    if not asc_lord:
        # Unknown sign — degrade gracefully to 35-Sala with a warning.
        return {
            "cycle_length": 35,
            "ascendant_lord": "",
            "ascendant_lord_hi": "",
            "ascendant_sign": sign,
            "ascendant_sign_hi": _SIGN_HI.get(sign, sign),
            "trigger": "unknown_sign",
            "reason_en": (
                f"Ascendant sign '{ascendant_sign}' not recognised — "
                f"defaulting to 35-Sala Chakar."
            ),
            "reason_hi": (
                f"लग्न राशि '{ascendant_sign}' पहचानी नहीं गई — "
                f"डिफ़ॉल्ट रूप से 35-साला चक्र लागू।"
            ),
            "shadow_year_en": None,
            "shadow_year_hi": None,
            "source": "LK_CANONICAL",
            "lk_ref": "3.04",
        }

    sign_hi = _SIGN_HI.get(sign, sign)
    lord_hi = _PLANET_HI.get(asc_lord, asc_lord)

    # ── Step 2: check for shadow planet physically in H1 ────────
    shadow_in_h1 = [p for p in h1_planets if p in _SHADOW_PLANETS]

    if shadow_in_h1:
        # Shadow planet sitting in the 1st house overrides the
        # formal sign-lord for Chakar purposes — 36-Sala fires.
        shadow = shadow_in_h1[0]  # Rahu wins if both present (canonical)
        if "Rahu" in shadow_in_h1:
            shadow = "Rahu"
        shadow_hi = _PLANET_HI.get(shadow, shadow)
        return {
            "cycle_length": 36,
            "ascendant_lord": shadow,
            "ascendant_lord_hi": shadow_hi,
            "ascendant_sign": sign,
            "ascendant_sign_hi": sign_hi,
            "trigger": "shadow_in_h1",
            "reason_en": (
                f"{shadow} (shadow planet) occupies the 1st house, "
                f"overriding {asc_lord} as the effective ascendant lord. "
                f"LK canon adds one shadow-year, so the 36-Sala Chakar applies."
            ),
            "reason_hi": (
                f"{shadow_hi} (छाया ग्रह) प्रथम भाव में विराजमान है और "
                f"{lord_hi} की जगह प्रभावी लग्नेश बन जाता है। "
                f"लाल किताब अनुसार एक छाया-वर्ष जुड़ता है अतः 36-साला चक्र लागू होता है।"
            ),
            "shadow_year_en": (
                f"A 36th 'shadow year' is added before the Saala Grah cycle "
                f"repeats. During this year the native should avoid major "
                f"initiations — it is a karmic reset, not a new beginning."
            ),
            "shadow_year_hi": (
                f"साला ग्रह चक्र दोहराने से पहले 36वाँ 'छाया वर्ष' जुड़ता है। "
                f"इस वर्ष नए आरंभ से बचना चाहिए — यह कर्मिक पुनः-संतुलन है, "
                f"नए कार्य का आरंभ नहीं।"
            ),
            "source": "LK_CANONICAL",
            "lk_ref": "3.04",
        }

    # ── Step 3: default — sign lord is a visible planet → 35-Sala ──
    return {
        "cycle_length": 35,
        "ascendant_lord": asc_lord,
        "ascendant_lord_hi": lord_hi,
        "ascendant_sign": sign,
        "ascendant_sign_hi": sign_hi,
        "trigger": "visible_lord",
        "reason_en": (
            f"Ascendant is {sign}, lord {asc_lord} — a visible planet. "
            f"The classical 35-Sala Chakar applies (cycle repeats every 35 years "
            f"across three life phases of 35 years each)."
        ),
        "reason_hi": (
            f"लग्न {sign_hi} है, लग्नेश {lord_hi} — एक दृश्य ग्रह। "
            f"शास्त्रीय 35-साला चक्र लागू होता है (प्रति 35 वर्ष में चक्र "
            f"पुनरावृत्ति, तीन जीवन-चरणों में विभाजित)।"
        ),
        "shadow_year_en": None,
        "shadow_year_hi": None,
        "source": "LK_CANONICAL",
        "lk_ref": "3.04",
    }
