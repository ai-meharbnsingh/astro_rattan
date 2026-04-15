"""Numerology calculation routes."""
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.models import NumerologyRequest, MobileNumerologyRequest
from app.numerology_engine import (
    calculate_numerology,
    calculate_mobile_numerology,
    analyze_name_numerology,
    calculate_vehicle_numerology,
    calculate_house_numerology
)

router = APIRouter()


class NameNumerologyRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    birth_date: Optional[str] = Field(default="", max_length=20)
    name_type: str = Field(default="full_name", max_length=20)


class VehicleNumerologyRequest(BaseModel):
    vehicle_number: str = Field(min_length=1, max_length=30)
    owner_name: Optional[str] = Field(default="", max_length=200)
    birth_date: Optional[str] = Field(default="", max_length=20)


class HouseNumerologyRequest(BaseModel):
    address: str = Field(min_length=1, max_length=500)
    birth_date: Optional[str] = Field(default="", max_length=20)


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


@router.post("/api/numerology/name")
def name_numerology(req: NameNumerologyRequest):
    """Comprehensive Name Numerology Analysis (Pythagorean + Chaldean)."""
    try:
        result = analyze_name_numerology(
            full_name=req.full_name,
            birth_date=req.birth_date,
            name_type=req.name_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return result


@router.post("/api/numerology/vehicle")
def vehicle_numerology(req: VehicleNumerologyRequest):
    """Vehicle/Car Number Plate Numerology Analysis."""
    try:
        result = calculate_vehicle_numerology(
            vehicle_number=req.vehicle_number,
            owner_name=req.owner_name,
            birth_date=req.birth_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return result


@router.post("/api/numerology/house")
def house_numerology(req: HouseNumerologyRequest):
    """House/Property Address Numerology Analysis."""
    try:
        result = calculate_house_numerology(
            address=req.address,
            birth_date=req.birth_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return result
