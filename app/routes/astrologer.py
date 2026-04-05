"""Astrologer dashboard and profile management routes."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user, require_role
from app.database import get_db
from app.models import AstrologerProfileUpdate, AstrologerAvailability

router = APIRouter()


@router.get("/api/astrologers/favorites")
def get_favorite_astrologers(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the current user's favorite astrologers.

    TODO: The favorites table does not exist yet. Once an
    ``astrologer_favorites`` table is created (user_id, astrologer_id),
    this endpoint should query it and return joined astrologer profiles.
    For now it returns an empty list so the frontend does not break.
    """
    return {"favorites": []}


def _get_astrologer_record(user_id: str, db: Any):
    """Fetch astrologer record by user_id or raise 403."""
    row = db.execute(
        "SELECT * FROM astrologers WHERE user_id = %s", (user_id,)
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Astrologer profile not found for this user",
        )
    return row


@router.get("/api/astrologer/dashboard")
def astrologer_dashboard(
    user: dict = Depends(require_role("astrologer")),
    db: Any = Depends(get_db),
):
    """Astrologer dashboard with consultation stats and earnings."""
    user_id = user.get("sub")
    astrologer = _get_astrologer_record(user_id, db)
    astrologer_id = astrologer["id"]

    total_consultations = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE astrologer_id = %s",
        (astrologer_id,),
    ).fetchone()["c"]

    pending = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE astrologer_id = %s AND status = 'requested'",
        (astrologer_id,),
    ).fetchone()["c"]

    active = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE astrologer_id = %s AND status = 'active'",
        (astrologer_id,),
    ).fetchone()["c"]

    completed = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE astrologer_id = %s AND status = 'completed'",
        (astrologer_id,),
    ).fetchone()["c"]

    total_earnings = db.execute(
        "SELECT COALESCE(SUM(total_charge), 0) as c FROM consultations WHERE astrologer_id = %s AND status = 'completed'",
        (astrologer_id,),
    ).fetchone()["c"]

    return {
        "earnings": round(total_earnings, 2),
        "consultations": total_consultations,
        "rating": astrologer["rating"],
        "upcoming": pending,
    }


@router.get("/api/astrologer/profile")
def astrologer_profile(
    user: dict = Depends(require_role("astrologer")),
    db: Any = Depends(get_db),
):
    """Return the current astrologer's profile."""
    user_id = user.get("sub")
    astrologer = _get_astrologer_record(user_id, db)
    return dict(astrologer)


@router.get("/api/astrologer/consultations")
def astrologer_consultations(
    user: dict = Depends(require_role("astrologer")),
    db: Any = Depends(get_db),
):
    """List all consultations for this astrologer."""
    user_id = user.get("sub")
    astrologer = _get_astrologer_record(user_id, db)

    rows = db.execute(
        """
        SELECT c.*,
               CASE
                   WHEN c.notes LIKE 'https://meet.jit.si/%' THEN c.notes
                   ELSE NULL
               END as video_link,
               u.name as client_name,
               u.email as client_email
        FROM consultations c
        JOIN users u ON u.id = c.user_id
        WHERE c.astrologer_id = %s
        ORDER BY c.created_at DESC
        """,
        (astrologer["id"],),
    ).fetchall()

    return [dict(row) for row in rows]


@router.patch("/api/astrologer/profile")
def update_profile(
    req: AstrologerProfileUpdate,
    user: dict = Depends(require_role("astrologer")),
    db: Any = Depends(get_db),
):
    """Update astrologer profile fields."""
    user_id = user.get("sub")
    astrologer = _get_astrologer_record(user_id, db)

    updates = []
    params = []

    if req.bio is not None:
        updates.append("bio = %s")
        params.append(req.bio)
    if req.specializations is not None:
        updates.append("specializations = %s")
        params.append(req.specializations)
    if req.per_minute_rate is not None:
        updates.append("per_minute_rate = %s")
        params.append(req.per_minute_rate)
    if req.languages is not None:
        updates.append("languages = %s")
        params.append(req.languages)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    params.append(astrologer["id"])
    db.execute(
        f"UPDATE astrologers SET {', '.join(updates)} WHERE id = %s", params
    )
    db.commit()

    # Return updated profile per contract: {profile}
    updated = db.execute(
        "SELECT * FROM astrologers WHERE id = %s", (astrologer["id"],)
    ).fetchone()
    return dict(updated)


@router.patch("/api/astrologer/availability")
def update_availability(
    req: AstrologerAvailability,
    user: dict = Depends(require_role("astrologer")),
    db: Any = Depends(get_db),
):
    """Toggle astrologer availability."""
    user_id = user.get("sub")
    astrologer = _get_astrologer_record(user_id, db)

    db.execute(
        "UPDATE astrologers SET is_available = %s WHERE id = %s",
        (1 if req.is_available else 0, astrologer["id"]),
    )
    db.commit()

    # Return updated profile per contract: {profile}
    updated = db.execute(
        "SELECT * FROM astrologers WHERE id = %s", (astrologer["id"],)
    ).fetchone()
    return dict(updated)
