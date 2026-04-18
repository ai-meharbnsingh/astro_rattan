"""
panchadha_maitri_engine.py — Panchadha Maitri (5-fold Planetary Friendship)
============================================================================
Implements Phaladeepika Adhyaya 2.

Combines:
  1. Naisargika Maitri  — permanent/natural friendship (fixed classical table)
  2. Tatkalika Maitri   — temporary friendship based on chart positions

Combined Panchadha results:
  Natural Friend  + Temporary Friend  → Adhimitra  (Great Friend)
  Natural Friend  + Temporary Enemy   → Sama        (Neutral/Equal)
  Natural Neutral + Temporary Friend  → Mitra       (Friend)
  Natural Neutral + Temporary Enemy   → Shatru      (Enemy)
  Natural Enemy   + Temporary Friend  → Sama        (Neutral/Equal)
  Natural Enemy   + Temporary Enemy   → Adhishatru  (Great Enemy)

Only the 7 classical planets are analysed: Sun Moon Mars Mercury Jupiter Venus Saturn.
Rahu/Ketu have no classical natural friendships and are skipped.
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Classical planets only
# ---------------------------------------------------------------------------
CLASSICAL_PLANETS: List[str] = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# ---------------------------------------------------------------------------
# Naisargika Maitri — Phaladeepika Adh. 2
# Values: "Friend", "Neutral", "Enemy"
# ---------------------------------------------------------------------------
_NATURAL: Dict[str, Dict[str, str]] = {
    "Sun":     {"Moon": "Friend",  "Mars": "Friend",  "Jupiter": "Friend",
                "Mercury": "Neutral",
                "Venus": "Enemy",  "Saturn": "Enemy"},
    "Moon":    {"Sun": "Friend",   "Mercury": "Friend",
                "Mars": "Neutral", "Jupiter": "Neutral", "Venus": "Neutral", "Saturn": "Neutral"},
    "Mars":    {"Sun": "Friend",   "Moon": "Friend",   "Jupiter": "Friend",
                "Venus": "Neutral", "Saturn": "Neutral",
                "Mercury": "Enemy"},
    "Mercury": {"Sun": "Friend",   "Venus": "Friend",
                "Mars": "Neutral", "Jupiter": "Neutral", "Saturn": "Neutral",
                "Moon": "Enemy"},
    "Jupiter": {"Sun": "Friend",   "Moon": "Friend",   "Mars": "Friend",
                "Saturn": "Neutral",
                "Mercury": "Enemy", "Venus": "Enemy"},
    "Venus":   {"Mercury": "Friend", "Saturn": "Friend",
                "Mars": "Neutral",   "Jupiter": "Neutral",
                "Sun": "Enemy",      "Moon": "Enemy"},
    "Saturn":  {"Mercury": "Friend", "Venus": "Friend",
                "Jupiter": "Neutral",
                "Sun": "Enemy",  "Moon": "Enemy",  "Mars": "Enemy"},
}


def _natural_relation(planet_a: str, planet_b: str) -> str:
    """Return natural relation of planet_b from planet_a's perspective."""
    return _NATURAL.get(planet_a, {}).get(planet_b, "Neutral")


# ---------------------------------------------------------------------------
# Tatkalika Maitri — temporary friendship via house distance
# ---------------------------------------------------------------------------
# B is temporary Friend of A when B occupies house 2,3,4,10,11,12 from A
_TEMP_FRIEND_HOUSES: set = {2, 3, 4, 10, 11, 12}


def _house_distance(house_a: int, house_b: int) -> int:
    """
    Count from house_a to house_b going forward (1-indexed, 1–12).
    house_a itself = 1, next house = 2, etc.
    Returns value in range 1–12.
    """
    dist = (house_b - house_a) % 12
    return dist if dist != 0 else 12


def _tatkalika_relation(house_a: int, house_b: int) -> str:
    """
    Return temporary relation of planet_b from planet_a's perspective.
    'Friend' if B is in houses 2,3,4,10,11,12 from A, else 'Enemy'.
    """
    dist = _house_distance(house_a, house_b)
    return "Friend" if dist in _TEMP_FRIEND_HOUSES else "Enemy"


