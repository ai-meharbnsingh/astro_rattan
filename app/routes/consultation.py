"""Consultation booking and astrologer listing routes."""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from app.auth import get_current_user, require_role
from app.database import get_db
from app.models import ConsultationBookRequest

router = APIRouter()


# ============================================================
# Public — Astrologer listings
# ============================================================

@router.get("/api/astrologers")
def list_astrologers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all approved and available astrologers. No auth required."""
    offset = (page - 1) * limit

    count_row = db.execute(
        "SELECT COUNT(*) as total FROM astrologers WHERE is_approved = 1",
    ).fetchone()

    rows = db.execute(
        """
        SELECT a.id, a.user_id, a.display_name, a.bio, a.specializations,
               a.experience_years, a.per_minute_rate, a.languages,
               a.rating, a.total_consultations, a.is_available
        FROM astrologers a
        WHERE a.is_approved = 1
        ORDER BY a.rating DESC, a.total_consultations DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    ).fetchall()

    return [dict(row) for row in rows]


@router.get("/api/astrologers/{astrologer_id}")
def get_astrologer(astrologer_id: str, db: sqlite3.Connection = Depends(get_db)):
    """Get a single astrologer profile. No auth required."""
    row = db.execute(
        """
        SELECT a.id, a.user_id, a.display_name, a.bio, a.specializations,
               a.experience_years, a.per_minute_rate, a.languages,
               a.rating, a.total_consultations, a.is_available
        FROM astrologers a
        WHERE a.id = ? AND a.is_approved = 1
        """,
        (astrologer_id,),
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astrologer not found"
        )

    return dict(row)


# ============================================================
# User — Booking and listing consultations
# ============================================================

@router.post("/api/consultations/book", status_code=status.HTTP_201_CREATED)
def book_consultation(
    req: ConsultationBookRequest,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Book a consultation with an astrologer. Requires JWT."""
    user_id = user.get("sub")

    # Verify astrologer exists, is approved and available
    astrologer = db.execute(
        "SELECT id, is_available, is_approved FROM astrologers WHERE id = ?",
        (req.astrologer_id,),
    ).fetchone()

    if astrologer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astrologer not found"
        )

    if not astrologer["is_approved"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Astrologer is not approved"
        )

    if not astrologer["is_available"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Astrologer is currently unavailable"
        )

    cursor = db.execute(
        """
        INSERT INTO consultations (user_id, astrologer_id, type, scheduled_at)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, req.astrologer_id, req.type.value, req.scheduled_at),
    )
    rowid = cursor.lastrowid
    consultation = db.execute(
        "SELECT id FROM consultations WHERE rowid = ?", (rowid,)
    ).fetchone()
    db.commit()

    # Return full consultation record per contract: {consultation}
    full = db.execute(
        "SELECT * FROM consultations WHERE id = ?", (consultation["id"],)
    ).fetchone()
    return dict(full)


@router.get("/api/consultations")
def list_consultations(
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List the current user's consultations. Requires JWT."""
    user_id = user.get("sub")

    rows = db.execute(
        """
        SELECT c.*,
               CASE
                   WHEN c.notes LIKE 'https://meet.jit.si/%' THEN c.notes
                   ELSE NULL
               END as video_link,
               a.display_name as astrologer_name
        FROM consultations c
        JOIN astrologers a ON a.id = c.astrologer_id
        WHERE c.user_id = ?
        ORDER BY c.created_at DESC
        """,
        (user_id,),
    ).fetchall()

    return [dict(row) for row in rows]


# ============================================================
# Astrologer — Accept and complete consultations
# ============================================================

@router.patch("/api/consultations/{consultation_id}/accept")
def accept_consultation(
    consultation_id: str,
    user: dict = Depends(require_role("astrologer")),
    db: sqlite3.Connection = Depends(get_db),
):
    """Astrologer accepts a consultation request."""
    user_id = user.get("sub")

    # Find the astrologer record for this user
    astrologer = db.execute(
        "SELECT id FROM astrologers WHERE user_id = ?", (user_id,)
    ).fetchone()

    if astrologer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Astrologer profile not found"
        )

    consultation = db.execute(
        "SELECT id, status, astrologer_id FROM consultations WHERE id = ?",
        (consultation_id,),
    ).fetchone()

    if consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Consultation not found"
        )

    if consultation["astrologer_id"] != astrologer["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your consultation"
        )

    if consultation["status"] != "requested":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot accept consultation in '{consultation['status']}' status",
        )

    db.execute(
        "UPDATE consultations SET status = 'accepted' WHERE id = ?",
        (consultation_id,),
    )
    db.commit()

    # Return updated consultation per contract: {consultation}
    updated = db.execute(
        "SELECT * FROM consultations WHERE id = ?", (consultation_id,)
    ).fetchone()
    return dict(updated)


