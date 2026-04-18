"""
Astrologer Dashboard routes — P3.5 Professional client management.

Aggregates metrics + activity + consultation lifecycle across the
pre-existing `clients` / `notes` / `consultations` / `kundlis` tables so
the frontend can render a single professional CRM-style dashboard
without N+1 round-trips.

Endpoints (all require role == 'astrologer' or 'admin'):

  GET  /api/astrologer/dashboard                  → overview metrics
  GET  /api/astrologer/activity-feed              → recent events across clients
  GET  /api/astrologer/consultations              → scheduled consultations
  POST /api/astrologer/consultations              → create a consultation
  PATCH /api/astrologer/consultations/{id}        → update status / notes
  DELETE /api/astrologer/consultations/{id}       → cancel
  GET  /api/astrologer/client-timeline/{id}       → unified per-client timeline
"""
from __future__ import annotations

from datetime import datetime, timedelta, date as _date
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/astrologer", tags=["astrologer"])


def _require_astrologer(user: dict) -> None:
    """Gate these endpoints to verified astrologers (admin allowed too)."""
    role = user.get("role")
    if role not in ("astrologer", "admin"):
        raise HTTPException(
            status_code=403,
            detail="Astrologer role required",
        )


# ══════════════════════════════════════════════════════════════════
# GET /api/astrologer/dashboard — overview metrics
# ══════════════════════════════════════════════════════════════════

