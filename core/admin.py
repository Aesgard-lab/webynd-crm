from django.contrib import admin
from .models import FranchiseSettings, GymSettings, CurrencyConfig, SystemLog


@admin.register(FranchiseSettings)
class FranchiseSettingsAdmin(admin.ModelAdmin):
    list_display = ['franchise', 'auto_send_invoice', 'monthly_statement_day']
    search_fields = ['franchise__name']
    list_filter = ['auto_send_invoice']


@admin.register(GymSettings)
class GymSettingsAdmin(admin.ModelAdmin):
    list_display = ['gym', 'franchise', 'auto_send_invoice']
    search_fields = ['gym__name']
    list_filter = ['auto_send_invoice', 'franchise']


@admin.register(CurrencyConfig)
class CurrencyConfigAdmin(admin.ModelAdmin):
    list_display = ['code', 'symbol', 'name']


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'module', 'action']
    search_fields = ['user__email', 'module', 'action']
    list_filter = ['module']
