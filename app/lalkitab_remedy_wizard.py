"""
app/lalkitab_remedy_wizard.py

P2.4 — Intent-driven Remedy Wizard.

Transforms a user INTENT (e.g., "marriage", "finance", "career") into a set of
RANKED Lal Kitab remedies that are tailored to that specific intent, rather
than the static list of nine planet-level remedies produced by
`get_remedies()`.

Public API:
    recommend_remedies(intent, planet_positions, afflictions) -> dict

The function re-ranks planet remedies against an INTENT_PROFILE. It does NOT
invent new remedies — every remedy returned is the same enriched remedy the
`/api/lalkitab/remedies/enriched` endpoint already produces. This keeps the
wizard safely labelled LK_DERIVED (re-ranking of canonical remedies), not
PRODUCT (we would have to tag it PRODUCT if we fabricated new rituals).

Bilingual: every intent and every `match_reason_*` carries EN + HI.
"""

from __future__ import annotations

from typing import Any

from app.lalkitab_source_tags import LK_DERIVED


# ─────────────────────────────────────────────────────────────────────────
# INTENT PROFILE
# Map a user's life-intent to:
#   focus_planets : planets whose Lal Kitab significations govern this intent
#   focus_houses  : Lal Kitab houses (fixed Aries=H1 scheme) that rule this intent
#   avoid         : (planet, house) pairs that are WARNING patterns for this
#                   intent — e.g., Saturn in H2 = finance drain
#   label_en/hi   : bilingual display label for the intent card
#   icon          : suggested lucide-react icon NAME (frontend can override)
# ─────────────────────────────────────────────────────────────────────────
INTENT_PROFILE: dict[str, dict[str, Any]] = {
    "finance": {
        "focus_planets": ["Jupiter", "Venus"],
        "focus_houses": [2, 11],
        "avoid": [("Saturn", 2)],
        "label_en": "Finance / Wealth",
        "label_hi": "धन / वित्त",
        "icon": "Wallet",
        "desc_en": "Improve earnings, savings, and financial stability.",
        "desc_hi": "आय, बचत और आर्थिक स्थिरता सुधारें।",
    },
    "marriage": {
        "focus_planets": ["Venus", "Moon"],
        "focus_houses": [7],
        "avoid": [("Mars", 7)],
        "label_en": "Marriage / Relationships",
        "label_hi": "विवाह / संबंध",
        "icon": "Heart",
        "desc_en": "Harmony and longevity in marriage and partnerships.",
        "desc_hi": "विवाह और साझेदारी में सामंजस्य।",
    },
    "career": {
        "focus_planets": ["Sun", "Saturn", "Mercury"],
        "focus_houses": [3, 10, 11],
        "avoid": [],
        "label_en": "Career / Profession",
        "label_hi": "करियर / व्यवसाय",
        "icon": "Briefcase",
        "desc_en": "Recognition, promotions, and stable professional life.",
        "desc_hi": "मान्यता, पदोन्नति और स्थिर व्यवसाय।",
    },
    "health": {
        "focus_planets": ["Sun", "Moon"],
        "focus_houses": [1, 4, 6],
        "avoid": [("Saturn", 6)],
        "label_en": "Health / Vitality",
        "label_hi": "स्वास्थ्य / जीवन-शक्ति",
        "icon": "Activity",
        "desc_en": "Strengthen vitality and counter chronic health issues.",
        "desc_hi": "जीवन-शक्ति बढ़ाएँ और पुरानी बीमारियों का सामना करें।",
    },
    "children": {
        "focus_planets": ["Jupiter", "Moon"],
        "focus_houses": [5],
        "avoid": [("Rahu", 5)],
        "label_en": "Children / Progeny",
        "label_hi": "संतान",
        "icon": "Baby",
        "desc_en": "Conception, childbirth, and progeny welfare.",
        "desc_hi": "गर्भधारण, संतान-जन्म और संतान के कल्याण।",
    },
    "spirituality": {
        "focus_planets": ["Jupiter", "Ketu"],
        "focus_houses": [9, 12],
        "avoid": [],
        "label_en": "Spirituality / Moksha",
        "label_hi": "आध्यात्म / मोक्ष",
        "icon": "Flame",
        "desc_en": "Guru-grace, inner peace, and spiritual practice.",
        "desc_hi": "गुरु कृपा, आंतरिक शांति और साधना।",
    },
    "home": {
        "focus_planets": ["Moon", "Mars"],
        "focus_houses": [4],
        "avoid": [("Saturn", 4)],
        "label_en": "Home / Mother / Property",
        "label_hi": "घर / माँ / भूमि",
        "icon": "Home",
        "desc_en": "Peace at home, maternal health, and real-estate matters.",
        "desc_hi": "घर में शांति, माता का स्वास्थ्य, भूमि-संबंधी मामले।",
    },
    "enemies": {
        "focus_planets": ["Mars", "Saturn"],
        "focus_houses": [6],
        "avoid": [],
        "label_en": "Enemies / Opponents",
        "label_hi": "शत्रु / विरोधी",
        "icon": "Swords",
        "desc_en": "Overcome enemies, hidden rivals, and workplace conflict.",
        "desc_hi": "शत्रुओं, छुपे विरोधियों और कार्यस्थल के टकराव पर विजय।",
    },
    "legal": {
        "focus_planets": ["Saturn", "Rahu"],
        "focus_houses": [6, 11],
        "avoid": [],
        "label_en": "Legal / Litigation",
        "label_hi": "मुक़दमा / कानूनी",
        "icon": "Scale",
        "desc_en": "Court cases, disputes, and legal matters.",
        "desc_hi": "अदालत, विवाद और कानूनी मामलों में सहायता।",
    },
}


