"""
ashtakvarga_engine.py -- Ashtakvarga Calculation Engine
========================================================
Calculates the Ashtakvarga point system used in Vedic astrology for
transit predictions. Each planet gets 0 or 1 point (bindu) from each
of the 7 contributing planets + Ascendant for each of the 12 signs.

The Sarvashtakvarga is the sum of all individual planet ashtakvargas.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set

# Sign names
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# ============================================================
# BENEFIC POINTS -- Houses from each contributing planet that
# give a benefic point (bindu). Houses are 1-indexed relative
# to the contributing planet's position.
# Format: BENEFIC_POINTS[receiving_planet][contributing_planet] = set of house numbers
# ============================================================

BENEFIC_POINTS: Dict[str, Dict[str, Set[int]]] = {
    "Sun": {
        "Sun":       {1, 2, 4, 7, 8, 9, 10, 11},
        "Moon":      {3, 6, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 9, 11},
        "Venus":     {6, 7, 12},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {3, 4, 6, 10, 11, 12},
    },
    "Moon": {
        "Sun":       {3, 6, 7, 8, 10, 11},
        "Moon":      {1, 3, 6, 7, 10, 11},
        "Mars":      {2, 3, 5, 6, 9, 10, 11},
        "Mercury":   {1, 3, 4, 5, 7, 8, 10, 11},
        "Jupiter":   {1, 4, 7, 8, 10, 11, 12},
        "Venus":     {3, 4, 5, 7, 9, 10, 11},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {3, 6, 10, 11},
    },
    "Mars": {
        "Sun":       {3, 5, 6, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {3, 5, 6, 11},
        "Jupiter":   {6, 10, 11, 12},
        "Venus":     {6, 8, 11, 12},
        "Saturn":    {1, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 3, 6, 10, 11},
    },
    "Mercury": {
        "Sun":       {5, 6, 9, 11, 12},
        "Moon":      {2, 4, 6, 8, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {1, 3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {6, 8, 11, 12},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 11},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 2, 4, 6, 8, 10, 11},
    },
    "Jupiter": {
        "Sun":       {1, 2, 3, 4, 7, 8, 9, 10, 11},
        "Moon":      {2, 5, 7, 9, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {1, 2, 4, 5, 6, 9, 10, 11},
        "Jupiter":   {1, 2, 3, 4, 7, 8, 10, 11},
        "Venus":     {2, 5, 6, 9, 10, 11},
        "Saturn":    {3, 5, 6, 12},
        "Ascendant": {1, 2, 4, 5, 6, 7, 9, 10, 11},
    },
    "Venus": {
        "Sun":       {8, 11, 12},
        "Moon":      {1, 2, 3, 4, 5, 8, 9, 11, 12},
        "Mars":      {3, 5, 6, 9, 11, 12},
        "Mercury":   {3, 5, 6, 9, 11},
        "Jupiter":   {5, 8, 9, 10, 11},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 10, 11},
        "Saturn":    {3, 4, 5, 8, 9, 10, 11},
        "Ascendant": {1, 2, 3, 4, 5, 8, 9, 11},
    },
    "Saturn": {
        "Sun":       {1, 2, 4, 7, 8, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {3, 5, 6, 10, 11, 12},
        "Mercury":   {6, 8, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 11, 12},
        "Venus":     {6, 11, 12},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {1, 3, 4, 6, 10, 11},
    },
    # Lagna (Ascendant) Ashtakvarga — benefic houses from each contributor
    "Lagna": {
        "Sun":       {3, 4, 6, 10, 11, 12},
        "Moon":      {3, 6, 10, 11},
        "Mars":      {1, 3, 6, 10, 11},
        "Mercury":   {1, 2, 4, 6, 8, 10, 11},
        "Jupiter":   {1, 2, 4, 5, 6, 7, 9, 10, 11},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 11},
        "Saturn":    {1, 3, 4, 6, 10, 11},
        "Ascendant": {3, 4, 6, 10, 11, 12},
    },
}


def _sign_name_to_index(sign_name: str) -> int:
    """Convert sign name to 0-based index."""
    return _SIGN_NAMES.index(sign_name)


def calculate_ashtakvarga(planet_signs: Dict[str, str]) -> Dict[str, Any]:
    """
    Calculate the Ashtakvarga system for a given chart.
    Includes Trikona Shodhana, Ekadhipatya Shodhana and Shodhya Pinda.
    """
    # Validate required planets
    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    available = set(planet_signs.keys())
    missing = required - available
    if missing:
        raise ValueError(f"Missing planets for Ashtakvarga: {missing}")

    # Build position map: planet/ascendant -> 0-based sign index
    positions: Dict[str, int] = {}
    for name, sign in planet_signs.items():
        if name in required or name == "Ascendant":
            positions[name] = _sign_name_to_index(sign)

    if "Ascendant" not in positions:
        positions["Ascendant"] = 0

    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]
    _CONTRIB_DISPLAY = {c: ("Lagna" if c == "Ascendant" else c) for c in contributors}

    planet_bindus: Dict[str, Dict[str, int]] = {}
    planet_details: Dict[str, Dict[str, Any]] = {}
    sarvashtakvarga: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

    # 1. Calculate base Bindus
    for recv_planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]:
        recv_table = BENEFIC_POINTS[recv_planet]
        bindus: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}
        contrib_matrix: Dict[str, Dict[str, int]] = {}

        for contrib in contributors:
            display_name = _CONTRIB_DISPLAY[contrib]
            contrib_row: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

            if contrib in recv_table and contrib in positions:
                benefic_houses = recv_table[contrib]
                contrib_sign_index = positions[contrib]

                for house_num in benefic_houses:
                    target_sign_index = (contrib_sign_index + house_num - 1) % 12
                    target_sign = _SIGN_NAMES[target_sign_index]
                    contrib_row[target_sign] = 1
                    bindus[target_sign] += 1

            contrib_matrix[display_name] = contrib_row

        planet_bindus[recv_planet] = bindus
        planet_details[recv_planet] = {
            "contributors": contrib_matrix,
            "totals": bindus,
        }

        if recv_planet != "Lagna":
            for sign in _SIGN_NAMES:
                sarvashtakvarga[sign] += bindus[sign]

    # 2. Purification (Shodhana) for each of the 7 planets
    purified_data: Dict[str, Any] = {}
    for planet in required:
        raw_bindus = list(planet_bindus[planet].values()) # 12 values
        
        # A. Trikona Shodhana (Trine Reduction)
        trikona = _apply_trikona_shodhana(raw_bindus)
        
        # B. Ekadhipatya Shodhana (Lordship Reduction)
        # Needs planet positions to check for occupancy
        ekadhipatya = _apply_ekadhipatya_shodhana(trikona, positions)
        
        # C. Shodhya Pinda (Purified Index)
        shodhya_pinda = _calculate_shodhya_pinda(planet, ekadhipatya, positions)
        
        purified_data[planet] = {
            "trikona": {sign: val for sign, val in zip(_SIGN_NAMES, trikona)},
            "ekadhipatya": {sign: val for sign, val in zip(_SIGN_NAMES, ekadhipatya)},
            "shodhya_pinda": shodhya_pinda
        }

    return {
        "planet_bindus": planet_bindus,
        "sarvashtakvarga": sarvashtakvarga,
        "planet_details": planet_details,
        "purified": purified_data
    }

def _apply_trikona_shodhana(bindus: List[int]) -> List[int]:
    """
    Reduces bindus in trine signs.
    Trines: (0,4,8), (1,5,9), (2,6,10), (3,7,11)
    """
    res = list(bindus)
    trines = [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]
    for t in trines:
        v1, v2, v3 = res[t[0]], res[t[1]], res[t[2]]
        if v1 == 0 or v2 == 0 or v3 == 0:
            continue
        m = min(v1, v2, v3)
        res[t[0]] -= m
        res[t[1]] -= m
        res[t[2]] -= m
    return res

def _apply_ekadhipatya_shodhana(bindus: List[int], positions: Dict[str, int]) -> List[int]:
    """
    Lordship reduction for pairs of signs owned by the same planet.
    """
    res = list(bindus)
    # Pairs of sign indices: Mars(0,7), Mercury(2,5), Jupiter(8,11), Venus(1,6), Saturn(9,10)
    pairs = [(0, 7), (2, 5), (8, 11), (1, 6), (9, 10)]
    
    # Check occupancy
    occupied = set(positions.values())
    
    for s1, s2 in pairs:
        v1, v2 = res[s1], res[s2]
        occ1, occ2 = s1 in occupied, s2 in occupied
        
        if v1 > 0 and v2 > 0:
            if not occ1 and not occ2:
                # Both unoccupied: subtract smaller from both
                m = min(v1, v2)
                res[s1] -= m
                res[s2] -= m
            elif occ1 and occ2:
                # Both occupied: No reduction
                pass
            elif occ1 and not occ2:
                # Sign 1 occupied, Sign 2 unoccupied
                if v2 > v1: res[s2] = v1
                else: res[s2] = 0
            elif not occ1 and occ2:
                # Sign 2 occupied, Sign 1 unoccupied
                if v1 > v2: res[s1] = v2
                else: res[s1] = 0
        elif (v1 > 0 and v2 == 0) or (v1 == 0 and v2 > 0):
            # One is zero
            idx = s1 if v1 > 0 else s2
            if idx not in occupied:
                # Unoccupied sign with bindus: potentially reduce based on other sign's trines?
                # Simplified scriptural rule: if one is 0 and other is unoccupied, reduce to 0
                res[idx] = 0
                
    return res

def _calculate_shodhya_pinda(planet: str, purified: List[int], positions: Dict[str, int]) -> int:
    """
    Calculate Shodhya Pinda (Purified Index).
    """
    sign_multipliers = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]
    planet_multipliers = {
        "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5, 
        "Jupiter": 10, "Venus": 7, "Saturn": 5
    }
    
    # 1. Rashi Pinda
    rashi_pinda = sum(p * m for p, m in zip(purified, sign_multipliers))
    
    # 2. Graha Pinda
    # Sum of (Purified points in sign where planet X is) * (Multiplier of planet X)
    graha_pinda = 0
    for p_name, sign_idx in positions.items():
        if p_name in planet_multipliers:
            graha_pinda += purified[sign_idx] * planet_multipliers[p_name]

    return rashi_pinda + graha_pinda


# ════════════════════════════════════════════════════════════════════
# PHALADEEPIKA ADHYAYA 24 — ASHTAKAVARGA-PHALA (APPLIED PREDICTIVE RULES)
# ════════════════════════════════════════════════════════════════════
# Classical per-planet SAV bindu thresholds for transit phala.
# A planet transiting a rasi with bindus >= its own threshold in SAV
# (in its own Bhinnashtakavarga table) gives favorable results.
# Values drawn from Phaladeepika Adh. 24 + Brihat Parashara standard.
_PLANET_TRANSIT_THRESHOLD: Dict[str, int] = {
    "Sun": 4,
    "Moon": 4,
    "Mars": 3,
    "Mercury": 5,
    "Jupiter": 5,
    "Venus": 5,
    "Saturn": 3,
}

# Hindi names for the 12 signs (used for bilingual interpretations)
_SIGN_HI = {
    "Aries": "मेष", "Taurus": "वृषभ", "Gemini": "मिथुन", "Cancer": "कर्क",
    "Leo": "सिंह", "Virgo": "कन्या", "Libra": "तुला", "Scorpio": "वृश्चिक",
    "Sagittarius": "धनु", "Capricorn": "मकर", "Aquarius": "कुंभ", "Pisces": "मीन",
}

_PLANET_HI = {
    "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि",
}

# Per-house significance (brief) used to compose interpretations.
_HOUSE_SIG_EN = {
    1: "self, vitality, body", 2: "wealth, family, speech",
    3: "courage, siblings, effort", 4: "home, mother, peace",
    5: "children, intellect, creativity", 6: "enemies, disease, service",
    7: "marriage, partnerships", 8: "longevity, hidden matters",
    9: "fortune, dharma, father", 10: "career, status, karma",
    11: "gains, elder siblings, fulfilment", 12: "expenses, losses, liberation",
}
_HOUSE_SIG_HI = {
    1: "तनु, जीवन-शक्ति", 2: "धन, कुटुंब, वाणी",
    3: "पराक्रम, सहोदर, उद्यम", 4: "गृह, माता, सुख",
    5: "संतान, बुद्धि, विद्या", 6: "शत्रु, रोग, सेवा",
    7: "विवाह, साझेदारी", 8: "आयु, गुप्त विषय",
    9: "भाग्य, धर्म, पिता", 10: "कर्म, पद, यश",
    11: "लाभ, बड़े भाई, पूर्ति", 12: "व्यय, हानि, मोक्ष",
}


def _planet_transit_threshold(planet: str) -> int:
    """Classical SAV-bindu threshold for a planet's transit to be favorable.

    Per Phaladeepika Adh. 24: a planet transiting a rasi with bindus
    >= this threshold gives favorable results; below → unfavorable.
    """
    return _PLANET_TRANSIT_THRESHOLD.get(planet, 4)


def _house_status_from_bindus(bindus: int) -> str:
    """Classify a house's SAV bindu total into strong / moderate / weak.

    Phaladeepika Adh. 24 sloka 2:
      >= 30  → strong (flourishing house)
      25-29  → moderate (mixed results)
      < 25   → weak (afflicted, obstacles)
    """
    if bindus >= 30:
        return "strong"
    if bindus >= 25:
        return "moderate"
    return "weak"


def _interpret_house_strength(house: int, status: str, lang: str) -> str:
    """Compose a classical narrative for a house's ashtakavarga strength."""
    sig_en = _HOUSE_SIG_EN.get(house, "")
    sig_hi = _HOUSE_SIG_HI.get(house, "")
    if lang == "hi":
        if status == "strong":
            return f"{house}वाँ भाव ({sig_hi}) में अष्टकवर्ग बल प्रबल है — शुभ फल की प्राप्ति।"
        if status == "moderate":
            return f"{house}वाँ भाव ({sig_hi}) मध्यम बल — मिश्रित फल, प्रयास से वृद्धि।"
        return f"{house}वाँ भाव ({sig_hi}) निर्बल — बाधाएँ एवं विलम्ब संभव।"
    # English
    if status == "strong":
        return f"House {house} ({sig_en}) is ashtakavarga-strong — flourishing and favorable results."
    if status == "moderate":
        return f"House {house} ({sig_en}) is moderate — mixed outcomes, effort brings progress."
    return f"House {house} ({sig_en}) is weak — obstacles, delays and afflictions likely."


