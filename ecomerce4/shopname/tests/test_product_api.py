from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from shopname.models import Product, Category


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Books', slug='books')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(
            name='Django for Professionals',
            slug='django-pro',
            price=50.00,
            category=self.category,
            stock=10,
            is_active=True
        )

    def test_get_product_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


    def test_product_price_filter(self):
        Product.objects.create(
            name='Expensive Book', slug='expensive', price=200.00,
            category=self.category, stock=5, is_active=True
        )