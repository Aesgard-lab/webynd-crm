from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError

from saas.models import Module, ModulePrice, PriceCycle


class GymStripeCustomer(models.Model):
    gym = models.OneToOneField(
        "gyms.Gym", on_delete=models.CASCADE, related_name="stripe_customer"
    )
    stripe_customer_id = models.CharField(
        max_length=120, unique=True, null=True, blank=True, db_index=True
    )
    billing_email = models.EmailField(blank=True)
    default_payment_method_id = models.CharField(max_length=120, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gym Stripe customer"
        verbose_name_plural = "Gym Stripe customers"

    def __str__(self):
        return f"{self.gym.name} ({self.stripe_customer_id or 'no-customer'})"


class StripeSubscriptionStatus(models.TextChoices):
    INCOMPLETE = "incomplete", "Incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired", "Incomplete expired"
    TRIALING = "trialing", "Trialing"
    ACTIVE = "active", "Active"
    PAST_DUE = "past_due", "Past due"
    CANCELED = "canceled", "Canceled"
    UNPAID = "unpaid", "Unpaid"
    PAUSED = "paused", "Paused"  # Stripe lo usa en algunos planes


class GymStripeSubscription(models.Model):
    gym = models.ForeignKey(
        "gyms.Gym", on_delete=models.CASCADE, related_name="stripe_subscriptions"
    )
    customer = models.ForeignKey(
        GymStripeCustomer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscriptions",
    )
    stripe_subscription_id = models.CharField(
        max_length=120, unique=True, null=True, blank=True, db_index=True
    )
    status = models.CharField(
        max_length=30, choices=StripeSubscriptionStatus.choices, default=StripeSubscriptionStatus.INCOMPLETE
    )
    cycle = models.CharField(max_length=20, choices=PriceCycle.choices)

    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # Como regla de negocio: solo 1 suscripción ACTIVE por gym
            models.UniqueConstraint(
                fields=["gym"],
                condition=Q(status=StripeSubscriptionStatus.ACTIVE),
                name="uniq_active_stripe_subscription_per_gym",
            )
        ]

    def __str__(self):
        return f"Sub {self.gym.name} [{self.status}]"

    @property
    def is_active(self) -> bool:
        return self.status == StripeSubscriptionStatus.ACTIVE


class GymStripeSubscriptionItem(models.Model):
    subscription = models.ForeignKey(
        GymStripeSubscription, on_delete=models.CASCADE, related_name="items"
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    module_price = models.ForeignKey(
        ModulePrice, on_delete=models.SET_NULL, null=True, blank=True
    )
    stripe_subscription_item_id = models.CharField(
        max_length=120, unique=True, null=True, blank=True, db_index=True
    )

    # snapshot de facturación (importe/moneda/qty) tomado del ModulePrice
    amount_snapshot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="EUR")
    quantity = models.PositiveIntegerField(default=1)

    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("subscription", "module")]
        verbose_name = "Subscription item"
        verbose_name_plural = "Subscription items"

    def __str__(self):
        return f"{self.module.code} x{self.quantity} @ {self.amount_snapshot or '?'} {self.currency}"

    def clean(self):
        if self.module_price:
            if self.module_price.module_id != self.module_id:
                raise ValidationError(
                    {"module_price": "El precio no corresponde al módulo seleccionado."}
                )
            if self.subscription and self.module_price.cycle != self.subscription.cycle:
                raise ValidationError(
                    {"module_price": "El ciclo del precio no coincide con el de la suscripción."}
                )

    def save(self, *args, **kwargs):
        # Autocompleta snapshot desde module_price si no está informado
        if self.module_price and self.amount_snapshot is None:
            self.amount_snapshot = self.module_price.amount
            self.currency = self.module_price.currency
        super().save(*args, **kwargs)
