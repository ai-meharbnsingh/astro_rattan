"""
Interpretation text API routes — serves prediction/personality text
from the static interpretation database to kundli pages and PDF reports.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.database import get_db
from app.reports.interpretations import (
    ASCENDANT_PERSONALITY,
    DASHA_INTERPRETATIONS,
    ANTARDASHA_INTERPRETATIONS,
    LAGNA_NATURE,
    LIFE_PREDICTIONS,
    MAHADASHA_DETAILED,
    NAKSHATRA_INTERPRETATIONS,
    NAKSHATRA_PHAL,
    PLANET_IN_HOUSE,
    BHAVESH_INTERPRETATIONS,
    GEMSTONE_DATA,
)

router = APIRouter(prefix="/api/interpretations", tags=["interpretations"])


# ── Helper to fetch kundli chart data ──────────────────────────
def _fetch_chart(db, kundli_id: str, user_id: str) -> dict:
    import json
    row = db.execute(
        "SELECT chart_data, person_name, birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")
    chart = json.loads(row["chart_data"]) if isinstance(row["chart_data"], str) else row["chart_data"]
    return {"chart": chart, "person_name": row["person_name"], "birth_date": str(row["birth_date"])}


@router.get("/lagna/{sign}", status_code=status.HTTP_200_OK)
def get_lagna_interpretation(sign: str):
    """Get ascendant personality profile for a zodiac sign."""
    sign_title = sign.strip().title()
    lagna = LAGNA_NATURE.get(sign_title)
    personality = ASCENDANT_PERSONALITY.get(sign_title)
    if not lagna:
        raise HTTPException(status_code=404, detail=f"Sign '{sign}' not found")
    return {
        "sign": sign_title,
        "lagna_nature": lagna,
        "personality": personality or {},
    }


@router.get("/nakshatra/{nakshatra}", status_code=status.HTTP_200_OK)
def get_nakshatra_interpretation(nakshatra: str, pada: int = None):
    """Get nakshatra interpretation + pada-specific predictions."""
    nak_title = nakshatra.strip().title()
    interp = NAKSHATRA_INTERPRETATIONS.get(nak_title)
    if not interp:
        raise HTTPException(status_code=404, detail=f"Nakshatra '{nakshatra}' not found")
    result = {"nakshatra": nak_title, "interpretation": interp}
    phal = NAKSHATRA_PHAL.get(nak_title, {})
    if pada and pada in phal:
        result["pada_prediction"] = phal[pada]
        result["pada"] = pada
    elif phal:
        result["all_pada_predictions"] = phal
    return result


@router.get("/planet-in-house/{planet}/{house}", status_code=status.HTTP_200_OK)
def get_planet_in_house(planet: str, house: int):
    """Get interpretation for a planet in a specific house."""
    planet_title = planet.strip().title()
    planet_data = PLANET_IN_HOUSE.get(planet_title)
    if not planet_data:
        raise HTTPException(status_code=404, detail=f"Planet '{planet}' not found")
    house_data = planet_data.get(house)
    if not house_data:
        raise HTTPException(status_code=404, detail=f"House {house} not found for {planet}")
    return {"planet": planet_title, "house": house, "interpretation": house_data}


@router.get("/dasha/{planet}", status_code=status.HTTP_200_OK)
def get_dasha_interpretation(planet: str, house: int = None):
    """Get mahadasha interpretation. Optionally include house-specific detail."""
    planet_title = planet.strip().title()
    general = DASHA_INTERPRETATIONS.get(planet_title)
    if not general:
        raise HTTPException(status_code=404, detail=f"Planet '{planet}' not found")
    result = {"planet": planet_title, "general": general}
    if house is not None:
        detailed = MAHADASHA_DETAILED.get(planet_title, {})
        house_text = detailed.get(house)
        if house_text:
            result["house_specific"] = {"house": house, "prediction": house_text}
    return result


@router.get("/life-predictions/{area}/{sign}", status_code=status.HTTP_200_OK)
def get_life_prediction(area: str, sign: str):
    """Get life prediction for a specific area and house sign."""
    area_lower = area.strip().lower()
    sign_title = sign.strip().title()
    area_data = LIFE_PREDICTIONS.get(area_lower)
    if not area_data:
        valid = list(LIFE_PREDICTIONS.keys())
        raise HTTPException(status_code=404, detail=f"Area '{area}' not found. Valid: {valid}")
    text = area_data.get(sign_title)
    if not text:
        raise HTTPException(status_code=404, detail=f"Sign '{sign}' not found for area '{area}'")
    return {"area": area_lower, "sign": sign_title, "prediction": text}


@router.get("/kundli/{kundli_id}/full", status_code=status.HTTP_200_OK)
def get_full_interpretations(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get all interpretation texts for a kundli — personality, life predictions,
    dasha, nakshatra phal, planet-in-house for all planets."""
    data = _fetch_chart(db, kundli_id, current_user["sub"])
    chart = data["chart"]
    planets = chart.get("planets", {})
    ascendant = chart.get("ascendant", {})
    houses = chart.get("houses", [])

    asc_sign = ascendant.get("sign", "Aries")
    moon = planets.get("Moon", {})
    moon_nak = moon.get("nakshatra", "Ashwini") if isinstance(moon, dict) else "Ashwini"
    moon_pada = moon.get("pada", 1) if isinstance(moon, dict) else 1

    # Build house-sign map (whole sign)
    house_signs = {}
    if houses:
        for h in houses:
            if isinstance(h, dict):
                house_signs[h.get("house", 0)] = h.get("sign", "")

    result = {
        "kundli_id": kundli_id,
        "person_name": data["person_name"],
    }

    # 1. Ascendant personality
    result["ascendant"] = {
        "sign": asc_sign,
        "lagna_nature": LAGNA_NATURE.get(asc_sign, {}),
        "personality": ASCENDANT_PERSONALITY.get(asc_sign, {}),
    }

    # 2. Nakshatra Phal
    result["nakshatra"] = {
        "name": moon_nak,
        "pada": moon_pada,
        "interpretation": NAKSHATRA_INTERPRETATIONS.get(moon_nak, {}),
        "pada_prediction": NAKSHATRA_PHAL.get(moon_nak, {}).get(moon_pada, ""),
    }

    # 3. Life predictions (based on house signs)
    life = {}
    area_house_map = {
        "career": 10, "health": 6, "marriage": 7, "finance": 2,
        "education": 5, "character": 1, "hobbies": 5, "family": 4,
    }
    for area, house_num in area_house_map.items():
        sign = house_signs.get(house_num, asc_sign)
        area_data = LIFE_PREDICTIONS.get(area, {})
        life[area] = area_data.get(sign, "")
    result["life_predictions"] = life

    # 4. Planet in house for all 9 planets
    pih = {}
    for pname, pdata in planets.items():
        if isinstance(pdata, dict) and pname in PLANET_IN_HOUSE:
            h = pdata.get("house", 1)
            pih[pname] = PLANET_IN_HOUSE[pname].get(h, {})
    result["planet_in_house"] = pih

    # 5. Current dasha interpretation
    # (caller should pass current mahadasha planet separately, but we include all)
    result["dasha_interpretations"] = {
        p: DASHA_INTERPRETATIONS.get(p, {}) for p in
        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    }

    # 6. Gemstone recommendations
    result["gemstones"] = GEMSTONE_DATA

    return result
