"""KP Astrology and Lal Kitab Remedies routes."""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.database import get_db
from app.kp_engine import calculate_kp_cuspal
from app.lalkitab_engine import get_remedies

router = APIRouter()


@router.post("/api/kp/cuspal")
def kp_cuspal(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Calculate KP cuspal chart with star lords, sub lords, and significators.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_longitudes and house_cusps from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    chart_data = json.loads(row["chart_data"])

    # Extract planet longitudes from chart_data
    planet_longitudes = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        planet_longitudes[planet_name] = info.get("longitude", 0.0)

    # Extract house cusps from chart_data
    house_cusps = chart_data.get("placidus_cusps", chart_data.get("house_cusps", []))
    if not house_cusps or len(house_cusps) != 12:
        # Generate default cusps from ascendant if house_cusps not stored
        asc_lon = chart_data.get("ascendant", {}).get("longitude", 0.0)
        house_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]

    if not planet_longitudes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet longitudes",
        )

    try:
        result = calculate_kp_cuspal(planet_longitudes, house_cusps)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    # Contract response: {cuspal_chart, significators}
    return {
        "cuspal_chart": {
            "cusps": result.get("cusps", []),
            "planets": result.get("planets", {}),
        },
        "significators": result.get("significators", {}),
    }


@router.post("/api/lalkitab/remedies")
def lalkitab_remedies(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Get Lal Kitab remedies for weak or afflicted planets.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_positions from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    chart_data = json.loads(row["chart_data"])

    # Extract planet positions as {planet: sign}
    planet_positions = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        planet_positions[planet_name] = info.get("sign", "Aries")

    if not planet_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        result = get_remedies(planet_positions)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {"remedies_by_planet": result}
