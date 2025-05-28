from django.urls import path
from shop.shopify_webhook import ShopifyWebhookAPIView
from shop.views import ProductAPIView

urlpatterns = [
    path('v1/products', ProductAPIView.as_view()),
    path('v1/products/<int:pk>', ProductAPIView.as_view()),
    path('v1/shopify/webhook', ShopifyWebhookAPIView.as_view(), name='shopify-webhook'),

]