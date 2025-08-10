import pytest
from pydantic import ValidationError
from app.models import User


class TestUserModel:
    """Test cases for the User model."""
    
    def test_user_creation_with_all_fields(self):
        """Test creating a User with all fields including phone and address."""
        user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "address": "123 Main St, New York, NY 10001"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
        assert user.address == "123 Main St, New York, NY 10001"
    
    def test_user_creation_with_minimal_fields(self):
        """Test creating a User with only required fields (backward compatibility)."""
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
        assert user.address is None
    
    def test_user_creation_with_phone_only(self):
        """Test creating a User with phone but no address."""
        user_data = {
            "id": 1,
            "name": "Bob Wilson",
            "email": "bob.wilson@example.com",
            "phone": "+1-555-987-6543"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Bob Wilson"
        assert user.email == "bob.wilson@example.com"
        assert user.phone == "+1-555-987-6543"
        assert user.address is None
    
    def test_user_creation_with_address_only(self):
        """Test creating a User with address but no phone."""
        user_data = {
            "id": 1,
            "name": "Alice Cooper",
            "email": "alice.cooper@example.com",
            "address": "456 Oak Ave, Los Angeles, CA 90210"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Alice Cooper"
        assert user.email == "alice.cooper@example.com"
        assert user.phone is None
        assert user.address == "456 Oak Ave, Los Angeles, CA 90210"
    
    def test_user_creation_with_explicit_none_values(self):
        """Test creating a User with explicitly set None for optional fields."""
        user_data = {
            "id": 1,
            "name": "Charlie Brown",
            "email": "charlie.brown@example.com",
            "phone": None,
            "address": None
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Charlie Brown"
        assert user.email == "charlie.brown@example.com"
        assert user.phone is None
        assert user.address is None
    
    def test_user_serialization_with_all_fields(self):
        """Test serializing User model to dict with all fields."""
        user = User(
            id=1,
            name="David Lee",
            email="david.lee@example.com",
            phone="555-987-6543",
            address="789 Pine St, Chicago, IL 60601"
        )
        user_dict = user.model_dump()
        
        expected = {
            "id": 1,
            "name": "David Lee",
            "email": "david.lee@example.com",
            "phone": "555-987-6543",
            "address": "789 Pine St, Chicago, IL 60601"
        }
        assert user_dict == expected
    
    def test_user_serialization_with_minimal_fields(self):
        """Test serializing User model to dict with minimal fields."""
        user = User(
            id=1,
            name="Eva Green",
            email="eva.green@example.com"
        )
        user_dict = user.model_dump()
        
        expected = {
            "id": 1,
            "name": "Eva Green",
            "email": "eva.green@example.com",
            "phone": None,
            "address": None
        }
        assert user_dict == expected
    
    def test_user_json_serialization_with_all_fields(self):
        """Test JSON serialization of User model with all fields."""
        user = User(
            id=1,
            name="Frank Miller",
            email="frank.miller@example.com",
            phone="123-456-7890",
            address="321 Elm St, Boston, MA 02101"
        )
        user_json = user.model_dump_json()
        
        expected_fields = [
            '"id":1',
            '"name":"Frank Miller"',
            '"email":"frank.miller@example.com"',
            '"phone":"123-456-7890"',
            '"address":"321 Elm St, Boston, MA 02101"'
        ]
        for field in expected_fields:
            assert field in user_json
    
    def test_user_json_serialization_with_minimal_fields(self):
        """Test JSON serialization of User model with minimal fields."""
        user = User(
            id=1,
            name="Grace Kelly",
            email="grace.kelly@example.com"
        )
        user_json = user.model_dump_json()
        
        expected_fields = [
            '"id":1',
            '"name":"Grace Kelly"',
            '"email":"grace.kelly@example.com"',
            '"phone":null',
            '"address":null'
        ]
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
    
    def test_address_field_accepts_various_formats(self):
        """Test that address field accepts various address formats."""
        address_formats = [
            "123 Main St, New York, NY 10001",
            "456 Oak Avenue, Apartment 2B, Los Angeles, CA 90210",
            "789 Pine Street\nSuite 100\nChicago, IL 60601",
            "321 Elm St",
            "Building A, Floor 5, Room 502, Tech Park",
            "P.O. Box 1234, Small Town, ST 12345",
            "1600 Pennsylvania Avenue NW, Washington, DC 20500"
        ]
        
        for address in address_formats:
            user = User(
                id=1,
                name="Test User",
                email="test@example.com",
                address=address
            )
            assert user.address == address
    
    def test_address_field_with_empty_string(self):
        """Test that address field accepts empty string."""
        user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            address=""
        )
        assert user.address == ""
    
    def test_user_equality_with_all_fields(self):
        """Test User model equality comparison with all fields."""
        user1 = User(
            id=1,
            name="Test User",
            email="test@example.com",
            phone="555-123-4567",
            address="123 Main St, City, ST 12345"
        )
        user2 = User(
            id=1,
            name="Test User",
            email="test@example.com",
            phone="555-123-4567",
            address="123 Main St, City, ST 12345"
        )
        user3 = User(
            id=1,
            name="Test User",
            email="test@example.com",
            phone="555-123-4567"
        )
        
        assert user1 == user2
        assert user1 != user3  # Different address values (None vs string)
    
    def test_user_equality_with_minimal_fields(self):
        """Test User model equality comparison with minimal fields."""
        user1 = User(
            id=1,
            name="Test User",
            email="test@example.com"
        )
        user2 = User(
            id=1,
            name="Test User",
            email="test@example.com"
        )
        
        assert user1 == user2
    
    def test_user_model_copy_with_phone(self):
        """Test copying User model with phone modifications."""
        original_user = User(
            id=1,
            name="Original User",
            email="original@example.com",
            phone="555-123-4567",
            address="123 Original St"
        )
        
        # Copy with phone update
        updated_user = original_user.model_copy(update={"phone": "999-888-7777"})
        assert updated_user.phone == "999-888-7777"
        assert updated_user.id == original_user.id
        assert updated_user.name == original_user.name
        assert updated_user.email == original_user.email
        assert updated_user.address == original_user.address
        
        # Copy with phone removed (set to None)
        no_phone_user = original_user.model_copy(update={"phone": None})
        assert no_phone_user.phone is None
        assert no_phone_user.id == original_user.id
        assert no_phone_user.name == original_user.name
        assert no_phone_user.email == original_user.email
        assert no_phone_user.address == original_user.address
    
    def test_user_model_copy_with_address(self):
        """Test copying User model with address modifications."""
        original_user = User(
            id=1,
            name="Original User",
            email="original@example.com",
            phone="555-123-4567",
            address="123 Original St"
        )
        
        # Copy with address update
        updated_user = original_user.model_copy(update={"address": "456 New Address Ave"})
        assert updated_user.address == "456 New Address Ave"
        assert updated_user.id == original_user.id
        assert updated_user.name == original_user.name
        assert updated_user.email == original_user.email
        assert updated_user.phone == original_user.phone
        
        # Copy with address removed (set to None)
        no_address_user = original_user.model_copy(update={"address": None})
        assert no_address_user.address is None
        assert no_address_user.id == original_user.id
        assert no_address_user.name == original_user.name
        assert no_address_user.email == original_user.email
        assert no_address_user.phone == original_user.phone
    
    def test_user_model_copy_with_multiple_fields(self):
        """Test copying User model with multiple field modifications."""
        original_user = User(
            id=1,
            name="Original User",
            email="original@example.com",
            phone="555-123-4567",
            address="123 Original St"
        )
        
        # Copy with multiple updates
        updated_user = original_user.model_copy(update={
            "phone": "999-888-7777",
            "address": "789 Updated Blvd"
        })
        assert updated_user.phone == "999-888-7777"
        assert updated_user.address == "789 Updated Blvd"
        assert updated_user.id == original_user.id
        assert updated_user.name == original_user.name
        assert updated_user.email == original_user.email
    
    def test_backward_compatibility_phone_only(self):
        """Test that existing code using only phone field still works."""
        # Simulate existing code that only knows about phone field
        user_data = {
            "id": 1,
            "name": "Legacy User",
            "email": "legacy@example.com",
            "phone": "555-legacy-01"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Legacy User"
        assert user.email == "legacy@example.com"
        assert user.phone == "555-legacy-01"
        assert user.address is None  # New field defaults to None
    
    def test_backward_compatibility_no_optional_fields(self):
        """Test that existing code with no optional fields still works."""
        # Simulate existing code that only knows about required fields
        user_data = {
            "id": 1,
            "name": "Minimal User",
            "email": "minimal@example.com"
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.name == "Minimal User"
        assert user.email == "minimal@example.com"
        assert user.phone is None  # Existing optional field defaults to None
        assert user.address is None  # New optional field defaults to None