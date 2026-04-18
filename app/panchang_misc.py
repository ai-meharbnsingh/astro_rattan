"""
panchang_misc.py -- Miscellaneous Panchang Calculations
========================================================
Pure calculation functions (no Flask/FastAPI dependencies).
All strings carry both English AND Hindi labels.

Calculations covered:
- Mantri Mandala (planetary cabinet for the Hindu year)
- Kaliyuga & astronomical epoch data (Kali Ahargana, Rata Die, MJD)
- Panchaka Rahita Muhurta (safe/unsafe windows during Panchaka)
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# ============================================================
# MANTRI MANDALA — Planetary Cabinet (मन्त्री मण्डल)
# ============================================================
# The 10 roles in the Mantri Mandala, assigned cyclically from the
# Raja (King) planet determined by the weekday of Chaitra Shukla
# Pratipada for the given Vikram Samvat year.

MANDALA_ROLES: List[tuple[str, str]] = [
    ("Raja", "राजा"),                    # King
    ("Mantri", "मन्त्री"),              # Minister
    ("Senadhipati", "सेनाधिपति"),       # Commander
    ("Sasyadhipati", "सस्याधिपति"),     # Crops Lord
    ("Dhanyadhipati", "धान्याधिपति"),   # Grain Lord
    ("Dhanadhipati", "धनाधिपति"),       # Wealth Lord
    ("Meghadhipati", "मेघाधिपति"),      # Rain Lord
    ("Rasadhipati", "रसाधिपति"),        # Liquids Lord
    ("Nirasadhipati", "नीरसाधिपति"),    # Minerals Lord
    ("Phaladhipati", "फलाधिपति"),       # Fruits Lord
]

PLANET_NAMES: Dict[str, str] = {
    "Sun": "सूर्य",
    "Moon": "चन्द्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "बृहस्पति",
    "Venus": "शुक्र",
    "Saturn": "शनि",
}

# Classical 7-planet weekday order (Sun=Sunday .. Saturn=Saturday)
GRAHA_ORDER: List[str] = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
]

# Raja planet for recent Vikram Samvat years (based on weekday of
# Chaitra Shukla Pratipada).  Extend as needed.
SAMVAT_RAJA: Dict[int, str] = {
    2080: "Mercury",  # 2023-24
    2081: "Jupiter",  # 2024-25
    2082: "Saturn",   # 2025-26
    2083: "Sun",      # 2026-27
    2084: "Moon",     # 2027-28
}


def calculate_mantri_mandala(vikram_samvat_year: int) -> List[Dict[str, str]]:
    """
    Return the 10-member planetary cabinet for *vikram_samvat_year*.

    Each entry: {"role", "role_hindi", "planet", "planet_hindi"}.

    The Raja (King) planet is looked up from SAMVAT_RAJA.  If the year
    is unknown, a modulo-7 fallback on GRAHA_ORDER is used so we always
    return a result.
    """
    raja_planet = SAMVAT_RAJA.get(vikram_samvat_year)
    if raja_planet is None:
        # Fallback: cycle through GRAHA_ORDER based on year
        raja_planet = GRAHA_ORDER[vikram_samvat_year % 7]

    raja_idx = GRAHA_ORDER.index(raja_planet)

    result: List[Dict[str, str]] = []
    for i, (role_en, role_hi) in enumerate(MANDALA_ROLES):
        planet = GRAHA_ORDER[(raja_idx + i) % len(GRAHA_ORDER)]
        result.append({
            "role": role_en,
            "role_hindi": role_hi,
            "planet": planet,
            "planet_hindi": PLANET_NAMES[planet],
        })
    return result


# ============================================================
# KALIYUGA & ASTRONOMICAL EPOCH DATA
# ============================================================
# Kaliyuga epoch: 3102 BCE (Feb 17/18), Julian Day 588465.5.
# Kali year = Gregorian year + 3101 (simplified; before April use +3101).

KALI_EPOCH_JD: float = 588465.5  # JD of Kaliyuga start
RATA_DIE_OFFSET: float = 1721424.5
MJD_OFFSET: float = 2400000.5


def calculate_astronomical_data(
    date_str: str,
    jd: Optional[float] = None,
    ayanamsha: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Compute astronomical epoch values for a Gregorian date string (YYYY-MM-DD).

    Returns dict with:
      kaliyuga_year, kali_ahargana, rata_die, julian_day,
      modified_julian_day, ayanamsha — each with English & Hindi labels.
    """
    year, month, day = map(int, date_str.split("-"))

    # Kaliyuga year (simplified)
    kali_year = year + 3101

    # Kali Ahargana: days elapsed since Kaliyuga start
    kali_ahargana = int(jd - KALI_EPOCH_JD) if jd else 0

    # Rata Die: days elapsed since epoch of the proleptic Gregorian calendar
    rata_die = int(jd - RATA_DIE_OFFSET) if jd else 0

    # Modified Julian Day
    mjd = int(jd - MJD_OFFSET) if jd else 0

    return {
        "kaliyuga_year": kali_year,
        "kaliyuga_year_label": f"{kali_year} Years",
        "kaliyuga_year_label_hindi": f"{kali_year} वर्ष",
        "kali_ahargana": kali_ahargana,
        "kali_ahargana_label": f"{kali_ahargana} Days",
        "kali_ahargana_label_hindi": f"{kali_ahargana} दिन",
        "rata_die": rata_die,
        "rata_die_label": f"{rata_die} Days",
        "rata_die_label_hindi": f"{rata_die} दिन",
        "julian_day": round(jd, 1) if jd else 0,
        "julian_day_label": f"JD {round(jd, 1)}" if jd else "",
        "julian_day_label_hindi": f"जूलियन दिन {round(jd, 1)}" if jd else "",
        "modified_julian_day": mjd,
        "modified_julian_day_label": f"MJD {mjd}" if jd else "",
        "modified_julian_day_label_hindi": f"एमजेडी {mjd}" if jd else "",
        "ayanamsha": round(ayanamsha, 6) if ayanamsha else 0,
        "ayanamsha_label": f"Lahiri {round(ayanamsha, 6)}\u00b0" if ayanamsha else "",
        "ayanamsha_label_hindi": f"लाहिरी {round(ayanamsha, 6)}\u00b0" if ayanamsha else "",
    }


