from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bonus, BonusActivity
from .serializers import BonusSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404


class BonusViewSet(viewsets.ModelViewSet):
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Si es cliente (logueado desde Flutter con user vinculado)
        if hasattr(user, 'client'):
            return Bonus.objects.filter(
                client=user.client,
                expires_at__gte=timezone.now().date()
            )

        # Si es staff o admin
        if user.is_superadmin or user.is_admin:
            return Bonus.objects.all()

        # Fallback vacío
        return Bonus.objects.none()

    @action(detail=True, methods=['post'], url_path='use-activity')
    def use_activity(self, request, pk=None):
        activity_id = request.data.get('activity_id')
        bonus = self.get_object()

        try:
            activity = bonus.activities.get(pk=activity_id)
        except BonusActivity.DoesNotExist:
            return Response({'error': 'Actividad no encontrada'}, status=404)

        if bonus.get_remaining() <= 0:
            return Response({'error': 'Bono agotado'}, status=400)

        activity.register_use()
        bonus.used_quantity += 1
        bonus.save()

        return Response({
            'message': 'Uso registrado correctamente',
            'remaining': bonus.get_remaining()
        })
