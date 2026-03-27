"""Admin user management routes — list, create, update, deactivate, activate, activity."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import require_role, hash_password
from app.database import get_db
from app.models import AdminUserUpdate, AdminUserCreate

router = APIRouter()


@router.get("/api/admin/users")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all users with pagination."""
    offset = (page - 1) * limit

    count_row = db.execute("SELECT COUNT(*) as total FROM users").fetchone()
    rows = db.execute(
        """
        SELECT id, email, name, role, phone, is_active, created_at, updated_at
        FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s
        """,
        (limit, offset),
    ).fetchall()

    return {
        "users": [dict(row) for row in rows],
        "total": count_row["total"],
    }


@router.get("/api/admin/users/{user_id}")
def get_user_detail(
    user_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """View full user detail with activity counts."""
    row = db.execute(
        """SELECT id, email, name, role, phone, avatar_url,
                  date_of_birth, gender, city, is_active, created_at, updated_at
           FROM users WHERE id = %s""",
        (user_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    kundli_count = db.execute(
        "SELECT COUNT(*) as c FROM kundlis WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    order_count = db.execute(
        "SELECT COUNT(*) as c FROM orders WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    consultation_count = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    ai_usage_count = db.execute(
        "SELECT COUNT(*) as c FROM ai_chat_logs WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]

    result = dict(row)
    result["kundli_count"] = kundli_count
    result["order_count"] = order_count
    result["consultation_count"] = consultation_count
    result["ai_usage_count"] = ai_usage_count
    return result


@router.post("/api/admin/users", status_code=status.HTTP_201_CREATED)
def admin_create_user(
    req: AdminUserCreate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Create a user manually (for creating astrologer/admin accounts)."""
    existing = db.execute("SELECT id FROM users WHERE email = %s", (req.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    pw_hash = hash_password(req.password)
    db.execute(
        "INSERT INTO users (email, password_hash, name, role, phone) VALUES (%s, %s, %s, %s, %s)",
        (req.email, pw_hash, req.name, req.role.value, req.phone),
    )
    db.commit()

    created = db.execute(
        """SELECT id, email, name, role, phone, is_active, created_at, updated_at
           FROM users WHERE email = %s""",
        (req.email,),
    ).fetchone()
    return dict(created)


@router.patch("/api/admin/users/{user_id}/deactivate")
def deactivate_user(
    user_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Deactivate a user. Cannot deactivate self."""
    if user["sub"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate yourself"
        )

    target = db.execute("SELECT id FROM users WHERE id = %s", (user_id,)).fetchone()
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.execute(
        "UPDATE users SET is_active = 0, updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
        (user_id,),
    )
    db.commit()

    updated = db.execute(
        "SELECT id, email, name, role, is_active, updated_at FROM users WHERE id = %s",
        (user_id,),
    ).fetchone()
    return dict(updated)


@router.patch("/api/admin/users/{user_id}/activate")
def activate_user(
    user_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Reactivate a user."""
    target = db.execute("SELECT id FROM users WHERE id = %s", (user_id,)).fetchone()
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.execute(
        "UPDATE users SET is_active = 1, updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
        (user_id,),
    )
    db.commit()

    updated = db.execute(
        "SELECT id, email, name, role, is_active, updated_at FROM users WHERE id = %s",
        (user_id,),
    ).fetchone()
    return dict(updated)


@router.get("/api/admin/users/{user_id}/activity")
def get_user_activity(
    user_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """View all user activity — kundlis, orders, consultations, AI chats, reports."""
    target = db.execute("SELECT id FROM users WHERE id = %s", (user_id,)).fetchone()
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    kundlis = db.execute(
        "SELECT id, person_name, birth_date, birth_place, created_at FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    orders = db.execute(
        "SELECT id, status, total, payment_status, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    consultations = db.execute(
        "SELECT id, type, status, scheduled_at, created_at FROM consultations WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    ai_chats = db.execute(
        "SELECT id, chat_type, user_message, created_at FROM ai_chat_logs WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    reports = db.execute(
        "SELECT id, report_type, status, price, created_at FROM reports WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    return {
        "kundlis": [dict(r) for r in kundlis],
        "orders": [dict(r) for r in orders],
        "consultations": [dict(r) for r in consultations],
        "ai_chats": [dict(r) for r in ai_chats],
        "reports": [dict(r) for r in reports],
    }


@router.patch("/api/admin/users/{user_id}")
def update_user(
    user_id: str,
    req: AdminUserUpdate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Update a user's role or active status."""
    target = db.execute("SELECT id FROM users WHERE id = %s", (user_id,)).fetchone()
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updates = []
    params = []
    if req.role is not None:
        updates.append("role = %s")
        params.append(req.role.value)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    updates.append("updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')")
    params.append(user_id)

    db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", params)
    db.commit()

    updated = db.execute(
        "SELECT id, email, name, role, phone, created_at, updated_at FROM users WHERE id = %s",
        (user_id,),
    ).fetchone()
    return dict(updated)
