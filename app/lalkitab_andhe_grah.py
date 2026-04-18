"""
app/lalkitab_andhe_grah.py

Andhe Grah (अंधे ग्रह) — Blind Planet detection.

Source: Lal Kitab 1952 (Pt. Roop Chand Joshi), chapters 2.12 and 4.14.

Concept
-------
A "blind planet" has lost its functional drishti (sight) in the chart
and therefore cannot deliver its own significations reliably. In LK
1952, a remedy performed for a blind planet, or for a planet CLOSE to
a blind planet, can backfire — the blind planet intercepts the remedy
energy and redirects it into the life-area it was failing to guard.

Detection criteria (any ONE makes the planet Andhe):

  1. Part of an ANDHA TEVA enemy pair in the 10th house
     (Sun+Saturn, Moon+Rahu, Mars+Mercury, Jupiter+Venus, etc.)
  2. In H12 (house of hidden losses) with an enemy planet
  3. Retrograde AND combust simultaneously — both senses impaired
  4. In its own debilitation sign AND in a dusthana house (6/8/12)
  5. Surrounded on both sides (adjacent houses H±1) by enemies —
     "Papakartari" blind-spot rule

LK 4.14 mandates: whenever a remedy targets a blind planet OR a
planet adjacent to a blind planet, the user MUST be warned BEFORE
the remedy is shown — not after.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


# Enemy pairs that create Andha Teva when both in H10 (source: LK 2.12).
_ANDHA_ENEMY_PAIRS = [
    {"Sun", "Saturn"},
    {"Sun", "Venus"},
    {"Moon", "Rahu"},
    {"Moon", "Ketu"},
    {"Mars", "Mercury"},
    {"Mars", "Rahu"},
    {"Jupiter", "Mercury"},
    {"Jupiter", "Venus"},
    {"Saturn", "Moon"},
]

# Mirror of lalkitab_advanced.LK_ENEMIES — kept local to avoid cycle
_LK_ENEMIES_LOCAL = {
    "Sun":     {"Saturn", "Rahu", "Ketu"},
    "Moon":    {"Rahu", "Ketu"},
    "Mars":    {"Mercury", "Ketu"},
    "Mercury": {"Moon", "Ketu"},
    "Jupiter": {"Mercury", "Venus", "Rahu", "Ketu", "Saturn"},
    "Venus":   {"Sun", "Moon", "Rahu"},
    "Saturn":  {"Sun", "Moon", "Mars"},
    "Rahu":    {"Sun", "Moon", "Jupiter"},
    "Ketu":    {"Moon", "Mars"},
}

# Debilitation signs per planet
_DEBILITATION = {
    "Sun":     "Libra",
    "Moon":    "Scorpio",
    "Mars":    "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus":   "Virgo",
    "Saturn":  "Aries",
    "Rahu":    "Scorpio",
    "Ketu":    "Taurus",
}

_DUSTHANA = {6, 8, 12}


def detect_andhe_grah(
    planet_positions: List[Dict[str, Any]],
    chart_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Return per-planet blind-status plus a list of blind planets.

    Args:
        planet_positions: list of {planet, house, sign} dicts
            (LK houses — Aries=1 through Pisces=12).
        chart_data: optional full chart dict used to check retrograde
            and combustion — when absent those criteria are skipped.

    Returns:
        {
            "blind_planets": ["Saturn", "Rahu", ...],
            "per_planet": {
                "Saturn": {
                    "is_blind": True,
                    "reasons": [
                        "part of Andha Teva enemy pair Sun+Saturn in H10",
                        "retrograde + combust",
                    ],
                    "severity": "high",
                    "warning_en": "Remedies for Saturn may backfire...",
                    "warning_hi": "...",
                },
                ...
            },
            "adjacency_warnings": [
                {"planet": "Jupiter", "adjacent_to_blind": ["Mars"],
                 "note": "Jupiter is adjacent to blind Mars — remedy..."},
            ],
            "source": "LK_CANONICAL",
        }
    """
    by_house: Dict[int, List[str]] = {}
    sign_by_planet: Dict[str, str] = {}
    house_by_planet: Dict[str, int] = {}
    for p in planet_positions:
        name = p.get("planet")
        h = p.get("house")
        if not name or not isinstance(h, int):
            continue
        by_house.setdefault(h, []).append(name)
        sign_by_planet[name] = p.get("sign", "")
        house_by_planet[name] = h

    # Extract retrograde, combust, and sign fallback from the full chart if supplied
    retrograde: Dict[str, bool] = {}
    combust: Dict[str, bool] = {}
    if isinstance(chart_data, dict) and "planets" in chart_data:
        for n, info in chart_data["planets"].items():
            retrograde[n] = bool(info.get("retrograde") or info.get("is_retrograde"))
            combust[n]    = bool(info.get("is_combust"))
            # Only fill sign from chart_data when the positions list left it blank
            if n in sign_by_planet and not sign_by_planet[n]:
                sign_by_planet[n] = info.get("sign", "")

    per_planet: Dict[str, Dict[str, Any]] = {}

    for pname in _LK_ENEMIES_LOCAL.keys():
        if pname not in house_by_planet:
            continue

        phouse = house_by_planet[pname]
        psign = sign_by_planet.get(pname, "")
        reasons: List[str] = []

        # Rule 1 — Andha-Teva enemy-pair in H10
        planets_in_h10 = set(by_house.get(10, []))
        for pair in _ANDHA_ENEMY_PAIRS:
            if pname in pair and pair.issubset(planets_in_h10):
                partner = next(iter(pair - {pname}))
                reasons.append(
                    f"part of Andha-Teva enemy pair ({pname}+{partner}) in H10"
                )
                break

        # Rule 2 — H12 with an enemy
        if phouse == 12:
            enemies_in_h12 = [
                q for q in by_house.get(12, [])
                if q != pname and q in _LK_ENEMIES_LOCAL.get(pname, set())
            ]
            if enemies_in_h12:
                reasons.append(
                    f"in H12 (hidden losses) with enemy: {', '.join(enemies_in_h12)}"
                )

        # Rule 3 — retrograde AND combust simultaneously
        if retrograde.get(pname) and combust.get(pname):
            reasons.append("retrograde AND combust — both senses impaired")

        # Rule 4 — debilitated AND in dusthana
        if _DEBILITATION.get(pname) == psign and phouse in _DUSTHANA:
            reasons.append(
                f"debilitated ({psign}) and in dusthana H{phouse}"
            )

        # Rule 5 — Papakartari blind-spot (enemies on both adjacent houses)
        prev_h = ((phouse - 1 - 1) % 12) + 1
        next_h = ((phouse - 1 + 1) % 12) + 1
        prev_enemies = [
            q for q in by_house.get(prev_h, [])
            if q in _LK_ENEMIES_LOCAL.get(pname, set())
        ]
        next_enemies = [
            q for q in by_house.get(next_h, [])
            if q in _LK_ENEMIES_LOCAL.get(pname, set())
        ]
        if prev_enemies and next_enemies:
            reasons.append(
                f"Papakartari — enemies on both sides "
                f"(H{prev_h}: {','.join(prev_enemies)} / "
                f"H{next_h}: {','.join(next_enemies)})"
            )

        is_blind = len(reasons) > 0
        # High severity if 2+ triggers or rule 1 (Andha Teva) or rule 3.
        severity = "high" if (
            len(reasons) >= 2
            or any("Andha-Teva" in r for r in reasons)
            or any("retrograde AND combust" in r for r in reasons)
        ) else ("medium" if is_blind else "none")

        warning_en = (
            f"BLIND PLANET WARNING ({severity}): {pname} is functionally "
            f"blind — " + "; ".join(reasons) + ". Per LK 4.14, remedies "
            f"targeted at {pname} risk backfiring; the blind planet "
            f"intercepts the remedy energy and redirects it into the "
            f"very life-area it is failing to guard. Consult a qualified "
            f"pandit before attempting any {pname} remedy."
        ) if is_blind else ""

        warning_hi = (
            f"अंधे ग्रह चेतावनी ({severity}): {pname} कार्यात्मक रूप से अंधा है — "
            + "; ".join(reasons) + "। लाल किताब 4.14 के अनुसार, {pname} के "
            f"उपाय उल्टा पड़ सकते हैं; अंधा ग्रह उपाय की ऊर्जा को पकड़ कर "
            f"उसी क्षेत्र में भेज देता है जिसे वह नहीं संभाल पा रहा। किसी "
            f"भी {pname} उपाय से पहले योग्य पंडित से परामर्श करें।"
        ) if is_blind else ""

        per_planet[pname] = {
            "planet": pname,
            "house": phouse,
            "sign": psign,
            "is_blind": is_blind,
            "severity": severity,
            "reasons": reasons,
            "warning_en": warning_en,
            "warning_hi": warning_hi,
        }

    blind_list = [name for name, info in per_planet.items() if info["is_blind"]]

    # Adjacency warnings — planets in houses adjacent to blind planets
    # must also carry a LK 4.14 caution flag on their remedies.
    adjacency_warnings: List[Dict[str, Any]] = []
    blind_houses = {per_planet[b]["house"] for b in blind_list}
    for pname, info in per_planet.items():
        if info["is_blind"]:
            continue
        h = info["house"]
        adj_houses = {((h - 1 - 1) % 12) + 1, ((h - 1 + 1) % 12) + 1}
        adjacent_blind = []
        for bh in blind_houses:
            if bh in adj_houses:
                adjacent_blind.extend(
                    b for b in blind_list if per_planet[b]["house"] == bh
                )
        if adjacent_blind:
            adjacency_warnings.append({
                "planet": pname,
                "house": h,
                "adjacent_to_blind": adjacent_blind,
                "note_en": (
                    f"{pname} (H{h}) is adjacent to blind planet(s) "
                    f"{', '.join(adjacent_blind)}. Per LK 4.14, remedies "
                    f"for {pname} may leak into the adjacent blind "
                    f"planet's house — observe the blind-planet precautions "
                    f"even though {pname} itself is not blind."
                ),
                "note_hi": (
                    f"{pname} (भाव {h}) अंधे ग्रह {', '.join(adjacent_blind)} "
                    f"के पास है। लाल किताब 4.14 के अनुसार, {pname} के उपाय "
                    f"निकटवर्ती अंधे ग्रह के भाव में फैल सकते हैं — भले ही "
                    f"{pname} स्वयं अंधा न हो, अंधे ग्रह की सावधानियां मानें।"
                ),
            })

    return {
        "blind_planets": blind_list,
        "per_planet": per_planet,
        "adjacency_warnings": adjacency_warnings,
        "lk_ref": "2.12 / 4.14",
        "source": "LK_CANONICAL",
    }
