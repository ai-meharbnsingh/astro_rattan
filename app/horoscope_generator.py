"""H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes."""
import json
import logging
import random
import psycopg2
import psycopg2.extras
from datetime import date, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

from app.database import DATABASE_URL

# The 12 zodiac signs
SIGNS: List[str] = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

# Ruling planets per sign (used in template generation)
_RULERS = {
    "aries": "Mars", "taurus": "Venus", "gemini": "Mercury", "cancer": "Moon",
    "leo": "Sun", "virgo": "Mercury", "libra": "Venus", "scorpio": "Mars",
    "sagittarius": "Jupiter", "capricorn": "Saturn", "aquarius": "Saturn", "pisces": "Jupiter",
}

# Elements per sign
_ELEMENTS = {
    "aries": "fire", "taurus": "earth", "gemini": "air", "cancer": "water",
    "leo": "fire", "virgo": "earth", "libra": "air", "scorpio": "water",
    "sagittarius": "fire", "capricorn": "earth", "aquarius": "air", "pisces": "water",
}

# Template pools for template-based generation
_CAREER = [
    "Career opportunities may arise unexpectedly today.",
    "Focus on professional goals — your hard work is about to pay off.",
    "A colleague may offer valuable insight that changes your perspective.",
    "Financial matters look favorable; consider long-term investments.",
    "Your leadership qualities will be noticed by those in authority.",
    "A creative project at work gains momentum today.",
]

_LOVE = [
    "Romance is in the air — be open to heartfelt conversations.",
    "Your partner appreciates your emotional depth today.",
    "Single? An intriguing connection may develop through mutual friends.",
    "Communication strengthens your closest relationships.",
    "Show vulnerability — it deepens bonds more than you expect.",
    "Family harmony brings comfort and joy.",
]

_HEALTH = [
    "Pay attention to rest — your body needs recovery time.",
    "A morning walk or yoga session will boost your energy levels.",
    "Digestive health needs attention; choose lighter meals today.",
    "Mental clarity comes through meditation or quiet reflection.",
    "Physical exercise will help channel restless energy productively.",
    "Hydration and balanced nutrition are key priorities today.",
]

_SPIRITUAL = [
    "The planetary alignment favors spiritual growth and self-reflection.",
    "Chanting or prayer during Brahma Muhurta amplifies positive energy.",
    "Trust your intuition — the cosmos guides you toward your dharma.",
    "A moment of silence reveals answers you've been seeking.",
    "Past karma resolves as you embrace compassion and forgiveness.",
    "Connect with nature to ground your spiritual energy.",
]

_CHALLENGES = [
    "Minor obstacles test your patience — stay calm and composed.",
    "Avoid impulsive decisions, especially in financial matters.",
    "Miscommunication is possible — choose words carefully.",
    "Unexpected changes in plans require flexibility and grace.",
    "Guard against overcommitting — prioritize what truly matters.",
    "Emotional sensitivity may be heightened — practice self-care.",
]


from app.astro_engine import calculate_planet_positions

# ---------------------------------------------------------------------------
# Vedic Rulership and Dignities
# ---------------------------------------------------------------------------
_EXALTED_SIGNS = {
    "Sun": "aries", "Moon": "taurus", "Mars": "capricorn",
    "Mercury": "virgo", "Jupiter": "cancer", "Venus": "pisces",
    "Saturn": "libra", "Rahu": "gemini", "Ketu": "sagittarius",
}

_DEBILITATED_SIGNS = {
    "Sun": "libra", "Moon": "scorpio", "Mars": "cancer",
    "Mercury": "pisces", "Jupiter": "capricorn", "Venus": "virgo",
    "Saturn": "aries", "Rahu": "sagittarius", "Ketu": "gemini",
}

