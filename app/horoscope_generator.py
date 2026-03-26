"""H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes."""
import random
import sqlite3
from datetime import date, timedelta
from typing import List

from app.config import DB_PATH

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
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")

    today = date.today().isoformat()

    existing = conn.execute(
        "SELECT COUNT(*) FROM horoscopes WHERE period_type = 'daily' AND period_date = ?",
        (today,),
    ).fetchone()[0]

    if existing >= 12:
        conn.close()
        return

    for sign in SIGNS:
        # Check if this specific sign already has today's horoscope
        row = conn.execute(
            "SELECT id FROM horoscopes WHERE sign = ? AND period_type = 'daily' AND period_date = ?",
            (sign, today),
        ).fetchone()
        if row:
            continue

        # Try AI first, fall back to templates
        content = _try_ai_horoscope(sign, today)
        if not content:
            content = _generate_template_horoscope(sign)

        conn.execute(
            "INSERT INTO horoscopes (sign, period_type, period_date, content) VALUES (?, ?, ?, ?)",
            (sign, "daily", today, content),
        )

    conn.commit()
    conn.close()
    print(f"[horoscope] Generated daily horoscopes for {today}")


def seed_weekly_horoscopes(db_path: str = None):
    """Seed 12 weekly horoscopes as initial content."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")

    # Monday of current week
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_date = monday.isoformat()

    existing = conn.execute(
        "SELECT COUNT(*) FROM horoscopes WHERE period_type = 'weekly' AND period_date = ?",
        (week_date,),
    ).fetchone()[0]

    if existing >= 12:
        conn.close()
        return

    for sign in SIGNS:
        row = conn.execute(
            "SELECT id FROM horoscopes WHERE sign = ? AND period_type = 'weekly' AND period_date = ?",
            (sign, week_date),
        ).fetchone()
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

        conn.execute(
            "INSERT INTO horoscopes (sign, period_type, period_date, content) VALUES (?, ?, ?, ?)",
            (sign, "weekly", week_date, content),
        )

    conn.commit()
    conn.close()
    print(f"[horoscope] Seeded weekly horoscopes for week of {week_date}")
