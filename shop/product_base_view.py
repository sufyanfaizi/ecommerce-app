# views/base/product_base_view.py
from rest_framework import permissions, filters, viewsets
from shop.product_filter import ProductFilter
from shop.permissions import ProductPermission
from shop.serializers import ProductSerializer



class ProductBaseAPIView(viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    filterset_class = ProductFilter
    search_fields = ['name', 'sku']


