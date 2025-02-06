import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.crud import create_contact, get_contacts, update_contact, delete_contact, get_contact_by_id
from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate
from app.routers.auth import get_current_user
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

@pytest.fixture
async def async_client():
    """Fixture to create an asynchronous test client."""
    async with AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as client:
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

def generate_expired_token():
    expired_time = datetime.utcnow() - timedelta(days=1)
    payload = {"sub": "test@example.com", "exp": expired_time}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def test_update_contact(async_db: AsyncSession, test_contact, test_user):
    """Test updating a contact."""
    contact = await create_contact(async_db, test_contact, test_user.id)
    updated_data = ContactUpdate(first_name="Updated Name")
    updated_contact = await update_contact(async_db, contact.id, updated_data, test_user.id)
    assert updated_contact.first_name == "Updated Name"

async def test_delete_contact(async_db: AsyncSession, test_contact, test_user):
    """Test deleting a contact."""
    contact = await create_contact(async_db, test_contact, test_user.id)
    await delete_contact(async_db, contact.id, test_user.id)
    deleted_contact = await get_contact_by_id(async_db, contact.id, test_user.id)
    assert deleted_contact is None

def test_get_current_user_expired_token():
    """Test get_current_user with expired token."""
    token = generate_expired_token()
    with pytest.raises(HTTPException) as exc:
        get_current_user(token)
    assert exc.value.status_code == 401

def test_get_current_user_no_auth_header():
    """Test get_current_user without an authorization header."""
    with pytest.raises(HTTPException) as exc:
        get_current_user("")
    assert exc.value.status_code == 401