_OWN_SIGNS = {
    "Sun": ["leo"],
    "Moon": ["cancer"],
    "Mars": ["aries", "scorpio"],
    "Mercury": ["gemini", "virgo"],
    "Jupiter": ["sagittarius", "pisces"],
    "Venus": ["taurus", "libra"],
    "Saturn": ["capricorn", "aquarius"],
}

def _get_current_transits() -> Dict[str, str]:
    """Calculate today's planetary positions (signs) for horoscope weighting."""
    today = date.today().isoformat()
    # Delhi, India for global standard IST/transit calculation
    res = calculate_planet_positions(today, "12:00:00", 28.6, 77.2, 5.5)
    transits = {}
    for p_name, p_data in res.get("planets", {}).items():
        transits[p_name] = p_data.get("sign", "Aries").lower()
    return transits

def _generate_template_horoscope(sign: str, transits: Optional[Dict[str, str]] = None) -> str:
    """
    Generate a horoscope using template pools, weighted by the 
    current transit position of the sign's ruler.
    """
    if not transits:
        transits = {}
        
    ruler = _RULERS.get(sign)
    ruler_sign = transits.get(ruler, "aries").lower()
    element = _ELEMENTS[sign]

    # Calculate dignity for weighting
    is_exalted = _EXALTED_SIGNS.get(ruler) == ruler_sign
    is_debilitated = _DEBILITATED_SIGNS.get(ruler) == ruler_sign
    is_own = ruler_sign in _OWN_SIGNS.get(ruler, [])

    # Relative house calculation (1-indexed)
    sign_idx = SIGNS.index(sign)
    ruler_idx = SIGNS.index(ruler_sign)
    rel_house = ((ruler_idx - sign_idx) % 12) + 1

    # Weighting pools based on dignity
    # 6/8/12 = challenges
    # 1/5/9/10 = strength
    has_challenge = is_debilitated or rel_house in [6, 8, 12]
    is_strong = is_exalted or is_own or rel_house in [1, 5, 9, 10]

    intro_templates = [
        f"{ruler}'s influence brings transformative energy to {sign.title()} today.",
        f"As a {element} sign ruled by {ruler}, you feel a surge of clarity and purpose.",
        f"The cosmic alignment favors {sign.title()} — {ruler} empowers your natural strengths.",
        f"Today's planetary transits highlight {sign.title()}'s {element} energy through {ruler}'s guidance.",
    ]

    intro = random.choice(intro_templates)
    
    # Pick templates with bias
    career = random.choice(_CAREER)
    if is_strong:
        career = _CAREER[random.randint(4, 5)] # Favor high-success templates
        
    love = random.choice(_LOVE)
    if rel_house == 5:
        love = _LOVE[0] # "Romance is in the air"
        
    health = random.choice(_HEALTH)
    if has_challenge:
        health = _HEALTH[0] # "Pay attention to rest"
        
    spiritual = random.choice(_SPIRITUAL)
    if is_own:
        spiritual = _SPIRITUAL[random.randint(2, 4)]

    # Include a challenge if planetary alignment is difficult
    challenge = ""
    if has_challenge or random.random() < 0.2:
        challenge = f" {random.choice(_CHALLENGES)}"

    return f"{intro} {career} {love} {health} {spiritual}{challenge}"


def _try_ai_horoscope(sign: str, period_date: str) -> str:
    """Attempt to generate a horoscope using AI. Returns empty string — AI engine removed."""
    return ""


