from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from scheduler.models import Reservation
from core.models import NotificationRule
from marketing.utils import send_notification_email


@shared_task
def check_booking_notifications():
    now = timezone.now()

    # --- BOOKING REMINDER (ej. 2h antes) ---
    reminder_rules = NotificationRule.objects.filter(
        trigger='booking_reminder',
        enabled=True,
        send_to_client=True
    ).select_related('gym', 'template')

    for rule in reminder_rules:
        hours_before = rule.hours_before or 2
        target_start = now + timedelta(hours=hours_before)

        upcoming_reservations = Reservation.objects.filter(
            session__gym=rule.gym,
            session__start_time__gte=target_start,
            session__start_time__lt=target_start + timedelta(minutes=30),
            cancelled=False,
        ).select_related('client', 'session')

        for r in upcoming_reservations:
            if r.client.email:
                send_notification_email(
                    gym=rule.gym,
                    template=rule.template,
                    subject="Recordatorio de tu reserva",
                    to_email=r.client.email
                )

    # --- BOOKING THANKS (ej. 1h después) ---
    thanks_rules = NotificationRule.objects.filter(
        trigger='booking_thanks',
        enabled=True,
        send_to_client=True
    ).select_related('gym', 'template')

    for rule in thanks_rules:
        hours_after = rule.hours_before or 1
        target_end = now - timedelta(hours=hours_after)

        recent_reservations = Reservation.objects.filter(
            session__gym=rule.gym,
            session__end_time__gte=target_end - timedelta(minutes=30),
            session__end_time__lt=target_end,
            checked_in=True,
            cancelled=False,
        ).select_related('client', 'session')

        for r in recent_reservations:
            if r.client.email:
                send_notification_email(
                    gym=rule.gym,
                    template=rule.template,
                    subject="Gracias por asistir",
                    to_email=r.client.email
                )
