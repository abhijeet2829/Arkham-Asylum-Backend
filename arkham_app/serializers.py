from rest_framework import serializers
from .models import AuditLog, CellBlock, InmateProfile, MedicalFile
from django.contrib.auth.models import User, Group
from django.db import transaction


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"

class CellBlockSerializer(serializers.ModelSerializer):
    current_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CellBlock
        fields = ['id', 'name', 'max_capacity', 'current_count']

class InmateProfileSerializer(serializers.ModelSerializer):
    cell_block = serializers.SlugRelatedField(
        slug_field='name', 
        queryset=CellBlock.objects.all()
    )
    referral_diagnosis = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = InmateProfile
        fields = ['id', 'name', 'alias', 'cell_block', 'status', 'referral_diagnosis']

    def create(self, validated_data):
        referral = validated_data.pop('referral_diagnosis')

        with transaction.atomic():
            inmate = InmateProfile.objects.create(**validated_data)
            MedicalFile.objects.create(
                inmate=inmate,
                referral_diagnosis=referral
            )

        return inmate

class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFile
        fields = "__all__"

class InmateDetailSerializer(serializers.ModelSerializer):
    cell_block = serializers.SlugRelatedField(
        slug_field='name', 
        queryset=CellBlock.objects.all()
    )
    medical_record = MedicalFileSerializer(source='medicalfile', read_only=True)

    class Meta:
        model = InmateProfile
        fields = ['id', 'name', 'alias', 'cell_block', 'status', 'medical_record']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'groups']