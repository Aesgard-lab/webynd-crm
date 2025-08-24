from django.contrib import admin
from .models import Bonus, BonusActivity


class BonusActivityInline(admin.TabularInline):
    model = BonusActivity
    extra = 0
    readonly_fields = ['usage_log']
    can_delete = False


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ['client', 'plan', 'gym', 'start_date', 'expires_at', 'assigned_quantity', 'get_used', 'get_remaining', 'auto_renew']
    list_filter = ['plan', 'auto_renew', 'gym']
    search_fields = ['client__first_name', 'client__last_name', 'plan__name', 'gym__name']
    inlines = [BonusActivityInline]
    readonly_fields = ['billing_created', 'created_at']

    def get_used(self, obj):
        return obj.used_quantity
    get_used.short_description = "Usado"

    def get_remaining(self, obj):
        return obj.get_remaining()
    get_remaining.short_description = "Restante"
