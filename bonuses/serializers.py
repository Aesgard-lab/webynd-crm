from rest_framework import serializers
from .models import Bonus, BonusActivity


class BonusActivitySerializer(serializers.ModelSerializer):
    used = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = BonusActivity
        fields = ['id', 'activity_name', 'usage_log', 'used', 'remaining']

    def get_used(self, obj):
        return obj.get_usage_count()

    def get_remaining(self, obj):
        return obj.get_remaining()


class BonusSerializer(serializers.ModelSerializer):
    activities = BonusActivitySerializer(many=True, read_only=True)
    is_expired = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Bonus
        fields = [
            'id', 'plan', 'start_date', 'expires_at', 'assigned_quantity',
            'used_quantity', 'remaining', 'auto_renew', 'is_expired', 'activities'
        ]

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_remaining(self, obj):
        return obj.get_remaining()
