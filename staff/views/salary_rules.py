from rest_framework import viewsets, permissions
from staff.models import SalaryRule
from staff.serializers import SalaryRuleSerializer

class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin or request.user.is_admin
        )

class SalaryRuleViewSet(viewsets.ModelViewSet):
    queryset = SalaryRule.objects.all()
    serializer_class = SalaryRuleSerializer
    permission_classes = [IsSuperAdminOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return SalaryRule.objects.all()
        return SalaryRule.objects.filter(staff__gym__owner=user)
