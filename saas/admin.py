from django.contrib import admin
from .models import Module, ModulePrice

class ModulePriceInline(admin.TabularInline):
    model = ModulePrice
    extra = 0
    fields = ("cycle", "amount", "currency", "is_active", "effective_from", "effective_to")
    show_change_link = True

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("code", "name", "description")
    prepopulated_fields = {"code": ("name",)}  # autocompleta el slug 'code' a partir de 'name'
    inlines = [ModulePriceInline]
    readonly_fields = ("created_at", "updated_at")
    ordering = ("code",)

@admin.register(ModulePrice)
class ModulePriceAdmin(admin.ModelAdmin):
    list_display = (
        "id", "module", "cycle", "amount", "currency",
        "is_active", "effective_from", "effective_to", "created_at"
    )
    list_filter = ("cycle", "currency", "is_active")
    search_fields = ("module__name", "module__code")
    raw_id_fields = ("module",)  # selector rápido si hay muchos módulos
    readonly_fields = ("created_at", "updated_at")
    ordering = ("module__code", "cycle")
