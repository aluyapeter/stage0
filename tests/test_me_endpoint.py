# tests/test_me_endpoint.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_me_endpoint():
    response = client.get("/me")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    
    data = response.json()
    assert data["status"] == "success"
    assert "user" in data
    assert all(k in data["user"] for k in ["email", "name", "stack"])
    assert "timestamp" in data
    assert data["timestamp"].endswith("Z")
    assert "fact" in data and isinstance(data["fact"], str)
