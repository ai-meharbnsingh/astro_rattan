"""Product catalog routes — public, no auth required."""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.database import get_db

router = APIRouter()


@router.get("/api/products")
def list_products(
    category: str = Query(None, description="Filter by product category"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Any = Depends(get_db),
):
    """
    List active products with optional category filter and pagination.
    Contract response: {products, total, page}
    """
    offset = (page - 1) * limit

    # Build query dynamically based on optional category filter
    if category:
        count_row = db.execute(
            "SELECT COUNT(*) as total FROM products WHERE is_active = 1 AND category = %s",
            (category,),
        ).fetchone()
        rows = db.execute(
            "SELECT * FROM products WHERE is_active = 1 AND category = %s "
            "ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (category, limit, offset),
        ).fetchall()
    else:
        count_row = db.execute(
            "SELECT COUNT(*) as total FROM products WHERE is_active = 1",
        ).fetchone()
        rows = db.execute(
            "SELECT * FROM products WHERE is_active = 1 "
            "ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset),
        ).fetchall()

    total = count_row["total"]
    products = [dict(row) for row in rows]

    return {
        "products": products,
        "total": total,
        "page": page,
    }


@router.get("/api/products/{product_id}")
def get_product(product_id: str, db: Any = Depends(get_db)):
    """
    Get a single product by ID. No authentication required.
    Contract response: {product detail} — returned directly, no wrapper.
    """
    row = db.execute(
        "SELECT * FROM products WHERE id = %s AND is_active = 1", (product_id,)
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return dict(row)
