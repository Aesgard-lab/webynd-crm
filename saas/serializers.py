# saas/serializers.py
from rest_framework import serializers
from .models import Module, ModulePrice

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            "id", "code", "name", "description",
            "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ModulePriceSerializer(serializers.ModelSerializer):
    module_name = serializers.ReadOnlyField(source="module.name")
    module_code = serializers.ReadOnlyField(source="module.code")

    class Meta:
        model = ModulePrice
        fields = [
            "id", "module", "module_name", "module_code",
            "cycle", "amount", "currency", "is_active",
            "effective_from", "effective_to",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "module_name", "module_code"]

    def validate(self, data):
        """
        Pequeña validación: si vienen ambas fechas, que from <= to.
        """
        ef, et = data.get("effective_from"), data.get("effective_to")
        if ef and et and ef > et:
            raise serializers.ValidationError({"effective_to": "Debe ser posterior o igual a effective_from."})
        return data
