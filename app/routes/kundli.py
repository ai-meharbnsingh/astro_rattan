"""Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha, divisional, ashtakvarga, avakhada, yogas, geocode, pdf."""
import io
import json
from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.auth import get_current_user
from app.database import get_db
from app.models import KundliRequest, KundliMatchRequest, DivisionalChartRequest
from app.astro_engine import calculate_planet_positions
from app.astro_iogita_engine import run_astro_analysis
from app.dosha_engine import check_mangal_dosha, check_kaal_sarp, check_sade_sati, analyze_yogas_and_doshas
from app.dasha_engine import calculate_dasha, calculate_extended_dasha
from app.varshphal_engine import calculate_varshphal
from app.divisional_charts import (
    calculate_divisional_chart_detailed,
    calculate_divisional_houses,
    DIVISIONAL_CHARTS,
)
from app.ashtakvarga_engine import calculate_ashtakvarga
from app.shadbala_engine import calculate_shadbala, calculate_bhav_bala
from app.avakhada_engine import calculate_avakhada
from app.transit_engine import calculate_transits
from app.kp_engine import calculate_kp_cuspal
from app.lifelong_sade_sati import calculate_lifelong_sade_sati
from app.yogini_dasha_engine import calculate_yogini_dasha
from datetime import datetime

router = APIRouter(prefix="/api/kundli", tags=["kundli"])


# ── geocode ─────────────────────────────────────────────────

