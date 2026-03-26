"""Prashnavali routes — Ram Shalaka, Hanuman, Ramcharitmanas, Gita oracle."""
from fastapi import APIRouter, status

from app.models import RamShalakaRequest, PrashnavaliRequest
from app.prashnavali_engine import ram_shalaka, hanuman_prashna, ramcharitmanas_prashna, gita_prashna

router = APIRouter(prefix="/api/prashnavali", tags=["prashnavali"])


@router.post("/ram-shalaka", status_code=status.HTTP_200_OK)
def do_ram_shalaka(body: RamShalakaRequest):
    """Ram Shalaka Prashnavali — pick a cell from the 15x15 grid."""
    # API uses 1-based row/col, engine uses 0-based
    return ram_shalaka(body.row - 1, body.col - 1)


@router.post("/hanuman", status_code=status.HTTP_200_OK)
def do_hanuman_prashna(body: PrashnavaliRequest):
    """Hanuman Prashna — answer via Hanuman Chalisa chaupais."""
    return hanuman_prashna(body.question)


@router.post("/ramcharitmanas", status_code=status.HTTP_200_OK)
def do_ramcharitmanas_prashna(body: PrashnavaliRequest):
    """Ramcharitmanas Prashna — answer using Tulsidas verses."""
    return ramcharitmanas_prashna(body.question)


@router.post("/gita", status_code=status.HTTP_200_OK)
def do_gita_prashna(body: PrashnavaliRequest):
    """Gita Prashna — answer using Bhagavad Gita slokas."""
    return gita_prashna(body.question)