# ============================================================
# PANCHAKA RAHITA MUHURTA (पंचक रहित मुहूर्त)
# ============================================================
# Panchaka occurs when Moon transits through the last 5 nakshatras
# (Dhanishta, Shatabhisha, Purva Bhadrapada, Uttara Bhadrapada, Revati).
# Each of those nakshatras maps to a specific Panchaka type.

PANCHAKA_NAKSHATRAS: Dict[str, tuple[str, str, bool]] = {
    "Dhanishta":          ("Mrityu Panchaka",  "मृत्यु पंचक",  False),   # death risk
    "Shatabhisha":        ("Agni Panchaka",    "अग्नि पंचक",   False),   # fire risk
    "Purva Bhadrapada":   ("Raja Panchaka",    "राज पंचक",      True),    # govt ok
    "Uttara Bhadrapada":  ("Chora Panchaka",   "चोर पंचक",      False),   # theft risk
    "Revati":             ("Roga Panchaka",    "रोग पंचक",      False),   # disease risk
}

# Also allow variant spellings commonly seen in panchang data
_NAKSHATRA_ALIASES: Dict[str, str] = {
    "Dhanista":              "Dhanishta",
    "Satabhisha":            "Shatabhisha",
    "Satabisha":             "Shatabhisha",
    "Poorva Bhadrapada":     "Purva Bhadrapada",
    "Uttara Bhadra":         "Uttara Bhadrapada",
    "Uttarabhadrapada":      "Uttara Bhadrapada",
}


