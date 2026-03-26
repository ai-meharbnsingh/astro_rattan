"""Focused browser smoke tests for critical frontend pages."""
import sqlite3
from pathlib import Path

import httpx
from PIL import Image
from playwright.sync_api import expect

def _register_user(api_url: str, email: str, name: str, password: str = "password123") -> dict:
    response = httpx.post(
        f"{api_url}/api/auth/register",
        json={"email": email, "password": password, "name": name},
        timeout=10,
    )
    assert response.status_code == 201, response.text
    return response.json()


def _login_user(api_url: str, email: str, password: str = "password123") -> dict:
    response = httpx.post(
        f"{api_url}/api/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert response.status_code == 200, response.text
    return response.json()


def _set_browser_token(page, frontend_url: str, token: str):
    page.goto(frontend_url)
    page.evaluate("(authToken) => localStorage.setItem('astrovedic_token', authToken)", token)


def _promote_admin(db_path: str, user_id: str):
    with sqlite3.connect(db_path) as connection:
        connection.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        connection.commit()


def _promote_astrologer(db_path: str, user_id: str, display_name: str):
    with sqlite3.connect(db_path) as connection:
        connection.execute("UPDATE users SET role = 'astrologer' WHERE id = ?", (user_id,))
        connection.execute(
            """
            INSERT INTO astrologers
                (user_id, display_name, bio, specializations, experience_years,
                 per_minute_rate, languages, is_available, is_approved)
            VALUES (?, ?, 'Experienced Vedic astrologer', 'Vedic,Tarot,Palmistry', 7, 25.0, '["English","Hindi"]', 1, 1)
            """,
            (user_id, display_name),
        )
        connection.commit()


class TestFrontendSmoke:
    """Browser-level smoke coverage for core frontend routes."""

    def test_blog_index_and_detail_render(self, page, frontend_url):
        page.goto(f"{frontend_url}/blog")
        expect(page.get_by_role("heading", name="AstroVedic Blog")).to_be_visible()
        expect(page).to_have_title("AstroVedic Blog - Practical Astrology, Panchang, Remedies")

        article_link = page.locator('a[href^="/blog/"]').first
        article_href = article_link.get_attribute("href")
        assert article_href and article_href.startswith("/blog/")
        article_link.click()

        page.wait_for_url(f"**{article_href}")
        expect(page.locator("article")).to_be_visible()
        canonical = page.eval_on_selector('link[rel="canonical"]', "node => node.href")
        assert canonical.endswith(article_href)
        assert "AstroVedic Blog" not in page.title()

    def test_palmistry_photo_flow_renders_result(self, page, api_url, frontend_url, tmp_path):
        user = _register_user(api_url, "smoke_palm@test.com", "Palm Smoke User")
        token = user["token"]
        _set_browser_token(page, frontend_url, token)

        image_path = Path(tmp_path) / "palm.png"
        Image.new("RGB", (640, 880), color=(214, 183, 164)).save(image_path)

        page.goto(f"{frontend_url}/palmistry")
        expect(page.get_by_role("heading", name="Palmistry Reading")).to_be_visible()
        page.locator('input[type="file"]').set_input_files(str(image_path))
        page.get_by_role("button", name="Analyze Palm Photo").click()

        expect(page.get_by_role("tab", name="Results")).to_be_enabled()
        expect(page.get_by_role("heading", name="Your Palm Reading")).to_be_visible()
        expect(page.get_by_text("Detected Traits")).to_be_visible()

    def test_admin_dashboard_blog_tab_loads(self, page, api_url, frontend_url, e2e_db_path):
        registration = _register_user(api_url, "smoke_admin@test.com", "Admin Smoke User")
        _promote_admin(e2e_db_path, registration["user"]["id"])
        login = _login_user(api_url, "smoke_admin@test.com")
        _set_browser_token(page, frontend_url, login["token"])

        page.goto(f"{frontend_url}/admin")
        expect(page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()
        page.get_by_role("tab", name="Blog").click()
        expect(page.get_by_role("button", name="Add Blog Post")).to_be_visible()

    def test_astrologer_dashboard_profile_loads(self, page, api_url, frontend_url, e2e_db_path):
        registration = _register_user(api_url, "smoke_astro@test.com", "Astro Smoke User")
        _promote_astrologer(e2e_db_path, registration["user"]["id"], "Smoke Astro")
        login = _login_user(api_url, "smoke_astro@test.com")
        _set_browser_token(page, frontend_url, login["token"])

        page.goto(f"{frontend_url}/astrologer-dashboard")
        expect(page.get_by_role("tab", name="Profile")).to_be_visible()
        page.get_by_role("tab", name="Profile").click()
        expect(page.get_by_text("My Profile")).to_be_visible()

    def test_user_profile_reports_tab_loads(self, page, api_url, frontend_url):
        registration = _register_user(api_url, "smoke_profile@test.com", "Profile Smoke User")
        _set_browser_token(page, frontend_url, registration["token"])

        page.goto(f"{frontend_url}/profile")
        expect(page.get_by_role("tab", name="Reports")).to_be_visible()
        page.get_by_role("tab", name="Reports").click()
        expect(page.get_by_text("My Reports")).to_be_visible()
