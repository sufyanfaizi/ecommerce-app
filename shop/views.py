# views/product_views.py
from rest_framework.response import Response
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from shop.serializers import ProductSerializer
from shop.product_base_view import ProductBaseAPIView
from django.db import transaction


class ProductAPIView(ProductBaseAPIView):
    def get(self, request, pk=None):
        if pk:
            product = self.product_service.get_by_id(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            queryset = self.product_service.get_all()
            filter_backend = DjangoFilterBackend()
            queryset = filter_backend.filter_queryset(request, queryset, self)
            search_filter = filters.SearchFilter()
            queryset = search_filter.filter_queryset(request, queryset, self)
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = self.product_service.create(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)

        product = self.product_service.get_by_id(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            updated = self.product_service.update(product, serializer.validated_data)
            return Response(ProductSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def patch(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for partial update."}, status=status.HTTP_400_BAD_REQUEST)

        product = self.product_service.get_by_id(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            updated = self.product_service.update(product, serializer.validated_data)
            return Response(ProductSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Product ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        product = self.product_service.get_by_id(pk)
        self.product_service.delete(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