def generate_daily_horoscopes(db_path: str = None):
    """Generate daily horoscopes for all 12 signs for today. Skips if already exist."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False

    today = date.today().isoformat()
    transits = _get_current_transits()

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT COUNT(*) as c FROM horoscopes WHERE period_type = 'daily' AND period_date = %s",
            (today,),
        )
        existing = cur.fetchone()["c"]

    if existing >= 12:
        conn.close()
        return

    for sign in SIGNS:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id FROM horoscopes WHERE sign = %s AND period_type = 'daily' AND period_date = %s",
                (sign, today),
            )
            row = cur.fetchone()
        if row:
            continue

        # Try AI first, fall back to templates
        content = _try_ai_horoscope(sign, today)
        if not content:
            content = _generate_template_horoscope(sign, transits)

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO horoscopes (sign, period_type, period_date, content) VALUES (%s, %s, %s, %s)",
                (sign, "daily", today, content),
            )

    conn.commit()
    conn.close()
    logger.info("[horoscope] Generated daily horoscopes for %s", today)


def seed_weekly_horoscopes(db_path: str = None):
    """Seed 12 weekly horoscopes as initial content."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False

    # Monday of current week
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_date = monday.isoformat()

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT COUNT(*) as c FROM horoscopes WHERE period_type = 'weekly' AND period_date = %s",
            (week_date,),
        )
        existing = cur.fetchone()["c"]

    if existing >= 12:
        conn.close()
        return

    for sign in SIGNS:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id FROM horoscopes WHERE sign = %s AND period_type = 'weekly' AND period_date = %s",
                (sign, week_date),
            )
            row = cur.fetchone()
        if row:
            continue

        ruler = _RULERS[sign]
        element = _ELEMENTS[sign]
        content = (
            f"This week, {sign.title()} natives benefit from {ruler}'s strengthening influence. "
            f"As a {element} sign, your natural qualities are amplified. "
            f"{random.choice(_CAREER)} {random.choice(_LOVE)} "
            f"{random.choice(_SPIRITUAL)} "
            f"The week ahead holds potential for growth in all areas of life. "
            f"Stay grounded and trust the cosmic timing."
        )

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO horoscopes (sign, period_type, period_date, content) VALUES (%s, %s, %s, %s)",
                (sign, "weekly", week_date, content),
            )

    conn.commit()
    conn.close()
    logger.info("[horoscope] Seeded weekly horoscopes for week of %s", week_date)


# ---------------------------------------------------------------------------
# AI-personalized horoscope generation
# ---------------------------------------------------------------------------

_SECTIONS = ("general", "love", "career", "finance", "health")


def _build_ai_horoscope_prompt(
    sign: str,
    period: str,
    birth_data: Optional[Dict] = None,
) -> tuple:
    """Return (system_prompt, user_prompt) for AI-personalized horoscope."""
    ruler = _RULERS[sign]
    element = _ELEMENTS[sign]

    system_prompt = (
        "You are an expert Vedic astrologer (Jyotishi) who writes personalized horoscopes. "
        "Generate a horoscope with EXACTLY these five sections: General, Love, Career, Finance, Health. "
        "Format your response as valid JSON with keys: general, love, career, finance, health. "
        "Each value should be a string of 2-4 sentences. "
        "Use Vedic astrology concepts (transits, nakshatras, planetary influences). "
        "Be warm, encouraging, and specific. Do not include markdown formatting."
    )

    birth_context = ""
    if birth_data:
        parts = []
        if birth_data.get("birth_date"):
            parts.append(f"born on {birth_data['birth_date']}")
        if birth_data.get("birth_time"):
            parts.append(f"at {birth_data['birth_time']}")
        if birth_data.get("birth_place"):
            parts.append(f"in {birth_data['birth_place']}")
        if parts:
            birth_context = (
                f" The native was {', '.join(parts)}. "
                "Personalize the reading based on this birth information."
            )

    user_prompt = (
        f"Generate a {period} horoscope for {sign.title()} "
        f"(a {element} sign ruled by {ruler}). "
        f"Consider current planetary transits and {ruler}'s influence on this sign.{birth_context} "
        f"Respond ONLY with a JSON object having keys: general, love, career, finance, health."
    )

    return system_prompt, user_prompt


