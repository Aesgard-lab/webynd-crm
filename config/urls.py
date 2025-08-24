from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.views import MeView

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- Auth / identidad ---
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", MeView.as_view(), name="me"),

    # --- Routers de las apps (todas bajo /api/) ---
    # Cada app debe definir su propio router/paths dentro de su urls.py
    # Por ejemplo, clients/urls.py registra 'clients' en un DefaultRouter()
    path("api/", include("clients.urls")),         # → /api/clients/
    path("api/", include("bonuses.urls")),         # → /api/bonuses/...
    path("api/", include("subscriptions.urls")),   # → /api/subscriptions/...
    path("api/", include("products.urls")),
    path("api/", include("services.urls")),
    path("api/", include("staff.urls")),
    path("api/", include("scheduler.urls")),
    path("api/", include("marketing.urls")),
    path("api/", include("dashboard.urls")),
    path("api/", include("reports.urls")),
    path("api/", include("gyms.urls")),            # → /api/gyms/
    path("api/", include("auth_app.urls")),        # endpoints extra de auth_app si los hubiera
    path('api/superadmin/saas/', include('saas.urls')),
    path("api/superadmin/orgs/", include("gyms.urls")),
    path("api/superadmin/stripe/", include("saas_payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
