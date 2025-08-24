from django.db.models import Count
from rest_framework import viewsets, permissions
from .models import ScheduledSession, Reservation
from .serializers import ScheduledSessionSerializer, ReservationSerializer
from core.models import NotificationRule
from marketing.utils import send_notification_email

class IsGymAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin or request.user.is_admin
        )

class ScheduledSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledSessionSerializer
    permission_classes = [IsGymAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return ScheduledSession.objects.all().annotate(
                reservation_count=Count('reservations')
            )
        return ScheduledSession.objects.filter(gym__owner=user).annotate(
            reservation_count=Count('reservations')
        )

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsGymAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return Reservation.objects.all()
        return Reservation.objects.filter(session__gym__owner=user)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsGymAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return Reservation.objects.all()
        return Reservation.objects.filter(session__gym__owner=user)

    def perform_create(self, serializer):
        reservation = serializer.save()

        # 🔔 Enviar notificación al cliente
        gym = reservation.session.gym
        client = reservation.client

        rules = NotificationRule.objects.filter(
            gym=gym,
            trigger='booking_created',
            enabled=True,
            send_to_client=True
        ).select_related('template')

        for rule in rules:
            if client.email:
                send_notification_email(
                    gym=gym,
                    template=rule.template,
                    subject="Reserva confirmada",
                    to_email=client.email
                )