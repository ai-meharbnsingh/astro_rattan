"""Community Forum routes — categories, threads, replies, likes, search."""
import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    ForumCategory,
    ThreadCreate,
    ThreadResponse,
    ReplyCreate,
    ReplyResponse,
)

router = APIRouter(prefix="/api/forum", tags=["forum"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _optional_user(
    db: sqlite3.Connection = Depends(get_db),
):
    """Return None — used as a placeholder; real optional auth handled inline."""
    return None


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

@router.get("/categories")
def list_categories(
    db: sqlite3.Connection = Depends(get_db),
):
    """List all active forum categories with thread counts."""
    rows = db.execute(
        """
        SELECT c.*, COALESCE(t.cnt, 0) AS thread_count
        FROM forum_categories c
        LEFT JOIN (
            SELECT category_id, COUNT(*) AS cnt FROM forum_threads GROUP BY category_id
        ) t ON t.category_id = c.id
        WHERE c.is_active = 1
        ORDER BY c.order_index
        """
    ).fetchall()
    return [
        ForumCategory(
            id=r["id"],
            name=r["name"],
            description=r["description"],
            icon=r["icon"],
            order_index=r["order_index"],
            is_active=bool(r["is_active"]),
            thread_count=r["thread_count"],
        )
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Threads
# ---------------------------------------------------------------------------

@router.get("/threads")
def list_threads(
    category_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db),
):
    """List threads optionally filtered by category, paginated, newest first.
    Pinned threads always come first."""
    offset = (page - 1) * per_page
    params: list = []
    where = ""
    if category_id:
        where = "WHERE ft.category_id = ?"
        params.append(category_id)

    # Total count
    count_row = db.execute(
        f"SELECT COUNT(*) FROM forum_threads ft {where}", params
    ).fetchone()
    total = count_row[0] if count_row else 0

    rows = db.execute(
        f"""
        SELECT ft.*, u.name AS author_name, u.avatar_url AS author_avatar,
               fc.name AS category_name
        FROM forum_threads ft
        JOIN users u ON u.id = ft.user_id
        JOIN forum_categories fc ON fc.id = ft.category_id
        {where}
        ORDER BY ft.is_pinned DESC, ft.updated_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [per_page, offset],
    ).fetchall()

    threads = [
        ThreadResponse(
            id=r["id"],
            category_id=r["category_id"],
            user_id=r["user_id"],
            title=r["title"],
            content=r["content"],
            is_pinned=bool(r["is_pinned"]),
            is_locked=bool(r["is_locked"]),
            views_count=r["views_count"],
            replies_count=r["replies_count"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            author_name=r["author_name"],
            author_avatar=r["author_avatar"],
            category_name=r["category_name"],
        )
        for r in rows
    ]
    return {"threads": threads, "total": total, "page": page, "per_page": per_page}


# ---------------------------------------------------------------------------
# Single Thread
# ---------------------------------------------------------------------------

@router.get("/thread/{thread_id}")
def get_thread(
    thread_id: str,
    db: sqlite3.Connection = Depends(get_db),
):
    """Get a single thread with all its replies. Increments view count."""
    row = db.execute(
        """
        SELECT ft.*, u.name AS author_name, u.avatar_url AS author_avatar,
               fc.name AS category_name
        FROM forum_threads ft
        JOIN users u ON u.id = ft.user_id
        JOIN forum_categories fc ON fc.id = ft.category_id
        WHERE ft.id = ?
        """,
        (thread_id,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Increment views
    db.execute(
        "UPDATE forum_threads SET views_count = views_count + 1 WHERE id = ?",
        (thread_id,),
    )
    db.commit()

    thread = ThreadResponse(
        id=row["id"],
        category_id=row["category_id"],
        user_id=row["user_id"],
        title=row["title"],
        content=row["content"],
        is_pinned=bool(row["is_pinned"]),
        is_locked=bool(row["is_locked"]),
        views_count=row["views_count"] + 1,
        replies_count=row["replies_count"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        author_name=row["author_name"],
        author_avatar=row["author_avatar"],
        category_name=row["category_name"],
    )

    reply_rows = db.execute(
        """
        SELECT fr.*, u.name AS author_name, u.avatar_url AS author_avatar
        FROM forum_replies fr
        JOIN users u ON u.id = fr.user_id
        WHERE fr.thread_id = ?
        ORDER BY fr.is_best_answer DESC, fr.created_at ASC
        """,
        (thread_id,),
    ).fetchall()

    replies = [
        ReplyResponse(
            id=r["id"],
            thread_id=r["thread_id"],
            user_id=r["user_id"],
            content=r["content"],
            is_best_answer=bool(r["is_best_answer"]),
            likes_count=r["likes_count"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            author_name=r["author_name"],
            author_avatar=r["author_avatar"],
        )
        for r in reply_rows
    ]

    return {"thread": thread, "replies": replies}


# ---------------------------------------------------------------------------
# Create Thread
# ---------------------------------------------------------------------------

@router.post("/thread", status_code=status.HTTP_201_CREATED)
def create_thread(
    body: ThreadCreate,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Create a new forum thread (auth required)."""
    # Verify category exists
    cat = db.execute(
        "SELECT id FROM forum_categories WHERE id = ? AND is_active = 1",
        (body.category_id,),
    ).fetchone()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    cursor = db.execute(
        """
        INSERT INTO forum_threads (category_id, user_id, title, content)
        VALUES (?, ?, ?, ?)
        """,
        (body.category_id, current_user["id"], body.title, body.content),
    )
    db.commit()

    thread_id = cursor.lastrowid
    # Fetch the created thread by rowid
    row = db.execute(
        """
        SELECT ft.*, u.name AS author_name, u.avatar_url AS author_avatar,
               fc.name AS category_name
        FROM forum_threads ft
        JOIN users u ON u.id = ft.user_id
        JOIN forum_categories fc ON fc.id = ft.category_id
        WHERE ft.rowid = ?
        """,
        (thread_id,),
    ).fetchone()

    return ThreadResponse(
        id=row["id"],
        category_id=row["category_id"],
        user_id=row["user_id"],
        title=row["title"],
        content=row["content"],
        is_pinned=bool(row["is_pinned"]),
        is_locked=bool(row["is_locked"]),
        views_count=row["views_count"],
        replies_count=row["replies_count"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        author_name=row["author_name"],
        author_avatar=row["author_avatar"],
        category_name=row["category_name"],
    )


# ---------------------------------------------------------------------------
# Reply to Thread
# ---------------------------------------------------------------------------

@router.post("/thread/{thread_id}/reply", status_code=status.HTTP_201_CREATED)
def create_reply(
    thread_id: str,
    body: ReplyCreate,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Add a reply to a thread (auth required)."""
    thread = db.execute(
        "SELECT id, is_locked FROM forum_threads WHERE id = ?", (thread_id,)
    ).fetchone()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if thread["is_locked"]:
        raise HTTPException(status_code=403, detail="Thread is locked")

    cursor = db.execute(
        "INSERT INTO forum_replies (thread_id, user_id, content) VALUES (?, ?, ?)",
        (thread_id, current_user["id"], body.content),
    )
    db.execute(
        """
        UPDATE forum_threads
        SET replies_count = replies_count + 1, updated_at = datetime('now')
        WHERE id = ?
        """,
        (thread_id,),
    )
    db.commit()

    row = db.execute(
        """
        SELECT fr.*, u.name AS author_name, u.avatar_url AS author_avatar
        FROM forum_replies fr
        JOIN users u ON u.id = fr.user_id
        WHERE fr.rowid = ?
        """,
        (cursor.lastrowid,),
    ).fetchone()

    return ReplyResponse(
        id=row["id"],
        thread_id=row["thread_id"],
        user_id=row["user_id"],
        content=row["content"],
        is_best_answer=bool(row["is_best_answer"]),
        likes_count=row["likes_count"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        author_name=row["author_name"],
        author_avatar=row["author_avatar"],
    )


# ---------------------------------------------------------------------------
# Like / Unlike Reply
# ---------------------------------------------------------------------------

@router.post("/reply/{reply_id}/like")
def toggle_like(
    reply_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Toggle like on a reply (auth required). Returns new like state."""
    reply = db.execute(
        "SELECT id FROM forum_replies WHERE id = ?", (reply_id,)
    ).fetchone()
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    existing = db.execute(
        "SELECT id FROM forum_likes WHERE user_id = ? AND reply_id = ?",
        (current_user["id"], reply_id),
    ).fetchone()

    if existing:
        db.execute("DELETE FROM forum_likes WHERE id = ?", (existing["id"],))
        db.execute(
            "UPDATE forum_replies SET likes_count = MAX(likes_count - 1, 0) WHERE id = ?",
            (reply_id,),
        )
        db.commit()
        return {"liked": False}
    else:
        db.execute(
            "INSERT INTO forum_likes (user_id, reply_id) VALUES (?, ?)",
            (current_user["id"], reply_id),
        )
        db.execute(
            "UPDATE forum_replies SET likes_count = likes_count + 1 WHERE id = ?",
            (reply_id,),
        )
        db.commit()
        return {"liked": True}


# ---------------------------------------------------------------------------
# Best Answer
# ---------------------------------------------------------------------------

@router.post("/reply/{reply_id}/best-answer")
def mark_best_answer(
    reply_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Mark/unmark a reply as best answer (thread owner only)."""
    reply = db.execute(
        "SELECT fr.*, ft.user_id AS thread_owner_id FROM forum_replies fr JOIN forum_threads ft ON ft.id = fr.thread_id WHERE fr.id = ?",
        (reply_id,),
    ).fetchone()
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")
    if reply["thread_owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Only the thread owner can mark best answer")

    new_state = 0 if reply["is_best_answer"] else 1

    # Clear any existing best answer on this thread, then set new one
    db.execute(
        "UPDATE forum_replies SET is_best_answer = 0 WHERE thread_id = ?",
        (reply["thread_id"],),
    )
    if new_state:
        db.execute(
            "UPDATE forum_replies SET is_best_answer = 1 WHERE id = ?",
            (reply_id,),
        )
    db.commit()

    return {"is_best_answer": bool(new_state)}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

@router.get("/search")
def search_threads(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db),
):
    """Search threads by title or content."""
    offset = (page - 1) * per_page
    like = f"%{q}%"

    count_row = db.execute(
        "SELECT COUNT(*) FROM forum_threads WHERE title LIKE ? OR content LIKE ?",
        (like, like),
    ).fetchone()
    total = count_row[0] if count_row else 0

    rows = db.execute(
        """
        SELECT ft.*, u.name AS author_name, u.avatar_url AS author_avatar,
               fc.name AS category_name
        FROM forum_threads ft
        JOIN users u ON u.id = ft.user_id
        JOIN forum_categories fc ON fc.id = ft.category_id
        WHERE ft.title LIKE ? OR ft.content LIKE ?
        ORDER BY ft.updated_at DESC
        LIMIT ? OFFSET ?
        """,
        (like, like, per_page, offset),
    ).fetchall()

    threads = [
        ThreadResponse(
            id=r["id"],
            category_id=r["category_id"],
            user_id=r["user_id"],
            title=r["title"],
            content=r["content"],
            is_pinned=bool(r["is_pinned"]),
            is_locked=bool(r["is_locked"]),
            views_count=r["views_count"],
            replies_count=r["replies_count"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            author_name=r["author_name"],
            author_avatar=r["author_avatar"],
            category_name=r["category_name"],
        )
        for r in rows
    ]
    return {"threads": threads, "total": total, "page": page, "per_page": per_page}
