from django.db import models
from gyms.models import Gym, Franchise
from staff.models import Staff  # Asegurate de tener esta app creada
from django.core.exceptions import ValidationError



class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)

    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    iva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    iva_included = models.BooleanField(default=True)

    available_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    max_capacity = models.PositiveIntegerField(default=1)

    staff = models.ManyToManyField(Staff, blank=True)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, null=True, blank=True, related_name='services')
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True, related_name='services')
    is_shared_with_gyms = models.BooleanField(default=False)

    def clean(self):
        if self.gym and self.franchise:
            raise ValidationError("Un servicio no puede pertenecer a un gimnasio y a una franquicia al mismo tiempo.")

    @property
    def final_price(self):
        if self.iva_included:
            return self.price
        return round(self.price * (1 + self.iva_percent / 100), 2)

    def __str__(self):
        return self.name
