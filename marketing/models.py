from django.db import models
from django.conf import settings

from gyms.models import Gym, Franchise
from clients.models import Client
from staff.models import Staff
from auth_app.models import CustomUser


class MarketingTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('popup', 'Popup'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TEMPLATE_TYPES)
    html_content = models.TextField()
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class MarketingCampaign(models.Model):
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('popup', 'Popup'),
    ]
    SENDER_LEVEL = [
        ('superadmin', 'Superadmin'),
        ('franchise', 'Franchise'),
        ('gym', 'Gym'),
    ]
    RECIPIENT_TYPES = [
        ('clients', 'Clientes'),
        ('staff', 'Staff'),
        ('both', 'Ambos'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TEMPLATE_TYPES)
    sender_level = models.CharField(max_length=20, choices=SENDER_LEVEL)
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPES, default='clients')
    template = models.ForeignKey(MarketingTemplate, on_delete=models.CASCADE)

    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True, blank=True)
    target_gyms = models.ManyToManyField(Gym, related_name='targeted_campaigns', blank=True)

    subject = models.CharField(max_length=255, blank=True, null=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class CampaignRecipient(models.Model):
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='recipients')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')  # pending, sent, failed

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(client__isnull=False) |
                    models.Q(staff__isnull=False)
                ),
                name='at_least_one_recipient'
            )
        ]
