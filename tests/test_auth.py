import pytest
import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from jose import jwt
from dotenv import load_dotenv
from app.config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "testsecret")
ALGORITHM = "HS256"

@pytest.fixture
def test_user():
    """Fixture to create a test user."""
    class User:
        id = 1
        email = "test@example.com"
    return User()

@pytest.fixture
def test_db():
    """Mock database session."""
    class TestDB(Session):
        def query(self, model):
            class Query:
                def filter(self, condition):
                    if "test@example.com" in str(condition):
                        return self
                    return None
                def first(self):
                    return test_user()
            return Query()
    return TestDB()

@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing."""
    return jwt.encode({"sub": "test@example.com"}, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def invalid_token():
    """Generate an invalid JWT token."""
    return "invalid.token.value"

async def test_get_current_user_valid_token(valid_token, async_db):
    """Test get_current_user with a valid token."""
    user = await get_current_user(valid_token, async_db)
    assert user is not None

def test_get_current_user_invalid_token(invalid_token, test_db):
    """Test get_current_user with an invalid token."""
    with pytest.raises(HTTPException):
        get_current_user(invalid_token, test_db)

@pytest.fixture
def expired_token():
    """Создает токен с истекшим сроком действия."""
    payload = {"sub": "test@example.com", "exp": datetime.utcnow() - timedelta(days=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def token_without_sub():
    """Создает токен без `sub` поля."""
    payload = {"exp": datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.mark.asyncio
async def test_get_current_user_expired_token(expired_token, test_db):
    """Тестирует get_current_user с истекшим токеном."""
    with pytest.raises(Exception) as exc_info:
        await get_current_user(expired_token, test_db)
    assert "Invalid token" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_current_user_missing_sub(token_without_sub, test_db):
    """Тестирует get_current_user без `sub` в токене."""
    with pytest.raises(Exception) as exc_info:
        await get_current_user(token_without_sub, test_db)
    assert "Invalid token" in str(exc_info.value)
