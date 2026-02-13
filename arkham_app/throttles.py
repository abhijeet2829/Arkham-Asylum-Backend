from rest_framework.throttling import UserRateThrottle

class InmateTransferThrottle(UserRateThrottle):
    scope = 'inmate_transfer'

class MedicalAccessThrottle(UserRateThrottle):
    scope = 'medical_file_access'

class AuditLogAccessThrottle(UserRateThrottle):
    scope = 'audit_log_access'