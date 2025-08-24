# activities/admin.py

from django.contrib import admin
from .models import ActivityCategory, ActivitySubcategory, Activity


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'is_active')
    list_filter = ('gym', 'is_active')
    search_fields = ('name',)


@admin.register(ActivitySubcategory)
class ActivitySubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'category', 'subcategory', 'duration_minutes', 'intensity', 'is_active')
    list_filter = ('gym', 'category', 'subcategory', 'intensity', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'gym', 'category', 'subcategory', 'image')
        }),
        ('Configuración', {
            'fields': ('duration_minutes', 'intensity', 'is_active')
        }),
        ('Reservas y cancelaciones', {
            'fields': ('min_reservation_notice', 'min_cancellation_notice', 'open_reservation_hour')
        }),
        ('Auditoría', {
            'fields': ('created_at',)
        }),
    )