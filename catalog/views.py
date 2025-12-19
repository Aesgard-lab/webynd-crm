from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from gyms.models import GymMembership, Gym
from .models import CatalogCategory, CatalogSubcategory
from .serializers import CatalogCategorySerializer, CatalogSubcategorySerializer


def allowed_gym_ids(user):
    gym_ids = list(
        GymMembership.objects.filter(user=user, is_active=True).values_list("gym_id", flat=True)
    )
    owner_ids = list(Gym.objects.filter(owner=user).values_list("id", flat=True))
    return list(set(gym_ids + owner_ids))


def allowed_franchise_ids(user):
    gids = allowed_gym_ids(user)
    return list(
        Gym.objects.filter(id__in=gids)
        .exclude(franchise_id__isnull=True)
        .values_list("franchise_id", flat=True)
        .distinct()
    )


class CatalogCategoryViewSet(viewsets.ModelViewSet):
    queryset = CatalogCategory.objects.all()
    serializer_class = CatalogCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["module", "scope", "gym", "franchise", "is_active"]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.is_superuser:
            return qs

        gids = allowed_gym_ids(user)
        fids = allowed_franchise_ids(user)

        return qs.filter(
            Q(scope="gym", gym_id__in=gids) |
            Q(scope="franchise", franchise_id__in=fids)
        ).distinct()


class CatalogSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = CatalogSubcategory.objects.select_related("category").all()
    serializer_class = CatalogSubcategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "category__name"]
    ordering_fields = ["id", "name", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.is_superuser:
            return qs

        gids = allowed_gym_ids(user)
        fids = allowed_franchise_ids(user)

        return qs.filter(
            Q(category__scope="gym", category__gym_id__in=gids) |
            Q(category__scope="franchise", category__franchise_id__in=fids)
        ).distinct()
