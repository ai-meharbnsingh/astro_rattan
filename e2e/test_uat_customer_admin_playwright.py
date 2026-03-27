"""Detailed Playwright UAT for customer and admin journeys."""
import os
import time
from typing import Any

import httpx
import psycopg2
from playwright.sync_api import Page, expect
from app.database import DATABASE_URL

SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "screenshots",
    "uat_watch",
)


def _snapshot(page: Page, name: str) -> str:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{int(time.time())}_{name}.png")
    page.screenshot(path=path, full_page=True)
    return path


def _register_user(api_url: str, email: str, name: str, password: str = "password123") -> dict[str, Any]:
    response = httpx.post(
        f"{api_url}/api/auth/register",
        json={"email": email, "password": password, "name": name},
        timeout=20,
    )
    assert response.status_code == 201, response.text
    return response.json()


def _login_user(api_url: str, email: str, password: str = "password123") -> dict[str, Any]:
    response = httpx.post(
        f"{api_url}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    assert response.status_code == 200, response.text
    return response.json()


def _promote_admin(user_id: str) -> None:
    connection = psycopg2.connect(DATABASE_URL)
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", ("admin", user_id))
        connection.commit()
    finally:
        connection.close()


def _set_browser_token(page: Page, frontend_url: str, token: str) -> None:
    page.goto(frontend_url)
    page.evaluate("(authToken) => localStorage.setItem('astrovedic_token', authToken)", token)


class TestCustomerDetailedUAT:
    def test_customer_pages_load_and_nav_work(self, page: Page, frontend_url: str):
        routes = [
            "/",
            "/kundli",
            "/horoscope",
            "/panchang",
            "/ai-chat",
            "/library",
            "/shop",
            "/consultation",
            "/blog",
        ]

        for route in routes:
            page.goto(f"{frontend_url}{route}")
            page.wait_for_load_state("domcontentloaded")
            expect(page.locator("#root")).to_be_visible()
            if route != "/":
                assert page.url.endswith(route), f"Expected URL to end with {route}, got {page.url}"
            assert len(page.locator("body").inner_text().strip()) > 100
            _snapshot(page, f"customer_page_{route.strip('/').replace('-', '_') or 'home'}")

    def test_customer_add_to_cart_and_place_order(self, page: Page, api_url: str, frontend_url: str):
        ts = int(time.time())
        email = f"uat_customer_{ts}@astrovedic.com"
        password = "password123"
        registration = _register_user(api_url, email, "UAT Customer", password)
        _set_browser_token(page, frontend_url, registration["token"])

        products_response = httpx.get(f"{api_url}/api/products", timeout=20)
        assert products_response.status_code == 200, products_response.text
        products = products_response.json().get("products", [])
        assert products, "Expected at least one active product for cart flow"
        product_name = products[0]["name"]

        page.goto(f"{frontend_url}/shop")
        page.wait_for_load_state("networkidle")
        _snapshot(page, "customer_shop_loaded")

        product_card = page.locator("h3", has_text=product_name).first
        expect(product_card).to_be_visible()
        product_card.locator("xpath=ancestor::div[contains(@class,'p-4')][1]//button").first.click()
        _snapshot(page, "customer_added_to_cart_from_shop")

        page.goto(f"{frontend_url}/cart")
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_contain_text("Your Cart")
        expect(page.locator("body")).to_contain_text(product_name)
        _snapshot(page, "customer_cart_with_item")

        page.get_by_role("button", name="Proceed to Shipping").click()
        page.get_by_placeholder("Full Name").fill("UAT Customer")
        page.get_by_placeholder("Address Line 1").fill("221B Baker Street")
        page.get_by_placeholder("City").fill("Mumbai")
        page.get_by_placeholder("State").fill("MH")
        page.get_by_placeholder("Pincode").fill("400001")
        page.get_by_placeholder("Phone").fill("9999999999")
        page.get_by_role("button", name="Continue to Payment").click()
        _snapshot(page, "customer_shipping_filled")

        page.get_by_role("button", name="Place Order").click()
        expect(page.locator("body")).to_contain_text("Order Placed!")
        _snapshot(page, "customer_order_placed")

        login = _login_user(api_url, email, password)
        orders_response = httpx.get(
            f"{api_url}/api/orders",
            headers={"Authorization": f"Bearer {login['token']}"},
            timeout=20,
        )
        assert orders_response.status_code == 200, orders_response.text
        orders = orders_response.json()
        assert isinstance(orders, list)
        assert len(orders) >= 1


class TestAdminDetailedUAT:
    def test_admin_create_product_from_dashboard(self, page: Page, api_url: str, frontend_url: str):
        ts = int(time.time())
        email = f"uat_admin_{ts}@astrovedic.com"
        password = "password123"
        registration = _register_user(api_url, email, "UAT Admin", password)
        _promote_admin(registration["user"]["id"])
        login = _login_user(api_url, email, password)
        _set_browser_token(page, frontend_url, login["token"])

        new_product_name = f"UAT Product {ts}"

        page.goto(f"{frontend_url}/admin")
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()
        _snapshot(page, "admin_dashboard_loaded")

        page.get_by_role("tab", name="Products").click()
        page.get_by_role("button", name="Add Product").click()
        expect(page.get_by_role("dialog")).to_be_visible()
        _snapshot(page, "admin_product_dialog_open")

        dialog = page.get_by_role("dialog")
        dialog.get_by_placeholder("Product name").fill(new_product_name)
        dialog.get_by_placeholder("Product description").fill("UAT created product through admin dashboard")
        dialog.get_by_placeholder("0", exact=True).fill("12")
        dialog.get_by_placeholder("0.00", exact=True).fill("2499")
        dialog.get_by_placeholder("e.g. Sun, Moon, Saturn", exact=True).fill("Sun")
        dialog.get_by_placeholder("e.g. 10g, 5 carats", exact=True).fill("10g")
        _snapshot(page, "admin_product_form_filled")
        page.get_by_role("button", name="Create Product").click()

        expect(page.get_by_role("table")).to_contain_text(new_product_name)
        _snapshot(page, "admin_product_created_visible")

        admin_products_resp = httpx.get(
            f"{api_url}/api/admin/products",
            headers={"Authorization": f"Bearer {login['token']}"},
            timeout=20,
        )
        assert admin_products_resp.status_code == 200, admin_products_resp.text
        products = admin_products_resp.json().get("products", [])
        assert any(p.get("name") == new_product_name for p in products), "Admin product creation not reflected in API"

    def test_admin_tabs_interface_walkthrough(self, page: Page, api_url: str, frontend_url: str):
        ts = int(time.time())
        email = f"uat_admin_tabs_{ts}@astrovedic.com"
        password = "password123"
        registration = _register_user(api_url, email, "UAT Admin Tabs", password)
        _promote_admin(registration["user"]["id"])
        login = _login_user(api_url, email, password)
        _set_browser_token(page, frontend_url, login["token"])

        page.goto(f"{frontend_url}/admin")
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()

        admin_tabs = ["Overview", "Users", "Orders", "Products", "Content", "Blog", "AI Logs"]
        for tab in admin_tabs:
            page.get_by_role("tab", name=tab).click()
            page.wait_for_timeout(800)
            _snapshot(page, f"admin_tab_{tab.lower().replace(' ', '_')}")


class TestExtendedCustomerInterfaceUAT:
    def test_customer_extended_pages_walkthrough(self, page: Page, api_url: str, frontend_url: str):
        ts = int(time.time())
        email = f"uat_customer_pages_{ts}@astrovedic.com"
        password = "password123"
        registration = _register_user(api_url, email, "UAT Customer Extended", password)
        _set_browser_token(page, frontend_url, registration["token"])

        routes = [
            "/dashboard",
            "/profile",
            "/reports",
            "/messages",
            "/numerology",
            "/prashnavali",
            "/palmistry",
            "/transits",
            "/community",
            "/referral",
            "/journey",
            "/cosmic-calendar",
            "/preferences",
        ]

        for route in routes:
            page.goto(f"{frontend_url}{route}")
            page.wait_for_load_state("domcontentloaded")
            expect(page.locator("#root")).to_be_visible()
            page.wait_for_timeout(700)
            _snapshot(page, f"customer_extended_{route.strip('/').replace('-', '_')}")

            for tab_name in ["Overview", "Reports", "Orders", "Settings", "Profile", "History"]:
                tab = page.get_by_role("tab", name=tab_name)
                if tab.count() > 0 and tab.first.is_visible():
                    tab.first.click()
                    page.wait_for_timeout(600)
                    _snapshot(page, f"{route.strip('/').replace('-', '_')}_tab_{tab_name.lower()}")


class TestLibraryUICompleteness:
    def test_library_tabs_links_and_visible_data(self, page: Page, frontend_url: str):
        page.goto(f"{frontend_url}/library")
        page.wait_for_load_state("networkidle")
        expect(page.locator("h2")).to_contain_text("Spiritual")
        _snapshot(page, "library_home_loaded")

        gita_tab = page.get_by_role("tab", name="Gita")
        mantra_tab = page.get_by_role("tab", name="Mantras")
        aarti_tab = page.get_by_role("tab", name="Aarti")
        chalisa_tab = page.get_by_role("tab", name="Chalisa")
        expect(gita_tab).to_be_visible()
        expect(mantra_tab).to_be_visible()
        expect(aarti_tab).to_be_visible()
        expect(chalisa_tab).to_be_visible()

        gita_cards = page.locator("h3:has-text('Chapter')")
        assert gita_cards.count() >= 4, "Gita tab shows too few chapters"
        page.get_by_role("button", name="View 3 Verses").first.click()
        page.wait_for_timeout(1400)
        expect(page.locator("body")).to_contain_text("Bhagavad Gita - Chapter")
        expect(page.locator("body")).to_contain_text("Chapter 2, Verse")
        expect(page.locator("body")).to_contain_text("Download Audio")
        _snapshot(page, "library_gita_tab")

        mantra_tab.click()
        page.wait_for_timeout(1200)
        mantra_cards = page.locator("h3")
        assert mantra_cards.count() >= 4, "Mantra tab shows too few items"
        expect(page.locator("body")).to_contain_text("Download Audio")
        _snapshot(page, "library_mantra_tab")

        aarti_tab.click()
        page.wait_for_timeout(1200)
        aarti_cards = page.locator("h3")
        assert aarti_cards.count() >= 4, "Aarti tab shows too few items"
        _snapshot(page, "library_aarti_tab")

        chalisa_tab.click()
        page.wait_for_timeout(1200)
        chalisa_cards = page.locator("h3")
        assert chalisa_cards.count() >= 3, "Chalisa tab shows too few items"
        _snapshot(page, "library_chalisa_tab")

        page.get_by_role("button", name="Ask AI Gita").click()
        page.wait_for_load_state("domcontentloaded")
        assert page.url.endswith("/ai-chat"), f"AI CTA should route to /ai-chat, got {page.url}"
        _snapshot(page, "library_ai_cta_navigated")
