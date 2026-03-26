"""
matching_engine.py — Kundli Gun Milan (Ashtakoota) Matching Engine
===================================================================
Calculates compatibility score between two horoscopes based on
8 Koots (Ashtakoota) with max 36 points (Gun Milan).
"""

# ============================================================
# CONSTANTS
# ============================================================

# 8 Koots with max points
GUN_MILAN_KOOTS = {
    "Varna": {"max": 1, "description": "Spiritual compatibility (caste/ego level)"},
    "Vasya": {"max": 2, "description": "Mutual attraction and dominance"},
    "Tara": {"max": 3, "description": "Birth star compatibility (health/destiny)"},
    "Yoni": {"max": 4, "description": "Sexual and physical compatibility"},
    "Graha Maitri": {"max": 5, "description": "Planetary friendship (mental compatibility)"},
    "Gana": {"max": 6, "description": "Temperament compatibility (Deva/Manushya/Rakshasa)"},
    "Bhakoot": {"max": 7, "description": "Emotional and financial compatibility"},
    "Nadi": {"max": 8, "description": "Health and genetic compatibility"},
}

GUN_MILAN_TOTAL = 36  # sum of all max points

# 27 Nakshatras with their properties for matching
# Each nakshatra: {varna, vasya, tara_group, yoni, graha_lord, gana, rashi, nadi}
NAKSHATRA_DATA = {
    "Ashwini":          {"varna": "Vaishya",    "vasya": "Horse",    "yoni": "Horse",     "gana": "Deva",      "lord": "Ketu",    "rashi": "Aries",       "nadi": "Aadi"},
    "Bharani":          {"varna": "Shudra",     "vasya": "Elephant", "yoni": "Elephant",  "gana": "Manushya",  "lord": "Venus",   "rashi": "Aries",       "nadi": "Madhya"},
    "Krittika":         {"varna": "Brahmin",    "vasya": "Goat",     "yoni": "Goat",      "gana": "Rakshasa",  "lord": "Sun",     "rashi": "Taurus",      "nadi": "Antya"},
    "Rohini":           {"varna": "Shudra",     "vasya": "Serpent",  "yoni": "Serpent",   "gana": "Manushya",  "lord": "Moon",    "rashi": "Taurus",      "nadi": "Antya"},
    "Mrigashira":       {"varna": "Vaishya",    "vasya": "Serpent",  "yoni": "Serpent",   "gana": "Deva",      "lord": "Mars",    "rashi": "Gemini",      "nadi": "Aadi"},
    "Ardra":            {"varna": "Shudra",     "vasya": "Dog",      "yoni": "Dog",       "gana": "Manushya",  "lord": "Rahu",    "rashi": "Gemini",      "nadi": "Madhya"},
    "Punarvasu":        {"varna": "Vaishya",    "vasya": "Cat",      "yoni": "Cat",       "gana": "Deva",      "lord": "Jupiter", "rashi": "Cancer",      "nadi": "Antya"},
    "Pushya":           {"varna": "Kshatriya",  "vasya": "Goat",     "yoni": "Goat",      "gana": "Deva",      "lord": "Saturn",  "rashi": "Cancer",      "nadi": "Aadi"},
    "Ashlesha":         {"varna": "Shudra",     "vasya": "Cat",      "yoni": "Cat",       "gana": "Rakshasa",  "lord": "Mercury", "rashi": "Cancer",      "nadi": "Madhya"},
    "Magha":            {"varna": "Shudra",     "vasya": "Rat",      "yoni": "Rat",       "gana": "Rakshasa",  "lord": "Ketu",    "rashi": "Leo",         "nadi": "Antya"},
    "Purva Phalguni":   {"varna": "Brahmin",    "vasya": "Rat",      "yoni": "Rat",       "gana": "Manushya",  "lord": "Venus",   "rashi": "Leo",         "nadi": "Aadi"},
    "Uttara Phalguni":  {"varna": "Kshatriya",  "vasya": "Cow",      "yoni": "Cow",       "gana": "Manushya",  "lord": "Sun",     "rashi": "Virgo",       "nadi": "Madhya"},
    "Hasta":            {"varna": "Vaishya",    "vasya": "Buffalo",  "yoni": "Buffalo",   "gana": "Deva",      "lord": "Moon",    "rashi": "Virgo",       "nadi": "Antya"},
    "Chitra":           {"varna": "Shudra",     "vasya": "Tiger",    "yoni": "Tiger",     "gana": "Rakshasa",  "lord": "Mars",    "rashi": "Libra",       "nadi": "Aadi"},
    "Swati":            {"varna": "Brahmin",    "vasya": "Buffalo",  "yoni": "Buffalo",   "gana": "Deva",      "lord": "Rahu",    "rashi": "Libra",       "nadi": "Madhya"},
    "Vishakha":         {"varna": "Brahmin",    "vasya": "Tiger",    "yoni": "Tiger",     "gana": "Rakshasa",  "lord": "Jupiter", "rashi": "Scorpio",     "nadi": "Antya"},
    "Anuradha":         {"varna": "Shudra",     "vasya": "Deer",     "yoni": "Deer",      "gana": "Deva",      "lord": "Saturn",  "rashi": "Scorpio",     "nadi": "Aadi"},
    "Jyeshtha":         {"varna": "Vaishya",    "vasya": "Deer",     "yoni": "Deer",      "gana": "Rakshasa",  "lord": "Mercury", "rashi": "Scorpio",     "nadi": "Madhya"},
    "Mula":             {"varna": "Shudra",     "vasya": "Dog",      "yoni": "Dog",       "gana": "Rakshasa",  "lord": "Ketu",    "rashi": "Sagittarius", "nadi": "Antya"},
    "Purva Ashadha":    {"varna": "Brahmin",    "vasya": "Monkey",   "yoni": "Monkey",    "gana": "Manushya",  "lord": "Venus",   "rashi": "Sagittarius", "nadi": "Aadi"},
    "Uttara Ashadha":   {"varna": "Kshatriya",  "vasya": "Mongoose", "yoni": "Mongoose",  "gana": "Manushya",  "lord": "Sun",     "rashi": "Capricorn",   "nadi": "Madhya"},
    "Shravana":         {"varna": "Vaishya",    "vasya": "Monkey",   "yoni": "Monkey",    "gana": "Deva",      "lord": "Moon",    "rashi": "Capricorn",   "nadi": "Antya"},
    "Dhanishta":        {"varna": "Vaishya",    "vasya": "Lion",     "yoni": "Lion",      "gana": "Rakshasa",  "lord": "Mars",    "rashi": "Aquarius",    "nadi": "Aadi"},
    "Shatabhisha":      {"varna": "Shudra",     "vasya": "Horse",    "yoni": "Horse",     "gana": "Rakshasa",  "lord": "Rahu",    "rashi": "Aquarius",    "nadi": "Madhya"},
    "Purva Bhadrapada": {"varna": "Brahmin",    "vasya": "Lion",     "yoni": "Lion",      "gana": "Manushya",  "lord": "Jupiter", "rashi": "Pisces",      "nadi": "Antya"},
    "Uttara Bhadrapada":{"varna": "Kshatriya",  "vasya": "Cow",      "yoni": "Cow",       "gana": "Manushya",  "lord": "Saturn",  "rashi": "Pisces",      "nadi": "Aadi"},
    "Revati":           {"varna": "Shudra",     "vasya": "Elephant", "yoni": "Elephant",  "gana": "Deva",      "lord": "Mercury", "rashi": "Pisces",      "nadi": "Madhya"},
}

