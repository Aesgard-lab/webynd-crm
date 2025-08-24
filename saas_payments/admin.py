from django.contrib import admin
from .models import GymStripeCustomer, GymStripeSubscription, GymStripeSubscriptionItem


@admin.register(GymStripeCustomer)
class GymStripeCustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "gym", "stripe_customer_id", "billing_email", "created_at")
    search_fields = ("gym__name", "stripe_customer_id", "billing_email")
    list_filter = ()
    readonly_fields = ("created_at", "updated_at")


class SubscriptionItemInline(admin.TabularInline):
    model = GymStripeSubscriptionItem
    extra = 0
    fields = ("module", "module_price", "amount_snapshot", "currency", "quantity", "is_enabled")
    autocomplete_fields = ("module", "module_price")


@admin.register(GymStripeSubscription)
class GymStripeSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gym",
        "status",
        "cycle",
        "stripe_subscription_id",
        "current_period_start",
        "current_period_end",
        "created_at",
    )
    list_filter = ("status", "cycle")
    search_fields = ("gym__name", "stripe_subscription_id")
    inlines = [SubscriptionItemInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(GymStripeSubscriptionItem)
class GymStripeSubscriptionItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subscription",
        "module",
        "module_price",
        "amount_snapshot",
        "currency",
        "quantity",
        "is_enabled",
        "created_at",
    )
    search_fields = ("subscription__stripe_subscription_id", "module__code")
    list_filter = ("is_enabled",)
    readonly_fields = ("created_at", "updated_at")
