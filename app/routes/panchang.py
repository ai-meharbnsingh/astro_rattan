"""Panchang routes — daily panchang, choghadiya, muhurat, sunrise, and festivals."""
import json
import sqlite3
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.panchang_engine import calculate_panchang, calculate_rahu_kaal, calculate_choghadiya
from app.muhurat_engine import find_muhurat, get_monthly_muhurats, EVENT_TYPES

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


@router.get("/api/panchang", status_code=status.HTTP_200_OK)
def get_panchang(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),   # Delhi default
    longitude: float = Query(default=77.2090),
    db: sqlite3.Connection = Depends(get_db),
):
    """Calculate Panchang for a given date and location."""
    target_date = date_str or _today()
    _parse_date(target_date)  # Validate date format

    # Check cache first
    cached = db.execute(
        "SELECT * FROM panchang_cache WHERE date = ? AND latitude = ? AND longitude = ?",
        (target_date, latitude, longitude),
    ).fetchone()

    if cached:
        # Parse JSON strings back to objects for cached fields
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

        return {
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
            "moonrise": cached["moonrise"],
            "moonset": cached["moonset"],
        }

    # Calculate fresh
    panchang = calculate_panchang(target_date, latitude, longitude)

    # Rahu Kaal
    dt = _parse_date(target_date)
    weekday = dt.weekday()
    rahu_kaal = calculate_rahu_kaal(weekday, panchang["sunrise"], panchang["sunset"])

    # Approximate moonrise/moonset (roughly sunrise + 50min per lunar day, sunset + similar offset)
    # This is a rough approximation; a real implementation would use ephemeris
    moonrise_approx = panchang.get("moonrise", _approx_moonrise(panchang["sunrise"]))
    moonset_approx = panchang.get("moonset", _approx_moonset(panchang["sunset"]))

    # Cache the result
    tithi_str = json.dumps(panchang["tithi"])
    nak_str = json.dumps(panchang["nakshatra"])
    yoga_str = json.dumps(panchang["yoga"])
    karana_str = json.dumps(panchang["karana"])
    rahu_str = json.dumps(rahu_kaal)

    db.execute(
        """INSERT OR IGNORE INTO panchang_cache
           (date, latitude, longitude, tithi, nakshatra, yoga, karana,
            rahu_kaal, choghadiya, sunrise, sunset, moonrise, moonset)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            target_date, latitude, longitude,
            tithi_str, nak_str, yoga_str, karana_str,
            rahu_str, "[]",
            panchang["sunrise"], panchang["sunset"],
            moonrise_approx, moonset_approx,
        ),
    )
    db.commit()

    return {
        "date": target_date,
        "latitude": latitude,
        "longitude": longitude,
        "tithi": panchang["tithi"],
        "nakshatra": panchang["nakshatra"],
        "yoga": panchang["yoga"],
        "karana": panchang["karana"],
        "rahu_kaal": rahu_kaal,
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "moonrise": moonrise_approx,
        "moonset": moonset_approx,
    }


def _approx_moonrise(sunrise: str) -> str:
    """Approximate moonrise as ~50 minutes after sunrise (varies by lunar day)."""
    parts = sunrise.split(":")
    h, m = int(parts[0]), int(parts[1])
    total = h * 60 + m + 50
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def _approx_moonset(sunset: str) -> str:
    """Approximate moonset as ~50 minutes after sunset."""
    parts = sunset.split(":")
    h, m = int(parts[0]), int(parts[1])
    total = h * 60 + m + 50
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


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


@router.get("/api/panchang/muhurat", status_code=status.HTTP_200_OK)
def get_muhurat(
    muhurat_type: str = Query(default="marriage"),
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get auspicious muhurat dates for a given type and period.
    Contract response: {dates: [{date, time_range, quality}]}
    """
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    # Check cache
    cached = db.execute(
        "SELECT results FROM muhurat_cache WHERE muhurat_type = ? AND year = ? AND month = ? AND latitude = ? AND longitude = ?",
        (muhurat_type, target_year, target_month, latitude, longitude),
    ).fetchone()

    if cached:
        raw_results = json.loads(cached["results"])
        # Transform to contract format: {dates: [{date, time_range, quality}]}
        dates = [
            {
                "date": r.get("date", ""),
                "time_range": f"Sunrise to Sunset ({r.get('tithi', 'Shukla')} {r.get('nakshatra', '')})",
                "quality": r.get("quality", "auspicious"),
            }
            for r in raw_results
        ]
        return {"dates": dates}

    # Generate muhurat dates by checking panchang for each day of the month
    import calendar
    days_in_month = calendar.monthrange(target_year, target_month)[1]
    auspicious_dates = []

    for day in range(1, days_in_month + 1):
        d = date(target_year, target_month, day)
        d_str = d.isoformat()
        panchang = calculate_panchang(d_str, latitude, longitude)
        tithi = panchang["tithi"]

        # Simple auspicious check: Shukla paksha, non-Ashtami/Navami tithis
        if tithi["paksha"] == "Shukla" and tithi["name"] not in ("Ashtami", "Navami", "Chaturdashi"):
            auspicious_dates.append({
                "date": d_str,
                "tithi": tithi["name"],
                "nakshatra": panchang["nakshatra"]["name"],
                "quality": "auspicious",
            })

    # Cache result
    results_json = json.dumps(auspicious_dates)
    db.execute(
        """INSERT OR IGNORE INTO muhurat_cache
           (muhurat_type, year, month, latitude, longitude, results)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (muhurat_type, target_year, target_month, latitude, longitude, results_json),
    )
    db.commit()

    # Transform to contract format
    dates = [
        {
            "date": r["date"],
            "time_range": f"Sunrise to Sunset ({r['tithi']} {r['nakshatra']})",
            "quality": r["quality"],
        }
        for r in auspicious_dates
    ]
    return {"dates": dates}


@router.get("/api/panchang/sunrise", status_code=status.HTTP_200_OK)
def get_sunrise(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Get sunrise, sunset, moonrise, moonset for a given date and location.
    Contract response: {sunrise, sunset, moonrise, moonset}
    """
    target_date = date_str or _today()
    _parse_date(target_date)  # Validate date format

    panchang = calculate_panchang(target_date, latitude, longitude)

    moonrise = panchang.get("moonrise", _approx_moonrise(panchang["sunrise"]))
    moonset = panchang.get("moonset", _approx_moonset(panchang["sunset"]))

    return {
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "moonrise": moonrise,
        "moonset": moonset,
    }


@router.get("/api/festivals", status_code=status.HTTP_200_OK)
def list_festivals(
    year: int = Query(default=None),
    category: str = Query(default=None),
    db: sqlite3.Connection = Depends(get_db),
):
    """List festivals for a given year, optionally filtered by category."""
    target_year = year or date.today().year

    if category:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = ? AND category = ? ORDER BY date",
            (target_year, category),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = ? ORDER BY date",
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
