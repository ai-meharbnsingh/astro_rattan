"""Analytics routes — lightweight page-view tracking and admin reporting."""
from typing import Any, Optional
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from app.auth import require_role
from app.database import get_db
from app.rate_limit import request_rate_limit_key

router = APIRouter(tags=["analytics"])
limiter = Limiter(key_func=request_rate_limit_key)


class HitPayload(BaseModel):
    path: str = Field(max_length=200)
    session_id: str = Field(max_length=64)
    referrer: Optional[str] = Field(default=None, max_length=500)
    user_id: Optional[str] = Field(default=None, max_length=64)


@router.post("/api/analytics/hit", status_code=204)
@limiter.limit("10/minute")
def record_hit(
    payload: HitPayload,
    request: Request,
    db: Any = Depends(get_db),
):
    """Record a single page view from the frontend SPA.
    No auth required — called client-side on every route change.
    Rate limited to 10/minute per IP to prevent spam."""
    path = payload.path or "/"
    if not path.startswith("/"):
        path = "/" + path
    referrer = payload.referrer or None

    db.execute(
        """INSERT INTO page_views (path, session_id, user_id, referrer)
           VALUES (%s, %s, %s, %s)""",
        (path, payload.session_id, payload.user_id, referrer),
    )
    db.commit()


@router.get("/api/admin/analytics")
def get_analytics(
    current_user: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    """Aggregated traffic analytics for the admin panel."""
    # Total all-time
    total_views = db.execute("SELECT COUNT(*) as c FROM page_views").fetchone()["c"]
    total_sessions = db.execute("SELECT COUNT(DISTINCT session_id) as c FROM page_views").fetchone()["c"]

    # Today
    today_views = db.execute(
        "SELECT COUNT(*) as c FROM page_views WHERE created_at >= CURRENT_DATE"
    ).fetchone()["c"]
    today_sessions = db.execute(
        "SELECT COUNT(DISTINCT session_id) as c FROM page_views WHERE created_at >= CURRENT_DATE"
    ).fetchone()["c"]

    # This week (Mon–Sun)
    week_views = db.execute(
        "SELECT COUNT(*) as c FROM page_views WHERE created_at >= date_trunc('week', NOW())"
    ).fetchone()["c"]
    week_sessions = db.execute(
        "SELECT COUNT(DISTINCT session_id) as c FROM page_views WHERE created_at >= date_trunc('week', NOW())"
    ).fetchone()["c"]

    # This month
    month_views = db.execute(
        "SELECT COUNT(*) as c FROM page_views WHERE created_at >= date_trunc('month', NOW())"
    ).fetchone()["c"]

    # Top pages — last 30 days
    top_pages = db.execute(
        """SELECT path, COUNT(*) as views, COUNT(DISTINCT session_id) as visitors
           FROM page_views
           WHERE created_at >= NOW() - INTERVAL '30 days'
           GROUP BY path
           ORDER BY views DESC
           LIMIT 15"""
    ).fetchall()

    # Hourly traffic — today (0–23)
    hourly = db.execute(
        """SELECT EXTRACT(HOUR FROM created_at)::int as hour, COUNT(*) as views
           FROM page_views
           WHERE created_at >= CURRENT_DATE
           GROUP BY hour
           ORDER BY hour"""
    ).fetchall()
    hourly_map = {row["hour"]: row["views"] for row in hourly}
    hourly_today = [{"hour": h, "views": hourly_map.get(h, 0)} for h in range(24)]

    # Daily traffic — last 30 days
    daily = db.execute(
        """SELECT DATE(created_at) as day, COUNT(*) as views, COUNT(DISTINCT session_id) as visitors
           FROM page_views
           WHERE created_at >= NOW() - INTERVAL '30 days'
           GROUP BY day
           ORDER BY day"""
    ).fetchall()

    return {
        "total_views": total_views,
        "total_sessions": total_sessions,
        "today_views": today_views,
        "today_sessions": today_sessions,
        "week_views": week_views,
        "week_sessions": week_sessions,
        "month_views": month_views,
        "top_pages": [dict(r) for r in top_pages],
        "hourly_today": hourly_today,
        "daily_last_30": [
            {"day": str(r["day"]), "views": r["views"], "visitors": r["visitors"]}
            for r in daily
        ],
    }
