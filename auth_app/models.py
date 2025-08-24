from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Elimina por completo el campo username de AbstractUser
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Role(models.TextChoices):
        SUPERADMIN = "superadmin", "Superadmin"
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        CLIENT = "client", "Client"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        blank=True,
        null=True,
        help_text="Si está vacío, se infiere: superadmin > staff > client",
    )

    photo = models.ImageField(upload_to="avatars/", null=True, blank=True)

    # Sede activa actual del usuario (para multi-gimnasio)
    current_gym = models.ForeignKey(
        "gyms.Gym",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="current_users",
        help_text="Última sede activa del usuario."
    )

    @property
    def effective_role(self) -> str:
        if self.role:
            return self.role
        if self.is_superuser:
            return self.Role.SUPERADMIN
        if self.is_staff:
            return self.Role.STAFF
        return self.Role.CLIENT

    def __str__(self) -> str:
        return self.email or super().__str__()


