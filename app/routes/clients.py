"""Client management routes — astrologers manage their clients' profiles."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional

from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/clients", tags=["clients"])


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_offset: Optional[float] = 5.5
    gender: Optional[str] = "male"
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_offset: Optional[float] = None
    gender: Optional[str] = None
    notes: Optional[str] = None


@router.get("")
def list_clients(
    search: str = Query(default="", max_length=100),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all clients for the logged-in astrologer, with optional name search."""
    if search:
        rows = db.execute(
            """SELECT c.*,
                      (SELECT COUNT(*) FROM kundlis k WHERE k.client_id = c.id) as kundli_count
               FROM clients c
               WHERE c.astrologer_id = %s AND c.name ILIKE %s
               ORDER BY c.updated_at DESC""",
            (current_user["sub"], f"%{search}%"),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT c.*,
                      (SELECT COUNT(*) FROM kundlis k WHERE k.client_id = c.id) as kundli_count
               FROM clients c
               WHERE c.astrologer_id = %s
               ORDER BY c.updated_at DESC""",
            (current_user["sub"],),
        ).fetchall()
    return [dict(r) for r in rows]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_client(
    body: ClientCreate,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Create a new client profile."""
    row = db.execute(
        """INSERT INTO clients
           (astrologer_id, name, phone, birth_date, birth_time, birth_place,
            latitude, longitude, timezone_offset, gender, notes)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           RETURNING *""",
        (
            current_user["sub"], body.name, body.phone, body.birth_date,
            body.birth_time, body.birth_place, body.latitude, body.longitude,
            body.timezone_offset, body.gender, body.notes,
        ),
    ).fetchone()
    db.commit()
    return dict(row)


@router.get("/{client_id}")
def get_client(
    client_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get client profile with all their kundlis."""
    client = db.execute(
        "SELECT * FROM clients WHERE id = %s AND astrologer_id = %s",
        (client_id, current_user["sub"]),
    ).fetchone()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    kundlis = db.execute(
        """SELECT id, person_name, birth_date, birth_time, birth_place, chart_type, created_at
           FROM kundlis WHERE client_id = %s ORDER BY created_at DESC""",
        (client_id,),
    ).fetchall()

    return {"client": dict(client), "kundlis": [dict(k) for k in kundlis]}


@router.patch("/{client_id}")
def update_client(
    client_id: str,
    body: ClientUpdate,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Update client profile."""
    existing = db.execute(
        "SELECT id FROM clients WHERE id = %s AND astrologer_id = %s",
        (client_id, current_user["sub"]),
    ).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Client not found")

    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [client_id, current_user["sub"]]
    db.execute(
        f"UPDATE clients SET {set_clause}, updated_at = NOW() WHERE id = %s AND astrologer_id = %s",
        values,
    )
    db.commit()
    return {"message": "Client updated"}


# ── Notes ────────────────────────────────────────────────────

class NoteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    chart_type: str = "general"
    kundli_id: Optional[str] = None


@router.get("/{client_id}/notes")
def list_notes(
    client_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all notes for a client, newest first."""
    # Verify client belongs to this astrologer
    client = db.execute(
        "SELECT id FROM clients WHERE id = %s AND astrologer_id = %s",
        (client_id, current_user["sub"]),
    ).fetchone()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    rows = db.execute(
        "SELECT id, content, chart_type, kundli_id, created_at FROM notes WHERE client_id = %s AND astrologer_id = %s ORDER BY created_at DESC",
        (client_id, current_user["sub"]),
    ).fetchall()
    return [dict(r) for r in rows]


@router.post("/{client_id}/notes", status_code=201)
def add_note(
    client_id: str,
    body: NoteCreate,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Add a note for a client."""
    client = db.execute(
        "SELECT id FROM clients WHERE id = %s AND astrologer_id = %s",
        (client_id, current_user["sub"]),
    ).fetchone()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    row = db.execute(
        """INSERT INTO notes (astrologer_id, client_id, kundli_id, chart_type, content)
           VALUES (%s, %s, %s, %s, %s) RETURNING *""",
        (current_user["sub"], client_id, body.kundli_id, body.chart_type, body.content),
    ).fetchone()
    db.commit()
    return dict(row)
