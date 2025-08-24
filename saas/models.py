# saas/models.py
from django.db import models


class PriceCycle(models.TextChoices):
    MONTHLY = "monthly", "Mensual"
    QUARTERLY = "quarterly", "Trimestral"
    ANNUAL = "annual", "Anual"


class Module(models.Model):
    code = models.SlugField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # ---- Stripe (opcional, se rellenará al sincronizar) ----
    stripe_product_id = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name


class ModulePrice(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="prices"
    )
    cycle = models.CharField(max_length=12, choices=PriceCycle.choices)
    amount = models.DecimalField(max_digits=9, decimal_places=2)  # sin prorrateo
    currency = models.CharField(max_length=3, default="EUR")
    is_active = models.BooleanField(default=True)

    # Opcional (útil para historificar precios luego)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)

    # ---- Stripe (opcional, se rellenará al sincronizar) ----
    stripe_price_id = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # mismo módulo + ciclo + inicio de vigencia no se repite
        unique_together = ("module", "cycle", "effective_from")
        ordering = ["module__code", "cycle"]

    def __str__(self):
        return f"{self.module.code} - {self.cycle} {self.amount} {self.currency}"
