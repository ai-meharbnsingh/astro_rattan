"""Library routes — Gita chapters/verses and spiritual content library."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db

router = APIRouter(tags=["library"])


# -- Gita -------------------------------------------------------

@router.get("/api/gita/chapters", status_code=status.HTTP_200_OK)
def list_gita_chapters(db: Any = Depends(get_db)):
    """List all Bhagavad Gita chapters with verse counts.
    Contract response: [{chapter, title, verses_count, summary}]
    """
    rows = db.execute(
        """SELECT chapter, COUNT(*) as verses_count, MIN(title) as title
           FROM content_library
           WHERE category = 'gita' AND chapter IS NOT NULL
           GROUP BY chapter
           ORDER BY chapter""",
    ).fetchall()

    if not rows:
        # Return default 18 chapters if DB is empty
        return [
            {"chapter": ch, "title": f"Chapter {ch}", "verses_count": 0, "summary": f"Chapter {ch} of the Bhagavad Gita"}
            for ch in range(1, 19)
        ]

    return [
        {
            "chapter": r["chapter"],
            "title": r["title"] or f"Chapter {r['chapter']}",
            "verses_count": r["verses_count"],
            "summary": f"Chapter {r['chapter']} — {r['title'] or 'Bhagavad Gita'} with {r['verses_count']} verses",
        }
        for r in rows
    ]


@router.get("/api/gita/chapter/{ch}", status_code=status.HTTP_200_OK)
def get_gita_chapter(ch: int, db: Any = Depends(get_db)):
    """Get all verses for a specific Gita chapter.
    Contract response: {chapter, title, verses}
    """
    if ch < 1 or ch > 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter must be between 1 and 18",
        )

    rows = db.execute(
        """SELECT id, chapter, verse, title, sanskrit_text, translation, commentary, content
           FROM content_library
           WHERE category = 'gita' AND chapter = %s
           ORDER BY verse""",
        (ch,),
    ).fetchall()

    # Determine chapter title from first row or default
    chapter_title = f"Chapter {ch}"
    if rows:
        first_title = rows[0]["title"]
        if first_title:
            chapter_title = first_title

    return {
        "chapter": ch,
        "title": chapter_title,
        "verses": [
            {
                "id": r["id"],
                "verse": r["verse"],
                "title": r["title"],
                "sanskrit": r["sanskrit_text"],
                "translation": r["translation"],
                "commentary": r["commentary"],
                "content": r["content"],
            }
            for r in rows
        ],
    }


@router.get("/api/gita/verse/{ch}/{v}", status_code=status.HTTP_200_OK)
def get_gita_verse(ch: int, v: int, db: Any = Depends(get_db)):
    """Get a specific Gita verse by chapter and verse number.
    Contract response: {sanskrit, translation, commentary}
    """
    row = db.execute(
        """SELECT id, chapter, verse, title, sanskrit_text, translation, commentary, content, audio_url
           FROM content_library
           WHERE category = 'gita' AND chapter = %s AND verse = %s""",
        (ch, v),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verse {ch}.{v} not found",
        )

    return {
        "sanskrit": row["sanskrit_text"],
        "translation": row["translation"],
        "commentary": row["commentary"],
    }


# -- Spiritual Content Library ----------------------------------

@router.get("/api/library/item/{item_id}", status_code=status.HTTP_200_OK)
def get_library_item(item_id: str, db: Any = Depends(get_db)):
    """Get a specific library item by ID with full content."""
    row = db.execute(
        """SELECT id, category, title, title_hindi, content, audio_url,
                  chapter, verse, sanskrit_text, translation, commentary, sort_order
           FROM content_library
           WHERE id = %s""",
        (item_id,),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library item not found",
        )

    return {
        "id": row["id"],
        "category": row["category"],
        "title": row["title"],
        "title_hindi": row["title_hindi"],
        "content": row["content"],
        "audio_url": row["audio_url"],
        "chapter": row["chapter"],
        "verse": row["verse"],
        "sanskrit_text": row["sanskrit_text"],
        "translation": row["translation"],
        "commentary": row["commentary"],
    }


@router.get("/api/library/{category}", status_code=status.HTTP_200_OK)
def list_library_items(category: str, db: Any = Depends(get_db)):
    """List all items in a content category.
    Contract response: [{id, title, content_preview}]
    """
    valid_categories = ("gita", "aarti", "mantra", "pooja", "vrat_katha", "chalisa", "festival")
    if category not in valid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}",
        )

    rows = db.execute(
        """SELECT id, title, title_hindi, content
           FROM content_library
           WHERE category = %s
           ORDER BY sort_order, title""",
        (category,),
    ).fetchall()

    return [
        {
            "id": r["id"],
            "title": r["title"],
            "title_hindi": r["title_hindi"],
            "content_preview": (r["content"] or "")[:200],
        }
        for r in rows
    ]