# Varna hierarchy (higher can match with same or lower)
VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}

# Planetary friendship for Graha Maitri
PLANET_FRIENDS = {
    "Sun":     {"friends": {"Moon", "Mars", "Jupiter"}, "enemies": {"Venus", "Saturn"}, "neutral": {"Mercury", "Rahu", "Ketu"}},
    "Moon":    {"friends": {"Sun", "Mercury"}, "enemies": set(), "neutral": {"Mars", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}},
    "Mars":    {"friends": {"Sun", "Moon", "Jupiter"}, "enemies": {"Mercury"}, "neutral": {"Venus", "Saturn", "Rahu", "Ketu"}},
    "Mercury": {"friends": {"Sun", "Venus"}, "enemies": {"Moon"}, "neutral": {"Mars", "Jupiter", "Saturn", "Rahu", "Ketu"}},
    "Jupiter": {"friends": {"Sun", "Moon", "Mars"}, "enemies": {"Mercury", "Venus"}, "neutral": {"Saturn", "Rahu", "Ketu"}},
    "Venus":   {"friends": {"Mercury", "Saturn"}, "enemies": {"Sun", "Moon"}, "neutral": {"Mars", "Jupiter", "Rahu", "Ketu"}},
    "Saturn":  {"friends": {"Mercury", "Venus"}, "enemies": {"Sun", "Moon", "Mars"}, "neutral": {"Jupiter", "Rahu", "Ketu"}},
    "Rahu":    {"friends": {"Mercury", "Venus", "Saturn"}, "enemies": {"Sun", "Moon", "Mars"}, "neutral": {"Jupiter", "Ketu"}},
    "Ketu":    {"friends": {"Mars", "Jupiter"}, "enemies": {"Venus", "Mercury"}, "neutral": {"Sun", "Moon", "Saturn", "Rahu"}},
}

