"""Gamification routes — karma points, streaks, badges, and learning paths."""
import json
import sqlite3
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api", tags=["gamification"])

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POINTS_MAP = {
    "daily_login": 10,
    "kundli_generated": 50,
    "ai_chat": 20,
    "panchang_viewed": 15,
    "shop_purchase": 100,
    "consultation_completed": 200,
    "library_read": 10,
    "prashnavali_used": 25,
    "learning_completed": 50,
}

LEVEL_THRESHOLDS = [0, 100, 300, 600, 1000, 2000, 3500, 5000, 7500, 10000]

ALL_BADGES = [
    {"id": "first_kundli", "name": "First Kundli", "description": "Generated your first birth chart", "icon": "chart"},
    {"id": "ai_explorer", "name": "AI Explorer", "description": "Had your first AI consultation", "icon": "brain"},
    {"id": "panchang_regular", "name": "Panchang Regular", "description": "Viewed Panchang 7 times", "icon": "calendar"},
    {"id": "streak_7", "name": "7-Day Streak", "description": "Logged in 7 days in a row", "icon": "fire"},
    {"id": "streak_30", "name": "30-Day Streak", "description": "Logged in 30 days in a row", "icon": "flame"},
    {"id": "spiritual_scholar", "name": "Spiritual Scholar", "description": "Read 10 library items", "icon": "book"},
    {"id": "shop_champion", "name": "Shop Champion", "description": "Made your first purchase", "icon": "cart"},
    {"id": "consultation_seeker", "name": "Consultation Seeker", "description": "Completed your first consultation", "icon": "users"},
    {"id": "prashnavali_master", "name": "Prashnavali Master", "description": "Used Prashnavali 10 times", "icon": "dice"},
    {"id": "numerology_novice", "name": "Numerology Novice", "description": "Explored numerology readings", "icon": "hash"},
    {"id": "tarot_reader", "name": "Tarot Reader", "description": "Drew your first tarot spread", "icon": "cards"},
    {"id": "cosmic_guru", "name": "Cosmic Guru (Level 10)", "description": "Reached the highest level of cosmic wisdom", "icon": "star"},
]

BADGE_MAP = {b["id"]: b for b in ALL_BADGES}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _calculate_level(total_points: int) -> int:
    """Return level 1-10 based on total points."""
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_points >= threshold:
            level = i + 1
    return min(level, 10)


def _ensure_karma_profile(db: sqlite3.Connection, user_id: str):
    """Create a user_karma row if it doesn't exist yet."""
    existing = db.execute(
        "SELECT 1 FROM user_karma WHERE user_id = ?", (user_id,)
    ).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO user_karma (user_id, total_points, current_streak, longest_streak, level) "
            "VALUES (?, 0, 0, 0, 1)",
            (user_id,),
        )
        db.commit()


def _award_points(
    db: sqlite3.Connection,
    user_id: str,
    action_type: str,
    description: str | None = None,
) -> int:
    """Award points for an action. Returns points awarded."""
    points = POINTS_MAP.get(action_type, 0)
    if points == 0:
        return 0

    _ensure_karma_profile(db, user_id)

    db.execute(
        "INSERT INTO karma_transactions (user_id, points, action_type, description) "
        "VALUES (?, ?, ?, ?)",
        (user_id, points, action_type, description),
    )

    db.execute(
        "UPDATE user_karma SET total_points = total_points + ? WHERE user_id = ?",
        (points, user_id),
    )

    # Recalculate level
    row = db.execute(
        "SELECT total_points FROM user_karma WHERE user_id = ?", (user_id,)
    ).fetchone()
    new_level = _calculate_level(row["total_points"])
    db.execute(
        "UPDATE user_karma SET level = ? WHERE user_id = ?",
        (new_level, user_id),
    )

    db.commit()

    # Check for Cosmic Guru badge at level 10
    if new_level >= 10:
        _try_award_badge(db, user_id, "cosmic_guru")

    return points


def _try_award_badge(db: sqlite3.Connection, user_id: str, badge_id: str) -> bool:
    """Award a badge if not already earned. Returns True if newly awarded."""
    existing = db.execute(
        "SELECT 1 FROM user_badges WHERE user_id = ? AND badge_id = ?",
        (user_id, badge_id),
    ).fetchone()
    if existing:
        return False
    db.execute(
        "INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)",
        (user_id, badge_id),
    )
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Karma Routes
# ---------------------------------------------------------------------------


