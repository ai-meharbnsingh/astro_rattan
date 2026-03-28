"""Pydantic request/response models for AstroVedic API."""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from enum import Enum


# ============================================================
# Enums
# ============================================================
class UserRole(str, Enum):
    user = "user"
    astrologer = "astrologer"
    admin = "admin"

class ZodiacSign(str, Enum):
    aries = "aries"; taurus = "taurus"; gemini = "gemini"; cancer = "cancer"
    leo = "leo"; virgo = "virgo"; libra = "libra"; scorpio = "scorpio"
    sagittarius = "sagittarius"; capricorn = "capricorn"; aquarius = "aquarius"; pisces = "pisces"

class HoroscopePeriod(str, Enum):
    daily = "daily"; weekly = "weekly"; monthly = "monthly"; yearly = "yearly"

class ProductCategory(str, Enum):
    gemstone = "gemstone"; rudraksha = "rudraksha"; bracelet = "bracelet"
    yantra = "yantra"; vastu = "vastu"

class OrderStatus(str, Enum):
    placed = "placed"; confirmed = "confirmed"; shipped = "shipped"
    delivered = "delivered"; cancelled = "cancelled"

class PaymentMethod(str, Enum):
    cod = "cod"; razorpay = "razorpay"; stripe = "stripe"

class ConsultationType(str, Enum):
    chat = "chat"; call = "call"; video = "video"

class PrashnavaliType(str, Enum):
    ram_shalaka = "ram_shalaka"; hanuman_prashna = "hanuman_prashna"
    ramcharitmanas = "ramcharitmanas"; gita = "gita"

class ContentCategory(str, Enum):
    gita = "gita"; aarti = "aarti"; mantra = "mantra"; pooja = "pooja"
    vrat_katha = "vrat_katha"; chalisa = "chalisa"; festival = "festival"

class ReportType(str, Enum):
    full_kundli = "full_kundli"; marriage = "marriage"; career = "career"
    health = "health"; yearly = "yearly"

class TarotSpread(str, Enum):
    single = "single"; three = "three"; celtic_cross = "celtic_cross"


# ============================================================
# Auth
# ============================================================
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)
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
    created_at: str

class TokenResponse(BaseModel):
    user: UserResponse
    token: str


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


class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)
    role: UserRole
    phone: Optional[str] = None


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

class KundliMatchRequest(BaseModel):
    kundli_id_1: str
    kundli_id_2: str

class DivisionalChartRequest(BaseModel):
    chart_type: str = "D9"  # D9, D10, etc.


# ============================================================
# AI
# ============================================================
class AIInterpretRequest(BaseModel):
    kundli_id: str

class AIAskRequest(BaseModel):
    question: str = Field(min_length=1)
    kundli_id: Optional[str] = None

class AIGitaRequest(BaseModel):
    question: str = Field(min_length=1)

class AIOracleRequest(BaseModel):
    question: str = Field(min_length=1)
    mode: str = "yes_no"  # yes_no or tarot


# ============================================================
# Prashnavali
# ============================================================
class RamShalakaRequest(BaseModel):
    row: int = Field(ge=1, le=15)
    col: int = Field(ge=1, le=15)

class PrashnavaliRequest(BaseModel):
    question: str = Field(min_length=1)


# ============================================================
# E-Commerce
# ============================================================
class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str
    category: ProductCategory
    price: float = Field(gt=0)
    compare_price: Optional[float] = None
    image_url: Optional[str] = None
    weight: Optional[str] = None
    planet: Optional[str] = None
    properties: Optional[str] = None
    stock: int = Field(ge=0)

class CartAddRequest(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, default=1)

class CartUpdateRequest(BaseModel):
    quantity: int = Field(ge=1)

class OrderCreateRequest(BaseModel):
    shipping_address: str = Field(min_length=10)
    payment_method: PaymentMethod

class PaymentInitiateRequest(BaseModel):
    order_id: str
    provider: PaymentMethod


class ReportPaymentInitiateRequest(BaseModel):
    report_id: str
    provider: PaymentMethod


# ============================================================
# Consultation
# ============================================================
class ConsultationBookRequest(BaseModel):
    astrologer_id: str
    type: ConsultationType
    scheduled_at: Optional[str] = None

class AstrologerProfileUpdate(BaseModel):
    bio: Optional[str] = None
    specializations: Optional[str] = None
    per_minute_rate: Optional[float] = Field(default=None, gt=0)
    languages: Optional[str] = None

class AstrologerAvailability(BaseModel):
    is_available: bool


class AstrologerClientCreate(BaseModel):
    client_name: str = Field(min_length=1)
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    birth_date: Optional[str] = None  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM:SS
    birth_place: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    timezone_offset: Optional[float] = Field(default=5.5, ge=-12, le=14)
    gender: Optional[str] = "male"
    notes: Optional[str] = None


class AstrologerClientUpdate(BaseModel):
    client_name: Optional[str] = Field(default=None, min_length=1)
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    timezone_offset: Optional[float] = Field(default=None, ge=-12, le=14)
    gender: Optional[str] = None
    notes: Optional[str] = None


class AstrologerRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)
    phone: Optional[str] = None
    display_name: Optional[str] = None
    specializations: str = "Vedic"
    experience_years: int = Field(default=0, ge=0)
    per_minute_rate: float = Field(default=10.0, gt=0)
    languages: str = '["English"]'


# ============================================================
# Reports
# ============================================================
class ReportRequest(BaseModel):
    kundli_id: str
    report_type: ReportType


# ============================================================
# Admin
# ============================================================
class AdminUserUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class AdminOrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None