def list_intents() -> list[dict[str, Any]]:
    """Public helper — return all intent cards for the first wizard step."""
    return [
        {
            "id": iid,
            "label_en": prof["label_en"],
            "label_hi": prof["label_hi"],
            "desc_en": prof["desc_en"],
            "desc_hi": prof["desc_hi"],
            "icon": prof["icon"],
            "focus_planets": list(prof["focus_planets"]),
            "focus_houses": list(prof["focus_houses"]),
        }
        for iid, prof in INTENT_PROFILE.items()
    ]


def _match_reason(
    planet: str,
    lk_house: int,
    intent: str,
    focus_planets: list[str],
    focus_houses: list[int],
    avoid: list[tuple[str, int]],
    is_weak: bool,
    afflictions: list[str],
) -> tuple[str, str, float]:
    """
    Explain WHY this remedy ranks for the intent, in EN + HI, and return
    a relevance score in [0, 1.5] used for sorting (higher = more relevant).
    """
    intent_en = INTENT_PROFILE[intent]["label_en"]
    intent_hi = INTENT_PROFILE[intent]["label_hi"]
    score = 0.0
    reasons_en: list[str] = []
    reasons_hi: list[str] = []

    is_avoid_hit = (planet, lk_house) in avoid

    if planet in focus_planets:
        score += 0.6
        reasons_en.append(
            f"{planet} directly governs {intent_en}"
        )
        reasons_hi.append(
            f"{planet} सीधे {intent_hi} का स्वामी है"
        )

    if lk_house in focus_houses:
        score += 0.5
        reasons_en.append(
            f"sits in House {lk_house}, a key house for {intent_en}"
        )
        reasons_hi.append(
            f"भाव {lk_house} में है — जो {intent_hi} का मुख्य भाव है"
        )

    if is_avoid_hit:
        # A warned pair: this means the placement is ACTIVELY damaging the
        # intent — urgent remedy.
        score += 0.8
        reasons_en.append(
            f"⚠ {planet} in House {lk_house} is a known obstacle for {intent_en}"
        )
        reasons_hi.append(
            f"⚠ भाव {lk_house} में {planet} {intent_hi} के लिए ज्ञात बाधा है"
        )

    if is_weak:
        score += 0.3
        reasons_en.append("the planet is weak in this chart")
        reasons_hi.append("इस कुंडली में ग्रह कमज़ोर है")

    if afflictions:
        score += 0.15
        affl_str = ", ".join(afflictions)
        reasons_en.append(f"afflictions present: {affl_str}")
        reasons_hi.append(f"दोष मौजूद: {affl_str}")

    if not reasons_en:
        # Baseline: still show a faint match so all planets sort cleanly.
        reasons_en.append(f"general supporting remedy for {intent_en}")
        reasons_hi.append(f"{intent_hi} के लिए सामान्य सहायक उपाय")
        score = 0.05

    return ("; ".join(reasons_en), "; ".join(reasons_hi), round(score, 3))


