"""Admin product management routes — CRUD, stock update, toggle, image upload."""
import os
import uuid
from typing import Any
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from app.auth import require_role
from app.database import get_db
from app.models import ProductCreate

router = APIRouter()


# ============================================================
# Product CRUD
# ============================================================

@router.get("/api/admin/products")
def admin_list_products(
    category: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all products with optional category filter (admin view includes inactive)."""
    offset = (page - 1) * limit
    if category:
        count = db.execute(
            "SELECT COUNT(*) as c FROM products WHERE category = %s", (category,)
        ).fetchone()["c"]
        rows = db.execute(
            "SELECT * FROM products WHERE category = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (category, limit, offset),
        ).fetchall()
    else:
        count = db.execute("SELECT COUNT(*) as c FROM products").fetchone()["c"]
        rows = db.execute(
            "SELECT * FROM products ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset),
        ).fetchall()

    return {"products": [dict(r) for r in rows], "total": count, "page": page}


@router.post("/api/admin/products", status_code=status.HTTP_201_CREATED)
def admin_create_product(
    req: ProductCreate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Create a new product."""
    cursor = db.execute(
        """INSERT INTO products (name, description, category, price, compare_price,
           image_url, weight, planet, properties, stock)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (
            req.name, req.description, req.category.value, req.price,
            req.compare_price, req.image_url, req.weight, req.planet,
            req.properties, req.stock,
        ),
    )
    product_id = cursor.fetchone()["id"]
    db.commit()

    row = db.execute("SELECT * FROM products WHERE id = %s", (product_id,)).fetchone()
    return dict(row)


@router.patch("/api/admin/products/{product_id}")
def admin_update_product(
    product_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Update a product (name, description, price, stock, is_active, etc.)."""
    existing = db.execute("SELECT id FROM products WHERE id = %s", (product_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return {"message": "Use PUT with full ProductCreate body or individual field updates"}


@router.put("/api/admin/products/{product_id}")
def admin_replace_product(
    product_id: str,
    req: ProductCreate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Replace a product entirely."""
    existing = db.execute("SELECT id FROM products WHERE id = %s", (product_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.execute(
        """UPDATE products SET name=%s, description=%s, category=%s, price=%s,
           compare_price=%s, image_url=%s, weight=%s, planet=%s, properties=%s,
           stock=%s, updated_at=to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id=%s""",
        (
            req.name, req.description, req.category.value, req.price,
            req.compare_price, req.image_url, req.weight, req.planet,
            req.properties, req.stock, product_id,
        ),
    )
    db.commit()

    row = db.execute("SELECT * FROM products WHERE id = %s", (product_id,)).fetchone()
    return dict(row)


@router.patch("/api/admin/products/{product_id}/stock")
def admin_update_stock(
    product_id: str,
    stock: int = Query(..., ge=0),
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Quick stock update for a product."""
    existing = db.execute("SELECT id FROM products WHERE id = %s", (product_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.execute(
        "UPDATE products SET stock = %s, updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
        (stock, product_id),
    )
    db.commit()
    return {"product_id": product_id, "stock": stock}


@router.patch("/api/admin/products/{product_id}/toggle")
def admin_toggle_product(
    product_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Toggle product active/inactive."""
    row = db.execute("SELECT id, is_active FROM products WHERE id = %s", (product_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    new_status = 0 if row["is_active"] else 1
    db.execute(
        "UPDATE products SET is_active = %s, updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
        (new_status, product_id),
    )
    db.commit()
    return {"product_id": product_id, "is_active": bool(new_status)}


# ============================================================
# Image upload
# ============================================================

_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")


@router.post("/api/admin/upload-image")
def upload_image(
    file: UploadFile = File(...),
    user: dict = Depends(require_role("admin")),
):
    """Upload an image file. Returns the URL to access it."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided"
        )

    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{ext}' not allowed. Allowed: {', '.join(_ALLOWED_EXTENSIONS)}",
        )

    unique_name = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(_UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(_UPLOAD_DIR, unique_name)
    contents = file.file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return {"url": f"/static/uploads/{unique_name}"}
