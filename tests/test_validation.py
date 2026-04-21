from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_user_registration():
  
    payload = {
        "username": "john_doe",
        "age": 25,
        "email": "john@example.com",
        "password": "securepass123",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User john_doe registered successfully"
    assert data["user"]["username"] == "john_doe"

def test_invalid_age_less_or_equal_18():
   
    payload = {
        "username": "young_user",
        "age": 18,
        "email": "young@example.com",
        "password": "securepass123"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("age" in str(error) for error in errors)

def test_invalid_email():
  
    payload = {
        "username": "test_user",
        "age": 25,
        "email": "not-an-email",
        "password": "securepass123"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("email" in str(error).lower() for error in errors)

def test_password_too_short():
  
    payload = {
        "username": "test_user",
        "age": 25,
        "email": "test@example.com",
        "password": "short"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("password" in str(error).lower() for error in errors)

def test_missing_required_field():
 
    payload = {
        "username": "test_user",
        "age": 25
        
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 422