from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog, InmateProfile, MedicalFile
from .serializers import AuditLogSerializer, InmateProfileSerializer, MedicalFileSerializer, UserSerializer, InmateDetailSerializer
from .permissions import StrictDjangoModelPermissions, IsSuperAdmin
from rest_framework.response import Response
from .decorators import audit_read
from .throttles import MedicalAccessThrottle, AuditLogAccessThrottle
from django.contrib.auth.models import User
from .filters import InmateProfileFilter
from .pagination import ArkhamPagination



def test(request):
    return JsonResponse({"message": "Welcome to the Arkham Asylum Backend!"})


class SecurityViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = AuditLogSerializer
    throttle_classes = [AuditLogAccessThrottle]
    http_method_names = ['get']


class InmateViewSet(viewsets.ModelViewSet):
    queryset = InmateProfile.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = InmateProfileSerializer
    filterset_class = InmateProfileFilter
    pagination_class = ArkhamPagination
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.action == 'partial_update':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if not self.request.user.groups.filter(name__in=['Public Visitor', 'Security Staff']).exists():
                return InmateDetailSerializer
        return super().get_serializer_class()
    
    @audit_read(InmateProfile)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        is_security = user.groups.filter(name='Security Staff').exists()

        # Only Super Admins and Security Staff can PATCH inmates
        if not user.is_superuser and not is_security:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)

        # Security Staff can only update cell_block
        if is_security and set(request.data.keys()) - {'cell_block'}:
            return Response({"error": "Security Staff can only update cell_block."}, status=403)

        inmate = self.get_object()

        # --- TRANSFER SAFETY ENGINE ---
        # Only fires for Security Staff changing cell_block
        if 'cell_block' in request.data and is_security:
            medical_file = getattr(inmate, 'medicalfile', None)
            if not medical_file:
                return Response({"error": "No medical file found for this inmate. Transfer blocked."}, status=403)

            now = timezone.now()

            # Check for recent Medical Staff review (< 7 days)
            medical_check = AuditLog.objects.filter(
                target_model='MedicalFile',
                target_id=medical_file.id,
                actor_group='Medical Staff',
                action_type__in=['DETAILED_READ', 'UPDATE'],
                timestamp__gte=now - timedelta(days=7)
            ).exists()

            if not medical_check:
                return Response({
                    "error": "Transfer blocked. No Medical Staff has reviewed or updated this inmate's file in the last 7 days."
                }, status=403)

            # Check for recent Super Admin awareness (< 1 day)
            admin_check = AuditLog.objects.filter(
                target_model='MedicalFile',
                target_id=medical_file.id,
                actor_group='Super Admin',
                action_type='DETAILED_READ',
                timestamp__gte=now - timedelta(days=1)
            ).exists()

            if not admin_check:
                return Response({
                    "error": "Transfer blocked. No Super Admin has reviewed this inmate's file in the last 24 hours."
                }, status=403)
        # --- END SAFETY ENGINE ---

        return super().partial_update(request, *args, **kwargs)


class MedicalViewSet(viewsets.ModelViewSet):
    queryset = MedicalFile.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = MedicalFileSerializer
    pagination_class = ArkhamPagination
    throttle_classes = [MedicalAccessThrottle]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.user.groups.filter(name='Medical Staff').exists():
            return MedicalFile.objects.filter(assigned_to=self.request.user)
        return MedicalFile.objects.all()

    @audit_read(MedicalFile)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    http_method_names = ['get', 'patch']