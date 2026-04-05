"""User preferences routes — proxy to notification_preferences table.

The PreferencesPage.tsx frontend calls GET/PUT /api/preferences.
The actual notification preferences logic already lives in the notifications
router at /api/notifications/preferences, but the frontend expects the
shorter path.  This module provides the /api/preferences endpoints so
both paths work.
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/preferences", tags=["preferences"])


# ---- Pydantic models ----

class PreferencesUpdate(BaseModel):
    transit_alerts: Optional[bool] = None
    muhurat_alerts: Optional[bool] = None
    festival_alerts: Optional[bool] = None
    daily_digest: Optional[bool] = None
    email_notifications: Optional[bool] = None


# ---- Routes ----

@router.get("", status_code=status.HTTP_200_OK)
def get_preferences(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get notification preferences for the current user."""
    user_id = current_user["sub"]
    row = db.execute(
        "SELECT * FROM notification_preferences WHERE user_id = %s",
        (user_id,),
    ).fetchone()

    if not row:
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


@router.put("", status_code=status.HTTP_200_OK)
def update_preferences(
    body: PreferencesUpdate,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Update notification preferences for the current user."""
    user_id = current_user["sub"]

    existing = db.execute(
        "SELECT user_id FROM notification_preferences WHERE user_id = %s",
        (user_id,),
    ).fetchone()

    if not existing:
        db.execute(
            """INSERT INTO notification_preferences
               (user_id, transit_alerts, muhurat_alerts, festival_alerts, daily_digest, email_notifications)
               VALUES (%s, 1, 1, 1, 1, 0)""",
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
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        values = list(updates.values()) + [user_id]
        db.execute(
            f"UPDATE notification_preferences SET {set_clause} WHERE user_id = %s",
            values,
        )
        db.commit()

    row = db.execute(
        "SELECT * FROM notification_preferences WHERE user_id = %s",
        (user_id,),
    ).fetchone()

    return {
        "transit_alerts": bool(row["transit_alerts"]),
        "muhurat_alerts": bool(row["muhurat_alerts"]),
        "festival_alerts": bool(row["festival_alerts"]),
        "daily_digest": bool(row["daily_digest"]),
        "email_notifications": bool(row["email_notifications"]),
    }
