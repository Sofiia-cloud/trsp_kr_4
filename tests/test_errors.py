from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_custom_exception_a_triggered():
 
    response = client.get("/trigger-a?value=-5")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "negative" in data["error"]

def test_custom_exception_a_not_triggered():
 
    response = client.get("/trigger-a?value=10")
    assert response.status_code == 200
    assert response.json()["value"] == 10

def test_custom_exception_b_triggered():

    response = client.get("/trigger-b/0")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"]

def test_custom_exception_b_not_triggered():
  
    response = client.get("/trigger-b/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42