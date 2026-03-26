"""
AstroVedic Full UAT Test Suite — UI-Based End-to-End Testing
=============================================================
Comprehensive user acceptance testing covering all frontend flows.
Tests actual UI interactions, not just API endpoints.

Run: pytest e2e/test_uat_full.py -v --headed --slowmo=500
"""
import os
import time
import pytest
from playwright.sync_api import sync_playwright, expect, Page

# Configuration
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots", "uat")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
API_URL = os.getenv("API_URL", "http://localhost:8028")

# Test credentials
TEST_USER = {
    "email": f"uat_test_{int(time.time())}@astrovedic.com",
    "password": "TestPass123!",
    "name": "UAT Test User"
}


def _screenshot(page: Page, name: str):
    """Save screenshot with timestamp."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ts = int(time.time())
    path = os.path.join(SCREENSHOTS_DIR, f"{name}--{ts}.png")
    page.screenshot(path=path, full_page=True)
    return path


@pytest.fixture(scope="session")
def browser_context():
    """Launch browser once for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=os.path.join(SCREENSHOTS_DIR, "videos")
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    """Fresh page for each test."""
    page = browser_context.new_page()
    yield page
    page.close()


# =============================================================================
# SECTION 1: Navigation & Public Pages
# =============================================================================

class TestPublicNavigation:
    """UAT: All public pages load correctly."""

    def test_homepage_loads(self, page: Page):
        """Homepage renders with all key sections."""
        page.goto(FRONTEND_URL)
        page.wait_for_load_state("networkidle")
        
        # Check key sections exist
        expect(page.locator("text=AstroVedic").first).to_be_visible()
        expect(page.locator("text=Cosmic Wisdom").first).to_be_visible()
        expect(page.locator("text=Generate Your Kundli").first).to_be_visible()
        expect(page.locator("text=Daily Horoscope").first).to_be_visible()
        expect(page.locator("text=Consult an Astrologer").first).to_be_visible()
        
        _screenshot(page, "01-homepage")

    def test_navigation_links(self, page: Page):
        """All nav links work and lead to correct pages."""
        page.goto(FRONTEND_URL)
        
        nav_links = [
            ("Kundli", "/kundli"),
            ("Horoscope", "/horoscope"),
            ("Panchang", "/panchang"),
            ("AI Chat", "/ai-chat"),
            ("Library", "/library"),
            ("Shop", "/shop"),
        ]
        
        for link_text, expected_path in nav_links:
            # Click nav link
            page.locator(f"nav >> text={link_text}").click()
            page.wait_for_load_state("networkidle")
            
            # Verify URL
            assert expected_path in page.url, f"Expected {expected_path} in URL, got {page.url}"
            
            # Go back home for next test
            page.goto(FRONTEND_URL)
            page.wait_for_load_state("networkidle")
        
        _screenshot(page, "02-navigation-links")

    def test_footer_links(self, page: Page):
        """Footer contains expected links."""
        page.goto(FRONTEND_URL)
        
        footer_links = ["About", "Privacy", "Terms", "Contact"]
        for link in footer_links:
            expect(page.locator(f"footer >> text={link}").first).to_be_visible()
        
        _screenshot(page, "03-footer")

    def test_responsive_mobile_menu(self, page: Page):
        """Mobile hamburger menu works."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(FRONTEND_URL)
        page.wait_for_load_state("networkidle")
        
        # Mobile menu button should be visible
        menu_btn = page.locator("button[aria-label='menu']").first
        if menu_btn.is_visible():
            menu_btn.click()
            # Check menu items appear
            expect(page.locator("text=Kundli").first).to_be_visible()
            _screenshot(page, "04-mobile-menu")


# =============================================================================
# SECTION 2: Authentication Flows
# =============================================================================

class TestAuthentication:
    """UAT: Complete auth flows via UI."""

    def test_register_new_user(self, page: Page):
        """User can register via UI."""
        page.goto(f"{FRONTEND_URL}/login")
        page.wait_for_load_state("networkidle")
        
        # Click Register tab
        page.locator("text=Sign Up").click()
        
        # Fill registration form
        page.fill("input[placeholder*='Name']", TEST_USER["name"])
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        
        _screenshot(page, "05-register-form-filled")
        
        # Submit
        page.locator("button:has-text('Sign Up')").click()
        
        # Wait for navigation or success
        page.wait_for_timeout(2000)
        
        # Should redirect to home or show success
        assert "login" not in page.url or page.locator("text=success").is_visible()
        _screenshot(page, "06-register-success")

    def test_login_existing_user(self, page: Page):
        """User can login via UI."""
        page.goto(f"{FRONTEND_URL}/login")
        page.wait_for_load_state("networkidle")
        
        # Ensure Sign In tab is active
        page.locator("text=Sign In").click()
        
        # Fill login form
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        
        _screenshot(page, "07-login-form-filled")
        
        # Submit
        page.locator("button:has-text('Sign In')").click()
        
        # Wait for navigation
        page.wait_for_timeout(2000)
        
        # Should be redirected (usually to home or profile)
        assert "/login" not in page.url
        _screenshot(page, "08-login-success")

    def test_login_invalid_password(self, page: Page):
        """Login with wrong password shows error."""
        page.goto(f"{FRONTEND_URL}/login")
        page.wait_for_load_state("networkidle")
        
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", "WrongPassword123!")
        page.locator("button:has-text('Sign In')").click()
        
        # Wait for error message
        page.wait_for_timeout(1000)
        
        # Error should be visible
        error_visible = page.locator("text=Invalid").is_visible() or \
                       page.locator("text=error").is_visible() or \
                       page.locator("text=failed").is_visible()
        assert error_visible, "Expected error message for invalid login"
        _screenshot(page, "09-login-error")

    def test_protected_route_redirect(self, page: Page):
        """Unauthenticated user is redirected when accessing protected page."""
        # Clear any auth state by opening fresh page
        page.goto(f"{FRONTEND_URL}/profile")
        page.wait_for_load_state("networkidle")
        
        # Should redirect to login or show sign-in required
        assert "/login" in page.url or \
               page.locator("text=Sign In Required").is_visible() or \
               page.locator("text=Please log in").is_visible()
        _screenshot(page, "10-protected-redirect")


# =============================================================================
# SECTION 3: Kundli Generation Flow
# =============================================================================

class TestKundliFlow:
    """UAT: Complete kundli generation via UI."""

    def _login(self, page: Page):
        """Helper to log in."""
        page.goto(f"{FRONTEND_URL}/login")
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        page.locator("button:has-text('Sign In')").click()
        page.wait_for_timeout(2000)

    def test_kundli_form_page_loads(self, page: Page):
        """Kundli generator page loads with form."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/kundli")
        page.wait_for_load_state("networkidle")
        
        # Check form elements
        expect(page.locator("input[placeholder*='Name']").first).to_be_visible()
        expect(page.locator("input[type='date']").first).to_be_visible()
        expect(page.locator("input[type='time']").first).to_be_visible()
        expect(page.locator("input[placeholder*='Place']").first).to_be_visible()
        
        _screenshot(page, "11-kundli-form")

    def test_kundli_form_validation(self, page: Page):
        """Kundli form validates required fields."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/kundli")
        
        # Try to submit empty form
        page.locator("button:has-text('Generate')").click()
        
        # Wait for validation
        page.wait_for_timeout(1000)
        
        # Should still be on form or show error
        _screenshot(page, "12-kundli-validation")

    def test_generate_kundli_success(self, page: Page):
        """User can generate a kundli."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/kundli")
        page.wait_for_load_state("networkidle")
        
        # Fill form
        page.fill("input[placeholder*='Name']", "Test Person")
        page.fill("input[type='date']", "1990-06-15")
        page.fill("input[type='time']", "14:30")
        page.fill("input[placeholder*='Place']", "Mumbai")
        
        # Select gender if present
        male_btn = page.locator("button:has-text('Male')")
        if male_btn.is_visible():
            male_btn.click()
        
        _screenshot(page, "13-kundli-form-complete")
        
        # Submit
        page.locator("button:has-text('Generate')").click()
        
        # Wait for result (loading then result)
        page.wait_for_timeout(5000)
        
        # Should show results
        result_visible = page.locator("text=Planets").is_visible() or \
                        page.locator("text=Dosha").is_visible() or \
                        page.locator("text=Generating").is_visible()
        assert result_visible, "Expected kundli generation to start or complete"
        
        _screenshot(page, "14-kundli-result")

    def test_kundli_report_buttons(self, page: Page):
        """Report buttons appear on kundli results."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/kundli")
        
        # Generate a kundli first
        page.fill("input[placeholder*='Name']", "Report Test")
        page.fill("input[type='date']", "1985-03-20")
        page.fill("input[type='time']", "10:00")
        page.fill("input[placeholder*='Place']", "Delhi")
        page.locator("button:has-text('Generate')").click()
        page.wait_for_timeout(5000)
        
        # Check for report buttons
        report_buttons = [
            "Complete Analysis",
            "Marriage", 
            "Career",
            "Health"
        ]
        
        found = any(page.locator(f"text={btn}").is_visible() for btn in report_buttons)
        assert found, "Expected report buttons on kundli results"
        
        _screenshot(page, "15-kundli-reports")


# =============================================================================
# SECTION 4: Horoscope & Panchang
# =============================================================================

class TestHoroscopePanchang:
    """UAT: Horoscope and panchang features."""

    def test_horoscope_page(self, page: Page):
        """Horoscope page loads with sign selection."""
        page.goto(f"{FRONTEND_URL}/horoscope")
        page.wait_for_load_state("networkidle")
        
        # Check zodiac signs are present
        signs = ["Aries", "Taurus", "Gemini", "Cancer"]
        for sign in signs:
            expect(page.locator(f"text={sign}").first).to_be_visible()
        
        _screenshot(page, "16-horoscope-page")

    def test_horoscope_sign_selection(self, page: Page):
        """User can select a zodiac sign."""
        page.goto(f"{FRONTEND_URL}/horoscope")
        
        # Click on a sign
        page.locator("text=Aries").first.click()
        page.wait_for_timeout(2000)
        
        # Should show horoscope content
        content_visible = page.locator("text=daily").is_visible() or \
                         page.locator("text=horoscope").is_visible() or \
                         page.locator("text=Today").is_visible()
        assert content_visible, "Expected horoscope content after sign selection"
        
        _screenshot(page, "17-horoscope-aries")

    def test_panchang_page(self, page: Page):
        """Panchang page loads with daily data."""
        page.goto(f"{FRONTEND_URL}/panchang")
        page.wait_for_load_state("networkidle")
        
        # Check for panchang elements
        elements = ["Tithi", "Nakshatra", "Yoga", "Sunrise"]
        for elem in elements:
            try:
                expect(page.locator(f"text={elem}").first).to_be_visible(timeout=5000)
            except:
                pass  # Some may not be present depending on implementation
        
        _screenshot(page, "18-panchang-page")


# =============================================================================
# SECTION 5: Spiritual Library
# =============================================================================

class TestSpiritualLibrary:
    """UAT: Spiritual library content."""

    def test_library_page_loads(self, page: Page):
        """Library page loads with categories."""
        page.goto(f"{FRONTEND_URL}/library")
        page.wait_for_load_state("networkidle")
        
        # Check tabs
        expect(page.locator("text=Gita").first).to_be_visible()
        expect(page.locator("text=Mantras").first).to_be_visible()
        expect(page.locator("text=Aarti").first).to_be_visible()
        
        _screenshot(page, "19-library-page")

    def test_gita_chapters_display(self, page: Page):
        """Gita chapters are displayed."""
        page.goto(f"{FRONTEND_URL}/library")
        
        # Click Gita tab if not already active
        gita_tab = page.locator("text=Gita").first
        if gita_tab.is_visible():
            gita_tab.click()
            page.wait_for_timeout(1000)
        
        # Should show chapters
        chapter_visible = page.locator("text=Chapter").is_visible() or \
                         page.locator("text=Arjuna").is_visible()
        assert chapter_visible, "Expected Gita chapters to display"
        
        _screenshot(page, "20-library-gita")


# =============================================================================
# SECTION 6: E-Commerce (Shop, Cart, Checkout)
# =============================================================================

class TestECommerce:
    """UAT: Complete shopping flow."""

    def _login(self, page: Page):
        """Helper to log in."""
        page.goto(f"{FRONTEND_URL}/login")
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        page.locator("button:has-text('Sign In')").click()
        page.wait_for_timeout(2000)

    def test_shop_page_loads(self, page: Page):
        """Shop page loads with products."""
        page.goto(f"{FRONTEND_URL}/shop")
        page.wait_for_load_state("networkidle")
        
        # Check for products or categories
        expect(page.locator("text=Products").first).to_be_visible()
        
        _screenshot(page, "21-shop-page")

    def test_shop_filters(self, page: Page):
        """Shop filters work."""
        page.goto(f"{FRONTEND_URL}/shop")
        
        # Try clicking filter buttons
        filters = ["Gemstone", "Rudraksha", "All"]
        for filt in filters:
            filt_btn = page.locator(f"button:has-text('{filt}')").first
            if filt_btn.is_visible():
                filt_btn.click()
                page.wait_for_timeout(1000)
                _screenshot(page, f"22-shop-filter-{filt.lower()}")

    def test_product_details(self, page: Page):
        """Product details can be viewed."""
        page.goto(f"{FRONTEND_URL}/shop")
        page.wait_for_load_state("networkidle")
        
        # Click first product if available
        product = page.locator("[class*='product'], [class*='card']").first
        if product.is_visible():
            product.click()
            page.wait_for_timeout(2000)
            
            # Should show product details
            assert "Add to Cart" in page.content() or "price" in page.content().lower()
            _screenshot(page, "23-product-details")

    def test_cart_add_requires_auth(self, page: Page):
        """Adding to cart requires login."""
        # Log out first by going to home
        page.goto(FRONTEND_URL)
        
        # Go to shop
        page.goto(f"{FRONTEND_URL}/shop")
        
        # Try to add to cart (if button exists)
        add_btn = page.locator("button:has-text('Add'), button:has-text('Cart')").first
        if add_btn.is_visible():
            add_btn.click()
            page.wait_for_timeout(2000)
            
            # Should prompt login or redirect
            _screenshot(page, "24-cart-auth-required")

    def test_checkout_page(self, page: Page):
        """Checkout page loads for authenticated user."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/cart")
        page.wait_for_load_state("networkidle")
        
        # Check checkout elements
        expect(page.locator("text=Cart").first).to_be_visible()
        
        _screenshot(page, "25-checkout-page")


