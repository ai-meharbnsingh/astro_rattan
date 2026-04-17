"""
Lal Kitab Prediction Studio (backend)

Purpose:
- Provide the "general predictions" scoring grid as a backend-calculated feature.
- This removes the last major frontend-only (mock/fallback) scoring logic.

Notes:
- This is a heuristic scoring system used by the UI for confidence + tone.
- It is NOT a replacement for dedicated prediction endpoints
  (marriage/career/health/wealth) which remain authoritative for those topics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple


# -----------------------------
# Constants (ported from frontend)
# -----------------------------

SCORE_NEUTRAL_BASE = 50
SCORE_PAKKA_GHAR_BONUS = 30
SCORE_PRIMARY_HOUSE_BONUS = 15
SCORE_STRONG_HOUSE_BONUS = 8
SCORE_WEAK_HOUSE_PENALTY = 12
SCORE_BENEFIC_PRIMARY_BONUS = 7
SCORE_BENEFIC_DUSTHANA_PENALTY = 10
SCORE_MALEFIC_DUSTHANA_PENALTY = 15
SCORE_MALEFIC_NO_DIGNITY_PENALTY = 5
SCORE_CO_SUPPORT_BONUS = 5
SCORE_VARGOTTAMA_BONUS = 15
SCORE_NAVAMSA_EXALTED_BONUS = 12
SCORE_NAVAMSA_DEBILITATED_PENALTY = 15
SCORE_FLOOR = 5
SCORE_CEILING = 100
SCORE_DEFAULT_EMPTY = 50

CONFIDENCE_HIGH_THRESHOLD = 70
CONFIDENCE_MODERATE_THRESHOLD = 55
CONFIDENCE_LOW_THRESHOLD = 40

DEGREES_PER_SIGN = 30
NAVAMSA_DIVISIONS_PER_SIGN = 9
NAVAMSA_SIGN_COUNT = 12

DUSTHANA_HOUSES = (6, 8, 12)

# Pakka Ghar (planet permanent houses) used by the scoring model.
PAKKA_GHAR: Dict[str, int] = {
    "Sun": 1,
    "Moon": 4,
    "Mars": 3,
    "Mercury": 7,
    "Jupiter": 2,
    "Venus": 7,
    "Saturn": 8,
    "Rahu": 12,
    "Ketu": 6,
}

# Navamsa exaltation/debilitation signs (0-indexed, 0=Aries)
NAVAMSA_EXALT: Dict[str, int] = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
    "Rahu": 1,
    "Ketu": 8,
}

NAVAMSA_DEBIL: Dict[str, int] = {
    "Sun": 6,
    "Moon": 7,
    "Mars": 3,
    "Mercury": 11,
    "Jupiter": 9,
    "Venus": 5,
    "Saturn": 0,
    "Rahu": 7,
    "Ketu": 2,
}


# -----------------------------
# Models
# -----------------------------

Confidence = Literal["high", "moderate", "low", "speculative"]


@dataclass(frozen=True)
class PredictionArea:
    key: str
    en: str
    hi: str
    primary_houses: Tuple[int, ...]
    primary_planets: Tuple[str, ...]
    positive_en: str
    positive_hi: str
    caution_en: str
    caution_hi: str
    remedy_en: str
    remedy_hi: str


# Keep the same keys used by the frontend tab.
PREDICTION_AREAS: Tuple[PredictionArea, ...] = (
    PredictionArea(
        key="career",
        en="Career & Authority",
        hi="करियर और अधिकार",
        primary_houses=(10, 1, 6),
        primary_planets=("Sun", "Saturn", "Mars"),
        positive_en="Career advancement and recognition in authority roles likely.",
        positive_hi="करियर में उन्नति और अधिकार पदों में पहचान संभव।",
        caution_en="Avoid confrontations at workplace. Delays in promotions possible.",
        caution_hi="कार्यस्थल पर टकराव से बचें। पदोन्नति में देरी संभव।",
        remedy_en="Offer water to the Sun every morning. Donate wheat on Sundays.",
        remedy_hi="प्रतिदिन सुबह सूर्य को जल चढ़ाएं। रविवार को गेहूं दान करें।",
    ),
    PredictionArea(
        key="money",
        en="Money & Finance",
        hi="धन और वित्त",
        primary_houses=(2, 11, 8),
        primary_planets=("Jupiter", "Venus", "Mercury"),
        positive_en="Financial gains and wealth accumulation favored.",
        positive_hi="वित्तीय लाभ और धन संचय अनुकूल।",
        caution_en="Avoid risky investments. Unexpected expenses possible.",
        caution_hi="जोखिम भरे निवेश से बचें। अचानक खर्च संभव।",
        remedy_en="Donate yellow items on Thursdays. Feed cows with green fodder.",
        remedy_hi="गुरुवार को पीली वस्तुएं दान करें। गायों को हरा चारा खिलाएं।",
    ),
    PredictionArea(
        key="love",
        en="Love & Relationships",
        hi="प्रेम और संबंध",
        primary_houses=(7, 5, 2),
        primary_planets=("Venus", "Moon", "Mercury"),
        positive_en="Harmony and emotional support in relationships.",
        positive_hi="संबंधों में सामंजस्य और भावनात्मक सहयोग।",
        caution_en="Misunderstandings or emotional distance possible.",
        caution_hi="गलतफहमियां या भावनात्मक दूरी संभव।",
        remedy_en="Keep your home fragrant. Donate white sweets on Fridays.",
        remedy_hi="घर को सुगंधित रखें। शुक्रवार को सफेद मिठाई दान करें।",
    ),
    PredictionArea(
        key="health",
        en="Health & Vitality",
        hi="स्वास्थ्य और ऊर्जा",
        primary_houses=(1, 6, 8),
        primary_planets=("Sun", "Mars", "Saturn"),
        positive_en="Good stamina with disciplined routine.",
        positive_hi="अनुशासित दिनचर्या से अच्छी ऊर्जा।",
        caution_en="Be careful of chronic issues or sudden flare-ups.",
        caution_hi="पुरानी समस्याओं या अचानक बढ़ने वाले रोगों से सावधान रहें।",
        remedy_en="Avoid intoxicants. Donate black sesame on Saturdays.",
        remedy_hi="नशे से बचें। शनिवार को काला तिल दान करें।",
    ),
    PredictionArea(
        key="education",
        en="Education & Skills",
        hi="शिक्षा और कौशल",
        primary_houses=(4, 5, 9),
        primary_planets=("Mercury", "Jupiter", "Moon"),
        positive_en="Learning improves and skills grow steadily.",
        positive_hi="सीखने की क्षमता बढ़ती है और कौशल मजबूत होता है।",
        caution_en="Avoid distractions; consistency matters most.",
        caution_hi="ध्यान भटकने से बचें; निरंतरता सबसे महत्वपूर्ण है।",
        remedy_en="Study at sunrise. Donate books or stationery.",
        remedy_hi="सूर्योदय पर अध्ययन करें। किताबें या स्टेशनरी दान करें।",
    ),
    PredictionArea(
        key="family",
        en="Family & Home",
        hi="परिवार और घर",
        primary_houses=(4, 2, 7),
        primary_planets=("Moon", "Venus", "Jupiter"),
        positive_en="Domestic comfort and family unity increases.",
        positive_hi="घरेलू सुख और परिवारिक एकता बढ़ती है।",
        caution_en="Household tensions possible; keep patience.",
        caution_hi="घर में तनाव संभव; धैर्य रखें।",
        remedy_en="Keep water clean at home. Offer milk at Shivling on Mondays.",
        remedy_hi="घर में पानी साफ रखें। सोमवार को शिवलिंग पर दूध चढ़ाएं।",
    ),
    PredictionArea(
        key="legal",
        en="Legal & Enemies",
        hi="कानून और शत्रु",
        primary_houses=(6, 8, 12),
        primary_planets=("Mars", "Saturn", "Rahu"),
        positive_en="Legal matters resolve favorably. Victory over enemies.",
        positive_hi="कानूनी मामले अनुकूल रूप से सुलझते हैं। शत्रुओं पर विजय।",
        caution_en="Avoid legal disputes. Be careful of hidden enemies.",
        caution_hi="कानूनी विवादों से बचें। छिपे शत्रुओं से सावधान रहें।",
        remedy_en="Donate red lentils on Tuesdays. Float red items in water.",
        remedy_hi="मंगलवार को मसूर दाल दान करें। पानी में लाल वस्तुएं बहाएं।",
    ),
    PredictionArea(
        key="spiritual",
        en="Spiritual Growth",
        hi="आध्यात्मिक विकास",
        primary_houses=(9, 12, 5),
        primary_planets=("Jupiter", "Ketu", "Sun"),
        positive_en="Strong spiritual progress and inner growth. Guru connection.",
        positive_hi="मजबूत आध्यात्मिक प्रगति और आंतरिक विकास। गुरु संबंध।",
        caution_en="Spiritual practice needed. Connect with a mentor or teacher.",
        caution_hi="आध्यात्मिक अभ्यास आवश्यक। किसी गुरु या शिक्षक से जुड़ें।",
        remedy_en="Feed stray dogs. Apply turmeric tilak on Thursdays.",
        remedy_hi="आवारा कुत्तों को खिलाएं। गुरुवार को हल्दी का तिलक लगाएं।",
    ),
)


def _house_strength(planets_in_house: List[str]) -> Literal["strong", "weak", "empty"]:
    if not planets_in_house:
        return "empty"
    benefics = {"Jupiter", "Venus", "Moon", "Mercury"}
    malefics = {"Saturn", "Mars", "Rahu", "Ketu"}
    has_benefic = any(p in benefics for p in planets_in_house)
    has_malefic = any(p in malefics for p in planets_in_house)
    if has_benefic and not has_malefic:
        return "strong"
    if has_malefic and not has_benefic:
        return "weak"
    return "strong"  # mixed: treat as mitigated/strong


def score_to_confidence(score: int) -> Confidence:
    if score >= CONFIDENCE_HIGH_THRESHOLD:
        return "high"
    if score >= CONFIDENCE_MODERATE_THRESHOLD:
        return "moderate"
    if score >= CONFIDENCE_LOW_THRESHOLD:
        return "low"
    return "speculative"


def _navamsa_dignity_adjustment(planet: str, lon: float) -> int:
    """
    Ported Navamsa logic from frontend:
    - Compute D1 sign and D9 sign for longitude.
    - Apply vargottama/exaltation/debilitation bonuses.
    """
    d1_sign = int(lon // DEGREES_PER_SIGN) % NAVAMSA_SIGN_COUNT
    pada = int(((lon % DEGREES_PER_SIGN) * NAVAMSA_DIVISIONS_PER_SIGN) // DEGREES_PER_SIGN)
    navamsa_sign = (d1_sign * NAVAMSA_DIVISIONS_PER_SIGN + pada) % NAVAMSA_SIGN_COUNT
    adj = 0
    if d1_sign == navamsa_sign:
        adj += SCORE_VARGOTTAMA_BONUS
    if NAVAMSA_EXALT.get(planet) == navamsa_sign:
        adj += SCORE_NAVAMSA_EXALTED_BONUS
    if NAVAMSA_DEBIL.get(planet) == navamsa_sign:
        adj -= SCORE_NAVAMSA_DEBILITATED_PENALTY
    return adj


def compute_area_score(
    area: PredictionArea,
    planet_positions: Dict[str, int],
    planet_longitudes: Optional[Dict[str, float]] = None,
) -> int:
    total_score = 0
    count = 0
    benefics = {"Jupiter", "Venus", "Moon", "Mercury"}
    malefics = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}
    dushthanas = set(DUSTHANA_HOUSES)

    # Precompute house->planets and house strengths.
    house_to_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for p, h in planet_positions.items():
        if isinstance(h, int) and 1 <= h <= 12:
            house_to_planets[h].append(p)
    house_strengths: Dict[int, str] = {h: _house_strength(ps) for h, ps in house_to_planets.items()}

    for planet_key in area.primary_planets:
        house = planet_positions.get(planet_key)
        if not house:
            continue

        score = SCORE_NEUTRAL_BASE
        is_pakka = house == PAKKA_GHAR.get(planet_key)
        if is_pakka:
            score += SCORE_PAKKA_GHAR_BONUS

        in_primary_house = house in area.primary_houses
        if in_primary_house:
            score += SCORE_PRIMARY_HOUSE_BONUS

        hs = house_strengths.get(house)
        if hs == "strong":
            score += SCORE_STRONG_HOUSE_BONUS
        if hs == "weak":
            score -= SCORE_WEAK_HOUSE_PENALTY

        if planet_key in benefics and in_primary_house:
            score += SCORE_BENEFIC_PRIMARY_BONUS
        if planet_key in benefics and house in dushthanas:
            score -= SCORE_BENEFIC_DUSTHANA_PENALTY

        if planet_key in malefics and house in dushthanas:
            score -= SCORE_MALEFIC_DUSTHANA_PENALTY
        if planet_key in malefics and in_primary_house and not is_pakka:
            score -= SCORE_MALEFIC_NO_DIGNITY_PENALTY

        co_support = 0
        for p in area.primary_planets:
            if p == planet_key:
                continue
            ph = planet_positions.get(p, -1)
            if ph in area.primary_houses:
                co_support += 1
        if co_support > 0:
            score += SCORE_CO_SUPPORT_BONUS

        if planet_longitudes is not None:
            try:
                lon = float(planet_longitudes.get(planet_key, 0.0) or 0.0)
            except Exception:
                lon = 0.0
            score += _navamsa_dignity_adjustment(planet_key, lon)

        score = max(SCORE_FLOOR, min(SCORE_CEILING, score))
        total_score += score
        count += 1

    if count == 0:
        return SCORE_DEFAULT_EMPTY
    return int(round(total_score / count))


# ─────────────────────────────────────────────────────────────
# Chart-specific text generation (Codex R3 fix)
# Adds planet-name / house / dignity references into each area
# so predictions stop reading like generic templates.
# ─────────────────────────────────────────────────────────────

# Area-specific one-line themes per planet. Keeps text focused on
# what this planet *means* for this area (career/money/health/…).
AREA_PLANET_THEME: Dict[str, Dict[str, str]] = {
    "career":    {"Sun": "public authority and recognition",
                  "Saturn": "long-term discipline and partnerships",
                  "Mars": "drive and initiative"},
    "money":     {"Jupiter": "wisdom-led wealth",
                  "Venus": "luxury and accumulated assets",
                  "Mercury": "commerce and skill-based income"},
    "love":      {"Venus": "harmony and partnership",
                  "Moon": "emotional connection",
                  "Mercury": "communication in relationships"},
    "health":    {"Sun": "core vitality",
                  "Mars": "physical energy and inflammation",
                  "Saturn": "longevity, bones and joints"},
    "education": {"Mercury": "learning and skill acquisition",
                  "Jupiter": "wisdom and higher study",
                  "Moon": "receptivity and memory"},
    "family":    {"Moon": "mother and home-feel",
                  "Venus": "domestic harmony",
                  "Jupiter": "elders and dharma at home"},
    "legal":     {"Mars": "aggression and combat",
                  "Saturn": "verdicts and delays",
                  "Rahu": "hidden agendas"},
    "spiritual": {"Jupiter": "dharma and teacher connection",
                  "Ketu": "detachment and liberation",
                  "Sun": "inner light"},
}

# Mapping for the remedy sentence: the specific life-area consequence
# of the weakest planet, so the remedy hook makes sense contextually.
AREA_WEAKEST_HOOK_EN: Dict[str, str] = {
    "career":    "career output",
    "money":     "financial flow",
    "love":     "relationship stability",
    "health":    "physical vitality",
    "education": "study progress",
    "family":    "domestic peace",
    "legal":     "legal standing",
    "spiritual": "inner progress",
}

# Dignity → rank (higher is stronger)
_DIGNITY_RANK = {
    "Exalted": 5, "Own Sign": 4, "Friendly": 3,
    "Neutral": 2, "Enemy": 1, "Debilitated": 0,
}

def _dignity_phrase(dignity: str) -> str:
    return {
        "Exalted":     "exalted",
        "Own Sign":    "in own sign",
        "Friendly":    "in friendly sign",
        "Neutral":     "in neutral sign",
        "Enemy":       "in enemy sign",
        "Debilitated": "debilitated",
    }.get(dignity, "")


def _strength_verdict(dignity: str) -> str:
    rank = _DIGNITY_RANK.get(dignity, 2)
    if rank >= 4:
        return "strong"
    if rank == 3:
        return "supportive"
    if rank == 2:
        return "neutral"
    return "weakened"


def _build_specific_text(
    area: "PredictionArea",
    planet_positions: Dict[str, int],
    planet_longitudes: Optional[Dict[str, float]],
) -> Dict[str, str]:
    """
    Generate chart-specific EN/HI text for one prediction area.

    Returns a dict with positive_en, caution_en, remedy_en (plus HI)
    that names the actual trace planets, their houses and dignities.
    Falls back to empty strings if the chart has no trace planets.
    """
    # Local imports to avoid cycles
    from app.astro_engine import get_sign_from_longitude
    from app.lalkitab_engine import _get_dignity_label, REMEDIES_BY_HOUSE

    # Build a list of (planet, house, sign, dignity) for trace planets.
    details = []
    for p in area.primary_planets:
        h = planet_positions.get(p)
        if not h:
            continue
        sign = ""
        if planet_longitudes and p in planet_longitudes:
            try:
                sign = get_sign_from_longitude(float(planet_longitudes[p]))
            except Exception:
                sign = ""
        dignity = _get_dignity_label(p, sign) if sign else "Neutral"
        details.append({"planet": p, "house": h, "sign": sign, "dignity": dignity})

    if not details:
        return {}

    # Sort by strength (strongest first)
    details.sort(key=lambda d: _DIGNITY_RANK.get(d["dignity"], 2), reverse=True)
    strongest = details[0]
    weakest = details[-1]
    area_themes = AREA_PLANET_THEME.get(area.key, {})

    # Detect cluster (2+ trace planets in same house)
    house_counts: Dict[int, int] = {}
    for d in details:
        house_counts[d["house"]] = house_counts.get(d["house"], 0) + 1
    clustered = [h for h, c in house_counts.items() if c >= 2]

    def describe(d: dict) -> str:
        theme = area_themes.get(d["planet"], "")
        dig_phrase = _dignity_phrase(d["dignity"])
        theme_note = f" — {theme}" if theme else ""
        return f"{d['planet']} {dig_phrase} in H{d['house']}{theme_note}"

    # ── Positive sentence: strongest + (optionally) 2nd strong ──
    positive_parts = []
    for d in details:
        rank = _DIGNITY_RANK.get(d["dignity"], 2)
        if rank >= 3:  # Friendly or better
            positive_parts.append(describe(d))
    if positive_parts:
        positive_en = "Strengths: " + "; ".join(positive_parts) + "."
    else:
        positive_en = (
            f"No planet in this area's trace is classically strong in its sign. "
            f"{strongest['planet']} in H{strongest['house']} is the best available "
            f"anchor, but results stay moderate."
        )

    # ── Caution sentence: weakest (only if actually weak) ──
    rank_weakest = _DIGNITY_RANK.get(weakest["dignity"], 2)
    if rank_weakest <= 1:  # Enemy or Debilitated
        caution_en = (
            f"Caution: {describe(weakest)} is the risk vector — its weakness drags "
            f"down {AREA_WEAKEST_HOOK_EN.get(area.key, 'this life area')}."
        )
    elif rank_weakest == 2:
        caution_en = (
            f"Caution: {weakest['planet']} neutral in H{weakest['house']} is the "
            f"softest link — no crisis, just ordinary friction."
        )
    else:
        caution_en = (
            "Caution: no planet in this area's trace is seriously afflicted. "
            "Standard diligence is enough."
        )

    # ── Cluster note (if 2+ trace planets share a house) ──
    if clustered:
        ch = clustered[0]
        cluster_planets = [d["planet"] for d in details if d["house"] == ch]
        caution_en += (
            f" Note: {len(cluster_planets)} of the {area.en.lower()} "
            f"planets ({', '.join(cluster_planets)}) cluster in H{ch} — the axis "
            f"of H{ch} carries disproportionate weight for this area."
        )

    # ── Remedy: target the WEAKEST planet's LK position remedy ──
    wp_name, wp_house = weakest["planet"], weakest["house"]
    canonical = REMEDIES_BY_HOUSE.get(wp_name, {}).get(wp_house, {})
    hook = AREA_WEAKEST_HOOK_EN.get(area.key, "this area")
    if canonical.get("en"):
        remedy_en = (
            f"Remedy: the weakest trace planet is {wp_name} in H{wp_house} "
            f"({weakest['dignity']}). Targeting it directly uplifts {hook}. "
            f"{canonical['en']}"
        )
        remedy_hi = (
            f"उपाय: इस क्षेत्र में सबसे कमज़ोर ग्रह {wp_name} भाव {wp_house} में "
            f"({weakest['dignity']}) है। उसे सीधे बल देने से {hook} सुधरता है। "
            f"{canonical.get('hi', '')}"
        )
    else:
        remedy_en = (
            f"Remedy: weakest trace planet is {wp_name} in H{wp_house}. "
            f"Use its standard Lal Kitab remedy for this house."
        )
        remedy_hi = (
            f"उपाय: सबसे कमज़ोर ग्रह {wp_name} भाव {wp_house}। उसका "
            f"लाल किताब उपाय अपनाएं।"
        )

    # ── Hindi positive / caution (transliterated structurally) ──
    def describe_hi(d):
        theme = area_themes.get(d["planet"], "")
        dig_phrase = {
            "Exalted": "उच्च का", "Own Sign": "स्वराशि में",
            "Friendly": "मित्र राशि में", "Neutral": "तटस्थ",
            "Enemy": "शत्रु राशि में", "Debilitated": "नीच का",
        }.get(d["dignity"], "")
        theme_note = f" — {theme}" if theme else ""
        return f"{d['planet']} भाव {d['house']} में {dig_phrase}{theme_note}"

    if positive_parts:
        positive_hi = "बल: " + "; ".join(describe_hi(d) for d in details
                                         if _DIGNITY_RANK.get(d["dignity"], 2) >= 3) + "।"
    else:
        positive_hi = (
            f"इस क्षेत्र के त्रिकोण में कोई ग्रह स्वतः बली नहीं। "
            f"{strongest['planet']} भाव {strongest['house']} में सर्वश्रेष्ठ उपलब्ध सहारा है।"
        )

    if rank_weakest <= 1:
        caution_hi = (
            f"सावधानी: {describe_hi(weakest)} — यह कमज़ोरी "
            f"{AREA_WEAKEST_HOOK_EN.get(area.key, 'इस क्षेत्र')} को प्रभावित करती है।"
        )
    elif rank_weakest == 2:
        caution_hi = (
            f"सावधानी: {weakest['planet']} भाव {weakest['house']} में तटस्थ — "
            f"संकट नहीं, पर सामान्य रुकावट।"
        )
    else:
        caution_hi = "सावधानी: इस क्षेत्र के ग्रह गंभीर रूप से पीड़ित नहीं — सामान्य सावधानी पर्याप्त।"

    if clustered:
        ch = clustered[0]
        cp = [d["planet"] for d in details if d["house"] == ch]
        caution_hi += (
            f" टिप्पणी: इस क्षेत्र के {len(cp)} ग्रह "
            f"({', '.join(cp)}) भाव {ch} में इकट्ठे हैं — इस अक्ष पर अधिक भार।"
        )

    return {
        "positive_en": positive_en,
        "positive_hi": positive_hi,
        "caution_en": caution_en,
        "caution_hi": caution_hi,
        "remedy_en": remedy_en,
        "remedy_hi": remedy_hi,
        "weakest_planet": wp_name,
        "weakest_house": wp_house,
        "weakest_dignity": weakest["dignity"],
        "strongest_planet": strongest["planet"],
        "strongest_house": strongest["house"],
        "strongest_dignity": strongest["dignity"],
        "trace_details": details,
    }


def build_prediction_studio(
    planet_positions: Dict[str, int],
    planet_longitudes: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Returns:
      {
        "areas": [
          { key, title_en, title_hi, score, confidence, is_positive,
            positive_en, positive_hi, caution_en, caution_hi, remedy_en, remedy_hi,
            trace: [{planet, house}, ...]
          },
          ...
        ]
      }
    """
    areas_out: List[Dict[str, Any]] = []
    for area in PREDICTION_AREAS:
        score = compute_area_score(area, planet_positions, planet_longitudes)
        conf = score_to_confidence(score)
        trace = []
        for p in area.primary_planets:
            h = int(planet_positions.get(p) or 0)
            if h:
                trace.append({"planet": p, "house": h})

        # Build chart-specific text that names actual planets + houses
        # + dignities instead of emitting the generic template.
        specific = _build_specific_text(area, planet_positions, planet_longitudes)

        positive_en = specific.get("positive_en") or area.positive_en
        positive_hi = specific.get("positive_hi") or area.positive_hi
        caution_en  = specific.get("caution_en")  or area.caution_en
        caution_hi  = specific.get("caution_hi")  or area.caution_hi
        remedy_en   = specific.get("remedy_en")   or area.remedy_en
        remedy_hi   = specific.get("remedy_hi")   or area.remedy_hi

        areas_out.append(
            {
                "key": area.key,
                "title_en": area.en,
                "title_hi": area.hi,
                "score": score,
                "confidence": conf,
                "is_positive": score >= 55,
                "positive_en": positive_en,
                "positive_hi": positive_hi,
                "caution_en": caution_en,
                "caution_hi": caution_hi,
                "remedy_en": remedy_en,
                "remedy_hi": remedy_hi,
                "trace": trace,
                # Chart-specific metadata for the frontend / audit:
                "weakest_planet": specific.get("weakest_planet"),
                "weakest_house": specific.get("weakest_house"),
                "weakest_dignity": specific.get("weakest_dignity"),
                "strongest_planet": specific.get("strongest_planet"),
                "strongest_house": specific.get("strongest_house"),
                "strongest_dignity": specific.get("strongest_dignity"),
            }
        )
    from app.lalkitab_source_tags import source_of
    src = source_of("build_prediction_studio")  # PRODUCT
    for area in areas_out:
        area.setdefault("source", src)
    return {"areas": areas_out, "source": src}

