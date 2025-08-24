# activities/serializers.py

from rest_framework import serializers
from .models import Activity, ActivityCategory, ActivitySubcategory


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'


class ActivitySubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySubcategory
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    category = ActivityCategorySerializer(read_only=True)
    subcategory = ActivitySubcategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=ActivityCategory.objects.all(), write_only=True, source='category')
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=ActivitySubcategory.objects.all(), write_only=True, source='subcategory')

    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'gym', 'category', 'subcategory',
            'category_id', 'subcategory_id',
            'duration_minutes', 'intensity', 'is_active',
            'min_reservation_notice', 'min_cancellation_notice',
            'open_reservation_hour', 'image', 'created_at'
        ]
        read_only_fields = ('created_at',)
