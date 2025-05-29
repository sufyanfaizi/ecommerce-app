from django.contrib import admin
from .models import Product
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField
from shop.utils import increase_price

@admin.action(description='Bulk increase price by 10%%')
def increase_price_action(modeladmin, request, queryset):
    increase_price(queryset , percentage=10)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity', 'last_updated')
    list_filter = ('sku', 'name', 'last_updated')
    actions = [increase_price_action]