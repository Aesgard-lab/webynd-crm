from django.utils.text import slugify
from rest_framework import serializers
from .models import Franchise, Gym

class FranchiseSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")
    gyms_count = serializers.IntegerField(source="gyms.count", read_only=True)

    class Meta:
        model = Franchise
        fields = [
            "id", "name", "slug", "owner", "owner_email",
            "logo", "primary_color", "secondary_color",
            "is_active", "created_at", "updated_at",
            "gyms_count",
        ]
        read_only_fields = ["created_at", "updated_at", "owner_email", "gyms_count"]

    def validate_slug(self, value):
        return value or slugify(self.initial_data.get("name", ""))

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.get("slug") and "name" in validated_data:
            validated_data["slug"] = slugify(validated_data["name"])
        return super().update(instance, validated_data)


class GymSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")
    franchise_name = serializers.ReadOnlyField(source="franchise.name")

    class Meta:
        model = Gym
        fields = [
            "id", "name", "slug", "owner", "owner_email",
            "franchise", "franchise_name",
            "address", "timezone", "locale", "country", "currency",
            "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "owner_email", "franchise_name"]

    def validate_slug(self, value):
        return value or slugify(self.initial_data.get("name", ""))

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.get("slug") and "name" in validated_data:
            validated_data["slug"] = slugify(validated_data["name"])
        return super().update(instance, validated_data)
