"""Pydantic request/response models for Astro Rattan API."""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Any, Optional
from enum import Enum


# ============================================================
# Enums
# ============================================================
class UserRole(str, Enum):
    user = "user"
    astrologer = "astrologer"
    admin = "admin"


# ============================================================
# Auth
# ============================================================
class SendOtpRequest(BaseModel):
    email: EmailStr

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    new_password: Optional[str] = Field(default=None, min_length=6)

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1)
    email_token: str = Field(min_length=1)
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None  # YYYY-MM-DD
    gender: Optional[str] = None  # male/female/other
    city: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Any = None

class TokenResponse(BaseModel):
    user: UserResponse
    token: str
    refresh_token: str = ""


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None  # YYYY-MM-DD
    gender: Optional[str] = None  # male/female/other
    city: Optional[str] = None
    avatar_url: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)


class AstrologerRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1)
    email_token: str = Field(min_length=1)
    phone: str = Field(min_length=4, description="Phone number is required for astrologers")
    display_name: Optional[str] = None
    specializations: str = "Vedic"
    experience_years: int = Field(default=0, ge=0)
    per_minute_rate: float = Field(default=10.0, gt=0)
    languages: str = '["English"]'


# ============================================================
# Kundli
# ============================================================
class KundliRequest(BaseModel):
    person_name: str = Field(min_length=1)
    birth_date: str  # ISO date YYYY-MM-DD
    birth_time: str  # HH:MM:SS
    birth_place: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone_offset: float = Field(ge=-12, le=14)
    ayanamsa: str = "lahiri"
    client_id: Optional[str] = None  # Link to existing client
    chart_type: str = "vedic"  # vedic, lalkitab
    phone: Optional[str] = None  # Auto-create client if provided
    gender: Optional[str] = None

    @field_validator('birth_date')
    @classmethod
    def validate_date(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('birth_date must be YYYY-MM-DD format')
        return v

    @field_validator('birth_time')
    @classmethod
    def validate_time(cls, v):
        import re
        from datetime import datetime
        v = v.strip()

        # Remove duplicate seconds (e.g., "20:10:00:00" → "20:10:00")
        parts = v.replace(' ', ':').split(':')
        # Filter out AM/PM from parts
        am_pm = ''
        clean_parts = []
        for p in parts:
            upper = p.strip().upper()
            if upper in ('AM', 'PM'):
                am_pm = upper
            else:
                clean_parts.append(p.strip())

        # Rebuild clean time string
        if len(clean_parts) >= 3:
            v_clean = f"{clean_parts[0]}:{clean_parts[1]}:{clean_parts[2]}"
        elif len(clean_parts) == 2:
            v_clean = f"{clean_parts[0]}:{clean_parts[1]}:00"
        else:
            v_clean = v

        if am_pm:
            v_clean = f"{v_clean} {am_pm}"

        # Try 24-hour formats first
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                datetime.strptime(v_clean, fmt)
                return v_clean
            except ValueError:
                continue
        # Try 12-hour formats with AM/PM — convert to 24-hour
        for fmt in ('%I:%M:%S %p', '%I:%M %p'):
            try:
                parsed = datetime.strptime(v_clean, fmt)
                return parsed.strftime('%H:%M:%S')
            except ValueError:
                continue
        raise ValueError('birth_time must be HH:MM:SS or HH:MM format')

class KundliMatchRequest(BaseModel):
    kundli_id_1: str
    kundli_id_2: str

class DivisionalChartRequest(BaseModel):
    chart_type: str = "D9"  # D9, D10, etc.
    birth_time_uncertainty_seconds: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated uncertainty in birth time in seconds (e.g., 30 for ±30s). Used for D60 Shashtiamsa accuracy assessment."
    )


# ============================================================
# Numerology
# ============================================================
class NumerologyRequest(BaseModel):
    name: str = Field(min_length=1)
    birth_date: str  # YYYY-MM-DD

class MobileNumerologyRequest(BaseModel):
    phone_number: str = Field(min_length=4)
    name: str = ""
    birth_date: str = ""  # YYYY-MM-DD (optional but enables DOB-based features)
    areas_of_struggle: list = []  # ["health", "relationship", "career", "money", "job"]


# ============================================================
# Admin
# ============================================================
class AdminUserUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
