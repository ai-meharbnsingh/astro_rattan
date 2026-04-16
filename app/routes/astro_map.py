"""Astro-Cartography / Locational Astrology routes."""
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.astro_mapping_engine import (
    MAJOR_CITIES,
    calculate_astro_map,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/astro-map", tags=["astro-map"])


# ── Request / Response models ────────────────────────────────

class AstroMapRequest(BaseModel):
    birth_date: str = Field(..., description="Birth date YYYY-MM-DD")
    birth_time: str = Field(..., description="Birth time HH:MM:SS")
    tz_offset: float = Field(..., ge=-12, le=14, description="Timezone offset in hours (e.g. 5.5 for IST)")
    planet_longitudes: Dict[str, float] = Field(
        ...,
        description="Sidereal longitudes for planets, e.g. {\"Sun\": 126.87, \"Moon\": 224.02, ...}",
    )
    cities: Optional[List[str]] = Field(
        default=None,
        description="Optional list of city names to analyse. Defaults to all major cities.",
    )


# ── POST /api/astro-map ─────────────────────────────────────

@router.post("", status_code=status.HTTP_200_OK)
def post_astro_map(req: AstroMapRequest):
    """
    Calculate Astro-Cartography analysis for a birth chart across cities.

    Accepts planet longitudes (sidereal) and returns per-city house placements,
    strengths/cautions, overall scores, best-city rankings by life area, and
    planetary line data.
    """
    # Resolve city subset
    cities_dict: Optional[Dict[str, tuple]] = None
    if req.cities:
        unknown = [c for c in req.cities if c not in MAJOR_CITIES]
        if unknown:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": f"Unknown cities: {', '.join(unknown)}. Use GET /api/astro-map/cities for available options.",
                    "hi": f"अज्ञात शहर: {', '.join(unknown)}। उपलब्ध विकल्पों के लिए GET /api/astro-map/cities का उपयोग करें।",
                },
            )
        cities_dict = {c: MAJOR_CITIES[c] for c in req.cities}

    try:
        result = calculate_astro_map(
            birth_date=req.birth_date,
            birth_time=req.birth_time,
            birth_tz_offset=req.tz_offset,
            planet_longitudes=req.planet_longitudes,
            cities=cities_dict,
        )
    except Exception:
        logger.exception("Astro-map calculation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "en": "Astro-map calculation failed. Please check input data.",
                "hi": "ज्योतिष-मानचित्र गणना विफल। कृपया इनपुट डेटा जांचें।",
            },
        )

    return result


# ── GET /api/astro-map/cities ────────────────────────────────

@router.get("/cities", status_code=status.HTTP_200_OK)
def list_available_cities():
    """Return the list of supported cities with coordinates."""
    cities = [
        {"name": name, "latitude": lat, "longitude": lon}
        for name, (lat, lon) in sorted(MAJOR_CITIES.items())
    ]
    return {"cities": cities, "total": len(cities)}
