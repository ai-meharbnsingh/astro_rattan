"""Numerology calculation routes."""
from fastapi import APIRouter, HTTPException, status
from app.models import NumerologyRequest, MobileNumerologyRequest
from app.numerology_engine import calculate_numerology, calculate_mobile_numerology

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
            detail="Invalid input — please check your data",
        )

    return result


@router.post("/api/numerology/mobile")
def mobile_numerology(req: MobileNumerologyRequest):
    """
    Calculate mobile number numerology: vibration number, prediction, qualities, challenges.
    No authentication required.
    """
    try:
        result = calculate_mobile_numerology(
            req.phone_number,
            name=req.name,
            birth_date=req.birth_date,
            areas_of_struggle=req.areas_of_struggle,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input — please check your data",
        )

    return result
