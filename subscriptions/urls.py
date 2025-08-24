# subscriptions/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, SubscriptionActivityUseView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('activity/use/', SubscriptionActivityUseView.as_view(), name='subscription-activity-use'),
]
