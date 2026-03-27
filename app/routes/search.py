"""H-11: Global Search using PostgreSQL ILIKE — search products, content, and astrologers."""
from typing import Any
from fastapi import APIRouter, Depends, Query, status
from app.database import get_db

router = APIRouter(prefix="/api/search", tags=["search"])


def _search_products(db: Any, query: str, limit: int = 20):
    """Search products using ILIKE."""
    results = []
    rows = db.execute(
        """
        SELECT id, name AS title, description AS snippet, category
        FROM products
        WHERE is_active = 1 AND (name ILIKE %s OR description ILIKE %s OR category ILIKE %s)
        LIMIT %s
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%", limit),
    ).fetchall()
    for row in rows:
        results.append({
            "type": "product",
            "id": row["id"],
            "title": row["title"],
            "snippet": (row["snippet"] or "")[:200],
            "score": 0,
        })
    return results


def _search_content_fts(db: Any, query: str, limit: int = 20):
    """Search content library using ILIKE."""
    results = []
    rows = db.execute(
        """
        SELECT id, title, content AS snippet, category
        FROM content_library
        WHERE title ILIKE %s OR content ILIKE %s OR category ILIKE %s
        LIMIT %s
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%", limit),
    ).fetchall()
    for row in rows:
        results.append({
            "type": "content",
            "id": row["id"],
            "title": row["title"],
            "snippet": (row["snippet"] or "")[:200],
            "score": 0,
        })
    return results


def _search_astrologers(db: Any, query: str, limit: int = 20):
    """Search astrologers using ILIKE on name/bio."""
    results = []
    rows = db.execute(
        """
        SELECT a.id, a.display_name AS title, a.bio AS snippet,
               a.specializations, a.rating
        FROM astrologers a
        WHERE a.is_approved = 1
          AND (a.display_name ILIKE %s OR a.bio ILIKE %s OR a.specializations ILIKE %s)
        LIMIT %s
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%", limit),
    ).fetchall()
    for row in rows:
        results.append({
            "type": "astrologer",
            "id": row["id"],
            "title": row["title"],
            "snippet": (row["snippet"] or "")[:200],
            "score": 0,
        })
    return results


@router.get("", status_code=status.HTTP_200_OK)
def global_search(
    q: str = Query(..., min_length=1, max_length=200),
    type: str = Query("all", pattern="^(all|products|content|astrologers)$"),
    db: Any = Depends(get_db),
):
    """Global search across products, content library, and astrologers.

    Query params:
        q: search query string
        type: all | products | content | astrologers
    Returns:
        {results: [{type, id, title, snippet, score}], total}
    """
    results = []

    if type in ("all", "products"):
        results.extend(_search_products(db, q))

    if type in ("all", "content"):
        results.extend(_search_content_fts(db, q))

    if type in ("all", "astrologers"):
        results.extend(_search_astrologers(db, q))

    return {
        "results": results,
        "total": len(results),
    }