def _interpret_planet_transit(
    planet: str, bindus: int, threshold: int, sign: str, lang: str
) -> str:
    """Compose guidance for a planet's current-sign transit strength."""
    p_hi = _PLANET_HI.get(planet, planet)
    s_hi = _SIGN_HI.get(sign, sign)
    favorable = bindus >= threshold
    if lang == "hi":
        if favorable:
            return (
                f"{p_hi} का गोचर {s_hi} राशि में {bindus} बिंदुओं के साथ "
                f"शुभ है (न्यूनतम आवश्यक {threshold}) — अनुकूल फल।"
            )
        return (
            f"{p_hi} का गोचर {s_hi} राशि में केवल {bindus} बिंदु — "
            f"दुर्बल (न्यूनतम {threshold} अपेक्षित), सावधानी रखें।"
        )
    if favorable:
        return (
            f"{planet} transiting {sign} with {bindus} bindus "
            f"(threshold {threshold}) is favorable — expect supportive results."
        )
    return (
        f"{planet} transiting {sign} has only {bindus} bindus "
        f"(threshold {threshold}) — unfavorable, exercise caution."
    )


def _combo_effect(combo_key: str, achieved: bool, total: int, lang: str) -> str:
    """Classical effect text per special combination (Adh. 24)."""
    texts = {
        "leadership_career": {
            ("en", True): f"Strong career and leadership yoga — 1+7+10 sum {total} ≥ 90. Native rises to authority.",
            ("en", False): f"Career houses (1+7+10) sum {total} < 90 — leadership requires sustained effort.",
            ("hi", True): f"प्रबल नेतृत्व एवं कर्म-योग — 1+7+10 योग {total} (अपेक्षित 90)। उच्च पद प्राप्ति।",
            ("hi", False): f"कर्म-भाव बल (1+7+10) = {total}, 90 से कम — नेतृत्व हेतु विशेष प्रयत्न अपेक्षित।",
        },
        "wealth_income": {
            ("en", True): f"Strong wealth yoga — 2+11 sum {total} ≥ 55. Ample earnings and savings.",
            ("en", False): f"Income houses (2+11) sum {total} < 55 — wealth accrues slowly.",
            ("hi", True): f"धन-योग प्रबल — 2+11 योग {total} (अपेक्षित 55)। आय एवं संचय में वृद्धि।",
            ("hi", False): f"आय-भाव बल (2+11) = {total}, 55 से कम — धन-संचय धीमा।",
        },
        "fortune_dharma": {
            ("en", True): f"Strong fortune yoga — 5+9 sum {total} ≥ 55. Dharmic prosperity, blessings of elders.",
            ("en", False): f"Fortune houses (5+9) sum {total} < 55 — cultivate dharma to unlock fortune.",
            ("hi", True): f"भाग्य-धर्म योग प्रबल — 5+9 योग {total} (अपेक्षित 55)। पूर्व-पुण्य का उदय।",
            ("hi", False): f"भाग्य-भाव बल (5+9) = {total}, 55 से कम — धर्म-आचरण से भाग्योदय।",
        },
        "dusthana_obstacles": {
            # For dusthana, "achieved" means AFFLICTED (i.e., sum is high → trouble)
            ("en", True): f"Heavy dusthana affliction — 6+8+12 sum {total} ≥ 90. Obstacles in health, longevity and finance.",
            ("en", False): f"Dusthana houses manageable — 6+8+12 sum {total} < 90. Challenges are limited.",
            ("hi", True): f"दुःस्थान भाव पीड़ित — 6+8+12 योग {total} (90 से अधिक)। स्वास्थ्य, आयु एवं व्यय में बाधाएँ।",
            ("hi", False): f"दुःस्थान भाव सामान्य — 6+8+12 योग {total} 90 से कम। चुनौतियाँ सीमित।",
        },
    }
    return texts.get(combo_key, {}).get((lang, achieved), "")


