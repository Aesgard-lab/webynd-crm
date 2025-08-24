from django.db import models
from auth_app.models import CustomUser
from gyms.models import Gym, Franchise
from activities.models import Activity


class Staff(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Datos personales
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="staff/", null=True, blank=True)

    # Relación organizacional
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name="staff",   # 👈 ahora la inversa es gym.staff.all()
    )
    franchise = models.ForeignKey(
        Franchise, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Rol y permisos
    role = models.CharField(max_length=100, blank=True)
    can_sell = models.BooleanField(default=False)
    can_create_subs = models.BooleanField(default=False)
    can_manage_clients = models.BooleanField(default=False)
    can_see_finance = models.BooleanField(default=False)
    can_book_classes = models.BooleanField(default=False)

    # Horarios
    uses_gym_schedule = models.BooleanField(default=True)
    schedule_start = models.TimeField(null=True, blank=True)
    schedule_end = models.TimeField(null=True, blank=True)

    # Estado
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"


class CheckIn(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="checkins")
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        out_label = self.check_out_time or "..."
        return f"{self.staff} - Entrada: {self.check_in_time} / Salida: {out_label}"


class SalaryRule(models.Model):
    REGRA_CHOICES = [
        ("fixed_monthly", "Salario fijo mensual"),
        ("per_class", "Pago por clase dictada"),
        ("per_service", "Pago por servicio 1:1"),
        ("per_sale", "Comisión por venta"),
    ]

    MODO_PAGO_CHOICES = [
        ("fixed", "Cantidad fija"),
        ("percent", "Porcentaje"),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="salary_rules")
    tipo_regla = models.CharField(max_length=20, choices=REGRA_CHOICES)

    actividad = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)

    hora_inicio = models.TimeField(null=True, blank=True, help_text="Filtrado opcional por franja horaria")
    hora_fin = models.TimeField(null=True, blank=True)

    modo_pago = models.CharField(max_length=10, choices=MODO_PAGO_CHOICES)
    valor = models.DecimalField(max_digits=7, decimal_places=2, help_text="Monto en euros o porcentaje")

    por_cliente_asistido = models.BooleanField(
        default=False,
        help_text="Aplicar el pago por cada cliente que asistió",
    )

    min_clientes_asistidos = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Mínimo de clientes que deben asistir para que se active la regla",
    )

    min_porcentaje_aforo = models.FloatField(
        null=True, blank=True,
        help_text="Porcentaje mínimo de aforo ocupado requerido (entre 0.0 y 1.0)",
    )

    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Regla Salarial"
        verbose_name_plural = "Reglas Salariales"

    def __str__(self) -> str:
        tipo = self.get_tipo_regla_display()
        monto = f"{self.valor}{'%' if self.modo_pago == 'percent' else '€'}"
        return f"{self.staff} - {tipo} ({monto})"
