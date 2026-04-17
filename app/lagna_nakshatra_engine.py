"""
lagna_nakshatra_engine.py — Janma Predictions (Lagna + Moon Nakshatra)
======================================================================
Implements Phaladeepika Adhyaya 9 (Mesha-phala — Lagna-wise profile) and
Adhyaya 10 (Nakshatradhyaya — Moon's nakshatra predictions).

Data:
  app/data/lagna_profiles.json       — 12 Lagna profiles (body / temperament / fortune)
  app/data/nakshatra_predictions.json — 27 Moon-nakshatra profiles

Main functions:
  analyze_lagna_profile(chart_data) -> dict
  analyze_moon_nakshatra(chart_data) -> dict
  analyze_janma_predictions(chart_data) -> dict
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

# ───────────────────────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────────────────────

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

ZODIAC_SIGN_HI = {
    "Aries": "मेष", "Taurus": "वृष", "Gemini": "मिथुन", "Cancer": "कर्क",
    "Leo": "सिंह", "Virgo": "कन्या", "Libra": "तुला", "Scorpio": "वृश्चिक",
    "Sagittarius": "धनु", "Capricorn": "मकर", "Aquarius": "कुम्भ", "Pisces": "मीन",
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_SPAN = 360.0 / 27.0            # 13.3333...°
PADA_SPAN = NAKSHATRA_SPAN / 4.0         # 3.3333...°

# ───────────────────────────────────────────────────────────────
# Data loading
# ───────────────────────────────────────────────────────────────

_LAGNA_PATH = os.path.join(os.path.dirname(__file__), "data", "lagna_profiles.json")
_NAK_PATH = os.path.join(os.path.dirname(__file__), "data", "nakshatra_predictions.json")

_LAGNA_CACHE: Optional[Dict[str, Any]] = None
_NAK_CACHE: Optional[Dict[str, Any]] = None


def load_lagna_profiles() -> Dict[str, Any]:
    """Load and cache the 12-Lagna profile JSON."""
    global _LAGNA_CACHE
    if _LAGNA_CACHE is None:
        with open(_LAGNA_PATH, "r", encoding="utf-8") as f:
            _LAGNA_CACHE = json.load(f)
    return _LAGNA_CACHE


def load_nakshatra_predictions() -> Dict[str, Any]:
    """Load and cache the 27-nakshatra prediction JSON."""
    global _NAK_CACHE
    if _NAK_CACHE is None:
        with open(_NAK_PATH, "r", encoding="utf-8") as f:
            _NAK_CACHE = json.load(f)
    return _NAK_CACHE


# ───────────────────────────────────────────────────────────────
# Helpers — nakshatra / pada from longitude
# ───────────────────────────────────────────────────────────────

def get_nakshatra_index(longitude: float) -> int:
    """Return 0..26 index for a sidereal longitude in [0, 360)."""
    try:
        lon = float(longitude) % 360.0
    except (TypeError, ValueError):
        return 0
    idx = int(lon // NAKSHATRA_SPAN)
    if idx < 0:
        idx = 0
    if idx > 26:
        idx = 26
    return idx


def get_pada(longitude: float) -> int:
    """Return pada 1..4 for the given sidereal longitude.

    Each pada = 3°20' = 3.3333...°. Uses a small epsilon so that classical
    round boundaries (3°20', 6°40', 10°) fall cleanly into the next pada
    rather than being left on the previous one due to the tiny float error
    in PADA_SPAN (Python stores 3.333... as 3.3333333333333335).
    """
    try:
        lon = float(longitude) % 360.0
    except (TypeError, ValueError):
        return 1
    within = lon - (int(lon // NAKSHATRA_SPAN) * NAKSHATRA_SPAN)
    eps = 1e-9
    pada_idx = int((within + eps) // PADA_SPAN)
    if pada_idx < 0:
        pada_idx = 0
    if pada_idx > 3:
        pada_idx = 3
    return pada_idx + 1


# ───────────────────────────────────────────────────────────────
# Adh. 9 — Lagna profile
# ───────────────────────────────────────────────────────────────

def analyze_lagna_profile(chart_data: Any) -> Dict[str, Any]:
    """
    Return Lagna (ascendant-sign) profile from Phaladeepika Adh. 9.

    Output: {
      lagna_sign, lagna_sign_hi,
      body_type_en, body_type_hi,
      temperament_en, temperament_hi,
      fortune_en, fortune_hi,
      lucky_directions_en, lucky_directions_hi,
      sloka_ref
    }

    On unknown/missing lagna sign → returns empty-string fields and empty
    direction lists with a safe default sloka_ref; does not raise.
    """
    profiles = load_lagna_profiles()

    lagna_sign = ""
    if isinstance(chart_data, dict):
        asc = chart_data.get("ascendant")
        if isinstance(asc, dict):
            lagna_sign = str(asc.get("sign") or "")

    entry = profiles.get(lagna_sign) if lagna_sign in profiles else None
    if not entry:
        return {
            "lagna_sign": lagna_sign,
            "lagna_sign_hi": ZODIAC_SIGN_HI.get(lagna_sign, ""),
            "body_type_en": "",
            "body_type_hi": "",
            "temperament_en": "",
            "temperament_hi": "",
            "fortune_en": "",
            "fortune_hi": "",
            "lucky_directions_en": [],
            "lucky_directions_hi": [],
            "sloka_ref": "Phaladeepika Adh. 9",
        }

    return {
        "lagna_sign": lagna_sign,
        "lagna_sign_hi": ZODIAC_SIGN_HI.get(lagna_sign, ""),
        "body_type_en": entry.get("body_type_en", ""),
        "body_type_hi": entry.get("body_type_hi", ""),
        "temperament_en": entry.get("temperament_en", ""),
        "temperament_hi": entry.get("temperament_hi", ""),
        "fortune_en": entry.get("fortune_en", ""),
        "fortune_hi": entry.get("fortune_hi", ""),
        "lucky_directions_en": list(entry.get("lucky_directions_en", [])),
        "lucky_directions_hi": list(entry.get("lucky_directions_hi", [])),
        "sloka_ref": entry.get("sloka_ref", "Phaladeepika Adh. 9"),
    }


# ───────────────────────────────────────────────────────────────
# Adh. 10 — Moon-nakshatra predictions
# ───────────────────────────────────────────────────────────────

def _extract_moon_longitude(chart_data: Any) -> Optional[float]:
    """Best-effort extraction of Moon's sidereal longitude from a chart dict.

    Accepts either a full-longitude (0..360) or a sign_degree (0..30); when
    sign_degree is present with a sign, the full longitude is reconstructed.
    Returns None if no Moon data available.
    """
    if not isinstance(chart_data, dict):
        return None
    planets = chart_data.get("planets")
    if not isinstance(planets, dict):
        return None
    moon = planets.get("Moon")
    if not isinstance(moon, dict):
        return None

    # Prefer full longitude if present
    lon = moon.get("longitude")
    try:
        if lon is not None:
            lonf = float(lon)
            return lonf % 360.0
    except (TypeError, ValueError):
        pass

    # Else reconstruct from sign + sign_degree (whole-sign)
    sign = str(moon.get("sign") or "")
    sign_deg = moon.get("sign_degree")
    if sign in ZODIAC_SIGNS and sign_deg is not None:
        try:
            return (ZODIAC_SIGNS.index(sign) * 30.0 + float(sign_deg)) % 360.0
        except (TypeError, ValueError):
            return None
    return None


def analyze_moon_nakshatra(chart_data: Any) -> Dict[str, Any]:
    """
    Return Moon-nakshatra prediction from Phaladeepika Adh. 10.

    Output: {
      nakshatra, pada (1..4),
      deity_en, deity_hi, symbol_en, symbol_hi,
      character_en, character_hi,
      strengths_en/hi, vulnerabilities_en/hi,
      career_affinity_en/hi,
      sloka_ref
    }

    On missing Moon → empty fields with safe default sloka_ref.
    """
    predictions = load_nakshatra_predictions()
    moon_lon = _extract_moon_longitude(chart_data)

    if moon_lon is None:
        return {
            "nakshatra": "",
            "pada": 0,
            "deity_en": "",
            "deity_hi": "",
            "symbol_en": "",
            "symbol_hi": "",
            "character_en": "",
            "character_hi": "",
            "strengths_en": [],
            "strengths_hi": [],
            "vulnerabilities_en": [],
            "vulnerabilities_hi": [],
            "career_affinity_en": [],
            "career_affinity_hi": [],
            "sloka_ref": "Phaladeepika Adh. 10",
        }

    nak_idx = get_nakshatra_index(moon_lon)
    pada = get_pada(moon_lon)
    nak_name = NAKSHATRAS[nak_idx]
    entry = predictions.get(nak_name, {})

    return {
        "nakshatra": nak_name,
        "pada": pada,
        "deity_en": entry.get("deity_en", ""),
        "deity_hi": entry.get("deity_hi", ""),
        "symbol_en": entry.get("symbol_en", ""),
        "symbol_hi": entry.get("symbol_hi", ""),
        "character_en": entry.get("character_en", ""),
        "character_hi": entry.get("character_hi", ""),
        "strengths_en": list(entry.get("strengths_en", [])),
        "strengths_hi": list(entry.get("strengths_hi", [])),
        "vulnerabilities_en": list(entry.get("vulnerabilities_en", [])),
        "vulnerabilities_hi": list(entry.get("vulnerabilities_hi", [])),
        "career_affinity_en": list(entry.get("career_affinity_en", [])),
        "career_affinity_hi": list(entry.get("career_affinity_hi", [])),
        "sloka_ref": entry.get("sloka_ref", "Phaladeepika Adh. 10"),
    }


# ───────────────────────────────────────────────────────────────
# Combined Janma Predictions
# ───────────────────────────────────────────────────────────────

def _combined_narrative_en(lagna: Dict[str, Any], moon: Dict[str, Any]) -> str:
    if not lagna.get("lagna_sign") and not moon.get("nakshatra"):
        return ""
    parts: List[str] = []
    if lagna.get("lagna_sign"):
        parts.append(
            f"With {lagna['lagna_sign']} Lagna the native is shaped outwardly by "
            f"{lagna.get('body_type_en', '').rstrip('.')}, tempered within by "
            f"{lagna.get('temperament_en', '').rstrip('.')}."
        )
    if moon.get("nakshatra"):
        parts.append(
            f"The Moon in {moon['nakshatra']} (pada {moon.get('pada', 0)}), "
            f"ruled by {moon.get('deity_en', '').rstrip('.')}, gives a mind that is "
            f"{moon.get('character_en', '').rstrip('.')}."
        )
    return " ".join(parts).strip()


def _combined_narrative_hi(lagna: Dict[str, Any], moon: Dict[str, Any]) -> str:
    if not lagna.get("lagna_sign") and not moon.get("nakshatra"):
        return ""
    parts: List[str] = []
    if lagna.get("lagna_sign"):
        parts.append(
            f"{lagna.get('lagna_sign_hi', '') or lagna['lagna_sign']} लग्न में जन्म से "
            f"बाह्य स्वरूप: {lagna.get('body_type_hi', '').rstrip('।')}। अन्तःकरण: "
            f"{lagna.get('temperament_hi', '').rstrip('।')}।"
        )
    if moon.get("nakshatra"):
        parts.append(
            f"चन्द्र {moon['nakshatra']} नक्षत्र (पाद {moon.get('pada', 0)}) में; "
            f"देवता {moon.get('deity_hi', '')}। मनोभाव: "
            f"{moon.get('character_hi', '').rstrip('।')}।"
        )
    return " ".join(parts).strip()


def analyze_janma_predictions(chart_data: Any) -> Dict[str, Any]:
    """
    Return combined Lagna + Moon-Nakshatra analysis (Phaladeepika Adh. 9 + 10).

    Output: {
      lagna_profile: {...Adh. 9...},
      moon_nakshatra: {...Adh. 10...},
      combined_narrative_en, combined_narrative_hi,
      sloka_ref
    }
    """
    lagna = analyze_lagna_profile(chart_data)
    moon = analyze_moon_nakshatra(chart_data)
    return {
        "lagna_profile": lagna,
        "moon_nakshatra": moon,
        "combined_narrative_en": _combined_narrative_en(lagna, moon),
        "combined_narrative_hi": _combined_narrative_hi(lagna, moon),
        "sloka_ref": "Phaladeepika Adh. 9 + Adh. 10",
    }
