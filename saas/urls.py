# saas/urls.py
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, ModulePriceViewSet

router = DefaultRouter()
router.register(r"modules", ModuleViewSet, basename="module")
router.register(r"module-prices", ModulePriceViewSet, basename="moduleprice")

urlpatterns = router.urls