@router.get("/karma/profile")
def get_karma_profile(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get the authenticated user's karma profile with badges."""
    user_id = current_user["id"]
    _ensure_karma_profile(db, user_id)

    row = db.execute(
        "SELECT * FROM user_karma WHERE user_id = ?", (user_id,)
    ).fetchone()

    earned_badges = db.execute(
        "SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?", (user_id,)
    ).fetchall()
    earned_map = {b["badge_id"]: b["earned_at"] for b in earned_badges}

    badges = []
    for b in ALL_BADGES:
        badges.append({
            **b,
            "earned": b["id"] in earned_map,
            "earned_at": earned_map.get(b["id"]),
        })

    next_level_points = (
        LEVEL_THRESHOLDS[row["level"]]
        if row["level"] < 10
        else LEVEL_THRESHOLDS[-1]
    )

    return {
        "user_id": user_id,
        "total_points": row["total_points"],
        "current_streak": row["current_streak"],
        "longest_streak": row["longest_streak"],
        "last_activity_date": row["last_activity_date"],
        "level": row["level"],
        "next_level_points": next_level_points,
        "badges": badges,
    }


@router.post("/karma/checkin")
def daily_checkin(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Daily check-in: awards points and updates streak."""
    user_id = current_user["id"]
    _ensure_karma_profile(db, user_id)

    today = date.today().isoformat()
    row = db.execute(
        "SELECT * FROM user_karma WHERE user_id = ?", (user_id,)
    ).fetchone()

    last_activity = row["last_activity_date"]

    # Prevent double check-in
    if last_activity == today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in today",
        )

    # Calculate streak
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last_activity == yesterday:
        new_streak = row["current_streak"] + 1
    else:
        new_streak = 1

    longest = max(row["longest_streak"], new_streak)

    db.execute(
        "UPDATE user_karma SET current_streak = ?, longest_streak = ?, last_activity_date = ? "
        "WHERE user_id = ?",
        (new_streak, longest, today, user_id),
    )
    db.commit()

    points = _award_points(db, user_id, "daily_login", "Daily check-in")

    # Streak badges
    if new_streak >= 7:
        _try_award_badge(db, user_id, "streak_7")
    if new_streak >= 30:
        _try_award_badge(db, user_id, "streak_30")

    return {
        "points_awarded": points,
        "current_streak": new_streak,
        "longest_streak": longest,
        "total_points": db.execute(
            "SELECT total_points FROM user_karma WHERE user_id = ?", (user_id,)
        ).fetchone()["total_points"],
    }


@router.get("/karma/transactions")
def list_transactions(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    """List the user's karma point history."""
    user_id = current_user["id"]
    rows = db.execute(
        "SELECT id, user_id, points, action_type, description, created_at "
        "FROM karma_transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user_id, limit, offset),
    ).fetchall()

    return [dict(r) for r in rows]


@router.get("/karma/leaderboard")
def leaderboard(
    db: sqlite3.Connection = Depends(get_db),
):
    """Top 10 users by karma points."""
    rows = db.execute(
        "SELECT uk.user_id, uk.total_points, uk.level, uk.current_streak, u.name "
        "FROM user_karma uk JOIN users u ON uk.user_id = u.id "
        "ORDER BY uk.total_points DESC LIMIT 10"
    ).fetchall()

    return [
        {
            "rank": i + 1,
            "user_id": r["user_id"],
            "name": r["name"],
            "total_points": r["total_points"],
            "level": r["level"],
            "current_streak": r["current_streak"],
        }
        for i, r in enumerate(rows)
    ]


# ---------------------------------------------------------------------------
# Badge Routes
# ---------------------------------------------------------------------------


@router.get("/badges")
def list_badges(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all available badges with earned status for the current user."""
    user_id = current_user["id"]
    earned = db.execute(
        "SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?", (user_id,)
    ).fetchall()
    earned_map = {b["badge_id"]: b["earned_at"] for b in earned}

    return [
        {
            **b,
            "earned": b["id"] in earned_map,
            "earned_at": earned_map.get(b["id"]),
        }
        for b in ALL_BADGES
    ]


# ---------------------------------------------------------------------------
# Learning Routes
# ---------------------------------------------------------------------------


@router.get("/learning/modules")
def list_modules(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
    category: str | None = None,
):
    """List learning path modules with completion status."""
    user_id = current_user["id"]

    if category:
        modules = db.execute(
            "SELECT * FROM learning_modules WHERE category = ? ORDER BY order_index",
            (category,),
        ).fetchall()
    else:
        modules = db.execute(
            "SELECT * FROM learning_modules ORDER BY category, order_index"
        ).fetchall()

    completed = db.execute(
        "SELECT module_id FROM learning_progress WHERE user_id = ?", (user_id,)
    ).fetchall()
    completed_ids = {r["module_id"] for r in completed}

    return [
        {
            "id": m["id"],
            "title": m["title"],
            "description": m["description"],
            "category": m["category"],
            "order_index": m["order_index"],
            "points_reward": m["points_reward"],
            "completed": m["id"] in completed_ids,
        }
        for m in modules
    ]


@router.get("/learning/module/{module_id}")
def get_module(
    module_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get full module content."""
    module = db.execute(
        "SELECT * FROM learning_modules WHERE id = ?", (module_id,)
    ).fetchone()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    completed = db.execute(
        "SELECT 1 FROM learning_progress WHERE user_id = ? AND module_id = ?",
        (current_user["id"], module_id),
    ).fetchone()

    content = module["content_json"]
    try:
        content = json.loads(content) if content else {}
    except json.JSONDecodeError:
        content = {}

    return {
        "id": module["id"],
        "title": module["title"],
        "description": module["description"],
        "category": module["category"],
        "order_index": module["order_index"],
        "content": content,
        "points_reward": module["points_reward"],
        "completed": completed is not None,
    }


@router.post("/learning/complete/{module_id}")
def complete_module(
    module_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Mark a learning module as complete and award points."""
    user_id = current_user["id"]

    module = db.execute(
        "SELECT * FROM learning_modules WHERE id = ?", (module_id,)
    ).fetchone()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    already = db.execute(
        "SELECT 1 FROM learning_progress WHERE user_id = ? AND module_id = ?",
        (user_id, module_id),
    ).fetchone()
    if already:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module already completed",
        )

    db.execute(
        "INSERT INTO learning_progress (user_id, module_id) VALUES (?, ?)",
        (user_id, module_id),
    )
    db.commit()

    points = _award_points(
        db, user_id, "learning_completed",
        f"Completed: {module['title']}",
    )

    # Check for Spiritual Scholar badge (completed 10+ modules)
    total_completed = db.execute(
        "SELECT COUNT(*) as cnt FROM learning_progress WHERE user_id = ?",
        (user_id,),
    ).fetchone()["cnt"]
    if total_completed >= 10:
        _try_award_badge(db, user_id, "spiritual_scholar")

    return {
        "points_awarded": points,
        "module_id": module_id,
        "total_completed": total_completed,
    }
