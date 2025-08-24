from django.contrib import admin
from .models import Plan, PlanActivity


class PlanActivityInline(admin.TabularInline):
    model = PlanActivity
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'plan_type',
        'category',
        'subcategory',
        'price',
        'is_active',
        'can_be_purchased_online',
    ]
    list_filter = ['plan_type', 'category', 'subcategory', 'is_active']
    search_fields = ['name', 'description']
    inlines = [PlanActivityInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'plan_type', 'category', 'subcategory', 'description', 'is_active')
        }),
        ('Precio y Facturación', {
            'fields': ('price', 'signup_fee', 'price_includes_tax', 'tax_percentage', 'billing_day', 'enable_prorate', 'auto_renew')
        }),
        ('Visibilidad y opciones de venta', {
            'fields': ('can_be_purchased_online', 'allow_multiple_subscriptions', 'html_embed_code')
        }),
    )
