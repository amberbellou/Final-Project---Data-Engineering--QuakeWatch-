from fastapi.testclient import TestClient
from app.api import app

def test_routes_exist():
    client = TestClient(app)
    assert client.get("/events").status_code == 200
    assert client.get("/stats/by-country").status_code == 200
