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
]
