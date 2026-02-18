from rest_framework import serializers
from .models import AuditLog, InmateProfile, MedicalFile
from django.contrib.auth.models import User, Group

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


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'groups']