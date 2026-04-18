"""Muhurat Finder API — activity-specific auspicious date finder + compatibility routes."""
from __future__ import annotations

import calendar
import logging
from datetime import date
from typing import Any

from fastapi import APIRouter, Query, Response, status

from app.panchang_engine import calculate_panchang
from app.muhurat_rules import get_all_activities
from app.muhurat_finder import find_muhurat_dates, find_travel_muhurat

logger = logging.getLogger(__name__)

router = APIRouter(tags=["muhurat"])


def _is_auspicious_day(panchang: dict[str, Any]) -> bool:
    tithi = panchang.get("tithi", {}) or {}
    name = str(tithi.get("name", ""))
    paksha = str(tithi.get("paksha", ""))
    return paksha == "Shukla" and name not in {"Ashtami", "Navami", "Chaturdashi"}


def _monthly_days(year: int, month: int, latitude: float, longitude: float) -> list[dict[str, Any]]:
    total_days = calendar.monthrange(year, month)[1]
    days: list[dict[str, Any]] = []
    for day in range(1, total_days + 1):
        d = date(year, month, day).isoformat()
        panchang = calculate_panchang(d, latitude, longitude)
        ok = _is_auspicious_day(panchang)
        days.append(
            {
                "date": d,
                "has_muhurat": ok,
                "quality": "good" if ok else "poor",
                "windows_count": 1 if ok else 0,
                "tithi": (panchang.get("tithi", {}) or {}).get("name", ""),
                "nakshatra": (panchang.get("nakshatra", {}) or {}).get("name", ""),
            }
        )
    return days


@router.get("/api/muhurat/monthly", status_code=status.HTTP_200_OK)
def muhurat_monthly(
    event_type: str = Query(default="marriage"),
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    response: Response = None,
):
    """⚠ DEPRECATED: Use /api/muhurat/finder instead.

    Monthly calendar-style muhurat compatibility endpoint (simplified logic).
    This endpoint uses basic Shukla Paksha + tithi checks only.
    For full activity-specific rules, use /api/muhurat/finder."""
    # Add deprecation headers
    if response:
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = "2026-12-31T23:59:59Z"
        response.headers["Link"] = '</api/muhurat/finder>; rel="successor-version"'

    logger.warning(
        f"DEPRECATED: /api/muhurat/monthly called with event_type={event_type}. "
        "Use /api/muhurat/finder instead for activity-specific muhurat rules."
    )

    today = date.today()
    target_year = year or today.year
    target_month = month or today.month
    if target_month < 1 or target_month > 12:
        return {"event_type": event_type, "days": []}
    return {
        "event_type": event_type,
        "year": target_year,
        "month": target_month,
        "days": _monthly_days(target_year, target_month, latitude, longitude),
    }


@router.get("/api/muhurat/find", status_code=status.HTTP_200_OK)
def muhurat_find(
    event_type: str = Query(default="marriage"),
    date_str: str = Query(alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    response: Response = None,
):
    """⚠ DEPRECATED: Use /api/muhurat/finder instead.

    Daily window compatibility endpoint for a selected date (simplified logic).
    This endpoint uses basic Shukla Paksha + tithi checks only.
    For full activity-specific rules, use /api/muhurat/finder with ?activity="""
    # Add deprecation headers
    if response:
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = "2026-12-31T23:59:59Z"
        response.headers["Link"] = '</api/muhurat/finder>; rel="successor-version"'

    logger.warning(
        f"DEPRECATED: /api/muhurat/find called with event_type={event_type}, date={date_str}. "
        "Use /api/muhurat/finder with ?activity= parameter instead for activity-specific rules."
    )

    panchang = calculate_panchang(date_str, latitude, longitude)
    tithi = (panchang.get("tithi", {}) or {}).get("name", "")
    nak = (panchang.get("nakshatra", {}) or {}).get("name", "")
    ok = _is_auspicious_day(panchang)
    windows = []
    if ok:
        windows.append(
            {
                "start_time": panchang.get("sunrise", "--:--"),
                "end_time": panchang.get("sunset", "--:--"),
                "quality": "good",
                "factors": [f"{tithi} {nak}".strip()],
            }
        )
    return {"event_type": event_type, "date": date_str, "windows": windows}


# ============================================================
# NEW: Activity-specific Muhurat Finder (rules-based)
# ============================================================

@router.get("/api/muhurat/activities", status_code=status.HTTP_200_OK)
def list_activities(lang: str = Query(default="en")):
    """List all available muhurat activity types with localization."""
    activities = get_all_activities()
    if lang == "hi":
        return {
            "activities": [
                {
                    "key": a["key"],
                    "name": a.get("name_hindi", a["name"]),
                    "description": a.get("description_hindi", a["description"]),
                    "icon": a["icon"]
                }
                for a in activities
            ]
        }
    return {
        "activities": [
            {
                "key": a["key"],
                "name": a["name"],
                "description": a["description"],
                "icon": a["icon"]
            }
            for a in activities
        ]
    }


@router.get("/api/muhurat/finder", status_code=status.HTTP_200_OK)
def muhurat_finder(
    activity: str = Query(..., description="Activity key (e.g. marriage, griha_pravesh, vehicle_purchase)"),
    month: int = Query(default=None),
    year: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    limit: int = Query(default=15, ge=1, le=31),
    birth_moon_rashi: int = Query(default=None, ge=0, le=11,
        description="Birth Moon rashi index (0=Aries … 11=Pisces) for Chandra Balam"),
    birth_nakshatra: int = Query(default=None, ge=0, le=26,
        description="Birth nakshatra index (0=Ashwini … 26=Revati) for Tara Balam"),
):
    """Find auspicious dates for a specific activity in a given month.

    Uses traditional Vedic rules: favorable tithis, nakshatras, weekdays,
    lagnas, and avoids Rahu Kaal, Bhadra, Panchaka, Ganda Moola, Sankranti,
    Dagdha Tithi, Guru/Shukra Asta, Guru Vakri, Shani Vakri, Kula Kanthaka,
    Simha Surya.

    Pass birth_moon_rashi + birth_nakshatra for personalised Chandra Balam
    and Tara Balam scoring.
    """
    from fastapi import HTTPException
    if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
        raise HTTPException(status_code=400, detail="Invalid latitude/longitude range")
    today = date.today()
    target_month = month or today.month
    target_year = year or today.year

    if not (1 <= target_month <= 12):
        return {"error": f"Invalid month: {target_month}", "dates": []}

    return find_muhurat_dates(
        activity_key=activity,
        month=target_month,
        year=target_year,
        latitude=latitude,
        longitude=longitude,
        limit=limit,
        birth_moon_rashi=birth_moon_rashi,
        birth_nakshatra=birth_nakshatra,
    )


@router.get("/api/muhurat/travel", status_code=status.HTTP_200_OK)
def travel_muhurat(
    direction: str = Query(..., description="Travel direction: East, West, North, South, NE, NW, SE, SW"),
    month: int = Query(default=None),
    year: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    limit: int = Query(default=15, ge=1, le=31),
):
    """Find auspicious travel dates for a specific direction."""
    from fastapi import HTTPException
    if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
        raise HTTPException(status_code=400, detail="Invalid latitude/longitude range")
    today = date.today()
    target_month = month or today.month
    target_year = year or today.year
    if not (1 <= target_month <= 12):
        return {"error": f"Invalid month: {target_month}", "dates": []}
    return find_travel_muhurat(
        direction=direction,
        month=target_month,
        year=target_year,
        latitude=latitude,
        longitude=longitude,
        limit=limit,
    )
