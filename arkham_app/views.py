from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog, InmateProfile, MedicalFile
from .serializers import AuditLogSerializer, InmateProfileSerializer, MedicalFileSerializer
from .permissions import StrictDjangoModelPermissions, IsSecurityStaff
from rest_framework.decorators import action
from rest_framework.response import Response
from .decorators import audit_read
from .throttles import InmateTransferThrottle, MedicalAccessThrottle, AuditLogAccessThrottle



def test(request):
    return JsonResponse({"message": "Welcome to the Arkham Asylum Backend!"})


class SecurityViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = AuditLogSerializer
    throttle_classes = [AuditLogAccessThrottle]


class InmateViewSet(viewsets.ModelViewSet):
    queryset = InmateProfile.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    serializer_class = InmateProfileSerializer
    
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
    throttle_classes = [MedicalAccessThrottle]

    @audit_read(MedicalFile)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)