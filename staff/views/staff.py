from rest_framework import viewsets, permissions
from staff.models import Staff
from staff.serializers import StaffSerializer


class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin or request.user.is_admin
        )


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    permission_classes = [IsSuperAdminOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return Staff.objects.all()
        return Staff.objects.filter(gym__owner=user)
