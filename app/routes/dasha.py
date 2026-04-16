"""Dasha routes — Ashtottari, Moola, and Tara dasha systems."""
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.models import AshtottariDashaRequest, MoolaDashaRequest, TaraDashaRequest
from app.ashtottari_dasha_engine import calculate_ashtottari_dasha
from app.moola_dasha_engine import calculate_moola_dasha
from app.tara_dasha_engine import calculate_tara_dasha

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dasha"])


# ─────────────────────────────────────────────────────────────
# Ashtottari Dasha (108-year system, 8 planets, no Ketu)
# ─────────────────────────────────────────────────────────────

@router.post("/api/kundli/dasha/ashtottari")
def ashtottari_dasha(
    body: AshtottariDashaRequest,
    user: dict = Depends(get_current_user),
):
    """
    Calculate Ashtottari Dasha periods from birth nakshatra.

    The Ashtottari system uses 8 planets (no Ketu) with a 108-year cycle.
    Applicable when birth nakshatra falls within the 22 nakshatras of the scheme.
    """
    try:
        result = calculate_ashtottari_dasha(
            birth_nakshatra=body.birth_nakshatra,
            birth_date=body.birth_date,
            moon_longitude=body.moon_longitude,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("Ashtottari dasha calculation error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


# ─────────────────────────────────────────────────────────────
# Moola (Jaimini) Dasha — sign-based rashi dasha
# ─────────────────────────────────────────────────────────────

@router.post("/api/kundli/dasha/moola")
def moola_dasha(
    body: MoolaDashaRequest,
    user: dict = Depends(get_current_user),
):
    """
    Calculate Moola (Jaimini) Dasha periods.

    Sign-based dasha system. Starting sign determined by comparing
    strength of Lagna and 7th house.
    """
    try:
        result = calculate_moola_dasha(
            lagna_sign=body.lagna_sign,
            seventh_sign=body.seventh_sign,
            planet_positions=body.planet_positions,
            birth_date=body.birth_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("Moola dasha calculation error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


# ─────────────────────────────────────────────────────────────
# Tara Dasha — nakshatra-based 9-group system (120 years)
# ─────────────────────────────────────────────────────────────

@router.post("/api/kundli/dasha/tara")
def tara_dasha(
    body: TaraDashaRequest,
    user: dict = Depends(get_current_user),
):
    """
    Calculate Tara Dasha periods from birth nakshatra.

    Divides 27 nakshatras into 9 Tara groups of 3, cycling from birth
    nakshatra. Total cycle = 120 years (same as Vimshottari).
    """
    try:
        result = calculate_tara_dasha(
            birth_nakshatra=body.birth_nakshatra,
            birth_date=body.birth_date,
            moon_longitude=body.moon_longitude,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("Tara dasha calculation error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result
