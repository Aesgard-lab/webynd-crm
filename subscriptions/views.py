# subscriptions/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer, SubscriptionActivityUseSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_superadmin', False):
            return Subscription.objects.all()
        return Subscription.objects.filter(client__gym__owner=user)

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.copy_plan_activities()


class SubscriptionActivityUseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubscriptionActivityUseSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
