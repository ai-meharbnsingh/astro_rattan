"""Muhurat Finder API — activity-specific auspicious date finder + compatibility routes."""
from __future__ import annotations

import calendar
from datetime import date
from typing import Any

from fastapi import APIRouter, Query, status

from app.panchang_engine import calculate_panchang
from app.muhurat_rules import get_all_activities
from app.muhurat_finder import find_muhurat_dates, find_travel_muhurat

router = APIRouter(tags=["muhurat"])


def _monthly_days(year: int, month: int, latitude: float, longitude: float, event_type: str = "marriage") -> list[dict[str, Any]]:
    full_result = find_muhurat_dates(
        activity_key=event_type,
        month=month,
        year=year,
        latitude=latitude,
        longitude=longitude,
        limit=31,
    )
    if "error" in full_result:
        # Unknown activity — fall back to simple paksha+tithi check
        total_days = calendar.monthrange(year, month)[1]
        days: list[dict[str, Any]] = []
        for day in range(1, total_days + 1):
            d_str = date(year, month, day).isoformat()
            panchang = calculate_panchang(d_str, latitude, longitude)
            tithi = panchang.get("tithi", {}) or {}
            ok = (tithi.get("paksha") == "Shukla"
                  and tithi.get("name") not in {"Ashtami", "Navami", "Chaturdashi"})
            days.append({
                "date": d_str,
                "has_muhurat": ok,
                "quality": "good" if ok else "poor",
                "windows_count": 1 if ok else 0,
                "tithi": tithi.get("name", ""),
                "nakshatra": (panchang.get("nakshatra", {}) or {}).get("name", ""),
            })
        return days

    dates_map: dict[str, dict[str, Any]] = {e["date"]: e for e in full_result.get("dates", [])}
    total_days = calendar.monthrange(year, month)[1]
    days = []
    for day in range(1, total_days + 1):
        d_str = date(year, month, day).isoformat()
        entry = dates_map.get(d_str)
        if entry:
            score = entry.get("score", 0)
            ok = score >= 50
            days.append({
                "date": d_str,
                "has_muhurat": ok,
                "quality": entry.get("quality", "good" if ok else "poor"),
                "windows_count": 1 if ok else 0,
                "tithi": entry.get("tithi", ""),
                "nakshatra": entry.get("nakshatra", ""),
                "score": score,
            })
        else:
            # Hard-blocked (Chaturmasa, Sankranti window, etc.)
            days.append({
                "date": d_str,
                "has_muhurat": False,
                "quality": "poor",
                "windows_count": 0,
                "tithi": "",
                "nakshatra": "",
                "score": 0,
            })
    return days


@router.get("/api/muhurat/monthly", status_code=status.HTTP_200_OK)
def muhurat_monthly(
    event_type: str = Query(default="marriage"),
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Monthly calendar-style muhurat compatibility endpoint."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month
    if target_month < 1 or target_month > 12:
        return {"event_type": event_type, "days": []}
    return {
        "event_type": event_type,
        "year": target_year,
        "month": target_month,
        "days": _monthly_days(target_year, target_month, latitude, longitude, event_type),
    }


@router.get("/api/muhurat/find", status_code=status.HTTP_200_OK)
def muhurat_find(
    event_type: str = Query(default="marriage"),
    date_str: str = Query(alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Daily window compatibility endpoint for a selected date."""
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return {"event_type": event_type, "date": date_str, "windows": []}

    full_result = find_muhurat_dates(
        activity_key=event_type,
        month=d.month,
        year=d.year,
        latitude=latitude,
        longitude=longitude,
        limit=31,
    )
    entry = next((e for e in full_result.get("dates", []) if e["date"] == date_str), None)

    windows = []
    if entry and entry.get("score", 0) >= 50:
        windows.append({
            "start_time": entry.get("sunrise", "--:--"),
            "end_time": entry.get("sunset", "--:--"),
            "quality": entry.get("quality", "good"),
            "factors": (entry.get("reasons_good") or [])[:3],
        })
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
    """Find auspicious travel dates for a specific direction.

    Uses the Travel Muhurta rules from Muhurt Chintamani (Prakarana 10):
    direction-specific nakshatra matching + Pushya nakshatra bonus.
    """
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

