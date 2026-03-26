"""Admin content management routes — CRUD for spiritual content library."""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.auth import require_role
from app.database import get_db
from app.models import ContentCreate

router = APIRouter()


@router.get("/api/admin/content")
def list_content(
    category: str = Query(None, description="Filter by content category"),
    user: dict = Depends(require_role("admin")),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all content entries with optional category filter."""
    if category:
        rows = db.execute(
            """SELECT id, category, title, title_hindi, content, audio_url,
               chapter, verse, sanskrit_text, translation, commentary, sort_order, created_at
               FROM content_library WHERE category = ? ORDER BY sort_order, created_at DESC""",
            (category,),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT id, category, title, title_hindi, content, audio_url,
               chapter, verse, sanskrit_text, translation, commentary, sort_order, created_at
               FROM content_library ORDER BY sort_order, created_at DESC""",
        ).fetchall()
    return {"items": [dict(r) for r in rows]}


@router.post("/api/admin/content", status_code=status.HTTP_201_CREATED)
def create_content(
    req: ContentCreate,
    user: dict = Depends(require_role("admin")),
    db: sqlite3.Connection = Depends(get_db),
):
    """Create a new spiritual content entry."""
    cursor = db.execute(
        """
        INSERT INTO content_library
            (category, title, title_hindi, content, audio_url,
             chapter, verse, sanskrit_text, translation, commentary, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            req.category.value, req.title, req.title_hindi, req.content,
            req.audio_url, req.chapter, req.verse, req.sanskrit_text,
            req.translation, req.commentary, req.sort_order,
        ),
    )
    rowid = cursor.lastrowid
    content_row = db.execute(
        "SELECT id, category, title, created_at FROM content_library WHERE rowid = ?",
        (rowid,),
    ).fetchone()
    db.commit()

    return dict(content_row)


@router.patch("/api/admin/content/{content_id}")
def update_content(
    content_id: str,
    req: ContentCreate,
    user: dict = Depends(require_role("admin")),
    db: sqlite3.Connection = Depends(get_db),
):
    """Update an existing content entry (full replace of provided fields)."""
    existing = db.execute(
        "SELECT id FROM content_library WHERE id = ?", (content_id,)
    ).fetchone()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )

    db.execute(
        """
        UPDATE content_library SET
            category = ?, title = ?, title_hindi = ?, content = ?,
            audio_url = ?, chapter = ?, verse = ?, sanskrit_text = ?,
            translation = ?, commentary = ?, sort_order = ?
        WHERE id = ?
        """,
        (
            req.category.value, req.title, req.title_hindi, req.content,
            req.audio_url, req.chapter, req.verse, req.sanskrit_text,
            req.translation, req.commentary, req.sort_order, content_id,
        ),
    )
    db.commit()

    updated = db.execute(
        "SELECT * FROM content_library WHERE id = ?", (content_id,)
    ).fetchone()
    return dict(updated)


@router.delete("/api/admin/content/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(
    content_id: str,
    user: dict = Depends(require_role("admin")),
    db: sqlite3.Connection = Depends(get_db),
):
    """Delete a content entry."""
    existing = db.execute(
        "SELECT id FROM content_library WHERE id = ?", (content_id,)
    ).fetchone()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )

    db.execute("DELETE FROM content_library WHERE id = ?", (content_id,))
    db.commit()

    return None
