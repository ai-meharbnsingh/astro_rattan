"""
lalkitab_master_summary.py — Master Summary Generator for Lal Kitab charts.

All outputs derived from actual chart computation — no hardcoded predictions.
Reference: Lal Kitab 1952 (Pt. Roop Chand Joshi).
"""
from __future__ import annotations
from typing import Any, Dict, List


_PLANET_DOMAIN: Dict[str, Dict[str, str]] = {
    "Sun":     {"en": "authority, health, father",   "hi": "सत्ता, स्वास्थ्य, पिता"},
    "Moon":    {"en": "emotions, mother, mind",       "hi": "भावनाएँ, माता, मन"},
    "Mars":    {"en": "property, siblings, courage",  "hi": "संपत्ति, भाई-बहन, साहस"},
    "Mercury": {"en": "trade, communication, skill",  "hi": "व्यापार, संचार, कुशलता"},
    "Jupiter": {"en": "wisdom, children, prosperity", "hi": "ज्ञान, संतान, समृद्धि"},
    "Venus":   {"en": "marriage, luxury, arts",       "hi": "विवाह, विलासिता, कला"},
    "Saturn":  {"en": "discipline, service, karma",   "hi": "अनुशासन, सेवा, कर्म"},
    "Rahu":    {"en": "ambition, illusion, foreign",  "hi": "महत्वाकांक्षा, भ्रम, विदेश"},
    "Ketu":    {"en": "spirituality, loss, research", "hi": "आध्यात्मिकता, हानि, शोध"},
}

_HOUSE_THEME: Dict[int, Dict[str, str]] = {
    1:  {"en": "self/body",         "hi": "स्वयं/शरीर"},
    2:  {"en": "family/wealth",     "hi": "परिवार/धन"},
    3:  {"en": "courage/siblings",  "hi": "साहस/भाई-बहन"},
    4:  {"en": "home/mother",       "hi": "घर/माता"},
    5:  {"en": "children/mind",     "hi": "संतान/बुद्धि"},
    6:  {"en": "enemies/debts",     "hi": "शत्रु/ऋण"},
    7:  {"en": "marriage/partners", "hi": "विवाह/साझेदार"},
    8:  {"en": "longevity/secrets", "hi": "आयु/रहस्य"},
    9:  {"en": "fortune/religion",  "hi": "भाग्य/धर्म"},
    10: {"en": "career/status",     "hi": "करियर/प्रतिष्ठा"},
    11: {"en": "income/gains",      "hi": "आय/लाभ"},
    12: {"en": "loss/liberation",   "hi": "हानि/मोक्ष"},
}

_URGENCY_RANK = {"high": 0, "medium": 1, "low": 2}


