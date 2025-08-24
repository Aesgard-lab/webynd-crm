# saas/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from core.pagination import DefaultPagination
from .models import Module, ModulePrice
from .serializers import ModuleSerializer, ModulePriceSerializer


class IsAuthenticatedReadWriteRestricted(permissions.BasePermission):
    """
    - Cualquier usuario autenticado: lectura
    - Escritura: superuser/staff/admin
    """
    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(u, "is_superuser", False) or getattr(u, "is_staff", False) or getattr(u, "is_admin", False)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().order_by("code")
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedReadWriteRestricted]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["code", "name", "description"]
    ordering_fields = ["code", "name", "created_at", "updated_at"]
    ordering = ["code"]


class ModulePriceViewSet(viewsets.ModelViewSet):
    queryset = ModulePrice.objects.select_related("module").all().order_by("module__code", "cycle")
    serializer_class = ModulePriceSerializer
    permission_classes = [IsAuthenticatedReadWriteRestricted]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["module", "cycle", "currency", "is_active"]
    search_fields = ["module__name", "module__code"]
    ordering_fields = ["module__code", "cycle", "amount", "created_at", "updated_at", "is_active"]
    ordering = ["module__code", "cycle"]