# ---------------------------------------------------------------------------
# Panchadha combination table
# ---------------------------------------------------------------------------
_PANCHADHA: Dict[Tuple[str, str], Tuple[str, str]] = {
    ("Friend",  "Friend"): ("Adhimitra",  "अधिमित्र"),
    ("Friend",  "Enemy"):  ("Sama",       "सम"),
    ("Neutral", "Friend"): ("Mitra",      "मित्र"),
    ("Neutral", "Enemy"):  ("Shatru",     "शत्रु"),
    ("Enemy",   "Friend"): ("Sama",       "सम"),
    ("Enemy",   "Enemy"):  ("Adhishatru", "अधिशत्रु"),
}


def _panchadha(natural: str, temporary: str) -> Tuple[str, str]:
    """Return (panchadha_en, panchadha_hi) for a given natural+temporary pair."""
    return _PANCHADHA[(natural, temporary)]


# ---------------------------------------------------------------------------
# Per-pair classical context (planet-specific flavour text)
# ---------------------------------------------------------------------------
_PAIR_CONTEXT: Dict[frozenset, str] = {
    frozenset({"Sun", "Moon"}):    "vitality and mind",
    frozenset({"Sun", "Mars"}):    "authority and courage",
    frozenset({"Sun", "Mercury"}): "intellect and self-expression",
    frozenset({"Sun", "Jupiter"}): "soul purpose and wisdom",
    frozenset({"Sun", "Venus"}):   "ego and desire/luxury",
    frozenset({"Sun", "Saturn"}):  "authority and discipline/karma",
    frozenset({"Moon", "Mars"}):   "emotions and drive/aggression",
    frozenset({"Moon", "Mercury"}): "mind and communication",
    frozenset({"Moon", "Jupiter"}): "intuition and higher knowledge",
    frozenset({"Moon", "Venus"}):  "feelings and aesthetic pleasures",
    frozenset({"Moon", "Saturn"}): "emotions and restriction/endurance",
    frozenset({"Mars", "Mercury"}): "action and analytical thinking",
    frozenset({"Mars", "Jupiter"}): "energy and righteousness",
    frozenset({"Mars", "Venus"}):  "passion and sensuality",
    frozenset({"Mars", "Saturn"}): "drive and obstruction/perseverance",
    frozenset({"Mercury", "Jupiter"}): "intellect and philosophy",
    frozenset({"Mercury", "Venus"}):   "communication and artistic flair",
    frozenset({"Mercury", "Saturn"}):  "analysis and discipline",
    frozenset({"Jupiter", "Venus"}):   "dharma/expansion and pleasure/wealth",
    frozenset({"Jupiter", "Saturn"}):  "wisdom and karmic limitation",
    frozenset({"Venus", "Saturn"}):    "desire and renunciation/delay",
}

# Deeper interpretation per relation type for specific pairs
_ADHISHATRU_CONTEXT: Dict[frozenset, str] = {
    frozenset({"Sun", "Saturn"}):  "authority clashes with discipline; career advancement may involve conflict with authority figures or the native's own self-discipline",
    frozenset({"Sun", "Venus"}):   "ego and desire are at odds; over-indulgence or neglect of relationships possible",
    frozenset({"Moon", "Mercury"}): "emotional reactions can override rational analysis, or vice versa",
    frozenset({"Jupiter", "Mercury"}): "optimistic expansion conflicts with analytical precision; over-thinking vs over-reaching",
    frozenset({"Jupiter", "Venus"}): "moral/spiritual values clash with material pleasure-seeking; tension between dharma and bhoga",
    frozenset({"Mars", "Mercury"}): "impulsive action vs careful reasoning; decisions may be rushed or incoherently timed",
    frozenset({"Moon", "Saturn"}): "emotional warmth suppressed by restriction; potential for melancholy or delayed happiness",
}

_ADHIMITRA_CONTEXT: Dict[frozenset, str] = {
    frozenset({"Sun", "Moon"}):    "mind and vitality are perfectly aligned; robust health and emotional clarity",
    frozenset({"Sun", "Mars"}):    "leadership and courage reinforce each other; bold decisive action",
    frozenset({"Sun", "Jupiter"}): "soul purpose and wisdom work in unison; strong moral compass and fortunate outcomes",
    frozenset({"Moon", "Jupiter"}): "emotional intelligence amplified by higher wisdom; naturally nurturing and spiritually inclined",
    frozenset({"Mars", "Jupiter"}): "righteous action and energetic drive combined; excellent for achievement with ethics",
    frozenset({"Mercury", "Venus"}): "communication and aesthetic sense complement each other; talent in arts, language, and diplomacy",
    frozenset({"Mercury", "Saturn"}): "analytical thinking sharpened by patience; excellent for research, law, and strategy",
    frozenset({"Venus", "Saturn"}):  "disciplined enjoyment; ability to build lasting relationships or material wealth through sustained effort",
}