def _parse_ai_sections(response: str) -> Optional[Dict[str, str]]:
    """Try to extract the five horoscope sections from AI response JSON."""
    try:
        # Strip potential markdown code fences
        text = response.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            if text.startswith("json"):
                text = text[4:].strip()

        data = json.loads(text)
        if isinstance(data, dict) and all(k in data for k in _SECTIONS):
            return {k: str(data[k]) for k in _SECTIONS}
    except (json.JSONDecodeError, TypeError, KeyError):
        pass

    # Fallback: try to find a JSON object within the response
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
            if isinstance(data, dict) and all(k in data for k in _SECTIONS):
                return {k: str(data[k]) for k in _SECTIONS}
    except (json.JSONDecodeError, TypeError, KeyError):
        pass

    return None


def _template_fallback_sections(sign: str, period: str = "daily") -> Dict[str, str]:
    """Generate period-aware template horoscope sections as a fallback."""
    ruler = _RULERS[sign]
    element = _ELEMENTS[sign]

    period_context = {
        "daily": {
            "general": [
                f"{ruler}'s influence brings focused momentum to {sign.title()} today.",
                f"As a {element} sign ruled by {ruler}, your decisions carry extra clarity today.",
                f"Today's transits support practical action for {sign.title()}.",
            ],
            "love": [
                "In love, stay clear and warm in communication; small gestures bring better harmony.",
                "Relationship matters improve when you listen first and respond calmly.",
                "Single natives may notice a meaningful connection through routine interactions.",
            ],
            "career": [
                "At work, prioritize one key task and complete it before taking on new demands.",
                "Professional visibility is stronger today; disciplined effort gets noticed quickly.",
                "Keep meetings concise and outcome-focused for better progress.",
            ],
            "finance": [
                "Money flow stays manageable if you avoid impulse spending and review essentials.",
                "Financial decisions benefit from caution; postpone risky commitments for now.",
                "A practical budget adjustment today creates steadier balance.",
            ],
            "health": [
                "Energy is stable when you maintain hydration, lighter meals, and proper sleep.",
                "Nervous tension reduces with a short walk, breathwork, or quiet reflection.",
                "Avoid overexertion; consistency works better than intensity today.",
            ],
        },
        "weekly": {
            "general": [
                f"This week, {ruler}'s movement supports structured progress for {sign.title()}.",
                f"The week favors steady planning over rushed decisions for {sign.title()} natives.",
                f"Weekly trends show stronger outcomes when {sign.title()} follows clear priorities.",
            ],
            "love": [
                "Love and family matters improve in the second half of the week through patient dialogue.",
                "Relationship energy is mixed early week, then smoother by mid-week.",
                "Shared plans and practical support strengthen bonds this week.",
            ],
            "career": [
                "Career momentum builds after mid-week; keep early-week efforts disciplined and organized.",
                "Professional progress is best through collaboration and consistent follow-through.",
                "Handle pending work first; fresh opportunities open toward week end.",
            ],
            "finance": [
                "Financially, this week supports correction and control rather than high-risk expansion.",
                "Keep spending planned; avoid emotional purchases around mid-week.",
                "Review dues and recurring expenses for better stability by weekend.",
            ],
            "health": [
                "Health remains balanced if routine is protected, especially sleep and digestion.",
                "Weekly stress peaks around workload; short recovery breaks prevent burnout.",
                "Moderate exercise and lighter evening food improve overall stamina.",
            ],
        },
        "monthly": {
            "general": [
                f"This month, {ruler} sets a practical growth cycle for {sign.title()} with clearer direction by mid-month.",
                f"Monthly transits favor patient strategy; early adjustments lead to stronger results later.",
                f"{sign.title()} enters a month of consolidation first, then expansion in the second half.",
            ],
            "love": [
                "In relationships, the first half needs patience, while the second half supports emotional clarity and reconnection.",
                "Love improves after mid-month when communication becomes more direct and supportive.",
                "Singles may find steady prospects through trusted circles rather than sudden encounters.",
            ],
            "career": [
                "Career shows gradual rise: early month is for planning and cleanup, late month brings visible traction.",
                "Use the first two weeks to organize priorities; recognition is stronger in the final phase.",
                "Professional decisions taken after mid-month are likely to be more stable.",
            ],
            "finance": [
                "Monthly finance improves through budgeting discipline; avoid speculative moves in the opening phase.",
                "Cash flow stabilizes when you reduce optional spending early and optimize commitments later.",
                "Second-half opportunities can support gains if you stay conservative with risk.",
            ],
            "health": [
                "Health favors routine correction this month; digestion, sleep rhythm, and stress management need consistency.",
                "Energy may fluctuate early month, then improve steadily with disciplined habits.",
                "A sustainable routine gives better monthly outcomes than short, intense efforts.",
            ],
        },
        "yearly": {
            "general": [
                f"This year, {ruler} guides {sign.title()} through a disciplined long-cycle of rebuilding, then expansion.",
                f"The annual pattern emphasizes foundations first and stronger outward progress in later phases.",
                f"{sign.title()} sees a year of measured growth where patience converts into durable gains.",
            ],
            "love": [
                "Relationship themes mature this year: communication and shared responsibility become the main growth keys.",
                "Love life improves in stages, with deeper stability after unresolved patterns are addressed.",
                "Singles are more likely to attract meaningful long-term compatibility than short-term excitement.",
            ],
            "career": [
                "Career advancement is steady through consistent performance; major leaps come after groundwork is complete.",
                "This year rewards process, credibility, and long-horizon planning over quick wins.",
                "Professional authority strengthens when you focus on execution quality and reliability.",
            ],
            "finance": [
                "Annual finance favors accumulation and protection; disciplined allocation outperforms aggressive speculation.",
                "Build reserves, reduce leakages, and prioritize long-term financial structure this year.",
                "Larger gains are possible when decisions are timed and risk-managed carefully.",
            ],
            "health": [
                "Yearly health outlook improves with a stable routine; stress, recovery, and metabolic balance need continuous care.",
                "Energy trends are favorable when sleep and movement stay non-negotiable across the year.",
                "Preventive care and consistency matter more than reactive fixes this cycle.",
            ],
        },
    }

    context = period_context.get(period, period_context["daily"])

    return {
        "general": random.choice(context["general"]) + " " + random.choice(_SPIRITUAL),
        "love": random.choice(context["love"]),
        "career": random.choice(context["career"]),
        "finance": random.choice(context["finance"]),
        "health": random.choice(context["health"]),
    }


