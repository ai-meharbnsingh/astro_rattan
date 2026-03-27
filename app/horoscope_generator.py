"""H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes."""
import json
import random
import psycopg2
import psycopg2.extras
from datetime import date, timedelta
from typing import Dict, List, Optional

from app.database import DATABASE_URL

# The 12 zodiac signs
SIGNS: List[str] = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

# Ruling planets per sign (used in template generation)
_RULERS = {
    "aries": "Mars", "taurus": "Venus", "gemini": "Mercury", "cancer": "Moon",
    "leo": "Sun", "virgo": "Mercury", "libra": "Venus", "scorpio": "Pluto",
    "sagittarius": "Jupiter", "capricorn": "Saturn", "aquarius": "Uranus", "pisces": "Neptune",
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


def _generate_template_horoscope(sign: str) -> str:
    """Generate a horoscope using template pools with sign-specific planetary context."""
    ruler = _RULERS[sign]
    element = _ELEMENTS[sign]

    intro_templates = [
        f"{ruler}'s influence brings transformative energy to {sign.title()} today.",
        f"As a {element} sign ruled by {ruler}, you feel a surge of clarity and purpose.",
        f"The cosmic alignment favors {sign.title()} — {ruler} empowers your natural strengths.",
        f"Today's planetary transits highlight {sign.title()}'s {element} energy through {ruler}'s guidance.",
    ]

    intro = random.choice(intro_templates)
    career = random.choice(_CAREER)
    love = random.choice(_LOVE)
    health = random.choice(_HEALTH)
    spiritual = random.choice(_SPIRITUAL)

    # 50% chance of including a challenge
    challenge = ""
    if random.random() < 0.5:
        challenge = f" {random.choice(_CHALLENGES)}"

    return f"{intro} {career} {love} {health} {spiritual}{challenge}"


def _try_ai_horoscope(sign: str, period_date: str) -> str:
    """Attempt to generate a horoscope using AI. Returns empty string if unavailable."""
    try:
        from app.ai_engine import call_ai
        ruler = _RULERS[sign]
        prompt = (
            f"Generate a Vedic astrology horoscope for {sign.title()} (ruled by {ruler}) "
            f"for {period_date}. Include career, love, health, and spiritual guidance. "
            f"Keep it under 200 words, warm and encouraging with specific planetary references. "
            f"Do not use markdown formatting."
        )
        result = call_ai(prompt)
        if result and len(result) > 50:
            return result
    except Exception:
        pass
    return ""


def generate_daily_horoscopes(db_path: str = None):
    """Generate daily horoscopes for all 12 signs for today. Skips if already exist."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False

    today = date.today().isoformat()

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
            content = _generate_template_horoscope(sign)

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO horoscopes (sign, period_type, period_date, content) VALUES (%s, %s, %s, %s)",
                (sign, "daily", today, content),
            )

    conn.commit()
    conn.close()
    print(f"[horoscope] Generated daily horoscopes for {today}")


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
    print(f"[horoscope] Seeded weekly horoscopes for week of {week_date}")


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


def _template_fallback_sections(sign: str) -> Dict[str, str]:
    """Generate template-based horoscope sections as a fallback."""
    ruler = _RULERS[sign]
    element = _ELEMENTS[sign]

    intro_templates = [
        f"{ruler}'s influence brings transformative energy to {sign.title()} today.",
        f"As a {element} sign ruled by {ruler}, you feel a surge of clarity and purpose.",
        f"The cosmic alignment favors {sign.title()} — {ruler} empowers your natural strengths.",
    ]

    return {
        "general": random.choice(intro_templates) + " " + random.choice(_SPIRITUAL),
        "love": random.choice(_LOVE),
        "career": random.choice(_CAREER),
        "finance": random.choice([
            "Financial matters look favorable; consider long-term investments.",
            "Avoid impulsive spending — plan carefully and save for the future.",
            "Unexpected income or a financial opportunity may present itself.",
            "Review your budget and focus on financial stability this period.",
        ]),
        "health": random.choice(_HEALTH),
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

    # Attempt AI generation
    sections = None
    source = "template"

    try:
        from app.ai_engine import _call_ai

        system_prompt, user_prompt = _build_ai_horoscope_prompt(sign, period, birth_data)
        response = _call_ai(system_prompt, user_prompt, temperature=0.7)

        if response:
            sections = _parse_ai_sections(response)
            if sections:
                source = "ai"
    except Exception:
        pass

    # Fallback to template-based generation
    if sections is None:
        sections = _template_fallback_sections(sign)

    return {
        "sign": sign,
        "period": period,
        "ruling_planet": ruler,
        "element": element,
        "sections": sections,
        "source": source,
        "personalized": birth_data is not None and source == "ai",
    }
