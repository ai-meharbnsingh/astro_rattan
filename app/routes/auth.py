"""Auth routes — register, login, get current user, profile management."""
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from slowapi import Limiter

from app.auth import hash_password, verify_password, create_token, create_refresh_token, decode_token, get_current_user
from app.database import get_db
from app.models import (
    SendOtpRequest,
    VerifyOtpRequest,
    UserRegister,
    LoginRequest,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    UserProfileUpdate,
    ChangePasswordRequest,
    AstrologerRegisterRequest,
)

from app.config import LOGIN_RATE_LIMIT
from app.rate_limit import request_rate_limit_key

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Rate limiter instance — shares config with main app limiter
limiter = Limiter(key_func=request_rate_limit_key)


def _generate_otp() -> str:
    """Generate a 6-digit numeric OTP."""
    return f"{secrets.randbelow(900000) + 100000}"


def _send_otp_email(email: str, otp: str) -> bool:
    """Send OTP via Resend API. Returns True on success, False on failure."""
    import os
    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key:
        print(f"[OTP] RESEND_API_KEY not set — OTP for {email}: {otp}")
        return True  # Allow registration in dev (OTP logged to console)
    try:
        import resend
        resend.api_key = api_key
        from_addr = os.getenv("RESEND_FROM", "Astro Rattan <onboarding@resend.dev>")
        resend.Emails.send({
            "from": from_addr,
            "to": [email],
            "subject": f"Astro Rattan - Verification Code: {otp}",
            "reply_to": "ai.meharbansingh@gmail.com",
            "html": (
                f"<div style='font-family:Georgia,serif;max-width:480px;margin:0 auto;padding:32px;'>"
                f"<h2 style='color:#C4A35A;'>Astro Rattan</h2>"
                f"<p>Your verification code is:</p>"
                f"<p style='font-size:32px;font-weight:bold;letter-spacing:8px;color:#1a1a2e;'>{otp}</p>"
                f"<p style='color:#666;'>This code expires in 10 minutes.</p>"
                f"</div>"
            ),
        })
        return True
    except Exception as e:
        print(f"[OTP] Failed to send email to {email}: {e}")
        return False


def _verify_email_token(email_token: str, expected_email: str):
    """Validate the email verification token matches the registration email."""
    payload = decode_token(email_token)
    if not payload or payload.get("purpose") != "email_verified":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired email verification token. Please verify your email first.",
        )
    if payload.get("email", "").lower() != expected_email.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email token does not match registration email.",
        )


