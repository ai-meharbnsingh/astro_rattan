"""Yoga Search routes — search across kundli database for specific yoga combinations.

Pro astrologer research tool. All endpoints require authentication.
"""
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.database import get_db
from app.yoga_search_engine import (
    YOGA_TYPES,
    search_kundlis_for_yoga,
    get_yoga_statistics,
    get_kundli_yoga_profile,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/yoga-search", tags=["yoga-search"])


@router.get("/types", status_code=status.HTTP_200_OK)
def list_yoga_types():
    """Return all searchable yoga types.

    No auth required — informational endpoint so the frontend
    can populate a dropdown.
    """
    return {"yoga_types": YOGA_TYPES, "total": len(YOGA_TYPES)}


@router.get("", status_code=status.HTTP_200_OK)
def search_for_yoga(
    yoga: str = Query(..., min_length=2, description="Yoga name to search for (e.g. 'gajakesari', 'Ruchaka Yoga')"),
    limit: int = Query(50, ge=1, le=200, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Search all stored kundlis for a specific yoga.

    Scans every kundli owned by the authenticated user, runs canonical
    yoga detection from dosha_engine, and returns matching charts.

    **Pro-tier endpoint** — requires authentication.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = search_kundlis_for_yoga(db, yoga, user_id, limit=limit, offset=offset)

    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    return result


@router.get("/statistics", status_code=status.HTTP_200_OK)
def yoga_statistics(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get yoga prevalence statistics across all stored kundlis.

    Returns count and percentage for each detected yoga type,
    plus most-common and rarest lists.

    **Pro-tier endpoint** — requires authentication.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return get_yoga_statistics(db, user_id)


@router.get("/profile/{kundli_id}", status_code=status.HTTP_200_OK)
def kundli_yoga_profile(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get full yoga profile for a single kundli.

    Returns all detected yogas with descriptions and involved planets.
    Useful as a detail view after finding a match via search.

    **Pro-tier endpoint** — requires authentication.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = get_kundli_yoga_profile(db, kundli_id, user_id)

    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"],
        )

    return result
