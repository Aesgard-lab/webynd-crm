from django.contrib import admin
from django.utils.html import format_html
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'gym', 'email', 'phone', 'full_dni',
        'alert_indicator', 'photo_thumbnail', 'created_at'
    ]
    list_filter = ['gym', 'alert_level']
    search_fields = ['first_name', 'last_name', 'email', 'dni_number']
    readonly_fields = ['created_at', 'dni_letter', 'photo_preview']

    fieldsets = (
        ('Identificación', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone',
                'photo', 'photo_preview'
            )
        }),
        ('DNI y dirección', {
            'fields': ('dni_number', 'dni_letter', 'address', 'zip_code')
        }),
        ('Gimnasio y usuario', {
            'fields': ('gym', 'user')
        }),
        ('Alertas y notas', {
            'fields': ('alert_level', 'notes', 'notes_tags')
        }),
        ('Trazabilidad', {
            'fields': ('created_at',)
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name or ''}"
    full_name.short_description = "Nombre completo"

    def full_dni(self, obj):
        return obj.full_dni()
    full_dni.short_description = "DNI"

    def alert_indicator(self, obj):
        colors = {
            'none': '',
            'vip': 'gold',
            'low': 'blue',
            'medium': 'orange',
            'high': 'red'
        }
        labels = {
            'none': '',
            'vip': 'VIP',
            'low': 'Leve',
            'medium': 'Moderada',
            'high': 'Grave'
        }
        color = colors.get(obj.alert_level, '')
        label = labels.get(obj.alert_level, '')
        if label:
            return format_html(
                '<span style="color: white; background-color: {}; padding: 2px 6px; border-radius: 4px;">{}</span>',
                color, label
            )
        return "-"
    alert_indicator.short_description = "Alerta"

    def photo_thumbnail(self, obj):
        """Miniatura en list_display."""
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.photo.url)
        return "-"
    photo_thumbnail.short_description = "Foto"

    def photo_preview(self, obj):
        """Vista previa grande en el formulario."""
        if obj.photo:
            return format_html('<img src="{}" style="max-height:200px;border-radius:6px;" />', obj.photo.url)
        return "Sin foto"
    photo_preview.short_description = "Vista previa"
