from django.contrib import admin
from .models import Franchise, Gym, GymMembership


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "owner", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "owner__email")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "owner", "franchise", "is_active", "created_at")
    list_filter = ("is_active", "country", "currency", "franchise")
    search_fields = ("name", "slug", "address", "franchise__name", "owner__email")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("franchise", "owner")
    ordering = ("id",)



@admin.register(GymMembership)
class GymMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "gym", "role", "is_active",
                    "can_manage_clients", "can_manage_cash", "can_manage_activities", "can_manage_bonuses",
                    "created_at")
    list_filter = ("role", "is_active", "gym")
    search_fields = ("user__email", "user__first_name", "user__last_name", "gym__name")
    autocomplete_fields = ("user", "gym")
    ordering = ("-created_at",)
