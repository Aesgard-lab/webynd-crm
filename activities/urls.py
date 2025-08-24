# activities/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityCategoryViewSet, ActivitySubcategoryViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'categories', ActivityCategoryViewSet, basename='activity-categories')
router.register(r'subcategories', ActivitySubcategoryViewSet, basename='activity-subcategories')

urlpatterns = [
    path('', include(router.urls)),
]
