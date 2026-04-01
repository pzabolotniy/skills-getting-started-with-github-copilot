import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    # Arrange: create a new TestClient for each test
    return TestClient(app)

def test_get_activities(client):
    # Arrange is handled by the fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]
    # Act: unregister
    del_resp = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert del_resp.status_code == 200
    assert f"Removed {email}" in del_resp.json()["message"]
    # Act: unregister again (should fail)
    del_resp2 = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert del_resp2.status_code == 404
    assert "Student not found" in del_resp2.json()["detail"]
