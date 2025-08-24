from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField, JSONField  # si usas PostgreSQL
from auth_app.models import CustomUser
from gyms.models import Gym


def calcular_letra_dni(numero):
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    try:
        return letras[int(numero) % 23]
    except (ValueError, IndexError):
        return ""


class Client(models.Model):
    ALERT_CHOICES = [
        ('none', 'Sin alerta'),
        ('vip', 'VIP'),
        ('low', 'Alerta leve'),
        ('medium', 'Alerta moderada'),
        ('high', 'Alerta grave'),
    ]

    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE,
        related_name='clients'
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Solo obligatorios
    first_name = models.CharField(max_length=100)
    email = models.EmailField()

    # Opcionales
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    dni_number = models.CharField(
        max_length=8, blank=True, null=True,
        help_text="Solo los números"
    )
    dni_letter = models.CharField(max_length=1, blank=True, null=True)

    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    alert_level = models.CharField(
        max_length=10, choices=ALERT_CHOICES,
        default='none'
    )

    # Notas y etiquetas
    notes = models.TextField(blank=True, null=True)
    notes_tags = ArrayField(
        models.CharField(max_length=50),
        default=list, blank=True
    )  # si quieres tags simples de texto

    # Si prefieres almacenar etiquetas más ricas (color, categoría, etc.):
    # notes_tags = JSONField(default=list, blank=True)

    photo = models.ImageField(
        upload_to='clients/photos/',
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.dni_number and not self.dni_letter:
            self.dni_letter = calcular_letra_dni(self.dni_number)
        super().save(*args, **kwargs)

    def full_dni(self):
        return f"{self.dni_number or ''}{self.dni_letter or ''}"

    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def __str__(self):
        return self.full_name() or self.email

    # ------- Relaciones virtuales -------
    @property
    def active_subscriptions(self):
        return self.subscriptions.filter(is_active=True)

    @property
    def past_subscriptions(self):
        return self.subscriptions.filter(is_active=False)

    @property
    def bonuses(self):
        return self.bonuses.all()

    @property
    def billing_entries(self):
        return self.billings.all()

    @property
    def reservations(self):
        return self.reservation_set.all()
