"""Notification routes — list, mark-read, preferences."""
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from typing import Optional

from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


# ---- Pydantic models ----

class NotificationPreferencesUpdate(BaseModel):
    transit_alerts: Optional[bool] = None
    muhurat_alerts: Optional[bool] = None
    festival_alerts: Optional[bool] = None
    daily_digest: Optional[bool] = None
    email_notifications: Optional[bool] = None


# ---- Routes ----

@router.get("", status_code=status.HTTP_200_OK)
def list_notifications(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List user notifications, paginated, newest first."""
    user_id = current_user["sub"]
    offset = (page - 1) * limit

    total = db.execute(
        "SELECT COUNT(*) as cnt FROM user_notifications WHERE user_id = ?",
        (user_id,),
    ).fetchone()["cnt"]

    rows = db.execute(
        """SELECT id, type, title, message, is_read, link, created_at
           FROM user_notifications
           WHERE user_id = ?
           ORDER BY created_at DESC
           LIMIT ? OFFSET ?""",
        (user_id, limit, offset),
    ).fetchall()

    return {
        "notifications": [
            {
                "id": r["id"],
                "type": r["type"],
                "title": r["title"],
                "message": r["message"],
                "is_read": bool(r["is_read"]),
                "link": r["link"],
                "created_at": r["created_at"],
            }
            for r in rows
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/unread-count", status_code=status.HTTP_200_OK)
def unread_count(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Count of unread notifications."""
    user_id = current_user["sub"]
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM user_notifications WHERE user_id = ? AND is_read = 0",
        (user_id,),
    ).fetchone()
    return {"unread_count": row["cnt"]}


@router.patch("/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_as_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Mark a single notification as read."""
    user_id = current_user["sub"]
    row = db.execute(
        "SELECT id FROM user_notifications WHERE id = ? AND user_id = ?",
        (notification_id, user_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    db.execute(
        "UPDATE user_notifications SET is_read = 1 WHERE id = ? AND user_id = ?",
        (notification_id, user_id),
    )
    db.commit()
    return {"status": "ok"}


@router.patch("/read-all", status_code=status.HTTP_200_OK)
def mark_all_read(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Mark all notifications as read."""
    user_id = current_user["sub"]
    db.execute(
        "UPDATE user_notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0",
        (user_id,),
    )
    db.commit()
    return {"status": "ok"}


@router.get("/preferences", status_code=status.HTTP_200_OK)
def get_preferences(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get notification preferences for the current user."""
    user_id = current_user["sub"]
    row = db.execute(
        "SELECT * FROM notification_preferences WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if not row:
        # Return defaults
        return {
            "transit_alerts": True,
            "muhurat_alerts": True,
            "festival_alerts": True,
            "daily_digest": True,
            "email_notifications": False,
        }

    return {
        "transit_alerts": bool(row["transit_alerts"]),
        "muhurat_alerts": bool(row["muhurat_alerts"]),
        "festival_alerts": bool(row["festival_alerts"]),
        "daily_digest": bool(row["daily_digest"]),
        "email_notifications": bool(row["email_notifications"]),
    }


@router.put("/preferences", status_code=status.HTTP_200_OK)
def update_preferences(
    body: NotificationPreferencesUpdate,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Update notification preferences for the current user."""
    user_id = current_user["sub"]

    existing = db.execute(
        "SELECT user_id FROM notification_preferences WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if not existing:
        # Insert defaults first
        db.execute(
            """INSERT INTO notification_preferences (user_id, transit_alerts, muhurat_alerts, festival_alerts, daily_digest, email_notifications)
               VALUES (?, 1, 1, 1, 1, 0)""",
            (user_id,),
        )
        db.commit()

    updates = {}
    if body.transit_alerts is not None:
        updates["transit_alerts"] = int(body.transit_alerts)
    if body.muhurat_alerts is not None:
        updates["muhurat_alerts"] = int(body.muhurat_alerts)
    if body.festival_alerts is not None:
        updates["festival_alerts"] = int(body.festival_alerts)
    if body.daily_digest is not None:
        updates["daily_digest"] = int(body.daily_digest)
    if body.email_notifications is not None:
        updates["email_notifications"] = int(body.email_notifications)

    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [user_id]
        db.execute(
            f"UPDATE notification_preferences SET {set_clause} WHERE user_id = ?",
            values,
        )
        db.commit()

    # Return updated preferences
    row = db.execute(
        "SELECT * FROM notification_preferences WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    return {
        "transit_alerts": bool(row["transit_alerts"]),
        "muhurat_alerts": bool(row["muhurat_alerts"]),
        "festival_alerts": bool(row["festival_alerts"]),
        "daily_digest": bool(row["daily_digest"]),
        "email_notifications": bool(row["email_notifications"]),
    }
