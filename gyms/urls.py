# gyms/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FranchiseViewSet, GymViewSet, GymBrandView

router = DefaultRouter()
router.register(r"franchises", FranchiseViewSet, basename="franchise")
router.register(r"gyms", GymViewSet, basename="gym")

urlpatterns = [
    path("", include(router.urls)),
    path("gyms/brand/<int:gym_id>/", GymBrandView.as_view(), name="gym-brand"),
]
