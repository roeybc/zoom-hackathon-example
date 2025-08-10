import pytest
from app.models import User


class TestUserModel:
    """Test cases for the User model."""

    def test_user_with_all_fields(self):
        """Test creating a user with all fields including address."""
        user = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            address="123 Test St, Test City, TC"
        )
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.address == "123 Test St, Test City, TC"

    def test_user_without_address(self):
        """Test creating a user without address (should default to None)."""
        user = User(
            id=2,
            name="Jane Smith",
            email="jane@example.com"
        )
        
        assert user.id == 2
        assert user.name == "Jane Smith"
        assert user.email == "jane@example.com"
        assert user.address is None

    def test_user_with_empty_address(self):
        """Test creating a user with empty string address."""
        user = User(
            id=3,
            name="Empty Address",
            email="empty@example.com",
            address=""
        )
        
        assert user.id == 3
        assert user.name == "Empty Address"
        assert user.email == "empty@example.com"
        assert user.address == ""

    def test_user_serialization_with_address(self):
        """Test that user with address serializes correctly."""
        user = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            address="123 Test St, Test City, TC"
        )
        
        user_dict = user.model_dump()
        expected = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Test St, Test City, TC"
        }
        
        assert user_dict == expected

    def test_user_serialization_without_address(self):
        """Test that user without address serializes correctly."""
        user = User(
            id=2,
            name="Jane Smith",
            email="jane@example.com"
        )
        
        user_dict = user.model_dump()
        expected = {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "address": None
        }
        
        assert user_dict == expected

    def test_user_from_dict_with_address(self):
        """Test creating user from dict with address."""
        user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Test St, Test City, TC"
        }
        
        user = User(**user_data)
        assert user.address == "123 Test St, Test City, TC"

    def test_user_from_dict_without_address(self):
        """Test creating user from dict without address."""
        user_data = {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
        
        user = User(**user_data)
        assert user.address is None