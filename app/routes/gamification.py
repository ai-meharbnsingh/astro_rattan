"""Gamification routes — karma points, streaks, badges, and learning paths."""
import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.database import get_db
from app.models import Badge, KarmaTransaction, LearningModule

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

BADGES = [
    {"id": "first_kundli", "name": "First Kundli", "description": "Generated your first birth chart", "icon": "scroll"},
    {"id": "ai_explorer", "name": "AI Explorer", "description": "Had your first AI astrology chat", "icon": "bot"},
    {"id": "panchang_regular", "name": "Panchang Regular", "description": "Viewed Panchang 10 times", "icon": "calendar"},
    {"id": "streak_7", "name": "7-Day Streak", "description": "Logged in for 7 consecutive days", "icon": "flame"},
    {"id": "streak_30", "name": "30-Day Streak", "description": "Logged in for 30 consecutive days", "icon": "fire"},
    {"id": "spiritual_scholar", "name": "Spiritual Scholar", "description": "Completed 5 learning modules", "icon": "book-open"},
    {"id": "shop_champion", "name": "Shop Champion", "description": "Made your first purchase", "icon": "shopping-bag"},
    {"id": "consultation_seeker", "name": "Consultation Seeker", "description": "Completed your first consultation", "icon": "phone"},
    {"id": "prashnavali_master", "name": "Prashnavali Master", "description": "Used Prashnavali 10 times", "icon": "sparkles"},
    {"id": "numerology_novice", "name": "Numerology Novice", "description": "Explored numerology readings", "icon": "hash"},
    {"id": "tarot_reader", "name": "Tarot Reader", "description": "Drew your first tarot spread", "icon": "layers"},
    {"id": "cosmic_guru", "name": "Cosmic Guru (Level 10)", "description": "Reached the highest karma level", "icon": "crown"},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _calculate_level(total_points: int) -> int:
    """Return the level (1-10) based on total karma points."""
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_points >= threshold:
            level = i + 1
    return min(level, 10)


def _ensure_karma_row(db: sqlite3.Connection, user_id: str):
    """Create a user_karma row if it doesn't exist yet."""
    existing = db.execute("SELECT 1 FROM user_karma WHERE user_id = ?", (user_id,)).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO user_karma (user_id, total_points, current_streak, longest_streak, level) "
            "VALUES (?, 0, 0, 0, 1)",
            (user_id,),
        )
        db.commit()


def _award_points(db: sqlite3.Connection, user_id: str, action_type: str, description: str | None = None):
    """Award karma points for an action, update level, and return the new totals."""
    _ensure_karma_row(db, user_id)
    points = POINTS_MAP.get(action_type, 0)
    if points == 0:
        return

    # Insert transaction
    db.execute(
        "INSERT INTO karma_transactions (user_id, points, action_type, description) VALUES (?, ?, ?, ?)",
        (user_id, points, action_type, description),
    )

    # Update total & level
    db.execute(
        "UPDATE user_karma SET total_points = total_points + ?, "
        "last_activity_date = date('now') WHERE user_id = ?",
        (points, user_id),
    )
    db.commit()

    # Recalculate level
    row = db.execute("SELECT total_points FROM user_karma WHERE user_id = ?", (user_id,)).fetchone()
    new_level = _calculate_level(row["total_points"])
    db.execute("UPDATE user_karma SET level = ? WHERE user_id = ?", (new_level, user_id))
    db.commit()

    # Check badge for cosmic guru
    if new_level >= 10:
        _try_award_badge(db, user_id, "cosmic_guru")


def _try_award_badge(db: sqlite3.Connection, user_id: str, badge_id: str):
    """Award a badge if the user doesn't already have it."""
    existing = db.execute(
        "SELECT 1 FROM user_badges WHERE user_id = ? AND badge_id = ?",
        (user_id, badge_id),
    ).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)",
            (user_id, badge_id),
        )
        db.commit()


