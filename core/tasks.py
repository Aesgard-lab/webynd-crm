from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from core.models import NotificationRule
from clients.models import Client
from subscriptions.models import Subscription
from staff.models import Staff
from marketing.utils import send_notification_email


@shared_task
def check_notification_events():
    now = timezone.now()
    today = now.date()
    rules = NotificationRule.objects.filter(enabled=True).select_related('gym', 'template')

    for rule in rules:
        gym = rule.gym
        template = rule.template
        if not template:
            continue

        trigger = rule.trigger

        if trigger == 'birthday':
            clients = Client.objects.filter(
                gym=gym,
                birth_date__day=today.day,
                birth_date__month=today.month
            )
            for client in clients:
                send_if_allowed(rule, gym, template, "¡Feliz cumpleaños!", client=client)

        elif trigger == 'subscription_expiring':
            hours = rule.hours_before or 72
            days = hours // 24
            target_date = today + timedelta(days=days)
            clients = Client.objects.filter(
                gym=gym,
                subscription__end_date=target_date
            )
            for client in clients:
                send_if_allowed(rule, gym, template, "Tu suscripción está por vencer", client=client)

        elif trigger == 'subscription_expired':
            clients = Client.objects.filter(
                gym=gym,
                subscription__end_date=today
            )
            for client in clients:
                send_if_allowed(rule, gym, template, "Tu suscripción ha vencido", client=client)

        elif trigger == 'daily_report':
            staff_members = Staff.objects.filter(gym=gym)
            for staff in staff_members:
                send_if_allowed(rule, gym, template, "Reporte Diario del Gimnasio", staff=staff)


def send_if_allowed(rule, gym, template, subject, client=None, staff=None):
    if client and rule.send_to_client and client.email:
        send_notification_email(
            gym=gym,
            template=template,
            subject=subject,
            to_email=client.email
        )
    if staff and rule.send_to_staff and staff.email:
        send_notification_email(
            gym=gym,
            template=template,
            subject=subject,
            to_email=staff.email
        )
