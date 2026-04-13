"""Vastu Shastra routes — mandala analysis, entrance padas, remedies, room placement."""
from typing import Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.auth import get_current_user

from app.vastu.engine import (
    calculate_mandala,
    analyze_entrance,
    suggest_remedies,
    get_room_placement,
    get_complete_vastu_analysis,
)

router = APIRouter(tags=["vastu"])


# ============================================================
# Pydantic request models
# ============================================================
class BuildingType(str, Enum):
    residential = "residential"
    commercial = "commercial"
    temple = "temple"


VALID_PROBLEMS = {
    "wealth", "health", "relationship", "career", "education",
    "legal", "sleep", "conflict", "fertility", "depression", "debt", "accident",
}


class VastuRemediesRequest(BaseModel):
    problems: list[str] = Field(min_length=1, description="Problem keywords: wealth, health, relationship, career, education, legal, sleep, conflict, fertility, depression, debt, accident")
    building_type: BuildingType = BuildingType.residential
    entrance_direction: Optional[str] = None

    @field_validator("problems")
    @classmethod
    def validate_problems(cls, v: list[str]) -> list[str]:
        cleaned = [p.lower().strip() for p in v if p.strip()]
        invalid = [p for p in cleaned if p not in VALID_PROBLEMS]
        if invalid:
            raise ValueError(f"Invalid problem(s): {invalid}. Allowed: {sorted(VALID_PROBLEMS)}")
        return cleaned


class VastuAnalyzeRequest(BaseModel):
    building_type: BuildingType = BuildingType.residential
    entrance_direction: Optional[str] = None
    entrance_degrees: Optional[float] = Field(default=None, ge=0, lt=360)
    problems: Optional[list[str]] = None

    @field_validator("problems")
    @classmethod
    def validate_problems(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        cleaned = [p.lower().strip() for p in v if p.strip()]
        invalid = [p for p in cleaned if p not in VALID_PROBLEMS]
        if invalid:
            raise ValueError(f"Invalid problem(s): {invalid}. Allowed: {sorted(VALID_PROBLEMS)}")
        return cleaned


# ============================================================
# GET /api/vastu/mandala — Vastu Purusha Mandala (45 Devtas)
# ============================================================
@router.get("/api/vastu/mandala", status_code=status.HTTP_200_OK)
def vastu_mandala(
    building_type: BuildingType = Query(default=BuildingType.residential),
    entrance_direction: Optional[str] = Query(default=None, description="Direction code: N, NE, E, SE, S, SW, W, NW or pada like N3"),
    entrance_degrees: Optional[float] = Query(default=None, ge=0, lt=360, description="Precise compass degrees 0-360"),
):
    """
    Calculate Vastu Purusha Mandala with 45 Devtas analysis.
    Returns grid layout, zone-wise devtas, body mapping, and energy balance.
    """
    result = calculate_mandala(building_type.value, entrance_direction, entrance_degrees)
    return result


# ============================================================
# GET /api/vastu/entrance — 32 Entrance Padas Analysis
# ============================================================
@router.get("/api/vastu/entrance", status_code=status.HTTP_200_OK)
def vastu_entrance(
    direction: str = Query(description="Direction code: N, NE, E, SE, S, SW, W, NW or pada code like N3, E5"),
    degrees: Optional[float] = Query(default=None, ge=0, lt=360, description="Precise compass degrees 0-360"),
):
    """
    Analyze entrance direction against the ancient 32-pada system.
    Returns quality rating, effects, ruling devta, and remedies if needed.
    """
    result = analyze_entrance(direction, degrees)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )
    return result


# ============================================================
# POST /api/vastu/remedies — Remedy suggestions based on problems
# ============================================================
@router.post("/api/vastu/remedies", status_code=status.HTTP_200_OK)
def vastu_remedies(req: VastuRemediesRequest, user: dict = Depends(get_current_user)):
    """
    Suggest Vastu remedies based on reported problems. Requires authentication.
    """
    result = suggest_remedies(
        req.problems,
        req.building_type.value,
        req.entrance_direction,
    )
    return result


# ============================================================
# GET /api/vastu/room-placement — Room placement guide
# ============================================================
@router.get("/api/vastu/room-placement", status_code=status.HTTP_200_OK)
def vastu_room_placement(
    room_type: Optional[str] = Query(default=None, description="Room type: pooja, kitchen, master_bedroom, living_room, bathroom, staircase, water_tank_underground, water_tank_overhead, study_room, children_bedroom"),
):
    """
    Get Vastu-compliant room placement recommendations.
    Pass room_type for specific room, or omit for all rooms.
    """
    result = get_room_placement(room_type)
    return result


# ============================================================
# POST /api/vastu/analyze — Complete Vastu analysis
# ============================================================
@router.post("/api/vastu/analyze", status_code=status.HTTP_200_OK)
def vastu_full_analysis(req: VastuAnalyzeRequest, user: dict = Depends(get_current_user)):
    """
    Complete Vastu analysis — combines mandala, entrance, rooms, and remedies. Requires authentication.
    """
    result = get_complete_vastu_analysis(
        building_type=req.building_type.value,
        entrance_direction=req.entrance_direction,
        entrance_degrees=req.entrance_degrees,
        problems=req.problems,
    )
    return result
