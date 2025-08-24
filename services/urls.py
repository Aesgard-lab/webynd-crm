from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServiceCategoryViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-categories')

urlpatterns = [
    path('', include(router.urls)),
]
