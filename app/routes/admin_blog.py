"""Admin CRUD routes for editorial blog content."""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import require_role
from app.blog_seed import slugify
from app.database import get_db
from app.models import BlogPostCreate, BlogPostUpdate

router = APIRouter(tags=["admin-blog"])


def _serialize_post(row) -> dict:
    try:
        tags = json.loads(row["tags"] or "[]")
    except json.JSONDecodeError:
        tags = []

    return {
        "id": row["id"],
        "slug": row["slug"],
        "title": row["title"],
        "excerpt": row["excerpt"],
        "content": row["content"],
        "cover_image_url": row["cover_image_url"],
        "tags": tags,
        "author_name": row["author_name"],
        "seo_title": row["seo_title"],
        "seo_description": row["seo_description"],
        "is_published": bool(row["is_published"]),
        "published_at": row["published_at"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _unique_slug(db: Any, desired_slug: str, post_id: str | None = None) -> str:
    base_slug = slugify(desired_slug)
    candidate = base_slug
    counter = 2
    while True:
        row = db.execute(
            "SELECT id FROM blog_posts WHERE slug = %s",
            (candidate,),
        ).fetchone()
        if row is None or row["id"] == post_id:
            return candidate
        candidate = f"{base_slug}-{counter}"
        counter += 1


@router.get("/api/admin/blog")
def list_admin_blog(
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """List all blog posts for admin review."""
    rows = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        ORDER BY datetime(created_at) DESC
        """
    ).fetchall()
    return {"items": [_serialize_post(row) for row in rows]}


@router.post("/api/admin/blog", status_code=status.HTTP_201_CREATED)
def create_blog_post(
    req: BlogPostCreate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Create a blog post with a unique slug."""
    slug = _unique_slug(db, req.slug or req.title)
    cursor = db.execute(
        """
        INSERT INTO blog_posts
            (slug, title, excerpt, content, cover_image_url, tags, author_name,
             seo_title, seo_description, is_published, published_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        RETURNING id
        """,
        (
            slug,
            req.title,
            req.excerpt,
            req.content,
            req.cover_image_url,
            json.dumps(req.tags),
            req.author_name,
            req.seo_title,
            req.seo_description,
            int(req.is_published),
        ),
    )
    new_id = cursor.fetchone()["id"]
    db.commit()
    row = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        WHERE id = %s
        """,
        (new_id,),
    ).fetchone()
    return _serialize_post(row)


@router.patch("/api/admin/blog/{post_id}")
def update_blog_post(
    post_id: str,
    req: BlogPostUpdate,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Update blog post fields."""
    existing = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        WHERE id = %s
        """,
        (post_id,),
    ).fetchone()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    payload = dict(existing)
    updates = req.model_dump(exclude_unset=True)
    if "slug" in updates or "title" in updates:
        payload["slug"] = _unique_slug(db, updates.get("slug") or updates.get("title") or payload["slug"], post_id=post_id)
    if "tags" in updates:
        payload["tags"] = json.dumps(updates["tags"] or [])
    if "is_published" in updates:
        payload["is_published"] = int(bool(updates["is_published"]))
    for field in ("title", "excerpt", "content", "cover_image_url", "author_name", "seo_title", "seo_description"):
        if field in updates:
            payload[field] = updates[field]

    db.execute(
        """
        UPDATE blog_posts
        SET slug = %s, title = %s, excerpt = %s, content = %s, cover_image_url = %s, tags = %s,
            author_name = %s, seo_title = %s, seo_description = %s, is_published = %s,
            updated_at = NOW()
        WHERE id = %s
        """,
        (
            payload["slug"],
            payload["title"],
            payload["excerpt"],
            payload["content"],
            payload["cover_image_url"],
            payload["tags"],
            payload["author_name"],
            payload["seo_title"],
            payload["seo_description"],
            payload["is_published"],
            post_id,
        ),
    )
    db.commit()
    row = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        WHERE id = %s
        """,
        (post_id,),
    ).fetchone()
    return _serialize_post(row)


@router.delete("/api/admin/blog/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(
    post_id: str,
    user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Delete a blog post."""
    existing = db.execute("SELECT id FROM blog_posts WHERE id = %s", (post_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    db.execute("DELETE FROM blog_posts WHERE id = %s", (post_id,))
    db.commit()
    return None
