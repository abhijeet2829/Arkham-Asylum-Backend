import pytest
from rest_framework import status

@pytest.mark.django_db
class TestSystemManagement:

    def test_cell_blocks_dashboard(self, super_admin_client, cell_blocks):

        
        response = super_admin_client.get('/api/v1/default-router/cell-blocks')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        assert response.data['results'][0]['name'] == 'Block-A'
        assert response.data['results'][0]['max_capacity'] == 2

    def test_cell_blocks_unauthorized(self, medical_staff_client):

        
        response = medical_staff_client.get('/api/v1/default-router/cell-blocks')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_groups_list(self, super_admin_client, medical_staff_user, security_staff_user):
        response = super_admin_client.get('/api/v1/default-router/user-groups')
        assert response.status_code == status.HTTP_200_OK
        usernames = [user['username'] for user in response.data['results']]
        assert 'dr_arkham' in usernames
        assert 'guard_gordon' in usernames

    def test_user_groups_update(self, super_admin_client, security_staff_user):

        
        payload = {"groups": []}
        response = super_admin_client.patch(
            f'/api/v1/default-router/user-groups/{security_staff_user.id}', 
            data=payload, 
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['groups'] == []

    def test_user_groups_unauthorized(self, security_staff_client):

        
        response = security_staff_client.get('/api/v1/default-router/user-groups')
        assert response.status_code == status.HTTP_403_FORBIDDEN
