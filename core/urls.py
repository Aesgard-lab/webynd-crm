from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymSettingsViewSet, FranchiseSettingsViewSet, CurrencyConfigViewSet
from .views import NotificationRuleViewSet


router = DefaultRouter()
router.register(r'gym-settings', GymSettingsViewSet)
router.register(r'franchise-settings', FranchiseSettingsViewSet)
router.register(r'currencies', CurrencyConfigViewSet)
router.register(r'notification-rules', NotificationRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
