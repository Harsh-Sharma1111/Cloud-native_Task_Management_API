import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create and configure a new app instance for each test session."""
    # Create the app with testing configuration
    app = create_app('test')
    
    # Establish an application context before running tests
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers(client, app):
    """Fixture to create a user, log in, and return the auth headers."""
    with app.app_context():
        # Create a test user directly in the database
        user = User(
            name="Test User",
            email="testuser@example.com",
            password_hash=generate_password_hash("testpassword"),
            role="member"
        )
        db.session.add(user)
        db.session.commit()
        
    # Log in via the API to get the JWT token
    response = client.post('/api/auth/login', json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    token = response.get_json().get('token')
    return {"Authorization": f"Bearer {token}"}
