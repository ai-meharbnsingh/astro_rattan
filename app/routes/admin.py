"""Admin routes — user management, stats, kundli overview."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import get_current_user, require_role
from app.database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Dashboard stats — user count, kundli count, recent activity."""
    users = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    kundlis = db.execute("SELECT COUNT(*) as c FROM kundlis").fetchone()["c"]
    horoscopes = db.execute("SELECT COUNT(*) as c FROM horoscopes").fetchone()["c"]
    panchang = db.execute("SELECT COUNT(*) as c FROM panchang_cache").fetchone()["c"]

    recent_users = db.execute(
        "SELECT id, email, name, role, created_at FROM users ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    recent_kundlis = db.execute(
        """SELECT k.id, k.person_name, k.birth_date, k.created_at, u.email
           FROM kundlis k JOIN users u ON k.user_id = u.id
           ORDER BY k.created_at DESC LIMIT 5"""
    ).fetchall()

    astrologers_count = db.execute("SELECT COUNT(*) as c FROM users WHERE role IN ('astrologer', 'admin')").fetchone()["c"]
    clients_count = db.execute("SELECT COUNT(*) as c FROM clients").fetchone()["c"]

    # Astrologers with their client counts
    astrologers_list = db.execute(
        """SELECT u.id, u.name, u.email, u.role, u.created_at,
                  (SELECT COUNT(*) FROM clients c WHERE c.astrologer_id = u.id) as client_count,
                  (SELECT COUNT(*) FROM kundlis k WHERE k.user_id = u.id) as kundli_count
           FROM users u WHERE u.role IN ('astrologer', 'admin')
           ORDER BY u.created_at DESC"""
    ).fetchall()

    return {
        "counts": {
            "users": users,
            "astrologers": astrologers_count,
            "clients": clients_count,
            "kundlis": kundlis,
            "horoscopes": horoscopes,
            "panchang_cached": panchang,
        },
        "astrologers": [dict(r) for r in astrologers_list],
        "recent_users": [dict(r) for r in recent_users],
        "recent_kundlis": [dict(r) for r in recent_kundlis],
    }


@router.get("/users")
def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all users with pagination."""
    offset = (page - 1) * limit
    total = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    users = db.execute(
        """SELECT id, email, name, role, phone, city, is_active, created_at, updated_at
           FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s""",
        (limit, offset),
    ).fetchall()

    return {
        "users": [dict(r) for r in users],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/users/{user_id}")
def get_user_detail(
    user_id: str,
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Get detailed user info + their kundlis."""
    user = db.execute(
        "SELECT id, email, name, role, phone, city, date_of_birth, gender, is_active, created_at FROM users WHERE id = %s",
        (user_id,),
    ).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    kundlis = db.execute(
        "SELECT id, person_name, birth_date, birth_time, birth_place, created_at FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    return {"user": dict(user), "kundlis": [dict(k) for k in kundlis]}


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: str,
    body: dict,
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Change a user's role (user/astrologer/admin)."""
    new_role = body.get("role")
    if new_role not in ("user", "astrologer", "admin"):
        raise HTTPException(status_code=400, detail="Role must be user, astrologer, or admin")
    db.execute("UPDATE users SET role = %s, updated_at = NOW() WHERE id = %s", (new_role, user_id))
    db.commit()
    return {"message": f"User role updated to {new_role}"}


@router.patch("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: str,
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Activate or deactivate a user account."""
    if user_id == current_user["sub"]:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    db.execute(
        "UPDATE users SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END, updated_at = NOW() WHERE id = %s",
        (user_id,),
    )
    db.commit()
    return {"message": "User status toggled"}


@router.get("/kundlis")
def list_all_kundlis(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all kundlis across all users."""
    offset = (page - 1) * limit
    total = db.execute("SELECT COUNT(*) as c FROM kundlis").fetchone()["c"]
    kundlis = db.execute(
        """SELECT k.id, k.person_name, k.birth_date, k.birth_time, k.birth_place, k.created_at, u.email, u.name as user_name
           FROM kundlis k JOIN users u ON k.user_id = u.id
           ORDER BY k.created_at DESC LIMIT %s OFFSET %s""",
        (limit, offset),
    ).fetchall()

    return {
        "kundlis": [dict(k) for k in kundlis],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }
