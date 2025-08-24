from django.db import models
from django.utils import timezone
from datetime import timedelta
from clients.models import Client
from gyms.models import Gym
from plans.models import Plan
from billing.utils import create_billing_entry


class Bonus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bonuses')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, limit_choices_to={'plan_type': 'bonus'})
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='bonuses')

    start_date = models.DateField()
    duration_days = models.PositiveIntegerField(default=120)
    expires_at = models.DateField(blank=True, null=True)

    assigned_quantity = models.PositiveIntegerField()
    used_quantity = models.PositiveIntegerField(default=0)

    auto_renew = models.BooleanField(default=False)
    signup_fee = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    billing_created = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.expires_at:
            self.expires_at = self.start_date + timedelta(days=self.duration_days)

        super().save(*args, **kwargs)

        if is_new and not self.billing_created and self.signup_fee > 0:
            concept = f"Bono: {self.plan.name}"
            create_billing_entry(
                gym=self.gym,
                client=self.client,
                item_type='bonus',
                reference_id=self.id,
                concept=concept,
                unit_price=self.signup_fee,
                quantity=1,
                tax_percentage=self.plan.tax_percentage,
            )
            self.billing_created = True
            super().save(update_fields=['billing_created'])

    def get_remaining(self):
        return self.assigned_quantity - self.used_quantity

    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now().date()

    def __str__(self):
        return f"Bono {self.plan.name} - {self.client}"


class BonusActivity(models.Model):
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE, related_name='activities')
    activity_name = models.CharField(max_length=100)
    usage_log = models.JSONField(default=list)

    def register_use(self):
        self.usage_log.append(timezone.now().isoformat())
        self.save()

    def get_usage_count(self):
        return len(self.usage_log)

    def get_remaining(self):
        return self.bonus.assigned_quantity - self.get_usage_count()

    def __str__(self):
        return f"{self.activity_name} ({self.bonus.client})"
