"""Product bundle routes — consultation + product bundling with discounts."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import get_current_user, require_role
from app.database import get_db
from app.models import BundleCreate, BundleUpdate, BundleResponse, BundleItemResponse

router = APIRouter()

# ---------------------------------------------------------------------------
# Consultation pricing lookup (per-minute rates for fixed-duration packages)
# ---------------------------------------------------------------------------
CONSULTATION_PRICES = {
    "chat": 500.0,    # 30-min chat consultation base price (INR)
    "call": 1000.0,   # 30-min call consultation base price (INR)
    "video": 1500.0,  # 30-min video consultation base price (INR)
}


def _build_bundle_response(bundle_row: dict, items: list, db: Any) -> dict:
    """Build a full bundle response dict with calculated prices."""
    bundle_items = []
    original_price = 0.0

    for item in items:
        item_dict = dict(item)
        product_name = None
        product_price = None

        if item_dict.get("product_id"):
            product = db.execute(
                "SELECT name, price FROM products WHERE id = %s",
                (item_dict["product_id"],),
            ).fetchone()
            if product:
                product_name = product["name"]
                product_price = product["price"]
                original_price += product_price * item_dict["quantity"]
        elif item_dict.get("consultation_type"):
            ctype = item_dict["consultation_type"]
            product_price = CONSULTATION_PRICES.get(ctype, 0.0)
            product_name = f"{ctype.capitalize()} Consultation"
            original_price += product_price * item_dict["quantity"]

        bundle_items.append(
            BundleItemResponse(
                id=item_dict["id"],
                product_id=item_dict.get("product_id"),
                consultation_type=item_dict.get("consultation_type"),
                quantity=item_dict["quantity"],
                product_name=product_name,
                product_price=product_price,
            ).model_dump()
        )

    discount = bundle_row["discount_percent"]
    discounted_price = round(original_price * (1 - discount / 100), 2)
    savings = round(original_price - discounted_price, 2)

    return BundleResponse(
        id=bundle_row["id"],
        name=bundle_row["name"],
        description=bundle_row.get("description"),
        bundle_type=bundle_row["bundle_type"],
        discount_percent=discount,
        is_active=bool(bundle_row["is_active"]),
        created_at=bundle_row["created_at"],
        items=bundle_items,
        original_price=round(original_price, 2),
        discounted_price=discounted_price,
        savings=savings,
    ).model_dump()


# ---------------------------------------------------------------------------
# Public endpoints
# ---------------------------------------------------------------------------
@router.get("/api/bundles")
def list_bundles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Any = Depends(get_db),
):
    """List all active bundles with calculated prices."""
    offset = (page - 1) * limit

    count_row = db.execute(
        "SELECT COUNT(*) as total FROM product_bundles WHERE is_active = 1",
    ).fetchone()
    total = count_row["total"]

    rows = db.execute(
        "SELECT * FROM product_bundles WHERE is_active = 1 "
        "ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (limit, offset),
    ).fetchall()

    bundles = []
    for row in rows:
        items = db.execute(
            "SELECT * FROM bundle_items WHERE bundle_id = %s", (row["id"],)
        ).fetchall()
        bundles.append(_build_bundle_response(dict(row), items, db))

    return {"bundles": bundles, "total": total, "page": page}


@router.get("/api/bundles/{bundle_id}")
def get_bundle(bundle_id: str, db: Any = Depends(get_db)):
    """Get a single bundle with full details and calculated savings."""
    row = db.execute(
        "SELECT * FROM product_bundles WHERE id = %s AND is_active = 1",
        (bundle_id,),
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bundle not found"
        )

    items = db.execute(
        "SELECT * FROM bundle_items WHERE bundle_id = %s", (bundle_id,)
    ).fetchall()

    return _build_bundle_response(dict(row), items, db)


# ---------------------------------------------------------------------------
# Admin endpoints
# ---------------------------------------------------------------------------
@router.post("/api/bundles", status_code=status.HTTP_201_CREATED)
def create_bundle(
    req: BundleCreate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Create a new product bundle (admin only)."""
    # Validate items — each must have product_id or consultation_type
    for item in req.items:
        if not item.product_id and not item.consultation_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each bundle item must have a product_id or consultation_type",
            )
        if item.product_id and item.consultation_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bundle item cannot have both product_id and consultation_type",
            )
        # Verify product exists if product_id given
        if item.product_id:
            product = db.execute(
                "SELECT id FROM products WHERE id = %s AND is_active = 1",
                (item.product_id,),
            ).fetchone()
            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found",
                )

    # Insert bundle
    cursor = db.execute(
        "INSERT INTO product_bundles (name, description, bundle_type, discount_percent) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (req.name, req.description, req.bundle_type.value, req.discount_percent),
    )
    bundle_id = cursor.fetchone()["id"]

    # Insert bundle items
    for item in req.items:
        db.execute(
            "INSERT INTO bundle_items (bundle_id, product_id, consultation_type, quantity) "
            "VALUES (%s, %s, %s, %s)",
            (bundle_id, item.product_id, item.consultation_type, item.quantity),
        )

    db.commit()

    # Return full bundle response
    bundle_row = db.execute(
        "SELECT * FROM product_bundles WHERE id = %s", (bundle_id,)
    ).fetchone()
    items = db.execute(
        "SELECT * FROM bundle_items WHERE bundle_id = %s", (bundle_id,)
    ).fetchall()

    return _build_bundle_response(dict(bundle_row), items, db)