def _top_3_remedies(remedies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return top-3 actionable remedies ranked by urgency then strength (descending)."""
    actionable = [r for r in remedies if r.get("has_remedy") and r.get("remedy_en")]
    actionable.sort(key=lambda r: (
        _URGENCY_RANK.get(r.get("urgency", "low"), 2),
        -(r.get("strength", 50)),
    ))
    return [
        {
            "planet": r["planet"],
            "planet_hi": r.get("planet_hi", r["planet"]),
            "lk_house": r["lk_house"],
            "urgency": r.get("urgency", "low"),
            "strength": r.get("strength", 50),
            "remedy_en": r.get("remedy_en", ""),
            "remedy_hi": r.get("remedy_hi", ""),
            "problem_en": r.get("problem_en", ""),
            "problem_hi": r.get("problem_hi", ""),
            "how_en": r.get("how_en", ""),
            "how_hi": r.get("how_hi", ""),
            "day": r.get("day", ""),
            "classification": r.get("classification", ""),
        }
        for r in actionable[:3]
    ]


def _core_pattern(
    sacrifice_results: List[Dict[str, Any]],
    positions: List[Dict[str, Any]],
    karmic_debts: List[Any],
) -> Dict[str, str]:
    """
    Derives the dominant life pattern from cross-planet conflicts, karmic debts,
    and dusthana clusters. Returns {en, hi} built entirely from data fields.
    """
    parts_en: List[str] = []
    parts_hi: List[str] = []

    # Sacrifice patterns (high severity first)
    ranked_sac = sorted(
        sacrifice_results,
        key=lambda s: 0 if s.get("severity") == "high" else 1,
    )
    for s in ranked_sac[:2]:
        sacrificer = s.get("sacrificer", "")
        cost = s.get("cost_area", {}).get("areas", {})
        growth = s.get("growth_area", {}).get("areas", {})
        cost_en = cost.get("en", sacrificer) if isinstance(cost, dict) else str(cost)
        cost_hi = cost.get("hi", sacrificer) if isinstance(cost, dict) else str(cost)
        growth_en = growth.get("en", "") if isinstance(growth, dict) else str(growth)
        growth_hi = growth.get("hi", "") if isinstance(growth, dict) else str(growth)
        parts_en.append(
            f"{sacrificer} sacrifices {cost_en} to sustain {growth_en} "
            f"({s.get('condition', '')})."
        )
        parts_hi.append(
            f"{sacrificer} {cost_hi} का बलिदान करके {growth_hi} को बनाए रखता है "
            f"({s.get('condition', '')})।"
        )

    # Active karmic debts
    if karmic_debts:
        debt_planets = [
            d.get("planet", d.get("rin_planet", ""))
            for d in karmic_debts[:2]
            if isinstance(d, dict) and d.get("planet", d.get("rin_planet", ""))
        ]
        if debt_planets:
            dp_en = " and ".join(debt_planets)
            dp_hi = " और ".join(debt_planets)
            parts_en.append(f"Karmic debts of {dp_en} require active clearing.")
            parts_hi.append(f"{dp_hi} के कर्मिक ऋण को सक्रिय रूप से चुकाना आवश्यक है।")

    # Dusthana cluster
    pos_map = {p.get("planet", ""): p.get("house", 0) for p in positions if isinstance(p, dict)}
    dusthana = [pl for pl, h in pos_map.items() if h in {6, 8, 12}]
    if len(dusthana) >= 2:
        dl = ", ".join(dusthana[:3])
        parts_en.append(f"{dl} in dusthana houses (6/8/12) amplify karmic challenges.")
        parts_hi.append(f"{dl} दुःस्थान भावों (6/8/12) में कर्मिक चुनौतियाँ बढ़ाते हैं।")

    if not parts_en:
        parts_en.append("Chart shows balanced planetary distribution with moderate karmic load.")
        parts_hi.append("कुंडली संतुलित ग्रह वितरण और सामान्य कर्मिक भार दर्शाती है।")

    return {"en": " ".join(parts_en), "hi": " ".join(parts_hi)}


def _main_problem(remedies: List[Dict[str, Any]], karmic_debts: List[Any]) -> Dict[str, Any]:
    """
    Identify the single most pressing problem: planet with highest urgency
    and lowest strength score that has an active remedy need.
    """
    for urgency_level in ("high", "medium", "low"):
        candidates = [
            r for r in remedies
            if r.get("urgency") == urgency_level and r.get("has_remedy")
        ]
        if candidates:
            break
    else:
        candidates = remedies[:1]

    if not candidates:
        return {"planet": None, "en": "No critical problem identified.", "hi": "कोई गंभीर समस्या नहीं।"}

    worst = min(candidates, key=lambda r: r.get("strength", 100))
    planet = worst["planet"]
    house = worst.get("lk_house", 0)
    house_theme = _HOUSE_THEME.get(house, {"en": f"house {house}", "hi": f"भाव {house}"})

    # Check for matching karmic debt
    debt_suffix_en = ""
    debt_suffix_hi = ""
    for d in (karmic_debts or []):
        if isinstance(d, dict):
            dp = d.get("planet", d.get("rin_planet", ""))
            if dp == planet:
                desc_en = d.get("description_en", d.get("en_desc", ""))
                desc_hi = d.get("description_hi", d.get("hi_desc", ""))
                if desc_en:
                    debt_suffix_en = f" Active karmic debt: {desc_en}"
                    debt_suffix_hi = f" सक्रिय कर्मिक ऋण: {desc_hi}"
                break

    problem_en = worst.get("problem_en", "")
    problem_hi = worst.get("problem_hi", "")
    if not problem_en:
        domain = _PLANET_DOMAIN.get(planet, {"en": "life areas", "hi": "जीवन क्षेत्र"})
        problem_en = (
            f"{planet} in H{house} ({house_theme['en']}) is the most challenged planet "
            f"(strength {worst.get('strength', '?')}%), weakening {domain['en']}."
        )
        problem_hi = (
            f"H{house} ({house_theme['hi']}) में {planet} सबसे चुनौतीपूर्ण ग्रह है "
            f"(शक्ति {worst.get('strength', '?')}%), {domain['hi']} को कमज़ोर करता है।"
        )

    return {
        "planet": planet,
        "lk_house": house,
        "strength": worst.get("strength", 0),
        "urgency": worst.get("urgency", "high"),
        "en": problem_en + debt_suffix_en,
        "hi": problem_hi + debt_suffix_hi,
    }


def _dasha_2yr_outlook(dasha_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a 2-year narrative from actual saala grah dasha data.
    Returns: timeline (current + 2 upcoming years), summary_{en,hi}.
    """
    current = dasha_data.get("current_saala_grah", {})
    upcoming = dasha_data.get("upcoming_periods", [])

    timeline: List[Dict[str, Any]] = []
    if current:
        timeline.append({
            "year": current.get("started_year"),
            "ends_year": current.get("ends_year"),
            "planet": current.get("planet"),
            "planet_hi": current.get("planet_hi", ""),
            "label": "current",
            "en": current.get("en_desc", ""),
            "hi": current.get("hi_desc", ""),
        })
    for p in upcoming[:2]:
        timeline.append({
            "year": p.get("year"),
            "planet": p.get("planet"),
            "planet_hi": p.get("planet_hi", ""),
            "label": "upcoming",
            "en": p.get("en_desc", ""),
            "hi": p.get("hi_desc", ""),
        })

    # Build one-line summary from first sentence of each desc
    parts_en, parts_hi = [], []
    for entry in timeline:
        yr = entry.get("year", "")
        planet = entry.get("planet", "")
        desc_en = entry.get("en", "").split(".")[0] if entry.get("en") else ""
        desc_hi = entry.get("hi", "").split("।")[0] if entry.get("hi") else ""
        if yr and planet:
            parts_en.append(f"{yr} ({planet}): {desc_en}.")
            parts_hi.append(f"{yr} ({planet}): {desc_hi}।")

    return {
        "timeline": timeline,
        "summary_en": " → ".join(parts_en),
        "summary_hi": " → ".join(parts_hi),
    }


def generate_master_summary(
    positions: List[Dict[str, Any]],
    remedies: List[Dict[str, Any]],
    karmic_debts: List[Any],
    sacrifice_results: List[Dict[str, Any]],
    dasha_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a complete master summary for a Lal Kitab chart.

    Args:
        positions:        list of {planet, house, ...} from chart
        remedies:         enriched remedy list from get_remedies()
        karmic_debts:     from calculate_karmic_debts()
        sacrifice_results: from analyze_sacrifice()
        dasha_data:       from get_dasha_timeline()

    Returns dict with:
        core_pattern   — dominant life conflict {en, hi}
        main_problem   — single biggest planet issue {planet, lk_house, strength, en, hi}
        top_3_actions  — ranked top-3 remedies list
        dasha_2yr      — 2-year saala grah narrative {timeline, summary_en, summary_hi}
    """
    return {
        "core_pattern": _core_pattern(sacrifice_results, positions, karmic_debts),
        "main_problem": _main_problem(remedies, karmic_debts),
        "top_3_actions": _top_3_remedies(remedies),
        "dasha_2yr": _dasha_2yr_outlook(dasha_data),
    }