def recommend_remedies(
    intent: str,
    planet_positions: list[dict[str, Any]],
    afflictions: "dict[str, list[str]] | None" = None,
) -> dict[str, Any]:
    """
    Main wizard entry point.

    Args:
        intent:            one of INTENT_PROFILE keys
        planet_positions:  list of enriched remedy dicts (as produced by
                           the existing /api/lalkitab/remedies/enriched route
                           — same shape: planet, planet_hi, sign, lk_house,
                           dignity, strength, has_remedy, urgency, remedy_en/hi,
                           problem_en/hi, reason_en/hi, how_en/hi, material, day)
        afflictions:       optional {planet: [affliction strings]} map. When
                           absent we fall back to `has_remedy` as a weakness
                           signal.

    Returns:
        {
            intent, intent_label_en, intent_label_hi,
            focus_planets, focus_houses, avoid,
            ranked_remedies: [ { ... enriched remedy fields ...,
                                  match_reason_en, match_reason_hi,
                                  relevance_score } ],
            top_picks: [ ... up to 3 top-scored ... ],
            source: "LK_DERIVED"
        }

    NEVER invents a remedy — only re-ranks what `get_remedies()` already
    returned. If intent is unknown, returns source="LK_DERIVED" with a
    clear `error` field and an empty ranking.
    """
    afflictions = afflictions or {}

    if intent not in INTENT_PROFILE:
        return {
            "intent": intent,
            "intent_label_en": intent,
            "intent_label_hi": intent,
            "focus_planets": [],
            "focus_houses": [],
            "avoid": [],
            "ranked_remedies": [],
            "top_picks": [],
            "source": LK_DERIVED,
            "error": f"Unknown intent '{intent}'. "
                     f"Must be one of: {sorted(INTENT_PROFILE.keys())}",
        }

    prof = INTENT_PROFILE[intent]
    focus_planets = list(prof["focus_planets"])
    focus_houses = list(prof["focus_houses"])
    avoid: list[tuple[str, int]] = [
        (p, h) for (p, h) in prof.get("avoid", [])
    ]

    ranked: list[dict[str, Any]] = []
    for rem in planet_positions or []:
        # Defensive: skip any malformed entries rather than crash.
        planet = rem.get("planet")
        lk_house = rem.get("lk_house")
        if not planet or not isinstance(lk_house, int) or lk_house <= 0:
            continue

        is_weak = bool(rem.get("has_remedy", False))
        planet_afflictions = afflictions.get(planet, []) or rem.get("afflictions", []) or []

        reason_en, reason_hi, score = _match_reason(
            planet=planet,
            lk_house=lk_house,
            intent=intent,
            focus_planets=focus_planets,
            focus_houses=focus_houses,
            avoid=avoid,
            is_weak=is_weak,
            afflictions=planet_afflictions,
        )

        enriched = dict(rem)
        enriched["match_reason_en"] = reason_en
        enriched["match_reason_hi"] = reason_hi
        enriched["relevance_score"] = score
        enriched["matches_focus_planet"] = planet in focus_planets
        enriched["matches_focus_house"] = lk_house in focus_houses
        enriched["matches_avoid"] = (planet, lk_house) in avoid
        ranked.append(enriched)

    # Sort: highest relevance first, then by has_remedy (urgent first), then
    # by urgency (high > medium > low), then alphabetical planet name for
    # deterministic output in tests.
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    ranked.sort(
        key=lambda r: (
            -r.get("relevance_score", 0.0),
            0 if r.get("has_remedy") else 1,
            urgency_order.get(r.get("urgency", "low"), 3),
            str(r.get("planet", "")),
        )
    )

    top_picks = ranked[:3]

    return {
        "intent": intent,
        "intent_label_en": prof["label_en"],
        "intent_label_hi": prof["label_hi"],
        "focus_planets": focus_planets,
        "focus_houses": focus_houses,
        "avoid": [{"planet": p, "house": h} for (p, h) in avoid],
        "ranked_remedies": ranked,
        "top_picks": top_picks,
        "source": LK_DERIVED,
    }
