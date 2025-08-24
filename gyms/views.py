from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers
from rest_framework.filters import SearchFilter, OrderingFilter

from core.pagination import DefaultPagination  # usa la paginación estándar count/results
from .models import Franchise, Gym
from .serializers import FranchiseSerializer, GymSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


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


class FranchiseViewSet(viewsets.ModelViewSet):
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticatedReadWriteRestricted]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "owner"]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name"]

    def get_queryset(self):
        u = self.request.user
        qs = Franchise.objects.select_related("owner")
        if getattr(u, "is_superuser", False):
            return qs.order_by("name")
        return qs.filter(owner=u).order_by("name")

    def perform_create(self, serializer):
        """
        - Superuser: puede asignar 'owner' por payload
        - Si no se envía, usar el superuser como owner
        - Resto: la franquicia pertenece al usuario actual
        """
        u = self.request.user
        if getattr(u, "is_superuser", False):
            owner_id = self.request.data.get("owner")
            if owner_id:
                try:
                    owner = User.objects.get(pk=owner_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError({"owner": "El propietario indicado no existe."})
                serializer.save(owner=owner)
                return
            # Si eres superuser y no mandas owner, usarte como owner por defecto
            serializer.save(owner=u)
        else:
            serializer.save(owner=u)


class GymViewSet(viewsets.ModelViewSet):
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticatedReadWriteRestricted]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["id", "owner", "franchise", "is_active", "country", "currency"]
    search_fields = ["name", "slug", "address", "franchise__name"]
    ordering_fields = ["id", "name", "created_at", "updated_at"]
    ordering = ["id"]

    def get_queryset(self):
        u = self.request.user
        qs = Gym.objects.select_related("owner", "franchise")
        if getattr(u, "is_superuser", False):
            return qs.order_by("id")
        return qs.filter(owner=u).order_by("id")

    def perform_create(self, serializer):
        """
        - Superuser: puede fijar 'owner'
        - Resto: el owner es el usuario actual
        """
        u = self.request.user
        if getattr(u, "is_superuser", False):
            owner_id = self.request.data.get("owner")
            if owner_id:
                try:
                    owner = User.objects.get(pk=owner_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError({"owner": "El propietario indicado no existe."})
                serializer.save(owner=owner)
                return
        serializer.save(owner=u)



class GymBrandView(APIView):
    """
    Devuelve la marca del gym (logo y colores), heredada de Franchise si existe.
    GET /api/gyms/brand/<gym_id>/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, gym_id: int):
        try:
            gym = Gym.objects.select_related("franchise").get(pk=gym_id)
        except Gym.DoesNotExist:
            return Response({"detail": "Gym not found."}, status=404)

        franchise = gym.franchise
        data = {
            "gym_id": gym.id,
            "gym_name": gym.name,
            "logo": (franchise.logo.url if getattr(franchise, "logo", None) else None),
            "primary_color": getattr(franchise, "primary_color", None) or "#3d99f5",
            "secondary_color": getattr(franchise, "secondary_color", None) or "#111418",
        }
        return Response(data, status=200)
    