# Yoni compatibility: same animal = 4, friendly = 3, neutral = 2, enemy = 1, sworn enemy = 0
YONI_ENEMIES = {
    frozenset({"Horse", "Buffalo"}),
    frozenset({"Elephant", "Lion"}),
    frozenset({"Dog", "Deer"}),
    frozenset({"Serpent", "Mongoose"}),
    frozenset({"Cat", "Rat"}),
    frozenset({"Monkey", "Goat"}),
    frozenset({"Tiger", "Cow"}),
}

# Gana compatibility matrix
# Deva-Deva=3, Deva-Manushya=2, Deva-Rakshasa=1, Manushya-Manushya=3, Manushya-Rakshasa=0, Rakshasa-Rakshasa=3
GANA_SCORE = {
    ("Deva", "Deva"): 6,
    ("Deva", "Manushya"): 3,
    ("Manushya", "Deva"): 3,
    ("Deva", "Rakshasa"): 1,
    ("Rakshasa", "Deva"): 1,
    ("Manushya", "Manushya"): 6,
    ("Manushya", "Rakshasa"): 0,
    ("Rakshasa", "Manushya"): 0,
    ("Rakshasa", "Rakshasa"): 6,
}

# Rashi index for Bhakoot calculation
RASHI_INDEX = {
    "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
    "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
    "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12,
}

# Bhakoot unfavorable combinations (ratio from person1 rashi to person2 rashi)
# These ratios produce 0 points: 2/12, 5/9, 6/8
BHAKOOT_BAD_RATIOS = {(2, 12), (12, 2), (5, 9), (9, 5), (6, 8), (8, 6)}


# ============================================================
# SCORING FUNCTIONS
# ============================================================

def _score_varna(n1: dict, n2: dict) -> tuple:
    """Varna koot: groom's varna should be >= bride's. Max 1 point."""
    r1 = VARNA_RANK.get(n1["varna"], 0)
    r2 = VARNA_RANK.get(n2["varna"], 0)
    score = 1 if r1 >= r2 else 0
    return score, "Spiritual ego compatibility — groom's varna is equal or higher." if score else "Varna mismatch — groom's spiritual rank is lower."


def _score_vasya(n1: dict, n2: dict) -> tuple:
    """Vasya koot: mutual influence/attraction. Max 2 points."""
    if n1["vasya"] == n2["vasya"]:
        return 2, "Same vasya group — strong mutual attraction."
    # Simplified: different vasya = 1 if not sworn enemies, else 0
    pair = frozenset({n1["vasya"], n2["vasya"]})
    if pair in YONI_ENEMIES:
        return 0, "Vasya groups are incompatible — dominance conflict."
    return 1, "Partial vasya compatibility — moderate mutual influence."