def _resolve_nakshatra(name: str) -> str:
    """Normalise common nakshatra spelling variants."""
    stripped = name.strip()
    return _NAKSHATRA_ALIASES.get(stripped, stripped)


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' to minutes since midnight."""
    parts = t.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to 'HH:MM'."""
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"


def calculate_panchaka_rahita(
    nakshatra_name: str,
    nakshatra_end_time: str,
    sunrise: str,
    sunset: str,
) -> Optional[Dict[str, Any]]:
    """
    Determine whether Panchaka is active and return safe/unsafe windows.

    Returns ``None`` if the nakshatra does not trigger Panchaka.

    When Panchaka *is* active, returns::

        {
            "active": True,
            "type": "Mrityu Panchaka",
            "type_hindi": "मृत्यु पंचक",
            "safe_for_govt": False,
            "unsafe_window": {"start": "06:10", "end": "14:30"},
            "unsafe_window_label": "06:10 – 14:30",
            "unsafe_window_label_hindi": "06:10 – 14:30 (अशुभ)",
            "safe_window": {"start": "14:30", "end": "18:30"},
            "safe_window_label": "14:30 – 18:30",
            "safe_window_label_hindi": "14:30 – 18:30 (शुभ)",
        }
    """
    resolved = _resolve_nakshatra(nakshatra_name)

    if resolved not in PANCHAKA_NAKSHATRAS:
        return None

    type_en, type_hi, safe_for_govt = PANCHAKA_NAKSHATRAS[resolved]

    sr = _time_to_minutes(sunrise)
    ss = _time_to_minutes(sunset)
    end = _time_to_minutes(nakshatra_end_time)

    # Panchaka is active from sunrise until the nakshatra ends.
    # Safe window is from nakshatra end until sunset (if end < sunset).
    if end <= sr:
        # Nakshatra ends before sunrise — no panchaka during the day
        return None

    unsafe_start = max(sr, sr)  # starts at sunrise
    unsafe_end = min(end, ss)   # until nakshatra ends or sunset

    safe_start = unsafe_end
    safe_end = ss

    # If no safe window remains (nakshatra extends past sunset)
    has_safe = safe_start < safe_end

    result: Dict[str, Any] = {
        "active": True,
        "type": type_en,
        "type_hindi": type_hi,
        "safe_for_govt": safe_for_govt,
        "unsafe_window": {
            "start": _minutes_to_time(unsafe_start),
            "end": _minutes_to_time(unsafe_end),
        },
        "unsafe_window_label": (
            f"{_minutes_to_time(unsafe_start)} – {_minutes_to_time(unsafe_end)}"
        ),
        "unsafe_window_label_hindi": (
            f"{_minutes_to_time(unsafe_start)} – {_minutes_to_time(unsafe_end)} (अशुभ)"
        ),
    }

    if has_safe:
        result["safe_window"] = {
            "start": _minutes_to_time(safe_start),
            "end": _minutes_to_time(safe_end),
        }
        result["safe_window_label"] = (
            f"{_minutes_to_time(safe_start)} – {_minutes_to_time(safe_end)}"
        )
        result["safe_window_label_hindi"] = (
            f"{_minutes_to_time(safe_start)} – {_minutes_to_time(safe_end)} (शुभ)"
        )
    else:
        result["safe_window"] = None
        result["safe_window_label"] = "No safe window / कोई शुभ समय नहीं"
        result["safe_window_label_hindi"] = "कोई शुभ समय नहीं"

    return result


# ============================================================
# CHATURMASA (चातुर्मास)
# ============================================================

_CHATURMASA_FULL_MONTHS = {"Shravana", "Bhadrapada", "Ashwin"}


def calculate_chaturmasa(hindu_month: str, tithi_index: int, paksha: str) -> Dict[str, Any]:
    """
    Determine whether the given Hindu date falls within Chaturmasa.

    Chaturmasa runs from Ashadh Shukla Ekadashi (tithi_index 10 in 0-based)
    to Kartik Shukla Ekadashi.
    """
    active = False
    if hindu_month in _CHATURMASA_FULL_MONTHS:
        active = True
    elif hindu_month == "Ashadh":
        if paksha == "Shukla" and tithi_index >= 10:  # Ekadashi onward
            active = True
    elif hindu_month == "Kartik":
        if paksha == "Krishna":
            active = True
        elif paksha == "Shukla" and tithi_index < 10:  # Before Ekadashi
            active = True

    return {
        "active": active,
        "period": "Chaturmasa",
        "period_hindi": "चातुर्मास",
        "warning": "Major ceremonies prohibited during Chaturmasa",
        "warning_hindi": "चातुर्मास में बड़े संस्कार वर्जित हैं",
        "start_month": "Ashadh",
        "end_month": "Kartik",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_misc(
    date_str: str,
    vikram_samvat: int,
    jd: Optional[float] = None,
    ayanamsha: Optional[float] = None,
    nakshatra_name: str = "",
    nakshatra_end_time: str = "",
    sunrise: str = "",
    sunset: str = "",
) -> Dict[str, Any]:
    """
    Aggregate all miscellaneous panchang calculations.

    Returns dict with keys:
      - mantri_mandala  (list of 10 role dicts)
      - astronomical    (epoch data dict)
      - panchaka_rahita (dict or None)
    """
    mantri = calculate_mantri_mandala(vikram_samvat)

    astro = calculate_astronomical_data(date_str, jd=jd, ayanamsha=ayanamsha)

    panchaka: Optional[Dict[str, Any]] = None
    if nakshatra_name and nakshatra_end_time and sunrise and sunset:
        panchaka = calculate_panchaka_rahita(
            nakshatra_name, nakshatra_end_time, sunrise, sunset,
        )

    return {
        "mantri_mandala": mantri,
        "astronomical": astro,
        "panchaka_rahita": panchaka,
    }
