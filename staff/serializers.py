from rest_framework import serializers
from .models import Staff, SalaryRule
from activities.models import Activity


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    

class SalaryRuleSerializer(serializers.ModelSerializer):
    staff_nombre = serializers.SerializerMethodField(read_only=True)
    actividad_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SalaryRule
        fields = '__all__'

    def get_staff_nombre(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}"

    def get_actividad_nombre(self, obj):
        return obj.actividad.name if obj.actividad else None
