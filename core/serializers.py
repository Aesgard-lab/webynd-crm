from rest_framework import serializers
from .models import GymSettings, FranchiseSettings, CurrencyConfig
from .models import NotificationRule


class GymSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymSettings
        exclude = ['id']


class FranchiseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchiseSettings
        exclude = ['id']


class CurrencyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConfig
        fields = '__all__'
        

class NotificationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRule
        fields = '__all__'

