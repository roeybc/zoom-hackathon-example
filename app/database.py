from .models import User

# Mock database
_users = {
    1: User(id=1, name="Alice", email="alice@example.com", address="123 Main St, New York, NY 10001"),
    2: User(id=2, name="Bob", email="bob@example.com", address="456 Oak Ave, San Francisco, CA 94102"),
    3: User(id=3, name="Charlie", email="charlie@example.com", address="789 Pine Rd, Austin, TX 73301"),
}

def get_all_users():
    """Returns all users from the mock database."""
    return list(_users.values())

def get_user_by_id(user_id):
    """Returns a single user by their ID."""
    return _users.get(user_id)