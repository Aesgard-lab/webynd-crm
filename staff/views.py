from rest_framework import viewsets, permissions
from .models import Staff
from .serializers import StaffSerializer

class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin or request.user.is_admin
        )


