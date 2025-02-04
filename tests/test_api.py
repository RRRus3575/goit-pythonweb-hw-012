import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def async_client():
    """Fixture to create an asynchronous test client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

async def test_register_user(async_client):
    """Test user registration endpoint."""
    response = await async_client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert "id" in response.json()

async def test_login_user(async_client):
    """Test user login endpoint."""
    response = await async_client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_protected_route(async_client):
    """Test access to a protected route without authentication."""
    response = await async_client.get("/contacts")
    assert response.status_code == 401
