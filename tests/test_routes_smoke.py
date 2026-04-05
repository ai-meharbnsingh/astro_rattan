"""Smoke tests for route modules — verify imports and router objects exist.

These tests verify that every route module:
1. Imports without error
2. Exports an APIRouter instance
3. Has at least one registered route

Route modules that already have dedicated test files are included here too
for completeness — if a module's imports break, this catches it fast.
"""
import pytest
from fastapi import APIRouter


# ── All route modules registered in app/routes/__init__.py ───────────
ROUTE_MODULES = [
    "app.routes.auth",
    "app.routes.kundli",
    "app.routes.horoscope",
    "app.routes.panchang",
    "app.routes.ai",
    "app.routes.prashnavali",
    "app.routes.library",
    "app.routes.kp_lalkitab",
    "app.routes.numerology",
    "app.routes.tarot",
    "app.routes.palmistry",
    "app.routes.products",
    "app.routes.cart",
    "app.routes.orders",
    "app.routes.payments",
    "app.routes.consultation",
    "app.routes.messages",
    "app.routes.reports",
    "app.routes.astrologer",
    "app.routes.search",
    "app.routes.blog",
    "app.routes.referral",
    "app.routes.bundles",
    "app.routes.forum",
    "app.routes.gamification",
    "app.routes.notifications",
    "app.routes.cosmic_calendar",
    "app.routes.whatsapp",
    "app.routes.astrologer_clients",
    "app.routes.admin_users",
    "app.routes.admin_orders",
    "app.routes.admin_products",
    "app.routes.admin_content",
    "app.routes.admin_dashboard",
    "app.routes.admin_blog",
]

# Route modules that had no dedicated test files at time of writing
UNTESTED_ROUTE_MODULES = [
    "app.routes.referral",
    "app.routes.bundles",
    "app.routes.forum",
    "app.routes.gamification",
    "app.routes.notifications",
    "app.routes.cosmic_calendar",
    "app.routes.whatsapp",
    "app.routes.astrologer_clients",
    "app.routes.messages",
    "app.routes.kp_lalkitab",
    "app.routes.panchang",
    "app.routes.numerology",
    "app.routes.tarot",
    "app.routes.prashnavali",
]


class TestRouteModuleImports:
    """Every route module must import without crashing."""

    @pytest.mark.parametrize("module_path", ROUTE_MODULES)
    def test_route_module_imports(self, module_path):
        import importlib
        mod = importlib.import_module(module_path)
        assert mod is not None

    @pytest.mark.parametrize("module_path", ROUTE_MODULES)
    def test_route_module_has_router(self, module_path):
        import importlib
        mod = importlib.import_module(module_path)
        assert hasattr(mod, "router"), f"{module_path} missing 'router' attribute"
        assert isinstance(mod.router, APIRouter), (
            f"{module_path}.router is {type(mod.router)}, expected APIRouter"
        )

    @pytest.mark.parametrize("module_path", ROUTE_MODULES)
    def test_route_module_has_routes_registered(self, module_path):
        import importlib
        mod = importlib.import_module(module_path)
        router = mod.router
        assert len(router.routes) > 0, (
            f"{module_path}.router has 0 routes registered"
        )


class TestRouteRegistryInit:
    """The route __init__.py must export all_routers with all routers."""

    def test_all_routers_list_exists(self):
        from app.routes import all_routers
        assert isinstance(all_routers, list)
        assert len(all_routers) >= 30  # 35 routers at time of writing

    def test_all_routers_are_api_routers(self):
        from app.routes import all_routers
        for i, router in enumerate(all_routers):
            assert isinstance(router, APIRouter), (
                f"all_routers[{i}] is {type(router)}, expected APIRouter"
            )

    def test_all_routers_have_routes(self):
        from app.routes import all_routers
        for router in all_routers:
            assert len(router.routes) > 0, (
                f"Router with tags={router.tags} has 0 routes"
            )


class TestUntestedRouteModulesHaveEndpoints:
    """Deeper checks for route modules that lack dedicated test files."""

    @pytest.mark.parametrize("module_path", UNTESTED_ROUTE_MODULES)
    def test_untested_route_has_get_or_post(self, module_path):
        """Each untested route module must have at least one GET or POST endpoint."""
        import importlib
        mod = importlib.import_module(module_path)
        router = mod.router
        methods_found = set()
        for route in router.routes:
            if hasattr(route, "methods"):
                methods_found.update(route.methods)
        assert methods_found, f"{module_path} has no HTTP methods on any route"
        # Must have at least GET or POST
        assert methods_found & {"GET", "POST"}, (
            f"{module_path} has methods {methods_found} but no GET or POST"
        )


class TestAppBootstrap:
    """The main FastAPI app must load with all routers mounted."""

    def test_app_imports_and_has_routes(self):
        from app.main import app
        # The app should have a large number of routes (all routers mounted)
        assert len(app.routes) >= 50, (
            f"app has only {len(app.routes)} routes, expected 50+"
        )

    def test_app_title_is_set(self):
        from app.main import app
        assert app.title is not None
        assert len(app.title) > 0
