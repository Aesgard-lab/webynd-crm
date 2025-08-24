from django.db import models

# Create your models here.
from django.db import models
from gyms.models import Gym
from activities.models import Activity
from services.models import Service
from staff.models import Staff
from clients.models import Client
from bonuses.models import Bonus
from django.core.exceptions import ValidationError



class ScheduledSession(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='scheduled_sessions')

    # Solo uno de estos puede estar definido
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)

    staff = models.ManyToManyField(Staff, blank=True, related_name='scheduled_sessions')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    max_capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    is_recurrent = models.BooleanField(default=False)
    repeat_until = models.DateField(null=True, blank=True)
    repeat_days = models.CharField(
        max_length=20, blank=True,
        help_text="Días de la semana separados por coma: 0=Lun, 6=Dom. Ej: '0,2,4'"
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.activity and self.service:
            raise ValidationError("No puedes asignar una actividad y un servicio al mismo tiempo.")
        if not self.activity and not self.service:
            raise ValidationError("Debes asignar una actividad o un servicio.")

    def __str__(self):
        label = self.activity.name if self.activity else self.service.name
        return f"{label} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Reservation(models.Model):
    session = models.ForeignKey(ScheduledSession, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')

    created_at = models.DateTimeField(auto_now_add=True)

    cancelled = models.BooleanField(default=False)
    cancelled_late = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    bonus_used = models.ForeignKey(Bonus, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.client} → {self.session}"