def _score_tara(n1: dict, n2: dict) -> tuple:
    """Tara koot: based on nakshatra number positions. Max 3 points."""
    naks = list(NAKSHATRA_DATA.keys())
    try:
        idx1 = naks.index(next(k for k in naks if k == list(NAKSHATRA_DATA.keys())[naks.index(k)]))
        idx2 = naks.index(next(k for k in naks if k == list(NAKSHATRA_DATA.keys())[naks.index(k)]))
        # Find actual indices
        nak_names = list(NAKSHATRA_DATA.keys())
        i1 = nak_names.index(n1["_name"])
        i2 = nak_names.index(n2["_name"])
    except (ValueError, KeyError):
        return 1, "Tara calculation: moderate compatibility."

    # Tara = (target_nak - source_nak) % 9
    tara_val = ((i2 - i1) % 9) + 1  # 1-9 cycle
    # Favorable taras: 1 (Janma), 2 (Sampat), 4 (Kshema), 6 (Sadhana), 8 (Mitra)
    favorable = {1, 2, 4, 6, 8}
    if tara_val in favorable:
        return 3, f"Tara {tara_val} — favorable birth star relationship."
    elif tara_val in {3, 5}:
        return 1, f"Tara {tara_val} — mildly unfavorable birth star relationship."
    else:  # 7 (Vadha), 9 (Pratyari)
        return 0, f"Tara {tara_val} — unfavorable birth star relationship."


def _score_yoni(n1: dict, n2: dict) -> tuple:
    """Yoni koot: sexual/physical compatibility. Max 4 points."""
    y1, y2 = n1["yoni"], n2["yoni"]
    if y1 == y2:
        return 4, f"Same yoni ({y1}) — excellent physical compatibility."
    pair = frozenset({y1, y2})
    if pair in YONI_ENEMIES:
        return 0, f"Enemy yoni ({y1} vs {y2}) — significant physical incompatibility."
    # Neutral or friendly
    return 2, f"Neutral yoni ({y1} vs {y2}) — moderate physical compatibility."


def _score_graha_maitri(n1: dict, n2: dict) -> tuple:
    """Graha Maitri koot: planetary lord friendship. Max 5 points."""
    lord1, lord2 = n1["lord"], n2["lord"]
    if lord1 == lord2:
        return 5, f"Same nakshatra lord ({lord1}) — excellent mental compatibility."

    rel1 = PLANET_FRIENDS.get(lord1, {})
    rel2 = PLANET_FRIENDS.get(lord2, {})

    mutual_friend = lord2 in rel1.get("friends", set()) and lord1 in rel2.get("friends", set())
    one_friend = lord2 in rel1.get("friends", set()) or lord1 in rel2.get("friends", set())
    mutual_enemy = lord2 in rel1.get("enemies", set()) and lord1 in rel2.get("enemies", set())

    if mutual_friend:
        return 5, f"Mutual planetary friendship ({lord1} & {lord2}) — strong mental bond."
    elif one_friend:
        return 3, f"One-sided planetary friendship ({lord1} & {lord2}) — moderate mental bond."
    elif mutual_enemy:
        return 0, f"Mutual planetary enmity ({lord1} & {lord2}) — mental friction likely."
    else:
        return 2, f"Neutral planetary relationship ({lord1} & {lord2}) — average mental compatibility."


def _score_gana(n1: dict, n2: dict) -> tuple:
    """Gana koot: temperament compatibility. Max 3 points."""
    g1, g2 = n1["gana"], n2["gana"]
    score = GANA_SCORE.get((g1, g2), 1)
    if score == 3:
        desc = f"Same or compatible gana ({g1} & {g2}) — harmonious temperaments."
    elif score == 0:
        desc = f"Incompatible gana ({g1} & {g2}) — temperament clash likely."
    else:
        desc = f"Partially compatible gana ({g1} & {g2}) — manageable differences."
    return score, desc


