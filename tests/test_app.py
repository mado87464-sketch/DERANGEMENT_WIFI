import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Ticket

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_index_page(client):
    """Test that the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Support WiFi' in response.data

def test_login_page(client):
    """Test that the login page loads correctly"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_register_page(client):
    """Test that the register page loads correctly"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Inscription' in response.data

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'user_type': 'client'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.user_type == 'client'

def test_user_login(client):
    """Test user login"""
    # First register a user
    client.post('/register', data={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password123',
        'user_type': 'client'
    })
    
    # Then try to login
    response = client.post('/login', data={
        'username': 'testuser2',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_protected_routes(client):
    """Test that protected routes redirect to login"""
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirect to login
    
    response = client.get('/create_ticket')
    assert response.status_code == 302  # Redirect to login

if __name__ == '__main__':
    pytest.main([__file__])
