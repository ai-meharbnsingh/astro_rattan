"""Shopping cart routes — all require JWT auth."""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.database import get_db
from app.models import CartAddRequest, CartUpdateRequest

router = APIRouter()


@router.get("/api/cart")
def get_cart(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Get the current user's cart with product details."""
    user_id = user.get("sub")

    rows = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
               p.name, p.price, p.image_url, p.stock, p.category
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = ?
        ORDER BY ci.created_at DESC
        """,
        (user_id,),
    ).fetchall()

    items = [dict(row) for row in rows]
    total = sum(item["price"] * item["quantity"] for item in items)

    return {"items": items, "total": round(total, 2)}


@router.post("/api/cart/add", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    req: CartAddRequest,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Add a product to the cart. Checks stock availability."""
    user_id = user.get("sub")

    # Verify product exists and is active
    product = db.execute(
        "SELECT id, stock, is_active FROM products WHERE id = ?", (req.product_id,)
    ).fetchone()

    if product is None or not product["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Check if already in cart
    existing = db.execute(
        "SELECT id, quantity FROM cart_items WHERE user_id = ? AND product_id = ?",
        (user_id, req.product_id),
    ).fetchone()

    new_qty = req.quantity
    if existing:
        new_qty = existing["quantity"] + req.quantity

    # Check stock
    if new_qty > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product['stock']}",
        )

    if existing:
        db.execute(
            "UPDATE cart_items SET quantity = ? WHERE id = ?",
            (new_qty, existing["id"]),
        )
    else:
        db.execute(
            "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, req.product_id, req.quantity),
        )

    db.commit()

    # Return the updated cart per contract: {cart}
    # Re-fetch cart to return full state
    cart_rows = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
               p.name, p.price, p.image_url, p.stock, p.category
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = ?
        ORDER BY ci.created_at DESC
        """,
        (user_id,),
    ).fetchall()
    cart_items = [dict(r) for r in cart_rows]
    cart_total = sum(item["price"] * item["quantity"] for item in cart_items)
    return {"items": cart_items, "total": round(cart_total, 2)}


@router.patch("/api/cart/{item_id}")
def update_cart_item(
    item_id: str,
    req: CartUpdateRequest,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Update quantity of a cart item. Must belong to current user."""
    user_id = user.get("sub")

    item = db.execute(
        "SELECT ci.id, ci.product_id FROM cart_items ci WHERE ci.id = ? AND ci.user_id = ?",
        (item_id, user_id),
    ).fetchone()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )

    # Check stock
    product = db.execute(
        "SELECT stock FROM products WHERE id = ?", (item["product_id"],)
    ).fetchone()

    if product and req.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product['stock']}",
        )

    db.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (req.quantity, item_id))
    db.commit()

    # Return updated cart per contract: {cart}
    cart_rows = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
               p.name, p.price, p.image_url, p.stock, p.category
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = ?
        ORDER BY ci.created_at DESC
        """,
        (user_id,),
    ).fetchall()
    cart_items = [dict(r) for r in cart_rows]
    cart_total = sum(it["price"] * it["quantity"] for it in cart_items)
    return {"items": cart_items, "total": round(cart_total, 2)}


@router.delete("/api/cart/{item_id}")
def remove_cart_item(
    item_id: str,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Remove an item from the cart. Must belong to current user."""
    user_id = user.get("sub")

    item = db.execute(
        "SELECT id FROM cart_items WHERE id = ? AND user_id = ?",
        (item_id, user_id),
    ).fetchone()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )

    db.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))
    db.commit()

    # Return updated cart per contract: {cart}
    cart_rows = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
               p.name, p.price, p.image_url, p.stock, p.category
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = ?
        ORDER BY ci.created_at DESC
        """,
        (user_id,),
    ).fetchall()
    remaining = [dict(r) for r in cart_rows]
    remaining_total = sum(it["price"] * it["quantity"] for it in remaining)
    return {"items": remaining, "total": round(remaining_total, 2)}
