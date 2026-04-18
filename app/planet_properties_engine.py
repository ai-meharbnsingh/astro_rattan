"""
planet_properties_engine.py — Phaladeepika Adh. 1–2 Planet Properties
======================================================================

Implements three classical Vedic astrology classification systems from
Phaladeepika Adhyayas 1 and 2 (Mantreshvara):

  Feature #18 — Stage of Life (graha svabhava / Baladi Avastha)
    Each planet has a fixed natural stage (Youth / Child / Mature / Old)
    AND a degree-based dynamic stage per sign position (Bala → Mrita).

  Feature #20 — Sattvika / Rajasa / Tamasa guna classification
    Each planet is assigned one of the three Prakritic gunas.

  Feature #21 — Shirodaya / Prusthodaya / Ubhaodaya rising mode
    Each sign has a classical "rising mode" that characterises when in
    life the Lagna delivers its strongest results.

Public API:
    get_planet_properties(chart_data)   → per-planet stage + guna + avastha
    get_lagna_rising_analysis(chart_data) → lagna rising mode details

Data source:
    app/data/planet_properties.json
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, Tuple

# ── Data Loading ─────────────────────────────────────────────────────

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "planet_properties.json")

_DATA: Optional[Dict[str, Any]] = None


def _load_data() -> Dict[str, Any]:
    global _DATA
    if _DATA is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as fh:
            _DATA = json.load(fh)
    return _DATA


# ── Sign Constants ───────────────────────────────────────────────────

_SIGN_NAMES = [
    "Aries",       # 1  — odd
    "Taurus",      # 2  — even
    "Gemini",      # 3  — odd
    "Cancer",      # 4  — even
    "Leo",         # 5  — odd
    "Virgo",       # 6  — even
    "Libra",       # 7  — odd
    "Scorpio",     # 8  — even
    "Sagittarius", # 9  — odd
    "Capricorn",   # 10 — even
    "Aquarius",    # 11 — odd
    "Pisces",      # 12 — even
]

# Sign number (1-based) -> True if odd
_ODD_SIGN: Dict[int, bool] = {i + 1: (i + 1) % 2 == 1 for i in range(12)}

# Name to 1-based sign number
_SIGN_NUMBER: Dict[str, int] = {name: i + 1 for i, name in enumerate(_SIGN_NAMES)}

ALL_PLANETS = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
)


# ── Baladi Avastha Calculation ───────────────────────────────────────

# Stage sequence for ODD signs (degree 0 → 30):
#   0-6  = Bala, 6-12 = Kumara, 12-18 = Yuva, 18-24 = Vriddha, 24-30 = Mrita
_ODD_SEQUENCE = ["Bala", "Kumara", "Yuva", "Vriddha", "Mrita"]

# Stage sequence for EVEN signs (reversed):
#   0-6  = Mrita, 6-12 = Vriddha, 12-18 = Yuva, 18-24 = Kumara, 24-30 = Bala
_EVEN_SEQUENCE = ["Mrita", "Vriddha", "Yuva", "Kumara", "Bala"]


def _compute_baladi_avastha(
    sign_name: str,
    sign_degree: float,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Determine Baladi Avastha for a planet at `sign_degree` degrees (0-30)
    within `sign_name`.

    Returns a dict merging the stage key and stage-level data.
    """
    sign_num = _SIGN_NUMBER.get(sign_name)
    if sign_num is None:
        return {"stage": "Unknown", "name_hi": "अज्ञात", "strength_fraction": 0.0,
                "description_en": "Sign not recognised.", "description_hi": "राशि अज्ञात।"}

    deg = max(0.0, min(float(sign_degree), 29.9999))
    bucket = int(deg / 6)           # 0..4
    bucket = min(bucket, 4)

    is_odd = _ODD_SIGN[sign_num]
    sequence = _ODD_SEQUENCE if is_odd else _EVEN_SEQUENCE
    stage_key = sequence[bucket]

    stage_data = data["baladi_avastha_stages"].get(stage_key, {})
    result = {"stage": stage_key}
    result.update(stage_data)
    return result


# ── Public API ───────────────────────────────────────────────────────

