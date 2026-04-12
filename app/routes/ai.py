"""AI interpretation routes for kundli predictions."""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.database import get_db
from app.horoscope_generator import generate_ai_horoscope

router = APIRouter(tags=["ai"])


def _normalize_period(raw: str) -> str:
    period = (raw or "").strip().lower()
    if period not in {"general", "daily", "monthly", "yearly"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="prediction_type must be one of: general, daily, monthly, yearly",
        )
    return "daily" if period == "general" else period


def _compose_interpretation(sections: dict[str, str]) -> str:
    lines = []
    for title, key in (
        ("General", "general"),
        ("Love", "love"),
        ("Career", "career"),
        ("Finance", "finance"),
        ("Health", "health"),
    ):
        val = (sections.get(key) or "").strip()
        if not val:
            continue
        lines.append(f"## {title}\n{val}")
    return "\n\n".join(lines).strip()


@router.post("/api/ai/interpret", status_code=status.HTTP_200_OK)
def ai_interpret(
    payload: dict,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return AI-style period prediction for a saved kundli."""
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id is required")

    period = _normalize_period(str(payload.get("prediction_type", "general")))

    row = db.execute(
        """SELECT id, person_name, birth_date, birth_time, birth_place, chart_data
           FROM kundlis WHERE id = %s AND user_id = %s""",
        (kundli_id, current_user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = row.get("chart_data") or {}
    if isinstance(chart_data, str):
        try:
            chart_data = json.loads(chart_data)
        except json.JSONDecodeError:
            chart_data = {}

    moon_sign = (
        chart_data.get("planets", {}).get("Moon", {}).get("sign")
        if isinstance(chart_data.get("planets"), dict)
        else None
    )
    if not moon_sign:
        moon_sign = chart_data.get("ascendant", {}).get("sign")
    sign = str(moon_sign or "Aries").strip().lower()

    generated = generate_ai_horoscope(
        sign=sign,
        period=period,
        birth_data={
            "birth_date": row.get("birth_date"),
            "birth_time": row.get("birth_time"),
            "birth_place": row.get("birth_place"),
        },
    )
    sections = generated.get("sections", {}) if isinstance(generated, dict) else {}
    interpretation = _compose_interpretation(sections if isinstance(sections, dict) else {})

    return {
        "kundli_id": kundli_id,
        "prediction_type": payload.get("prediction_type", "general"),
        "source": generated.get("source", "template") if isinstance(generated, dict) else "template",
        "sign": generated.get("sign", sign) if isinstance(generated, dict) else sign,
        "interpretation": interpretation,
        "sections": sections,
    }

