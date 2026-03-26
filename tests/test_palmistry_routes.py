"""Palmistry routes tests."""
import io

import pytest
from PIL import Image
from tests.conftest import _register_user, _auth_header


class TestPalmistryGuide:
    """Test GET /api/palmistry/guide - static reference data."""

    def test_palmistry_guide_200(self, client):
        """Should return static palmistry guide data."""
        resp = client.get("/api/palmistry/guide")
        assert resp.status_code == 200
        data = resp.json()
        assert "meanings" in data
        assert "lines" in data
        assert "mounts" in data
        assert "shapes" in data
        assert len(data["lines"]) > 0
        assert len(data["mounts"]) > 0

    def test_palmistry_guide_no_auth_required(self, client):
        """Guide should be accessible without authentication."""
        resp = client.get("/api/palmistry/guide")
        assert resp.status_code == 200


class TestPalmistryAnalyze:
    """Test POST /api/palmistry/analyze - AI-powered analysis."""

    @pytest.fixture(scope="class")
    def palmistry_user(self, client):
        """Register a user for palmistry tests."""
        user, token = _register_user(client, "palmistry_test@test.com", name="Palmistry User")
        return {"user": user, "token": token}

    def test_analyze_palmistry_200(self, client, palmistry_user):
        """Should return personalized reading with all fields."""
        resp = client.post(
            "/api/palmistry/analyze",
            json={
                "hand_shape": "earth",
                "dominant_hand": "right",
                "finger_length": "short",
                "heart_line": "long_curved",
                "head_line": "long_straight",
                "life_line": "long_deep",
                "fate_line": "deep_clear",
                "sun_line": "present",
                "mounts_prominent": ["jupiter", "venus"],
            },
            headers=_auth_header(palmistry_user["token"]),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reading" in data
        assert "ai_insights" in data
        
        reading = data["reading"]
        assert "hand_type" in reading
        assert "personality" in reading
        assert "relationships" in reading
        assert "life_path" in reading
        assert "career" in reading
        assert "overall" in reading

    def test_analyze_palmistry_minimal_data(self, client, palmistry_user):
        """Should work with minimal required fields."""
        resp = client.post(
            "/api/palmistry/analyze",
            json={
                "hand_shape": "water",
                "dominant_hand": "left",
                "finger_length": "average",
                "heart_line": "short_straight",
                "head_line": "curved",
                "life_line": "curved",
            },
            headers=_auth_header(palmistry_user["token"]),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reading" in data

    def test_analyze_palmistry_without_auth(self, client):
        """Should require authentication."""
        resp = client.post(
            "/api/palmistry/analyze",
            json={
                "hand_shape": "fire",
                "dominant_hand": "right",
                "finger_length": "long",
                "heart_line": "forked",
                "head_line": "double",
                "life_line": "broken",
            },
        )
        assert resp.status_code == 401

    def test_analyze_all_hand_shapes(self, client, palmistry_user):
        """Should handle all hand shape types."""
        shapes = ["earth", "air", "water", "fire"]
        
        for shape in shapes:
            resp = client.post(
                "/api/palmistry/analyze",
                json={
                    "hand_shape": shape,
                    "dominant_hand": "right",
                    "finger_length": "average",
                    "heart_line": "long_curved",
                    "head_line": "long_straight",
                    "life_line": "long_deep",
                },
                headers=_auth_header(palmistry_user["token"]),
            )
            assert resp.status_code == 200
            data = resp.json()
            assert data["reading"]["hand_type"]["type"] == shape

    def test_analyze_palmistry_image_success(self, client, palmistry_user):
        """Image-driven palmistry should return detected traits and reading."""
        image = Image.new("RGB", (640, 880), color=(210, 180, 160))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        resp = client.post(
            "/api/palmistry/analyze-image",
            data={"dominant_hand": "right"},
            files={"file": ("palm.png", buffer.getvalue(), "image/png")},
            headers=_auth_header(palmistry_user["token"]),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reading" in data
        assert "image_analysis" in data
        assert data["image_analysis"]["image_url"].startswith("/static/uploads/")
        assert data["image_analysis"]["derived_traits"]["hand_shape"] in {"earth", "air", "water", "fire"}
        assert data["image_analysis"]["confidence"] in {"low", "medium", "high"}

    def test_analyze_palmistry_image_requires_auth(self, client):
        """Image-driven route should require authentication."""
        image = Image.new("RGB", (320, 320), color=(200, 170, 150))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        resp = client.post(
            "/api/palmistry/analyze-image",
            data={"dominant_hand": "right"},
            files={"file": ("palm.png", buffer.getvalue(), "image/png")},
        )
        assert resp.status_code == 401

    def test_analyze_palmistry_image_rejects_small_upload(self, client, palmistry_user):
        """Very small uploads should be rejected."""
        image = Image.new("RGB", (80, 80), color=(200, 170, 150))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        resp = client.post(
            "/api/palmistry/analyze-image",
            data={"dominant_hand": "left"},
            files={"file": ("tiny.png", buffer.getvalue(), "image/png")},
            headers=_auth_header(palmistry_user["token"]),
        )
        assert resp.status_code == 400
