import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from arkham_app.models import CellBlock, InmateProfile, MedicalFile
from django.core.cache import cache

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def super_admin_user(db):
    user = User.objects.create_superuser(username='super_admin', password='password123', email='admin@arkham.com')
    return user

@pytest.fixture
def medical_staff_user(db):
    user = User.objects.create_user(username='dr_arkham', password='password123', email='doc@arkham.com')
    group, _ = Group.objects.get_or_create(name='Medical Staff')
    
    inmate_ct = ContentType.objects.get_for_model(InmateProfile)
    medical_ct = ContentType.objects.get_for_model(MedicalFile)
    perms = Permission.objects.filter(
        content_type__in=[inmate_ct, medical_ct],
        codename__in=['view_inmateprofile', 'view_medicalfile', 'change_medicalfile']
    )
    group.permissions.set(perms)
    user.groups.add(group)
    return user

@pytest.fixture
def security_staff_user(db):
    user = User.objects.create_user(username='guard_gordon', password='password123', email='guard@arkham.com')
    group, _ = Group.objects.get_or_create(name='Security Staff')
    
    inmate_ct = ContentType.objects.get_for_model(InmateProfile)
    perms = Permission.objects.filter(
        content_type=inmate_ct,
        codename__in=['view_inmateprofile', 'change_inmateprofile']
    )
    group.permissions.set(perms)
    user.groups.add(group)
    return user

@pytest.fixture
def public_visitor_user(db):
    user = User.objects.create_user(username='nosy_reporter', password='password123', email='news@gotham.com')
    group, _ = Group.objects.get_or_create(name='Public Visitor')
    
    inmate_ct = ContentType.objects.get_for_model(InmateProfile)
    perms = Permission.objects.filter(
        content_type=inmate_ct,
        codename__in=['view_inmateprofile']
    )
    group.permissions.set(perms)
    user.groups.add(group)
    return user

@pytest.fixture
def super_admin_client(api_client, super_admin_user):
    api_client.force_authenticate(user=super_admin_user)
    return api_client

@pytest.fixture
def medical_staff_client(api_client, medical_staff_user):
    api_client.force_authenticate(user=medical_staff_user)
    return api_client

@pytest.fixture
def security_staff_client(api_client, security_staff_user):
    api_client.force_authenticate(user=security_staff_user)
    return api_client

@pytest.fixture
def public_visitor_client(api_client, public_visitor_user):
    api_client.force_authenticate(user=public_visitor_user)
    return api_client

@pytest.fixture
def cell_blocks(db):
    block_a = CellBlock.objects.create(name='Block-A', max_capacity=2)
    block_b = CellBlock.objects.create(name='Block-B', max_capacity=5)
    block_c = CellBlock.objects.create(name='Block-C', max_capacity=10)
    return {'A': block_a, 'B': block_b, 'C': block_c}

@pytest.fixture
def dummy_inmate(db, cell_blocks):
    inmate = InmateProfile.objects.create(
        name='Joker',
        alias='Red Hood',
        cell_block=cell_blocks['A'],
        status='ACTIVE'
    )
    MedicalFile.objects.create(inmate=inmate, referral_diagnosis='Psychosis')
    return inmate

@pytest.fixture
def dummy_medical_file(db, dummy_inmate, medical_staff_user):
    medical_file = dummy_inmate.medicalfile
    medical_file.internal_diagnosis = 'Severe sociopathy'
    medical_file.meds = 'Lithium'
    medical_file.assigned_to = medical_staff_user
    medical_file.save()
    return medical_file

