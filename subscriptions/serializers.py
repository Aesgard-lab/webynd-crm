# subscriptions/serializers.py

from rest_framework import serializers
from .models import Subscription, SubscriptionActivity
from django.utils import timezone

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        client = data.get('client')

        if start and end and start >= end:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la de fin.")

        if self.instance is None:  # Solo en creación
            hoy = timezone.now().date()
            if Subscription.objects.filter(client=client, is_active=True, end_date__gte=hoy).exists():
                raise serializers.ValidationError("El cliente ya tiene una suscripción activa.")

        return data


class SubscriptionActivityUseSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        try:
            self.instance = SubscriptionActivity.objects.get(id=value)
        except SubscriptionActivity.DoesNotExist:
            raise serializers.ValidationError("Actividad no encontrada.")
        return value

    def save(self, **kwargs):
        success, message = self.instance.register_use()
        if not success:
            raise serializers.ValidationError(message)
        return {
            "message": message,
            "status": self.instance.get_status_badge(),
            "remaining": self.instance.get_remaining(),
            "used": self.instance.get_usage_count(),
            "activity": self.instance.activity_name
        }
