"""Tarot card drawing and interpretation routes."""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import decode_token
from app.models import TarotDrawRequest
from app.tarot_engine import draw_cards, interpret_spread

router = APIRouter()

_optional_bearer = HTTPBearer(auto_error=False)


@router.post("/api/tarot/draw")
def tarot_draw(
    req: TarotDrawRequest,
    credentials: HTTPAuthorizationCredentials = Depends(_optional_bearer),
):
    """
    Draw tarot cards for a given spread. JWT is optional.
    Contract response: {cards, interpretation}
    """
    user = None
    if credentials is not None:
        payload = decode_token(credentials.credentials)
        if payload is not None:
            user = payload

    cards = draw_cards(req.spread.value)
    interpretation = interpret_spread(cards, question=req.question)

    return {
        "cards": cards,
        "interpretation": interpretation,
    }
