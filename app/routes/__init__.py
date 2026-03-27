"""Route registry — import all routers for inclusion in the FastAPI app."""
from app.routes.auth import router as auth_router
from app.routes.kundli import router as kundli_router
from app.routes.horoscope import router as horoscope_router
from app.routes.panchang import router as panchang_router
from app.routes.ai import router as ai_router
from app.routes.prashnavali import router as prashnavali_router
from app.routes.library import router as library_router
from app.routes.kp_lalkitab import router as kp_lalkitab_router
from app.routes.numerology import router as numerology_router
from app.routes.tarot import router as tarot_router
from app.routes.palmistry import router as palmistry_router
from app.routes.products import router as products_router
from app.routes.cart import router as cart_router
from app.routes.orders import router as orders_router
from app.routes.payments import router as payments_router
from app.routes.consultation import router as consultation_router
from app.routes.messages import router as messages_router
from app.routes.reports import router as reports_router
from app.routes.astrologer import router as astrologer_router
from app.routes.search import router as search_router
from app.routes.blog import router as blog_router
from app.routes.referral import router as referral_router
from app.routes.bundles import router as bundles_router
from app.routes.forum import router as forum_router
from app.routes.gamification import router as gamification_router
from app.routes.notifications import router as notifications_router
from app.routes.cosmic_calendar import router as cosmic_calendar_router

# Admin sub-routers (H-03 split)
from app.routes.admin_users import router as admin_users_router
from app.routes.admin_orders import router as admin_orders_router
from app.routes.admin_products import router as admin_products_router
from app.routes.admin_content import router as admin_content_router
from app.routes.admin_dashboard import router as admin_dashboard_router
from app.routes.admin_blog import router as admin_blog_router

all_routers = [
    auth_router,
    kundli_router,
    horoscope_router,
    panchang_router,
    ai_router,
    prashnavali_router,
    library_router,
    kp_lalkitab_router,
    numerology_router,
    tarot_router,
    palmistry_router,
    products_router,
    cart_router,
    orders_router,
    payments_router,
    consultation_router,
    messages_router,
    reports_router,
    blog_router,
    admin_users_router,
    admin_orders_router,
    admin_products_router,
    admin_content_router,
    admin_dashboard_router,
    admin_blog_router,
    astrologer_router,
    search_router,
    referral_router,
    bundles_router,
    forum_router,
    gamification_router,
    notifications_router,
    cosmic_calendar_router,
]
