"""Muhurat Finder API — activity-specific auspicious date finder + compatibility routes."""
from __future__ import annotations

import calendar
from datetime import date
from typing import Any

from fastapi import APIRouter, Query, status

from app.panchang_engine import calculate_panchang
from app.muhurat_rules import get_all_activities
from app.muhurat_finder import find_muhurat_dates

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
        "days": _monthly_days(target_year, target_month, latitude, longitude),
    }


@router.get("/api/muhurat/find", status_code=status.HTTP_200_OK)
def muhurat_find(
    event_type: str = Query(default="marriage"),
    date_str: str = Query(alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Daily window compatibility endpoint for a selected date."""
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
def list_activities():
    """List all available muhurat activity types with Hindi translations."""
    return {"activities": get_all_activities()}


@router.get("/api/muhurat/finder", status_code=status.HTTP_200_OK)
def muhurat_finder(
    activity: str = Query(..., description="Activity key (e.g. marriage, griha_pravesh, vehicle_purchase)"),
    month: int = Query(default=None),
    year: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    limit: int = Query(default=15, ge=1, le=31),
):
    """Find auspicious dates for a specific activity in a given month.

    Uses traditional Vedic rules: favorable tithis, nakshatras, weekdays,
    lagnas, and avoids Rahu Kaal, Bhadra, Panchaka, Ganda Moola, etc.
    """
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
    )

