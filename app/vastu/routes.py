"""Vastu Shastra routes — mandala analysis, entrance padas, remedies, room placement."""
from typing import Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter

from app.auth import get_current_user
from app.rate_limit import request_rate_limit_key

limiter = Limiter(key_func=request_rate_limit_key)

from app.vastu.engine import (
    calculate_mandala,
    analyze_entrance,
    suggest_remedies,
    get_room_placement,
    get_complete_vastu_analysis,
    analyze_home_layout,
)
from app.vastu.data import ROOM_PLACEMENT

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
@limiter.limit("15/minute")
def vastu_remedies(request: Request, req: VastuRemediesRequest, user: dict = Depends(get_current_user)):
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
@limiter.limit("10/minute")
def vastu_full_analysis(request: Request, req: VastuAnalyzeRequest, user: dict = Depends(get_current_user)):
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


# ============================================================
# Home Layout models
# ============================================================
VALID_LAYOUT_DIRECTIONS = {"N", "NE", "E", "SE", "S", "SW", "W", "NW", "Center"}
VALID_ROOM_TYPES = set(ROOM_PLACEMENT.keys())


class HomeLayoutRequest(BaseModel):
    room_assignments: dict[str, list[str]] = Field(description="direction → list of room type keys")
    building_type: BuildingType = BuildingType.residential
    entrance_direction: Optional[str] = None

    @field_validator("room_assignments")
    @classmethod
    def validate_assignments(cls, v: dict) -> dict:
        if not v:
            raise ValueError("room_assignments must not be empty")
        total = 0
        for direction, rooms in v.items():
            if direction not in VALID_LAYOUT_DIRECTIONS:
                raise ValueError(f"Invalid direction: {direction}. Allowed: {sorted(VALID_LAYOUT_DIRECTIONS)}")
            if not isinstance(rooms, list) or len(rooms) == 0:
                raise ValueError(f"Each direction must have a non-empty list of rooms")
            if len(rooms) > 3:
                raise ValueError(f"Max 3 rooms per zone, got {len(rooms)} in {direction}")
            for room in rooms:
                if room not in VALID_ROOM_TYPES:
                    raise ValueError(f"Invalid room type: {room}. Allowed: {sorted(VALID_ROOM_TYPES)}")
            total += len(rooms)
        if total < 2:
            raise ValueError("Assign at least 2 rooms for a meaningful analysis")
        if total > 27:
            raise ValueError("Too many room assignments (max 27)")
        return v


# ============================================================
# POST /api/vastu/home-layout — Analyze user's home room layout
# ============================================================
@router.post("/api/vastu/home-layout", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def vastu_home_layout(request: Request, req: HomeLayoutRequest, user: dict = Depends(get_current_user)):
    """
    Analyze user's home room layout against Vastu principles.
    Input: room_assignments mapping directions to room types.
    Returns per-room compliance, devta-aware remedies, overall score.
    Requires authentication.
    """
    result = analyze_home_layout(
        room_assignments=req.room_assignments,
        building_type=req.building_type.value,
        entrance_direction=req.entrance_direction,
    )
    return result


# ============================================================
# Floor Plan Upload & Analysis
# ============================================================
from fastapi import File, UploadFile
from app.vastu.floorplan import (
    save_floorplan, map_room_placements, cleanup_old_uploads,
    ALLOWED_TYPES, MAX_FILE_SIZE,
)


@router.post("/api/vastu/upload-floorplan", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def upload_floorplan(
    request: Request,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    """
    Upload a floor plan image (PNG/JPG/WebP, max 5MB).
    Returns image_url for use in the floorplan mapper.
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{file.content_type}' not allowed. Use PNG, JPG, or WebP.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large ({len(contents)} bytes). Maximum is 5MB.",
        )

    try:
        result = save_floorplan(contents, file.content_type)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Opportunistic cleanup of old uploads (non-blocking)
    try:
        cleanup_old_uploads()
    except Exception:
        pass  # cleanup failure should not block upload

    return result


class FloorplanAnalysisRequest(BaseModel):
    image_url: str = Field(min_length=1)
    image_width: int = Field(gt=0)
    image_height: int = Field(gt=0)
    north_rotation: float = Field(default=0.0, ge=0, lt=360)
    room_markers: list[dict] = Field(min_length=2, description="List of {room_type, x, y}")
    building_type: BuildingType = BuildingType.residential
    entrance_direction: Optional[str] = None

    @field_validator("room_markers")
    @classmethod
    def validate_markers(cls, v: list[dict]) -> list[dict]:
        valid_rooms = set(ROOM_PLACEMENT.keys())
        for i, marker in enumerate(v):
            if "room_type" not in marker or "x" not in marker or "y" not in marker:
                raise ValueError(f"Marker {i} must have room_type, x, y fields")
            if marker["room_type"] not in valid_rooms:
                raise ValueError(f"Invalid room_type: {marker['room_type']}")
            if not isinstance(marker["x"], (int, float)) or not isinstance(marker["y"], (int, float)):
                raise ValueError(f"Marker {i}: x and y must be numbers")
        return v


@router.post("/api/vastu/analyze-floorplan", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def analyze_floorplan(
    request: Request,
    req: FloorplanAnalysisRequest,
    user: dict = Depends(get_current_user),
):
    """
    Analyze room placements on an uploaded floor plan.
    Converts pixel coordinates to Vastu directions, then runs full analysis.
    """
    # Convert pixel markers → direction-based assignments
    assignments = map_room_placements(
        room_markers=req.room_markers,
        image_width=req.image_width,
        image_height=req.image_height,
        north_rotation=req.north_rotation,
    )

    # Run existing home layout analysis
    result = analyze_home_layout(
        room_assignments=assignments,
        building_type=req.building_type.value,
        entrance_direction=req.entrance_direction,
    )

    # Add floorplan metadata to result
    result["floorplan"] = {
        "image_url": req.image_url,
        "image_width": req.image_width,
        "image_height": req.image_height,
        "north_rotation": req.north_rotation,
        "markers": req.room_markers,
        "direction_mapping": {
            f"{m['room_type']}@({m['x']},{m['y']})": assignments.get(
                next((d for d, rooms in assignments.items() if m["room_type"] in rooms), "?"), "?"
            )
            for m in req.room_markers
        },
    }

    return result
