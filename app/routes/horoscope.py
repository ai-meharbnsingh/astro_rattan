"""Horoscope routes — daily, weekly, all-signs, and transit-aware horoscopes."""
from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.horoscope_generator import (
    SIGNS,
    generate_ai_horoscope,
    _get_current_transits,
    _RULERS,
    _ELEMENTS,
    _EXALTED_SIGNS,
    _DEBILITATED_SIGNS,
    _OWN_SIGNS,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["horoscope"])

# Hindi sign names for bilingual support
SIGN_HINDI = {
    "aries": "मेष", "taurus": "वृषभ", "gemini": "मिथुन", "cancer": "कर्क",
    "leo": "सिंह", "virgo": "कन्या", "libra": "तुला", "scorpio": "वृश्चिक",
    "sagittarius": "धनु", "capricorn": "मकर", "aquarius": "कुंभ", "pisces": "मीन",
}

SIGN_EMOJI = {
    "aries": "\u2648", "taurus": "\u2649", "gemini": "\u264A", "cancer": "\u264B",
    "leo": "\u264C", "virgo": "\u264D", "libra": "\u264E", "scorpio": "\u264F",
    "sagittarius": "\u2650", "capricorn": "\u2651", "aquarius": "\u2652", "pisces": "\u2653",
}

SIGN_DATES = {
    "aries": "Mar 21 - Apr 19", "taurus": "Apr 20 - May 20",
    "gemini": "May 21 - Jun 20", "cancer": "Jun 21 - Jul 22",
    "leo": "Jul 23 - Aug 22", "virgo": "Aug 23 - Sep 22",
    "libra": "Sep 23 - Oct 22", "scorpio": "Oct 23 - Nov 21",
    "sagittarius": "Nov 22 - Dec 21", "capricorn": "Dec 22 - Jan 19",
    "aquarius": "Jan 20 - Feb 18", "pisces": "Feb 19 - Mar 20",
}

RULER_HINDI = {
    "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "बृहस्पति", "Venus": "शुक्र", "Saturn": "शनि",
}

ELEMENT_HINDI = {
    "fire": "अग्नि", "earth": "पृथ्वी", "air": "वायु", "water": "जल",
}


def _sign_meta(sign: str) -> dict:
    """Return metadata for a zodiac sign."""
    return {
        "sign": sign,
        "sign_hindi": SIGN_HINDI.get(sign, sign),
        "emoji": SIGN_EMOJI.get(sign, ""),
        "dates": SIGN_DATES.get(sign, ""),
        "ruling_planet": _RULERS.get(sign, ""),
        "ruling_planet_hindi": RULER_HINDI.get(_RULERS.get(sign, ""), ""),
        "element": _ELEMENTS.get(sign, ""),
        "element_hindi": ELEMENT_HINDI.get(_ELEMENTS.get(sign, ""), ""),
    }


@router.get("/api/horoscope/daily", status_code=status.HTTP_200_OK)
def get_daily_horoscope(
    sign: str = Query(..., description="Zodiac sign (e.g. aries)"),
    target_date: str = Query(None, alias="date", description="Date YYYY-MM-DD (default today)"),
    lang: str = Query("en", description="Language: en or hi"),
    db: Any = Depends(get_db),
):
    """Get daily horoscope for a specific sign and date."""
    sign = sign.strip().lower()
    if sign not in SIGNS:
        raise HTTPException(status_code=400, detail=f"Invalid sign: {sign}")
    lang = lang.strip().lower() if lang else "en"
    if lang not in ("en", "hi"):
        lang = "en"

    if not target_date:
        target_date = date.today().isoformat()

    # Try transit engine for rich response
    try:
        from app.transit_engine import generate_transit_horoscope
        result = generate_transit_horoscope(sign=sign, period="daily", target_date=target_date)
        if result and result.get("sections"):
            # Return bilingual sections — frontend txt() helper handles language selection
            return {
                **_sign_meta(sign),
                "period": "daily",
                "date": target_date,
                "sections": result.get("sections", {}),
                "scores": result.get("scores", {}),
                "mood": result.get("mood", {}),
                "lucky": result.get("lucky", {}),
                "dos": result.get("dos", []),
                "donts": result.get("donts", []),
                "source": result.get("source", "transit_engine"),
            }
    except Exception:
        logger.exception("Transit engine failed for daily %s/%s", sign, target_date)

    # Fallback: existing DB + template logic
    row = db.execute(
        "SELECT content, created_at FROM horoscopes WHERE sign = %s AND period_type = 'daily' AND period_date = %s",
        (sign, target_date),
    ).fetchone()

    if row:
        sections = _parse_content_to_sections(row["content"])
        if _has_meaningful_sections(sections):
            return {
                **_sign_meta(sign),
                "period": "daily",
                "date": target_date,
                "sections": sections,
                "source": "database",
            }

    # Generate on-the-fly via template engine
    generated = generate_ai_horoscope(sign=sign, period="daily")
    return {
        **_sign_meta(sign),
        "period": "daily",
        "date": target_date,
        "sections": generated.get("sections", {}),
        "source": generated.get("source", "template"),
    }


