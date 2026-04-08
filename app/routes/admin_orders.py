"""Admin order management routes — list and update orders."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import require_role
from app.database import get_db
from app.models import AdminOrderUpdate

router = APIRouter()


@router.get("/api/admin/orders")
def list_all_orders(
    status_filter: str = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all orders with optional status filter."""
    offset = (page - 1) * limit

    if status_filter:
        count_row = db.execute(
            "SELECT COUNT(*) as total FROM orders WHERE status = %s", (status_filter,)
        ).fetchone()
        rows = db.execute(
            """
            SELECT o.*, u.name as user_name, u.email as user_email
            FROM orders o JOIN users u ON u.id = o.user_id
            WHERE o.status = %s
            ORDER BY o.created_at DESC LIMIT %s OFFSET %s
            """,
            (status_filter, limit, offset),
        ).fetchall()
    else:
        count_row = db.execute("SELECT COUNT(*) as total FROM orders").fetchone()
        rows = db.execute(
            """
            SELECT o.*, u.name as user_name, u.email as user_email
            FROM orders o JOIN users u ON u.id = o.user_id
            ORDER BY o.created_at DESC LIMIT %s OFFSET %s
            """,
            (limit, offset),
        ).fetchall()

    return {
        "orders": [dict(row) for row in rows],
        "total": count_row["total"],
    }


@router.patch("/api/admin/orders/{order_id}")
def update_order(
    order_id: str,
    req: AdminOrderUpdate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Update an order's status or tracking number."""
    order = db.execute("SELECT id FROM orders WHERE id = %s", (order_id,)).fetchone()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    updates = []
    params = []
    if req.status is not None:
        updates.append("status = %s")
        params.append(req.status.value)
    if req.tracking_number is not None:
        updates.append("tracking_number = %s")
        params.append(req.tracking_number)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    updates.append("updated_at = NOW()")
    params.append(order_id)

    db.execute(f"UPDATE orders SET {', '.join(updates)} WHERE id = %s", params)
    db.commit()

    updated = db.execute("SELECT * FROM orders WHERE id = %s", (order_id,)).fetchone()
    return dict(updated)
