from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet, ProductSubCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-subcategories', ProductSubCategoryViewSet)

urlpatterns = router.urls