@router.get("/api/horoscope/weekly", status_code=status.HTTP_200_OK)
def get_weekly_horoscope(
    sign: str = Query(..., description="Zodiac sign (e.g. aries)"),
    lang: str = Query("en", description="Language: en or hi"),
    db: Any = Depends(get_db),
):
    """Get weekly horoscope for a specific sign."""
    sign = sign.strip().lower()
    if sign not in SIGNS:
        raise HTTPException(status_code=400, detail=f"Invalid sign: {sign}")
    lang = lang.strip().lower() if lang else "en"
    if lang not in ("en", "hi"):
        lang = "en"

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_date = monday.isoformat()
    week_end = (monday + timedelta(days=6)).isoformat()

    # Try transit engine for rich response
    try:
        from app.transit_engine import generate_transit_horoscope
        result = generate_transit_horoscope(sign=sign, period="weekly", target_date=week_date)
        if result and result.get("sections"):
            # Return bilingual sections — frontend txt() helper handles language selection
            return {
                **_sign_meta(sign),
                "period": "weekly",
                "week_start": week_date,
                "week_end": week_end,
                "sections": result.get("sections", {}),
                "scores": result.get("scores", {}),
                "mood": result.get("mood", {}),
                "lucky": result.get("lucky", {}),
                "dos": result.get("dos", []),
                "donts": result.get("donts", []),
                "source": result.get("source", "transit_engine"),
            }
    except Exception:
        logger.exception("Transit engine failed for weekly %s", sign)

    # Fallback: existing DB + template logic
    row = db.execute(
        "SELECT content, created_at FROM horoscopes WHERE sign = %s AND period_type = 'weekly' AND period_date = %s",
        (sign, week_date),
    ).fetchone()

    if row:
        sections = _parse_content_to_sections(row["content"])
        if _has_meaningful_sections(sections):
            return {
                **_sign_meta(sign),
                "period": "weekly",
                "week_start": week_date,
                "week_end": week_end,
                "sections": sections,
                "source": "database",
            }

    generated = generate_ai_horoscope(sign=sign, period="weekly")
    return {
        **_sign_meta(sign),
        "period": "weekly",
        "week_start": week_date,
        "week_end": week_end,
        "sections": generated.get("sections", {}),
        "source": generated.get("source", "template"),
    }


