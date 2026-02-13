from rest_framework import serializers
from .models import AuditLog, InmateProfile, MedicalFile

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"

class InmateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InmateProfile
        fields = "__all__"

class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFile
        fields = "__all__"