@router.put("/api/bundles/{bundle_id}")
def update_bundle(
    bundle_id: str,
    req: BundleUpdate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Update an existing bundle (admin only)."""
    existing = db.execute(
        "SELECT * FROM product_bundles WHERE id = %s", (bundle_id,)
    ).fetchone()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bundle not found"
        )

    updates = {}
    if req.name is not None:
        updates["name"] = req.name
    if req.description is not None:
        updates["description"] = req.description
    if req.discount_percent is not None:
        updates["discount_percent"] = req.discount_percent
    if req.is_active is not None:
        updates["is_active"] = 1 if req.is_active else 0

    if updates:
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        values = list(updates.values()) + [bundle_id]
        db.execute(
            f"UPDATE product_bundles SET {set_clause} WHERE id = %s", values
        )
        db.commit()

    bundle_row = db.execute(
        "SELECT * FROM product_bundles WHERE id = %s", (bundle_id,)
    ).fetchone()
    items = db.execute(
        "SELECT * FROM bundle_items WHERE bundle_id = %s", (bundle_id,)
    ).fetchall()

    return _build_bundle_response(dict(bundle_row), items, db)


@router.delete("/api/bundles/{bundle_id}")
def deactivate_bundle(
    bundle_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Soft-delete a bundle by marking it inactive (admin only)."""
    existing = db.execute(
        "SELECT id FROM product_bundles WHERE id = %s", (bundle_id,)
    ).fetchone()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bundle not found"
        )

    db.execute(
        "UPDATE product_bundles SET is_active = 0 WHERE id = %s", (bundle_id,)
    )
    db.commit()

    return {"detail": "Bundle deactivated", "id": bundle_id}


# ---------------------------------------------------------------------------
# Add bundle to cart
# ---------------------------------------------------------------------------
@router.post("/api/cart/add-bundle/{bundle_id}", status_code=status.HTTP_201_CREATED)
def add_bundle_to_cart(
    bundle_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Add all products from a bundle to the user's cart with the bundle discount applied.
    Consultation items are recorded as a note; product items are added to cart_items.
    """
    user_id = user.get("sub")

    bundle = db.execute(
        "SELECT * FROM product_bundles WHERE id = %s AND is_active = 1",
        (bundle_id,),
    ).fetchone()

    if bundle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bundle not found"
        )

    items = db.execute(
        "SELECT * FROM bundle_items WHERE bundle_id = %s", (bundle_id,)
    ).fetchall()

    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bundle has no items"
        )

    discount_percent = bundle["discount_percent"]
    added_products = []
    consultation_items = []

    for item in items:
        if item["product_id"]:
            # Verify product is active and in stock
            product = db.execute(
                "SELECT id, stock, is_active, name, price FROM products WHERE id = %s",
                (item["product_id"],),
            ).fetchone()

            if product is None or not product["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{item['product_id']}' in bundle is unavailable",
                )

            qty = item["quantity"]

            # Check existing cart item
            existing = db.execute(
                "SELECT id, quantity FROM cart_items WHERE user_id = %s AND product_id = %s",
                (user_id, item["product_id"]),
            ).fetchone()

            new_qty = qty
            if existing:
                new_qty = existing["quantity"] + qty

            if new_qty > product["stock"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{product['name']}'. Available: {product['stock']}",
                )

            if existing:
                db.execute(
                    "UPDATE cart_items SET quantity = %s WHERE id = %s",
                    (new_qty, existing["id"]),
                )
            else:
                db.execute(
                    "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (user_id, item["product_id"], qty),
                )

            added_products.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "quantity": qty,
                "unit_price": product["price"],
                "discounted_unit_price": round(product["price"] * (1 - discount_percent / 100), 2),
            })

        elif item["consultation_type"]:
            ctype = item["consultation_type"]
            base_price = CONSULTATION_PRICES.get(ctype, 0.0)
            consultation_items.append({
                "consultation_type": ctype,
                "quantity": item["quantity"],
                "base_price": base_price,
                "discounted_price": round(base_price * (1 - discount_percent / 100), 2),
            })

    db.commit()

    # Build cart summary
    cart_rows = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
               p.name, p.price, p.image_url, p.stock, p.category
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = %s
        ORDER BY ci.created_at DESC
        """,
        (user_id,),
    ).fetchall()
    cart_items = [dict(r) for r in cart_rows]
    cart_total = sum(it["price"] * it["quantity"] for it in cart_items)

    return {
        "message": f"Bundle '{bundle['name']}' added to cart with {discount_percent}% discount",
        "bundle_id": bundle_id,
        "bundle_name": bundle["name"],
        "discount_percent": discount_percent,
        "added_products": added_products,
        "consultation_items": consultation_items,
        "cart": {"items": cart_items, "total": round(cart_total, 2)},
    }
