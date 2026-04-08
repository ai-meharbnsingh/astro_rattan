"""Mundane Astrology routes — country charts, national analysis, eclipses, ingress."""
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.mundane_engine import (
    COUNTRY_CHARTS,
    calculate_eclipses,
    calculate_ingress,
    calculate_mundane_analysis,
)

router = APIRouter(prefix="/api/mundane", tags=["mundane"])


# ── List available countries ──────────────────────────────────

@router.get("/countries", status_code=status.HTTP_200_OK)
def list_countries():
    """Return the list of available country charts for mundane analysis."""
    countries = []
    for key, info in COUNTRY_CHARTS.items():
        countries.append({
            "key": key,
            "name": {"en": info["name"], "hi": info["name_hi"]},
            "capital": {"en": info["capital"], "hi": info["capital_hi"]},
            "independence_date": info["date"],
            "description": info["description"],
        })
    return {"countries": countries}


# ── Full mundane analysis for a country ───────────────────────

@router.get("/{country_key}/analysis", status_code=status.HTTP_200_OK)
def get_mundane_analysis(
    country_key: str,
    year: Optional[int] = Query(
        default=None,
        description="Year for eclipse/ingress data (defaults to current year)",
    ),
):
    """
    Full mundane astrology analysis for a country: birth chart, current transits,
    house analysis, conflict/economic/political/health/international indicators,
    and a summary.
    """
    if country_key not in COUNTRY_CHARTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "en": f"Country '{country_key}' not found. Use /api/mundane/countries for available options.",
                "hi": f"देश '{country_key}' नहीं मिला। उपलब्ध विकल्पों के लिए /api/mundane/countries का उपयोग करें।",
            },
        )

    result = calculate_mundane_analysis(country_key, year)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )
    return result


# ── Eclipse data ──────────────────────────────────────────────

@router.get("/eclipses", status_code=status.HTTP_200_OK)
def get_eclipses(
    year: int = Query(
        default=None,
        description="Year to retrieve eclipse data for (2024-2027 available)",
    ),
    country_key: Optional[str] = Query(
        default=None,
        description="Optional country key to calculate affected house in national chart",
    ),
):
    """
    Return solar and lunar eclipse data for a given year.
    Optionally maps each eclipse to the affected house in a country's chart.
    """
    if year is None:
        year = datetime.now(timezone.utc).year

    if year < 2024 or year > 2027:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "en": f"Eclipse data is available for years 2024-2027 only. Received: {year}",
                "hi": f"ग्रहण डेटा केवल 2024-2027 वर्षों के लिए उपलब्ध है। प्राप्त: {year}",
            },
        )

    if country_key and country_key not in COUNTRY_CHARTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "en": f"Country '{country_key}' not found.",
                "hi": f"देश '{country_key}' नहीं मिला।",
            },
        )

    eclipses = calculate_eclipses(year, country_key)
    return {
        "year": year,
        "country": country_key,
        "eclipses": eclipses,
        "total_count": len(eclipses),
    }


# ── Ingress / Sankranti dates ────────────────────────────────

@router.get("/ingress", status_code=status.HTTP_200_OK)
def get_ingress(
    year: int = Query(
        default=None,
        description="Year to calculate Sankranti (solar ingress) dates for",
    ),
):
    """
    Return the dates when the Sun enters each of the 12 sidereal signs
    (Sankranti / solar ingress dates) for a given year.
    """
    if year is None:
        year = datetime.now(timezone.utc).year

    ingress_data = calculate_ingress(year)
    return {
        "year": year,
        "description": {
            "en": "Sankranti dates — Sun's entry into each sidereal sign",
            "hi": "संक्रांति तिथियाँ — सूर्य का प्रत्येक सायन राशि में प्रवेश",
        },
        "ingress": ingress_data,
    }
