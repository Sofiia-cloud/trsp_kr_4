import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from app.main import app, db

fake = Faker()

@pytest.fixture
def clean_db():
   
    db.clear()
    yield db
    db.clear()

@pytest.fixture
async def async_client(clean_db):
   
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client



@pytest.mark.asyncio
async def test_create_user(async_client):
    
    payload = {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_user_existing(async_client):
    
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
  
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == user_id
    assert "username" in data
    assert "age" in data


@pytest.mark.asyncio
async def test_get_user_not_found(async_client):
   
    response = await async_client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_existing(async_client):
    
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
    
    delete_response = await async_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    
  
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_twice(async_client):
   
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
  
    delete1 = await async_client.delete(f"/users/{user_id}")
    assert delete1.status_code == 204
    
  
    delete2 = await async_client.delete(f"/users/{user_id}")
    assert delete2.status_code == 404


@pytest.mark.asyncio
async def test_create_user_with_faker_data(async_client):
  
    for _ in range(5):
        payload = {
            "username": fake.user_name(),
            "age": fake.random_int(min=18, max=80)
        }
        response = await async_client.post("/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["age"] == payload["age"]
        