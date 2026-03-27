"""Public blog routes and sitemap generation for editorial SEO."""
import json
from typing import Any
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.blog_seed import CORE_SITEMAP_PATHS
from app.config import SITE_URL
from app.database import get_db

router = APIRouter(tags=["blog"])


def _normalize_tags(raw_tags: str) -> list[str]:
    try:
        decoded = json.loads(raw_tags or "[]")
        return [str(tag) for tag in decoded]
    except json.JSONDecodeError:
        return []


def _serialize_post(row, include_content: bool = False) -> dict:
    payload = {
        "id": row["id"],
        "slug": row["slug"],
        "title": row["title"],
        "excerpt": row["excerpt"],
        "cover_image_url": row["cover_image_url"],
        "tags": _normalize_tags(row["tags"]),
        "author_name": row["author_name"],
        "seo_title": row["seo_title"],
        "seo_description": row["seo_description"],
        "is_published": bool(row["is_published"]),
        "published_at": row["published_at"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
    if include_content:
        payload["content"] = row["content"]
    return payload


@router.get("/api/blog/posts", status_code=status.HTTP_200_OK)
def list_blog_posts(db: Any = Depends(get_db)):
    """Return published editorial posts for the public blog."""
    rows = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        WHERE is_published = 1
        ORDER BY datetime(published_at) DESC, datetime(created_at) DESC
        """
    ).fetchall()
    items = [_serialize_post(row) for row in rows]
    return {"items": items, "total": len(items)}


@router.get("/api/blog/posts/{slug}", status_code=status.HTTP_200_OK)
def get_blog_post(slug: str, db: Any = Depends(get_db)):
    """Return a single published post by slug."""
    row = db.execute(
        """
        SELECT id, slug, title, excerpt, content, cover_image_url, tags, author_name,
               seo_title, seo_description, is_published, published_at, created_at, updated_at
        FROM blog_posts
        WHERE slug = %s AND is_published = 1
        """,
        (slug,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    return _serialize_post(row, include_content=True)


@router.get("/sitemap.xml", include_in_schema=False)
def dynamic_sitemap(db: Any = Depends(get_db)):
    """Return a runtime sitemap including current published blog posts."""
    base_url = SITE_URL.rstrip("/")
    rows = db.execute(
        """
        SELECT slug, published_at, updated_at
        FROM blog_posts
        WHERE is_published = 1
        ORDER BY datetime(published_at) DESC
        """
    ).fetchall()

    urls: list[str] = []
    for path in CORE_SITEMAP_PATHS:
        urls.append(
            f"  <url>\n"
            f"    <loc>{escape(base_url + path)}</loc>\n"
            f"  </url>"
        )
    for row in rows:
        lastmod = row["updated_at"] or row["published_at"]
        urls.append(
            f"  <url>\n"
            f"    <loc>{escape(base_url + '/blog/' + row['slug'])}</loc>\n"
            f"    <lastmod>{escape((lastmod or '')[:10])}</lastmod>\n"
            f"  </url>"
        )

    xml = (
        '<%sxml version="1.0" encoding="UTF-8"%s>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    return Response(content=xml, media_type="application/xml")
