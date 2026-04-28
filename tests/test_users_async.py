import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from app.main import app, db

fake = Faker()

@pytest.fixture
def clean_db():
    """Фикстура для очистки in-memory БД перед каждым тестом"""
    db.clear()
    yield db
    db.clear()

@pytest.fixture
async def async_client(clean_db):
    """Фикстура асинхронного клиента"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ========== АСИНХРОННЫЕ ТЕСТЫ (добавлен маркер async) ==========

@pytest.mark.asyncio
async def test_create_user(async_client):
    """Тест создания пользователя (201)"""
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
    """Тест получения существующего пользователя (200)"""
    # Сначала создаём пользователя
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
    # Получаем его
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == user_id
    assert "username" in data
    assert "age" in data


@pytest.mark.asyncio
async def test_get_user_not_found(async_client):
    """Тест получения несуществующего пользователя (404)"""
    response = await async_client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_existing(async_client):
    """Тест удаления существующего пользователя (204)"""
    # Создаём пользователя
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
    # Удаляем его
    delete_response = await async_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    
    # Проверяем что его больше нет
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_twice(async_client):
    """Тест повторного удаления того же пользователя (404)"""
    # Создаём пользователя
    create_response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    })
    user_id = create_response.json()["id"]
    
    # Первое удаление - успешно
    delete1 = await async_client.delete(f"/users/{user_id}")
    assert delete1.status_code == 204
    
    # Второе удаление - 404
    delete2 = await async_client.delete(f"/users/{user_id}")
    assert delete2.status_code == 404


@pytest.mark.asyncio
async def test_create_user_with_faker_data(async_client):
    """Тест создания пользователя с разными данными от Faker"""
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
        