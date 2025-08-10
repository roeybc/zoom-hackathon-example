import pytest
from app import database
from app.models import User


class TestDatabase:
    """Test cases for the database module."""

    def test_get_all_users_returns_list(self):
        """Test that get_all_users returns a list of users."""
        users = database.get_all_users()
        assert isinstance(users, list)
        assert len(users) == 3
        
        # Verify all items are User instances
        for user in users:
            assert isinstance(user, User)

    def test_get_all_users_includes_addresses(self):
        """Test that get_all_users returns users with address information."""
        users = database.get_all_users()
        user_dict = {user.id: user for user in users}
        
        # Alice should have an address
        alice = user_dict[1]
        assert alice.name == "Alice"
        assert alice.address == "123 Main St, New York, NY"
        
        # Bob should have an address
        bob = user_dict[2]
        assert bob.name == "Bob"
        assert bob.address == "456 Oak Ave, Los Angeles, CA"
        
        # Charlie should have no address (None)
        charlie = user_dict[3]
        assert charlie.name == "Charlie"
        assert charlie.address is None

    def test_get_user_by_id_existing_user(self):
        """Test getting an existing user by ID."""
        user = database.get_user_by_id(1)
        assert user is not None
        assert user.id == 1
        assert user.name == "Alice"
        assert user.address == "123 Main St, New York, NY"

    def test_get_user_by_id_nonexistent_user(self):
        """Test getting a non-existent user by ID."""
        user = database.get_user_by_id(999)
        assert user is None

    def test_get_user_by_id_user_without_address(self):
        """Test getting a user without address by ID."""
        user = database.get_user_by_id(3)
        assert user is not None
        assert user.id == 3
        assert user.name == "Charlie"
        assert user.address is None

    def test_all_users_have_required_fields(self):
        """Test that all users have the required fields."""
        users = database.get_all_users()
        
        for user in users:
            assert hasattr(user, 'id')
            assert hasattr(user, 'name')
            assert hasattr(user, 'email')
            assert hasattr(user, 'address')
            
            assert isinstance(user.id, int)
            assert isinstance(user.name, str)
            assert isinstance(user.email, str)
            assert user.address is None or isinstance(user.address, str)