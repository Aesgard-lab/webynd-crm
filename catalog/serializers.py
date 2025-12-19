from rest_framework import serializers
from .models import CatalogCategory, CatalogSubcategory


class CatalogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCategory
        fields = "__all__"


class CatalogSubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    module = serializers.CharField(source="category.module", read_only=True)

    class Meta:
        model = CatalogSubcategory
        fields = "__all__"
