from rest_framework.routers import DefaultRouter
from .views import BonusViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'bonuses', BonusViewSet, basename='bonuses')

urlpatterns = [
    path('', include(router.urls)),
]
