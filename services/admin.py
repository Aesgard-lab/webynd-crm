from django.contrib import admin
from .models import Service, ServiceCategory

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'duration_minutes', 'price', 'iva_percent',
        'iva_included', 'final_price_display', 'max_capacity',
        'available_online', 'is_active', 'gym', 'franchise'
    )
    list_filter = ('is_active', 'available_online', 'gym', 'franchise', 'category')
    search_fields = ('name', 'description')
    filter_horizontal = ('staff',)
    readonly_fields = ('final_price_display',)

    def final_price_display(self, obj):
        return f"{obj.final_price:.2f} €"
    final_price_display.short_description = "Precio Final (con IVA)"
