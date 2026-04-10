"""
matching_engine.py — Kundli Gun Milan (Ashtakoota) Matching Engine
===================================================================
Calculates compatibility score between two horoscopes based on
8 Koots (Ashtakoota) with max 36 points (Gun Milan).
"""

import logging

logger = logging.getLogger(__name__)

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

# Gana compatibility matrix (max 6 points)
# Same=6, Compatible (Deva-Manushya)=5, Opposite (Manushya-Rakshasa)=0
GANA_SCORE = {
    ("Deva", "Deva"): 6,
    ("Deva", "Manushya"): 5,
    ("Manushya", "Deva"): 5,
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

# Vasya groups based on Moon Rashi (NOT yoni animals)
VASYA_BY_RASHI = {
    "Aries": "Chatushpada", "Taurus": "Chatushpada", "Gemini": "Manava",
    "Cancer": "Jalchar", "Leo": "Vanchar", "Virgo": "Manava",
    "Libra": "Manava", "Scorpio": "Keeta", "Sagittarius": "Manava",
    "Capricorn": "Chatushpada", "Aquarius": "Manava", "Pisces": "Jalchar",
}

# Yoni friendly pairs (score 3)
YONI_FRIENDS = {
    frozenset({"Horse", "Cow"}), frozenset({"Elephant", "Goat"}),
    frozenset({"Dog", "Cat"}), frozenset({"Serpent", "Deer"}),
    frozenset({"Monkey", "Lion"}), frozenset({"Buffalo", "Tiger"}),
    frozenset({"Rat", "Mongoose"}),
}

# Rashi lords for dosha cancellation checks
RASHI_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

def _rashi_lord(rashi: str) -> str:
    return RASHI_LORD.get(rashi, "")

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
    """Vasya koot: mutual influence/attraction based on Moon rashi. Max 2 points."""
    v1 = VASYA_BY_RASHI.get(n1["rashi"], "Manava")
    v2 = VASYA_BY_RASHI.get(n2["rashi"], "Manava")
    if v1 == v2:
        return 2, f"Same vasya group ({v1}) — strong mutual attraction."
    # Keeta with any non-Keeta = 0
    if v1 == "Keeta" or v2 == "Keeta":
        return 0, f"Keeta vasya ({v1} vs {v2}) — dominance conflict."
    # Manava can dominate Chatushpada or Jalchar
    if v1 == "Manava" and v2 in ("Chatushpada", "Jalchar"):
        return 1, f"Manava dominates {v2} — partial vasya compatibility."
    if v2 == "Manava" and v1 in ("Chatushpada", "Jalchar"):
        return 1, f"Manava dominates {v1} — partial vasya compatibility."
    # Vanchar eats Chatushpada — average to 1
    if frozenset({v1, v2}) == frozenset({"Vanchar", "Chatushpada"}):
        return 1, f"Vanchar-Chatushpada ({v1} vs {v2}) — mixed dominance."
    # Other combinations
    return 1, f"Partial vasya compatibility ({v1} vs {v2}) — moderate mutual influence."


def _score_tara(n1: dict, n2: dict) -> tuple:
    """Tara koot: based on nakshatra distance. Max 3 points.
    D = (Bride_nak - Groom_nak) mod 27, R = D mod 9.
    If R ∈ {1,3,5,7} → 3 points (good), else → 0 (bad).
    """
    nak_names = list(NAKSHATRA_DATA.keys())
    try:
        i1 = nak_names.index(n1["_name"])  # groom
        i2 = nak_names.index(n2["_name"])  # bride
    except (ValueError, KeyError):
        return 1, "Tara calculation: unable to determine — partial score."

    # D = (Bride - Groom) mod 27
    d = (i2 - i1) % 27
    # R = D mod 9
    r = d % 9
    # Tara mapping (0-based remainder -> 1-based tara number):
    #   R=0 -> Janma(1, bad), R=1 -> Sampat(2, good), R=2 -> Vipat(3, bad),
    #   R=3 -> Kshema(4, good), R=4 -> Pratyari(5, bad), R=5 -> Sadhaka(6, good),
    #   R=6 -> Vadha(7, bad), R=7 -> Mitra(8, good), R=8 -> Parama Mitra(9, good)
    _TARA_NAMES = {
        0: "Janma", 1: "Sampat", 2: "Vipat", 3: "Kshema",
        4: "Pratyari", 5: "Sadhaka", 6: "Vadha", 7: "Mitra",
        8: "Parama Mitra",
    }
    tara_name = _TARA_NAMES.get(r, str(r))
    # Favorable: Sampat(1), Kshema(3), Sadhaka(5), Mitra(7), Parama Mitra(8)
    if r in {1, 3, 5, 7, 8}:
        return 3, f"Tara: {tara_name} (remainder {r}) — favorable birth star compatibility."
    else:
        return 0, f"Tara: {tara_name} (remainder {r}) — unfavorable birth star compatibility."


def _score_yoni(n1: dict, n2: dict) -> tuple:
    """Yoni koot: sexual/physical compatibility. Max 4 points.
    Same=4, Friendly=3, Neutral=2, Hostile=1, Sworn enemy=0.
    """
    y1, y2 = n1["yoni"], n2["yoni"]
    if y1 == y2:
        return 4, f"Same yoni ({y1}) — excellent physical compatibility."
    pair = frozenset({y1, y2})
    if pair in YONI_ENEMIES:
        return 0, f"Sworn enemy yoni ({y1} vs {y2}) — significant physical incompatibility."
    if pair in YONI_FRIENDS:
        return 3, f"Friendly yoni ({y1} & {y2}) — good physical compatibility."
    # Check for hostile (but not sworn enemy) — animals of same category but not friendly
    # All remaining pairs are neutral
    return 2, f"Neutral yoni ({y1} vs {y2}) — moderate physical compatibility."


def _score_graha_maitri(n1: dict, n2: dict) -> tuple:
    """Graha Maitri koot: planetary lord friendship. Max 5 points.
    Same lord or mutual friends=5, one friend + one neutral=4,
    both neutral=3, one friend + one enemy=1, mutual enemies=0.
    """
    lord1, lord2 = n1["lord"], n2["lord"]
    if lord1 == lord2:
        return 5, f"Same nakshatra lord ({lord1}) — excellent mental compatibility."

    rel1 = PLANET_FRIENDS.get(lord1, {})
    rel2 = PLANET_FRIENDS.get(lord2, {})

    # Determine each lord's view of the other
    l1_sees_l2 = (
        "friend" if lord2 in rel1.get("friends", set())
        else "enemy" if lord2 in rel1.get("enemies", set())
        else "neutral"
    )
    l2_sees_l1 = (
        "friend" if lord1 in rel2.get("friends", set())
        else "enemy" if lord1 in rel2.get("enemies", set())
        else "neutral"
    )

    pair = frozenset({l1_sees_l2, l2_sees_l1})

    if pair == {"friend"}:
        # Mutual friends
        return 5, f"Mutual planetary friendship ({lord1} & {lord2}) — strong mental bond."
    elif pair == {"friend", "neutral"}:
        # One friend + one neutral
        return 4, f"Friendly planetary relationship ({lord1} & {lord2}) — good mental bond."
    elif pair == {"neutral"}:
        # Both neutral
        return 3, f"Neutral planetary relationship ({lord1} & {lord2}) — average mental compatibility."
    elif pair == {"friend", "enemy"}:
        # One friend + one enemy
        return 1, f"Mixed planetary relationship ({lord1} & {lord2}) — conflicting mental tendencies."
    elif "enemy" in pair:
        # Mutual enemies or one enemy + one neutral
        return 0, f"Planetary enmity ({lord1} & {lord2}) — mental friction likely."
    else:
        return 2, f"Partial planetary compatibility ({lord1} & {lord2}) — moderate mental bond."


def _score_gana(n1: dict, n2: dict) -> tuple:
    """Gana koot: temperament compatibility. Max 3 points."""
    g1, g2 = n1["gana"], n2["gana"]
    score = GANA_SCORE.get((g1, g2), 1)
    if score >= 5:
        desc = f"Same or compatible gana ({g1} & {g2}) — harmonious temperaments."
    elif score == 0:
        desc = f"Incompatible gana ({g1} & {g2}) — temperament clash likely."
    elif score >= 2:
        desc = f"Partially compatible gana ({g1} & {g2}) — manageable differences."
    else:
        desc = f"Weak gana compatibility ({g1} & {g2}) — significant temperament differences."
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

def _normalize_nakshatra(raw: str) -> str:
    """Strip pada suffixes and normalize nakshatra name for NAKSHATRA_DATA lookup.

    Handles formats like:
        "Ashwini (1)"  -> "Ashwini"
        "ashwini"      -> "Ashwini"
        "PURVA PHALGUNI" -> "Purva Phalguni"
        "  Rohini  "   -> "Rohini"
    """
    import re
    # Strip whitespace
    name = raw.strip()
    # Remove trailing pada number in parentheses: "Ashwini (1)" -> "Ashwini"
    name = re.sub(r"\s*\(\d+\)\s*$", "", name)
    # Remove trailing pada number after dash: "Ashwini-1" -> "Ashwini"
    name = re.sub(r"\s*-\d+\s*$", "", name)
    # Title-case each word: "purva phalguni" -> "Purva Phalguni"
    name = name.title()
    return name


def calculate_gun_milan(
    person1_moon_nakshatra: str,
    person2_moon_nakshatra: str,
    person1_moon_rashi: str | None = None,
    person2_moon_rashi: str | None = None,
) -> dict:
    """
    Calculate Ashtakoota Gun Milan compatibility score.

    Args:
        person1_moon_nakshatra: Moon nakshatra of person 1 (groom)
        person2_moon_nakshatra: Moon nakshatra of person 2 (bride)
        person1_moon_rashi: Actual Moon rashi (sign) of person 1 from chart.
            If provided, overrides the static rashi in NAKSHATRA_DATA.
            Important for boundary nakshatras (e.g., Krittika pada 1 = Aries,
            not Taurus) which span two rashis.
        person2_moon_rashi: Actual Moon rashi (sign) of person 2 from chart.
            Same override behavior as person1_moon_rashi.

    Returns:
        {
            total_score: int (out of 36),
            koot_scores: {koot_name: {score, max, description}},
            compatibility_percentage: float,
            recommendation: str,
        }
    """
    # Normalize nakshatra names (strip pada suffixes, fix casing)
    person1_moon_nakshatra = _normalize_nakshatra(person1_moon_nakshatra)
    person2_moon_nakshatra = _normalize_nakshatra(person2_moon_nakshatra)

    logger.debug(
        "Gun Milan input: nak1=%s rashi1=%s | nak2=%s rashi2=%s",
        person1_moon_nakshatra, person1_moon_rashi,
        person2_moon_nakshatra, person2_moon_rashi,
    )

    if person1_moon_nakshatra not in NAKSHATRA_DATA:
        logger.warning("Unknown nakshatra after normalization: %r (raw input)", person1_moon_nakshatra)
        return {
            "total_score": 0,
            "koot_scores": {},
            "compatibility_percentage": 0.0,
            "recommendation": f"Unknown nakshatra: {person1_moon_nakshatra}",
            "error": f"Unknown nakshatra: {person1_moon_nakshatra}",
        }

    if person2_moon_nakshatra not in NAKSHATRA_DATA:
        logger.warning("Unknown nakshatra after normalization: %r (raw input)", person2_moon_nakshatra)
        return {
            "total_score": 0,
            "koot_scores": {},
            "compatibility_percentage": 0.0,
            "recommendation": f"Unknown nakshatra: {person2_moon_nakshatra}",
            "error": f"Unknown nakshatra: {person2_moon_nakshatra}",
        }

    n1 = {**NAKSHATRA_DATA[person1_moon_nakshatra], "_name": person1_moon_nakshatra}
    n2 = {**NAKSHATRA_DATA[person2_moon_nakshatra], "_name": person2_moon_nakshatra}

    # Override static rashi with actual Moon rashi from chart when provided.
    # This is critical for boundary nakshatras that span two rashis
    # (e.g., Krittika pada 1 is in Aries, but NAKSHATRA_DATA says Taurus).
    if person1_moon_rashi and person1_moon_rashi in RASHI_INDEX:
        if n1["rashi"] != person1_moon_rashi:
            logger.info(
                "Rashi override for %s: %s -> %s (boundary nakshatra)",
                person1_moon_nakshatra, n1["rashi"], person1_moon_rashi,
            )
        n1["rashi"] = person1_moon_rashi
    if person2_moon_rashi and person2_moon_rashi in RASHI_INDEX:
        if n2["rashi"] != person2_moon_rashi:
            logger.info(
                "Rashi override for %s: %s -> %s (boundary nakshatra)",
                person2_moon_nakshatra, n2["rashi"], person2_moon_rashi,
            )
        n2["rashi"] = person2_moon_rashi

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

    # ── Dosha Checks & Cancellation Rules ───────────────────────
    doshas = []

    # Nadi Dosha check + cancellation
    if koot_scores["Nadi"]["score"] == 0:
        nadi_cancelled = False
        cancel_reasons = []
        # Cancel if both have same rashi
        if n1["rashi"] == n2["rashi"]:
            nadi_cancelled = True
            cancel_reasons.append("Same rashi for both")
        # Cancel if both have same nakshatra but different padas (implied by different chart)
        if n1["_name"] == n2["_name"]:
            nadi_cancelled = True
            cancel_reasons.append("Same nakshatra for both")
        # Cancel if rashi lords are friends
        lord1, lord2 = n1["lord"], n2["lord"]
        rel1 = PLANET_FRIENDS.get(lord1, {})
        if lord2 in rel1.get("friends", set()):
            nadi_cancelled = True
            cancel_reasons.append(f"Nakshatra lords ({lord1} & {lord2}) are friends")

        doshas.append({
            "name": "Nadi Dosha",
            "present": True,
            "cancelled": nadi_cancelled,
            "cancel_reasons": cancel_reasons,
            "severity": "Low (cancelled)" if nadi_cancelled else "High",
            "description": "Same Nadi — health and progeny concerns." if not nadi_cancelled else f"Nadi Dosha present but cancelled: {'; '.join(cancel_reasons)}.",
        })
    else:
        doshas.append({"name": "Nadi Dosha", "present": False, "cancelled": False, "severity": "None", "description": "Different Nadi — no dosha."})

    # Bhakoot Dosha check + cancellation
    if koot_scores["Bhakoot"]["score"] == 0:
        bhakoot_cancelled = False
        cancel_reasons = []
        # Cancel if rashi lords are same
        lord1_r = PLANET_FRIENDS.get(_rashi_lord(n1["rashi"]), {})
        lord2_r = _rashi_lord(n2["rashi"])
        if _rashi_lord(n1["rashi"]) == lord2_r:
            bhakoot_cancelled = True
            cancel_reasons.append("Same rashi lord for both signs")
        # Cancel if rashi lords are mutual friends
        elif lord2_r in lord1_r.get("friends", set()):
            rl2 = PLANET_FRIENDS.get(lord2_r, {})
            if _rashi_lord(n1["rashi"]) in rl2.get("friends", set()):
                bhakoot_cancelled = True
                cancel_reasons.append(f"Rashi lords ({_rashi_lord(n1['rashi'])} & {lord2_r}) are mutual friends")
        # Cancel if Nadi koot scored full 8
        if koot_scores["Nadi"]["score"] == 8:
            bhakoot_cancelled = True
            cancel_reasons.append("Nadi koot is full (8/8)")

        doshas.append({
            "name": "Bhakoot Dosha",
            "present": True,
            "cancelled": bhakoot_cancelled,
            "cancel_reasons": cancel_reasons,
            "severity": "Low (cancelled)" if bhakoot_cancelled else "Medium",
            "description": "Bhakoot Dosha — emotional/financial challenges." if not bhakoot_cancelled else f"Bhakoot Dosha present but cancelled: {'; '.join(cancel_reasons)}.",
        })
    else:
        doshas.append({"name": "Bhakoot Dosha", "present": False, "cancelled": False, "severity": "None", "description": "Favorable Bhakoot — no dosha."})

    # Gana Dosha check (Manushya-Rakshasa = 0)
    if koot_scores["Gana"]["score"] == 0:
        doshas.append({
            "name": "Gana Dosha",
            "present": True,
            "cancelled": False,
            "cancel_reasons": [],
            "severity": "Medium",
            "description": f"Gana mismatch ({n1['gana']} & {n2['gana']}) — temperament clash. Remedies recommended.",
        })

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
        "doshas": doshas,
        "person1_details": {
            "nakshatra": person1_moon_nakshatra,
            "rashi": n1["rashi"],
            "varna": n1["varna"],
            "vasya": VASYA_BY_RASHI.get(n1["rashi"], "Manava"),
            "yoni": n1["yoni"],
            "gana": n1["gana"],
            "nadi": n1["nadi"],
            "lord": n1["lord"],
        },
        "person2_details": {
            "nakshatra": person2_moon_nakshatra,
            "rashi": n2["rashi"],
            "varna": n2["varna"],
            "vasya": VASYA_BY_RASHI.get(n2["rashi"], "Manava"),
            "yoni": n2["yoni"],
            "gana": n2["gana"],
            "nadi": n2["nadi"],
            "lord": n2["lord"],
        },
    }
