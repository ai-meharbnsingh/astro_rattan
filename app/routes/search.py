"""H-11: Global Search using FTS5 — search products, content, and astrologers."""
import sqlite3
from fastapi import APIRouter, Depends, Query, status
from app.database import get_db

router = APIRouter(prefix="/api/search", tags=["search"])


def _search_products_fts(db: sqlite3.Connection, query: str, limit: int = 20):
    """Search products using FTS5. Falls back to LIKE if FTS table doesn't exist."""
    results = []
    try:
        rows = db.execute(
            """
            SELECT p.id, p.name AS title, p.description AS snippet, p.category,
                   rank AS score
            FROM products_fts
            JOIN products p ON p.rowid = products_fts.rowid
            WHERE products_fts MATCH ?
            AND p.is_active = 1
            ORDER BY rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
        for row in rows:
            results.append({
                "type": "product",
                "id": row["id"],
                "title": row["title"],
                "snippet": (row["snippet"] or "")[:200],
                "score": row["score"],
            })
    except sqlite3.OperationalError:
        # FTS table may not exist yet; fall back to LIKE
        rows = db.execute(
            """
            SELECT id, name AS title, description AS snippet, category
            FROM products
            WHERE is_active = 1 AND (name LIKE ? OR description LIKE ? OR category LIKE ?)
            LIMIT ?
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


def _search_content_fts(db: sqlite3.Connection, query: str, limit: int = 20):
    """Search content library using FTS5. Falls back to LIKE if FTS table doesn't exist."""
    results = []
    try:
        rows = db.execute(
            """
            SELECT c.id, c.title, c.content AS snippet, c.category,
                   rank AS score
            FROM content_fts
            JOIN content_library c ON c.rowid = content_fts.rowid
            WHERE content_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
        for row in rows:
            results.append({
                "type": "content",
                "id": row["id"],
                "title": row["title"],
                "snippet": (row["snippet"] or "")[:200],
                "score": row["score"],
            })
    except sqlite3.OperationalError:
        # FTS table may not exist; fall back to LIKE
        rows = db.execute(
            """
            SELECT id, title, content AS snippet, category
            FROM content_library
            WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
            LIMIT ?
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


def _search_astrologers(db: sqlite3.Connection, query: str, limit: int = 20):
    """Search astrologers using LIKE on name/bio."""
    results = []
    rows = db.execute(
        """
        SELECT a.id, a.display_name AS title, a.bio AS snippet,
               a.specializations, a.rating
        FROM astrologers a
        WHERE a.is_approved = 1
          AND (a.display_name LIKE ? OR a.bio LIKE ? OR a.specializations LIKE ?)
        LIMIT ?
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
    db: sqlite3.Connection = Depends(get_db),
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
        results.extend(_search_products_fts(db, q))

    if type in ("all", "content"):
        results.extend(_search_content_fts(db, q))

    if type in ("all", "astrologers"):
        results.extend(_search_astrologers(db, q))

    # Sort by score (lower rank = better match for FTS5)
    results.sort(key=lambda r: r["score"])

    return {
        "results": results,
        "total": len(results),
    }
