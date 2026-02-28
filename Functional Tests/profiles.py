import pytest
from rest_framework import status

@pytest.mark.django_db
class TestProfiles:

    def test_get_own_profile(self, medical_staff_client):

        
        response = medical_staff_client.get('/api/auth/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'dr_arkham'
        assert response.data['email'] == 'doc@arkham.com'

    def test_update_own_profile(self, medical_staff_client):

        
        payload = {"email": "updated_doc@arkham.com"}
        response = medical_staff_client.patch('/api/auth/users/me/', data=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'updated_doc@arkham.com'

    def test_set_password(self, medical_staff_client, medical_staff_user, api_client):

        
        payload = {
            "new_password": "new_secure_password123",
            "current_password": "password123"
        }
        response = medical_staff_client.post('/api/auth/users/set_password/', data=payload)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        login_payload = {"username": "dr_arkham", "password": "password123"}
        fail_response = api_client.post('/api/auth/jwt/create/', data=login_payload)
        assert fail_response.status_code == status.HTTP_401_UNAUTHORIZED

        login_payload["password"] = "new_secure_password123"
        success_response = api_client.post('/api/auth/jwt/create/', data=login_payload)
        assert success_response.status_code == status.HTTP_200_OK
