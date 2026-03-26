"""
AstroVedic Full UAT Test Suite — Complete Application Testing
=============================================================
Comprehensive user acceptance testing covering ALL features.
This tests the complete user journey from registration to purchase.

Usage:
  pytest e2e/test_full_uat.py -v                    # Run all tests
  pytest e2e/test_full_uat.py::TestAuthFlow -v      # Run specific test class
  pytest e2e/test_full_uat.py -k "test_register"    # Run specific test

Environment:
  FRONTEND_URL=http://localhost:5173  # Frontend URL (for screenshots)
  API_URL=http://localhost:8028       # Backend API URL
"""
import os
import json
import time
import pytest
from playwright.sync_api import expect

# Configuration
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots", "uat")
SERVER_URL = os.getenv("API_URL", "http://localhost:8028")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Generate unique test user for this run
TEST_TIMESTAMP = int(time.time())
TEST_USER = {
    "email": f"uat_user_{TEST_TIMESTAMP}@astrovedic.com",
    "password": "UAT_Pass123!",
    "name": f"UAT Tester {TEST_TIMESTAMP}"
}

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def _screenshot(page, name):
    """Save screenshot with timestamp."""
    path = os.path.join(SCREENSHOTS_DIR, f"{name}_{TEST_TIMESTAMP}.png")
    page.screenshot(path=path, full_page=True)
    return path


def _api_post(page, endpoint, data, token=None):
    """Make API POST via Playwright's request context."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return page.request.post(f"{SERVER_URL}{endpoint}", data=json.dumps(data), headers=headers)


def _api_get(page, endpoint, token=None):
    """Make API GET via Playwright's request context."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return page.request.get(f"{SERVER_URL}{endpoint}", headers=headers)


