from django.contrib import admin
from .models import CatalogCategory, CatalogSubcategory


@admin.register(CatalogCategory)
class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "module", "scope", "name", "gym", "franchise", "is_active", "created_at")
    list_filter = ("module", "scope", "is_active")
    search_fields = ("name", "gym__name", "franchise__name")
    ordering = ("module", "name")


@admin.register(CatalogSubcategory)
class CatalogSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "name", "is_active", "created_at")
    list_filter = ("is_active", "category__module")
    search_fields = ("name", "category__name")
    ordering = ("category", "name")
