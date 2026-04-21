import json
import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.database import get_db
from app.remedy_engine import generate_astrological_remedies

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kundli", tags=["remedies"])

@router.post("/remedies")
def get_astrological_remedies(payload: Dict[str, Any], user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Get comprehensive Vedic astrological remedies based on chart logic.
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
    year = payload.get("year")
    
    try:
        remedy_data = generate_astrological_remedies(chart_data, year=year)
        return remedy_data
    except Exception as e:
        logger.exception(f"Error in remedy engine: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate remedies at this time",
        )
