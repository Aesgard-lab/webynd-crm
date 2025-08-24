from django.contrib import admin
from .models import ScheduledSession, Reservation


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    readonly_fields = ('client', 'created_at', 'cancelled', 'cancelled_late', 'checked_in', 'bonus_used', 'notes')
    can_delete = False


@admin.register(ScheduledSession)
class ScheduledSessionAdmin(admin.ModelAdmin):
    list_display = (
        'display_type', 'start_time', 'end_time',
        'gym', 'is_active', 'max_capacity', 'reservation_count'
    )
    list_filter = ('is_active', 'gym', 'activity', 'service', 'staff')
    search_fields = ('activity__name', 'service__name', 'notes')
    inlines = [ReservationInline]
    filter_horizontal = ('staff',)
    readonly_fields = ('created_at',)

    def display_type(self, obj):
        return obj.activity.name if obj.activity else obj.service.name
    display_type.short_description = 'Actividad / Servicio'

    def reservation_count(self, obj):
        return obj.reservations.count()
    reservation_count.short_description = 'Reservas'
