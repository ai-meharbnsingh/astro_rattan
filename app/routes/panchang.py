"""Panchang routes — daily panchang, choghadiya, muhurat, sunrise, festivals, and monthly view."""
import json
import calendar
from typing import Any
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.panchang_engine import (
    calculate_panchang,
    calculate_rahu_kaal,
    calculate_choghadiya,
    calculate_gulika_kaal,
    calculate_yamaganda,
    calculate_planetary_positions,
)
from app.festival_engine import detect_festivals

router = APIRouter(tags=["panchang"])


def _today() -> str:
    return date.today().isoformat()


def _parse_date(date_str: str) -> datetime:
    """Parse a date string, raising HTTPException on invalid format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD.",
        )


# ============================================================
# GET /api/panchang -- Full daily panchang (enhanced)
# ============================================================

@router.get("/api/panchang", status_code=status.HTTP_200_OK)
def get_panchang(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: Any = Depends(get_db),
):
    """Calculate complete Panchang for a given date and location."""
    target_date = date_str or _today()
    _parse_date(target_date)

    # Check cache first
    cached = db.execute(
        "SELECT * FROM panchang_cache WHERE date = %s AND latitude = %s AND longitude = %s",
        (target_date, latitude, longitude),
    ).fetchone()

    # Serve from cache only if it has extended data (new engine format)
    raw_ext_check = cached.get("choghadiya", "") if cached else ""
    cache_has_extended = cached and raw_ext_check and raw_ext_check not in ("", "[]")

    if cache_has_extended:
        tithi = cached["tithi"]
        if isinstance(tithi, str):
            tithi = json.loads(tithi)
        nakshatra = cached["nakshatra"]
        if isinstance(nakshatra, str):
            nakshatra = json.loads(nakshatra)
        yoga = cached["yoga"]
        if isinstance(yoga, str):
            yoga = json.loads(yoga)
        karana = cached["karana"]
        if isinstance(karana, str):
            karana = json.loads(karana)
        rahu_kaal = cached["rahu_kaal"]
        if isinstance(rahu_kaal, str):
            rahu_kaal = json.loads(rahu_kaal)

        # Try to load extended data from choghadiya column (stores full JSON now)
        extended = {}
        raw_ext = cached.get("choghadiya", "")
        if raw_ext and raw_ext != "[]":
            try:
                extended = json.loads(raw_ext) if isinstance(raw_ext, str) else raw_ext
            except (json.JSONDecodeError, TypeError):
                extended = {}

        result = {
            "date": cached["date"],
            "latitude": cached["latitude"],
            "longitude": cached["longitude"],
            "tithi": tithi,
            "nakshatra": nakshatra,
            "yoga": yoga,
            "karana": karana,
            "rahu_kaal": rahu_kaal,
            "sunrise": cached["sunrise"],
            "sunset": cached["sunset"],
            "moonrise": cached.get("moonrise", "--:--"),
            "moonset": cached.get("moonset", "--:--"),
        }
        # Merge extended data if present
        if isinstance(extended, dict):
            result.update(extended)
        return result

    # Calculate fresh
    panchang = calculate_panchang(target_date, latitude, longitude)

    # Detect festivals
    festivals = detect_festivals(
        tithi_name=panchang["tithi"]["name"],
        paksha=panchang["tithi"]["paksha"],
        nakshatra_name=panchang["nakshatra"]["name"],
        maas=panchang.get("hindu_calendar", {}).get("maas", ""),
    )
    panchang["festivals"] = festivals

    # Build extended data for cache (everything beyond core fields)
    extended_data = {
        "vaar": panchang.get("vaar"),
        "gulika_kaal": panchang.get("gulika_kaal"),
        "yamaganda": panchang.get("yamaganda"),
        "abhijit_muhurat": panchang.get("abhijit_muhurat"),
        "brahma_muhurat": panchang.get("brahma_muhurat"),
        "planetary_positions": panchang.get("planetary_positions"),
        "hindu_calendar": panchang.get("hindu_calendar"),
        "choghadiya": panchang.get("choghadiya"),
        "festivals": festivals,
        "ayanamsa": panchang.get("ayanamsa"),
        "sun_longitude": panchang.get("sun_longitude"),
        "moon_longitude": panchang.get("moon_longitude"),
    }

    # Cache the result
    tithi_str = json.dumps(panchang["tithi"])
    nak_str = json.dumps(panchang["nakshatra"])
    yoga_str = json.dumps(panchang["yoga"])
    karana_str = json.dumps(panchang["karana"])
    rahu_str = json.dumps(panchang.get("rahu_kaal", {}))
    extended_str = json.dumps(extended_data, default=str)

    db.execute(
        """INSERT INTO panchang_cache
           (date, latitude, longitude, tithi, nakshatra, yoga, karana,
            rahu_kaal, choghadiya, sunrise, sunset, moonrise, moonset)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (date, latitude, longitude) DO NOTHING""",
        (
            target_date, latitude, longitude,
            tithi_str, nak_str, yoga_str, karana_str,
            rahu_str, "[]",
            panchang["sunrise"], panchang["sunset"],
            panchang.get("moonrise", "--:--"),
            panchang.get("moonset", "--:--"),
        ),
    )
    db.commit()

    # Build full response
    return {
        "date": target_date,
        "latitude": latitude,
        "longitude": longitude,
        **panchang,
        "festivals": festivals,
    }


# ============================================================
# GET /api/panchang/month -- Monthly panchang overview
# ============================================================

@router.get("/api/panchang/month", status_code=status.HTTP_200_OK)
def get_monthly_panchang(
    month: int = Query(default=None),
    year: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Get panchang summary for each day of a month."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    if not (1 <= target_month <= 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid month: {target_month}. Must be 1-12.",
        )

    days_in_month = calendar.monthrange(target_year, target_month)[1]
    days = []

    for day in range(1, days_in_month + 1):
        d = date(target_year, target_month, day)
        d_str = d.isoformat()
        panchang = calculate_panchang(d_str, latitude, longitude)

        festivals = detect_festivals(
            tithi_name=panchang["tithi"]["name"],
            paksha=panchang["tithi"]["paksha"],
            nakshatra_name=panchang["nakshatra"]["name"],
            maas=panchang.get("hindu_calendar", {}).get("maas", ""),
        )

        days.append({
            "date": d_str,
            "weekday": d.strftime("%A"),
            "tithi": panchang["tithi"]["name"],
            "paksha": panchang["tithi"]["paksha"],
            "nakshatra": panchang["nakshatra"]["name"],
            "yoga": panchang["yoga"]["name"],
            "sunrise": panchang["sunrise"],
            "sunset": panchang["sunset"],
            "festivals": [f["name"] for f in festivals],
        })

    return {
        "month": target_month,
        "year": target_year,
        "latitude": latitude,
        "longitude": longitude,
        "days": days,
    }


# ============================================================
# GET /api/panchang/choghadiya
# ============================================================

@router.get("/api/panchang/choghadiya", status_code=status.HTTP_200_OK)
def get_choghadiya(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Calculate Choghadiya (auspicious time periods) for the day."""
    target_date = date_str or _today()
    dt = _parse_date(target_date)
    weekday = dt.weekday()

    panchang = calculate_panchang(target_date, latitude, longitude)
    periods = calculate_choghadiya(weekday, panchang["sunrise"], panchang["sunset"])

    return {
        "date": target_date,
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "periods": periods,
    }