def get_planet_properties(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns stage-of-life, Baladi Avastha, and guna for each planet in the chart.

    Args:
        chart_data: must contain a "planets" key, each entry having at least:
            - "sign" (str)     — sign name, e.g. "Aries"
            - "sign_degree" (float) — degree within sign (0-30)
            - "longitude" (float, optional) — ecliptic longitude (degrees)

    Returns:
    {
      "planets": {
        "<Planet>": {
          "stage_of_life": {
            "stage": str, "stage_hi": str,
            "description_en": str, "description_hi": str
          },
          "guna": {
            "guna": str, "guna_hi": str,
            "description_en": str, "description_hi": str
          },
          "baladi_avastha": {
            "stage": str, "name_hi": str, "strength_fraction": float,
            "description_en": str, "description_hi": str
          },
          "sign_degree": float,
          "sign": str,
        },
        ...
      },
      "sloka_ref": "Phaladeepika Adh. 2"
    }
    """
    data = _load_data()
    planets_in = chart_data.get("planets", {})
    planets_out: Dict[str, Any] = {}

    for planet_name, planet_data in planets_in.items():
        sign = planet_data.get("sign", "")
        sign_degree = float(planet_data.get("sign_degree", 0.0))

        # --- Stage of Life (fixed, by planet identity) ---
        stage_of_life = data["stage_of_life"].get(planet_name)
        if stage_of_life is None:
            stage_of_life = {
                "stage": "Unknown",
                "stage_hi": "अज्ञात",
                "description_en": "No classical stage defined for this body.",
                "description_hi": "इस ग्रह के लिए कोई शास्त्रीय अवस्था परिभाषित नहीं।",
            }

        # --- Guna (fixed, by planet identity) ---
        guna = data["gunas"].get(planet_name)
        if guna is None:
            guna = {
                "guna": "Unknown",
                "guna_hi": "अज्ञात",
                "description_en": "No classical guna defined for this body.",
                "description_hi": "इस ग्रह के लिए कोई शास्त्रीय गुण परिभाषित नहीं।",
            }

        # --- Baladi Avastha (dynamic, by degree in sign) ---
        baladi = _compute_baladi_avastha(sign, sign_degree, data)

        planets_out[planet_name] = {
            "stage_of_life": dict(stage_of_life),
            "guna": dict(guna),
            "baladi_avastha": baladi,
            "sign_degree": sign_degree,
            "sign": sign,
        }

    return {
        "planets": planets_out,
        "sloka_ref": (
            data["sloka_refs"]["stage_of_life"]
            + " | "
            + data["sloka_refs"]["gunas"]
            + " | "
            + data["sloka_refs"]["baladi_avastha"]
        ),
    }


def get_lagna_rising_analysis(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns Shirodaya / Prusthodaya / Ubhaodaya analysis for the Lagna sign.

    Args:
        chart_data: must contain an "ascendant" key with:
            - "sign" (str)      — sign name, e.g. "Leo"
            - "longitude" (float, optional) — ecliptic longitude

    Returns:
    {
      "lagna_sign": str,
      "rising_mode": str,          # "Shirodaya" | "Prusthodaya" | "Ubhaodaya"
      "rising_mode_hi": str,
      "effect_en": str,
      "effect_hi": str,
      "sloka_ref": str
    }
    """
    data = _load_data()
    ascendant = chart_data.get("ascendant", {})
    lagna_sign = ascendant.get("sign", "")

    rising = data["rising_signs"].get(lagna_sign)
    if rising is None:
        return {
            "lagna_sign": lagna_sign,
            "rising_mode": "Unknown",
            "rising_mode_hi": "अज्ञात",
            "effect_en": f"Rising mode not defined for sign '{lagna_sign}'.",
            "effect_hi": f"'{lagna_sign}' राशि के लिए उदय-प्रकार परिभाषित नहीं।",
            "sloka_ref": data["sloka_refs"]["rising_signs"],
        }

    return {
        "lagna_sign": lagna_sign,
        "rising_mode": rising["mode"],
        "rising_mode_hi": rising["mode_hi"],
        "effect_en": rising["effect_en"],
        "effect_hi": rising["effect_hi"],
        "sloka_ref": data["sloka_refs"]["rising_signs"],
    }
