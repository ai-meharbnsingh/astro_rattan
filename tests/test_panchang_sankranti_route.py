from fastapi.testclient import TestClient

from app.main import app


def test_panchang_sankranti_route_returns_12():
    with TestClient(app, raise_server_exceptions=False) as c:
        resp = c.get("/api/panchang/sankranti", params={"year": 2025, "latitude": 28.6139, "longitude": 77.2090})
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("year") == 2025
        assert data.get("ordered_from_mesha") is True
        assert isinstance(data.get("sankrantis"), list)
        assert len(data["sankrantis"]) == 12

