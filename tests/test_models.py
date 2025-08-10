import pytest
from pydantic import ValidationError
from app.models import User


class TestUserModel:
    """Test cases for the User model."""
    
    def test_user_creation_with_all_fields(self):
        """Test creating a User with all fields including phone."""
        user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
    
    def test_user_creation_without_phone(self):
        """Test creating a User without phone number (backward compatibility)."""
        user_data = {
            "id": 1,
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Jane Smith"
        assert user.email == "jane.smith@example.com"
        assert user.phone is None
    
    def test_user_creation_with_explicit_none_phone(self):
        """Test creating a User with explicitly set None phone."""
        user_data = {
            "id": 1,
            "name": "Bob Wilson",
            "email": "bob.wilson@example.com",
            "phone": None
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Bob Wilson"
        assert user.email == "bob.wilson@example.com"
        assert user.phone is None
    
    def test_user_serialization_with_phone(self):
        """Test serializing User model to dict with phone number."""
        user = User(
            id=1,
            name="Alice Cooper",
            email="alice.cooper@example.com",
            phone="555-987-6543"
        )
        user_dict = user.model_dump()
        
        expected = {
            "id": 1,
            "name": "Alice Cooper",
            "email": "alice.cooper@example.com",
            "phone": "555-987-6543"
        }
        assert user_dict == expected
    
    def test_user_serialization_without_phone(self):
        """Test serializing User model to dict without phone number."""
        user = User(
            id=1,
            name="Charlie Brown",
            email="charlie.brown@example.com"
        )
        user_dict = user.model_dump()
        
        expected = {
            "id": 1,
            "name": "Charlie Brown",
            "email": "charlie.brown@example.com",
            "phone": None
        }
        assert user_dict == expected
    
    def test_user_json_serialization_with_phone(self):
        """Test JSON serialization of User model with phone."""
        user = User(
            id=1,
            name="David Lee",
            email="david.lee@example.com",
            phone="123-456-7890"
        )
        user_json = user.model_dump_json()
        
        expected_fields = ['"id":1', '"name":"David Lee"', '"email":"david.lee@example.com"', '"phone":"123-456-7890"']
        for field in expected_fields:
            assert field in user_json
    
    def test_user_json_serialization_without_phone(self):
        """Test JSON serialization of User model without phone."""
        user = User(
            id=1,
            name="Eva Green",
            email="eva.green@example.com"
        )
        user_json = user.model_dump_json()
        
        expected_fields = ['"id":1', '"name":"Eva Green"', '"email":"eva.green@example.com"', '"phone":null']
        for field in expected_fields:
            assert field in user_json
    
    def test_user_validation_missing_required_fields(self):
        """Test that validation fails when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, name="Test User")  # Missing email
        
        assert "email" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, email="test@example.com")  # Missing name
        
        assert "name" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            User(name="Test User", email="test@example.com")  # Missing id
        
        assert "id" in str(exc_info.value)
    
    def test_user_validation_invalid_types(self):
        """Test that validation fails for invalid field types."""
        with pytest.raises(ValidationError) as exc_info:
            User(id="invalid", name="Test User", email="test@example.com")
        
        assert "id" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, name=123, email="test@example.com")
        
        assert "name" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, name="Test User", email=456)
        
        assert "email" in str(exc_info.value)
    
    def test_phone_field_accepts_various_formats(self):
        """Test that phone field accepts various phone number formats."""
        phone_formats = [
            "+1-555-123-4567",
            "555.123.4567",
            "(555) 123-4567",
            "15551234567",
            "+44 20 7946 0958",
            "555-123-4567"
        ]
        
        for phone in phone_formats:
            user = User(
                id=1,
                name="Test User",
                email="test@example.com",
                phone=phone
            )
            assert user.phone == phone
    
    def test_user_equality(self):
        """Test User model equality comparison."""
        user1 = User(
            id=1,
            name="Test User",
            email="test@example.com",
            phone="555-123-4567"
        )
        user2 = User(
            id=1,
            name="Test User",
            email="test@example.com",
            phone="555-123-4567"
        )
        user3 = User(
            id=1,
            name="Test User",
            email="test@example.com"
        )
        
        assert user1 == user2
        assert user1 != user3  # Different phone values (None vs string)
    
    def test_user_model_copy_with_phone(self):
        """Test copying User model with phone modifications."""
        original_user = User(
            id=1,
            name="Original User",
            email="original@example.com",
            phone="555-123-4567"
        )
        
        # Copy with phone update
        updated_user = original_user.model_copy(update={"phone": "999-888-7777"})
        assert updated_user.phone == "999-888-7777"
        assert updated_user.id == original_user.id
        assert updated_user.name == original_user.name
        assert updated_user.email == original_user.email
        
        # Copy with phone removed (set to None)
        no_phone_user = original_user.model_copy(update={"phone": None})
        assert no_phone_user.phone is None
        assert no_phone_user.id == original_user.id
        assert no_phone_user.name == original_user.name
        assert no_phone_user.email == original_user.email