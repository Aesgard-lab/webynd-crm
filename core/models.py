from django.db import models
from gyms.models import Gym, Franchise
from auth_app.models import CustomUser  # Para SystemLog


class CurrencyConfig(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Ej: EUR, USD, CLP
    symbol = models.CharField(max_length=5)              # Ej: €, $, $
    name = models.CharField(max_length=50)               # Ej: Euro, Dólar

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class FranchiseSettings(models.Model):
    franchise = models.OneToOneField(Franchise, on_delete=models.CASCADE, related_name='settings')

    # FACTURACIÓN
    auto_send_invoice = models.BooleanField(default=True)
    invoice_email_optional_on_manual = models.BooleanField(default=True)
    monthly_statement_day = models.IntegerField(default=1)
    monthly_statement_emails = models.TextField(blank=True, help_text="Emails separados por coma")

    invoice_prefix = models.CharField(max_length=20, default="INV")
    next_invoice_number = models.PositiveIntegerField(default=1)
    tax_id = models.CharField(max_length=50, blank=True, null=True)

    # SMTP (correo saliente)
    smtp_host = models.CharField(max_length=100, blank=True, null=True)
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_user = models.CharField(max_length=100, blank=True, null=True)
    smtp_password = models.CharField(max_length=100, blank=True, null=True)

    # STRIPE
    stripe_public_key = models.CharField(max_length=100, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=100, blank=True, null=True)

    # IDENTIDAD VISUAL / CONTACTO
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#000000')  # Ej: "#FF5733"
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # MONEDA
    currency = models.ForeignKey(CurrencyConfig, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Configuración de franquicia {self.franchise.name}"


class GymSettings(models.Model):
    gym = models.OneToOneField(Gym, on_delete=models.CASCADE, related_name='settings')
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    # FACTURACIÓN
    auto_send_invoice = models.BooleanField(null=True, blank=True)
    invoice_email_optional_on_manual = models.BooleanField(null=True, blank=True)
    monthly_statement_day = models.IntegerField(null=True, blank=True)
    monthly_statement_emails = models.TextField(blank=True, null=True)

    invoice_prefix = models.CharField(max_length=20, blank=True, null=True)
    next_invoice_number = models.PositiveIntegerField(null=True, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)

    # SMTP
    smtp_host = models.CharField(max_length=100, blank=True, null=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    smtp_user = models.CharField(max_length=100, blank=True, null=True)
    smtp_password = models.CharField(max_length=100, blank=True, null=True)

    # STRIPE
    stripe_public_key = models.CharField(max_length=100, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=100, blank=True, null=True)

    # VISUAL / CONTACTO
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # MONEDA
    currency = models.ForeignKey(CurrencyConfig, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Configuración de gimnasio {self.gym.name}"

    def get_value(self, field_name):
        """
        Devuelve el valor del campo si está configurado en el gimnasio.
        Si está vacío o None, lo hereda desde la franquicia.
        """
        value = getattr(self, field_name)
        if value not in [None, '', 0]:
            return value
        if hasattr(self.franchise, 'settings'):
            return getattr(self.franchise.settings, field_name)
        return None


class SystemLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.module} - {self.action}"
    

class NotificationRule(models.Model):
    TRIGGER_CHOICES = [
        ('booking_created', 'Reserva creada'),
        ('booking_reminder', 'Recordatorio antes de clase'),
        ('booking_thanks', 'Post asistencia'),
        ('no_show', 'Ausencia del cliente'),
        ('subscription_expiring', 'Suscripción por vencer'),
        ('subscription_expired', 'Suscripción vencida'),
        ('new_client', 'Nuevo cliente'),
        ('birthday', 'Cumpleaños del cliente'),
        ('daily_report', 'Reporte diario al staff'),
    ]

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='notification_rules')
    trigger = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    enabled = models.BooleanField(default=True)
    hours_before = models.IntegerField(null=True, blank=True)  # Para recordatorios
    template = models.ForeignKey('marketing.MarketingTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    send_to_client = models.BooleanField(default=True)
    send_to_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gym', 'trigger')
        verbose_name = "Regla de Notificación"
        verbose_name_plural = "Reglas de Notificación"

    def __str__(self):
        return f"{self.gym.name} - {self.trigger}"