def _check_action_badges(db: sqlite3.Connection, user_id: str):
    """Evaluate and award action-based badges by checking transaction history."""
    counts: dict[str, int] = {}
    rows = db.execute(
        "SELECT action_type, COUNT(*) as cnt FROM karma_transactions WHERE user_id = ? GROUP BY action_type",
        (user_id,),
    ).fetchall()
    for r in rows:
        counts[r["action_type"]] = r["cnt"]

    if counts.get("kundli_generated", 0) >= 1:
        _try_award_badge(db, user_id, "first_kundli")
    if counts.get("ai_chat", 0) >= 1:
        _try_award_badge(db, user_id, "ai_explorer")
    if counts.get("panchang_viewed", 0) >= 10:
        _try_award_badge(db, user_id, "panchang_regular")
    if counts.get("shop_purchase", 0) >= 1:
        _try_award_badge(db, user_id, "shop_champion")
    if counts.get("consultation_completed", 0) >= 1:
        _try_award_badge(db, user_id, "consultation_seeker")
    if counts.get("prashnavali_used", 0) >= 10:
        _try_award_badge(db, user_id, "prashnavali_master")

    # Learning modules completed
    completed_modules = db.execute(
        "SELECT COUNT(*) as cnt FROM learning_progress WHERE user_id = ?", (user_id,)
    ).fetchone()["cnt"]
    if completed_modules >= 5:
        _try_award_badge(db, user_id, "spiritual_scholar")

    # Streak badges
    karma_row = db.execute(
        "SELECT longest_streak FROM user_karma WHERE user_id = ?", (user_id,)
    ).fetchone()
    if karma_row:
        if karma_row["longest_streak"] >= 7:
            _try_award_badge(db, user_id, "streak_7")
        if karma_row["longest_streak"] >= 30:
            _try_award_badge(db, user_id, "streak_30")


# ---------------------------------------------------------------------------
# Routes — Karma
# ---------------------------------------------------------------------------

