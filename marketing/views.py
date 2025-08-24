from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MarketingTemplate, MarketingCampaign, CampaignRecipient
from .serializers import (
    MarketingTemplateSerializer,
    MarketingCampaignSerializer,
    CampaignRecipientSerializer
)
from .utils import execute_campaign


class MarketingTemplateViewSet(viewsets.ModelViewSet):
    queryset = MarketingTemplate.objects.all()
    serializer_class = MarketingTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all()
    serializer_class = MarketingCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='send-now')
    def send_now(self, request, pk=None):
        campaign = self.get_object()
        try:
            execute_campaign(campaign)
            return Response({"detail": "Campaña enviada."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignRecipientViewSet(viewsets.ModelViewSet):
    queryset = CampaignRecipient.objects.all()
    serializer_class = CampaignRecipientSerializer
    permission_classes = [permissions.IsAuthenticated]
