import pytest
from rest_framework import status
from arkham_app.models import AuditLog, MedicalFile

@pytest.mark.django_db
class TestAuditLogs:

    def test_audit_log_list(self, super_admin_client, dummy_medical_file):

        
        response = super_admin_client.get('/api/v1/default-router/security-logs')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        actions = [log['action_type'] for log in response.data['results']]
        assert 'CREATE' in actions

    def test_audit_immutable(self, super_admin_client, dummy_medical_file):

        
        log = AuditLog.objects.first()
        post_res = super_admin_client.post('/api/v1/default-router/security-logs', data={"action_type": "FAKE"})
        assert post_res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        patch_res = super_admin_client.patch(f'/api/v1/default-router/security-logs/{log.id}', data={"action_type": "FAKE"})
        assert patch_res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        del_res = super_admin_client.delete(f'/api/v1/default-router/security-logs/{log.id}')
        assert del_res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