def generate_ai_horoscope(
    sign: str,
    period: str = "daily",
    birth_data: Optional[Dict] = None,
) -> Dict:
    """
    Generate an AI-personalized horoscope with sectioned content.

    Uses the AI engine for personalized horoscope generation based on
    current planetary transits, the sign's ruling planet and element.
    Falls back to template-based generation if AI is unavailable.

    Args:
        sign: Zodiac sign (lowercase, e.g. "aries").
        period: One of "daily", "weekly", "monthly", "yearly".
        birth_data: Optional dict with keys birth_date, birth_time, birth_place.

    Returns:
        Dict with keys: sign, period, sections (dict of 5 sections),
        source ("ai" or "template"), and personalized (bool).
    """
    sign = sign.lower()
    if sign not in SIGNS:
        raise ValueError(f"Invalid zodiac sign: {sign}")
    if period not in ("daily", "weekly", "monthly", "yearly"):
        raise ValueError(f"Invalid period: {period}")

    ruler = _RULERS[sign]
    element = _ELEMENTS[sign]

    # AI engine removed — use template-based generation
    sections = None
    source = "template"

    if sections is None:
        sections = _template_fallback_sections(sign, period)

    return {
        "sign": sign,
        "period": period,
        "ruling_planet": ruler,
        "element": element,
        "sections": sections,
        "source": source,
        "personalized": birth_data is not None and source == "ai",
    }
