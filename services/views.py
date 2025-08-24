from rest_framework import viewsets, permissions
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer

class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin or request.user.is_admin
        )

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsSuperAdminOrAdmin]

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsSuperAdminOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return Service.objects.all()
        return Service.objects.filter(gym__owner=user)

    def perform_create(self, serializer):
        # Si es superadmin, se espera que envíe `gym` o `franchise`
        if self.request.user.is_admin:
            serializer.save(gym=self.request.user.gyms.first())
        else:
            serializer.save()
