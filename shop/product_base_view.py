# views/base/product_base_view.py
from rest_framework.views import APIView
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from shop.product_service import ProductService
from shop.product_filter import ProductFilter
from shop.permissions import ProductPermission


class ProductBaseAPIView(APIView):
    permission_classes = [ProductPermission]
    filterset_class = ProductFilter
    search_fields = ['name', 'sku']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
