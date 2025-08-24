from rest_framework import serializers
from .models import BillingEntry, Expense


class BillingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingEntry
        fields = [
            'id',
            'invoice_number',
            'item_type',
            'concept',
            'unit_price',
            'quantity',
            'tax_percentage',
            'total_iva',
            'total_price',
            'status',
            'created_at',
            'reference_id',
            'gym',
            'client',
        ]
        read_only_fields = [
            'invoice_number',
            'total_iva',
            'total_price',
            'created_at',
        ]

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        if data['unit_price'] < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return data


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id',
            'concept',
            'amount',
            'date',
            'method',
            'notes',
            'gym',
            'created_by',
        ]
        read_only_fields = [
            'created_by',
        ]

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del gasto no puede ser negativo.")
        return value

    def validate_concept(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Debes indicar un concepto para el gasto.")
        return value