@router.get("/karma/profile")
def get_karma_profile(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get the authenticated user's karma profile including points, streak, level, and badges."""
    user_id = current_user["sub"]
    _ensure_karma_row(db, user_id)

    row = db.execute(
        "SELECT user_id, total_points, current_streak, longest_streak, last_activity_date, level, created_at "
        "FROM user_karma WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    # Fetch earned badges
    earned_rows = db.execute(
        "SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?", (user_id,)
    ).fetchall()
    earned_map = {r["badge_id"]: r["earned_at"] for r in earned_rows}

    badges = []
    for b in BADGES:
        badges.append({
            "id": b["id"],
            "name": b["name"],
            "description": b["description"],
            "icon": b["icon"],
            "earned": b["id"] in earned_map,
            "earned_at": earned_map.get(b["id"]),
        })

    return {
        "user_id": row["user_id"],
        "total_points": row["total_points"],
        "current_streak": row["current_streak"],
        "longest_streak": row["longest_streak"],
        "last_activity_date": row["last_activity_date"],
        "level": row["level"],
        "badges": badges,
        "next_level_points": LEVEL_THRESHOLDS[row["level"]] if row["level"] < 10 else None,
    }


@router.post("/karma/checkin")
def daily_checkin(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Daily check-in: awards points and updates the login streak."""
    user_id = current_user["sub"]
    _ensure_karma_row(db, user_id)
    today = date.today().isoformat()

    row = db.execute(
        "SELECT last_activity_date, current_streak, longest_streak FROM user_karma WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    last_date = row["last_activity_date"]
    current_streak = row["current_streak"]
    longest_streak = row["longest_streak"]

    # Already checked in today
    if last_date == today:
        return {
            "message": "Already checked in today",
            "points_awarded": 0,
            "current_streak": current_streak,
            "total_points": db.execute(
                "SELECT total_points FROM user_karma WHERE user_id = ?", (user_id,)
            ).fetchone()["total_points"],
        }

    # Calculate streak
    if last_date:
        last = date.fromisoformat(last_date)
        diff = (date.today() - last).days
        if diff == 1:
            current_streak += 1
        else:
            current_streak = 1
    else:
        current_streak = 1

    if current_streak > longest_streak:
        longest_streak = current_streak

    # Update streak
    db.execute(
        "UPDATE user_karma SET current_streak = ?, longest_streak = ?, last_activity_date = ? WHERE user_id = ?",
        (current_streak, longest_streak, today, user_id),
    )
    db.commit()

    # Award points
    _award_points(db, user_id, "daily_login", "Daily check-in")

    # Check streak badges
    _check_action_badges(db, user_id)

    total = db.execute("SELECT total_points FROM user_karma WHERE user_id = ?", (user_id,)).fetchone()["total_points"]

    return {
        "message": "Check-in successful!",
        "points_awarded": POINTS_MAP["daily_login"],
        "current_streak": current_streak,
        "total_points": total,
    }


@router.get("/karma/transactions")
def list_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List the authenticated user's karma point history with pagination."""
    user_id = current_user["sub"]
    offset = (page - 1) * per_page

    total = db.execute(
        "SELECT COUNT(*) as cnt FROM karma_transactions WHERE user_id = ?", (user_id,)
    ).fetchone()["cnt"]

    rows = db.execute(
        "SELECT id, user_id, points, action_type, description, created_at "
        "FROM karma_transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user_id, per_page, offset),
    ).fetchall()

    transactions = [
        KarmaTransaction(
            id=r["id"], user_id=r["user_id"], points=r["points"],
            action_type=r["action_type"], description=r["description"],
            created_at=r["created_at"],
        ).model_dump()
        for r in rows
    ]

    return {
        "transactions": transactions,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 0,
    }


@router.get("/karma/leaderboard")
def get_leaderboard(
    db: sqlite3.Connection = Depends(get_db),
):
    """Return top 10 users by karma points."""
    rows = db.execute(
        "SELECT uk.user_id, uk.total_points, uk.level, uk.current_streak, u.name "
        "FROM user_karma uk "
        "JOIN users u ON u.id = uk.user_id "
        "ORDER BY uk.total_points DESC LIMIT 10",
    ).fetchall()

    leaderboard = []
    for rank, r in enumerate(rows, 1):
        leaderboard.append({
            "rank": rank,
            "user_id": r["user_id"],
            "name": r["name"],
            "total_points": r["total_points"],
            "level": r["level"],
            "current_streak": r["current_streak"],
        })

    return {"leaderboard": leaderboard}


# ---------------------------------------------------------------------------
# Routes — Badges
# ---------------------------------------------------------------------------

@router.get("/badges")
def list_badges(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all available badges with earned status for the authenticated user."""
    user_id = current_user["sub"]

    # Re-evaluate badges
    _check_action_badges(db, user_id)

    earned_rows = db.execute(
        "SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?", (user_id,)
    ).fetchall()
    earned_map = {r["badge_id"]: r["earned_at"] for r in earned_rows}

    badges = []
    for b in BADGES:
        badges.append(Badge(
            id=b["id"],
            name=b["name"],
            description=b["description"],
            icon=b["icon"],
            earned=b["id"] in earned_map,
            earned_at=earned_map.get(b["id"]),
        ).model_dump())

    return {"badges": badges}


# ---------------------------------------------------------------------------
# Routes — Learning Paths
# ---------------------------------------------------------------------------

@router.get("/learning/modules")
def list_learning_modules(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all learning path modules with completion status."""
    user_id = current_user["sub"]

    rows = db.execute(
        "SELECT id, title, description, category, order_index, content_json, points_reward "
        "FROM learning_modules ORDER BY order_index ASC",
    ).fetchall()

    # Completed module IDs
    completed_rows = db.execute(
        "SELECT module_id FROM learning_progress WHERE user_id = ?", (user_id,)
    ).fetchall()
    completed_ids = {r["module_id"] for r in completed_rows}

    modules = []
    for r in rows:
        modules.append(LearningModule(
            id=r["id"],
            title=r["title"],
            description=r["description"],
            category=r["category"],
            order_index=r["order_index"],
            content_json=r["content_json"],
            points_reward=r["points_reward"],
            completed=r["id"] in completed_ids,
        ).model_dump())

    return {"modules": modules, "total_completed": len(completed_ids), "total_modules": len(rows)}


@router.get("/learning/module/{module_id}")
def get_learning_module(
    module_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get a specific learning module's content."""
    user_id = current_user["sub"]

    row = db.execute(
        "SELECT id, title, description, category, order_index, content_json, points_reward "
        "FROM learning_modules WHERE id = ?",
        (module_id,),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning module not found")

    completed = db.execute(
        "SELECT 1 FROM learning_progress WHERE user_id = ? AND module_id = ?",
        (user_id, module_id),
    ).fetchone()

    return LearningModule(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        category=row["category"],
        order_index=row["order_index"],
        content_json=row["content_json"],
        points_reward=row["points_reward"],
        completed=completed is not None,
    ).model_dump()


@router.post("/learning/complete/{module_id}")
def complete_learning_module(
    module_id: str,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Mark a learning module as complete and award karma points."""
    user_id = current_user["sub"]

    # Verify module exists
    module = db.execute(
        "SELECT id, title, points_reward FROM learning_modules WHERE id = ?", (module_id,)
    ).fetchone()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning module not found")

    # Check if already completed
    already = db.execute(
        "SELECT 1 FROM learning_progress WHERE user_id = ? AND module_id = ?",
        (user_id, module_id),
    ).fetchone()
    if already:
        return {"message": "Module already completed", "points_awarded": 0}

    # Mark complete
    db.execute(
        "INSERT INTO learning_progress (user_id, module_id) VALUES (?, ?)",
        (user_id, module_id),
    )
    db.commit()

    # Award points
    _award_points(db, user_id, "learning_completed", f"Completed: {module['title']}")

    # Check badges
    _check_action_badges(db, user_id)

    return {
        "message": "Module completed! Points awarded.",
        "points_awarded": module["points_reward"],
    }
