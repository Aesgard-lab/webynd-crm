from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import Client
from core.models import NotificationRule
from marketing.utils import send_notification_email


@receiver(post_save, sender=Client)
def handle_new_client(sender, instance, created, **kwargs):
    if not created:
        return

    gym = instance.gym
    rules = NotificationRule.objects.filter(
        gym=gym,
        trigger='new_client',
        enabled=True,
        send_to_staff=True
    ).select_related('template')

    staff_list = gym.staff_set.filter(email__isnull=False)

    for rule in rules:
        for staff in staff_list:
            send_notification_email(
                gym=gym,
                template=rule.template,
                subject="Nuevo cliente registrado",
                to_email=staff.email
            )
