from django.urls import path
from shop.shopify_webhook import ShopifyWebhookAPIView
from shop.views import ProductAPIView
from rest_framework.routers import DefaultRouter
from shop.views import ProductAPIView


router = DefaultRouter()
router.register(r'v1/products', ProductAPIView, basename='product')
urlpatterns = [

    path('v1/shopify/webhook', ShopifyWebhookAPIView.as_view(), name='shopify-webhook'),

 ]
urlpatterns += router.urls
