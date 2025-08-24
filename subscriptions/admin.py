from django.contrib import admin
from .models import Subscription, SubscriptionActivity

class SubscriptionActivityInline(admin.TabularInline):
    model = SubscriptionActivity
    extra = 0
    readonly_fields = ['usage_log']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'start_date', 'end_date', 'is_active']
    inlines = [SubscriptionActivityInline]
    search_fields = ['name', 'client__first_name', 'client__last_name']