@router.post("/send-otp", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def send_otp(
    request: Request,
    body: SendOtpRequest,
    db: Any = Depends(get_db),
):
    """Send a 6-digit OTP to the given email for verification."""
    # Check if email already registered
    existing = db.execute("SELECT id FROM users WHERE email = %s", (body.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    otp = _generate_otp()
    expires_at = (datetime.now(tz=timezone.utc) + timedelta(minutes=10)).isoformat()

    # Remove any previous OTPs for this email
    db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
    db.execute(
        "INSERT INTO email_verifications (email, otp, expires_at) VALUES (%s, %s, %s)",
        (body.email, otp, expires_at),
    )
    db.commit()

    # Send OTP via SMTP
    sent = _send_otp_email(body.email, otp)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to send verification email. Please try again.",
        )
    return {"message": "Verification code sent to your email"}


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def verify_otp(
    request: Request,
    body: VerifyOtpRequest,
    db: Any = Depends(get_db),
):
    """Verify the OTP and return an email_token for registration."""
    row = db.execute(
        "SELECT id, otp, attempts, expires_at FROM email_verifications WHERE email = %s ORDER BY created_at DESC LIMIT 1",
        (body.email,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No verification pending for this email")

    # Check expiry
    expires_at = datetime.fromisoformat(row["expires_at"])
    if datetime.now(tz=timezone.utc) > expires_at:
        db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code expired. Please request a new one.")

    # Check attempts (max 5)
    if row["attempts"] >= 5:
        db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
        db.commit()
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many attempts. Please request a new code.")

    # Increment attempts
    db.execute("UPDATE email_verifications SET attempts = attempts + 1 WHERE id = %s", (row["id"],))
    db.commit()

    if row["otp"] != body.otp:
        remaining = 5 - row["attempts"] - 1
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid code. {remaining} attempts remaining.",
        )

    # OTP valid — clean up and issue email_token
    db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
    db.commit()

    email_token = create_token({"email": body.email, "purpose": "email_verified"})
    return {"verified": True, "email_token": email_token}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register(
    body: UserRegister,
    background_tasks: BackgroundTasks,
    db: Any = Depends(get_db),
):
    """Register a new user account. Requires a verified email_token from /verify-otp."""
    # Validate email verification token
    _verify_email_token(body.email_token, body.email)

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
    refresh = create_refresh_token({"sub": user.id})
    # Email service removed - welcome email disabled
    return TokenResponse(user=user, token=token, refresh_token=refresh)


@router.post("/register-astrologer", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register_astrologer(
    body: AstrologerRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Any = Depends(get_db),
):
    """Register a new astrologer account. Requires a verified email_token from /verify-otp."""
    _verify_email_token(body.email_token, body.email)

    row = db.execute("SELECT id FROM users WHERE email = %s", (body.email,)).fetchone()
    if row:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    pw_hash = hash_password(body.password)
    db.execute(
        """INSERT INTO users (email, password_hash, name, role, phone)
           VALUES (%s, %s, %s, 'astrologer', %s)""",
        (body.email, pw_hash, body.name, body.phone),
    )
    db.commit()

    user_row = db.execute(
        """SELECT id, email, name, role, phone, date_of_birth, gender, city, avatar_url, created_at
           FROM users WHERE email = %s""",
        (body.email,),
    ).fetchone()

    # Create astrologer profile entry
    db.execute(
        """INSERT INTO astrologers (user_id, display_name, specializations, experience_years, per_minute_rate, languages)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            user_row["id"],
            body.display_name or body.name,
            body.specializations,
            body.experience_years,
            body.per_minute_rate,
            body.languages,
        ),
    )
    db.commit()

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
    refresh = create_refresh_token({"sub": user.id})
    # Email service removed - welcome email disabled
    return TokenResponse(user=user, token=token, refresh_token=refresh)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
@limiter.limit(LOGIN_RATE_LIMIT)
def login(request: Request, body: LoginRequest, db: Any = Depends(get_db)):
    """Authenticate and return JWT token."""
    row = db.execute(
        """SELECT id, email, password_hash, name, role, phone, date_of_birth, gender, city,
                  avatar_url, created_at, is_active, COALESCE(token_version, 0) as token_version
           FROM users WHERE email = %s""",
        (body.email,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if row["is_active"] is not None and not row["is_active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

    tv = row["token_version"]
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
    token = create_token({"sub": user.id, "email": user.email, "role": user.role}, token_version=tv)
    refresh = create_refresh_token({"sub": user.id}, token_version=tv)
    return TokenResponse(user=user, token=token, refresh_token=refresh)


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(body: RefreshTokenRequest, db: Any = Depends(get_db)):
    """Exchange a valid refresh token for a new access token + refresh token."""
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = payload.get("sub")
    row = db.execute(
        """SELECT id, email, role, is_active FROM users WHERE id = %s""",
        (user_id,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if row["is_active"] is not None and not row["is_active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

    new_token = create_token({"sub": row["id"], "email": row["email"], "role": row["role"]})
    new_refresh = create_refresh_token({"sub": row["id"]})
    return {"token": new_token, "refresh_token": new_refresh}


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

    updates.append("updated_at = NOW()")
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
        "UPDATE users SET password_hash = %s, token_version = COALESCE(token_version, 0) + 1, updated_at = NOW() WHERE id = %s",
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


# ── Forgot Password ─────────────────────────────────────────

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    body: SendOtpRequest,
    db: Any = Depends(get_db),
):
    """Send a password reset OTP to the given email."""
    user = db.execute("SELECT id FROM users WHERE email = %s", (body.email,)).fetchone()
    if not user:
        # Don't reveal whether email exists
        return {"message": "If this email is registered, a reset code has been sent."}

    otp = _generate_otp()
    expires_at = (datetime.now(tz=timezone.utc) + timedelta(minutes=10)).isoformat()
    db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
    db.execute(
        "INSERT INTO email_verifications (email, otp, expires_at) VALUES (%s, %s, %s)",
        (body.email, otp, expires_at),
    )
    db.commit()

    import os
    api_key = os.getenv("RESEND_API_KEY", "")
    if api_key:
        try:
            import resend
            resend.api_key = api_key
            resend.Emails.send({
                "from": os.getenv("RESEND_FROM", "Astro Rattan <onboarding@resend.dev>"),
                "to": [body.email],
                "subject": f"Astro Rattan - Password Reset Code: {otp}",
                "html": (
                    f"<div style='font-family:Georgia,serif;max-width:480px;margin:0 auto;padding:32px;'>"
                    f"<h2 style='color:#C4A35A;'>Password Reset</h2>"
                    f"<p>Your reset code is:</p>"
                    f"<p style='font-size:32px;font-weight:bold;letter-spacing:8px;color:#1a1a2e;'>{otp}</p>"
                    f"<p style='color:#666;'>This code expires in 10 minutes. If you didn't request this, ignore this email.</p>"
                    f"</div>"
                ),
            })
        except Exception as e:
            print(f"[RESET] Failed to send email: {e}")
    else:
        print(f"[RESET] OTP for {body.email}: {otp}")

    return {"message": "If this email is registered, a reset code has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    body: VerifyOtpRequest,
    db: Any = Depends(get_db),
):
    """Reset password using OTP. Body: {email, otp, new_password}."""
    row = db.execute(
        "SELECT id, otp, attempts, expires_at FROM email_verifications WHERE email = %s ORDER BY created_at DESC LIMIT 1",
        (body.email,),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=400, detail="No reset code found. Please request a new one.")

    expires_at = row["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(tz=timezone.utc) > expires_at:
        raise HTTPException(status_code=400, detail="Reset code expired. Please request a new one.")

    if row["otp"] != body.otp:
        db.execute("UPDATE email_verifications SET attempts = attempts + 1 WHERE id = %s", (row["id"],))
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid code.")

    new_password = getattr(body, "new_password", None)
    if not new_password:
        raise HTTPException(status_code=400, detail="new_password is required.")

    db.execute(
        "UPDATE users SET password_hash = %s, token_version = COALESCE(token_version, 0) + 1, updated_at = NOW() WHERE email = %s",
        (hash_password(new_password), body.email),
    )
    db.execute("DELETE FROM email_verifications WHERE email = %s", (body.email,))
    db.commit()

    return {"message": "Password reset successfully. You can now log in."}