class ContentCreate(BaseModel):
    category: ContentCategory
    title: str = Field(min_length=1)
    title_hindi: Optional[str] = None
    content: str
    audio_url: Optional[str] = None
    chapter: Optional[int] = None
    verse: Optional[int] = None
    sanskrit_text: Optional[str] = None
    translation: Optional[str] = None
    commentary: Optional[str] = None
    sort_order: int = 0


class BlogPostCreate(BaseModel):
    title: str = Field(min_length=3)
    excerpt: str = Field(min_length=20)
    content: str = Field(min_length=50)
    cover_image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    author_name: str = "AstroVedic Editorial"
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    slug: Optional[str] = None
    is_published: bool = True


class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    excerpt: Optional[str] = Field(default=None, min_length=20)
    content: Optional[str] = Field(default=None, min_length=50)
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    author_name: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None


# ============================================================
# Numerology + Tarot
# ============================================================
class NumerologyRequest(BaseModel):
    name: str = Field(min_length=1)
    birth_date: str  # YYYY-MM-DD

class TarotDrawRequest(BaseModel):
    spread: TarotSpread = TarotSpread.single
    question: Optional[str] = None


# ============================================================
# Panchang
# ============================================================
class MuhuratType(str, Enum):
    marriage = "marriage"; griha_pravesh = "griha_pravesh"
    business_start = "business_start"; travel = "travel"
    naming_ceremony = "naming_ceremony"; mundan = "mundan"


class ReferralEarningStatus(str, Enum):
    pending = "pending"
    paid = "paid"


# ============================================================
# Referral / Affiliate
# ============================================================
class ReferralCode(BaseModel):
    code: str
    user_id: str
    discount_percent: float = 5.0
    commission_percent: float = 10.0
    uses_count: int = 0
    max_uses: Optional[int] = None
    is_active: bool = True


class ReferralEarning(BaseModel):
    id: str
    referrer_id: str
    referred_id: str
    order_id: str
    amount: float
    commission: float
    status: ReferralEarningStatus = ReferralEarningStatus.pending


class ReferralStats(BaseModel):
    total_referrals: int = 0
    total_earnings: float = 0.0
    pending_earnings: float = 0.0
    paid_earnings: float = 0.0


class ApplyReferralRequest(BaseModel):
    code: str = Field(min_length=1)


# ============================================================
# Product Bundles
# ============================================================
class BundleType(str, Enum):
    consultation_product = "consultation_product"
    multi_product = "multi_product"


class BundleItemCreate(BaseModel):
    product_id: Optional[str] = None
    consultation_type: Optional[str] = None  # chat, call, video
    quantity: int = Field(ge=1, default=1)

    @field_validator("consultation_type")
    @classmethod
    def validate_consultation_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("chat", "call", "video"):
            raise ValueError("consultation_type must be chat, call, or video")
        return v


class BundleCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    bundle_type: BundleType
    discount_percent: float = Field(ge=0, le=100)
    items: List[BundleItemCreate] = Field(min_length=1)


class BundleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    discount_percent: Optional[float] = Field(default=None, ge=0, le=100)
    is_active: Optional[bool] = None


# ============================================================
# Gamification
# ============================================================
class KarmaActionType(str, Enum):
    daily_login = "daily_login"
    kundli_generated = "kundli_generated"
    ai_chat = "ai_chat"
    panchang_viewed = "panchang_viewed"
    shop_purchase = "shop_purchase"
    consultation_completed = "consultation_completed"
    library_read = "library_read"
    prashnavali_used = "prashnavali_used"
    learning_completed = "learning_completed"


class LearningCategory(str, Enum):
    basics = "basics"
    kundli = "kundli"
    panchang = "panchang"
    doshas = "doshas"
    remedies = "remedies"
    advanced = "advanced"


class KarmaProfile(BaseModel):
    user_id: str
    total_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: Optional[str] = None
    level: int = 1
    badges: List[dict] = []


class KarmaTransaction(BaseModel):
    id: str
    user_id: str
    points: int
    action_type: str
    description: Optional[str] = None
    created_at: str


class Badge(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    earned: bool = False
    earned_at: Optional[str] = None


class LearningModule(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: str
    order_index: int = 0
    content_json: Optional[str] = None
    points_reward: int = 50
    completed: bool = False


class LearningProgress(BaseModel):
    id: str
    user_id: str
    module_id: str
    completed_at: str


# ============================================================
# Forum / Community
# ============================================================
class ForumCategory(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order_index: int = 0
    is_active: bool = True
    thread_count: int = 0


class ThreadCreate(BaseModel):
    category_id: str
    title: str = Field(min_length=3)
    content: str = Field(min_length=10)


class ThreadResponse(BaseModel):
    id: str
    category_id: str
    user_id: str
    title: str
    content: str
    is_pinned: bool = False
    is_locked: bool = False
    views_count: int = 0
    replies_count: int = 0
    created_at: str
    updated_at: str
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None
    category_name: Optional[str] = None


class ReplyCreate(BaseModel):
    content: str = Field(min_length=1)


class ReplyResponse(BaseModel):
    id: str
    thread_id: str
    user_id: str
    content: str
    is_best_answer: bool = False
    likes_count: int = 0
    created_at: str
    updated_at: str
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None
    liked_by_me: bool = False


class BundleItemResponse(BaseModel):
    id: str
    product_id: Optional[str] = None
    consultation_type: Optional[str] = None
    quantity: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None


class BundleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    bundle_type: str
    discount_percent: float
    is_active: bool
    created_at: str
    items: List[BundleItemResponse] = []
    original_price: float = 0.0
    discounted_price: float = 0.0
    savings: float = 0.0
