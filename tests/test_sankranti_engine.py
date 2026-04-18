from datetime import datetime

from app.sankranti_engine import find_sankranti_times, build_sankranti_payload


def test_find_sankranti_times_has_12_entries():
    events = find_sankranti_times(2025)
    assert len(events) == 12


def test_first_is_mesha_sankranti_around_april_14_ist():
    payload = build_sankranti_payload(2025, longitude=77.2090)  # IST heuristic
    first = payload["sankrantis"][0]
    assert first["rashi"] == "Mesha"
    # Local time should be around mid-April
    dt = datetime.strptime(first["ingress_local"], "%Y-%m-%d %H:%M")
    assert dt.month == 4
    assert dt.day in (13, 14)


def test_payload_has_windows():
    payload = build_sankranti_payload(2025, longitude=77.2090)
    first = payload["sankrantis"][0]
    assert "restriction_window" in first
    assert "amritkaal" in first
    assert first["restriction_window"]["hours_before"] == 16
    assert first["restriction_window"]["hours_after"] == 16
    assert first["amritkaal"]["is_classical"] is True