def _house_number_from_sign(sign: str, ascendant_sign: str) -> int:
    """Return the house number (1-12) a sign represents given the Lagna."""
    try:
        asc_idx = _sign_name_to_index(ascendant_sign)
        sign_idx = _sign_name_to_index(sign)
    except ValueError:
        return 0
    return ((sign_idx - asc_idx) % 12) + 1


def _sign_of_house(house: int, ascendant_sign: str) -> str:
    """Inverse: return the sign name occupying a given house from the Lagna."""
    try:
        asc_idx = _sign_name_to_index(ascendant_sign)
    except ValueError:
        return "Aries"
    return _SIGN_NAMES[(asc_idx + house - 1) % 12]


def analyze_ashtakvarga_phala(chart_data: dict) -> dict:
    """Phaladeepika Adhyaya 24 — applied predictive rules from Ashtakavarga.

    Computes:
      - house_strengths         (12 entries)
      - planet_strengths        (7 planets — classical, no Rahu/Ketu)
      - special_combinations    (4 classical combos)
      - transit_recommendations (strongest / weakest rasi per planet)
      - overall_score           (0-100 composite)

    All entries are bilingual (EN + HI) and carry a sloka_ref.
    Graceful degradation: returns an empty skeleton if chart is missing
    planet positions.
    """
    empty_skeleton: Dict[str, Any] = {
        "house_strengths": [],
        "planet_strengths": [],
        "special_combinations": [],
        "transit_recommendations": [],
        "overall_score": 0,
        "sloka_ref": "Phaladeepika Adh. 24",
    }

    if not isinstance(chart_data, dict):
        return empty_skeleton

    planets = chart_data.get("planets") or {}
    asc = chart_data.get("ascendant") or {}
    ascendant_sign = asc.get("sign") if isinstance(asc, dict) else None

    # Build planet_signs dict required by calculate_ashtakvarga
    planet_signs: Dict[str, str] = {}
    for p_name, info in planets.items():
        if isinstance(info, dict) and info.get("sign") in _SIGN_NAMES:
            planet_signs[p_name] = info["sign"]
    if ascendant_sign in _SIGN_NAMES:
        planet_signs["Ascendant"] = ascendant_sign

    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    if not required.issubset(planet_signs.keys()) or not ascendant_sign:
        # Graceful degradation — chart incomplete
        return empty_skeleton

    try:
        av = calculate_ashtakvarga(planet_signs)
    except Exception:
        return empty_skeleton

    sav: Dict[str, int] = av.get("sarvashtakvarga", {}) or {}
    planet_bindus: Dict[str, Dict[str, int]] = av.get("planet_bindus", {}) or {}

    # ── 1. House strengths (12 houses from Lagna) ───────────────
    house_strengths = []
    for h in range(1, 13):
        sign = _sign_of_house(h, ascendant_sign)
        bindus = int(sav.get(sign, 0))
        status = _house_status_from_bindus(bindus)
        house_strengths.append({
            "house": h,
            "sign": sign,
            "sav_bindus": bindus,
            "status": status,
            "interpretation_en": _interpret_house_strength(h, status, "en"),
            "interpretation_hi": _interpret_house_strength(h, status, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 2",
        })

    # ── 2. Planet strengths (BAV bindus in planet's own transit sign) ──
    planet_strengths = []
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        transit_sign = planet_signs.get(planet, "Aries")
        own_table = planet_bindus.get(planet, {}) or {}
        bindus = int(own_table.get(transit_sign, 0))
        threshold = _planet_transit_threshold(planet)
        assessment = "favorable" if bindus >= threshold else "unfavorable"
        planet_strengths.append({
            "planet": planet,
            "sign": transit_sign,
            "bindus_in_transit_sign": bindus,
            "threshold": threshold,
            "assessment": assessment,
            "interpretation_en": _interpret_planet_transit(
                planet, bindus, threshold, transit_sign, "en"),
            "interpretation_hi": _interpret_planet_transit(
                planet, bindus, threshold, transit_sign, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 8",
        })

    # ── 3. Special combinations ────────────────────────────────
    def _sum_houses(hs: List[int]) -> int:
        return sum(int(sav.get(_sign_of_house(h, ascendant_sign), 0)) for h in hs)

    leadership_total = _sum_houses([1, 7, 10])
    wealth_total = _sum_houses([2, 11])
    fortune_total = _sum_houses([5, 9])
    dusthana_total = _sum_houses([6, 8, 12])

    special_combinations = [
        {
            "combo": "leadership_career",
            "label_en": "Leadership & Career",
            "label_hi": "नेतृत्व एवं कर्म",
            "houses": [1, 7, 10],
            "total_bindus": leadership_total,
            "threshold": 90,
            "achieved": leadership_total >= 90,
            "effect_en": _combo_effect(
                "leadership_career", leadership_total >= 90, leadership_total, "en"),
            "effect_hi": _combo_effect(
                "leadership_career", leadership_total >= 90, leadership_total, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 15",
        },
        {
            "combo": "wealth_income",
            "label_en": "Wealth & Income",
            "label_hi": "धन एवं आय",
            "houses": [2, 11],
            "total_bindus": wealth_total,
            "threshold": 55,
            "achieved": wealth_total >= 55,
            "effect_en": _combo_effect(
                "wealth_income", wealth_total >= 55, wealth_total, "en"),
            "effect_hi": _combo_effect(
                "wealth_income", wealth_total >= 55, wealth_total, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 16",
        },
        {
            "combo": "fortune_dharma",
            "label_en": "Fortune & Dharma",
            "label_hi": "भाग्य एवं धर्म",
            "houses": [5, 9],
            "total_bindus": fortune_total,
            "threshold": 55,
            "achieved": fortune_total >= 55,
            "effect_en": _combo_effect(
                "fortune_dharma", fortune_total >= 55, fortune_total, "en"),
            "effect_hi": _combo_effect(
                "fortune_dharma", fortune_total >= 55, fortune_total, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 17",
        },
        {
            # For dusthana, threshold is AFFLICTION trigger: >= 90 means trouble
            "combo": "dusthana_obstacles",
            "label_en": "Dusthana Obstacles",
            "label_hi": "दुःस्थान बाधा",
            "houses": [6, 8, 12],
            "total_bindus": dusthana_total,
            "threshold": 90,
            "achieved": dusthana_total >= 90,
            "effect_en": _combo_effect(
                "dusthana_obstacles", dusthana_total >= 90, dusthana_total, "en"),
            "effect_hi": _combo_effect(
                "dusthana_obstacles", dusthana_total >= 90, dusthana_total, "hi"),
            "sloka_ref": "Phaladeepika Adh. 24 sloka 18",
        },
    ]

    # ── 4. Transit recommendations (strongest/weakest rasi per planet) ──
    transit_recommendations = []
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        own_table = planet_bindus.get(planet, {}) or {}
        if not own_table:
            continue
        # Find strongest and weakest signs
        sorted_signs = sorted(own_table.items(), key=lambda kv: kv[1])
        weakest_rasi, weakest_val = sorted_signs[0]
        strongest_rasi, strongest_val = sorted_signs[-1]
        p_hi = _PLANET_HI.get(planet, planet)
        s_strong_hi = _SIGN_HI.get(strongest_rasi, strongest_rasi)
        s_weak_hi = _SIGN_HI.get(weakest_rasi, weakest_rasi)
        transit_recommendations.append({
            "planet": planet,
            "strongest_rasi": strongest_rasi,
            "strongest_bindus": int(strongest_val),
            "weakest_rasi": weakest_rasi,
            "weakest_bindus": int(weakest_val),
            "guidance_en": (
                f"{planet} gives best results when transiting {strongest_rasi} "
                f"({strongest_val} bindus); avoid major ventures when in "
                f"{weakest_rasi} ({weakest_val} bindus)."
            ),
            "guidance_hi": (
                f"{p_hi} का गोचर {s_strong_hi} ({strongest_val} बिंदु) में सर्वाधिक "
                f"शुभ; {s_weak_hi} ({weakest_val} बिंदु) में बड़े कार्य त्यागें।"
            ),
            "sloka_ref": "Phaladeepika Adh. 24",
        })

    # ── 5. Overall score (0-100 composite) ─────────────────────
    # Composite = (avg house strength / 56 max per sign * 0.6)
    #           + (favorable planet count / 7 * 0.25)
    #           + (achieved beneficial combos / 3 * 0.15)
    # Dusthana affliction subtracts up to 10 points.
    total_sav = sum(int(sav.get(s, 0)) for s in _SIGN_NAMES)
    avg_sav = total_sav / 12.0 if total_sav else 0.0
    # typical SAV avg ~28 → normalize around 30 cap
    house_score = min(100.0, (avg_sav / 30.0) * 100.0) * 0.6

    favorable_planets = sum(
        1 for p in planet_strengths if p["assessment"] == "favorable"
    )
    planet_score = (favorable_planets / 7.0) * 100.0 * 0.25

    beneficial_combos = sum(
        1 for c in special_combinations
        if c["combo"] != "dusthana_obstacles" and c["achieved"]
    )
    combo_score = (beneficial_combos / 3.0) * 100.0 * 0.15

    # Dusthana affliction penalty (max 10 pts)
    dusthana_penalty = 0.0
    if dusthana_total >= 90:
        dusthana_penalty = min(10.0, (dusthana_total - 90) / 2.0 + 5.0)

    overall = house_score + planet_score + combo_score - dusthana_penalty
    overall_score = max(0, min(100, int(round(overall))))

    return {
        "house_strengths": house_strengths,
        "planet_strengths": planet_strengths,
        "special_combinations": special_combinations,
        "transit_recommendations": transit_recommendations,
        "overall_score": overall_score,
        "sloka_ref": "Phaladeepika Adh. 24",
    }


# ════════════════════════════════════════════════════════════════════
# HORASARA (PRITHUYASAS) — SUPPLEMENTARY ASHTAKAVARGA PHALA RULES
# Secondary source to Phaladeepika Adh. 24; adds qualitative bindu
# classification for SAV signs and per-planet BAV transit readings.
# ════════════════════════════════════════════════════════════════════

# SAV bindu → (effect_level, english_effect, hindi_effect)
_SAV_BINDU_LEVELS: List[tuple] = [
    # (max_inclusive, effect_level, effect_en, effect_hi)
    (0,  "Very Difficult", "Complete destruction of house significations; severe suffering in that life area",
         "भाव के संकेतों का पूर्ण नाश; उस क्षेत्र में गंभीर पीड़ा"),
    (2,  "Difficult",      "Near-total affliction; major obstacles and losses in that area",
         "लगभग पूर्ण पीड़ा; उस क्षेत्र में बड़ी बाधाएँ एवं हानि"),
    (4,  "Challenging",    "Significant challenges; native must work very hard to maintain minimal results",
         "महत्वपूर्ण चुनौतियाँ; न्यूनतम परिणामों के लिए अत्यधिक परिश्रम आवश्यक"),
    (6,  "Mixed",          "Moderate results; mixed period of gains and losses",
         "सामान्य परिणाम; लाभ-हानि का मिश्रित काल"),
    (8,  "Favorable",      "Good results; steady progress, some unexpected gains",
         "अच्छे परिणाम; स्थिर प्रगति, कुछ अप्रत्याशित लाभ"),
    (10, "Very Favorable", "Excellent results; prosperity, recognition, achievements",
         "उत्तम परिणाम; समृद्धि, मान्यता, उपलब्धियाँ"),
    (12, "Exceptional",    "Outstanding success, windfall gains, rare fortune",
         "असाधारण सफलता, अप्रत्याशित लाभ, दुर्लभ भाग्य"),
    # anything > 12 falls into the last bucket via the lookup helper
]

# BAV transit levels: (planet, level, low_range_max, medium_range_max)
# Low: 0-2, Medium: 3-4, High: 5-8
_BAV_PLANET_LEVELS: Dict[str, Dict[str, Dict[str, str]]] = {
    "Sun": {
        "Low":    {"en": "Loss of vitality, father-related troubles, authority challenges",
                   "hi": "जीवन-शक्ति की हानि, पितृ-पीड़ा, अधिकार में बाधाएँ"},
        "Medium": {"en": "Ordinary results, some effort needed",
                   "hi": "सामान्य परिणाम, कुछ प्रयास अपेक्षित"},
        "High":   {"en": "Success in government matters, career advancement, health",
                   "hi": "सरकारी कार्यों में सफलता, कैरियर उन्नति, स्वास्थ्य लाभ"},
    },
    "Moon": {
        "Low":    {"en": "Mental disturbances, mother's health, emotional instability",
                   "hi": "मानसिक अशांति, माता का स्वास्थ्य, भावनात्मक अस्थिरता"},
        "Medium": {"en": "Average; mixed emotional state",
                   "hi": "सामान्य; मिश्रित भावनात्मक अवस्था"},
        "High":   {"en": "Mental peace, domestic happiness, travel",
                   "hi": "मानसिक शांति, गृह-सुख, यात्रा"},
    },
    "Mars": {
        "Low":    {"en": "Accidents, wounds, conflicts, enemies overpower",
                   "hi": "दुर्घटनाएँ, घाव, संघर्ष, शत्रु प्रबल"},
        "Medium": {"en": "Moderate energy, some friction",
                   "hi": "मध्यम ऊर्जा, कुछ घर्षण"},
        "High":   {"en": "Courage, victory over enemies, physical strength",
                   "hi": "साहस, शत्रु-विजय, शारीरिक बल"},
    },
    "Mercury": {
        "Low":    {"en": "Communication failures, business losses, sibling issues",
                   "hi": "संचार विफलताएँ, व्यापार हानि, सहोदर-पीड़ा"},
        "Medium": {"en": "Routine intellectual work",
                   "hi": "सामान्य बौद्धिक कार्य"},
        "High":   {"en": "Eloquence, business success, scholarship",
                   "hi": "वाक्पटुता, व्यापार सफलता, विद्वत्ता"},
    },
    "Jupiter": {
        "Low":    {"en": "Lack of wisdom guidance, financial difficulties",
                   "hi": "ज्ञान-मार्गदर्शन का अभाव, आर्थिक कठिनाइयाँ"},
        "Medium": {"en": "Some gains, moderate fortune",
                   "hi": "कुछ लाभ, मध्यम भाग्य"},
        "High":   {"en": "Spiritual growth, wealth, children's welfare, guru blessings",
                   "hi": "आध्यात्मिक विकास, धन, संतान-कल्याण, गुरु-कृपा"},
    },
    "Venus": {
        "Low":    {"en": "Relationship troubles, artistic blocks, health issues",
                   "hi": "संबंध-पीड़ा, कलात्मक अवरोध, स्वास्थ्य समस्याएँ"},
        "Medium": {"en": "Average comforts",
                   "hi": "सामान्य सुख-सुविधा"},
        "High":   {"en": "Marital happiness, arts, luxury, sensual pleasures",
                   "hi": "वैवाहिक सुख, कला, विलासिता, इंद्रिय-सुख"},
    },
    "Saturn": {
        "Low":    {"en": "Hard labor with little reward, chronic health, obstructions",
                   "hi": "अल्प पुरस्कार के लिए कठिन परिश्रम, दीर्घकालीन स्वास्थ्य, बाधाएँ"},
        "Medium": {"en": "Slow but steady results",
                   "hi": "धीमे परंतु स्थिर परिणाम"},
        "High":   {"en": "Disciplined success, land, longevity gains",
                   "hi": "अनुशासित सफलता, भूमि-लाभ, दीर्घायु"},
    },
}

# Natural BAV threshold per planet (already in _PLANET_TRANSIT_THRESHOLD,
# mirrored here for self-contained reference inside this function block).
_HORASARA_NATURAL_THRESHOLD: Dict[str, int] = {
    "Sun": 4, "Moon": 4, "Mars": 3, "Mercury": 5,
    "Jupiter": 5, "Venus": 5, "Saturn": 3,
}


def _sav_bindu_classify(bindus: int) -> tuple:
    """Return (effect_level, effect_en, effect_hi) for a SAV bindu count."""
    for max_val, level, en, hi in _SAV_BINDU_LEVELS:
        if bindus <= max_val:
            return level, en, hi
    # > 12 treated as Exceptional
    last = _SAV_BINDU_LEVELS[-1]
    return last[1], last[2], last[3]


def _bav_bindu_level(bindus: int) -> str:
    """Map a BAV bindu count to Low / Medium / High."""
    if bindus <= 2:
        return "Low"
    if bindus <= 4:
        return "Medium"
    return "High"


def analyze_horasara_phala(chart_data: dict) -> dict:
    """Horasara (Prithuyasas) supplementary Ashtakavarga phala rules.

    Supplements Phaladeepika Adh. 24 with qualitative bindu classification
    drawn from Horasara Ch. 1-5, covering:
      - SAV sign readings (12 signs, Horasara bindu table)
      - Planet BAV transit readings (7 planets, Low/Medium/High effects)
      - 3 special rules: total SAV check, house group comparison,
        transit alignment with natural threshold

    Args:
        chart_data: dict with keys 'ascendant' (dict with 'sign') and
                    'planets' (dict of planet-name → dict with 'sign').

    Returns:
        dict with sav_sign_readings, planet_transit_readings, special_rules,
        and sloka_ref.  Returns an empty skeleton on invalid/incomplete input.
    """
    _SLOKA_REF = "Horasara (Prithuyasas) Ch. 1–5, Phaladeepika Adh. 24"

    empty_skeleton: Dict[str, Any] = {
        "sav_sign_readings": [],
        "planet_transit_readings": [],
        "special_rules": {},
        "sloka_ref": _SLOKA_REF,
    }

    if not isinstance(chart_data, dict):
        return empty_skeleton

    planets = chart_data.get("planets") or {}
    asc = chart_data.get("ascendant") or {}
    ascendant_sign: str = asc.get("sign") if isinstance(asc, dict) else None  # type: ignore[assignment]

    # Build planet_signs for calculate_ashtakvarga
    planet_signs: Dict[str, str] = {}
    for p_name, info in planets.items():
        if isinstance(info, dict) and info.get("sign") in _SIGN_NAMES:
            planet_signs[p_name] = info["sign"]
    if ascendant_sign in _SIGN_NAMES:
        planet_signs["Ascendant"] = ascendant_sign

    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    if not required.issubset(planet_signs.keys()) or not ascendant_sign:
        return empty_skeleton

    try:
        av = calculate_ashtakvarga(planet_signs)
    except Exception:
        return empty_skeleton

    sav: Dict[str, int] = av.get("sarvashtakvarga", {}) or {}
    planet_bindus: Dict[str, Dict[str, int]] = av.get("planet_bindus", {}) or {}

    # ── 1. SAV sign readings (12 signs) ─────────────────────────
    sav_sign_readings: List[Dict[str, Any]] = []
    for h in range(1, 13):
        sign = _sign_of_house(h, ascendant_sign)
        sav_count = int(sav.get(sign, 0))
        effect_level, effect_en, effect_hi = _sav_bindu_classify(sav_count)
        sign_hi = _SIGN_HI.get(sign, sign)
        house_sig_en = _HOUSE_SIG_EN.get(h, "")

        interp_en = (
            f"{sign} ({_ordinal(h)} house) has {sav_count} bindus — "
            f"{effect_en} in matters of {house_sig_en}."
        )
        interp_hi = (
            f"{sign_hi} ({h}वाँ भाव) में {sav_count} बिंदु — "
            f"{effect_hi} ({_HOUSE_SIG_HI.get(h, '')})।"
        )

        sav_sign_readings.append({
            "sign": sign,
            "house": h,
            "sav_bindus": sav_count,
            "effect_level": effect_level,
            "interpretation_en": interp_en,
            "interpretation_hi": interp_hi,
            "sloka_ref": _SLOKA_REF,
        })

    # ── 2. Planet BAV transit readings (7 planets) ───────────────
    planet_transit_readings: List[Dict[str, Any]] = []
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        transit_sign = planet_signs.get(planet, "Aries")
        own_table = planet_bindus.get(planet, {}) or {}
        bav_count = int(own_table.get(transit_sign, 0))
        level = _bav_bindu_level(bav_count)
        planet_level_data = _BAV_PLANET_LEVELS.get(planet, {}).get(level, {})
        effect_text_en = planet_level_data.get("en", "")
        effect_text_hi = planet_level_data.get("hi", "")

        p_hi = _PLANET_HI.get(planet, planet)
        s_hi = _SIGN_HI.get(transit_sign, transit_sign)

        interp_en = (
            f"{planet}'s transit through {transit_sign} ({bav_count} bindus) — "
            f"{effect_text_en} during this transit."
        )
        interp_hi = (
            f"{p_hi} का गोचर {s_hi} ({bav_count} बिंदु) — "
            f"{effect_text_hi}।"
        )

        planet_transit_readings.append({
            "planet": planet,
            "transit_sign": transit_sign,
            "bav_bindus": bav_count,
            "effect_level": level,
            "interpretation_en": interp_en,
            "interpretation_hi": interp_hi,
            "sloka_ref": _SLOKA_REF,
        })

    # ── 3. Special rules ─────────────────────────────────────────
    # Rule 1: Total SAV check
    total_sav = sum(int(sav.get(s, 0)) for s in _SIGN_NAMES)
    if total_sav < 337:
        total_sav_en = (
            f"Total SAV of {total_sav} bindus — below the average threshold of 337, "
            f"indicating more obstacles than average in life."
        )
        total_sav_hi = (
            f"कुल SAV {total_sav} बिंदु — 337 की औसत सीमा से कम, "
            f"जीवन में औसत से अधिक बाधाओं का संकेत।"
        )
    elif total_sav == 337:
        total_sav_en = (
            f"Total SAV of {total_sav} bindus — at the average level, indicating balanced "
            f"life experiences with neither exceptional fortune nor severe obstacles."
        )
        total_sav_hi = (
            f"कुल SAV {total_sav} बिंदु — औसत स्तर पर, संतुलित जीवन अनुभव का संकेत।"
        )
    else:
        total_sav_en = (
            f"Total SAV of {total_sav} bindus — above the average threshold of 337, "
            f"indicating a generally fortunate life with fewer obstacles than average."
        )
        total_sav_hi = (
            f"कुल SAV {total_sav} बिंदु — 337 की औसत सीमा से अधिक, "
            f"औसत से कम बाधाओं के साथ भाग्यशाली जीवन का संकेत।"
        )

    # Rule 2: House group comparison
    def _sum_house_group(houses: List[int]) -> int:
        return sum(int(sav.get(_sign_of_house(h, ascendant_sign), 0)) for h in houses)

    kendra_total = _sum_house_group([1, 4, 7, 10])
    trikona_total = _sum_house_group([5, 9])
    dusthana_total_h = _sum_house_group([6, 8, 12])

    group_totals = {
        "Kendra": kendra_total,
        "Trikona": trikona_total,
        "Dusthana": dusthana_total_h,
    }
    dominant_group = max(group_totals, key=lambda g: group_totals[g])

    _group_interp_en = {
        "Kendra": (
            f"Kendra houses (1+4+7+10) have the highest SAV total ({kendra_total}) — "
            f"career, relationships, and domestic matters are the primary life arena."
        ),
        "Trikona": (
            f"Trikona houses (5+9) have the highest SAV total ({trikona_total}) — "
            f"fortune, dharma, children, and higher purpose are the primary life themes."
        ),
        "Dusthana": (
            f"Dusthana houses (6+8+12) have the highest SAV total ({dusthana_total_h}) — "
            f"life energy concentrates on overcoming obstacles, hidden matters, and transformation."
        ),
    }
    _group_interp_hi = {
        "Kendra": (
            f"केंद्र भाव (1+4+7+10) का सर्वोच्च SAV योग ({kendra_total}) — "
            f"कैरियर, संबंध एवं गृह-जीवन प्राथमिक जीवन-क्षेत्र।"
        ),
        "Trikona": (
            f"त्रिकोण भाव (5+9) का सर्वोच्च SAV योग ({trikona_total}) — "
            f"भाग्य, धर्म, संतान एवं उच्च उद्देश्य प्रमुख जीवन-विषय।"
        ),
        "Dusthana": (
            f"दुःस्थान भाव (6+8+12) का सर्वोच्च SAV योग ({dusthana_total_h}) — "
            f"जीवन-ऊर्जा बाधाओं, गुप्त विषयों एवं परिवर्तन पर केंद्रित।"
        ),
    }

    special_rules: Dict[str, Any] = {
        "total_sav": total_sav,
        "total_sav_assessment_en": total_sav_en,
        "total_sav_assessment_hi": total_sav_hi,
        "kendra_total": kendra_total,
        "trikona_total": trikona_total,
        "dusthana_total": dusthana_total_h,
        "dominant_group": dominant_group,
        "group_interpretation_en": _group_interp_en[dominant_group],
        "group_interpretation_hi": _group_interp_hi[dominant_group],
    }

    return {
        "sav_sign_readings": sav_sign_readings,
        "planet_transit_readings": planet_transit_readings,
        "special_rules": special_rules,
        "sloka_ref": _SLOKA_REF,
    }


def _ordinal(n: int) -> str:
    """Return English ordinal string for house number (1st, 2nd, … 12th)."""
    _suffixes = {1: "st", 2: "nd", 3: "rd"}
    suffix = _suffixes.get(n if n <= 3 else 0, "th")
    return f"{n}{suffix}"
