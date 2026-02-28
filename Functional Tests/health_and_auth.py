import pytest
from rest_framework import status
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestHealthAndAuth:

    def test_health_check_endpoint(self, api_client):

        
        response = api_client.get('/api/v1/root/')
        assert response.status_code == status.HTTP_200_OK
        assert 'Welcome to the Arkham Asylum Backend!' in response.json()['message']

    def test_user_registration(self, api_client):

        
        payload = {
            "username": "new_inmate_handler",
            "password": "strongpassword123",
            "email": "handler@arkham.com"
        }
        response = api_client.post('/api/auth/users/', data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="new_inmate_handler").exists()

    def test_jwt_create(self, api_client):

        
        User.objects.create_user(username='test_login', password='password123')
        payload = {
            "username": "test_login",
            "password": "password123"
        }
        response = api_client.post('/api/auth/jwt/create/', data=payload)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_jwt_refresh(self, api_client):

        
        User.objects.create_user(username='test_refresh', password='password123')
        payload = {"username": "test_refresh", "password": "password123"}
        response = api_client.post('/api/auth/jwt/create/', data=payload)
        refresh_token = response.data['refresh']

        refresh_payload = {"refresh": refresh_token}
        refresh_response = api_client.post('/api/auth/jwt/refresh/', data=refresh_payload)
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data

    def test_jwt_verify(self, api_client):

        
        User.objects.create_user(username='test_verify', password='password123')
        payload = {"username": "test_verify", "password": "password123"}
        response = api_client.post('/api/auth/jwt/create/', data=payload)
        access_token = response.data['access']

        verify_payload = {"token": access_token}
        verify_response = api_client.post('/api/auth/jwt/verify/', data=verify_payload)
        
        assert verify_response.status_code == status.HTTP_200_OK