def _score_bhakoot(n1: dict, n2: dict) -> tuple:
    """Bhakoot koot: rashi-based emotional/financial compatibility. Max 7 points."""
    r1 = RASHI_INDEX.get(n1["rashi"], 0)
    r2 = RASHI_INDEX.get(n2["rashi"], 0)

    if r1 == 0 or r2 == 0:
        return 3, "Unable to determine Bhakoot — partial score assigned."

    diff_forward = ((r2 - r1) % 12) + 1 if ((r2 - r1) % 12) != 0 else 12
    diff_backward = ((r1 - r2) % 12) + 1 if ((r1 - r2) % 12) != 0 else 12

    # Check if the ratio is unfavorable
    if (diff_forward, diff_backward) in BHAKOOT_BAD_RATIOS:
        return 0, f"Bhakoot dosha ({diff_forward}/{diff_backward} ratio) — emotional/financial challenges."
    return 7, f"Favorable Bhakoot ({diff_forward}/{diff_backward}) — good emotional and financial harmony."


def _score_nadi(n1: dict, n2: dict) -> tuple:
    """Nadi koot: health and genetic compatibility. Max 8 points."""
    nd1, nd2 = n1["nadi"], n2["nadi"]
    if nd1 == nd2:
        return 0, f"Same Nadi ({nd1}) — Nadi Dosha! Health and progeny concerns. This is the most critical mismatch."
    return 8, f"Different Nadi ({nd1} vs {nd2}) — excellent health and genetic compatibility."


# ============================================================
# MAIN FUNCTION
# ============================================================

def calculate_gun_milan(person1_moon_nakshatra: str, person2_moon_nakshatra: str) -> dict:
    """
    Calculate Ashtakoota Gun Milan compatibility score.

    Args:
        person1_moon_nakshatra: Moon nakshatra of person 1 (groom)
        person2_moon_nakshatra: Moon nakshatra of person 2 (bride)

    Returns:
        {
            total_score: int (out of 36),
            koot_scores: {koot_name: {score, max, description}},
            compatibility_percentage: float,
            recommendation: str,
        }
    """
    if person1_moon_nakshatra not in NAKSHATRA_DATA:
        return {
            "total_score": 0,
            "koot_scores": {},
            "compatibility_percentage": 0.0,
            "recommendation": f"Unknown nakshatra: {person1_moon_nakshatra}",
            "error": f"Unknown nakshatra: {person1_moon_nakshatra}",
        }

    if person2_moon_nakshatra not in NAKSHATRA_DATA:
        return {
            "total_score": 0,
            "koot_scores": {},
            "compatibility_percentage": 0.0,
            "recommendation": f"Unknown nakshatra: {person2_moon_nakshatra}",
            "error": f"Unknown nakshatra: {person2_moon_nakshatra}",
        }

    n1 = {**NAKSHATRA_DATA[person1_moon_nakshatra], "_name": person1_moon_nakshatra}
    n2 = {**NAKSHATRA_DATA[person2_moon_nakshatra], "_name": person2_moon_nakshatra}

    # Score each koot
    scorers = [
        ("Varna", _score_varna),
        ("Vasya", _score_vasya),
        ("Tara", _score_tara),
        ("Yoni", _score_yoni),
        ("Graha Maitri", _score_graha_maitri),
        ("Gana", _score_gana),
        ("Bhakoot", _score_bhakoot),
        ("Nadi", _score_nadi),
    ]

    koot_scores = {}
    total = 0
    for koot_name, scorer in scorers:
        score, desc = scorer(n1, n2)
        max_pts = GUN_MILAN_KOOTS[koot_name]["max"]
        # Clamp score to max
        score = min(score, max_pts)
        koot_scores[koot_name] = {
            "score": score,
            "max": max_pts,
            "description": desc,
        }
        total += score

    pct = round((total / GUN_MILAN_TOTAL) * 100, 1)

    if total >= 30:
        recommendation = "Exceptional match"
    elif total >= 24:
        recommendation = "Excellent match"
    elif total >= 18:
        recommendation = "Good match"
    else:
        recommendation = "Not recommended"

    return {
        "total_score": total,
        "koot_scores": koot_scores,
        "compatibility_percentage": pct,
        "recommendation": recommendation,
    }
