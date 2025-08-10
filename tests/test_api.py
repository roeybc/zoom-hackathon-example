import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPI:
    """Test cases for the FastAPI endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the EKS-powered FastAPI app!"}

    def test_get_all_users(self):
        """Test getting all users includes address field."""
        response = client.get("/users")
        assert response.status_code == 200
        
        users = response.json()
        assert len(users) == 3
        
        # Verify structure of returned users
        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user
            assert "address" in user  # Address field should be present
            
            assert isinstance(user["id"], int)
            assert isinstance(user["name"], str)
            assert isinstance(user["email"], str)
            # Address can be str or None
            assert user["address"] is None or isinstance(user["address"], str)

    def test_get_all_users_specific_addresses(self):
        """Test that specific users have expected addresses."""
        response = client.get("/users")
        assert response.status_code == 200
        
        users = response.json()
        user_dict = {user["id"]: user for user in users}
        
        # Alice should have an address
        alice = user_dict[1]
        assert alice["name"] == "Alice"
        assert alice["address"] == "123 Main St, New York, NY"
        
        # Bob should have an address
        bob = user_dict[2]
        assert bob["name"] == "Bob"
        assert bob["address"] == "456 Oak Ave, Los Angeles, CA"
        
        # Charlie should have no address
        charlie = user_dict[3]
        assert charlie["name"] == "Charlie"
        assert charlie["address"] is None

    def test_get_user_by_id_with_address(self):
        """Test getting a specific user with address."""
        response = client.get("/user/1")
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == 1
        assert user["name"] == "Alice"
        assert user["email"] == "alice@example.com"
        assert user["address"] == "123 Main St, New York, NY"

    def test_get_user_by_id_without_address(self):
        """Test getting a specific user without address."""
        response = client.get("/user/3")
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == 3
        assert user["name"] == "Charlie"
        assert user["email"] == "charlie@example.com"
        assert user["address"] is None

    def test_get_user_by_id_nonexistent(self):
        """Test getting a non-existent user."""
        response = client.get("/user/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_response_model_compatibility(self):
        """Test that response models are still compatible."""
        # Test individual user endpoint
        response = client.get("/user/1")
        assert response.status_code == 200
        
        user = response.json()
        required_fields = ["id", "name", "email", "address"]
        for field in required_fields:
            assert field in user
        
        # Test users list endpoint
        response = client.get("/users")
        assert response.status_code == 200
        
        users = response.json()
        for user in users:
            for field in required_fields:
                assert field in user

    def test_backward_compatibility(self):
        """Test that the API is backward compatible - old clients can still work."""
        response = client.get("/users")
        assert response.status_code == 200
        
        users = response.json()
        
        # Even though address is optional, it should always be present in JSON
        # (with None value if not set) due to Pydantic serialization
        for user in users:
            assert "id" in user
            assert "name" in user  
            assert "email" in user
            assert "address" in user  # This ensures backward compatibility