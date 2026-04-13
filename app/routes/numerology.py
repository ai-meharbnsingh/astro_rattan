"""Numerology calculation routes."""
from fastapi import APIRouter, HTTPException, status
from app.models import NumerologyRequest, MobileNumerologyRequest
from app.numerology_engine import (
    calculate_numerology, 
    calculate_mobile_numerology,
    analyze_name_numerology,
    calculate_vehicle_numerology,
    calculate_house_numerology
)

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


@router.post("/api/numerology/name")
def name_numerology(req: dict):
    """
    Comprehensive Name Numerology Analysis
    
    Args:
        full_name: The name to analyze
        birth_date: Optional DOB for compatibility (YYYY-MM-DD)
        name_type: 'first_name', 'last_name', 'full_name', or 'business_name'
    
    Returns:
        Detailed name analysis with Pythagorean and Chaldean calculations
    """
    try:
        full_name = req.get("full_name", "")
        birth_date = req.get("birth_date", "")
        name_type = req.get("name_type", "full_name")
        
        result = analyze_name_numerology(
            full_name=full_name,
            birth_date=birth_date,
            name_type=name_type
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return result


@router.post("/api/numerology/vehicle")
def vehicle_numerology(req: dict):
    """
    Vehicle/Car Number Plate Numerology Analysis
    
    Args:
        vehicle_number: Vehicle registration number (e.g., "MH 01 AB 1234")
        owner_name: Optional owner's name
        birth_date: Optional owner's DOB (YYYY-MM-DD) for compatibility
    
    Returns:
        Vehicle numerology analysis with driving style, lucky colors, compatibility
    """
    try:
        vehicle_number = req.get("vehicle_number", "")
        owner_name = req.get("owner_name", "")
        birth_date = req.get("birth_date", "")
        
        result = calculate_vehicle_numerology(
            vehicle_number=vehicle_number,
            owner_name=owner_name,
            birth_date=birth_date
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return result


@router.post("/api/numerology/house")
def house_numerology(req: dict):
    """
    House/Property Address Numerology Analysis
    
    Args:
        address: Full address (e.g., "123 Main Street, Apt 4B")
        birth_date: Optional resident's DOB (YYYY-MM-DD) for compatibility
    
    Returns:
        House numerology analysis with energy prediction, Vastu tips, remedies
    """
    try:
        address = req.get("address", "")
        birth_date = req.get("birth_date", "")
        
        result = calculate_house_numerology(
            address=address,
            birth_date=birth_date
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return result