@router.get("/api/horoscope/monthly", status_code=status.HTTP_200_OK)
def get_monthly_horoscope(
    sign: str = Query(..., description="Zodiac sign (e.g. aries)"),
    lang: str = Query("en", description="Language: en or hi"),
    db: Any = Depends(get_db),
):
    """Get monthly horoscope for a specific sign."""
    sign = sign.strip().lower()
    if sign not in SIGNS:
        raise HTTPException(status_code=400, detail=f"Invalid sign: {sign}")
    lang = lang.strip().lower() if lang else "en"
    if lang not in ("en", "hi"):
        lang = "en"

    today = date.today()
    month_start = today.replace(day=1).isoformat()

    # Try transit engine for rich response
    try:
        from app.transit_engine import generate_transit_horoscope
        result = generate_transit_horoscope(sign=sign, period="monthly", target_date=month_start)
        if result and result.get("sections"):
            # Return bilingual sections — frontend txt() helper handles language selection
            response = {
                **_sign_meta(sign),
                "period": "monthly",
                "month_start": month_start,
                "sections": result.get("sections", {}),
                "scores": result.get("scores", {}),
                "mood": result.get("mood", {}),
                "lucky": result.get("lucky", {}),
                "dos": result.get("dos", []),
                "donts": result.get("donts", []),
                "source": result.get("source", "transit_engine"),
            }

            # Monthly extras: phases and key_dates
            try:
                from app.transit_engine import generate_monthly_extras
                extras = generate_monthly_extras(sign=sign, target_date=month_start)
                response["phases"] = extras.get("phases", [])
                response["key_dates"] = extras.get("key_dates", [])
            except Exception:
                logger.exception("Monthly extras failed for %s", sign)
                response["phases"] = []
                response["key_dates"] = []

            return response
    except Exception:
        logger.exception("Transit engine failed for monthly %s", sign)

    # Fallback: existing DB + template logic
    row = db.execute(
        "SELECT content, created_at FROM horoscopes WHERE sign = %s AND period_type = 'monthly' AND period_date = %s",
        (sign, month_start),
    ).fetchone()

    if row:
        sections = _parse_content_to_sections(row["content"])
        if _has_meaningful_sections(sections):
            return {
                **_sign_meta(sign),
                "period": "monthly",
                "month_start": month_start,
                "sections": sections,
                "source": "database",
            }

    generated = generate_ai_horoscope(sign=sign, period="monthly")
    return {
        **_sign_meta(sign),
        "period": "monthly",
        "month_start": month_start,
        "sections": generated.get("sections", {}),
        "source": generated.get("source", "template"),
    }


@router.get("/api/horoscope/yearly", status_code=status.HTTP_200_OK)
def get_yearly_horoscope(
    sign: str = Query(..., description="Zodiac sign (e.g. aries)"),
    lang: str = Query("en", description="Language: en or hi"),
    db: Any = Depends(get_db),
):
    """Get yearly horoscope for a specific sign."""
    sign = sign.strip().lower()
    if sign not in SIGNS:
        raise HTTPException(status_code=400, detail=f"Invalid sign: {sign}")
    lang = lang.strip().lower() if lang else "en"
    if lang not in ("en", "hi"):
        lang = "en"

    year_start = date.today().replace(month=1, day=1).isoformat()

    # Try transit engine for rich response
    try:
        from app.transit_engine import generate_transit_horoscope
        result = generate_transit_horoscope(sign=sign, period="yearly", target_date=year_start)
        if result and result.get("sections"):
            # Return bilingual sections — frontend txt() helper handles language selection
            response = {
                **_sign_meta(sign),
                "period": "yearly",
                "year_start": year_start,
                "sections": result.get("sections", {}),
                "scores": result.get("scores", {}),
                "mood": result.get("mood", {}),
                "lucky": result.get("lucky", {}),
                "dos": result.get("dos", []),
                "donts": result.get("donts", []),
                "source": result.get("source", "transit_engine"),
            }

            # Yearly extras: quarters, best_months, annual_theme
            try:
                from app.transit_engine import generate_yearly_extras
                extras = generate_yearly_extras(sign=sign)
                response["quarters"] = extras.get("quarters", [])
                response["best_months"] = extras.get("best_months", {})
                response["annual_theme"] = extras.get("annual_theme", {})
            except Exception:
                logger.exception("Yearly extras failed for %s", sign)
                response["quarters"] = []
                response["best_months"] = {}
                response["annual_theme"] = {}

            return response
    except Exception:
        logger.exception("Transit engine failed for yearly %s", sign)

    # Fallback: existing DB + template logic
    row = db.execute(
        "SELECT content, created_at FROM horoscopes WHERE sign = %s AND period_type = 'yearly' AND period_date = %s",
        (sign, year_start),
    ).fetchone()

    if row:
        sections = _parse_content_to_sections(row["content"])
        if _has_meaningful_sections(sections):
            return {
                **_sign_meta(sign),
                "period": "yearly",
                "year_start": year_start,
                "sections": sections,
                "source": "database",
            }

    generated = generate_ai_horoscope(sign=sign, period="yearly")
    return {
        **_sign_meta(sign),
        "period": "yearly",
        "year_start": year_start,
        "sections": generated.get("sections", {}),
        "source": generated.get("source", "template"),
    }


