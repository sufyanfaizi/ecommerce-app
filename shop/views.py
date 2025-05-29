from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Product
from shop.permissions import ProductPermission
from shop.serializers import ProductSerializer
from shop.product_filter import ProductFilter
from decimal import Decimal

class ProductAPIView(viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'sku']

    def get_queryset(self):
        return Product.get_all()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = Product.get_by_id(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = Product.create_product(serializer.validated_data)
            return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.get_by_id(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            updated = Product.update_product(product, serializer.validated_data)
            return Response(self.get_serializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def partial_update(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for partial update."}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.get_by_id(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            updated = Product.update_product(product, serializer.validated_data)
            return Response(self.get_serializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.get_by_id(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        Product.delete(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=False, methods=['post'], url_path='discount')
    def discount(self, request):
        sku = request.data.get('sku')
        product_id = request.data.get('product_id')
        discount_percent = request.data.get('discount_percent')

        if discount_percent is None:
            return Response({"error": "discount_percent is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            discount_percent = float(discount_percent)
            if discount_percent < 0 or discount_percent > 100:
                return Response({"error": "discount_percent must be between 0 and 100."},
                                status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "discount_percent must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        product = None
        if sku:
            product = Product.get_by_sku(sku=sku)
        elif product_id:
            product = Product.get_by_id(product_id=product_id)
        else:
            return Response({"error": "Either sku or product_id must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        Product.update_price(product , discount_percent)

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
