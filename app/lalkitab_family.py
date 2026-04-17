"""
lalkitab_family.py — Grah-Gasti: Family Chart Linking
======================================================
Cross-chart planetary harmony analysis for Lal Kitab.
"""
from typing import List, Dict, Any, Optional

_PAKKA_GHAR: Dict[str, int] = {
    "Sun": 1, "Moon": 4, "Mars": 3, "Mercury": 7,
    "Jupiter": 2, "Venus": 7, "Saturn": 8, "Rahu": 12, "Ketu": 6,
}
_LK_FRIENDS: Dict[str, set] = {
    "Sun":     {"Moon", "Mars", "Jupiter"},
    "Moon":    {"Sun", "Mercury", "Venus"},
    "Mars":    {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus", "Rahu"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus":   {"Mercury", "Saturn", "Rahu"},
    "Saturn":  {"Mercury", "Venus", "Rahu"},
    "Rahu":    {"Mercury", "Venus", "Saturn"},
    "Ketu":    {"Jupiter", "Mercury", "Venus"},
}
_LK_ENEMIES: Dict[str, set] = {
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
_BENEFIC = {"Jupiter", "Venus", "Moon", "Mercury"}
_MALEFIC = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}


def _safe_p_map(positions: List[Dict]) -> Dict[str, int]:
    return {p["planet"]: p["house"] for p in positions if p.get("planet") and isinstance(p.get("house"), int)}


def calculate_family_harmony(
    owner_positions: List[Dict[str, Any]],
    member_positions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Cross-chart harmony analysis between two Lal Kitab charts.

    Returns: {harmony_score, shared_planets, support_planets, tension_planets, theme}
    """
    o_map = _safe_p_map(owner_positions)
    m_map = _safe_p_map(member_positions)

    score = 50  # baseline
    shared_planets: List[str] = []
    support_planets: List[str] = []
    tension_planets: List[str] = []
    all_planets = set(o_map) | set(m_map)

    for planet in all_planets:
        o_house = o_map.get(planet)
        m_house = m_map.get(planet)
        if o_house is None or m_house is None:
            continue

        # Same house in both charts → shared
        if o_house == m_house:
            shared_planets.append(planet)
            if planet in _BENEFIC:
                score += 10
            elif planet in _MALEFIC:
                score -= 5

        # Both in their own Pakka Ghar → strong positive signal
        if o_house == _PAKKA_GHAR.get(planet) and m_house == _PAKKA_GHAR.get(planet):
            score += 8

    # Moon compatibility (emotional bond)
    o_moon = o_map.get("Moon")
    m_moon = m_map.get("Moon")
    if o_moon and m_moon:
        diff = abs(o_moon - m_moon)
        diff = min(diff, 12 - diff)
        if diff in {0, 6}:     # same or opposite — intense bond
            score += 5
        elif diff in {1, 5}:   # 2nd/6th — supportive
            score += 8
        elif diff in {3, 9}:   # trine — harmonious
            score += 12
        elif diff in {4, 8}:   # square — friction
            score -= 8

    # Cross-chart enemy detection
    for o_planet, o_house in o_map.items():
        for m_planet, m_house in m_map.items():
            if o_planet == m_planet:
                continue
            # Owner's planet is enemy of member's planet in same house zone
            same_zone = abs(o_house - m_house) <= 1 or (o_house == 1 and m_house == 12)
            if same_zone and m_planet in _LK_ENEMIES.get(o_planet, set()):
                if m_planet not in tension_planets:
                    tension_planets.append(m_planet)
                score -= 4
            elif same_zone and m_planet in _LK_FRIENDS.get(o_planet, set()):
                if m_planet not in support_planets:
                    support_planets.append(m_planet)
                score += 3

    score = max(0, min(100, score))

    # Theme
    if score >= 80:
        theme = {"en": "Deeply harmonious — mutual growth and support flow naturally between these charts.", "hi": "गहरा सौहार्द — इन कुंडलियों में परस्पर विकास और समर्थन स्वाभाविक रूप से बहता है।"}
    elif score >= 60:
        theme = {"en": "Good compatibility with areas of shared strength. Minor friction in specific houses.", "hi": "अच्छी अनुकूलता साझा शक्ति के क्षेत्रों के साथ।"}
    elif score >= 40:
        theme = {"en": "Mixed energy — this relationship has both supportive and challenging planetary dynamics.", "hi": "मिश्रित ऊर्जा — इस रिश्ते में सहायक और चुनौतीपूर्ण ग्रह गतिशीलता दोनों हैं।"}
    elif score >= 20:
        theme = {"en": "Significant karmic tension present. Conscious effort and remedies recommended.", "hi": "महत्वपूर्ण कर्मिक तनाव मौजूद। सचेत प्रयास और उपाय अनुशंसित।"}
    else:
        theme = {"en": "Deeply challenging combination. Lal Kitab remedies essential for both.", "hi": "अत्यंत चुनौतीपूर्ण संयोजन। दोनों के लिए लाल किताब उपाय आवश्यक।"}

    return {
        "harmony_score": score,
        "shared_planets": shared_planets,
        "support_planets": list(set(support_planets) - set(tension_planets)),
        "tension_planets": tension_planets,
        "theme": theme,
    }


def get_family_dominant_planet(all_positions: List[Dict[str, Any]]) -> Optional[str]:
    """Most frequent planet across all family charts — the family's ruling planet."""
    from collections import Counter
    planets = [p["planet"] for p in all_positions if p.get("planet")]
    if not planets:
        return None
    # Weight Pakka Ghar occupancies higher
    weighted = Counter()
    p_map = _safe_p_map(all_positions)
    for planet, house in p_map.items():
        weight = 2 if house == _PAKKA_GHAR.get(planet) else 1
        weighted[planet] += weight
    return weighted.most_common(1)[0][0] if weighted else None


def get_family_theme(avg_score: float) -> Dict[str, str]:
    if avg_score >= 70:
        return {"en": "Harmonious family — shared karma supports collective growth.", "hi": "सौहार्दपूर्ण परिवार — साझा कर्म सामूहिक विकास का समर्थन करता है।"}
    elif avg_score >= 45:
        return {"en": "Balanced family karma — cooperation strengthens the weaker charts.", "hi": "संतुलित पारिवारिक कर्म — सहयोग कमज़ोर कुंडलियों को मजबूत करता है।"}
    else:
        return {"en": "Complex family karma — each member carries significant individual burdens.", "hi": "जटिल पारिवारिक कर्म — प्रत्येक सदस्य महत्वपूर्ण व्यक्तिगत बोझ वहन करता है।"}
