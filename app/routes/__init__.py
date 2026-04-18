"""Route registry — import all routers for inclusion in the FastAPI app."""
from app.routes.auth import router as auth_router
from app.routes.kundli import router as kundli_router
from app.routes.panchang import router as panchang_router
from app.routes.kp_lalkitab import router as kp_lalkitab_router
from app.routes.numerology import router as numerology_router
from app.routes.mundane import router as mundane_router
from app.routes.clients import router as clients_router
from app.routes.admin import router as admin_router
from app.routes.analytics import router as analytics_router
from app.routes.feedback import router as feedback_router
from app.routes.ai import router as ai_router
from app.routes.muhurat import router as muhurat_router
from app.routes.horoscope import router as horoscope_router
from app.vastu.routes import router as vastu_router
from app.routes.yoga_search import router as yoga_search_router
from app.routes.astro_map import router as astro_map_router
from app.routes.dasha import router as dasha_router
from app.routes.interpretations import router as interpretations_router
from app.routes.lalkitab_farmaan import router as lalkitab_farmaan_router

all_routers = [
    auth_router,
    kundli_router,
    panchang_router,
    kp_lalkitab_router,
    numerology_router,
    mundane_router,
    clients_router,
    admin_router,
    analytics_router,
    feedback_router,
    ai_router,
    muhurat_router,
    horoscope_router,
    vastu_router,
    yoga_search_router,
    astro_map_router,
    dasha_router,
    interpretations_router,
    lalkitab_farmaan_router,
]
