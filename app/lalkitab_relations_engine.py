"""
Lal Kitab Relations Engine (backend)

Purpose:
- Compute conjunctions (yuti), aspects (drishti), and clashes/friendships
  based on Lal Kitab style planet relationships.
- This replaces the previous frontend-only computation that depended on
  hardcoded constants in `lalkitab-data.ts`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


PLANET_FRIENDS: Dict[str, List[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus", "Rahu"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn", "Rahu"],
    "Saturn": ["Venus", "Mercury", "Rahu"],
    "Rahu": ["Mercury", "Venus", "Saturn"],
    "Ketu": ["Jupiter", "Mars"],
}

PLANET_ENEMIES: Dict[str, List[str]] = {
    "Sun": ["Saturn", "Venus", "Rahu", "Ketu"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Mercury", "Rahu"],
    "Mercury": ["Moon", "Ketu"],
    "Jupiter": ["Venus", "Rahu"],
    "Venus": ["Sun", "Moon", "Ketu"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars", "Jupiter"],
    "Ketu": ["Mercury", "Venus", "Saturn"],
}

# Lal Kitab special aspects (additional aspects beyond the universal 7th).
# Format: offsets from the planet's house.
SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8],
    "Jupiter": [5, 9],
    "Saturn": [3, 10],
    "Rahu": [5, 9],
}


def _norm_house(h: int) -> int:
    return ((int(h) - 1) % 12) + 1


def are_friends(p1: str, p2: str) -> bool:
    return p2 in PLANET_FRIENDS.get(p1, [])


def are_enemies(p1: str, p2: str) -> bool:
    return p2 in PLANET_ENEMIES.get(p1, [])


def build_relations(planet_positions: Dict[str, int]) -> Dict[str, Any]:
    """
    planet_positions: {"Sun": 1..12, ...}

    Returns:
      {
        "conjunctions": [
          { "house": N, "planets": [...], "clashes": [[p1,p2],...], "friendships": [[p1,p2],...] }
        ],
        "aspects": [
          { "planet": "Mars", "from_house": 3, "aspect_houses": [7, 6, 10] }
        ],
      }
    """
    # Conjunctions (yuti): planets sharing the same house
    house_map: Dict[int, List[str]] = {}
    for planet, house in planet_positions.items():
        if not house:
            continue
        h = int(house)
        if h < 1 or h > 12:
            continue
        house_map.setdefault(h, []).append(planet)

    conjunctions: List[Dict[str, Any]] = []
    for house, planets in sorted(house_map.items()):
        if len(planets) < 2:
            continue
        clashes: List[Tuple[str, str]] = []
        friendships: List[Tuple[str, str]] = []
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                p1, p2 = planets[i], planets[j]
                if are_enemies(p1, p2) or are_enemies(p2, p1):
                    clashes.append((p1, p2))
                elif are_friends(p1, p2) or are_friends(p2, p1):
                    friendships.append((p1, p2))
        conjunctions.append(
            {
                "house": house,
                "planets": planets,
                "clashes": [list(x) for x in clashes],
                "friendships": [list(x) for x in friendships],
            }
        )

    # Aspects (drishti)
    aspects: List[Dict[str, Any]] = []
    for planet, from_house in planet_positions.items():
        if not from_house:
            continue
        fh = int(from_house)
        if fh < 1 or fh > 12:
            continue
        aspect_houses: List[int] = []
        # Universal 7th aspect
        aspect_houses.append(_norm_house(fh + 6))
        # Special aspects
        for off in SPECIAL_ASPECTS.get(planet, []):
            aspect_houses.append(_norm_house(fh + (off - 1)))
        # Unique + stable
        uniq = []
        seen = set()
        for h in aspect_houses:
            if h in seen:
                continue
            seen.add(h)
            uniq.append(h)
        aspects.append({"planet": planet, "from_house": fh, "aspect_houses": uniq})

    return {"conjunctions": conjunctions, "aspects": aspects}

