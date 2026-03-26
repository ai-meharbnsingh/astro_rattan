"""Numerology calculation routes."""
from fastapi import APIRouter, HTTPException, status
from app.models import NumerologyRequest
from app.numerology_engine import calculate_numerology

router = APIRouter()


@router.post("/api/numerology/calculate")
def numerology_calculate(req: NumerologyRequest):
    """
    Calculate Pythagorean numerology: life path, expression, soul urge, personality.
    No authentication required.
    """
    try:
        result = calculate_numerology(req.name, req.birth_date)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return result
