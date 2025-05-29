# filters/product_filter.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['price', 'sku', 'name', 'quantity']
