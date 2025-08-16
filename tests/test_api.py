# tests/test_api.py

from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_events_route():
    """Test that /events endpoint responds and returns a list."""
    response = client.get("/events")
    response.raise_for_status()
    data = response.json()
    assert isinstance(data, list), "Expected list of events"
    if data:
        assert "event_id" in data[0], "Missing 'event_id' key in event response"

def test_stats_by_country_route():
    """Test that /stats/by-country endpoint responds and returns a list of countries."""
    response = client.get("/stats/by-country")
    response.raise_for_status()
    data = response.json()
    assert isinstance(data, list), "Expected list of country stats"
    if data:
        assert "country" in data[0], "Missing 'country' key in country stat"
        assert "events" in data[0], "Missing 'events' key in country stat"
