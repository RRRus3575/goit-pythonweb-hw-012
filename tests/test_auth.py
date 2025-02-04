import pytest
import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from jose import jwt
from dotenv import load_dotenv

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

def test_get_current_user_valid_token(valid_token, test_db):
    """Test get_current_user with a valid token."""
    user = get_current_user(valid_token, test_db)
    assert user.email == "test@example.com"

def test_get_current_user_invalid_token(invalid_token, test_db):
    """Test get_current_user with an invalid token."""
    with pytest.raises(HTTPException):
        get_current_user(invalid_token, test_db)
