# subscriptions/models.py

from django.db import models
from django.utils import timezone
from clients.models import Client
from datetime import datetime, timedelta
from decimal import Decimal
from activities.models import Activity

class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey('plans.Plan', on_delete=models.PROTECT, related_name='subscriptions')

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_modified = models.BooleanField(default=False)
    signup_fee_applied = models.BooleanField(default=True)
    was_prorated = models.BooleanField(default=False)

    auto_renew = models.BooleanField(default=False)
    next_billing_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.client.first_name})"

    def save(self, *args, **kwargs):
        self.is_active = self.end_date >= timezone.now().date()
        if not self.price_modified:
            self.price = self.calculate_final_price()
        if not self.was_prorated and self.plan.enable_prorate:
            self.price = self.apply_prorate()
            self.was_prorated = True
        if self.auto_renew:
            self.next_billing_date = self.calculate_next_billing_date()
        super().save(*args, **kwargs)

    def calculate_final_price(self):
        if self.plan.price_includes_tax:
            return self.plan.price
        tax_multiplier = Decimal(1 + self.plan.tax_percentage / 100)
        return round(self.plan.price * tax_multiplier, 2)

    def apply_prorate(self):
        today = timezone.now().date()
        if today > self.start_date:
            total_days = (self.end_date - self.start_date).days + 1
            remaining_days = (self.end_date - today).days + 1
            prorate_ratio = Decimal(remaining_days) / Decimal(total_days)
            return round(self.calculate_final_price() * prorate_ratio, 2)
        return self.calculate_final_price()

    def calculate_next_billing_date(self):
        base_date = self.end_date + timedelta(days=1)
        return base_date.replace(day=self.plan.billing_day)

    def copy_plan_activities(self):
        self.activities.all().delete()
        for pa in self.plan.activities.all():
            SubscriptionActivity.objects.create(
                subscription=self,
                activity_name=pa.activity.name,
                limit_type=pa.limit_type,
                limit_quantity=pa.limit_quantity
            )

    def is_active_now(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def is_expired(self):
        return timezone.now().date() > self.end_date

    def days_left(self):
        today = timezone.now().date()
        return max((self.end_date - today).days, 0)

    def cancel(self):
        self.end_date = timezone.now().date()
        self.is_active = False
        self.save()

    def renew(self):
        delta = self.end_date - self.start_date
        self.start_date = self.end_date + timedelta(days=1)
        self.end_date = self.start_date + delta
        self.was_prorated = False
        self.signup_fee_applied = False
        self.save()
        self.copy_plan_activities()

    def get_activities_summary(self):
        return [
            {
                "name": act.activity_name,
                "limit": act.limit_quantity,
                "used": act.get_usage_count(),
                "remaining": act.get_remaining(),
                "status": act.get_status_badge()
            }
            for act in self.activities.all()
        ]

    def generate_billing_entry(self):
        # Aquí irá integración con Billing app
        pass


class SubscriptionActivity(models.Model):
    LIMIT_TYPE_CHOICES = [
        ('per_day', 'Por día'),
        ('per_week', 'Por semana'),
        ('per_month', 'Por mes'),
        ('total', 'Total fijo'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='activities')
    activity_name = models.CharField(max_length=100)
    limit_type = models.CharField(max_length=20, choices=LIMIT_TYPE_CHOICES)
    limit_quantity = models.PositiveIntegerField()
    usage_log = models.JSONField(default=list)

    def __str__(self):
        return f"{self.activity_name} ({self.subscription.client.first_name})"

    def can_use(self):
        now = timezone.now()
        period_start = self._get_period_start(now)

        usos_validos = [
            ts for ts in self.usage_log
            if timezone.make_aware(datetime.fromisoformat(ts)) >= period_start
        ]

        usos_restantes = self.limit_quantity - len(usos_validos)

        if usos_restantes > 0:
            return True, f"Puedes usar la actividad. Te quedan {usos_restantes} en este período."
        else:
            return False, f"Has alcanzado el límite de {self.limit_quantity} usos."

    def register_use(self):
        can, msg = self.can_use()
        if not can:
            return False, msg
        now_iso = timezone.now().isoformat()
        self.usage_log.append(now_iso)
        self.save()
        return True, f"Uso registrado. {msg}"

    def _get_period_start(self, now):
        if self.limit_type == 'per_day':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.limit_type == 'per_week':
            return (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.limit_type == 'per_month':
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif self.limit_type == 'total':
            return timezone.make_aware(datetime.min)
        else:
            return now

    def get_usage_count(self):
        now = timezone.now()
        period_start = self._get_period_start(now)
        return len([
            ts for ts in self.usage_log
            if timezone.make_aware(datetime.fromisoformat(ts)) >= period_start
        ])

    def get_remaining(self):
        return max(self.limit_quantity - self.get_usage_count(), 0)

    def get_status_badge(self):
        remaining = self.get_remaining()
        if remaining == 0:
            return "danger"
        elif remaining <= 2:
            return "warning"
        return "ok"
