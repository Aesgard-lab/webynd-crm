# clients/views.py
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Client
from gyms.models import Gym
from .serializers import ClientSerializer, ClientDetailSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Usuarios autenticados pueden leer.
    Para escribir (POST/PUT/PATCH/DELETE) requiere superuser, admin o staff.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            getattr(user, "is_superuser", False)
            or getattr(user, "is_admin", False)
            or getattr(user, "is_staff", False)
        )


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]
    

    # Filtros DRF
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["id", "gym", "email", "alert_level"]
    search_fields = ["first_name", "last_name", "email", "dni_number"]
    ordering_fields = ["id", "first_name", "last_name", "email", "created_at"]
    ordering = ["id"]

    def get_queryset(self):
        user = self.request.user

        # Superusuario: todos; si viene ?gym=<id> filtra por ese gym
        if getattr(user, "is_superuser", False):
            qs = Client.objects.all()
            gym_id = self.request.query_params.get("gym")
            if gym_id:
                qs = qs.filter(gym_id=gym_id)
            return qs.order_by("id")

        # Usuarios con relación a gyms (ManyToMany user.gyms)
        gyms_qs = None
        if hasattr(user, "gyms"):
            try:
                gyms_qs = user.gyms.all()
            except Exception:
                gyms_qs = None

        # Alternativa: gyms donde es owner
        if gyms_qs is None:
            try:
                gyms_qs = Gym.objects.filter(owner=user)
            except Exception:
                gyms_qs = Gym.objects.none()

        if gyms_qs is not None and gyms_qs.exists():
            return Client.objects.filter(gym__in=gyms_qs).order_by("id")

        # Fallback sin gyms asociados
        return Client.objects.none()

    def get_serializer_class(self):
        return ClientDetailSerializer if self.action == "retrieve" else ClientSerializer

    def perform_create(self, serializer):
        """
        Asigna el gym:
        - Superuser: debe indicar gym explícitamente en el POST.
        - No superuser: se usa el primer gym asociado (o gym owner).
        """
        user = self.request.user

        if getattr(user, "is_superuser", False):
            gym_id = self.request.data.get("gym")
            if not gym_id:
                raise serializers.ValidationError({"gym": "Este campo es obligatorio para superusuarios."})
            try:
                gym = Gym.objects.get(id=gym_id)
            except Gym.DoesNotExist:
                raise serializers.ValidationError({"gym": "El gimnasio indicado no existe."})
            serializer.save(gym=gym)
            return

        # No superuser
        gym = None
        if hasattr(user, "gyms"):
            try:
                gym = user.gyms.first()
            except Exception:
                gym = None
        if not gym:
            try:
                gym = Gym.objects.filter(owner=user).first()
            except Exception:
                gym = None
        if not gym:
            raise serializers.ValidationError({"gym": "Este usuario no tiene un gimnasio asociado."})

        serializer.save(gym=gym)

    # Convierte IntegrityError en 400 (evita 500 Internal Server Error)
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            raise serializers.ValidationError({"non_field_errors": [str(e)]})

    @action(detail=True, methods=["get"], url_path="billings")
    def filtered_billings(self, request, pk=None):
        """
        GET /api/clients/{id}/billings/?from=YYYY-MM-DD&to=YYYY-MM-DD
        """
        client = self.get_object()
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")

        qs = client.billings.all()
        if from_date:
            qs = qs.filter(created_at__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__lte=to_date)

        from billing.serializers import BillingEntrySerializer
        serializer = BillingEntrySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
