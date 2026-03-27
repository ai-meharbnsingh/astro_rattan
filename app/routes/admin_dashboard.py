"""Admin dashboard routes — stats, AI logs, astrologer approval."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import require_role
from app.database import get_db

router = APIRouter()


@router.get("/api/admin/dashboard")
def admin_dashboard(
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Admin dashboard summary with key metrics."""
    total_users = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    total_orders = db.execute("SELECT COUNT(*) as c FROM orders").fetchone()["c"]
    total_revenue = db.execute(
        "SELECT COALESCE(SUM(total), 0) as c FROM orders WHERE payment_status = 'paid'"
    ).fetchone()["c"]
    pending_orders = db.execute(
        "SELECT COUNT(*) as c FROM orders WHERE status = 'placed'"
    ).fetchone()["c"]
    total_consultations = db.execute(
        "SELECT COUNT(*) as c FROM consultations"
    ).fetchone()["c"]
    pending_astrologers = db.execute(
        "SELECT COUNT(*) as c FROM astrologers WHERE is_approved = 0"
    ).fetchone()["c"]
    total_kundlis = db.execute("SELECT COUNT(*) as c FROM kundlis").fetchone()["c"]
    total_reports = db.execute("SELECT COUNT(*) as c FROM reports").fetchone()["c"]

    return {
        "stats": {
            "users": total_users,
            "orders": total_orders,
            "revenue": round(total_revenue, 2),
            "pending_orders": pending_orders,
            "ai_usage": db.execute("SELECT COUNT(*) as c FROM ai_chat_logs").fetchone()["c"],
        },
    }


@router.get("/api/admin/ai-logs")
def list_ai_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List AI chat logs for monitoring and audit."""
    offset = (page - 1) * limit

    count_row = db.execute("SELECT COUNT(*) as total FROM ai_chat_logs").fetchone()
    rows = db.execute(
        """
        SELECT al.*, u.name as user_name, u.email as user_email
        FROM ai_chat_logs al
        JOIN users u ON u.id = al.user_id
        ORDER BY al.created_at DESC LIMIT %s OFFSET %s
        """,
        (limit, offset),
    ).fetchall()

    return {
        "logs": [dict(row) for row in rows],
        "total": count_row["total"],
    }


@router.patch("/api/admin/astrologers/{astrologer_id}/approve")
def approve_astrologer(
    astrologer_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Approve an astrologer profile."""
    astrologer = db.execute(
        "SELECT id FROM astrologers WHERE id = %s", (astrologer_id,)
    ).fetchone()

    if astrologer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astrologer not found"
        )

    db.execute(
        "UPDATE astrologers SET is_approved = 1 WHERE id = %s", (astrologer_id,)
    )
    db.commit()

    updated = db.execute(
        "SELECT * FROM astrologers WHERE id = %s", (astrologer_id,)
    ).fetchone()
    return dict(updated)
