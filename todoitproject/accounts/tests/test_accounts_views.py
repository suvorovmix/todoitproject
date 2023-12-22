import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from unittest.mock import patch


@pytest.fixture
def test_user(db):
    return User.objects.create_user('testuser', 'test@example.com', 'password123')

@pytest.fixture
def logged_in_client(client, test_user):
    client.login(username='testuser', password='password123')
    return client


class TestLoginView:
    def test_login_view_get(self, client):
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200

    def test_login_view_post(self, client, test_user):
        url = reverse('login')
        response = client.post(url, {'username': 'testuser', 'password': 'password123'})
        assert response.status_code == 302
        assert response.url == reverse('index')


class TestRegisterView:
    def test_register_view_get(self, client):
        url = reverse('register')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_view_post_valid(self, db, client):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password1': 'newpassword123'
        }
        response = client.post(url, data)
        assert User.objects.filter(username='newuser').exists()
        assert response.status_code == 302
        assert response.url == reverse('index')

    def test_register_view_invalid_email(self, client):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',  # Invalid email
            'password': 'password123',
            'password1': 'password123'
        }
        response = client.post(url, data)
        assert response.status_code == 200  
        assert 'Email is wrong!' in [str(msg) for msg in messages.get_messages(response.wsgi_request)]

    def test_register_view_password_mismatch(self, client):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password1': 'differentpassword'  # Mismatched password
        }
        response = client.post(url, data)
        assert response.status_code == 200  
        assert 'Passwords did not match!' in [str(msg) for msg in messages.get_messages(response.wsgi_request)]

    def test_register_view_user_creation_failure(self, client):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password1': 'password123'
        }
        # Mocking User Creation Failure
        with patch.object(User.objects, 'create_user', side_effect=Exception("Mocked exception")):
            response = client.post(url, data)
        assert response.status_code == 200  
        assert 'Something is going wrong! (Mocked exception)' in [str(msg) for msg in messages.get_messages(response.wsgi_request)]

class TestLogoutView:
    def test_logout_view(self, logged_in_client):
        url = reverse('logout')
        response = logged_in_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')