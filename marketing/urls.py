from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarketingTemplateViewSet,
    MarketingCampaignViewSet,
    CampaignRecipientViewSet
)

router = DefaultRouter()
router.register(r'templates', MarketingTemplateViewSet)
router.register(r'campaigns', MarketingCampaignViewSet)
router.register(r'recipients', CampaignRecipientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
