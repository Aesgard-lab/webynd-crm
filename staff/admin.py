from django.contrib import admin
from .models import Staff
from django.utils.html import format_html
from .models import SalaryRule

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'dni', 'role',
        'gym', 'franchise', 'is_active_display',
        'photo_tag'
    )
    list_filter = ('gym', 'franchise', 'active')
    search_fields = ('first_name', 'last_name', 'email', 'dni')
    readonly_fields = ('photo_tag',)
    list_per_page = 25

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Nombre completo'

    def is_active_display(self, obj):
        return "✅" if obj.active else "❌"
    is_active_display.short_description = 'Activo'

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.photo.url)
        return "—"
    photo_tag.short_description = 'Foto'
    


@admin.register(SalaryRule)
class SalaryRuleAdmin(admin.ModelAdmin):
    list_display = (
        'staff', 'tipo_regla', 'actividad', 'modo_pago', 'valor',
        'por_cliente_asistido', 'min_clientes_asistidos',
        'min_porcentaje_aforo', 'hora_inicio', 'hora_fin', 'activo'
    )
    list_filter = ('tipo_regla', 'modo_pago', 'por_cliente_asistido', 'activo')
    search_fields = ('staff__first_name', 'staff__last_name', 'actividad__name')
    autocomplete_fields = ['staff', 'actividad']


