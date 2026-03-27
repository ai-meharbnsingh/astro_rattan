"""Auth routes — register, login, get current user, profile management."""
import json
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from slowapi import Limiter

from app.auth import hash_password, verify_password, create_token, get_current_user
from app.database import get_db
from app.email_service import send_registration_welcome
from app.models import (
    UserRegister,
    LoginRequest,
    UserResponse,
    TokenResponse,
    UserProfileUpdate,
    ChangePasswordRequest,
)

from app.config import LOGIN_RATE_LIMIT
from app.rate_limit import request_rate_limit_key

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Rate limiter instance — shares config with main app limiter
limiter = Limiter(key_func=request_rate_limit_key)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register(
    body: UserRegister,
    background_tasks: BackgroundTasks,
    db: Any = Depends(get_db),
):
    """Register a new user account."""
    # Check if email already exists
    row = db.execute("SELECT id FROM users WHERE email = %s", (body.email,)).fetchone()
    if row:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    pw_hash = hash_password(body.password)
    db.execute(
        """INSERT INTO users (email, password_hash, name, phone, date_of_birth, gender, city)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (body.email, pw_hash, body.name, body.phone, body.date_of_birth, body.gender, body.city),
    )
    db.commit()

    user_row = db.execute(
        """SELECT id, email, name, role, phone, date_of_birth, gender, city, avatar_url, created_at
           FROM users WHERE email = %s""",
        (body.email,),
    ).fetchone()

    user = UserResponse(
        id=user_row["id"],
        email=user_row["email"],
        name=user_row["name"],
        role=user_row["role"],
        phone=user_row["phone"],
        date_of_birth=user_row["date_of_birth"],
        gender=user_row["gender"],
        city=user_row["city"],
        avatar_url=user_row["avatar_url"],
        created_at=user_row["created_at"],
    )
    token = create_token({"sub": user.id, "email": user.email, "role": user.role})
    background_tasks.add_task(send_registration_welcome, body.name, body.email)
    return TokenResponse(user=user, token=token)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
@limiter.limit(LOGIN_RATE_LIMIT)
def login(request: Request, body: LoginRequest, db: Any = Depends(get_db)):
    """Authenticate and return JWT token."""
    row = db.execute(
        """SELECT id, email, password_hash, name, role, phone, date_of_birth, gender, city,
                  avatar_url, created_at, is_active
           FROM users WHERE email = %s""",
        (body.email,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Reject deactivated users
    if row["is_active"] is not None and not row["is_active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

    user = UserResponse(
        id=row["id"],
        email=row["email"],
        name=row["name"],
        role=row["role"],
        phone=row["phone"],
        date_of_birth=row["date_of_birth"],
        gender=row["gender"],
        city=row["city"],
        avatar_url=row["avatar_url"],
        created_at=row["created_at"],
    )
    token = create_token({"sub": user.id, "email": user.email, "role": user.role})
    return TokenResponse(user=user, token=token)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_me(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the currently authenticated user's profile."""
    row = db.execute(
        """SELECT id, email, name, role, phone, date_of_birth, gender, city, avatar_url, created_at
           FROM users WHERE id = %s""",
        (current_user["sub"],),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=row["id"],
        email=row["email"],
        name=row["name"],
        role=row["role"],
        phone=row["phone"],
        date_of_birth=row["date_of_birth"],
        gender=row["gender"],
        city=row["city"],
        avatar_url=row["avatar_url"],
        created_at=row["created_at"],
    )


@router.patch("/profile", status_code=status.HTTP_200_OK)
def update_profile(
    body: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Update the current user's profile (name, phone, DOB, gender, city, avatar)."""
    user_id = current_user["sub"]

    updates = []
    params = []

    if body.name is not None:
        updates.append("name = %s")
        params.append(body.name)
    if body.phone is not None:
        updates.append("phone = %s")
        params.append(body.phone)
    if body.date_of_birth is not None:
        updates.append("date_of_birth = %s")
        params.append(body.date_of_birth)
    if body.gender is not None:
        if body.gender not in ("male", "female", "other"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="gender must be male, female, or other",
            )
        updates.append("gender = %s")
        params.append(body.gender)
    if body.city is not None:
        updates.append("city = %s")
        params.append(body.city)
    if body.avatar_url is not None:
        updates.append("avatar_url = %s")
        params.append(body.avatar_url)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    updates.append("updated_at = to_char(NOW(), 'YYYY-MM-DD\"T\"HH24:MI:SS')")
    params.append(user_id)

    db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", params)
    db.commit()

    row = db.execute(
        """SELECT id, email, name, role, phone, avatar_url,
                  date_of_birth, gender, city, is_active, created_at, updated_at
           FROM users WHERE id = %s""",
        (user_id,),
    ).fetchone()

    return dict(row)


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    body: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Change the current user's password."""
    user_id = current_user["sub"]

    row = db.execute(
        "SELECT password_hash FROM users WHERE id = %s", (user_id,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(body.current_password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect"
        )

    new_hash = hash_password(body.new_password)
    db.execute(
        "UPDATE users SET password_hash = %s, updated_at = to_char(NOW(), 'YYYY-MM-DD\"T\"HH24:MI:SS') WHERE id = %s",
        (new_hash, user_id),
    )
    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/history", status_code=status.HTTP_200_OK)
def user_history(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the current user's complete activity history."""
    user_id = current_user["sub"]

    # Kundlis
    kundli_count = db.execute(
        "SELECT COUNT(*) as c FROM kundlis WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    kundlis = db.execute(
        "SELECT id, person_name, birth_date, birth_place, created_at FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    # Orders
    order_count = db.execute(
        "SELECT COUNT(*) as c FROM orders WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    recent_orders = db.execute(
        "SELECT id, status, total, payment_status, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC LIMIT 10",
        (user_id,),
    ).fetchall()

    # Consultations
    consultation_count = db.execute(
        "SELECT COUNT(*) as c FROM consultations WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    recent_consultations = db.execute(
        "SELECT id, type, status, scheduled_at, created_at FROM consultations WHERE user_id = %s ORDER BY created_at DESC LIMIT 10",
        (user_id,),
    ).fetchall()

    # AI chats
    ai_chat_count = db.execute(
        "SELECT COUNT(*) as c FROM ai_chat_logs WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]

    # Reports
    report_count = db.execute(
        "SELECT COUNT(*) as c FROM reports WHERE user_id = %s", (user_id,)
    ).fetchone()["c"]
    reports = db.execute(
        "SELECT id, report_type, status, price, created_at FROM reports WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    return {
        "kundlis": {"count": kundli_count, "list": [dict(r) for r in kundlis]},
        "orders": {"count": order_count, "recent": [dict(r) for r in recent_orders]},
        "consultations": {"count": consultation_count, "recent": [dict(r) for r in recent_consultations]},
        "ai_chats": {"count": ai_chat_count},
        "reports": {"count": report_count, "list": [dict(r) for r in reports]},
    }
