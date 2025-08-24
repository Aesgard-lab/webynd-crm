# activities/models.py

from django.db import models
from gyms.models import Gym


class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='activity_categories', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ActivitySubcategory(models.Model):
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Activity(models.Model):
    INTENSITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('extreme', 'Extrema'),
    ]

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    category = models.ForeignKey(ActivityCategory, on_delete=models.PROTECT, related_name='activities', null=True, blank=True)
    subcategory = models.ForeignKey(ActivitySubcategory, on_delete=models.PROTECT, related_name='activities', null=True, blank=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)

    capacity = models.PositiveIntegerField(default=20, help_text="Capacidad máxima de personas por clase")

    is_active = models.BooleanField(default=True)

    min_reservation_notice = models.DurationField(
        help_text="Antelación mínima para reservar (ej: 1 day, 2:00:00 para 2 horas)"
    )
    min_cancellation_notice = models.DurationField(
        help_text="Antelación mínima para cancelar sin penalización"
    )
    open_reservation_hour = models.TimeField(
        blank=True, null=True,
        help_text="Hora diaria fija a partir de la cual se puede reservar (opcional)"
    )

    image = models.ImageField(upload_to='activities/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