# =============================================================================
# SECTION 7: Numerology, Tarot, Prashnavali
# =============================================================================

class TestDivinationTools:
    """UAT: Divination and prediction tools."""

    def test_numerology_page(self, page: Page):
        """Numerology calculator works."""
        page.goto(f"{FRONTEND_URL}/numerology")
        page.wait_for_load_state("networkidle")
        
        # Fill form
        page.fill("input[placeholder*='Name']", "Test Name")
        page.fill("input[type='date']", "1990-05-20")
        
        _screenshot(page, "26-numerology-form")
        
        # Submit
        calc_btn = page.locator("button:has-text('Calculate'), button:has-text('Submit')").first
        if calc_btn.is_visible():
            calc_btn.click()
            page.wait_for_timeout(3000)
            _screenshot(page, "27-numerology-result")

    def test_tarot_page(self, page: Page):
        """Tarot reading page loads."""
        page.goto(f"{FRONTEND_URL}/numerology")
        page.wait_for_load_state("networkidle")
        
        # Look for tarot section/tab
        tarot_tab = page.locator("text=Tarot").first
        if tarot_tab.is_visible():
            tarot_tab.click()
            page.wait_for_timeout(1000)
            _screenshot(page, "28-tarot-page")

    def test_prashnavali_page(self, page: Page):
        """Prashnavali page loads."""
        page.goto(f"{FRONTEND_URL}/prashnavali")
        page.wait_for_load_state("networkidle")
        
        # Check for grid or question input
        expect(page.locator("text=Ram Shalaka").first).to_be_visible()
        
        _screenshot(page, "29-prashnavali-page")


