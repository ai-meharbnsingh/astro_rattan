"""
varga_grading_engine.py -- Phaladeepika Adhyaya 3 (Vargadhyaya) Varga-Strength Tiers
====================================================================================

Implements classical varga-strength grading from Phaladeepika Adhyaya 3
(the Vargadhyaya — "Chapter on Varga").

For each of the 7 classical planets (Sun..Saturn), we evaluate its placement
across the Saptavarga (7-varga) scheme:

    D1  (Rasi)         -- birth sign
    D2  (Hora)         -- wealth/sustenance
    D3  (Drekkana)     -- siblings / initiative
    D7  (Saptamsa)     -- progeny
    D9  (Navamsa)      -- spouse / dharma core
    D12 (Dwadasamsa)   -- parents / heritage
    D30 (Trimsamsa)    -- misfortunes / character

A planet is said to "hold" a varga if in that varga it lands in a sign which
is its OWN, EXALTED, MOOLATRIKONA, or FRIENDLY sign (per classical rulership
and natural friendship tables).

The count of varga-holds across Saptavarga maps to classical strength tiers:

    0 holds -> Bhedaka (विभेदक)       -- broken / weak
    1 hold  -> Bhedaka                 -- weak
    2 holds -> Parijatamsa (पारिजातांश) -- modest
    3 holds -> Uttamamsa (उत्तमांश)     -- very good
    4 holds -> Gopuramsa (गोपुरांश)      -- elevated (some schools count 4)
    5 holds -> Gopuramsa                -- elevated
    6 holds -> Simhasanamsa (सिंहासनांश) -- royal
    7 holds -> Parvatamsa (पर्वतांश)     -- mountain-strength

Sloka reference: Phaladeepika Adh. 3, verses 1-8 (Mantreshvara).

This module provides:
    calculate_varga_strength(planet_longitudes) -> dict
    _varga_sign_for(longitude, division) -> (sign_name, sign_index)
    _has_dignity_hold(planet, sign_index) -> bool
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

# ── Constants ───────────────────────────────────────────────────────

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Sign lords (0-indexed sign -> planet)
_SIGN_LORDS: Dict[int, str] = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# Own signs (0-indexed) — BPHS & Phaladeepika
_OWN_SIGNS: Dict[str, set] = {
    "Sun": {4},          # Leo
    "Moon": {3},         # Cancer
    "Mars": {0, 7},      # Aries, Scorpio
    "Mercury": {2, 5},   # Gemini, Virgo
    "Jupiter": {8, 11},  # Sagittarius, Pisces
    "Venus": {1, 6},     # Taurus, Libra
    "Saturn": {9, 10},   # Capricorn, Aquarius
}

# Moolatrikona signs — single sign per planet
_MOOLATRIKONA: Dict[str, int] = {
    "Sun": 4,      # Leo
    "Moon": 1,     # Taurus
    "Mars": 0,     # Aries
    "Mercury": 5,  # Virgo
    "Jupiter": 8,  # Sagittarius
    "Venus": 6,    # Libra
    "Saturn": 10,  # Aquarius
}

# Exaltation signs
_EXALTATION: Dict[str, int] = {
    "Sun": 0,      # Aries
    "Moon": 1,     # Taurus
    "Mars": 9,     # Capricorn
    "Mercury": 5,  # Virgo
    "Jupiter": 3,  # Cancer
    "Venus": 11,   # Pisces
    "Saturn": 6,   # Libra
}

# Natural friendships (BPHS / Phaladeepika)
_NATURAL_FRIENDS: Dict[str, set] = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}

# The 7 vargas that compose the Saptavarga grading set
SAPTAVARGA: Tuple[int, ...] = (1, 2, 3, 7, 9, 12, 30)

SAPTAVARGA_NAMES: Dict[int, str] = {
    1: "Rasi (D1)",
    2: "Hora (D2)",
    3: "Drekkana (D3)",
    7: "Saptamsa (D7)",
    9: "Navamsa (D9)",
    12: "Dwadasamsa (D12)",
    30: "Trimsamsa (D30)",
}

# Classical planets (the 7 for which Phaladeepika grades varga-strength).
# Rahu & Ketu are not classically graded in this system.
CLASSICAL_PLANETS: Tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
)

# Tier definitions: count (holds) -> (name_en, name_hi, description_en, description_hi)
_TIER_BY_COUNT: Dict[int, Dict[str, str]] = {
    0: {
        "name": "Bhedaka",
        "name_hi": "भेदक",
        "description": "Broken / very weak — planet lacks varga support.",
        "description_hi": "अत्यन्त दुर्बल — ग्रह को वर्ग सहयोग प्राप्त नहीं।",
    },
    1: {
        "name": "Bhedaka",
        "name_hi": "भेदक",
        "description": "Weak — only one varga support.",
        "description_hi": "दुर्बल — केवल एक वर्ग में बल।",
    },
    2: {
        "name": "Parijatamsa",
        "name_hi": "पारिजातांश",
        "description": "Modest strength — 2 own vargas.",
        "description_hi": "साधारण बल — 2 स्ववर्गों में।",
    },
    3: {
        "name": "Uttamamsa",
        "name_hi": "उत्तमांश",
        "description": "Very good — 3 own vargas.",
        "description_hi": "उत्तम बल — 3 स्ववर्गों में।",
    },
    4: {
        "name": "Gopuramsa",
        "name_hi": "गोपुरांश",
        "description": "Elevated — 4 own vargas.",
        "description_hi": "उच्च बल — 4 स्ववर्गों में।",
    },
    5: {
        "name": "Gopuramsa",
        "name_hi": "गोपुरांश",
        "description": "High elevation — 5 own vargas (classical threshold).",
        "description_hi": "उच्च बल — 5 स्ववर्गों में (शास्त्रीय सीमा)।",
    },
    6: {
        "name": "Simhasanamsa",
        "name_hi": "सिंहासनांश",
        "description": "Royal strength — 6 own vargas; kingly results.",
        "description_hi": "राजसी बल — 6 स्ववर्गों में; राजोपम फल।",
    },
    7: {
        "name": "Parvatamsa",
        "name_hi": "पर्वतांश",
        "description": "Mountain strength — all 7 Saptavarga own vargas.",
        "description_hi": "पर्वत बल — सम्पूर्ण सप्तवर्गों में।",
    },
}

SLOKA_REF = "Phaladeepika Adh. 3 (Vargadhyaya), verses 1-8"


# ── Varga Sign Computation ──────────────────────────────────────────

def _varga_sign_for(longitude: float, division: int) -> Tuple[str, int]:
    """
    Return (sign_name, sign_index) for a planet at given ecliptic longitude
    in the specified divisional chart.

    Supports exactly the Saptavarga divisions: 1, 2, 3, 7, 9, 12, 30.

    Raises:
        ValueError: for unsupported divisions.
    """
    lon = longitude % 360.0
    base_sign = int(lon // 30.0) % 12
    degree_in_sign = lon - base_sign * 30.0

    if division == 1:
        idx = base_sign

    elif division == 2:
        # Hora: odd sign 0-15 -> Sun (Leo=4), 15-30 -> Moon (Cancer=3)
        #       even sign reversed.
        sign_number = base_sign + 1
        part = 0 if degree_in_sign < 15.0 else 1
        if sign_number % 2 == 1:  # odd
            idx = 4 if part == 0 else 3
        else:  # even
            idx = 3 if part == 0 else 4

    elif division == 3:
        # Drekkana: 0-10 same, 10-20 +4 (5th), 20-30 +8 (9th)
        part = min(int(degree_in_sign / 10.0), 2)
        idx = (base_sign + [0, 4, 8][part]) % 12

    elif division == 7:
        # Saptamsa: odd signs start from self, even signs from 7th (+6).
        part_size = 30.0 / 7.0
        part = min(int(degree_in_sign / part_size), 6)
        sign_number = base_sign + 1
        start = base_sign if (sign_number % 2 == 1) else (base_sign + 6) % 12
        idx = (start + part) % 12

    elif division == 9:
        # Navamsa: Fire->Aries(0), Earth->Cap(9), Air->Libra(6), Water->Cancer(3).
        part_size = 30.0 / 9.0
        part = min(int(degree_in_sign / part_size), 8)
        element = base_sign % 4  # 0=Fire,1=Earth,2=Air,3=Water
        start = {0: 0, 1: 9, 2: 6, 3: 3}[element]
        idx = (start + part) % 12

    elif division == 12:
        # Dwadasamsa: 2.5° each, starting from self.
        part = min(int(degree_in_sign / 2.5), 11)
        idx = (base_sign + part) % 12

    elif division == 30:
        # Trimsamsa: odd sign: 0-5 Mars(0), 5-10 Saturn(10), 10-18 Jupiter(8),
        #                      18-25 Mercury(2), 25-30 Venus(1).
        # Even sign: 0-5 Venus(6), 5-12 Mercury(5), 12-20 Jupiter(11),
        #            20-25 Saturn(9), 25-30 Mars(7).
        sign_number = base_sign + 1
        if sign_number % 2 == 1:  # odd
            if degree_in_sign < 5.0:
                idx = 0       # Mars -> Aries
            elif degree_in_sign < 10.0:
                idx = 10      # Saturn -> Aquarius
            elif degree_in_sign < 18.0:
                idx = 8       # Jupiter -> Sagittarius
            elif degree_in_sign < 25.0:
                idx = 2       # Mercury -> Gemini
            else:
                idx = 1       # Venus -> Taurus
        else:  # even
            if degree_in_sign < 5.0:
                idx = 6       # Venus -> Libra
            elif degree_in_sign < 12.0:
                idx = 5       # Mercury -> Virgo
            elif degree_in_sign < 20.0:
                idx = 11      # Jupiter -> Pisces
            elif degree_in_sign < 25.0:
                idx = 9       # Saturn -> Capricorn
            else:
                idx = 7       # Mars -> Scorpio
    else:
        raise ValueError(
            f"Unsupported Saptavarga division: {division}. "
            f"Supported: {SAPTAVARGA}"
        )

    return _SIGN_NAMES[idx], idx


# ── Dignity Hold Check ──────────────────────────────────────────────

def _has_dignity_hold(planet: str, sign_index: int) -> bool:
    """
    Return True if the planet is in its own / exalted / moolatrikona /
    friendly sign (classical Phaladeepika "varga-hold" criterion).
    """
    if planet not in CLASSICAL_PLANETS:
        return False

    # Own
    if sign_index in _OWN_SIGNS.get(planet, set()):
        return True

    # Moolatrikona
    if _MOOLATRIKONA.get(planet) == sign_index:
        return True

    # Exaltation
    if _EXALTATION.get(planet) == sign_index:
        return True

    # Friendly (natural friendship to sign's lord)
    lord = _SIGN_LORDS.get(sign_index)
    if lord and lord != planet and lord in _NATURAL_FRIENDS.get(planet, set()):
        return True

    return False


def _classify_hold(planet: str, sign_index: int) -> str:
    """
    Classify the varga-hold category for reporting:
    exalted / moolatrikona / own / friendly / none.
    """
    if planet not in CLASSICAL_PLANETS:
        return "none"
    if _EXALTATION.get(planet) == sign_index:
        return "exalted"
    if _MOOLATRIKONA.get(planet) == sign_index:
        return "moolatrikona"
    if sign_index in _OWN_SIGNS.get(planet, set()):
        return "own"
    lord = _SIGN_LORDS.get(sign_index)
    if lord and lord != planet and lord in _NATURAL_FRIENDS.get(planet, set()):
        return "friendly"
    return "none"


# ── Tier Lookup ─────────────────────────────────────────────────────

def _tier_for_count(count: int) -> Dict[str, str]:
    """Return the classical tier definition for a given hold-count (0..7)."""
    if count < 0:
        count = 0
    if count > 7:
        count = 7
    return dict(_TIER_BY_COUNT[count])


# ── Public API ──────────────────────────────────────────────────────

def calculate_varga_strength(
    planet_longitudes: Dict[str, float],
) -> Dict[str, Any]:
    """
    Calculate Phaladeepika Adhyaya 3 Saptavarga-based varga-strength tiers
    for the 7 classical planets.

    Args:
        planet_longitudes: mapping of planet name -> ecliptic longitude (degrees).
            Only keys in CLASSICAL_PLANETS are graded; others are ignored.

    Returns:
        {
          "sloka_ref": "Phaladeepika Adh. 3 ...",
          "scheme": "Saptavarga",
          "vargas": [1, 2, 3, 7, 9, 12, 30],
          "planets": {
            <planet>: {
              "holds": {1: {sign, sign_index, hold, category}, ...},
              "own_vargas": [<division>, ...],
              "count": int,
              "tier": {"name", "name_hi", "description", "description_hi"},
              "sloka_ref": str,
            },
            ...
          },
          "summary": {
            "strongest": [<planet>, ...],
            "weakest": [<planet>, ...],
            "counts": {<planet>: int}
          }
        }
    """
    planets_out: Dict[str, Any] = {}
    counts: Dict[str, int] = {}

    for planet in CLASSICAL_PLANETS:
        if planet not in planet_longitudes:
            continue

        lon = planet_longitudes[planet]
        holds: Dict[int, Dict[str, Any]] = {}
        own_vargas: List[int] = []

        for div in SAPTAVARGA:
            sign_name, sign_index = _varga_sign_for(lon, div)
            held = _has_dignity_hold(planet, sign_index)
            category = _classify_hold(planet, sign_index)
            holds[div] = {
                "varga": SAPTAVARGA_NAMES[div],
                "division": div,
                "sign": sign_name,
                "sign_index": sign_index,
                "hold": held,
                "category": category,
            }
            if held:
                own_vargas.append(div)

        count = len(own_vargas)
        counts[planet] = count
        tier = _tier_for_count(count)

        planets_out[planet] = {
            "holds": holds,
            "own_vargas": own_vargas,
            "count": count,
            "tier": tier,
            "sloka_ref": SLOKA_REF,
        }

    # Summary: strongest/weakest
    if counts:
        max_c = max(counts.values())
        min_c = min(counts.values())
        strongest = sorted([p for p, c in counts.items() if c == max_c])
        weakest = sorted([p for p, c in counts.items() if c == min_c])
    else:
        strongest = []
        weakest = []

    return {
        "sloka_ref": SLOKA_REF,
        "scheme": "Saptavarga",
        "vargas": list(SAPTAVARGA),
        "varga_names": dict(SAPTAVARGA_NAMES),
        "planets": planets_out,
        "summary": {
            "strongest": strongest,
            "weakest": weakest,
            "counts": counts,
        },
    }