def _build_effect(
    planet_a: str,
    planet_b: str,
    panchadha: str,
    natural_a: str,
    natural_b: str,
    temp_a: str,
    temp_b: str,
) -> Tuple[str, str]:
    """Build English and Hindi effect strings for the pair."""
    pair_key = frozenset({planet_a, planet_b})
    context = _PAIR_CONTEXT.get(pair_key, "their respective significations")

    # Base template per relationship
    if panchadha == "Adhimitra":
        extra = _ADHIMITRA_CONTEXT.get(pair_key, "")
        base_en = (
            f"{planet_a} and {planet_b} are great friends (Adhimitra) — "
            f"they powerfully support each other's significations ({context})."
        )
        if extra:
            base_en += f" Classically: {extra}."
        base_hi = (
            f"{planet_a} और {planet_b} अधिमित्र हैं — "
            f"ये एक-दूसरे के कारकत्व ({context}) का अधिकतम समर्थन करते हैं।"
        )

    elif panchadha == "Mitra":
        base_en = (
            f"{planet_a} and {planet_b} are friends (Mitra) — "
            f"good cooperation between {context}; generally helpful to each other."
        )
        base_hi = (
            f"{planet_a} और {planet_b} मित्र हैं — "
            f"{context} के क्षेत्र में सहयोग; सामान्यतः एक-दूसरे के लिए लाभकारी।"
        )

    elif panchadha == "Sama":
        base_en = (
            f"{planet_a} and {planet_b} maintain a neutral/equal (Sama) relationship — "
            f"mixed results between {context}; neither strong support nor clear opposition."
        )
        if natural_a == "Friend":
            base_en += f" {planet_a} naturally favours {planet_b} but temporary position creates friction."
        else:
            base_en += f" {planet_b} naturally favours {planet_a} but temporary position creates friction."
        base_hi = (
            f"{planet_a} और {planet_b} सम संबंध में हैं — "
            f"{context} में मिले-जुले परिणाम; न पूर्ण सहयोग, न स्पष्ट विरोध।"
        )

    elif panchadha == "Shatru":
        base_en = (
            f"{planet_a} and {planet_b} are in conflict (Shatru) — "
            f"tension between {context}; their significations work against each other in this chart."
        )
        base_hi = (
            f"{planet_a} और {planet_b} शत्रु संबंध में हैं — "
            f"{context} के बीच तनाव; इस कुंडली में इनके कारकत्व परस्पर बाधक हैं।"
        )

    else:  # Adhishatru
        extra = _ADHISHATRU_CONTEXT.get(pair_key, "")
        base_en = (
            f"{planet_a} and {planet_b} are great enemies (Adhishatru) — "
            f"strong opposition between {context}; their significations work powerfully against each other."
        )
        if extra:
            base_en += f" Classically: {extra}."
        base_hi = (
            f"{planet_a} और {planet_b} अधिशत्रु हैं — "
            f"{context} के मध्य प्रबल विरोध; इनके कारकत्व इस कुंडली में एक-दूसरे के विपरीत कार्य करते हैं।"
        )

    return base_en, base_hi


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_panchadha_maitri(chart_data: dict) -> dict:
    """
    Compute 5-fold planetary friendship matrix for a natal chart.
    Phaladeepika Adh. 2.

    chart_data must contain:
      chart_data["planets"] = {
          "Sun":     {"house": <1-12>, ...},
          "Moon":    {"house": <1-12>, ...},
          ... (all 7 classical planets)
      }

    Returns:
    {
        "planet_pairs": [
            {
                "planet_a": str,
                "planet_b": str,
                "natural_relation": str,      # Friend / Neutral / Enemy (A→B)
                "temporary_relation": str,    # Friend / Enemy (A→B)
                "natural_relation_b_to_a": str,
                "temporary_relation_b_to_a": str,
                "panchadha_relation": str,    # Adhimitra / Mitra / Sama / Shatru / Adhishatru
                "panchadha_relation_hi": str,
                "effect_en": str,
                "effect_hi": str,
                "house_distance_a_to_b": int,
                "house_distance_b_to_a": int,
                "sloka_ref": str
            },
            ...  # 21 pairs total
        ],
        "strongest_ally_pairs": [...],  # Adhimitra pairs
        "conflict_pairs":       [...],  # Adhishatru pairs
        "summary_en": str,
        "summary_hi": str,
        "sloka_ref": str
    }
    """
    planets_data: Dict[str, Any] = chart_data.get("planets", {})

    # Build house map; default to 1 if missing
    house_map: Dict[str, int] = {}
    for planet in CLASSICAL_PLANETS:
        p_info = planets_data.get(planet, {})
        house_map[planet] = int(p_info.get("house", 1))

    planet_pairs: List[Dict[str, Any]] = []

    for planet_a, planet_b in combinations(CLASSICAL_PLANETS, 2):
        house_a = house_map[planet_a]
        house_b = house_map[planet_b]

        # Natural relations (asymmetric lookup)
        nat_a_to_b = _natural_relation(planet_a, planet_b)
        nat_b_to_a = _natural_relation(planet_b, planet_a)

        # Temporary relations (position-based, asymmetric)
        temp_a_to_b = _tatkalika_relation(house_a, house_b)
        temp_b_to_a = _tatkalika_relation(house_b, house_a)

        # Panchadha from A's perspective (A→B is authoritative for this pair)
        panchadha_en, panchadha_hi = _panchadha(nat_a_to_b, temp_a_to_b)

        # House distances
        dist_a_to_b = _house_distance(house_a, house_b)
        dist_b_to_a = _house_distance(house_b, house_a)

        # Effect text
        effect_en, effect_hi = _build_effect(
            planet_a, planet_b,
            panchadha_en,
            nat_a_to_b, nat_b_to_a,
            temp_a_to_b, temp_b_to_a,
        )

        planet_pairs.append({
            "planet_a": planet_a,
            "planet_b": planet_b,
            "natural_relation": nat_a_to_b,
            "natural_relation_b_to_a": nat_b_to_a,
            "temporary_relation": temp_a_to_b,
            "temporary_relation_b_to_a": temp_b_to_a,
            "panchadha_relation": panchadha_en,
            "panchadha_relation_hi": panchadha_hi,
            "effect_en": effect_en,
            "effect_hi": effect_hi,
            "house_distance_a_to_b": dist_a_to_b,
            "house_distance_b_to_a": dist_b_to_a,
            "sloka_ref": "Phaladeepika Adh. 2",
        })

    # Derived lists
    strongest_ally_pairs = [p for p in planet_pairs if p["panchadha_relation"] == "Adhimitra"]
    conflict_pairs       = [p for p in planet_pairs if p["panchadha_relation"] == "Adhishatru"]

    # Counts for summary
    counts: Dict[str, int] = {
        "Adhimitra": 0, "Mitra": 0, "Sama": 0, "Shatru": 0, "Adhishatru": 0
    }
    for p in planet_pairs:
        counts[p["panchadha_relation"]] += 1

    # Build summary strings
    ally_names  = ", ".join(f"{p['planet_a']}-{p['planet_b']}" for p in strongest_ally_pairs) or "none"
    enemy_names = ", ".join(f"{p['planet_a']}-{p['planet_b']}" for p in conflict_pairs) or "none"

    summary_en = (
        f"Panchadha Maitri (Phaladeepika Adh. 2): "
        f"{counts['Adhimitra']} Adhimitra, {counts['Mitra']} Mitra, "
        f"{counts['Sama']} Sama, {counts['Shatru']} Shatru, {counts['Adhishatru']} Adhishatru pairs. "
        f"Great Friends (Adhimitra): {ally_names}. "
        f"Great Enemies (Adhishatru): {enemy_names}."
    )
    summary_hi = (
        f"पञ्चधा मैत्री (फलदीपिका अध्याय 2): "
        f"{counts['Adhimitra']} अधिमित्र, {counts['Mitra']} मित्र, "
        f"{counts['Sama']} सम, {counts['Shatru']} शत्रु, {counts['Adhishatru']} अधिशत्रु युग्म। "
        f"अधिमित्र युग्म: {ally_names}। "
        f"अधिशत्रु युग्म: {enemy_names}।"
    )

    return {
        "planet_pairs": planet_pairs,
        "strongest_ally_pairs": strongest_ally_pairs,
        "conflict_pairs": conflict_pairs,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 2",
    }
