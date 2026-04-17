"""
Lal Kitab Rules Engine (backend)

Purpose:
- Provide rule-driven structures used by the UI without relying on
  frontend hardcoded/mock datasets.

Currently served:
- Mirror house axis occupancy (1↔7, 2↔8, ...).
- Cross-house rule triggers (generic; text lives in frontend i18n).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


MIRROR_HOUSES: Tuple[Tuple[int, int], ...] = (
    (1, 7),
    (2, 8),
    (3, 9),
    (4, 10),
    (5, 11),
    (6, 12),
)

# Cross-house rules used by the UI (generic). Text is rendered via i18n keys.
CROSS_RULES: Tuple[Tuple[int, int], ...] = (
    (1, 7),
    (4, 10),
    (5, 9),
    (2, 8),
    (3, 9),
    (6, 12),
    (7, 1),
    (10, 4),
)


def build_rules(planet_positions: Dict[str, int]) -> Dict[str, Any]:
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for p, h in planet_positions.items():
        if not h:
            continue
        hn = int(h)
        if 1 <= hn <= 12:
            house_planets[hn].append(p)

    mirror_axis = []
    for h1, h2 in MIRROR_HOUSES:
        p1 = house_planets.get(h1, [])
        p2 = house_planets.get(h2, [])
        mirror_axis.append(
            {
                "h1": h1,
                "h2": h2,
                "planets_h1": p1,
                "planets_h2": p2,
                "has_mutual": bool(p1 and p2),
            }
        )

    cross_effects = []
    for idx, (from_h, to_h) in enumerate(CROSS_RULES, start=1):
        pf = house_planets.get(from_h, [])
        cross_effects.append(
            {
                "idx": idx,
                "from_house": from_h,
                "to_house": to_h,
                "trigger_planets": pf,
                "has_trigger": bool(pf),
            }
        )

    return {"mirror_axis": mirror_axis, "cross_effects": cross_effects}

