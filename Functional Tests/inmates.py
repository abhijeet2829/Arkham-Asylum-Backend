import pytest
from rest_framework import status
from arkham_app.models import InmateProfile, MedicalFile, AuditLog, CellBlock
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestInmateManagement:

    def test_inmate_list(self, security_staff_client, dummy_inmate):

        
        response = security_staff_client.get('/api/v1/default-router/inmates')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert response.data['results'][0]['name'] == 'Joker'

    def test_inmate_retrieve(self, medical_staff_client, dummy_inmate):

        
        response = medical_staff_client.get(f'/api/v1/default-router/inmates/{dummy_inmate.id}')
        assert response.status_code == status.HTTP_200_OK
        assert 'medical_record' in response.data

    def test_inmate_retrieve_public(self, public_visitor_client, dummy_inmate):

        
        response = public_visitor_client.get(f'/api/v1/default-router/inmates/{dummy_inmate.id}')
        assert response.status_code == status.HTTP_200_OK
        assert 'medical_record' not in response.data

    def test_inmate_admission_success(self, super_admin_client, cell_blocks):

        
        payload = {
            "name": "Bane",
            "alias": "Dorrance",
            "cell_block": "Block-B",
            "referral_diagnosis": "Venom addiction"
        }
        response = super_admin_client.post('/api/v1/default-router/inmates', data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        
        inmate = InmateProfile.objects.get(name="Bane")
        medical_file = MedicalFile.objects.get(inmate=inmate)
        assert medical_file.referral_diagnosis == "Venom addiction"

    def test_inmate_admission_full_capacity(self, super_admin_client, cell_blocks, dummy_inmate):

        
        block_a = cell_blocks['A']
        InmateProfile.objects.create(name='Inmate1', alias='A1', cell_block=block_a)
        
        payload = {
            "name": "Penguin",
            "alias": "Cobblepot",
            "cell_block": "Block-A",
            "referral_diagnosis": "Narcissism"
        }
        response = super_admin_client.post('/api/v1/default-router/inmates', data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "is at full capacity" in response.data['error']

    def test_inmate_transfer_success(self, security_staff_client, dummy_inmate, dummy_medical_file):

        
        AuditLog.objects.create(
            actor_name='dr_arkham', actor_group='Medical Staff', action_type='DETAILED_READ',
            target_model='MedicalFile', target_id=dummy_medical_file.id,
            timestamp=timezone.now() - timedelta(days=2)
        )
        AuditLog.objects.create(
            actor_name='super_admin', actor_group='Super Admin', action_type='DETAILED_READ',
            target_model='MedicalFile', target_id=dummy_medical_file.id,
            timestamp=timezone.now() - timedelta(hours=5)
        )

        payload = {"cell_block": "Block-C"}
        response = security_staff_client.patch(f'/api/v1/default-router/inmates/{dummy_inmate.id}', data=payload)
        
        assert response.status_code == status.HTTP_200_OK
        dummy_inmate.refresh_from_db()
        assert dummy_inmate.cell_block.name == 'Block-C'

    def test_inmate_transfer_blocked_no_admin_review(self, security_staff_client, dummy_inmate, dummy_medical_file):

        
        AuditLog.objects.create(
            actor_name='dr_arkham', actor_group='Medical Staff', action_type='DETAILED_READ',
            target_model='MedicalFile', target_id=dummy_medical_file.id,
            timestamp=timezone.now() - timedelta(days=2)
        )
        
        payload = {"cell_block": "Block-C"}
        response = security_staff_client.patch(f'/api/v1/default-router/inmates/{dummy_inmate.id}', data=payload)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "No Super Admin has reviewed" in response.data['error']
