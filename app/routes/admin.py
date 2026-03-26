"""Admin routes — re-exports from split sub-modules for backward compatibility.

H-03: The monolithic admin.py has been split into:
  - admin_users.py — user management
  - admin_orders.py — order management
  - admin_products.py — product CRUD, stock, toggle, image upload
  - admin_content.py — spiritual content CRUD
  - admin_dashboard.py — dashboard stats, AI logs, astrologer approval

This file provides the same `router` object by merging all sub-routers
so existing imports (e.g., `from app.routes.admin import router`) still work.
"""
from fastapi import APIRouter

from app.routes.admin_users import router as users_router
from app.routes.admin_orders import router as orders_router
from app.routes.admin_products import router as products_router
from app.routes.admin_content import router as content_router
from app.routes.admin_dashboard import router as dashboard_router

router = APIRouter()

# Merge all sub-routers into the single admin router
router.include_router(users_router)
router.include_router(orders_router)
router.include_router(products_router)
router.include_router(content_router)
router.include_router(dashboard_router)