# ============================================================
# GET /api/panchang/muhurat -- Monthly muhurat
# ============================================================

@router.get("/api/panchang/muhurat", status_code=status.HTTP_200_OK)
def get_muhurat(
    muhurat_type: str = Query(default="marriage"),
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: Any = Depends(get_db),
):
    """Get auspicious muhurat dates for a given type and period."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    # Check cache
    cached = db.execute(
        "SELECT results FROM muhurat_cache WHERE muhurat_type = %s AND year = %s AND month = %s AND latitude = %s AND longitude = %s",
        (muhurat_type, target_year, target_month, latitude, longitude),
    ).fetchone()

    if cached:
        raw_results = json.loads(cached["results"])
        dates = [
            {
                "date": r.get("date", ""),
                "time_range": f"Sunrise to Sunset ({r.get('tithi', 'Shukla')} {r.get('nakshatra', '')})",
                "quality": r.get("quality", "auspicious"),
            }
            for r in raw_results
        ]
        return {"dates": dates}

    days_in_month = calendar.monthrange(target_year, target_month)[1]
    auspicious_dates = []

    for day in range(1, days_in_month + 1):
        d = date(target_year, target_month, day)
        d_str = d.isoformat()
        panchang = calculate_panchang(d_str, latitude, longitude)
        tithi = panchang["tithi"]

        if tithi["paksha"] == "Shukla" and tithi["name"] not in ("Ashtami", "Navami", "Chaturdashi"):
            auspicious_dates.append({
                "date": d_str,
                "tithi": tithi["name"],
                "nakshatra": panchang["nakshatra"]["name"],
                "quality": "auspicious",
            })

    results_json = json.dumps(auspicious_dates)
    db.execute(
        """INSERT INTO muhurat_cache
           (muhurat_type, year, month, latitude, longitude, results)
           VALUES (%s, %s, %s, %s, %s, %s)
           ON CONFLICT (muhurat_type, year, month, latitude, longitude) DO NOTHING""",
        (muhurat_type, target_year, target_month, latitude, longitude, results_json),
    )
    db.commit()

    dates = [
        {
            "date": r["date"],
            "time_range": f"Sunrise to Sunset ({r['tithi']} {r['nakshatra']})",
            "quality": r["quality"],
        }
        for r in auspicious_dates
    ]
    return {"dates": dates}


# ============================================================
# Sunrise & Festivals
# ============================================================

@router.get("/api/panchang/sunrise", status_code=status.HTTP_200_OK)
def get_sunrise(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Get sunrise, sunset, moonrise, moonset for a given date and location."""
    target_date = date_str or _today()
    _parse_date(target_date)

    panchang = calculate_panchang(target_date, latitude, longitude)

    return {
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "moonrise": panchang.get("moonrise", "--:--"),
        "moonset": panchang.get("moonset", "--:--"),
    }


@router.get("/api/festivals", status_code=status.HTTP_200_OK)
def list_festivals(
    year: int = Query(default=None),
    category: str = Query(default=None),
    db: Any = Depends(get_db),
):
    """List festivals for a given year, optionally filtered by category."""
    target_year = year or date.today().year

    if category:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s AND category = %s ORDER BY date",
            (target_year, category),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s ORDER BY date",
            (target_year,),
        ).fetchall()

    return [
        {
            "name": r["name"],
            "date": r["date"],
            "description": r["description"],
            "rituals": r["rituals"],
        }
        for r in rows
    ]
