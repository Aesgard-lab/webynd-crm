from rest_framework import serializers
from .models import MarketingTemplate, MarketingCampaign, CampaignRecipient


class MarketingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingTemplate
        fields = '__all__'


class MarketingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingCampaign
        fields = '__all__'


class CampaignRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignRecipient
        fields = '__all__'
