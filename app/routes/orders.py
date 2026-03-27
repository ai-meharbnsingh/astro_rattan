"""Order management routes — all require JWT auth."""
from typing import Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from app.auth import get_current_user
from app.database import get_db
from app.email_service import send_order_alert, send_order_confirmation
from app.models import OrderCreateRequest

router = APIRouter()


@router.post("/api/orders", status_code=status.HTTP_201_CREATED)
def create_order(
    req: OrderCreateRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Create an order from the current user's cart.
    Validates stock, calculates total, moves cart items to order_items, clears cart.
    """
    user_id = user.get("sub")

    # Fetch cart items with product details
    cart_rows = db.execute(
        """
        SELECT ci.id as cart_id, ci.product_id, ci.quantity,
               p.name, p.price, p.stock
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = %s
        """,
        (user_id,),
    ).fetchall()

    if not cart_rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )

    cart_items = [dict(row) for row in cart_rows]
    user_row = db.execute(
        "SELECT email FROM users WHERE id = %s",
        (user_id,),
    ).fetchone()

    # Validate stock for all items
    for item in cart_items:
        if item["quantity"] > item["stock"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{item['name']}'. Available: {item['stock']}",
            )

    # Calculate total
    total = sum(item["price"] * item["quantity"] for item in cart_items)

    # Create order
    cursor = db.execute(
        """
        INSERT INTO orders (user_id, total, shipping_address, payment_method)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (user_id, round(total, 2), req.shipping_address, req.payment_method.value),
    )
    order_id = cursor.fetchone()["id"]

    # Create order items and reduce stock
    for item in cart_items:
        db.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, price, product_name)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, item["product_id"], item["quantity"], item["price"], item["name"]),
        )
        db.execute(
            "UPDATE products SET stock = stock - %s WHERE id = %s",
            (item["quantity"], item["product_id"]),
        )

    # Clear cart
    db.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))
    db.commit()

    # Return the full order per contract: {order}
    order_full = db.execute(
        "SELECT * FROM orders WHERE id = %s", (order_id,)
    ).fetchone()
    order_payload = {**dict(order_full), "items": cart_items}
    if user_row and user_row["email"]:
        background_tasks.add_task(send_order_confirmation, order_payload, user_row["email"])
        background_tasks.add_task(send_order_alert, order_payload, user_row["email"])
    return dict(order_full)


@router.get("/api/orders")
def list_orders(
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all orders for the current user."""
    user_id = user.get("sub")

    rows = db.execute(
        """
        SELECT id, status, total, shipping_address, payment_method,
               payment_status, tracking_number, created_at, updated_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
    ).fetchall()

    # Map id to order_number for frontend compatibility
    orders = []
    for row in rows:
        order = dict(row)
        order['order_number'] = f"ORD-{str(order['id'])[:8].upper()}"
        orders.append(order)
    return orders


@router.get("/api/orders/{order_id}")
def get_order(
    order_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Get a single order with its items. Must belong to current user."""
    user_id = user.get("sub")

    order = db.execute(
        "SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user_id)
    ).fetchone()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    items = db.execute(
        "SELECT * FROM order_items WHERE order_id = %s", (order_id,)
    ).fetchall()

    return {
        **dict(order),
        "items": [dict(item) for item in items],
    }
