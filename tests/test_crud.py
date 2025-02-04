import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import create_contact, get_contacts
from app.models import Contact
from app.schemas import ContactCreate

@pytest.fixture
async def test_contact():
    """Fixture to create a test contact data."""
    return ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday="2000-01-01",
        additional_info="Test contact"
    )

@pytest.fixture
async def test_user():
    """Fixture to create a test user."""
    class User:
        id = 1
    return User()

async def test_create_contact(async_db: AsyncSession, test_contact, test_user):
    """Test the create_contact function."""
    contact = await create_contact(async_db, test_contact, test_user.id)
    assert isinstance(contact, Contact)
    assert contact.first_name == "John"
    assert contact.email == "john.doe@example.com"

async def test_get_contacts(async_db: AsyncSession, test_user):
    """Test retrieving contacts for a user."""
    contacts = await get_contacts(async_db, test_user)
    assert isinstance(contacts, list)
