from rest_framework.permissions import DjangoModelPermissions, BasePermission



class StrictDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']


class IsSecurityStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name='Security Staff').exists()