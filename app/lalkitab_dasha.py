"""
lalkitab_dasha.py — Lal Kitab Saala Grah & 35-Year Dasha System
================================================================
Reference: Lal Kitab 1952 (Pandit Roop Chand Joshi)

The Saala Grah (Year Ruler) determines which planet governs each year of life.
The sequence cycles every 9 years: Sun→Moon→Jupiter→Rahu→Saturn→Mercury→Ketu→Venus→Mars
"""
from __future__ import annotations

from datetime import date as _date
from typing import Any, Dict, List


# ── Planet sequence (0-indexed) ───────────────────────────────────────────────
_PLANET_SEQUENCE: List[str] = [
    "Sun",      # index 0  — year 1, 10, 19, …
    "Moon",     # index 1  — year 2, 11, 20, …
    "Jupiter",  # index 2  — year 3, 12, 21, …
    "Rahu",     # index 3  — year 4, 13, 22, …
    "Saturn",   # index 4  — year 5, 14, 23, …
    "Mercury",  # index 5  — year 6, 15, 24, …
    "Ketu",     # index 6  — year 7, 16, 25, …
    "Venus",    # index 7  — year 8, 17, 26, …
    "Mars",     # index 8  — year 9, 18, 27, …
]

# ── Hindi planet names (Devanagari) ───────────────────────────────────────────
_PLANET_HI: Dict[str, str] = {
    "Sun":      "सूर्य",
    "Moon":     "चन्द्र",
    "Jupiter":  "गुरु",
    "Rahu":     "राहु",
    "Saturn":   "शनि",
    "Mercury":  "बुध",
    "Ketu":     "केतु",
    "Venus":    "शुक्र",
    "Mars":     "मंगल",
}

# ── English descriptions for each planet's Saala Grah year ───────────────────
_EN_DESC: Dict[str, str] = {
    "Sun": (
        "Year of authority, government, and father's health. "
        "Your confidence is high but avoid ego conflicts. "
        "Seek recognition through honest effort."
    ),
    "Moon": (
        "Year of emotions, mother's health, property matters, and mental fluctuations. "
        "Domestic life comes into focus. Guard against mood swings."
    ),
    "Jupiter": (
        "Year of wisdom, children, religion, and education. "
        "Most auspicious year in the cycle — seek blessings, expand knowledge, "
        "and invest in long-term growth."
    ),
    "Rahu": (
        "Year of confusion, foreign connections, sudden changes, and illusions. "
        "Be wary of deception. Unexpected events shake the routine."
    ),
    "Saturn": (
        "Year of hard work, discipline, service, and obstacles that teach lessons. "
        "Avoid shortcuts. Karmic debts surface and must be settled honestly."
    ),
    "Mercury": (
        "Year of trade, communication, skill, and business acumen. "
        "Favorable for writing, education, and commerce. Keep agreements in writing."
    ),
    "Ketu": (
        "Year of spirituality, research, isolation, and past karma surfacing. "
        "Inner work is more productive than outer ambition. Pilgrimages are auspicious."
    ),
    "Venus": (
        "Year of luxury, marriage, beauty, creative arts, and relationships. "
        "Enjoyment and partnership take centre stage. Avoid extravagance."
    ),
    "Mars": (
        "Year of energy, property, siblings, courage, and conflicts. "
        "Take initiative but avoid aggression. Property dealings and land matters are active."
    ),
}

# ── Hindi descriptions (Devanagari) ──────────────────────────────────────────
_HI_DESC: Dict[str, str] = {
    "Sun": (
        "सत्ता, सरकार और पिता के स्वास्थ्य का वर्ष। "
        "आत्मविश्वास ऊँचा रहता है परन्तु अहंकार से बचें। "
        "ईमानदार प्रयास से पहचान प्राप्त करें।"
    ),
    "Moon": (
        "भावनाओं, माता के स्वास्थ्य, संपत्ति और मानसिक उतार-चढ़ाव का वर्ष। "
        "घर-परिवार पर ध्यान केंद्रित रहता है। मन की चंचलता को नियंत्रित करें।"
    ),
    "Jupiter": (
        "ज्ञान, संतान, धर्म और शिक्षा का वर्ष। "
        "नौ वर्षों के चक्र में सबसे शुभ वर्ष — आशीर्वाद लें, ज्ञान बढ़ाएँ "
        "और दीर्घकालिक विकास में निवेश करें।"
    ),
    "Rahu": (
        "भ्रम, विदेशी संबंध, अचानक परिवर्तन और भ्रांतियों का वर्ष। "
        "धोखे से सावधान रहें। अप्रत्याशित घटनाएँ दिनचर्या बाधित कर सकती हैं।"
    ),
    "Saturn": (
        "परिश्रम, अनुशासन, सेवा और बाधाओं से सबक सीखने का वर्ष। "
        "शॉर्टकट से बचें। कर्मिक ऋण सामने आते हैं और उन्हें ईमानदारी से चुकाना होता है।"
    ),
    "Mercury": (
        "व्यापार, संचार, कुशलता और व्यावसायिक बुद्धि का वर्ष। "
        "लेखन, शिक्षा और वाणिज्य के लिए अनुकूल। समझौते लिखित में करें।"
    ),
    "Ketu": (
        "आध्यात्मिकता, शोध, एकांत और पिछले कर्म उभरने का वर्ष। "
        "बाहरी महत्वाकांक्षा से ज़्यादा आंतरिक कार्य फलदायी होता है। तीर्थयात्रा शुभ है।"
    ),
    "Venus": (
        "विलासिता, विवाह, सौंदर्य, सृजनात्मक कला और रिश्तों का वर्ष। "
        "आनंद और साझेदारी केंद्र में आती है। फिजूलखर्ची से बचें।"
    ),
    "Mars": (
        "ऊर्जा, संपत्ति, भाई-बहन, साहस और संघर्षों का वर्ष। "
        "पहल करें लेकिन आक्रामकता से बचें। संपत्ति और भूमि के मामले सक्रिय रहते हैं।"
    ),
}


