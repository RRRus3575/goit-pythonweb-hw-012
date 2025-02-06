import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Base
from app.database import engine, SessionLocal
from app.models import Contact, User

@pytest.fixture
def test_user():
    return User(id=1, email="test@example.com", password="hashedpassword")

@pytest.fixture
def test_contact():
    return Contact(first_name="John", last_name="Doe", email="john.doe@example.com")

@pytest.fixture(scope="function")
async def async_db():
    """create test DB"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
