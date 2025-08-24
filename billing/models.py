from django.db import models
from clients.models import Client
from gyms.models import Gym
from auth_app.models import CustomUser

class BillingEntry(models.Model):
    ITEM_TYPE_CHOICES = [
        ('bonus', 'Bono'),
        ('subscription', 'Suscripción'),
        ('product', 'Producto'),
        ('service', 'Servicio'),
    ]

    STATUS_CHOICES = [
        ('paid', 'Pagado'),
        ('pending', 'Pendiente'),
        ('cancelled', 'Cancelado'),
    ]

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='billings')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='billings')

    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    concept = models.CharField(max_length=255)  # Ej: "Bono Reformer 10 sesiones"
    reference_id = models.PositiveIntegerField()  # ID del bono/suscripción/etc.

    invoice_number = models.CharField(max_length=50, unique=True)  # Ej: INV-00001

    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    tax_percentage = models.IntegerField(default=21)
    total_iva = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.client} - {self.total_price}€"

  # <- Esta es tu clase de usuario

class Expense(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    concept = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.concept} ({self.amount})"