@router.get("/dashboard")
def get_dashboard_overview(
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Aggregated overview for the main dashboard hero.

    Returns counts + deltas so the frontend can render summary cards
    without a dozen separate requests.
    """
    _require_astrologer(user)
    astrologer_id = user["sub"]

    # ── client counts ──
    total_clients_row = db.execute(
        "SELECT COUNT(*) AS n FROM clients WHERE astrologer_id = %s",
        (astrologer_id,),
    ).fetchone()
    total_clients = int(total_clients_row["n"]) if total_clients_row else 0

    # Clients added in the last 30 / 7 days
    new_clients_30 = db.execute(
        "SELECT COUNT(*) AS n FROM clients WHERE astrologer_id = %s "
        "AND created_at >= NOW() - INTERVAL '30 days'",
        (astrologer_id,),
    ).fetchone()
    new_clients_7 = db.execute(
        "SELECT COUNT(*) AS n FROM clients WHERE astrologer_id = %s "
        "AND created_at >= NOW() - INTERVAL '7 days'",
        (astrologer_id,),
    ).fetchone()

    # ── kundli counts (charts generated for clients) ──
    # Scope to kundlis whose client_id belongs to this astrologer.
    total_kundlis_row = db.execute(
        """
        SELECT COUNT(*) AS n
        FROM kundlis k
        JOIN clients c ON k.client_id = c.id
        WHERE c.astrologer_id = %s
        """,
        (astrologer_id,),
    ).fetchone()
    total_kundlis = int(total_kundlis_row["n"]) if total_kundlis_row else 0

    # Chart-type breakdown
    chart_types_rows = db.execute(
        """
        SELECT k.chart_type, COUNT(*) AS n
        FROM kundlis k
        JOIN clients c ON k.client_id = c.id
        WHERE c.astrologer_id = %s
        GROUP BY k.chart_type
        ORDER BY n DESC
        """,
        (astrologer_id,),
    ).fetchall()

    # ── notes count ──
    total_notes_row = db.execute(
        "SELECT COUNT(*) AS n FROM notes WHERE astrologer_id = %s",
        (astrologer_id,),
    ).fetchone()

    # ── consultations lifecycle ──
    # `consultations` table's `astrologer_id` FK points to the astrologers
    # table (which keys on user_id). For simplicity we join on the user_id
    # column since every astrologer has an `astrologers` row.
    cons_rows = db.execute(
        """
        SELECT status, COUNT(*) AS n
        FROM consultations
        WHERE astrologer_id = %s
        GROUP BY status
        """,
        (astrologer_id,),
    ).fetchall()
    cons_by_status = {r["status"]: int(r["n"]) for r in (cons_rows or [])}

    # Upcoming consultations (scheduled_at in the future)
    upcoming_row = db.execute(
        """
        SELECT COUNT(*) AS n
        FROM consultations
        WHERE astrologer_id = %s
          AND scheduled_at IS NOT NULL
          AND scheduled_at >= NOW()
          AND status IN ('scheduled', 'confirmed')
        """,
        (astrologer_id,),
    ).fetchone()

    # Top 5 most-active clients (by kundli + note count)
    top_clients_rows = db.execute(
        """
        SELECT c.id, c.name, c.phone,
               COUNT(DISTINCT k.id) AS kundli_count,
               COUNT(DISTINCT n.id) AS note_count,
               MAX(GREATEST(
                 COALESCE(k.created_at, 'epoch'::timestamptz),
                 COALESCE(n.created_at, 'epoch'::timestamptz),
                 c.created_at
               )) AS last_activity
        FROM clients c
        LEFT JOIN kundlis k ON k.client_id = c.id
        LEFT JOIN notes n ON n.client_id = c.id
        WHERE c.astrologer_id = %s
        GROUP BY c.id, c.name, c.phone
        ORDER BY last_activity DESC NULLS LAST
        LIMIT 5
        """,
        (astrologer_id,),
    ).fetchall()

    return {
        "metrics": {
            "total_clients": total_clients,
            "new_clients_30d": int(new_clients_30["n"]) if new_clients_30 else 0,
            "new_clients_7d": int(new_clients_7["n"]) if new_clients_7 else 0,
            "total_kundlis": total_kundlis,
            "total_notes": int(total_notes_row["n"]) if total_notes_row else 0,
            "upcoming_consultations": int(upcoming_row["n"]) if upcoming_row else 0,
            "consultations_by_status": cons_by_status,
        },
        "chart_types": [
            {"chart_type": r["chart_type"], "count": int(r["n"])}
            for r in (chart_types_rows or [])
        ],
        "top_clients": [
            {
                "id": r["id"],
                "name": r["name"],
                "phone": r.get("phone"),
                "kundli_count": int(r["kundli_count"] or 0),
                "note_count": int(r["note_count"] or 0),
                "last_activity": r["last_activity"].isoformat() if r.get("last_activity") else None,
            }
            for r in (top_clients_rows or [])
        ],
    }


# ══════════════════════════════════════════════════════════════════
# GET /api/astrologer/activity-feed — recent events across all clients
# ══════════════════════════════════════════════════════════════════

@router.get("/activity-feed")
def activity_feed(
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Unified activity stream merging kundli generations + notes +
    consultation events across all of this astrologer's clients.

    Each row carries a `kind` discriminator so the frontend can render
    different icons / colours per event type.
    """
    _require_astrologer(user)
    astrologer_id = user["sub"]

    events: list[dict] = []

    # Kundlis (chart generations)
    kundli_rows = db.execute(
        """
        SELECT k.id, k.person_name, k.chart_type, k.created_at,
               c.id AS client_id, c.name AS client_name
        FROM kundlis k
        JOIN clients c ON k.client_id = c.id
        WHERE c.astrologer_id = %s
        ORDER BY k.created_at DESC
        LIMIT %s
        """,
        (astrologer_id, limit),
    ).fetchall()
    for r in (kundli_rows or []):
        events.append({
            "kind": "kundli_generated",
            "timestamp": r["created_at"].isoformat() if r.get("created_at") else None,
            "client_id": r["client_id"],
            "client_name": r["client_name"],
            "title_en": f"Generated {r['chart_type']} chart",
            "title_hi": f"{r['chart_type']} कुंडली बनाई",
            "detail": r.get("person_name"),
            "ref_id": r["id"],
            "ref_type": "kundli",
        })

    # Notes
    note_rows = db.execute(
        """
        SELECT n.id, n.content, n.chart_type, n.created_at,
               c.id AS client_id, c.name AS client_name
        FROM notes n
        JOIN clients c ON n.client_id = c.id
        WHERE n.astrologer_id = %s
        ORDER BY n.created_at DESC
        LIMIT %s
        """,
        (astrologer_id, limit),
    ).fetchall()
    for r in (note_rows or []):
        content = r.get("content") or ""
        events.append({
            "kind": "note_added",
            "timestamp": r["created_at"].isoformat() if r.get("created_at") else None,
            "client_id": r["client_id"],
            "client_name": r["client_name"],
            "title_en": "Added note",
            "title_hi": "नोट जोड़ा",
            "detail": (content[:120] + "…") if len(content) > 120 else content,
            "ref_id": r["id"],
            "ref_type": "note",
            "chart_context": r.get("chart_type"),
        })

    # Consultations
    cons_rows = db.execute(
        """
        SELECT co.id, co.status, co.type, co.scheduled_at, co.created_at, co.updated_at,
               co.user_id AS consultation_client_uid,
               cl.id AS client_id, cl.name AS client_name
        FROM consultations co
        LEFT JOIN clients cl ON co.client_id = cl.id
        WHERE co.astrologer_id = %s
        ORDER BY co.updated_at DESC
        LIMIT %s
        """,
        (astrologer_id, limit),
    ).fetchall()
    for r in (cons_rows or []):
        ts = r.get("updated_at") or r.get("created_at")
        events.append({
            "kind": "consultation",
            "timestamp": ts.isoformat() if ts else None,
            "client_id": r.get("client_id"),
            "client_name": r.get("client_name"),
            "title_en": f"Consultation {r['status']} ({r['type']})",
            "title_hi": f"परामर्श {r['status']} ({r['type']})",
            "detail": r["scheduled_at"].isoformat() if r.get("scheduled_at") else None,
            "ref_id": r["id"],
            "ref_type": "consultation",
            "status": r.get("status"),
        })

    # Merge + sort + truncate
    events.sort(key=lambda e: e.get("timestamp") or "", reverse=True)
    return {"events": events[:limit], "total": len(events)}


# ══════════════════════════════════════════════════════════════════
# Consultation CRUD — POST / GET / PATCH / DELETE
# ══════════════════════════════════════════════════════════════════

class ConsultationCreate(BaseModel):
    client_id: Optional[str] = None       # astrologer's client (preferred)
    user_id: Optional[str] = None         # alternatively a platform user
    type: str = Field(default="chat")     # chat | audio | video | in-person
    status: str = Field(default="scheduled")
    scheduled_at: Optional[str] = None    # ISO-8601
    duration_minutes: Optional[int] = Field(default=30, ge=5, le=480)
    notes: Optional[str] = None


class ConsultationUpdate(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[str] = None
    duration_minutes: Optional[int] = Field(default=None, ge=5, le=480)
    notes: Optional[str] = None


_VALID_STATUSES = {"scheduled", "confirmed", "active", "completed", "cancelled", "no_show"}
_VALID_TYPES = {"chat", "audio", "video", "in_person"}


@router.post("/consultations", status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    _require_astrologer(user)
    if payload.type not in _VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"type must be one of {sorted(_VALID_TYPES)}")
    if payload.status not in _VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {sorted(_VALID_STATUSES)}")
    if not payload.client_id and not payload.user_id:
        raise HTTPException(status_code=400, detail="client_id or user_id required")

    # If client_id supplied, validate it belongs to this astrologer.
    if payload.client_id:
        row = db.execute(
            "SELECT id FROM clients WHERE id = %s AND astrologer_id = %s",
            (payload.client_id, user["sub"]),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Client not found under this astrologer")

    cur = db.execute(
        """
        INSERT INTO consultations
          (user_id, astrologer_id, client_id, type, status, scheduled_at, duration_minutes, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, created_at
        """,
        (
            payload.user_id or user["sub"],
            user["sub"],
            payload.client_id,
            payload.type,
            payload.status,
            payload.scheduled_at,
            payload.duration_minutes,
            payload.notes,
        ),
    )
    row = cur.fetchone()
    db.commit()
    return {
        "id": row["id"],
        "created_at": row["created_at"].isoformat() if row.get("created_at") else None,
    }


@router.get("/consultations")
def list_consultations(
    status_filter: Optional[str] = Query(None, alias="status"),
    client_id: Optional[str] = None,
    upcoming_only: bool = False,
    limit: int = Query(100, ge=1, le=500),
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    _require_astrologer(user)
    sql = """
        SELECT co.*, cl.name AS client_name, cl.phone AS client_phone
        FROM consultations co
        LEFT JOIN clients cl ON co.client_id = cl.id
        WHERE co.astrologer_id = %s
    """
    params: list[Any] = [user["sub"]]
    if status_filter:
        sql += " AND co.status = %s"
        params.append(status_filter)
    if client_id:
        sql += " AND co.client_id = %s"
        params.append(client_id)
    if upcoming_only:
        sql += " AND co.scheduled_at IS NOT NULL AND co.scheduled_at >= NOW()"
    sql += " ORDER BY co.scheduled_at NULLS LAST, co.created_at DESC LIMIT %s"
    params.append(limit)

    try:
        rows = db.execute(sql, tuple(params)).fetchall()
    except Exception:
        rows = []
    return {
        "consultations": [
            {
                **{k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in dict(r).items()},
            }
            for r in (rows or [])
        ]
    }


@router.patch("/consultations/{consultation_id}")
def update_consultation(
    consultation_id: str,
    payload: ConsultationUpdate,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    _require_astrologer(user)
    row = db.execute(
        "SELECT id FROM consultations WHERE id = %s AND astrologer_id = %s",
        (consultation_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Consultation not found")

    fields = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else payload.dict(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    if "status" in fields and fields["status"] not in _VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {sorted(_VALID_STATUSES)}")
    if "type" in fields and fields["type"] not in _VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"type must be one of {sorted(_VALID_TYPES)}")

    set_clauses = []
    params: list[Any] = []
    for key, val in fields.items():
        set_clauses.append(f"{key} = %s")
        params.append(val)
    set_clauses.append("updated_at = NOW()")
    params.append(consultation_id)

    db.execute(
        f"UPDATE consultations SET {', '.join(set_clauses)} WHERE id = %s",
        tuple(params),
    )
    db.commit()
    return {"ok": True}


@router.delete("/consultations/{consultation_id}")
def delete_consultation(
    consultation_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    _require_astrologer(user)
    row = db.execute(
        "SELECT id FROM consultations WHERE id = %s AND astrologer_id = %s",
        (consultation_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Consultation not found")
    db.execute("DELETE FROM consultations WHERE id = %s", (consultation_id,))
    db.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════
# GET /api/astrologer/client-timeline/{client_id}
# Unified per-client timeline (notes + kundlis + consultations merged)
# ══════════════════════════════════════════════════════════════════

@router.get("/client-timeline/{client_id}")
def client_timeline(
    client_id: str,
    limit: int = Query(100, ge=1, le=500),
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    _require_astrologer(user)
    # Validate ownership.
    owner = db.execute(
        "SELECT name, phone, birth_date FROM clients WHERE id = %s AND astrologer_id = %s",
        (client_id, user["sub"]),
    ).fetchone()
    if not owner:
        raise HTTPException(status_code=404, detail="Client not found under this astrologer")

    events: list[dict] = []

    # Notes for this client
    for n in (db.execute(
        "SELECT id, content, chart_type, kundli_id, created_at FROM notes "
        "WHERE client_id = %s AND astrologer_id = %s ORDER BY created_at DESC LIMIT %s",
        (client_id, user["sub"], limit),
    ).fetchall() or []):
        events.append({
            "kind": "note",
            "timestamp": n["created_at"].isoformat() if n.get("created_at") else None,
            "content": n.get("content"),
            "chart_type": n.get("chart_type"),
            "ref_id": n["id"],
        })

    # Kundlis for this client
    for k in (db.execute(
        "SELECT id, person_name, chart_type, created_at FROM kundlis "
        "WHERE client_id = %s ORDER BY created_at DESC LIMIT %s",
        (client_id, limit),
    ).fetchall() or []):
        events.append({
            "kind": "kundli",
            "timestamp": k["created_at"].isoformat() if k.get("created_at") else None,
            "person_name": k.get("person_name"),
            "chart_type": k.get("chart_type"),
            "ref_id": k["id"],
        })

    # Consultations for this client
    for c in (db.execute(
        "SELECT id, type, status, scheduled_at, duration_minutes, notes, created_at "
        "FROM consultations WHERE client_id = %s AND astrologer_id = %s "
        "ORDER BY scheduled_at DESC NULLS LAST, created_at DESC LIMIT %s",
        (client_id, user["sub"], limit),
    ).fetchall() or []):
        events.append({
            "kind": "consultation",
            "timestamp": (c["scheduled_at"] or c["created_at"]).isoformat() if (c.get("scheduled_at") or c.get("created_at")) else None,
            "type": c.get("type"),
            "status": c.get("status"),
            "scheduled_at": c["scheduled_at"].isoformat() if c.get("scheduled_at") else None,
            "duration_minutes": c.get("duration_minutes"),
            "notes": c.get("notes"),
            "ref_id": c["id"],
        })

    events.sort(key=lambda e: e.get("timestamp") or "", reverse=True)
    return {
        "client": {"id": client_id, "name": owner["name"], "phone": owner.get("phone"), "birth_date": owner.get("birth_date")},
        "events": events[:limit],
        "total": len(events),
    }
