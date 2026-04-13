from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_fake_route_gives_404():
    response = client.get("/fake-route")
    assert response.status_code == 404

def test_analyze_without_token_fails():
    response = client.post("/analyze", json={"text": "I love AI!"})
    assert response.status_code == 401

    assert response.json() == {"detail": "Not authenticated"}

def test_successful_registration_and_login():
    # Generate a random unique email for testing
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    password = "testpassword"

    # Register the user
    register_response = client.post("/auth/register", json={"email": unique_email, "password": password})
    
    assert register_response.status_code == 201
    assert register_response.json()["email"] == unique_email

    # Login with the same credentials
    login_response = client.post("/auth/login", json={"email": unique_email, "password": password})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


# Test 4: Testing Login with bad password
def test_login_wrong_password_fails():
    response = client.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "wrong_password"
        }
    )
    
    # We demand the Bouncer blocks them
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid Email or Password"}