@router.get("/geocode", status_code=status.HTTP_200_OK)
async def geocode_place(query: str = Query(..., min_length=2, description="Place name to geocode")):
    """Geocode a place name using the free Nominatim OpenStreetMap API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 5},
                headers={"User-Agent": "AstroRattan/1.0"},
            )
            resp.raise_for_status()
            results = resp.json()
            return [
                {"name": r["display_name"], "lat": float(r["lat"]), "lon": float(r["lon"])}
                for r in results
            ]
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Geocoding service unavailable. Please enter coordinates manually.",
        )


# ── helpers ──────────────────────────────────────────────────
def _fetch_kundli(db: Any, kundli_id: str, user_id: str) -> dict:
    """Fetch a kundli row or raise 404. Returns dict(row)."""
    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")
    return dict(row)


def _chart_data(row: dict) -> dict:
    """Parse the JSON chart_data column from a kundli row."""
    return json.loads(row["chart_data"])


# ── routes ───────────────────────────────────────────────────

@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_kundli(
    body: KundliRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Generate a new Vedic birth chart (kundli) and store it. Auto-creates/links client."""
    # Astrologers must provide phone when creating kundli for a new client
    user_role = current_user.get("role", "user")
    if user_role == "astrologer" and not body.client_id and not body.phone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Phone number is required when creating a kundli for a client.",
        )

    chart_data = calculate_planet_positions(
        birth_date=body.birth_date,
        birth_time=body.birth_time,
        latitude=body.latitude,
        longitude=body.longitude,
        tz_offset=body.timezone_offset,
    )
    chart_json = json.dumps(chart_data, default=str)

    # Auto-create or link client
    client_id = body.client_id
    if not client_id:
        # Check if client with same name exists for this astrologer
        existing = db.execute(
            "SELECT id FROM clients WHERE astrologer_id = %s AND name = %s LIMIT 1",
            (current_user["sub"], body.person_name),
        ).fetchone()
        if existing:
            client_id = existing["id"]
            # Update client's birth details if they were missing
            db.execute(
                """UPDATE clients SET birth_date = COALESCE(NULLIF(birth_date,''), %s),
                   birth_time = COALESCE(NULLIF(birth_time,''), %s),
                   birth_place = COALESCE(NULLIF(birth_place,''), %s),
                   latitude = COALESCE(latitude, %s), longitude = COALESCE(longitude, %s),
                   timezone_offset = COALESCE(timezone_offset, %s), updated_at = NOW()
                   WHERE id = %s""",
                (body.birth_date, body.birth_time, body.birth_place,
                 body.latitude, body.longitude, body.timezone_offset, client_id),
            )
        else:
            client_row = db.execute(
                """INSERT INTO clients (astrologer_id, name, phone, birth_date, birth_time,
                   birth_place, latitude, longitude, timezone_offset, gender)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (current_user["sub"], body.person_name, body.phone, body.birth_date,
                 body.birth_time, body.birth_place, body.latitude, body.longitude,
                 body.timezone_offset, body.gender or "male"),
            ).fetchone()
            client_id = client_row["id"]

    row = db.execute(
        """INSERT INTO kundlis
           (user_id, client_id, person_name, birth_date, birth_time, birth_place,
            latitude, longitude, timezone_offset, ayanamsa, chart_type, chart_data)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           RETURNING *""",
        (
            current_user["sub"], client_id,
            body.person_name, body.birth_date, body.birth_time, body.birth_place,
            body.latitude, body.longitude, body.timezone_offset, body.ayanamsa,
            body.chart_type or "vedic", chart_json,
        ),
    ).fetchone()
    db.commit()

    return {
        "id": row["id"],
        "client_id": client_id,
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "chart_type": row.get("chart_type", "vedic"),
        "chart_data": json.loads(row["chart_data"]),
        "created_at": row["created_at"],
    }


@router.get("", status_code=status.HTTP_200_OK)
@router.get("/list", status_code=status.HTTP_200_OK)
def list_kundlis(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all kundlis for the current user."""
    rows = db.execute(
        "SELECT id, person_name, birth_date, birth_time, birth_place, created_at "
        "FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (current_user["sub"],),
    ).fetchall()

    return [
        {
            "id": r["id"],
            "person_name": r["person_name"],
            "birth_date": r["birth_date"],
            "birth_time": r["birth_time"],
            "birth_place": r["birth_place"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]


@router.post("/match", status_code=status.HTTP_200_OK)
def match_kundlis(
    body: KundliMatchRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Ashtakoota Gun Milan — match two kundlis for compatibility (36-point system)."""
    from app.matching_engine import calculate_gun_milan

    row1 = _fetch_kundli(db, body.kundli_id_1, current_user["sub"])
    row2 = _fetch_kundli(db, body.kundli_id_2, current_user["sub"])

    chart1 = _chart_data(row1)
    chart2 = _chart_data(row2)

    # Extract Moon nakshatra and rashi from chart data
    planets1 = chart1.get("planets", {})
    planets2 = chart2.get("planets", {})

    def _moon_info(planets):
        if isinstance(planets, list):
            moon = next((p for p in planets if p.get("planet") == "Moon"), None)
            return (moon.get("nakshatra", ""), moon.get("sign", "")) if moon else ("", "")
        elif isinstance(planets, dict):
            moon = planets.get("Moon", {})
            return (moon.get("nakshatra", ""), moon.get("sign", "")) if moon else ("", "")
        return ("", "")

    nak1, rashi1 = _moon_info(planets1)
    nak2, rashi2 = _moon_info(planets2)

    if not nak1 or not nak2:
        raise HTTPException(status_code=422, detail="Moon nakshatra not found in one or both charts")

    result = calculate_gun_milan(nak1, nak2, rashi1, rashi2)
    result["person1_name"] = row1["person_name"]
    result["person2_name"] = row2["person_name"]
    return result


@router.get("/{kundli_id}", status_code=status.HTTP_200_OK)
def get_kundli(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Retrieve a single kundli by ID."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    return {
        "id": row["id"],
        "client_id": row.get("client_id"),
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "timezone_offset": row["timezone_offset"],
        "ayanamsa": row["ayanamsa"],
        "chart_type": row.get("chart_type", "vedic"),
        "chart_data": json.loads(row["chart_data"]),
        "iogita_analysis": json.loads(row["iogita_analysis"]) if row["iogita_analysis"] else None,
        "created_at": row["created_at"],
    }


@router.post("/{kundli_id}/regenerate", status_code=status.HTTP_200_OK)
def regenerate_kundli(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Recalculate chart data using current Swiss Ephemeris and update in DB."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart_data = calculate_planet_positions(
        birth_date=row["birth_date"],
        birth_time=row["birth_time"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        tz_offset=row["timezone_offset"],
    )
    chart_json = json.dumps(chart_data, default=str)
    db.execute(
        "UPDATE kundlis SET chart_data = %s, iogita_analysis = NULL WHERE id = %s AND user_id = %s",
        (chart_json, kundli_id, current_user["sub"]),
    )
    db.commit()
    return {
        "id": row["id"],
        "client_id": row.get("client_id"),
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "timezone_offset": row["timezone_offset"],
        "ayanamsa": row["ayanamsa"],
        "chart_type": row.get("chart_type", "vedic"),
        "chart_data": json.loads(chart_json),
        "created_at": row["created_at"],
        "regenerated": True,
    }


@router.post("/{kundli_id}/iogita", status_code=status.HTTP_200_OK)
def run_iogita_analysis(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Run io-gita atom engine analysis on a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Build planet_positions as {planet: sign}
    planet_positions = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_positions[planet_name] = info["sign"]

    # Need dasha to determine current mahadasha lord
    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
    moon_lon = moon_info.get("longitude", None)
    dasha_result = calculate_dasha(moon_nakshatra, str(row["birth_date"]), moon_longitude=moon_lon)
    current_dasha = dasha_result.get("current_dasha", "Venus")

    analysis = run_astro_analysis(planet_positions, current_dasha, row["person_name"])

    # Store analysis on the kundli row
    analysis_json = json.dumps(analysis, default=str)
    db.execute(
        "UPDATE kundlis SET iogita_analysis = %s WHERE id = %s",
        (analysis_json, kundli_id),
    )
    db.commit()

    return analysis


@router.post("/{kundli_id}/dosha", status_code=status.HTTP_200_OK)
def check_doshas(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Check Mangal Dosha, Kaal Sarp Dosha, and Sade Sati."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})

    # Mangal Dosha
    mars_house = planets.get("Mars", {}).get("house", 1)
    mangal = check_mangal_dosha(mars_house)

    # Kaal Sarp Dosha
    rahu_house = planets.get("Rahu", {}).get("house", 1)
    ketu_house = planets.get("Ketu", {}).get("house", 7)
    planet_houses = {}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if p in planets:
            planet_houses[p] = planets[p].get("house", 1)
    kaal_sarp = check_kaal_sarp(rahu_house, ketu_house, planet_houses)

    # Sade Sati — uses CURRENT TRANSIT Saturn position (not natal Saturn)
    moon_sign = planets.get("Moon", {}).get("sign", "Aries")
    # Calculate current Saturn position for transit-based Sade Sati check
    from datetime import datetime, timezone as _tz
    _now = datetime.now(_tz.utc)
    _today_positions = calculate_planet_positions(
        _now.strftime("%Y-%m-%d"), _now.strftime("%H:%M:%S"),
        latitude=row.get("latitude", 0.0), longitude=row.get("longitude", 0.0),
        tz_offset=round(row.get("longitude", 0.0) / 15.0 * 2) / 2,
    )
    saturn_transit_sign = _today_positions.get("planets", {}).get("Saturn", {}).get("sign", "Capricorn")
    sade_sati = check_sade_sati(moon_sign, saturn_transit_sign)

    # Gemstone recommendations based on ascendant lord and weak planets
    SIGN_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
    }
    PLANET_GEMS = {
        "Sun": {"gem": "Ruby (Manik)", "gem_hi": "माणिक्य (रूबी)", "metal": "Gold", "finger": "Ring finger", "day": "Sunday"},
        "Moon": {"gem": "Pearl (Moti)", "gem_hi": "मोती (पर्ल)", "metal": "Silver", "finger": "Little finger", "day": "Monday"},
        "Mars": {"gem": "Red Coral (Moonga)", "gem_hi": "मूंगा (रेड कोरल)", "metal": "Gold/Copper", "finger": "Ring finger", "day": "Tuesday"},
        "Mercury": {"gem": "Emerald (Panna)", "gem_hi": "पन्ना (एमराल्ड)", "metal": "Gold", "finger": "Little finger", "day": "Wednesday"},
        "Jupiter": {"gem": "Yellow Sapphire (Pukhraj)", "gem_hi": "पुखराज (येलो सफायर)", "metal": "Gold", "finger": "Index finger", "day": "Thursday"},
        "Venus": {"gem": "Diamond (Heera)", "gem_hi": "हीरा (डायमंड)", "metal": "Silver/Platinum", "finger": "Middle finger", "day": "Friday"},
        "Saturn": {"gem": "Blue Sapphire (Neelam)", "gem_hi": "नीलम (ब्लू सफायर)", "metal": "Iron/Silver", "finger": "Middle finger", "day": "Saturday"},
        "Rahu": {"gem": "Hessonite (Gomed)", "gem_hi": "गोमेद (हेसोनाइट)", "metal": "Silver", "finger": "Middle finger", "day": "Saturday"},
        "Ketu": {"gem": "Cat's Eye (Lehsunia)", "gem_hi": "लहसुनिया (कैट्स आई)", "metal": "Silver", "finger": "Ring finger", "day": "Tuesday"},
    }
    asc_sign = chart.get("ascendant", {}).get("sign", "Aries")
    asc_lord = SIGN_LORDS.get(asc_sign, "Sun")
    gemstone_recs = []
    # Primary: ascendant lord gemstone
    if asc_lord in PLANET_GEMS:
        g = PLANET_GEMS[asc_lord]
        gemstone_recs.append({
            "planet": asc_lord, "reason": "Ascendant Lord",
            "gemstone": g["gem"], "gemstone_hi": g["gem_hi"],
            "metal": g["metal"], "finger": g["finger"], "day": g["day"],
            "priority": "primary",
        })
    # Secondary: benefic planets for the ascendant
    BENEFICS_BY_ASC = {
        "Aries": ["Sun", "Jupiter"], "Taurus": ["Saturn", "Mercury"], "Gemini": ["Venus", "Saturn"],
        "Cancer": ["Mars", "Jupiter"], "Leo": ["Mars", "Jupiter"], "Virgo": ["Venus", "Mercury"],
        "Libra": ["Saturn", "Mercury"], "Scorpio": ["Jupiter", "Moon"], "Sagittarius": ["Sun", "Mars"],
        "Capricorn": ["Venus", "Mercury"], "Aquarius": ["Venus", "Saturn"], "Pisces": ["Moon", "Mars"],
    }
    for planet in BENEFICS_BY_ASC.get(asc_sign, []):
        if planet != asc_lord and planet in PLANET_GEMS:
            g = PLANET_GEMS[planet]
            gemstone_recs.append({
                "planet": planet, "reason": "Benefic for Ascendant",
                "gemstone": g["gem"], "gemstone_hi": g["gem_hi"],
                "metal": g["metal"], "finger": g["finger"], "day": g["day"],
                "priority": "secondary",
            })

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "mangal_dosha": mangal,
        "kaal_sarp_dosha": kaal_sarp,
        "sade_sati": sade_sati,
        "gemstone_recommendations": gemstone_recs,
    }


def _compute_dasha(db: Any, kundli_id: str, user_id: str) -> dict:
    """Shared logic for computing Vimshottari Dasha periods."""
    row = _fetch_kundli(db, kundli_id, user_id)
    chart = _chart_data(row)

    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
    moon_longitude = moon_info.get("longitude", None)
    result = calculate_dasha(moon_nakshatra, str(row["birth_date"]), moon_longitude=moon_longitude)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/dasha", status_code=status.HTTP_200_OK)
def get_dasha_via_get(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Vimshottari Dasha periods for a kundli (GET — no request body needed)."""
    return _compute_dasha(db, kundli_id, current_user["sub"])


@router.post("/{kundli_id}/dasha", status_code=status.HTTP_200_OK)
def get_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Vimshottari Dasha periods for a kundli (POST — kept for backward compatibility)."""
    return _compute_dasha(db, kundli_id, current_user["sub"])


@router.get("/{kundli_id}/divisional-charts", status_code=status.HTTP_200_OK)
def list_divisional_charts(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List available divisional chart types."""
    _fetch_kundli(db, kundli_id, current_user["sub"])  # Validate access
    return {
        "kundli_id": kundli_id,
        "charts": [
            {"division": d, "name": name, "code": f"D{d}"}
            for d, name in DIVISIONAL_CHARTS.items()
        ],
    }


@router.post("/{kundli_id}/divisional", status_code=status.HTTP_200_OK)
def get_divisional_chart(
    kundli_id: str,
    body: DivisionalChartRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate a divisional (varga) chart for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Extract planet longitudes
    planet_longitudes = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_longitudes[planet_name] = info["longitude"]

    # Parse division number from chart_type string (e.g. "D9" -> 9)
    chart_type = body.chart_type.upper()
    try:
        division = int(chart_type.replace("D", ""))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid chart type: {body.chart_type}. Use format 'D9', 'D10', etc.",
        )

    # Get detailed result with degree info
    detailed = calculate_divisional_chart_detailed(planet_longitudes, division)

    # Calculate divisional houses relative to divisional ascendant
    asc_longitude = chart.get("ascendant", {}).get("longitude", 0.0)
    houses = calculate_divisional_houses(asc_longitude, division)

    # Build a lookup: sign -> house number (for mapping planets to houses)
    sign_to_house = {h["sign"]: h["number"] for h in houses}

    # Build planet data suitable for InteractiveKundli component
    planet_positions = []
    for planet_name, info in detailed.items():
        sign_index = info["sign_index"]
        # House is relative to divisional ascendant, not absolute sign index
        house_num = sign_to_house.get(info["sign"], sign_index + 1)
        planet_positions.append({
            "planet": planet_name,
            "sign": info["sign"],
            "sign_degree": info["degree"],
            "house": house_num,
            "nakshatra": "",
            "longitude": sign_index * 30.0 + info["degree"],
        })

    # Simple sign mapping for backward compat
    planet_signs = {planet: info["sign"] for planet, info in detailed.items()}

    chart_name = DIVISIONAL_CHARTS.get(division, f"D{division}")

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "chart_type": chart_type,
        "chart_name": chart_name,
        "division": division,
        "planet_signs": planet_signs,
        "planet_positions": planet_positions,
        "houses": houses,
    }


@router.post("/{kundli_id}/ashtakvarga", status_code=status.HTTP_200_OK)
def get_ashtakvarga(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Ashtakvarga point system for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Build planet_signs: {planet: sign, Ascendant: sign}
    planet_signs = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_signs[planet_name] = info["sign"]

    ascendant_sign = chart.get("ascendant", {}).get("sign")
    if ascendant_sign:
        planet_signs["Ascendant"] = ascendant_sign

    result = calculate_ashtakvarga(planet_signs)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/shadbala", status_code=status.HTTP_200_OK)
def get_shadbala(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Shadbala (six-fold strength) for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})

    # Build planet_signs, planet_houses, and planet_longitudes
    planet_signs = {}
    planet_houses = {}
    planet_longitudes = {}
    for planet_name, info in planets.items():
        planet_signs[planet_name] = info.get("sign", "Aries")
        planet_houses[planet_name] = info.get("house", 1)
        if "longitude" in info:
            planet_longitudes[planet_name] = info["longitude"]

    # Parse birth_hour as decimal (e.g. "14:30:00" -> 14.5)
    birth_time = row.get("birth_time", "12:00:00")
    try:
        parts = str(birth_time).split(":")
        birth_hour = int(parts[0]) + int(parts[1]) / 60.0
    except (ValueError, IndexError):
        birth_hour = 12.0
    is_daytime = 6.0 <= birth_hour < 18.0

    # Moon-Sun elongation for Paksha Bala
    sun_lon = planet_longitudes.get("Sun", 0.0)
    moon_lon = planet_longitudes.get("Moon", 0.0)
    moon_sun_elongation = (moon_lon - sun_lon) % 360.0

    # Weekday, year, month from birth_date
    try:
        bd = datetime.strptime(str(row.get("birth_date", "2000-01-01")), "%Y-%m-%d")
        weekday = bd.weekday()     # Monday=0 .. Sunday=6
        birth_year = bd.year
        birth_month = bd.month
    except (ValueError, TypeError):
        weekday, birth_year, birth_month = 0, 2000, 1

    # Extract retrograde planets for Cheshta Bala
    retrograde_planets = set()
    for planet_name, info in planets.items():
        retro_flag = info.get("retrograde", False)
        retro_status = info.get("status", "")
        if retro_flag or "Retrograde" in retro_status or "retrograde" in retro_status:
            retrograde_planets.add(planet_name)

    result = calculate_shadbala(
        planet_signs=planet_signs,
        planet_houses=planet_houses,
        is_daytime=is_daytime,
        retrograde_planets=retrograde_planets,
        planet_longitudes=planet_longitudes,
        birth_hour=birth_hour,
        moon_sun_elongation=moon_sun_elongation,
        weekday=weekday,
        birth_year=birth_year,
        birth_month=birth_month,
    )
    # Bhav Bala — extract house signs from chart data
    houses_raw = chart.get("houses", [])
    house_signs: dict = {}
    for h in houses_raw:
        if isinstance(h, dict):
            num = h.get("number") or h.get("house")
            sign = h.get("sign", "Aries")
            if num:
                house_signs[int(num)] = sign
    result["bhav_bala"] = calculate_bhav_bala(
        house_signs=house_signs,
        planet_houses=planet_houses,
        planets_result=result["planets"],
    )

    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/avakhada", status_code=status.HTTP_200_OK)
def get_avakhada(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Avakhada Chakra — comprehensive birth summary table."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    result = calculate_avakhada(chart, birth_date=str(row.get("birth_date", "")))
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/extended-dasha", status_code=status.HTTP_200_OK)
def get_extended_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate extended Vimshottari Dasha with Mahadasha -> Antardasha -> Pratyantar."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
    moon_longitude = moon_info.get("longitude", None)
    result = calculate_extended_dasha(moon_nakshatra, str(row["birth_date"]), moon_longitude=moon_longitude)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/yogas-doshas", status_code=status.HTTP_200_OK)
def get_yogas_and_doshas(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Comprehensive Yoga & Dosha analysis — positive yogas and negative doshas."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})
    asc_sign = chart.get("ascendant", {}).get("sign", "")
    result = analyze_yogas_and_doshas(planets, asc_sign)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/lifelong-sadesati", status_code=status.HTTP_200_OK)
def get_lifelong_sadesati(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_sign = moon_info.get("sign", "Aries")
    ZODIAC = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    moon_sign_idx = ZODIAC.index(moon_sign)
    
    # parse birth datetime
    bd = row["birth_date"]
    bt = row["birth_time"]
    y, m, d = map(int, str(bd).split("-"))
    hr, mn, sec = 0, 0, 0
    if bt:
        parts = str(bt).split(":")
        hr = int(parts[0])
        mn = int(parts[1]) if len(parts) > 1 else 0
        sec = int(parts[2]) if len(parts) > 2 else 0
    dt = datetime(y, m, d, hr, mn, sec)
    
    result = calculate_lifelong_sade_sati(dt, moon_sign_idx, moon_sign)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/yogini-dasha", status_code=status.HTTP_200_OK)
def get_yogini_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
    moon_longitude = moon_info.get("longitude", 0.0)
    result = calculate_yogini_dasha(moon_nakshatra, str(row["birth_date"]), moon_longitude)
    return result
@router.get("/{kundli_id}/upagrahas", status_code=status.HTTP_200_OK)
def get_upagrahas(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    from app.upagraha_engine import calculate_upagrahas
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    
    result = calculate_upagrahas(
        birth_date=row["birth_date"],
        birth_time=row["birth_time"] or "12:00:00",
        lat=row["latitude"],
        lon=row["longitude"],
        tz_offset=row["timezone_offset"]
    )
    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "upagrahas": result
    }


@router.get("/{kundli_id}/sodashvarga", status_code=status.HTTP_200_OK)
def get_sodashvarga(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Sodashvarga — 16 divisional chart placements + Vimshopak Bala."""
    from app.sodashvarga_engine import calculate_sodashvarga
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})

    planet_longitudes = {}
    for pname, pinfo in planets.items():
        planet_longitudes[pname] = pinfo.get("longitude", 0.0)
    asc_lon = chart.get("ascendant", {}).get("longitude")
    if asc_lon is not None:
        planet_longitudes["Ascendant"] = asc_lon

    result = calculate_sodashvarga(planet_longitudes)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/aspects", status_code=status.HTTP_200_OK)
def get_aspects(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Planetary aspects on planets and bhavas."""
    from app.aspects_engine import calculate_aspects
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})
    houses = chart.get("houses", None)

    result = calculate_aspects(planets, houses)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/western-aspects", status_code=status.HTTP_200_OK)
def get_western_aspects(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Western degree-based aspects matrix (conjunction, square, trine, etc.)."""
    from app.aspects_engine import calculate_western_aspects, calculate_cusp_aspects
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})
    result = calculate_western_aspects(planets)

    # --- Aspects on Cusps (Nirayana + Sayana) ---
    nirayana_cusps = chart.get("placidus_cusps", [])
    if not nirayana_cusps or len(nirayana_cusps) != 12:
        # Fallback for older kundlis: compute equal-house cusps from ascendant
        asc_data = chart.get("ascendant", {})
        asc_lon = float(asc_data.get("longitude", 0.0)) if asc_data else 0.0
        if asc_lon > 0:
            nirayana_cusps = [round((asc_lon + i * 30.0) % 360.0, 4) for i in range(12)]
    if nirayana_cusps and len(nirayana_cusps) == 12:
        # Get ayanamsa to compute sayana (tropical) cusps
        ayanamsa_val = chart.get("ayanamsa_value")
        if ayanamsa_val is None:
            # Fallback: recalculate ayanamsa from birth data
            try:
                from app.astro_engine import _parse_datetime, _datetime_to_jd
                import swisseph as swe
                swe.set_sid_mode(swe.SIDM_LAHIRI)
                dt_local = _parse_datetime(
                    str(row["birth_date"]),
                    str(row["birth_time"]),
                    float(row["timezone_offset"]),
                )
                jd = _datetime_to_jd(dt_local)
                ayanamsa_val = swe.get_ayanamsa(jd)
            except Exception:
                ayanamsa_val = 24.0  # safe approximate fallback

        sayana_cusps = [(c + ayanamsa_val) % 360.0 for c in nirayana_cusps]
        cusp_aspects = calculate_cusp_aspects(planets, nirayana_cusps, sayana_cusps)
        result["cusp_aspects"] = cusp_aspects

    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/retrograde-stations", status_code=status.HTTP_200_OK)
def get_retrograde_stations(
    kundli_id: str,
    year: int = Query(default=None),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Retrograde and direct station dates for planets in a given year."""
    from app.retrograde_engine import calculate_retrograde_stations
    from datetime import datetime
    _fetch_kundli(db, kundli_id, current_user["sub"])  # validate access
    if not year:
        year = datetime.now().year
    stations = calculate_retrograde_stations(year)
    return {"kundli_id": kundli_id, "year": year, "stations": stations}


@router.get("/{kundli_id}/jaimini", status_code=status.HTTP_200_OK)
def get_jaimini(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Jaimini astrology — Chara Karakas, Special Lagnas, Drishti, Chara Dasha, Indu Lagna."""
    from app.jaimini_engine import calculate_jaimini
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    result = calculate_jaimini(chart, str(row.get("birth_date", "")))
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


# ── PDF Download ────────────────────────────────────────────

# Sign → Lord mapping used for house lordships table
_SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _sanitize_text(text: str) -> str:
    """Replace Unicode characters that Helvetica doesn't support."""
    return (str(text)
        .replace("\u2014", "-")   # em-dash
        .replace("\u2013", "-")   # en-dash
        .replace("\u2018", "'")   # left single quote
        .replace("\u2019", "'")   # right single quote
        .replace("\u201c", '"')   # left double quote
        .replace("\u201d", '"')   # right double quote
        .replace("\u2022", "*")   # bullet
        .replace("\u2026", "...")  # ellipsis
        .replace("\u00b0", "deg") # degree symbol
        .replace("\u2265", ">=")  # >=
        .replace("\u2264", "<=")  # <=
    )


def _build_kundli_pdf(row: dict, chart: dict) -> bytes:
    """Build a comprehensive, professional Kundli PDF report and return raw bytes.

    Page 1: Birth details + Planet table (extended) + Lordships
    Page 2: Vimshottari Dasha + Avakhada Chakra + Yoga/Dosha
    Page 3: Ashtakvarga (SAV + BAV) + Shadbala + io-gita
    """
    from fpdf import FPDF
    from datetime import datetime as _dt

    def _format_date_ddmmyyyy(d: str) -> str:
        """Convert YYYY-MM-DD to DD/MM/YYYY for display."""
        try:
            parts = str(d).split("-")
            if len(parts) == 3:
                return f"{parts[2]}/{parts[1]}/{parts[0]}"
        except Exception:
            pass
        return str(d)

    # ── Astrological reference tables ─────────────────────
    _SIGN_ELEMENT = {
        "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
        "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
        "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water",
    }
    _SIGN_MODALITY = {
        "Aries": "Moveable", "Taurus": "Fixed", "Gemini": "Dual",
        "Cancer": "Moveable", "Leo": "Fixed", "Virgo": "Dual",
        "Libra": "Moveable", "Scorpio": "Fixed", "Sagittarius": "Dual",
        "Capricorn": "Moveable", "Aquarius": "Fixed", "Pisces": "Dual",
    }
    _SIGN_GENDER = {
        "Aries": "M", "Taurus": "F", "Gemini": "M", "Cancer": "F",
        "Leo": "M", "Virgo": "F", "Libra": "M", "Scorpio": "F",
        "Sagittarius": "M", "Capricorn": "F", "Aquarius": "M", "Pisces": "F",
    }
    _EXALTATION = {
        "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
        "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    _DEBILITATION = {
        "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
        "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
        "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
    }
    _OWN_SIGNS = {
        "Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"],
        "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"],
        "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"],
    }
    _PLANET_NATURE = {
        "Sun": "Malefic", "Moon": "Benefic", "Mars": "Malefic", "Mercury": "Neutral",
        "Jupiter": "Benefic", "Venus": "Benefic", "Saturn": "Malefic",
        "Rahu": "Malefic", "Ketu": "Malefic",
    }

    def _get_dignity(planet: str, sign: str) -> str:
        if sign == _EXALTATION.get(planet):
            return "Exalted"
        if sign == _DEBILITATION.get(planet):
            return "Debilitated"
        if sign in _OWN_SIGNS.get(planet, []):
            return "Own Sign"
        return "Neutral"

    # ── Colors ────────────────────────────────────────────
    GOLD = (184, 134, 11)       # #B8860B
    GOLD_LIGHT = (245, 235, 210)
    ALT_ROW = (252, 248, 240)
    GREEN_MARK = (34, 139, 34)
    RED_MARK = (178, 34, 34)

    generated_date = _dt.now().strftime("%d %b %Y, %I:%M %p")
    footer_text = f"Powered by Semantic Gravity | astrorattan.com | Generated on {generated_date}"

    class KundliPDF(FPDF):
        def cell(self, w=0, h=0, txt="", *args, **kwargs):
            return super().cell(w, h, _sanitize_text(txt), *args, **kwargs)

        def multi_cell(self, w, h=0, txt="", *args, **kwargs):
            return super().multi_cell(w, h, _sanitize_text(txt), *args, **kwargs)

        def header(self):
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*GOLD)
            super().cell(0, 8, "Astro Rattan -- Vedic Birth Chart Report", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(2)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(120, 120, 120)
            super().cell(0, 8, _sanitize_text(f"Page {self.page_no()}  |  {footer_text}"), align="C")
            self.set_text_color(0, 0, 0)

        def section_title(self, title: str):
            self.set_font("Helvetica", "B", 11)
            self.set_fill_color(*GOLD)
            self.set_text_color(255, 255, 255)
            self.cell(0, 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(2)

        def table_header(self, cols: list, widths: list):
            self.set_font("Helvetica", "B", 8)
            self.set_fill_color(*GOLD_LIGHT)
            for i, h in enumerate(cols):
                self.cell(widths[i], 6, h, border=1, align="C", fill=True)
            self.ln()

        def table_row(self, vals: list, widths: list, row_idx: int = 0):
            self.set_font("Helvetica", "", 8)
            if row_idx % 2 == 1:
                self.set_fill_color(*ALT_ROW)
                fill = True
            else:
                fill = False
            for i, v in enumerate(vals):
                self.cell(widths[i], 5, str(v), border=1, align="C", fill=fill)
            self.ln()

    pdf = KundliPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ════════════════════════════════════════════════════════
    # PAGE 1: Birth Chart + Planet Details + Lordships
    # ════════════════════════════════════════════════════════
    pdf.add_page()

    # Birth details block
    person_name = row.get("person_name", "N/A")
    raw_birth_date = row.get("birth_date", "N/A")
    # Convert YYYY-MM-DD to DD/MM/YYYY for display
    try:
        bd_parts = str(raw_birth_date).split("-")
        birth_date = f"{bd_parts[2]}/{bd_parts[1]}/{bd_parts[0]}" if len(bd_parts) == 3 else str(raw_birth_date)
    except Exception:
        birth_date = str(raw_birth_date)
    birth_time = row.get("birth_time", "N/A")
    birth_place = row.get("birth_place", "N/A")
    ayanamsa = row.get("ayanamsa", "lahiri")

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 9, person_name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    asc_sign = chart.get("ascendant", {}).get("sign", "N/A")
    pdf.cell(0, 5, f"DOB: {birth_date}  |  Time: {birth_time}  |  Place: {birth_place}", align="C", new_x="LMARGIN", new_y="NEXT")
    ayanamsa_str = ayanamsa.title() if isinstance(ayanamsa, str) else str(ayanamsa)
    pdf.cell(0, 5, f"Ascendant (Lagna): {asc_sign}  |  Ayanamsa: {ayanamsa_str}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ── Planet Details Table (extended) ────────────────────
    planets = chart.get("planets", {})
    if planets:
        pdf.section_title("Planet Positions")

        p_headers = ["Planet", "Degree", "Sign", "M/F", "Modality", "Element", "Nakshatra", "Dignity", "R*", "Nature", "House"]
        p_widths = [17, 16, 20, 10, 18, 14, 22, 20, 8, 16, 12]  # sum ~173 fits in ~190 page width
        pdf.table_header(p_headers, p_widths)

        for idx, (planet_name, info) in enumerate(planets.items()):
            if not isinstance(info, dict):
                continue
            sign = info.get("sign", "N/A")
            degree_val = info.get("sign_degree", info.get("degree", None))
            degree_str = f"{degree_val:.1f}" if degree_val is not None else "N/A"
            house = str(info.get("house", "N/A"))
            nakshatra = info.get("nakshatra", "N/A")
            retro = "R" if info.get("retrograde") else ""
            gender = _SIGN_GENDER.get(sign, "?")
            modality = _SIGN_MODALITY.get(sign, "?")
            element = _SIGN_ELEMENT.get(sign, "?")
            dignity = _get_dignity(planet_name, sign)
            nature = _PLANET_NATURE.get(planet_name, "?")
            vals = [planet_name, degree_str, sign, gender, modality, element, nakshatra, dignity, retro, nature, house]
            pdf.table_row(vals, p_widths, idx)

        pdf.ln(4)

    # ── House Lordships Table ──────────────────────────────
    asc_sign_check = chart.get("ascendant", {}).get("sign")
    if asc_sign_check and asc_sign_check in _SIGN_ORDER:
        pdf.section_title("House Lordships")

        # Build planet-to-house lookup
        planet_house_map = {}
        for pn, pi in planets.items():
            if isinstance(pi, dict):
                planet_house_map[pn] = pi.get("house", "?")

        lord_headers = ["House", "Sign", "Lord", "Placed In"]
        lord_widths = [20, 35, 30, 25]
        pdf.table_header(lord_headers, lord_widths)

        asc_idx = _SIGN_ORDER.index(asc_sign_check)
        for house_num in range(1, 13):
            sign = _SIGN_ORDER[(asc_idx + house_num - 1) % 12]
            lord = _SIGN_LORD.get(sign, "N/A")
            placed_in = str(planet_house_map.get(lord, "?"))
            pdf.table_row([str(house_num), sign, lord, placed_in], lord_widths, house_num)

        pdf.ln(4)

    # ════════════════════════════════════════════════════════
    # PAGE 2: Dasha + Avakhada + Yoga/Dosha
    # ════════════════════════════════════════════════════════
    pdf.add_page()

    # ── Vimshottari Dasha ──────────────────────────────────
    moon_pdf_info = planets.get("Moon", {}) if planets else {}
    moon_nakshatra = moon_pdf_info.get("nakshatra", "Ashwini")
    moon_pdf_lon = moon_pdf_info.get("longitude", None)
    dasha_result = calculate_dasha(moon_nakshatra, str(birth_date), moon_longitude=moon_pdf_lon)

    pdf.section_title("Vimshottari Dasha")
    current_md = dasha_result.get("current_dasha", "Unknown")
    current_ad = dasha_result.get("current_antardasha", "Unknown")
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, f"Current Mahadasha: {current_md}  |  Current Antardasha: {current_ad}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    dasha_headers = ["Planet", "Start Date", "End Date", "Years"]
    dasha_widths = [30, 45, 45, 20]
    pdf.table_header(dasha_headers, dasha_widths)

    for idx, period in enumerate(dasha_result.get("mahadasha_periods", [])):
        planet = period.get("planet", "?")
        start = _format_date_ddmmyyyy(period.get("start_date", "?"))
        end = _format_date_ddmmyyyy(period.get("end_date", "?"))
        years = str(period.get("years", "?"))
        marker = " <" if planet == current_md else ""
        pdf.table_row([planet + marker, start, end, years], dasha_widths, idx)

    pdf.ln(4)

    # ── Avakhada Chakra ────────────────────────────────────
    avakhada = calculate_avakhada(chart)

    pdf.section_title("Avakhada Chakra")
    avakhada_items = [
        ("Ascendant", avakhada.get("ascendant", "N/A")),
        ("Ascendant Lord", avakhada.get("ascendant_lord", "N/A")),
        ("Rashi (Moon Sign)", avakhada.get("rashi", "N/A")),
        ("Rashi Lord", avakhada.get("rashi_lord", "N/A")),
        ("Nakshatra", f"{avakhada.get('nakshatra', 'N/A')} (Pada {avakhada.get('nakshatra_pada', 'N/A')})"),
        ("Yoga", avakhada.get("yoga", "N/A")),
        ("Karana", avakhada.get("karana", "N/A")),
        ("Yoni", avakhada.get("yoni", "N/A")),
        ("Gana", avakhada.get("gana", "N/A")),
        ("Nadi", avakhada.get("nadi", "N/A")),
        ("Varna", avakhada.get("varna", "N/A")),
        ("Naamakshar", avakhada.get("naamakshar", "N/A")),
        ("Sun Sign", avakhada.get("sun_sign", "N/A")),
    ]
    # Two-column layout
    pdf.set_font("Helvetica", "", 8)
    col_w = 48
    val_w = 45
    for i in range(0, len(avakhada_items), 2):
        label1, val1 = avakhada_items[i]
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(col_w, 5, label1 + ":", border=0)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(val_w, 5, str(val1), border=0)
        if i + 1 < len(avakhada_items):
            label2, val2 = avakhada_items[i + 1]
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(col_w, 5, label2 + ":", border=0)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(val_w, 5, str(val2), border=0)
        pdf.ln()

    pdf.ln(4)

    # ── Yoga & Dosha Summary ───────────────────────────────
    if planets:
        yoga_dosha = analyze_yogas_and_doshas(planets, chart.get("ascendant", {}).get("sign", ""))

        yogas = yoga_dosha.get("yogas", [])
        if yogas:
            pdf.section_title("Yogas (Positive Combinations)")
            pdf.set_font("Helvetica", "", 8)
            for y in yogas:
                if isinstance(y, dict):
                    name = y.get("name", y.get("yoga", "Yoga"))
                    present = y.get("present", True)
                    desc = y.get("description", y.get("effect", ""))
                    if present:
                        pdf.set_text_color(*GREEN_MARK)
                    pdf.set_font("Helvetica", "B", 8)
                    marker = "[+]" if present else "[ ]"
                    pdf.cell(0, 5, f"  {marker} {name}", new_x="LMARGIN", new_y="NEXT")
                    pdf.set_text_color(0, 0, 0)
                    if desc:
                        pdf.set_font("Helvetica", "", 7)
                        pdf.multi_cell(0, 4, f"      {desc}")
                else:
                    pdf.cell(0, 5, f"  {y}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        doshas = yoga_dosha.get("doshas", [])
        if doshas:
            pdf.section_title("Doshas (Afflictions)")
            pdf.set_font("Helvetica", "", 8)
            for d in doshas:
                if isinstance(d, dict):
                    name = d.get("name", d.get("dosha", "Dosha"))
                    severity = d.get("severity", "")
                    present = d.get("present", True)
                    desc = d.get("description", d.get("effect", ""))
                    label = f"  {name}"
                    if severity:
                        label += f" [{severity}]"
                    if present:
                        pdf.set_text_color(*RED_MARK)
                    pdf.set_font("Helvetica", "B", 8)
                    marker = "[!]" if present else "[ ]"
                    pdf.cell(0, 5, f"  {marker}{label}", new_x="LMARGIN", new_y="NEXT")
                    pdf.set_text_color(0, 0, 0)
                    if desc:
                        pdf.set_font("Helvetica", "", 7)
                        pdf.multi_cell(0, 4, f"      {desc}")
                else:
                    pdf.cell(0, 5, f"  {d}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

    # ════════════════════════════════════════════════════════
    # PAGE 3: Ashtakvarga + Shadbala + io-gita
    # ════════════════════════════════════════════════════════
    pdf.add_page()

    # ── Ashtakvarga ────────────────────────────────────────
    # Build planet_signs for ashtakvarga engine
    planet_signs_map = {}
    for pn, pi in planets.items():
        if isinstance(pi, dict):
            planet_signs_map[pn] = pi.get("sign", "Aries")
    asc_sign_av = chart.get("ascendant", {}).get("sign")
    if asc_sign_av:
        planet_signs_map["Ascendant"] = asc_sign_av

    ashtak = calculate_ashtakvarga(planet_signs_map)

    # SAV table
    pdf.section_title("Sarvashtakvarga (SAV)")
    sav = ashtak.get("sarvashtakvarga", {})
    sav_signs_short = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
    sav_widths = [15] * 12
    total_sav = sum(sav.get(s, 0) for s in _SIGN_ORDER)
    pdf.table_header(sav_signs_short, sav_widths)
    sav_vals = [str(sav.get(s, 0)) for s in _SIGN_ORDER]
    pdf.table_row(sav_vals, sav_widths, 0)
    pdf.set_font("Helvetica", "I", 7)
    pdf.cell(0, 4, f"Total SAV: {total_sav}  |  28+ per sign = strong", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # BAV table
    pdf.section_title("Bhinnashtakvarga (BAV)")
    bav = ashtak.get("planet_bindus", {})
    bav_headers = ["Planet"] + sav_signs_short + ["Total"]
    bav_widths_row = [17] + [13] * 12 + [17]
    pdf.table_header(bav_headers, bav_widths_row)
    for idx, planet in enumerate(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]):
        bindus = bav.get(planet, {})
        row_vals = [planet]
        row_total = 0
        for s in _SIGN_ORDER:
            v = bindus.get(s, 0)
            row_total += v
            row_vals.append(str(v))
        row_vals.append(str(row_total))
        pdf.table_row(row_vals, bav_widths_row, idx)

    pdf.ln(4)

    # ── Shadbala ───────────────────────────────────────────
    planet_houses_map = {}
    planet_longs_map = {}
    retro_set = set()
    for pn, pi in planets.items():
        if isinstance(pi, dict):
            planet_houses_map[pn] = pi.get("house", 1)
            if "longitude" in pi:
                planet_longs_map[pn] = pi["longitude"]
            if pi.get("retrograde") or "Retrograde" in pi.get("status", ""):
                retro_set.add(pn)
    bt = row.get("birth_time", "12:00:00")
    try:
        _bt_parts = str(bt).split(":")
        _pdf_birth_hour = int(_bt_parts[0]) + int(_bt_parts[1]) / 60.0
    except (ValueError, IndexError):
        _pdf_birth_hour = 12.0
    is_day = 6.0 <= _pdf_birth_hour < 18.0
    _pdf_sun_lon = planet_longs_map.get("Sun", 0.0)
    _pdf_moon_lon = planet_longs_map.get("Moon", 0.0)
    _pdf_elongation = (_pdf_moon_lon - _pdf_sun_lon) % 360.0
    try:
        _pdf_bd = datetime.strptime(str(row.get("birth_date", "2000-01-01")), "%Y-%m-%d")
        _pdf_weekday = _pdf_bd.weekday()
        _pdf_year = _pdf_bd.year
        _pdf_month = _pdf_bd.month
    except (ValueError, TypeError):
        _pdf_weekday, _pdf_year, _pdf_month = 0, 2000, 1
    shadbala = calculate_shadbala(
        planet_signs=planet_signs_map,
        planet_houses=planet_houses_map,
        is_daytime=is_day,
        retrograde_planets=retro_set,
        planet_longitudes=planet_longs_map,
        birth_hour=_pdf_birth_hour,
        moon_sun_elongation=_pdf_elongation,
        weekday=_pdf_weekday,
        birth_year=_pdf_year,
        birth_month=_pdf_month,
    )

    pdf.section_title("Shadbala (Six-fold Strength)")
    sb_headers = ["Planet", "Sthana", "Dig", "Kala", "Cheshta", "Naisargika", "Drik", "Total", "Reqd", "Ratio"]
    sb_widths = [17, 17, 15, 15, 17, 20, 15, 17, 15, 15]
    pdf.table_header(sb_headers, sb_widths)
    sb_planets_data = shadbala.get("planets", {})
    for idx, planet in enumerate(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]):
        d = sb_planets_data.get(planet)
        if not d:
            continue
        vals = [
            planet,
            str(d.get("sthana", 0)),
            str(d.get("dig", 0)),
            str(d.get("kala", 0)),
            str(d.get("cheshta", 0)),
            str(d.get("naisargika", 0)),
            str(d.get("drik", 0)),
            str(d.get("total", 0)),
            str(d.get("required", 0)),
            f"{d.get('ratio', 0)}x",
        ]
        pdf.table_row(vals, sb_widths, idx)

    pdf.ln(4)

    # ── io-gita Analysis (if stored) ──────────────────────
    iogita_raw = row.get("iogita_analysis")
    if iogita_raw:
        try:
            iogita = json.loads(iogita_raw) if isinstance(iogita_raw, str) else iogita_raw
        except (json.JSONDecodeError, TypeError):
            iogita = None
        if iogita and isinstance(iogita, dict):
            pdf.section_title("io-gita Semantic Gravity Analysis")
            pdf.set_font("Helvetica", "", 8)
            for key, val in iogita.items():
                text = f"{key}: {val}"
                pdf.multi_cell(0, 4, text)
            pdf.ln(3)

    # Return raw bytes
    return pdf.output()


@router.get("/{kundli_id}/pdf", status_code=status.HTTP_200_OK)
def download_kundli_pdf(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Generate and stream a Kundli PDF report for download."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    try:
        pdf_bytes = _build_kundli_pdf(row, chart)
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF generation unavailable — fpdf2 not installed",
        )

    safe_name = (row.get("person_name") or "kundli").replace(" ", "_")
    filename = f"kundli-{safe_name}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{kundli_id}/transits", status_code=status.HTTP_200_OK)
def get_transits(
    kundli_id: str,
    body: dict = None,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Gochara (transit) predictions for a kundli. Accepts optional transit_date and transit_time."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    body = body or {}
    transit_date = body.get("transit_date")
    transit_time = body.get("transit_time")
    result = calculate_transits(
        chart,
        latitude=row.get("latitude", 0.0),
        longitude=row.get("longitude", 0.0),
        transit_date=transit_date,
        transit_time=transit_time,
    )
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/kp-analysis", status_code=status.HTTP_200_OK)
def get_kp_analysis(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """KP (Krishnamurti Paddhati) analysis — sign lord, star lord, sub lord for planets and cusps."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])

    # Recalculate chart with KP (Krishnamurti) ayanamsa for accurate KP positions
    chart = calculate_planet_positions(
        birth_date=row["birth_date"],
        birth_time=row["birth_time"],
        latitude=row.get("latitude", 0.0),
        longitude=row.get("longitude", 0.0),
        tz_offset=row.get("timezone_offset", 0.0),
        ayanamsa="kp",
    )

    # Extract planet longitudes
    planet_longitudes = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_longitudes[planet_name] = info.get("longitude", 0.0)

    if not planet_longitudes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet longitudes",
        )

    # Extract house cusps (Placidus from swisseph) or fallback to equal houses
    house_cusps = chart.get("placidus_cusps", chart.get("house_cusps", []))
    if not house_cusps or len(house_cusps) != 12:
        asc_lon = chart.get("ascendant", {}).get("longitude", 0.0)
        house_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]

    try:
        kp = calculate_kp_cuspal(
            planet_longitudes, house_cusps,
            chart_data=chart, birth_date=row.get("birth_date"),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    # Shape response: planets as list with all KP fields
    planets_list = []
    for pname, pinfo in kp.get("planets", {}).items():
        planets_list.append({
            "planet": pname,
            "retrograde": pinfo.get("retrograde", False),
            "sign": pinfo.get("sign", ""),
            "sign_lord": pinfo.get("sign_lord", ""),
            "star_lord": pinfo.get("star_lord", ""),
            "sub_lord": pinfo.get("sub_lord", ""),
            "sub_sub_lord": pinfo.get("sub_sub_lord", ""),
            "nakshatra": pinfo.get("nakshatra", ""),
            "pada": pinfo.get("pada", 0),
            "degree": pinfo.get("longitude", 0.0),
            "degree_dms": pinfo.get("degree_dms", ""),
        })

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "planets": planets_list,
        "cusps": kp.get("cusps", []),
        "significators": kp.get("significators", {}),
        "house_significations": kp.get("house_significations", {}),
        "planet_significator_strengths": kp.get("planet_significator_strengths", {}),
        "ruling_planets": kp.get("ruling_planets", {}),
    }


# ── Varshphal (Solar Return / Annual Chart) ──────────────────────

@router.post("/{kundli_id}/varshphal", status_code=status.HTTP_200_OK)
def get_varshphal(
    kundli_id: str,
    body: dict = None,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Varshphal (annual horoscope) for a given year."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Default to current year if not specified
    from datetime import datetime as _dt
    target_year = (body or {}).get("year", _dt.now().year)

    result = calculate_varshphal(
        natal_chart_data=chart,
        target_year=target_year,
        birth_date=row["birth_date"],
        latitude=row.get("latitude", 0.0),
        longitude=row.get("longitude", 0.0),
        tz_offset=row.get("timezone_offset", 5.5),
    )
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


# ── delete kundli ─────────────────────────────────────────────────
# NOTE: More specific routes must come BEFORE dynamic routes like /{kundli_id}

@router.delete("/user/all", status_code=status.HTTP_200_OK)
async def delete_all_my_kundlis(
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete all kundlis for the current user."""
    user_id = current_user["sub"]
    count_row = db.execute(
        "SELECT COUNT(*) as count FROM kundlis WHERE user_id = %s", (user_id,)
    ).fetchone()
    deleted_count = count_row["count"] if count_row else 0

    # Delete dependent records first (foreign key references to kundlis)
    db.execute(
        "DELETE FROM ai_chat_logs WHERE kundli_id IN (SELECT id FROM kundlis WHERE user_id = %s)",
        (user_id,),
    )
    db.execute(
        "DELETE FROM reports WHERE kundli_id IN (SELECT id FROM kundlis WHERE user_id = %s)",
        (user_id,),
    )
    db.execute("DELETE FROM kundlis WHERE user_id = %s", (user_id,))
    db.commit()

    return {
        "message": "All kundlis deleted successfully",
        "deleted_count": deleted_count,
    }


@router.delete("/{kundli_id}", status_code=status.HTTP_200_OK)
async def delete_kundli(
    kundli_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a kundli (only if owned by current user or admin)."""
    try:
        # Check if kundli exists and belongs to user
        row = db.execute(
            "SELECT user_id FROM kundlis WHERE id = %s",
            (kundli_id,)
        ).fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kundli not found"
            )
        
        # Check ownership (allow admin to delete any)
        if row["user_id"] != current_user["sub"] and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this kundli"
            )
        
        # Delete dependent records first (foreign key references)
        db.execute("DELETE FROM ai_chat_logs WHERE kundli_id = %s", (kundli_id,))
        db.execute("DELETE FROM reports WHERE kundli_id = %s", (kundli_id,))
        db.execute("DELETE FROM kundlis WHERE id = %s", (kundli_id,))
        db.commit()
        
        return {"message": "Kundli deleted successfully", "kundli_id": kundli_id}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"ERROR in delete_kundli: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An internal error occurred")
