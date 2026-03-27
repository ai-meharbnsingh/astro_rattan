"""Cosmic Calendar routes — monthly calendar, today's snapshot, upcoming transits."""
import calendar
import hashlib
import json
import math
from typing import Any
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional

from app.auth import get_current_user, security
from app.database import get_db
from app.panchang_engine import calculate_panchang, calculate_rahu_kaal, calculate_choghadiya
from app.astro_engine import (
    calculate_planet_positions,
    get_sign_from_longitude,
    PLANETS,
    _approx_sun_longitude,
    _approx_moon_longitude,
    _approx_planet_longitude,
    _approx_rahu_longitude,
    _approx_ayanamsa,
    _datetime_to_jd,
    _parse_datetime,
)

router = APIRouter(prefix="/api/cosmic-calendar", tags=["cosmic-calendar"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DIRECTIONS = ["East", "North", "West", "South", "North-East", "South-East", "South-West", "North-West"]
_COLORS = [
    "Red", "Gold", "Green", "Blue", "White", "Yellow", "Orange",
    "Violet", "Pink", "Saffron", "Silver", "Turquoise",
]

_SUGGESTED_ACTIVITIES = {
    "Shukla": {
        "Pratipada": ["Start new ventures", "Begin learning", "Set intentions"],
        "Dwitiya": ["Financial planning", "Socializing", "Short travel"],
        "Tritiya": ["Creative pursuits", "Music and arts", "Charity"],
        "Chaturthi": ["Meditation", "Spiritual practices", "Avoid starting new work"],
        "Panchami": ["Education", "Scholarly activities", "Writing"],
        "Shashthi": ["Health routines", "Outdoor activities", "Sports"],
        "Saptami": ["Worship of Sun", "Travel", "Vehicle purchase"],
        "Ashtami": ["Fasting", "Spiritual sadhana", "Avoid major decisions"],
        "Navami": ["Property matters", "Construction", "Agriculture"],
        "Dashami": ["Auspicious ceremonies", "Government work", "Legal matters"],
        "Ekadashi": ["Fasting", "Devotion", "Charity"],
        "Dwadashi": ["Business deals", "Investments", "Partnership"],
        "Trayodashi": ["Celebrations", "Romance", "Friendship"],
        "Chaturdashi": ["Complete pending tasks", "Introspection", "Meditation"],
        "Purnima": ["Spiritual practices", "Charity", "Full moon meditation"],
    },
    "Krishna": {
        "Pratipada": ["Routine work", "Planning", "Organization"],
        "Dwitiya": ["Domestic tasks", "Home improvement", "Cooking"],
        "Tritiya": ["Reflection", "Journal writing", "Study"],
        "Chaturthi": ["Ganesh worship", "Remove obstacles", "Problem-solving"],
        "Panchami": ["Research", "Deep study", "Analysis"],
        "Shashthi": ["Health check-ups", "Rest", "Recovery"],
        "Saptami": ["Short journeys", "Communication", "Networking"],
        "Ashtami": ["Fasting for Kali", "Tantric practices", "Inner work"],
        "Navami": ["Ancestral rites", "Charity to elders", "Forgiveness"],
        "Dashami": ["Wrap up projects", "Review finances", "Accounting"],
        "Ekadashi": ["Fasting", "Vishnu worship", "Spiritual reading"],
        "Dwadashi": ["Break fast mindfully", "Gentle exercise", "Socializing"],
        "Trayodashi": ["Shiva worship", "Meditation", "Detachment practices"],
        "Chaturdashi": ["Deep meditation", "Silence", "Letting go"],
        "Amavasya": ["Ancestor worship", "Tarpan", "New moon meditation"],
    },
}


def _get_lucky_number(date_str: str) -> int:
    """Derive a lucky number (1-9) from the date."""
    parts = date_str.split("-")
    day = int(parts[2])
    month = int(parts[1])
    total = day + month
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total or 1


def _get_lucky_color(date_str: str) -> str:
    """Derive a lucky color from the date."""
    h = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
    return _COLORS[h % len(_COLORS)]


def _get_lucky_direction(date_str: str) -> str:
    """Derive a lucky direction from the date."""
    h = int(hashlib.md5(date_str.encode()).hexdigest()[8:16], 16)
    return _DIRECTIONS[h % len(_DIRECTIONS)]


def _get_suggested_activities(tithi: dict) -> list:
    """Get suggested activities based on tithi."""
    paksha = tithi.get("paksha", "Shukla")
    name = tithi.get("name", "Pratipada")
    paksha_data = _SUGGESTED_ACTIVITIES.get(paksha, _SUGGESTED_ACTIVITIES["Shukla"])
    return paksha_data.get(name, ["General spiritual practice", "Meditation", "Charity"])


def _get_current_planet_positions(date_str: str) -> dict:
    """Calculate current planetary positions for a given date."""
    dt = _parse_datetime(date_str, "12:00", 5.5)  # Noon IST
    jd = _datetime_to_jd(dt)
    ayanamsa = _approx_ayanamsa(jd)

    planets = {}
    planet_funcs = {
        "Sun": lambda: _approx_sun_longitude(jd),
        "Moon": lambda: _approx_moon_longitude(jd),
        "Mercury": lambda: _approx_planet_longitude(jd, "Mercury"),
        "Venus": lambda: _approx_planet_longitude(jd, "Venus"),
        "Mars": lambda: _approx_planet_longitude(jd, "Mars"),
        "Jupiter": lambda: _approx_planet_longitude(jd, "Jupiter"),
        "Saturn": lambda: _approx_planet_longitude(jd, "Saturn"),
        "Rahu": lambda: _approx_rahu_longitude(jd),
    }

    for name, func in planet_funcs.items():
        trop = func()
        sid = (trop - ayanamsa) % 360.0
        sign = get_sign_from_longitude(sid)
        planets[name] = {
            "longitude": round(sid, 2),
            "sign": sign,
            "degree": round(sid % 30.0, 2),
        }

    # Ketu
    rahu_lon = planets["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180.0) % 360.0
    planets["Ketu"] = {
        "longitude": round(ketu_lon, 2),
        "sign": get_sign_from_longitude(ketu_lon),
        "degree": round(ketu_lon % 30.0, 2),
    }

    return planets


def _compute_transits_for_chart(chart_data: dict, current_planets: dict) -> list:
    """Compute transits affecting a user's birth chart."""
    transits = []
    if not chart_data or "planets" not in chart_data:
        return transits

    natal_planets = chart_data["planets"]

    # Check each transiting planet against natal positions
    aspect_orb = 10.0  # degrees
    for t_name, t_data in current_planets.items():
        t_lon = t_data["longitude"]
        for n_name, n_data in natal_planets.items():
            n_lon = n_data.get("longitude", 0)
            diff = abs(t_lon - n_lon)
            if diff > 180:
                diff = 360 - diff

            aspect = None
            if diff <= aspect_orb:
                aspect = "conjunction"
            elif abs(diff - 60) <= aspect_orb:
                aspect = "sextile"
            elif abs(diff - 90) <= aspect_orb:
                aspect = "square"
            elif abs(diff - 120) <= aspect_orb:
                aspect = "trine"
            elif abs(diff - 180) <= aspect_orb:
                aspect = "opposition"

            if aspect and t_name != n_name:
                intensity = "strong" if t_name in ("Saturn", "Jupiter", "Rahu", "Ketu") else "moderate"
                nature = "challenging" if aspect in ("square", "opposition") else "favorable"
                transits.append({
                    "transiting_planet": t_name,
                    "natal_planet": n_name,
                    "aspect": aspect,
                    "transiting_sign": t_data["sign"],
                    "natal_sign": n_data.get("sign", ""),
                    "intensity": intensity,
                    "nature": nature,
                    "description": f"{t_name} in {t_data['sign']} {aspect} natal {n_name} in {n_data.get('sign', '')}",
                })

    return transits


def _get_muhurat_windows(date_str: str, latitude: float, longitude: float) -> list:
    """Get auspicious muhurat windows for a given date."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = dt.weekday()

    panchang = calculate_panchang(date_str, latitude, longitude)
    choghadiya = calculate_choghadiya(weekday, panchang["sunrise"], panchang["sunset"])

    windows = []
    for period in choghadiya:
        if period["quality"] in ("Best", "Good"):
            windows.append({
                "name": period["name"],
                "quality": period["quality"],
                "start": period["start"],
                "end": period["end"],
            })

    return windows


def _try_get_user(credentials):
    """Try to extract user from optional auth token. Returns None if not authenticated."""
    if credentials is None:
        return None
    from app.auth import decode_token
    payload = decode_token(credentials.credentials)
    return payload


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/month", status_code=status.HTTP_200_OK)
def get_month_calendar(
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    credentials=Depends(security),
    db: Any = Depends(get_db),
):
    """Return calendar data for a month with festivals, panchang, muhurats, and personalized events."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    if not (1 <= target_month <= 12):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Month must be between 1 and 12")

    days_in_month = calendar.monthrange(target_year, target_month)[1]

    # Fetch festivals for this month
    month_start = f"{target_year}-{target_month:02d}-01"
    month_end = f"{target_year}-{target_month:02d}-{days_in_month:02d}"
    festival_rows = db.execute(
        "SELECT name, date, description, category FROM festivals WHERE date >= %s AND date <= %s ORDER BY date",
        (month_start, month_end),
    ).fetchall()

    festivals_by_day = {}
    for f in festival_rows:
        day = int(f["date"].split("-")[2])
        if day not in festivals_by_day:
            festivals_by_day[day] = []
        festivals_by_day[day].append({
            "name": f["name"],
            "description": f["description"],
            "category": f["category"],
        })

    # Try to get user's kundli for personalized transits
    user = _try_get_user(credentials)
    user_chart = None
    if user:
        user_id = user.get("sub")
        if user_id:
            kundli_row = db.execute(
                "SELECT chart_data FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,),
            ).fetchone()
            if kundli_row and kundli_row["chart_data"]:
                try:
                    user_chart = json.loads(kundli_row["chart_data"])
                except (json.JSONDecodeError, TypeError):
                    pass

    days = []
    for day_num in range(1, days_in_month + 1):
        d_str = f"{target_year}-{target_month:02d}-{day_num:02d}"

        # Panchang summary
        panchang = calculate_panchang(d_str, latitude, longitude)

        # Muhurat windows
        muhurat_windows = _get_muhurat_windows(d_str, latitude, longitude)

        # Determine day type for color coding
        day_festivals = festivals_by_day.get(day_num, [])
        has_festival = len(day_festivals) > 0
        is_auspicious = panchang["tithi"]["paksha"] == "Shukla" and panchang["tithi"]["name"] not in ("Ashtami", "Navami", "Chaturdashi")
        is_inauspicious = panchang["tithi"]["name"] in ("Chaturdashi",) and panchang["tithi"]["paksha"] == "Krishna"

        day_type = "neutral"
        if has_festival:
            day_type = "festival"
        elif is_auspicious:
            day_type = "auspicious"
        elif is_inauspicious:
            day_type = "inauspicious"

        day_data = {
            "day": day_num,
            "date": d_str,
            "day_type": day_type,
            "panchang": {
                "tithi": panchang["tithi"],
                "nakshatra": panchang["nakshatra"],
                "yoga": panchang["yoga"],
                "karana": panchang["karana"],
                "sunrise": panchang["sunrise"],
                "sunset": panchang["sunset"],
            },
            "festivals": day_festivals,
            "muhurat_windows": muhurat_windows,
        }

        # Add personalized transits if user has a chart
        if user_chart:
            current_planets = _get_current_planet_positions(d_str)
            transits = _compute_transits_for_chart(user_chart, current_planets)
            # Limit to most significant transits per day
            significant = [t for t in transits if t["intensity"] == "strong"][:3]
            if not significant:
                significant = transits[:2]
            day_data["personalized_transits"] = significant

        days.append(day_data)

    return {
        "year": target_year,
        "month": target_month,
        "month_name": calendar.month_name[target_month],
        "days_in_month": days_in_month,
        "days": days,
    }


@router.get("/today", status_code=status.HTTP_200_OK)
def get_today_snapshot(
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    credentials=Depends(security),
    db: Any = Depends(get_db),
):
    """Today's personalized cosmic snapshot with planets, panchang, transits, lucky attributes."""
    today_str = date.today().isoformat()

    # Panchang
    panchang = calculate_panchang(today_str, latitude, longitude)

    # Current planetary positions
    current_planets = _get_current_planet_positions(today_str)

    # Rahu Kaal
    dt = datetime.strptime(today_str, "%Y-%m-%d")
    rahu_kaal = calculate_rahu_kaal(dt.weekday(), panchang["sunrise"], panchang["sunset"])

    # Choghadiya
    choghadiya = calculate_choghadiya(dt.weekday(), panchang["sunrise"], panchang["sunset"])

    # Lucky attributes
    lucky_number = _get_lucky_number(today_str)
    lucky_color = _get_lucky_color(today_str)
    lucky_direction = _get_lucky_direction(today_str)

    # Suggested activities based on tithi
    activities = _get_suggested_activities(panchang["tithi"])

    # Festivals today
    festival_rows = db.execute(
        "SELECT name, description, category FROM festivals WHERE date = %s",
        (today_str,),
    ).fetchall()
    festivals = [{"name": f["name"], "description": f["description"], "category": f["category"]} for f in festival_rows]

    result = {
        "date": today_str,
        "day_of_week": dt.strftime("%A"),
        "planetary_positions": current_planets,
        "panchang": {
            "tithi": panchang["tithi"],
            "nakshatra": panchang["nakshatra"],
            "yoga": panchang["yoga"],
            "karana": panchang["karana"],
            "sunrise": panchang["sunrise"],
            "sunset": panchang["sunset"],
            "rahu_kaal": rahu_kaal,
            "choghadiya": choghadiya,
        },
        "festivals": festivals,
        "lucky": {
            "number": lucky_number,
            "color": lucky_color,
            "direction": lucky_direction,
        },
        "suggested_activities": activities,
    }

    # Add personalized transits if user is authenticated and has kundli
    user = _try_get_user(credentials)
    if user:
        user_id = user.get("sub")
        if user_id:
            kundli_row = db.execute(
                "SELECT chart_data FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,),
            ).fetchone()
            if kundli_row and kundli_row["chart_data"]:
                try:
                    chart_data = json.loads(kundli_row["chart_data"])
                    transits = _compute_transits_for_chart(chart_data, current_planets)
                    result["personalized_transits"] = transits[:10]
                except (json.JSONDecodeError, TypeError):
                    pass

    return result


@router.get("/transits", status_code=status.HTTP_200_OK)
def get_upcoming_transits(
    kundli_id: str = Query(...),
    days: int = Query(default=30, ge=1, le=90),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get upcoming major transits for a user's chart over the next N days (default 30)."""
    user_id = current_user["sub"]

    # Fetch the kundli
    kundli_row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()

    if not kundli_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")

    try:
        chart_data = json.loads(kundli_row["chart_data"])
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid chart data")

    today = date.today()
    transit_timeline = []

    # Check significant transits for each day
    seen_transits = set()
    for day_offset in range(days):
        d = today + timedelta(days=day_offset)
        d_str = d.isoformat()
        current_planets = _get_current_planet_positions(d_str)
        transits = _compute_transits_for_chart(chart_data, current_planets)

        for t in transits:
            if t["intensity"] == "strong":
                key = f"{t['transiting_planet']}-{t['natal_planet']}-{t['aspect']}"
                if key not in seen_transits:
                    seen_transits.add(key)
                    transit_timeline.append({
                        "date": d_str,
                        "transiting_planet": t["transiting_planet"],
                        "natal_planet": t["natal_planet"],
                        "aspect": t["aspect"],
                        "transiting_sign": t["transiting_sign"],
                        "natal_sign": t["natal_sign"],
                        "nature": t["nature"],
                        "description": t["description"],
                    })

    return {
        "kundli_id": kundli_id,
        "days_ahead": days,
        "total_transits": len(transit_timeline),
        "transits": transit_timeline,
    }
