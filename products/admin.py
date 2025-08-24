from django.contrib import admin
from .models import Product, ProductCategory, ProductSubCategory
from django.utils.html import format_html

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'subcategory', 'price', 'iva_percent',
        'iva_included', 'final_price_display', 'stock', 'is_active',
        'gym', 'franchise', 'image_tag'
    ]
    list_filter = ['is_active', 'gym', 'franchise', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['final_price_display', 'image_tag']

    def final_price_display(self, obj):
        return f"{obj.final_price:.2f} €"
    final_price_display.short_description = 'Precio Final (con IVA)'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Imagen'
