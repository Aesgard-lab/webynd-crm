from django.contrib import admin
from .models import Expense, BillingEntry


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'concept', 'amount', 'gym', 'method', 'created_by')
    list_filter = ('gym', 'method', 'date')
    search_fields = ('concept', 'notes', 'created_by__email')
    autocomplete_fields = ['gym', 'created_by']
    date_hierarchy = 'date'
    ordering = ('-date',)


@admin.register(BillingEntry)
class BillingEntryAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'item_type', 'concept', 'unit_price', 'quantity',
        'total_price', 'status', 'created_at', 'gym', 'client'
    )
    list_filter = ('gym', 'item_type', 'status', 'created_at')
    search_fields = ('invoice_number', 'concept', 'client__email')
    autocomplete_fields = ['gym', 'client']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
