from rest_framework import viewsets
from .models import Product, ProductCategory, ProductSubCategory
from .serializers import ProductSerializer, ProductCategorySerializer, ProductSubCategorySerializer
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

class ProductSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductSubCategory.objects.all()
    serializer_class = ProductSubCategorySerializer
    permission_classes = [IsAuthenticated]
