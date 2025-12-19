from django.db import models

from gyms.models import Gym, Franchise


class CatalogCategory(models.Model):
    MODULE_CHOICES = [
        ("bonus", "Bonos"),
        ("subscription", "Suscripciones"),
        ("service", "Servicios"),
        ("product", "Productos"),
        ("activity", "Actividades"),
    ]

    SCOPE_CHOICES = [
        ("gym", "Gym"),
        ("franchise", "Franchise"),
    ]

    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default="gym")

    gym = models.ForeignKey(Gym, null=True, blank=True, on_delete=models.CASCADE, related_name="catalog_categories")
    franchise = models.ForeignKey(
        Franchise, null=True, blank=True, on_delete=models.CASCADE, related_name="catalog_categories"
    )

    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["module", "scope"]),
            models.Index(fields=["gym"]),
            models.Index(fields=["franchise"]),
        ]

        # Evita duplicados en el mismo “nivel” tenant
        constraints = [
            models.UniqueConstraint(
                fields=["module", "scope", "gym", "franchise", "name"],
                name="uniq_catalog_category_module_scope_tenant_name",
            )
        ]

    def clean(self):
        # coherencia scope
        if self.scope == "gym" and not self.gym_id:
            raise ValueError("scope='gym' requiere gym.")
        if self.scope == "franchise" and not self.franchise_id:
            raise ValueError("scope='franchise' requiere franchise.")
        if self.scope == "gym" and self.franchise_id:
            raise ValueError("scope='gym' no debe tener franchise.")
        if self.scope == "franchise" and self.gym_id:
            raise ValueError("scope='franchise' no debe tener gym.")

    def __str__(self):
        return f"[{self.module}] {self.name}"


class CatalogSubcategory(models.Model):
    category = models.ForeignKey(CatalogCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="uniq_catalog_subcategory_category_name")
        ]

    def __str__(self):
        return f"{self.category.name} · {self.name}"
