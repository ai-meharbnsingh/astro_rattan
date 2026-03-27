"""Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha, divisional, ashtakvarga."""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.database import get_db
from app.models import KundliRequest, KundliMatchRequest, DivisionalChartRequest
from app.astro_engine import calculate_planet_positions
from app.astro_iogita_engine import run_astro_analysis
from app.matching_engine import calculate_gun_milan
from app.dosha_engine import check_mangal_dosha, check_kaal_sarp, check_sade_sati
from app.dasha_engine import calculate_dasha
from app.divisional_charts import calculate_divisional_chart
from app.ashtakvarga_engine import calculate_ashtakvarga

router = APIRouter(prefix="/api/kundli", tags=["kundli"])


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
    """Generate a new Vedic birth chart (kundli) and store it."""
    chart_data = calculate_planet_positions(
        birth_date=body.birth_date,
        birth_time=body.birth_time,
        latitude=body.latitude,
        longitude=body.longitude,
        tz_offset=body.timezone_offset,
    )
    chart_json = json.dumps(chart_data, default=str)

    db.execute(
        """INSERT INTO kundlis
           (user_id, person_name, birth_date, birth_time, birth_place,
            latitude, longitude, timezone_offset, ayanamsa, chart_data)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            current_user["sub"],
            body.person_name,
            body.birth_date,
            body.birth_time,
            body.birth_place,
            body.latitude,
            body.longitude,
            body.timezone_offset,
            body.ayanamsa,
            chart_json,
        ),
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (current_user["sub"],),
    ).fetchone()

    return {
        "id": row["id"],
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "chart_data": json.loads(row["chart_data"]),
        "created_at": row["created_at"],
    }


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
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "timezone_offset": row["timezone_offset"],
        "ayanamsa": row["ayanamsa"],
        "chart_data": json.loads(row["chart_data"]),
        "iogita_analysis": json.loads(row["iogita_analysis"]) if row["iogita_analysis"] else None,
        "created_at": row["created_at"],
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
    dasha_result = calculate_dasha(moon_nakshatra, row["birth_date"])
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


@router.post("/match", status_code=status.HTTP_200_OK)
def match_kundlis(
    body: KundliMatchRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Ashtakoota Gun Milan — match two kundlis for compatibility."""
    row1 = _fetch_kundli(db, body.kundli_id_1, current_user["sub"])
    row2 = _fetch_kundli(db, body.kundli_id_2, current_user["sub"])

    chart1 = _chart_data(row1)
    chart2 = _chart_data(row2)

    moon1 = chart1.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")
    moon2 = chart2.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")

    result = calculate_gun_milan(moon1, moon2)
    result["person1"] = row1["person_name"]
    result["person2"] = row2["person_name"]
    return result


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

    # Sade Sati (use Moon sign + Saturn sign from chart)
    moon_sign = planets.get("Moon", {}).get("sign", "Aries")
    saturn_sign = planets.get("Saturn", {}).get("sign", "Capricorn")
    sade_sati = check_sade_sati(moon_sign, saturn_sign)

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "mangal_dosha": mangal,
        "kaal_sarp_dosha": kaal_sarp,
        "sade_sati": sade_sati,
    }


@router.post("/{kundli_id}/dasha", status_code=status.HTTP_200_OK)
def get_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Vimshottari Dasha periods for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    moon_nakshatra = chart.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")
    result = calculate_dasha(moon_nakshatra, row["birth_date"])
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


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

    result = calculate_divisional_chart(planet_longitudes, division)
    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "chart_type": chart_type,
        "division": division,
        "planet_signs": result,
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
