import pytest
from django.urls import reverse
from shopname.models import Product, Customer
from shopname.orders.models import Order
from .factories import ProductFactory


@pytest.mark.django_db
class TestUserFlows:

    def test_flow_anonymous_purchase(self, client):
        p = ProductFactory(price=500, stock=10)
        client.post(reverse('shopname:cart_add', args=[p.id]), {'quantity': 1})
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'i@t.com', 'phone_number': '1', 'address': 'Addr'}
        response = client.post(reverse('shopname:order_create'), data=data)
        assert response.status_code == 200  # Страница успеха
        assert Order.objects.count() == 1

    def test_flow_view_cart_page(self, client):
        url = reverse('shopname:cart_detail')
        response = client.get(url)
        assert response.status_code == 200
        assert 'cart' in response.context

    def test_flow_view_product_list(self, client):
        ProductFactory.create_batch(3)
        url = reverse('shopname:product_list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context['products']) >= 2

    def test_order_create_anonymous(self, client):
        p = ProductFactory()
        client.post(reverse('shopname:cart_add', kwargs={'product_id': p.id}))
        data = {'first_name': 'A', 'last_name': 'B', 'email': 'a@a.com', 'phone_number': '1', 'address': 'X'}
        response = client.post(reverse('shopname:order_create'), data=data)
        assert response.status_code == 200