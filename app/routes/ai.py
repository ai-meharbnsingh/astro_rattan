"""AI routes — kundli interpretation, Q&A, Gita wisdom, remedies, oracle."""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.database import get_db
from app.models import AIInterpretRequest, AIAskRequest, AIGitaRequest, AIOracleRequest
from app.ai_engine import ai_interpret_kundli, ai_ask_question, ai_gita_answer, ai_remedies, ai_oracle, get_active_model_label

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.get("/history", status_code=status.HTTP_200_OK)
def ai_chat_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the current user's AI chat history with pagination."""
    user_id = current_user["sub"]
    offset = (page - 1) * limit

    total = db.execute(
        "SELECT COUNT(*) as c FROM ai_chat_logs WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]

    rows = db.execute(
        """SELECT id, chat_type, kundli_id, user_message, ai_response, model_used, tokens_used, rating, created_at
           FROM ai_chat_logs WHERE user_id = %s
           ORDER BY created_at DESC LIMIT %s OFFSET %s""",
        (user_id, limit, offset),
    ).fetchall()

    return {"chats": [dict(r) for r in rows], "total": total}


@router.post("/interpret", status_code=status.HTTP_200_OK)
def interpret_kundli(
    body: AIInterpretRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """AI interpretation of a kundli chart. Contract input: {kundli_id}."""
    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (body.kundli_id, current_user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    result = ai_interpret_kundli(chart_data, prediction_type=body.prediction_type)

    # Log the AI interaction
    db.execute(
        """INSERT INTO ai_chat_logs (user_id, chat_type, kundli_id, user_message, ai_response, model_used)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            current_user["sub"],
            "kundli_interpretation",
            body.kundli_id,
            f"Interpret kundli {body.kundli_id}",
            result.get("interpretation", ""),
            get_active_model_label(),
        ),
    )
    db.commit()

    return result


@router.post("/ask", status_code=status.HTTP_200_OK)
def ask_question(
    body: AIAskRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Ask any astrology-related question, optionally with chart context."""
    chart_data = None
    if body.kundli_id:
        row = db.execute(
            "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
            (body.kundli_id, current_user["sub"]),
        ).fetchone()
        if row:
            chart_data = json.loads(row["chart_data"])

    result = ai_ask_question(body.question, chart_data)

    db.execute(
        """INSERT INTO ai_chat_logs (user_id, chat_type, kundli_id, user_message, ai_response, model_used)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            current_user["sub"],
            "ask_question",
            body.kundli_id,
            body.question,
            result.get("answer", ""),
            get_active_model_label(),
        ),
    )
    db.commit()

    return result


@router.post("/gita", status_code=status.HTTP_200_OK)
def gita_answer(body: AIGitaRequest):
    """Get Bhagavad Gita wisdom for a life question. No auth required."""
    return ai_gita_answer(body.question)


@router.post("/remedies", status_code=status.HTTP_200_OK)
def get_remedies(
    body: AIAskRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get personalized Vedic remedies based on kundli chart data."""
    if not body.kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required for remedies",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (body.kundli_id, current_user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    result = ai_remedies(chart_data)

    db.execute(
        """INSERT INTO ai_chat_logs (user_id, chat_type, kundli_id, user_message, ai_response, model_used)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            current_user["sub"],
            "remedies",
            body.kundli_id,
            body.question,
            json.dumps(result.get("remedies", []), default=str),
            get_active_model_label(),
        ),
    )
    db.commit()

    return result


@router.post("/oracle", status_code=status.HTTP_200_OK)
def oracle_answer(body: AIOracleRequest):
    """AI Oracle — yes/no or tarot mode answers. Auth optional per contract."""
    # Validate mode supports "yes_no" and "tarot" per contract
    valid_modes = ("yes_no", "tarot")
    mode = body.mode if body.mode in valid_modes else "yes_no"
    return ai_oracle(body.question, mode)
