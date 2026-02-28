import pytest
from rest_framework import status
from arkham_app.models import MedicalFile, AuditLog, InmateProfile

@pytest.mark.django_db
class TestMedicalRecords:

    def test_medical_list_filtering(self, medical_staff_client, dummy_medical_file, db, cell_blocks):

        
        inmate2 = InmateProfile.objects.create(name='Riddler', alias='Edward Nygma', cell_block=cell_blocks['B'])
        MedicalFile.objects.create(inmate=inmate2, referral_diagnosis='Obsession')

        response = medical_staff_client.get('/api/v1/default-router/medical-records')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == dummy_medical_file.id

    def test_medical_detailed_read_audit(self, medical_staff_client, dummy_medical_file):

        
        record_count = AuditLog.objects.filter(target_model='MedicalFile', target_id=dummy_medical_file.id, action_type='DETAILED_READ').count()
        
        response = medical_staff_client.get(f'/api/v1/default-router/medical-records/{dummy_medical_file.id}')
        assert response.status_code == status.HTTP_200_OK
        
        new_record_count = AuditLog.objects.filter(target_model='MedicalFile', target_id=dummy_medical_file.id, action_type='DETAILED_READ').count()
        assert new_record_count == record_count + 1

    def test_medical_update(self, medical_staff_client, dummy_medical_file):

        
        payload = {"internal_diagnosis": "Treated successfully"}
        response = medical_staff_client.patch(f'/api/v1/default-router/medical-records/{dummy_medical_file.id}', data=payload)
        assert response.status_code == status.HTTP_200_OK
        
        dummy_medical_file.refresh_from_db()
        assert dummy_medical_file.internal_diagnosis == "Treated successfully"

    def test_medical_delete_forbidden_for_staff(self, medical_staff_client, dummy_medical_file):

        
        response = medical_staff_client.delete(f'/api/v1/default-router/medical-records/{dummy_medical_file.id}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_medical_hard_delete_admin(self, super_admin_client, dummy_medical_file):

        
        response = super_admin_client.delete(f'/api/v1/default-router/medical-records/{dummy_medical_file.id}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not MedicalFile.objects.filter(id=dummy_medical_file.id).exists()
