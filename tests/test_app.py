import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Check participant is added
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Check participant is removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_nonexistent():
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_activity_not_found():
    email = "pytestuser@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_activity_not_found():
    email = "pytestuser@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
