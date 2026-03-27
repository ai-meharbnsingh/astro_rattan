"""Horoscope routes — daily/weekly/monthly/yearly horoscope by zodiac sign."""
from typing import Any
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.horoscope_generator import generate_ai_horoscope
from app.models import ZodiacSign, HoroscopePeriod

router = APIRouter(prefix="/api/horoscope", tags=["horoscope"])


def _current_period_date(period: str) -> str:
    """Return the canonical period date string for the current day."""
    today = date.today()
    if period == "daily":
        return today.isoformat()
    elif period == "weekly":
        # Monday of the current week
        monday = today - __import__("datetime").timedelta(days=today.weekday())
        return monday.isoformat()
    elif period == "monthly":
        return today.replace(day=1).isoformat()
    elif period == "yearly":
        return today.replace(month=1, day=1).isoformat()
    return today.isoformat()


# Default horoscope content when no DB entry exists
_DEFAULT_HOROSCOPES = {
    "aries": "A day of new beginnings. Mars energizes your ambitions — take bold action.",
    "taurus": "Focus on stability and comfort. Venus invites you to nurture your senses.",
    "gemini": "Communication is key today. Mercury sharpens your wit and social connections.",
    "cancer": "Emotions run deep. The Moon highlights home, family, and inner reflection.",
    "leo": "Your confidence shines. The Sun empowers you to lead and inspire others.",
    "virgo": "Attention to detail pays off. Mercury guides your analytical skills today.",
    "libra": "Seek balance and harmony. Venus encourages beautiful partnerships and diplomacy.",
    "scorpio": "Transformation is in the air. Pluto deepens your intensity and focus.",
    "sagittarius": "Adventure calls. Jupiter expands your horizons — embrace exploration.",
    "capricorn": "Discipline and hard work bring rewards. Saturn strengthens your resolve.",
    "aquarius": "Innovation and originality are favored. Uranus sparks your visionary ideas.",
    "pisces": "Intuition is your guide. Neptune enhances your creativity and spiritual awareness.",
}


@router.get("/ai/{sign}", status_code=status.HTTP_200_OK)
def get_ai_horoscope(
    sign: ZodiacSign,
    period: HoroscopePeriod = Query(default=HoroscopePeriod.daily),
    birth_date: Optional[str] = Query(default=None, description="Birth date (YYYY-MM-DD)"),
    birth_time: Optional[str] = Query(default=None, description="Birth time (HH:MM)"),
    birth_place: Optional[str] = Query(default=None, description="Birth place"),
):
    """Get AI-personalized horoscope for a zodiac sign with sectioned content.

    Returns personalized horoscope with sections: general, love, career, finance, health.
    Falls back to template-based generation if AI is unavailable.
    """
    birth_data = None
    if birth_date or birth_time or birth_place:
        birth_data = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_place": birth_place,
        }

    try:
        result = generate_ai_horoscope(
            sign=sign.value,
            period=period.value,
            birth_data=birth_data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return result


@router.get("/{sign}", status_code=status.HTTP_200_OK)
def get_horoscope(
    sign: ZodiacSign,
    period: HoroscopePeriod = Query(default=HoroscopePeriod.daily),
    db: Any = Depends(get_db),
):
    """Get horoscope for a zodiac sign and period (daily/weekly/monthly/yearly)."""
    period_date = _current_period_date(period.value)

    row = db.execute(
        "SELECT * FROM horoscopes WHERE sign = %s AND period_type = %s AND period_date = %s",
        (sign.value, period.value, period_date),
    ).fetchone()

    if row:
        return {
            "sign": row["sign"],
            "period": row["period_type"],
            "content": row["content"],
            "date": row["period_date"],
        }

    # Return default content when no curated horoscope exists
    return {
        "sign": sign.value,
        "period": period.value,
        "content": _DEFAULT_HOROSCOPES.get(sign.value, "The stars are aligning in your favor."),
        "date": period_date,
    }