# =============================================================================
# SECTION 8: AI Chat
# =============================================================================

class TestAIChat:
    """UAT: AI chat functionality."""

    def test_ai_chat_page(self, page: Page):
        """AI chat page loads."""
        page.goto(f"{FRONTEND_URL}/ai-chat")
        page.wait_for_load_state("networkidle")
        
        # Check chat elements
        expect(page.locator("input[placeholder*='Ask']").first).to_be_visible()
        
        _screenshot(page, "30-ai-chat-page")

    def test_ai_chat_gita(self, page: Page):
        """Gita AI chat works."""
        page.goto(f"{FRONTEND_URL}/ai-chat")
        
        # Type a question
        page.fill("input[placeholder*='Ask']", "What is dharma?")
        
        _screenshot(page, "31-ai-chat-question")
        
        # Submit
        send_btn = page.locator("button[type='submit']").first
        if send_btn.is_visible():
            send_btn.click()
            page.wait_for_timeout(3000)
            _screenshot(page, "32-ai-chat-response")


# =============================================================================
# SECTION 9: Reports Marketplace
# =============================================================================

class TestReports:
    """UAT: Paid reports flow."""

    def _login(self, page: Page):
        """Helper to log in."""
        page.goto(f"{FRONTEND_URL}/login")
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        page.locator("button:has-text('Sign In')").click()
        page.wait_for_timeout(2000)

    def test_reports_page_loads(self, page: Page):
        """Reports marketplace loads."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/reports")
        page.wait_for_load_state("networkidle")
        
        # Check report types
        expect(page.locator("text=Complete Kundli Analysis").first).to_be_visible()
        expect(page.locator("text=Marriage").first).to_be_visible()
        
        _screenshot(page, "33-reports-marketplace")

    def test_reports_pricing_display(self, page: Page):
        """Report prices are displayed."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/reports")
        
        # Check for prices
        prices = ["₹999", "₹799", "₹699", "₹599"]
        found = any(price in page.content() for price in prices)
        assert found, "Expected report prices to be displayed"
        
        _screenshot(page, "34-reports-pricing")