@router.patch("/api/consultations/{consultation_id}/complete")
def complete_consultation(
    consultation_id: str,
    user: dict = Depends(require_role("astrologer")),
    db: sqlite3.Connection = Depends(get_db),
):
    """Astrologer marks a consultation as completed."""
    user_id = user.get("sub")

    astrologer = db.execute(
        "SELECT id FROM astrologers WHERE user_id = ?", (user_id,)
    ).fetchone()

    if astrologer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Astrologer profile not found"
        )

    consultation = db.execute(
        "SELECT id, status, astrologer_id FROM consultations WHERE id = ?",
        (consultation_id,),
    ).fetchone()

    if consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Consultation not found"
        )

    if consultation["astrologer_id"] != astrologer["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your consultation"
        )

    if consultation["status"] not in ("accepted", "active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot complete consultation in '{consultation['status']}' status",
        )

    db.execute(
        "UPDATE consultations SET status = 'completed', ended_at = datetime('now') WHERE id = ?",
        (consultation_id,),
    )
    # Increment astrologer's total_consultations
    db.execute(
        "UPDATE astrologers SET total_consultations = total_consultations + 1 WHERE id = ?",
        (astrologer["id"],),
    )
    db.commit()

    # Return updated consultation per contract: {consultation}
    updated = db.execute(
        "SELECT * FROM consultations WHERE id = ?", (consultation_id,)
    ).fetchone()
    return dict(updated)


# ============================================================
# M-02: Video Call Integration (Jitsi Meet)
# ============================================================

class VideoLinkResponse(BaseModel):
    video_link: str
    room_name: str
    status: str


def _stored_jitsi_link(value: str | None) -> str | None:
    """Return the stored Jitsi link when notes already contain one."""
    if isinstance(value, str) and value.startswith("https://meet.jit.si/"):
        return value
    return None


@router.post(
    "/api/consultations/{consultation_id}/video-link",
    response_model=VideoLinkResponse,
)
def generate_video_link(
    consultation_id: str,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Generate a Jitsi Meet video link for a consultation. Requires JWT (participant only)."""
    user_id = user.get("sub")

    # Fetch consultation and verify it exists
    consultation = db.execute(
        """
        SELECT c.id, c.user_id, c.astrologer_id, c.type, c.status, c.notes,
               a.user_id as astrologer_user_id
        FROM consultations c
        JOIN astrologers a ON a.id = c.astrologer_id
        WHERE c.id = ?
        """,
        (consultation_id,),
    ).fetchone()

    if consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Consultation not found"
        )

    # Verify caller is a participant (client or astrologer)
    if user_id not in (consultation["user_id"], consultation["astrologer_user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a participant"
        )

    if consultation["type"] != "video":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video link is only available for video consultations",
        )

    if consultation["status"] not in ("accepted", "active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video room becomes available after the consultation is accepted",
        )

    stored_link = _stored_jitsi_link(consultation["notes"])
    if stored_link:
        room_name = stored_link.rstrip("/").rsplit("/", 1)[-1]
        video_link = stored_link
    else:
        room_name = f"AstroVedic-{consultation_id}"
        video_link = f"https://meet.jit.si/{room_name}"

    updated_status = "active" if consultation["status"] == "accepted" else consultation["status"]
    db.execute(
        """
        UPDATE consultations
        SET notes = ?, status = ?, started_at = COALESCE(started_at, datetime('now'))
        WHERE id = ?
        """,
        (video_link, updated_status, consultation_id),
    )
    db.commit()

    return VideoLinkResponse(video_link=video_link, room_name=room_name, status=updated_status)
