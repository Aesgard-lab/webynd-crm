from django.db import models
from activities.models import Activity


class Plan(models.Model):
    CATEGORY_CHOICES = [
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('bono', 'Bono'),
    ]

    SUBCATEGORY_CHOICES = [
        ('reformer', 'Reformer'),
        ('fitness', 'Fitness'),
        ('pilates', 'Pilates'),
    ]

    PLAN_TYPE_CHOICES = [
        ('subscription', 'Suscripción'),
        ('bonus', 'Bono'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, default='subscription')

    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    billing_day = models.IntegerField(default=1)
    can_be_purchased_online = models.BooleanField(default=False)
    enable_prorate = models.BooleanField(default=False)
    auto_renew = models.BooleanField(default=False)

    signup_fee = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_includes_tax = models.BooleanField(default=True)
    tax_percentage = models.IntegerField(default=21)

    allow_multiple_subscriptions = models.BooleanField(default=False)
    html_embed_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.plan_type})"


class PlanActivity(models.Model):
    LIMIT_TYPE_CHOICES = [
        ('per_day', 'Por día'),
        ('per_week', 'Por semana'),
        ('per_month', 'Por mes'),
        ('total', 'Total fijo'),
    ]

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='activities')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='plan_links')
    limit_type = models.CharField(max_length=20, choices=LIMIT_TYPE_CHOICES)
    limit_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.activity.name} - {self.limit_quantity} ({self.limit_type})"