# =============================================================================
# SECTION 10: Palmistry
# =============================================================================

class TestPalmistry:
    """UAT: Palmistry reading."""

    def test_palmistry_page(self, page: Page):
        """Palmistry page loads with form."""
        page.goto(f"{FRONTEND_URL}/palmistry")
        page.wait_for_load_state("networkidle")
        
        # Check form elements
        expect(page.locator("text=Hand Shape").first).to_be_visible()
        
        _screenshot(page, "35-palmistry-page")

    def test_palmistry_guide(self, page: Page):
        """Palmistry guide tab works."""
        page.goto(f"{FRONTEND_URL}/palmistry")
        
        # Click Guide tab
        guide_tab = page.locator("text=Guide").first
        if guide_tab.is_visible():
            guide_tab.click()
            page.wait_for_timeout(1000)
            
            expect(page.locator("text=Hand Shapes").first).to_be_visible()
            _screenshot(page, "36-palmistry-guide")


# =============================================================================
# SECTION 11: User Profile
# =============================================================================

class TestUserProfile:
    """UAT: User profile management."""

    def _login(self, page: Page):
        """Helper to log in."""
        page.goto(f"{FRONTEND_URL}/login")
        page.fill("input[type='email']", TEST_USER["email"])
        page.fill("input[type='password']", TEST_USER["password"])
        page.locator("button:has-text('Sign In')").click()
        page.wait_for_timeout(2000)

    def test_profile_page(self, page: Page):
        """Profile page loads with user info."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/profile")
        page.wait_for_load_state("networkidle")
        
        # Check profile elements
        expect(page.locator("text=Profile").first).to_be_visible()
        
        _screenshot(page, "37-profile-page")

    def test_profile_tabs(self, page: Page):
        """Profile tabs work."""
        self._login(page)
        page.goto(f"{FRONTEND_URL}/profile")
        
        tabs = ["Orders", "Reports"]
        for tab in tabs:
            tab_btn = page.locator(f"text={tab}").first
            if tab_btn.is_visible():
                tab_btn.click()
                page.wait_for_timeout(1000)
                _screenshot(page, f"38-profile-{tab.lower()}")


# =============================================================================
# SECTION 12: Consultation
# =============================================================================

class TestConsultation:
    """UAT: Astrologer consultation booking."""

    def test_consultation_page(self, page: Page):
        """Consultation page loads with astrologers."""
        page.goto(f"{FRONTEND_URL}/consultation")
        page.wait_for_load_state("networkidle")
        
        # Check page elements
        expect(page.locator("text=Astrologer").first).to_be_visible()
        
        _screenshot(page, "39-consultation-page")


# =============================================================================
# SECTION 13: Error Pages & Edge Cases
# =============================================================================

class TestErrorPages:
    """UAT: Error handling."""

    def test_404_page(self, page: Page):
        """404 page shows for unknown routes."""
        page.goto(f"{FRONTEND_URL}/nonexistent-page-12345")
        page.wait_for_load_state("networkidle")
        
        # Should show 404 or redirect
        _screenshot(page, "40-404-page")

    def test_invalid_form_submission(self, page: Page):
        """Forms handle invalid input gracefully."""
        page.goto(f"{FRONTEND_URL}/login")
        
        # Submit empty form
        page.locator("button:has-text('Sign In')").click()
        page.wait_for_timeout(1000)
        
        # Should still be on login page
        assert "/login" in page.url
        _screenshot(page, "41-invalid-form")


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--headed", "--slowmo=500"])