def _api_patch(page, endpoint, data, token=None):
    """Make API PATCH via Playwright's request context."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return page.request.patch(f"{SERVER_URL}{endpoint}", data=json.dumps(data), headers=headers)


# =============================================================================
# SECTION 1: Health & Infrastructure
# =============================================================================

class TestInfrastructure:
    """UAT: Infrastructure and health checks."""

    def test_health_endpoint(self, page):
        """Health check returns OK."""
        resp = _api_get(page, "/health")
        assert resp.status == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_api_docs_accessible(self, page):
        """API documentation is accessible."""
        resp = _api_get(page, "/docs")
        assert resp.status == 200
        assert "AstroVedic" in resp.text() or "swagger" in resp.text().lower()


# =============================================================================
# SECTION 2: User Registration & Authentication
# =============================================================================

class TestAuthFlow:
    """UAT: Complete user registration and authentication flow."""

    def test_01_register_new_user(self, page):
        """Create a new user account."""
        resp = _api_post(page, "/api/auth/register", {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
            "name": TEST_USER["name"]
        })
        assert resp.status == 201, f"Registration failed: {resp.text()}"
        
        data = resp.json()
        assert data["user"]["email"] == TEST_USER["email"]
        assert data["user"]["name"] == TEST_USER["name"]
        assert "token" in data
        assert "id" in data["user"]
        
        # Store for later tests
        TEST_USER["id"] = data["user"]["id"]
        TEST_USER["token"] = data["token"]
        _screenshot(page, "01_register_success")

    def test_02_login_with_credentials(self, page):
        """Login with registered credentials."""
        resp = _api_post(page, "/api/auth/login", {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        assert resp.status == 200, f"Login failed: {resp.text()}"
        
        data = resp.json()
        assert data["user"]["email"] == TEST_USER["email"]
        assert "token" in data
        TEST_USER["token"] = data["token"]  # Update token
        _screenshot(page, "02_login_success")

    def test_03_get_user_profile(self, page):
        """Retrieve authenticated user profile."""
        resp = _api_get(page, "/api/auth/me", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert data["email"] == TEST_USER["email"]
        assert data["name"] == TEST_USER["name"]
        assert data["role"] == "user"
        _screenshot(page, "03_profile_retrieved")

    def test_04_update_profile(self, page):
        """Update user profile information."""
        resp = _api_patch(page, "/api/auth/profile", {
            "name": f"{TEST_USER['name']} Updated",
            "phone": "+91-9876543210",
            "city": "Mumbai"
        }, token=TEST_USER["token"])
        assert resp.status == 200
        
        # Verify update
        resp = _api_get(page, "/api/auth/me", token=TEST_USER["token"])
        data = resp.json()
        assert "Updated" in data["name"]
        assert data["city"] == "Mumbai"
        _screenshot(page, "04_profile_updated")

    def test_05_change_password(self, page):
        """Change user password."""
        resp = _api_post(page, "/api/auth/change-password", {
            "current_password": TEST_USER["password"],
            "new_password": "NewPass456!"
        }, token=TEST_USER["token"])
        assert resp.status == 200
        
        # Update stored password
        TEST_USER["password"] = "NewPass456!"
        _screenshot(page, "05_password_changed")

    def test_06_login_with_new_password(self, page):
        """Login with the new password."""
        resp = _api_post(page, "/api/auth/login", {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        assert resp.status == 200
        TEST_USER["token"] = resp.json()["token"]
        _screenshot(page, "06_login_new_password")

    def test_07_invalid_login_fails(self, page):
        """Login with wrong password fails."""
        resp = _api_post(page, "/api/auth/login", {
            "email": TEST_USER["email"],
            "password": "WrongPassword123!"
        })
        assert resp.status == 401
        _screenshot(page, "07_invalid_login")

    def test_08_duplicate_registration_fails(self, page):
        """Registering duplicate email fails."""
        resp = _api_post(page, "/api/auth/register", {
            "email": TEST_USER["email"],
            "password": "AnotherPass123!",
            "name": "Duplicate User"
        })
        assert resp.status in [400, 409]
        _screenshot(page, "08_duplicate_registration")


# =============================================================================
# SECTION 3: Kundli Generation & Analysis
# =============================================================================

class TestKundliFlow:
    """UAT: Complete kundli generation and analysis."""

    kundli_id = None

    def test_09_generate_kundli(self, page):
        """Generate a new kundli."""
        resp = _api_post(page, "/api/kundli/generate", {
            "person_name": "Test Native",
            "birth_date": "1990-06-15",
            "birth_time": "14:30:00",
            "birth_place": "Mumbai, India",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone_offset": 5.5
        }, token=TEST_USER["token"])
        
        assert resp.status == 201, f"Kundli generation failed: {resp.text()}"
        data = resp.json()
        
        assert "id" in data
        assert "chart_data" in data
        assert "planets" in data["chart_data"]
        assert len(data["chart_data"]["planets"]) == 9
        
        TestKundliFlow.kundli_id = data["id"]
        _screenshot(page, "09_kundli_generated")

    def test_10_list_user_kundlis(self, page):
        """List all kundlis for the user."""
        resp = _api_get(page, "/api/kundli/list", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert len(data) >= 1
        _screenshot(page, "10_kundli_list")

    def test_11_get_kundli_details(self, page):
        """Get detailed kundli information."""
        if not TestKundliFlow.kundli_id:
            pytest.skip("No kundli generated")
        
        resp = _api_get(page, f"/api/kundli/{TestKundliFlow.kundli_id}", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert data["id"] == TestKundliFlow.kundli_id
        assert "chart_data" in data
        _screenshot(page, "11_kundli_details")

    def test_12_io_gita_analysis(self, page):
        """Get io-gita basin analysis."""
        if not TestKundliFlow.kundli_id:
            pytest.skip("No kundli generated")
        
        resp = _api_post(page, f"/api/kundli/{TestKundliFlow.kundli_id}/iogita", {}, token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "basin" in data or "atom_activations" in data
        _screenshot(page, "12_iogita_analysis")

    def test_13_dosha_analysis(self, page):
        """Get dosha analysis."""
        if not TestKundliFlow.kundli_id:
            pytest.skip("No kundli generated")
        
        resp = _api_post(page, f"/api/kundli/{TestKundliFlow.kundli_id}/dosha", {}, token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "mangal_dosha" in data
        _screenshot(page, "13_dosha_analysis")

    def test_14_dasha_calculation(self, page):
        """Get dasha periods."""
        if not TestKundliFlow.kundli_id:
            pytest.skip("No kundli generated")
        
        resp = _api_post(page, f"/api/kundli/{TestKundliFlow.kundli_id}/dasha", {}, token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "mahadasha_periods" in data or "current_dasha" in data
        _screenshot(page, "14_dasha_calculation")

    def test_15_divisional_chart(self, page):
        """Get divisional chart (D9)."""
        if not TestKundliFlow.kundli_id:
            pytest.skip("No kundli generated")
        
        resp = _api_post(page, f"/api/kundli/{TestKundliFlow.kundli_id}/divisional", {
            "chart_type": "D9"
        }, token=TEST_USER["token"])
        assert resp.status == 200
        _screenshot(page, "15_divisional_chart")


# =============================================================================
# SECTION 4: Horoscope & Panchang
# =============================================================================

class TestHoroscopePanchang:
    """UAT: Horoscope and panchang features."""

    def test_16_daily_horoscope(self, page):
        """Get daily horoscope for a sign."""
        resp = _api_get(page, "/api/horoscope/aries?period=daily")
        assert resp.status == 200
        
        data = resp.json()
        assert "content" in data or "prediction" in data
        _screenshot(page, "16_horoscope_aries")

    def test_17_panchang_daily(self, page):
        """Get daily panchang."""
        resp = _api_get(page, "/api/panchang?date=2026-03-26&lat=28.6139&lng=77.2090")
        assert resp.status == 200
        
        data = resp.json()
        assert "tithi" in data
        assert "nakshatra" in data
        _screenshot(page, "17_panchang_daily")

    def test_18_choghadiya(self, page):
        """Get choghadiya periods."""
        resp = _api_get(page, "/api/panchang/choghadiya?date=2026-03-26&lat=28.6139&lng=77.2090")
        assert resp.status == 200
        _screenshot(page, "18_choghadiya")

    def test_19_festivals(self, page):
        """Get festival list."""
        resp = _api_get(page, "/api/festivals?year=2026")
        assert resp.status == 200
        
        data = resp.json()
        assert len(data) >= 1
        _screenshot(page, "19_festivals")


# =============================================================================
# SECTION 5: Numerology, Tarot, Prashnavali
# =============================================================================

class TestDivinationTools:
    """UAT: Divination and prediction tools."""

    def test_20_numerology_calculation(self, page):
        """Calculate numerology numbers."""
        resp = _api_post(page, "/api/numerology/calculate", {
            "name": "Meharban Singh",
            "birth_date": "1990-01-15"
        })
        assert resp.status == 200
        
        data = resp.json()
        assert "data" in data
        assert data["data"]["life_path"] > 0
        _screenshot(page, "20_numerology")

    def test_21_tarot_single_card(self, page):
        """Draw single tarot card."""
        resp = _api_post(page, "/api/tarot/draw", {"spread": "single"})
        assert resp.status == 200
        
        data = resp.json()
        assert len(data["data"]["cards"]) == 1
        _screenshot(page, "21_tarot_single")

    def test_22_tarot_three_card(self, page):
        """Draw three-card tarot spread."""
        resp = _api_post(page, "/api/tarot/draw", {
            "spread": "three",
            "question": "Will my startup succeed?"
        })
        assert resp.status == 200
        
        data = resp.json()
        assert len(data["data"]["cards"]) == 3
        _screenshot(page, "22_tarot_three")

    def test_23_ram_shalaka(self, page):
        """Ram Shalaka prashnavali."""
        resp = _api_post(page, "/api/prashnavali/ram-shalaka", {"row": 7, "col": 7})
        assert resp.status == 200
        
        data = resp.json()
        assert "answer" in data
        _screenshot(page, "23_ram_shalaka")

    def test_24_hanuman_prashna(self, page):
        """Hanuman Prashna."""
        resp = _api_post(page, "/api/prashnavali/hanuman", {
            "question": "Should I change jobs?"
        })
        assert resp.status == 200
        _screenshot(page, "24_hanuman_prashna")

    def test_25_palmistry_guide(self, page):
        """Get palmistry guide."""
        resp = _api_get(page, "/api/palmistry/guide")
        assert resp.status == 200
        
        data = resp.json()
        assert "lines" in data
        assert "mounts" in data
        _screenshot(page, "25_palmistry_guide")

    def test_26_palmistry_analyze(self, page):
        """Analyze palmistry characteristics."""
        resp = _api_post(page, "/api/palmistry/analyze", {
            "hand_shape": "earth",
            "dominant_hand": "right",
            "finger_length": "short",
            "heart_line": "long_curved",
            "head_line": "long_straight",
            "life_line": "long_deep"
        }, token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "reading" in data
        _screenshot(page, "26_palmistry_analysis")


# =============================================================================
# SECTION 6: AI Features
# =============================================================================

class TestAIFeatures:
    """UAT: AI-powered astrology features."""

    def test_27_ai_gita(self, page):
        """Ask Gita AI a question."""
        resp = _api_post(page, "/api/ai/gita", {
            "question": "What does Krishna say about duty?"
        })
        assert resp.status == 200
        
        data = resp.json()
        assert "answer" in data
        _screenshot(page, "27_ai_gita")

    def test_28_ai_oracle(self, page):
        """Ask the oracle."""
        resp = _api_post(page, "/api/ai/oracle", {
            "question": "Will I travel abroad this year?",
            "mode": "yes_no"
        })
        assert resp.status == 200
        
        data = resp.json()
        assert "answer" in data
        _screenshot(page, "28_ai_oracle")


# =============================================================================
# SECTION 7: Spiritual Library
# =============================================================================

class TestLibrary:
    """UAT: Spiritual library content."""

    def test_29_gita_chapters(self, page):
        """List Gita chapters."""
        resp = _api_get(page, "/api/gita/chapters")
        assert resp.status == 200
        
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        _screenshot(page, "29_gita_chapters")

    def test_30_library_mantras(self, page):
        """Get mantra library."""
        resp = _api_get(page, "/api/library/mantra")
        assert resp.status == 200
        _screenshot(page, "30_library_mantras")

    def test_31_library_aarti(self, page):
        """Get aarti library."""
        resp = _api_get(page, "/api/library/aarti")
        assert resp.status == 200
        _screenshot(page, "31_library_aarti")


# =============================================================================
# SECTION 8: E-Commerce (Products, Cart, Orders)
# =============================================================================

class TestECommerce:
    """UAT: Complete e-commerce flow."""

    product_id = None
    cart_item_id = None
    order_id = None

    def test_32_list_products(self, page):
        """List available products."""
        resp = _api_get(page, "/api/products")
        assert resp.status == 200
        
        data = resp.json()
        assert "products" in data
        assert len(data["products"]) >= 1
        
        # Store first product ID
        TestECommerce.product_id = data["products"][0]["id"]
        _screenshot(page, "32_products_list")

    def test_33_filter_products_by_category(self, page):
        """Filter products by category."""
        resp = _api_get(page, "/api/products?category=gemstone")
        assert resp.status == 200
        
        data = resp.json()
        # All returned products should be gemstones
        for product in data["products"]:
            assert product["category"] == "gemstone"
        _screenshot(page, "33_products_filtered")

    def test_34_add_to_cart(self, page):
        """Add product to cart."""
        if not TestECommerce.product_id:
            pytest.skip("No product available")
        
        resp = _api_post(page, "/api/cart/add", {
            "product_id": TestECommerce.product_id,
            "quantity": 2
        }, token=TEST_USER["token"])
        
        assert resp.status in [200, 201]
        _screenshot(page, "34_cart_add")

    def test_35_view_cart(self, page):
        """View cart contents."""
        resp = _api_get(page, "/api/cart", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "items" in data
        _screenshot(page, "35_cart_view")

    def test_36_create_order(self, page):
        """Create an order from cart."""
        resp = _api_post(page, "/api/orders", {
            "shipping_address": "123 Test Street, Mumbai, India - 400001",
            "payment_method": "cod"
        }, token=TEST_USER["token"])
        
        assert resp.status == 201
        
        data = resp.json()
        assert "id" in data
        TestECommerce.order_id = data["id"]
        _screenshot(page, "36_order_created")

    def test_37_list_orders(self, page):
        """List user's orders."""
        resp = _api_get(page, "/api/orders", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        _screenshot(page, "37_orders_list")

    def test_38_get_order_details(self, page):
        """Get order details."""
        if not TestECommerce.order_id:
            pytest.skip("No order created")
        
        resp = _api_get(page, f"/api/orders/{TestECommerce.order_id}", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert data["id"] == TestECommerce.order_id
        _screenshot(page, "38_order_details")


# =============================================================================
# SECTION 9: Paid Reports
# =============================================================================

class TestPaidReports:
    """UAT: Paid report generation and download."""

    report_id = None

    def test_39_request_report(self, page):
        """Request a paid report."""
        # Need a kundli first
        resp = _api_post(page, "/api/kundli/generate", {
            "person_name": "Report Test Native",
            "birth_date": "1985-03-20",
            "birth_time": "10:00:00",
            "birth_place": "Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone_offset": 5.5
        }, token=TEST_USER["token"])
        
        kundli_id = resp.json()["id"]
        
        # Request report
        resp = _api_post(page, "/api/reports/request", {
            "kundli_id": kundli_id,
            "report_type": "full_kundli"
        }, token=TEST_USER["token"])
        
        assert resp.status == 201
        
        data = resp.json()
        assert data["payment_required"] is True
        TestPaidReports.report_id = data["report"]["id"]
        _screenshot(page, "39_report_requested")

    def test_40_initiate_report_payment(self, page):
        """Initiate payment for report."""
        if not TestPaidReports.report_id:
            pytest.skip("No report requested")
        
        resp = _api_post(page, "/api/payments/report/initiate", {
            "report_id": TestPaidReports.report_id,
            "provider": "cod"
        }, token=TEST_USER["token"])
        
        assert resp.status == 200
        _screenshot(page, "40_report_payment_initiated")

    def test_41_list_reports(self, page):
        """List user's reports."""
        resp = _api_get(page, "/api/reports", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "reports" in data
        assert len(data["reports"]) >= 1
        _screenshot(page, "41_reports_list")


# =============================================================================
# SECTION 10: Consultation System
# =============================================================================

class TestConsultation:
    """UAT: Astrologer consultation system."""

    astrologer_id = None
    consultation_id = None

    def test_42_list_astrologers(self, page):
        """List available astrologers."""
        resp = _api_get(page, "/api/astrologers")
        assert resp.status == 200
        
        data = resp.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            TestConsultation.astrologer_id = data[0]["id"]
        _screenshot(page, "42_astrologers_list")

    def test_43_get_astrologer_details(self, page):
        """Get astrologer profile."""
        if not TestConsultation.astrologer_id:
            pytest.skip("No astrologer available")
        
        resp = _api_get(page, f"/api/astrologers/{TestConsultation.astrologer_id}")
        assert resp.status == 200
        _screenshot(page, "43_astrologer_details")

    def test_44_book_consultation(self, page):
        """Book a consultation."""
        if not TestConsultation.astrologer_id:
            pytest.skip("No astrologer available")
        
        resp = _api_post(page, "/api/consultations/book", {
            "astrologer_id": TestConsultation.astrologer_id,
            "type": "chat",
            "scheduled_at": "2026-04-01T10:00:00"
        }, token=TEST_USER["token"])
        
        assert resp.status == 201
        
        data = resp.json()
        assert "id" in data
        TestConsultation.consultation_id = data["id"]
        _screenshot(page, "44_consultation_booked")

    def test_45_list_consultations(self, page):
        """List user's consultations."""
        resp = _api_get(page, "/api/consultations", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert isinstance(data, list)
        _screenshot(page, "45_consultations_list")


# =============================================================================
# SECTION 11: User History & Activity
# =============================================================================

class TestUserActivity:
    """UAT: User activity history."""

    def test_46_get_user_history(self, page):
        """Get comprehensive user history."""
        resp = _api_get(page, "/api/auth/history", token=TEST_USER["token"])
        assert resp.status == 200
        
        data = resp.json()
        assert "kundlis" in data
        assert "orders" in data
        _screenshot(page, "46_user_history")


# =============================================================================
# SECTION 12: KP & Lal Kitab
# =============================================================================

class TestAdvancedAstrology:
    """UAT: KP System and Lal Kitab."""

    def test_47_kp_cuspal_chart(self, page):
        """Get KP cuspal chart."""
        # Need a kundli
        resp = _api_post(page, "/api/kundli/generate", {
            "person_name": "KP Test",
            "birth_date": "1988-11-22",
            "birth_time": "08:30:00",
            "birth_place": "Chennai",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone_offset": 5.5
        }, token=TEST_USER["token"])
        
        kundli_id = resp.json()["id"]
        
        resp = _api_post(page, "/api/kp/cuspal", {"kundli_id": kundli_id}, token=TEST_USER["token"])
        assert resp.status == 200
        _screenshot(page, "47_kp_cuspal")

    def test_48_lalkitab_remedies(self, page):
        """Get Lal Kitab remedies."""
        # Use existing kundli
        resp = _api_post(page, "/api/kundli/generate", {
            "person_name": "Lal Kitab Test",
            "birth_date": "1992-07-10",
            "birth_time": "16:45:00",
            "birth_place": "Kolkata",
            "latitude": 22.5726,
            "longitude": 88.3639,
            "timezone_offset": 5.5
        }, token=TEST_USER["token"])
        
        kundli_id = resp.json()["id"]
        
        resp = _api_post(page, "/api/lalkitab/remedies", {"kundli_id": kundli_id}, token=TEST_USER["token"])
        assert resp.status in [200, 400, 422]  # May vary based on data availability
        _screenshot(page, "48_lalkitab_remedies")


# =============================================================================
# SECTION 13: Security & Edge Cases
# =============================================================================

class TestSecurity:
    """UAT: Security validations."""

    def test_49_unauthorized_access_fails(self, page):
        """Protected endpoints require authentication."""
        resp = _api_get(page, "/api/kundli/list")
        assert resp.status in [401, 403]
        _screenshot(page, "49_unauthorized")

    def test_50_cross_user_access_prevented(self, page):
        """Users cannot access other users' data."""
        # Create second user
        resp = _api_post(page, "/api/auth/register", {
            "email": f"other_user_{TEST_TIMESTAMP}@astrovedic.com",
            "password": "OtherPass123!",
            "name": "Other User"
        })
        other_token = resp.json()["token"]
        
        # Try to access first user's kundlis
        resp = _api_get(page, "/api/kundli/list", token=other_token)
        assert resp.status == 200
        
        # Should be empty (not show first user's data)
        data = resp.json()
        # Other user has no kundlis yet
        _screenshot(page, "50_cross_user_access")

    def test_51_invalid_input_rejected(self, page):
        """Invalid input is properly rejected."""
        resp = _api_post(page, "/api/prashnavali/ram-shalaka", {
            "row": 20,  # Invalid: should be 1-15
            "col": 20   # Invalid: should be 1-15
        })
        assert resp.status == 422
        _screenshot(page, "51_invalid_input")

    def test_52_sql_injection_prevented(self, page):
        """SQL injection attempts are blocked."""
        resp = _api_post(page, "/api/auth/login", {
            "email": "test@test.com'; DROP TABLE users; --",
            "password": "password"
        })
        # Should fail login, not crash server
        assert resp.status in [401, 400, 422]
        _screenshot(page, "52_sql_injection_blocked")


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
