from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduledSessionViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'sessions', ScheduledSessionViewSet, basename='sessions')
router.register(r'reservations', ReservationViewSet, basename='reservations')

urlpatterns = [
    path('', include(router.urls)),
]
