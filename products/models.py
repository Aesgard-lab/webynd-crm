from django.db import models
from gyms.models import Gym, Franchise
from django.core.exceptions import ValidationError

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    iva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)  # Ej: 21%
    iva_included = models.BooleanField(default=True)

    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    is_shared_with_gyms = models.BooleanField(default=False)

    def clean(self):
        if self.gym and self.franchise:
            raise ValidationError("Un producto no puede pertenecer a un gimnasio y a una franquicia al mismo tiempo.")

    @property
    def final_price(self):
        if self.iva_included:
            return self.price
        return round(self.price * (1 + self.iva_percent / 100), 2)

    def __str__(self):
        return self.name
