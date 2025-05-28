from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from shop.models import Product

class ShopifyWebhookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/shopify/webhook'  # update this if your path is different

        # Create a product to test with
        self.product = Product.objects.create(
            name='Sample Product',
            sku='SAMPLE001',
            price=15.99,
            quantity=10
        )

    def test_webhook_updates_quantity(self):
        data = {
            'sku': 'SAMPLE001',
            'quantity': 25
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'updated')

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 25)

    def test_webhook_product_not_found(self):
        data = {
            'sku': 'INVALIDSKU',
            'quantity': 30
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Product matches the given query.')
