from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CatalogCategoryViewSet, CatalogSubcategoryViewSet

router = DefaultRouter()
router.register(r"catalog-categories", CatalogCategoryViewSet, basename="catalog-categories")
router.register(r"catalog-subcategories", CatalogSubcategoryViewSet, basename="catalog-subcategories")

urlpatterns = [
    path("", include(router.urls)),
]
