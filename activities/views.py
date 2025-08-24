# activities/views.py

from rest_framework import viewsets, permissions
from .models import Activity, ActivityCategory, ActivitySubcategory
from .serializers import ActivitySerializer, ActivityCategorySerializer, ActivitySubcategorySerializer


class IsGymOwnerOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.gym.owner == request.user or request.user in obj.gym.staff.all()


class ActivityCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ActivityCategory.objects.all()
        return ActivityCategory.objects.filter(gym__owner=user)


class ActivitySubcategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySubcategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ActivitySubcategory.objects.all()
        return ActivitySubcategory.objects.filter(category__gym__owner=user)


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Activity.objects.all()
        return Activity.objects.filter(gym__owner=user)