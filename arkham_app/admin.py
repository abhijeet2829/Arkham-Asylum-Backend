from django.contrib import admin
from .models import InmateProfile, MedicalFile, AuditLog

admin.site.register(InmateProfile)
admin.site.register(MedicalFile)
admin.site.register(AuditLog)