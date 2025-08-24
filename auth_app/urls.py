# auth_app/urls.py
from django.urls import path
from django.urls import path
from .views import SetCurrentGymView
from .views import MyTokenObtainPairView, MyTokenRefreshView, MeView

urlpatterns = [
    path("auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="auth_me"),
    path("auth/set-current-gym/", SetCurrentGymView.as_view(), name="set-current-gym"),
]

