from rest_framework import viewsets, permissions
from .models import GymSettings, FranchiseSettings, CurrencyConfig
from .serializers import GymSettingsSerializer, FranchiseSettingsSerializer, CurrencyConfigSerializer
from .models import NotificationRule
from .serializers import NotificationRuleSerializer

class GymSettingsViewSet(viewsets.ModelViewSet):
    queryset = GymSettings.objects.all()
    serializer_class = GymSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]


class FranchiseSettingsViewSet(viewsets.ModelViewSet):
    queryset = FranchiseSettings.objects.all()
    serializer_class = FranchiseSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrencyConfigViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConfig.objects.all()
    serializer_class = CurrencyConfigSerializer
    permission_classes = [permissions.IsAuthenticated]



class NotificationRuleViewSet(viewsets.ModelViewSet):
    queryset = NotificationRule.objects.all()
    serializer_class = NotificationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]
