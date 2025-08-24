from rest_framework import serializers
from clients.models import Client
from subscriptions.models import Subscription
from bonuses.models import Bonus
from billing.models import BillingEntry
# from scheduler.models import Reservation  # si usas scheduler


# ---------- CLIENTES ----------
class ClientSerializer(serializers.ModelSerializer):
    full_dni = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name', 'last_name', 'email', 'phone',
            'dni_number', 'dni_letter', 'full_dni',
            'address', 'zip_code', 'alert_level',
            'notes', 'notes_tags', 'photo',
            'gym', 'user', 'created_at',
        ]
        read_only_fields = ['dni_letter', 'created_at']
        # Solo first_name y email son obligatorios. Todo lo demás opcional.
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},

            'last_name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
            'dni_number': {'required': False, 'allow_blank': True, 'allow_null': True},
            'address': {'required': False, 'allow_blank': True, 'allow_null': True},
            'zip_code': {'required': False, 'allow_blank': True, 'allow_null': True},
            'alert_level': {'required': False, 'allow_null': True},
            'notes': {'required': False, 'allow_blank': True, 'allow_null': True},
            'notes_tags': {'required': False, 'allow_null': True},
            'photo': {'required': False, 'allow_null': True},
            'gym': {'required': False, 'allow_null': True},   # se asigna en perform_create
            'user': {'required': False, 'allow_null': True},  # si lo asignas automáticamente
        }

    def get_full_dni(self, obj):
        return obj.full_dni()

    # Normalización de valores opcionales
    def to_internal_value(self, data):
        val = super().to_internal_value(data)
        # Convierte "" en None para campos opcionales
        for k in [
            'last_name', 'phone', 'dni_number', 'address', 'zip_code',
            'notes', 'photo'
        ]:
            if val.get(k) == "":
                val[k] = None
        # Normaliza notes_tags a lista vacía si viene nulo
        if 'notes_tags' in val and val['notes_tags'] is None:
            val['notes_tags'] = []
        return val

    def validate_phone(self, v):
        if v and not __import__("re").match(r"^\+?\d{6,15}$", v):
            raise serializers.ValidationError("Teléfono inválido")
        return v


# ---------- SUBSCRIPCIONES / BONOS / FACTURAS ----------
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active']


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ['id', 'plan', 'start_date', 'expires_at',
                  'assigned_quantity', 'used_quantity']


class BillingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingEntry
        fields = ['id', 'invoice_number', 'concept', 'total_price',
                  'status', 'created_at']


# Placeholder (activá solo si usás reservas)
# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = ['id', 'activity_name', 'date', 'status']


class ClientDetailSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, source='subscriptions.all', read_only=True)
    bonuses = BonusSerializer(many=True, source='bonuses.all', read_only=True)
    billings = BillingEntrySerializer(many=True, source='billings.all', read_only=True)
    # reservations = ReservationSerializer(many=True, source='reservation_set.all', read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'full_dni',
            'alert_level', 'notes', 'notes_tags', 'photo', 'created_at',
            'subscriptions', 'bonuses', 'billings',
            # 'reservations',
        ]
