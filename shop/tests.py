from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from shop.models import Product
from shop.permissions import PermissionGroup

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpass')
        group, _ = Group.objects.get_or_create(name=PermissionGroup.PRODUCT_MANAGER.value)
        self.user.groups.add(group)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            name='Existing Product',
            sku='EX001',
            price=20.00,
            quantity=100
        )

    def test_create_product(self):
        response = self.client.post('/api/v1/products', {
            'name': 'Test Product',
            'sku': 'TP001',
            'price': 10.99,
            'quantity': 50
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sku'], 'TP001')

    def test_get_all_products(self):
        response = self.client.get('/api/v1/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_single_product(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sku'], 'EX001')

    def test_update_product(self):
        response = self.client.put(f'/api/v1/products/{self.product.id}', {
            'name': 'Updated Product',
            'sku': 'EX001',
            'price': 25.00,
            'quantity': 80
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')

    def test_partial_update_product(self):
        response = self.client.patch(f'/api/v1/products/{self.product.id}', {
            'price': 15.00
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '15.00') 

    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/products/{self.product.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_create_product_missing_fields(self):
        response = self.client.post('/api/v1/products', {
            'sku': 'TP002'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/products')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
