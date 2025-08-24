# saas_payments/urls.py
from django.urls import path

from .views import EnsureCustomerView, CheckoutView, PortalView
from .webhooks import StripeWebhookView

app_name = "saas_payments"

urlpatterns = [
    path(
        "customers/<int:gym_id>/ensure/",
        EnsureCustomerView.as_view(),
        name="stripe-ensure-customer"
    ),
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="stripe-checkout"
    ),
    path(
        "portal/<int:gym_id>/",
        PortalView.as_view(),
        name="stripe-portal"
    ),
    path(
        "webhook/",
        StripeWebhookView.as_view(),
        name="stripe-webhook"
    ),
]
