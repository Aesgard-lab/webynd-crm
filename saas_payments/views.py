# saas_payments/views.py
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from gyms.models import Gym
from saas.models import ModulePrice
from .stripe_service import ensure_customer, create_checkout_session, create_billing_portal_session


class IsSuperAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and (u.is_superuser or u.is_staff or getattr(u, "is_admin", False)))


class EnsureCustomerView(APIView):
    permission_classes = [IsSuperAdminOrStaff]
    def post(self, request, gym_id: int):
        gym = get_object_or_404(Gym, pk=gym_id)
        customer = ensure_customer(gym)
        return Response({"gym": gym.id, "stripe_customer_id": customer.stripe_customer_id})


class CheckoutSerializer(serializers.Serializer):
    gym = serializers.IntegerField()
    items = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    success_url = serializers.URLField(required=False)
    cancel_url = serializers.URLField(required=False)


class CheckoutView(APIView):
    permission_classes = [IsSuperAdminOrStaff]
    def post(self, request):
        s = CheckoutSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        gym = get_object_or_404(Gym, pk=s.validated_data["gym"])
        # valida que existan los ModulePrice
        exists = ModulePrice.objects.filter(id__in=s.validated_data["items"]).count()
        if exists != len(s.validated_data["items"]):
            return Response({"detail": "Algún ModulePrice no existe."}, status=status.HTTP_400_BAD_REQUEST)

        url = create_checkout_session(
            gym=gym,
            module_price_ids=s.validated_data["items"],
            success_url=s.validated_data.get("success_url"),
            cancel_url=s.validated_data.get("cancel_url"),
        )
        return Response({"checkout_url": url})


class PortalView(APIView):
    permission_classes = [IsSuperAdminOrStaff]
    def post(self, request, gym_id: int):
        gym = get_object_or_404(Gym, pk=gym_id)
        return_url = request.data.get("return_url")
        url = create_billing_portal_session(gym=gym, return_url=return_url)
        return Response({"portal_url": url})
