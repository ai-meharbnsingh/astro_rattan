"""
graha_sambandha_engine.py — 5 Types of Planetary Connection
============================================================
Implements Phaladeepika Adhyaya 15-16 Graha Sambandha:
the five classical modes by which planets relate to each other.

API:
  analyze_graha_sambandha(planets: dict, asc_sign: str) -> dict
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Mars": [4, 8], "Jupiter": [5, 9], "Saturn": [3, 10],
    "Rahu": [5, 9], "Ketu": [5, 9],
}

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


def _house(p: dict) -> int:
    try:
        return int(p.get("house", 0))
    except (TypeError, ValueError):
        return 0


def _sign(p: dict) -> str:
    return str(p.get("sign", ""))


def _aspects(planet: str, from_house: int, to_house: int) -> bool:
    if not (1 <= from_house <= 12 and 1 <= to_house <= 12):
        return False
    offsets = [7] + list(_SPECIAL_ASPECTS.get(planet, []))
    for n in offsets:
        if ((from_house - 1 + n - 1) % 12) + 1 == to_house:
            return True
    return False


_SAMBANDHA_EFFECT: Dict[str, Tuple[str, str]] = {
    "Yuti": (
        "Conjunction creates a powerful blend — planets share the same house, merging their significations. "
        "Effects of both houses owned by each planet flow through one location. "
        "Phaladeepika Adh. 15: the strongest Sambandha; gives combined results of both planets.",
        "युति सर्वाधिक प्रबल संबंध है — दोनों ग्रह एक भाव में मिलकर अपने-अपने भावों का फल एक साथ देते हैं। "
        "फलदीपिका अ. 15: इनके फल परस्पर मिश्रित होते हैं।"
    ),
    "Paraspara Drishti": (
        "Mutual aspect — both planets see each other across houses. "
        "Full exchange of drishti creates awareness and tension between their significations. "
        "Phaladeepika Adh. 15: mutual sight strengthens both planets' influences.",
        "परस्पर दृष्टि — दोनों ग्रह एक-दूसरे को देखते हैं। दोनों के भावों में परस्पर जागरूकता एवं तनाव। "
        "फलदीपिका अ. 15: पारस्परिक दृष्टि दोनों ग्रहों को बलवान करती है।"
    ),
    "Parivartana": (
        "Exchange of signs — each planet occupies the other's own sign. "
        "Considered as powerful as conjunction. The two planets 'swap' houses, each giving results of the other. "
        "Phaladeepika Adh. 15: Parivartana is a Raja Yoga-level connection when involving strong bhavas.",
        "परिवर्तन — दोनों ग्रह एक-दूसरे की राशि में हैं। युति के समान प्रबल संबंध। "
        "फलदीपिका अ. 15: शुभ भावों में परिवर्तन राज-योग समान फल देता है।"
    ),
    "Eka Drishti": (
        "One-way aspect — one planet aspects the other but not vice versa. "
        "The aspecting planet exerts influence over the other's house significations. "
        "Phaladeepika Adh. 15: partial Sambandha — one planet shapes the destiny of the other.",
        "एकदृष्टि — एक ग्रह दूसरे को देखता है पर दूसरा नहीं। एकतरफा प्रभाव। "
        "फलदीपिका अ. 15: आंशिक संबंध — दृष्टि डालने वाला ग्रह दूसरे के भाव को प्रभावित करता है।"
    ),
    "Lordship Sambandha": (
        "Lordship connection — one planet lords the house occupied by the other. "
        "Creates a teacher-student or ruler-resident relationship between them. "
        "Phaladeepika Adh. 16: the lord of a house carries the karma of its resident planet.",
        "भावेश संबंध — एक ग्रह उस भाव का स्वामी है जिसमें दूसरा बैठा है। "
        "फलदीपिका अ. 16: भावेश अपने भाव के निवासी ग्रह का कर्म वहन करता है।"
    ),
}


def analyze_graha_sambandha(planets: dict, asc_sign: str = "") -> Dict[str, Any]:
    """
    Detect all 5 types of Graha Sambandha between planet pairs.

    Returns:
    {
      "connections": [
        {
          "planet_a": str, "planet_b": str,
          "sambandha_type": str,
          "effect_en": str, "effect_hi": str,
          "sloka_ref": str,
        }, ...
      ],
      "summary_en": str, "summary_hi": str,
      "sloka_ref": "Phaladeepika Adh. 15-16"
    }
    """
    connections = []
    seen_pairs: set = set()

    planet_data = {p: planets[p] for p in _PLANETS if isinstance(planets.get(p), dict)}

    def add_connection(pa: str, pb: str, stype: str) -> None:
        key = tuple(sorted([pa, pb])) + (stype,)
        if key in seen_pairs:
            return
        seen_pairs.add(key)
        eff = _SAMBANDHA_EFFECT[stype]
        ha = _house(planet_data[pa])
        hb = _house(planet_data[pb])
        connections.append({
            "planet_a": pa,
            "planet_b": pb,
            "house_a": ha,
            "house_b": hb,
            "sambandha_type": stype,
            "effect_en": eff[0],
            "effect_hi": eff[1],
            "sloka_ref": "Phaladeepika Adh. 15-16",
        })

    plist = list(planet_data.keys())
    for i, pa in enumerate(plist):
        for pb in plist[i + 1:]:
            da = planet_data[pa]
            db = planet_data[pb]
            ha = _house(da)
            hb = _house(db)
            sa = _sign(da)
            sb = _sign(db)

            # 1. Yuti (same house)
            if ha and hb and ha == hb:
                add_connection(pa, pb, "Yuti")
                continue  # Yuti subsumes all others

            # 2. Parivartana (mutual exchange)
            if sa and sb:
                if _SIGN_LORD.get(sa) == pb and _SIGN_LORD.get(sb) == pa:
                    add_connection(pa, pb, "Parivartana")
                    continue

            # 3. Paraspara Drishti (mutual aspect)
            if ha and hb:
                ab = _aspects(pa, ha, hb)
                ba = _aspects(pb, hb, ha)
                if ab and ba:
                    add_connection(pa, pb, "Paraspara Drishti")
                    continue

                # 4. Eka Drishti (one-way aspect)
                if ab or ba:
                    add_connection(pa, pb, "Eka Drishti")

            # 5. Lordship Sambandha
            if sa and sb and ha and hb:
                lord_of_a_sign = _SIGN_LORD.get(sa, "")
                lord_of_b_sign = _SIGN_LORD.get(sb, "")
                # pb is lord of pa's sign, OR pa is lord of pb's sign
                if lord_of_a_sign == pb or lord_of_b_sign == pa:
                    add_connection(pa, pb, "Lordship Sambandha")

    # Summary
    count = len(connections)
    type_counts: Dict[str, int] = {}
    for c in connections:
        type_counts[c["sambandha_type"]] = type_counts.get(c["sambandha_type"], 0) + 1

    summary_parts = [f"{v} {k}" for k, v in type_counts.items()]
    summary_en = (
        f"{count} planetary connections detected: {', '.join(summary_parts)}. "
        f"Per Phaladeepika Adh. 15-16, these Graha Sambandhas determine how planets "
        f"activate and modify each other's house significations."
    ) if count else (
        "No strong Graha Sambandha detected. Planets operate independently."
    )
    summary_hi = (
        f"कुल {count} ग्रह संबंध: {', '.join(summary_parts)}। "
        f"फलदीपिका अ. 15-16 के अनुसार ये संबंध ग्रहों के भावफल को परस्पर प्रभावित करते हैं।"
    ) if count else (
        "कोई प्रबल ग्रह संबंध नहीं। ग्रह स्वतंत्र रूप से फल देते हैं।"
    )

    return {
        "connections": connections,
        "count": count,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 15-16",
    }
