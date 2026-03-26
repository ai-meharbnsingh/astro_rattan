"""Tests for report request, retrieval, list, and paywall."""
import pytest
from tests.conftest import _register_user, _auth_header, _create_kundli


# ---- Fixtures ---- #

@pytest.fixture(scope="module")
def reports_setup(client, db):
    """Register a user and create a kundli for report tests."""
    user, token = _register_user(client, "reports_user@test.com", name="Reports User")
    kundli_id = _create_kundli(db, user["id"])
    return {"user_id": user["id"], "token": token, "kundli_id": kundli_id}


# ---- Tests ---- #

def test_request_report_201(client, reports_setup):
    """POST /api/reports/request creates a report — 201."""
    resp = client.post(
        "/api/reports/request",
        json={"kundli_id": reports_setup["kundli_id"], "report_type": "full_kundli"},
        headers=_auth_header(reports_setup["token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "report" in data
    assert data["report"]["report_type"] == "full_kundli"
    assert data["payment_required"] is True


def test_get_report_200(client, db, reports_setup):
    """GET /api/reports/{id} returns 200."""
    # Create a report first
    resp = client.post(
        "/api/reports/request",
        json={"kundli_id": reports_setup["kundli_id"], "report_type": "career"},
        headers=_auth_header(reports_setup["token"]),
    )
    report_id = resp.json()["report"]["id"]

    resp = client.get(
        f"/api/reports/{report_id}",
        headers=_auth_header(reports_setup["token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == report_id


def test_list_reports_200(client, reports_setup):
    """GET /api/reports returns 200 with a list."""
    resp = client.get("/api/reports", headers=_auth_header(reports_setup["token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "reports" in data
    assert isinstance(data["reports"], list)
    assert len(data["reports"]) >= 1


def test_report_paywall(client, db, reports_setup):
    """POST /api/reports/request returns payment_required=true in response.

    The paywall flag is set at request time. With TestClient, BackgroundTasks
    run synchronously so by the time we GET the report it may already be 'ready'.
    We verify the flag from the initial POST response instead.
    """
    resp = client.post(
        "/api/reports/request",
        json={"kundli_id": reports_setup["kundli_id"], "report_type": "marriage"},
        headers=_auth_header(reports_setup["token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["payment_required"] is True

    # Additionally: manually set a report to 'pending' status and verify paywall on GET
    report_id = data["report"]["id"]
    db.execute("UPDATE reports SET status = 'pending' WHERE id = ?", (report_id,))
    db.commit()

    resp = client.get(
        f"/api/reports/{report_id}",
        headers=_auth_header(reports_setup["token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["payment_required"] is True


def test_report_nonexistent_kundli_404(client, reports_setup):
    """Report for nonexistent kundli returns 404."""
    resp = client.post(
        "/api/reports/request",
        json={"kundli_id": "nonexistent_kundli_id", "report_type": "health"},
        headers=_auth_header(reports_setup["token"]),
    )
    assert resp.status_code == 404


def test_reports_without_auth_401(client):
    """Reports endpoints without auth return 401."""
    resp = client.get("/api/reports")
    assert resp.status_code == 401

    resp = client.post("/api/reports/request", json={"kundli_id": "x", "report_type": "career"})
    assert resp.status_code == 401


class TestReportPayments:
    """Test report payment initiation endpoints."""

    def test_initiate_report_payment_cod(self, client, reports_setup):
        """POST /api/payments/report/initiate with COD creates pending payment."""
        # Create a report first
        resp = client.post(
            "/api/reports/request",
            json={"kundli_id": reports_setup["kundli_id"], "report_type": "yearly"},
            headers=_auth_header(reports_setup["token"]),
        )
        report_id = resp.json()["report"]["id"]

        # Initiate payment
        resp = client.post(
            "/api/payments/report/initiate",
            json={"report_id": report_id, "provider": "cod"},
            headers=_auth_header(reports_setup["token"]),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["report_id"] == report_id
        assert data["provider"] == "cod"
        assert "payment_id" in data
        assert "amount" in data

    def test_initiate_report_payment_razorpay(self, client, reports_setup):
        """POST /api/payments/report/initiate with Razorpay returns key."""
        resp = client.post(
            "/api/reports/request",
            json={"kundli_id": reports_setup["kundli_id"], "report_type": "full_kundli"},
            headers=_auth_header(reports_setup["token"]),
        )
        report_id = resp.json()["report"]["id"]

        resp = client.post(
            "/api/payments/report/initiate",
            json={"report_id": report_id, "provider": "razorpay"},
            headers=_auth_header(reports_setup["token"]),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["provider"] == "razorpay"
        assert "provider_payment_id" in data

    def test_initiate_report_payment_already_ready(self, client, db, reports_setup):
        """Cannot initiate payment for already-ready report."""
        resp = client.post(
            "/api/reports/request",
            json={"kundli_id": reports_setup["kundli_id"], "report_type": "marriage"},
            headers=_auth_header(reports_setup["token"]),
        )
        report_id = resp.json()["report"]["id"]

        # Mark as ready
        db.execute("UPDATE reports SET status = 'ready' WHERE id = ?", (report_id,))
        db.commit()

        resp = client.post(
            "/api/payments/report/initiate",
            json={"report_id": report_id, "provider": "cod"},
            headers=_auth_header(reports_setup["token"]),
        )
        assert resp.status_code == 400
        assert "already" in resp.json()["detail"].lower()

    def test_initiate_report_payment_nonexistent_report(self, client, reports_setup):
        """Payment for nonexistent report returns 404."""
        resp = client.post(
            "/api/payments/report/initiate",
            json={"report_id": "nonexistent_report", "provider": "cod"},
            headers=_auth_header(reports_setup["token"]),
        )
        assert resp.status_code == 404

    def test_initiate_report_payment_without_auth(self, client):
        """Report payment initiation requires auth."""
        resp = client.post(
            "/api/payments/report/initiate",
            json={"report_id": "some_id", "provider": "cod"},
        )
        assert resp.status_code == 401
