# gyms/models.py
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Usa un color HEX válido, p. ej. #111827 o #06B6D4."
)

class Franchise(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,           # evita borrar la franquicia si borran al dueño por error
        related_name='franchises'
    )
    logo = models.ImageField(upload_to='franchises/logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, validators=[hex_color_validator], default="#111827")
    secondary_color = models.CharField(max_length=7, validators=[hex_color_validator], default="#06B6D4")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Gym(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='gyms'
    )
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='gyms'
    )

    address = models.CharField(max_length=255, blank=True)

    # Preferencias por sede (útiles para white-label y facturación)
    timezone = models.CharField(max_length=64, default="Europe/Madrid")
    locale = models.CharField(max_length=10, default="es-ES")
    country = models.CharField(max_length=2, default="ES")
    currency = models.CharField(max_length=3, default="EUR")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["franchise"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name
    

# ... (Franchise y Gym ya existen)

class GymMembership(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gym_memberships",
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Permisos por checkbox (ampliables)
    can_manage_clients = models.BooleanField(default=False)
    can_manage_cash = models.BooleanField(default=False)
    can_manage_activities = models.BooleanField(default=False)
    can_manage_bonuses = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "gym")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["gym"]),
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.user} @ {self.gym} ({self.role})"

