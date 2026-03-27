"""Referral / Affiliate routes — generate codes, track earnings, apply discounts."""
import secrets
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    ApplyReferralRequest,
    ReferralCode,
    ReferralEarning,
    ReferralStats,
)

router = APIRouter(prefix="/api/referral", tags=["referral"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _generate_unique_code(db: sqlite3.Connection) -> str:
    """Generate a unique 8-character alphanumeric referral code."""
    for _ in range(10):
        code = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8].upper()
        existing = db.execute(
            "SELECT 1 FROM referral_codes WHERE code = ?", (code,)
        ).fetchone()
        if not existing:
            return code
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not generate unique referral code",
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_referral_code(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Generate a unique referral code for the authenticated user.

    Each user may have only one active referral code. If the user already has
    one, the existing code is returned instead of creating a duplicate.
    """
    user_id = current_user["sub"]

    # Check if user already has a code
    existing = db.execute(
        "SELECT code, user_id, discount_percent, commission_percent, uses_count, max_uses, is_active "
        "FROM referral_codes WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if existing:
        return {
            "message": "Referral code already exists",
            "referral_code": ReferralCode(
                code=existing["code"],
                user_id=existing["user_id"],
                discount_percent=existing["discount_percent"],
                commission_percent=existing["commission_percent"],
                uses_count=existing["uses_count"],
                max_uses=existing["max_uses"],
                is_active=bool(existing["is_active"]),
            ).model_dump(),
        }

    code = _generate_unique_code(db)
    db.execute(
        "INSERT INTO referral_codes (code, user_id) VALUES (?, ?)",
        (code, user_id),
    )
    db.commit()

    return {
        "message": "Referral code generated",
        "referral_code": ReferralCode(
            code=code,
            user_id=user_id,
        ).model_dump(),
    }


@router.get("/my-code")
def get_my_referral_code(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Return the authenticated user's referral code, if one exists."""
    user_id = current_user["sub"]
    row = db.execute(
        "SELECT code, user_id, discount_percent, commission_percent, uses_count, max_uses, is_active "
        "FROM referral_codes WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No referral code found. Use POST /api/referral/generate to create one.",
        )

    return {
        "referral_code": ReferralCode(
            code=row["code"],
            user_id=row["user_id"],
            discount_percent=row["discount_percent"],
            commission_percent=row["commission_percent"],
            uses_count=row["uses_count"],
            max_uses=row["max_uses"],
            is_active=bool(row["is_active"]),
        ).model_dump(),
    }


@router.get("/stats", response_model=ReferralStats)
def get_referral_stats(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Return referral statistics for the authenticated user."""
    user_id = current_user["sub"]

    total_referrals = db.execute(
        "SELECT COUNT(DISTINCT referred_id) as cnt FROM referral_earnings WHERE referrer_id = ?",
        (user_id,),
    ).fetchone()["cnt"]

    earnings_row = db.execute(
        "SELECT "
        "  COALESCE(SUM(commission), 0) as total_earnings, "
        "  COALESCE(SUM(CASE WHEN status = 'pending' THEN commission ELSE 0 END), 0) as pending_earnings, "
        "  COALESCE(SUM(CASE WHEN status = 'paid' THEN commission ELSE 0 END), 0) as paid_earnings "
        "FROM referral_earnings WHERE referrer_id = ?",
        (user_id,),
    ).fetchone()

    return ReferralStats(
        total_referrals=total_referrals,
        total_earnings=earnings_row["total_earnings"],
        pending_earnings=earnings_row["pending_earnings"],
        paid_earnings=earnings_row["paid_earnings"],
    )


@router.get("/earnings")
def list_referral_earnings(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all referral earnings for the authenticated user with pagination."""
    user_id = current_user["sub"]
    offset = (page - 1) * per_page

    total = db.execute(
        "SELECT COUNT(*) as cnt FROM referral_earnings WHERE referrer_id = ?",
        (user_id,),
    ).fetchone()["cnt"]

    rows = db.execute(
        "SELECT re.id, re.referrer_id, re.referred_id, re.order_id, re.amount, "
        "  re.commission, re.status, re.created_at, u.name as referred_name "
        "FROM referral_earnings re "
        "LEFT JOIN users u ON u.id = re.referred_id "
        "WHERE re.referrer_id = ? "
        "ORDER BY re.created_at DESC LIMIT ? OFFSET ?",
        (user_id, per_page, offset),
    ).fetchall()

    earnings = []
    for r in rows:
        earning = ReferralEarning(
            id=r["id"],
            referrer_id=r["referrer_id"],
            referred_id=r["referred_id"],
            order_id=r["order_id"],
            amount=r["amount"],
            commission=r["commission"],
            status=r["status"],
        ).model_dump()
        earning["referred_name"] = r["referred_name"]
        earning["created_at"] = r["created_at"]
        earnings.append(earning)

    return {
        "earnings": earnings,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 0,
    }


@router.post("/apply")
def apply_referral_code(
    body: ApplyReferralRequest,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Apply a referral code during/after registration to link the referred user to a referrer.

    This creates the association so that commissions are tracked on the
    referred user's first purchase.
    """
    user_id = current_user["sub"]
    code = body.code.strip().upper()

    # Look up the referral code
    ref_row = db.execute(
        "SELECT id, code, user_id, discount_percent, commission_percent, uses_count, max_uses, is_active "
        "FROM referral_codes WHERE code = ?",
        (code,),
    ).fetchone()

    if not ref_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid referral code")

    if not ref_row["is_active"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Referral code is no longer active")

    if ref_row["max_uses"] is not None and ref_row["uses_count"] >= ref_row["max_uses"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Referral code has reached its maximum uses")

    # Prevent self-referral
    if ref_row["user_id"] == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot use your own referral code")

    # Check if user has already been referred
    already = db.execute(
        "SELECT 1 FROM referral_earnings WHERE referred_id = ?", (user_id,)
    ).fetchone()
    if already:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A referral code has already been applied to your account",
        )

    # Increment uses_count
    db.execute(
        "UPDATE referral_codes SET uses_count = uses_count + 1, updated_at = datetime('now') WHERE id = ?",
        (ref_row["id"],),
    )
    db.commit()

    return {
        "message": "Referral code applied successfully",
        "referrer_id": ref_row["user_id"],
        "discount_percent": ref_row["discount_percent"],
    }


@router.post("/validate/{code}")
def validate_referral_code(
    code: str,
    db: sqlite3.Connection = Depends(get_db),
):
    """Validate whether a referral code exists and is currently active.

    This endpoint does not require authentication so it can be called from
    the registration form before the user has an account.
    """
    code = code.strip().upper()

    ref_row = db.execute(
        "SELECT code, user_id, discount_percent, is_active, uses_count, max_uses "
        "FROM referral_codes WHERE code = ?",
        (code,),
    ).fetchone()

    if not ref_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid referral code")

    if not ref_row["is_active"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Referral code is no longer active")

    if ref_row["max_uses"] is not None and ref_row["uses_count"] >= ref_row["max_uses"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Referral code has reached its maximum uses")

    # Fetch referrer name for display
    referrer = db.execute(
        "SELECT name FROM users WHERE id = ?", (ref_row["user_id"],)
    ).fetchone()

    return {
        "valid": True,
        "code": ref_row["code"],
        "discount_percent": ref_row["discount_percent"],
        "referrer_name": referrer["name"] if referrer else None,
    }