@router.get("/api/horoscope/all", status_code=status.HTTP_200_OK)
def get_all_signs_horoscope(
    period: str = Query("daily", description="daily or weekly"),
    target_date: str = Query(None, alias="date", description="Date YYYY-MM-DD (default today)"),
    db: Any = Depends(get_db),
):
    """Get horoscopes for all 12 signs at once."""
    if period not in ("daily", "weekly"):
        raise HTTPException(status_code=400, detail="period must be daily or weekly")

    if not target_date:
        target_date = date.today().isoformat()

    if period == "weekly":
        d = date.fromisoformat(target_date)
        target_date = (d - timedelta(days=d.weekday())).isoformat()

    # Batch fetch from DB
    rows = db.execute(
        "SELECT sign, content FROM horoscopes WHERE period_type = %s AND period_date = %s",
        (period, target_date),
    ).fetchall()
    db_map = {r["sign"]: r["content"] for r in rows}

    results = []
    for sign in SIGNS:
        content = db_map.get(sign)
        if content:
            sections = _parse_content_to_sections(content)
            source = "database"
        else:
            generated = generate_ai_horoscope(sign=sign, period=period)
            sections = generated.get("sections", {})
            source = generated.get("source", "template")

        # Build a compact summary from the general section
        general = sections.get("general", "")
        summary = general[:160] + "..." if len(general) > 160 else general

        results.append({
            **_sign_meta(sign),
            "summary": summary,
            "sections": sections,
            "source": source,
        })

    return {
        "period": period,
        "date": target_date,
        "signs": results,
    }


@router.get("/api/horoscope/transits", status_code=status.HTTP_200_OK)
def get_transit_insights():
    """Get current planetary transits and their effects on each sign."""
    try:
        transits = _get_current_transits()
    except Exception:
        transits = {}

    sign_effects = []
    for sign in SIGNS:
        ruler = _RULERS.get(sign, "")
        ruler_sign = transits.get(ruler, "").lower()
        element = _ELEMENTS.get(sign, "")

        is_exalted = _EXALTED_SIGNS.get(ruler) == ruler_sign
        is_debilitated = _DEBILITATED_SIGNS.get(ruler) == ruler_sign
        is_own = ruler_sign in _OWN_SIGNS.get(ruler, [])

        if is_exalted:
            dignity = "exalted"
            strength = "very_strong"
        elif is_own:
            dignity = "own_sign"
            strength = "strong"
        elif is_debilitated:
            dignity = "debilitated"
            strength = "weak"
        else:
            dignity = "neutral"
            strength = "moderate"

        sign_effects.append({
            **_sign_meta(sign),
            "ruler_current_sign": ruler_sign.title() if ruler_sign else "Unknown",
            "ruler_current_sign_hindi": SIGN_HINDI.get(ruler_sign, ruler_sign.title() if ruler_sign else ""),
            "dignity": dignity,
            "strength": strength,
        })

    # Format transit positions
    transit_list = []
    for planet, sign_name in transits.items():
        transit_list.append({
            "planet": planet,
            "planet_hindi": RULER_HINDI.get(planet, planet),
            "current_sign": sign_name.title(),
            "current_sign_hindi": SIGN_HINDI.get(sign_name, sign_name.title()),
        })

    return {
        "date": date.today().isoformat(),
        "transits": transit_list,
        "sign_effects": sign_effects,
    }


def _parse_content_to_sections(content: str) -> dict:
    """Parse stored horoscope content (plain text) into sectioned format."""
    # If content is already short/simple, treat as general
    if not content or len(content) < 50:
        return {"general": content or "", "love": "", "career": "", "finance": "", "health": ""}

    # Try to split intelligently: look for sentence boundaries
    sentences = [s.strip() for s in content.replace(". ", ".|").split("|") if s.strip()]

    if len(sentences) >= 5:
        return {
            "general": ". ".join(sentences[:2]).rstrip(".") + ".",
            "career": sentences[2] if len(sentences) > 2 else "",
            "love": sentences[3] if len(sentences) > 3 else "",
            "health": sentences[4] if len(sentences) > 4 else "",
            "finance": sentences[5] if len(sentences) > 5 else "",
        }

    return {"general": content, "love": "", "career": "", "finance": "", "health": ""}


def _has_meaningful_sections(sections: dict | None) -> bool:
    """Return True when at least one section has useful text."""
    if not isinstance(sections, dict):
        return False
    for key in ("general", "love", "career", "finance", "health"):
        value = str(sections.get(key, "")).strip()
        if len(value) >= 15:
            return True
    return False
