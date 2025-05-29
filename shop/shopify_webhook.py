from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Product

class ShopifyWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        sku = data.get('sku')
        quantity = data.get('quantity')

        try:
            Product.update_quantity(sku , quantity)
            return Response({'status': 'updated'}, status=200)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
