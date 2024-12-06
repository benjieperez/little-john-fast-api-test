from fastapi.testclient import TestClient
import pytest
from main import app

@pytest.fixture
def client():
    return TestClient(app)

# Test to check if the app is working
def test_health_check(client):
    response = client.get("/api/health-check")  # Make a GET request to the /health endpoint
    assert response.status_code == 200  # The status code should be 200 (OK)