# ── Core helper ───────────────────────────────────────────────────────────────

def _planet_at_age(age: int) -> str:
    """Return the Saala Grah planet name for a given age (1-based)."""
    idx = (age - 1) % 9
    return _PLANET_SEQUENCE[idx]


def _calc_age(birth_date_str: str, current_date_str: str) -> int:
    """Return completed years of age (integer floor)."""
    bd = _date.fromisoformat(birth_date_str)
    cd = _date.fromisoformat(current_date_str)
    age = cd.year - bd.year
    if (cd.month, cd.day) < (bd.month, bd.day):
        age -= 1
    return age


# ── Public API ────────────────────────────────────────────────────────────────

def get_saala_grah(current_age: int) -> Dict[str, Any]:
    """
    Get the ruling planet (Saala Grah) for a given age.

    Args:
        current_age: completed years of life (integer, >= 1)

    Returns:
        dict with keys:
            planet           — English planet name
            planet_hi        — Devanagari planet name
            sequence_position — 1-based position in the 9-planet cycle (1–9)
            cycle_year       — same as sequence_position (alias for clarity)
            en_desc          — English description of this Saala Grah year
            hi_desc          — Hindi description of this Saala Grah year
    """
    planet = _planet_at_age(current_age)
    seq_pos = ((current_age - 1) % 9) + 1  # 1-based (1–9)
    return {
        "planet": planet,
        "planet_hi": _PLANET_HI[planet],
        "sequence_position": seq_pos,
        "cycle_year": seq_pos,
        "en_desc": _EN_DESC[planet],
        "hi_desc": _HI_DESC[planet],
    }


def get_dasha_timeline(birth_date: str, current_date: str) -> Dict[str, Any]:
    """
    Get the complete Lal Kitab Saala Grah Dasha timeline.

    Args:
        birth_date:   "YYYY-MM-DD"
        current_date: "YYYY-MM-DD"

    Returns:
        {
            current_age:       int,
            current_saala_grah: {planet, planet_hi, age, started_year,
                                  ends_year, en_desc, hi_desc},
            next_saala_grah:   {planet, planet_hi, starts_at_age, starts_year},
            life_phase:        {phase, years_in_phase, phase_end_age},
            upcoming_periods:  [{age, year, planet, planet_hi}, ...]  # 5 entries
            past_periods:      [{age, year, planet, planet_hi}, ...]  # 3 entries
        }
    """
    bd = _date.fromisoformat(birth_date)
    age = _calc_age(birth_date, current_date)
    cd = _date.fromisoformat(current_date)

    # ── Current Saala Grah ───────────────────────────────────────────────────
    csg_data = get_saala_grah(age)
    # The current year ruler started at the beginning of the current age year
    # (birthday to next birthday).
    started_year = bd.year + age          # calendar year when this age started
    ends_year = started_year + 1          # next birthday year ends this ruler

    current_saala_grah = {
        "planet": csg_data["planet"],
        "planet_hi": csg_data["planet_hi"],
        "age": age,
        "started_year": started_year,
        "ends_year": ends_year,
        "en_desc": csg_data["en_desc"],
        "hi_desc": csg_data["hi_desc"],
    }

    # ── Next Saala Grah ──────────────────────────────────────────────────────
    next_age = age + 1
    nsg_data = get_saala_grah(next_age)
    next_saala_grah = {
        "planet": nsg_data["planet"],
        "planet_hi": nsg_data["planet_hi"],
        "starts_at_age": next_age,
        "starts_year": ends_year,
    }

    # ── Life Phase ───────────────────────────────────────────────────────────
    # Phase 1: birth → 35, Phase 2: 36 → 70, Phase 3: 71+
    if age <= 35:
        phase = 1
        years_in_phase = age
        phase_end_age = 35
    elif age <= 70:
        phase = 2
        years_in_phase = age - 35
        phase_end_age = 70
    else:
        phase = 3
        years_in_phase = age - 70
        phase_end_age = 105

    life_phase = {
        "phase": phase,
        "years_in_phase": years_in_phase,
        "phase_end_age": phase_end_age,
    }

    # ── Upcoming periods (next 5 years) ──────────────────────────────────────
    upcoming_periods: List[Dict[str, Any]] = []
    for offset in range(1, 6):
        a = age + offset
        planet = _planet_at_age(a)
        upcoming_periods.append({
            "age": a,
            "year": bd.year + a,
            "planet": planet,
            "planet_hi": _PLANET_HI[planet],
        })

    # ── Past periods (last 3 years) ───────────────────────────────────────────
    past_periods: List[Dict[str, Any]] = []
    for offset in range(3, 0, -1):
        a = age - offset
        if a < 1:
            continue
        planet = _planet_at_age(a)
        past_periods.append({
            "age": a,
            "year": bd.year + a,
            "planet": planet,
            "planet_hi": _PLANET_HI[planet],
        })

    return {
        "current_age": age,
        "current_saala_grah": current_saala_grah,
        "next_saala_grah": next_saala_grah,
        "life_phase": life_phase,
        "upcoming_periods": upcoming_periods,
        "past_periods": past_periods,
    }
