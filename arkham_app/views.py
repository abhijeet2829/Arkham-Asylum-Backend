from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog, InmateProfile, MedicalFile
from .serializers import AuditLogSerializer, InmateProfileSerializer, MedicalFileSerializer, UserSerializer, InmateDetailSerializer
from .permissions import StrictDjangoModelPermissions, IsSecurityStaff, IsSuperAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from .decorators import audit_read
from .throttles import InmateTransferThrottle, MedicalAccessThrottle, AuditLogAccessThrottle
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if not self.request.user.groups.filter(name__in=['Public Visitor', 'Security Staff']).exists():
                return InmateDetailSerializer
        return super().get_serializer_class()
    
    @audit_read(InmateProfile)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# Custom permission to allow 'Security Staff' to perform controlled Update operations on only 'cell_block' field of 'InmateProfile' model
    @action(detail=True, methods=['post'], permission_classes=[IsSecurityStaff], throttle_classes=[InmateTransferThrottle])
    def transfer(self, request, pk=None):
        inmate = self.get_object() # Model instance of InmateProfile, not a regular Dictionary. The only way to spot such an instance's to study the entire codeblock & PREDICT it represents a database row
        new_block = request.data.get("cell_block")

        if not new_block:
            return Response({"error": "cell_block is required"}, status=400)

        inmate.cell_block = new_block
        inmate.save()
        
        return Response({
            "status": "Inmate transferred",
            "inmate": inmate.name,
            "new_block": inmate.cell_block
        })


class MedicalViewSet(viewsets.ModelViewSet):
    queryset = MedicalFile.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = MedicalFileSerializer
    pagination_class = ArkhamPagination
    throttle_classes = [MedicalAccessThrottle]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @audit_read(MedicalFile)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    http_method_names = ['get', 'patch']