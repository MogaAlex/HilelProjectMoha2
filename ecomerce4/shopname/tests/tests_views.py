import pytest
import asyncio
from django.urls import reverse
from shopname.models import Product, Customer
#from shopname.factories import ProductFactory, UserFactory

@pytest.mark.django_db
class TestViewsUrl:
    def test_product_list_url(self, client):
        response = client.get(reverse('shopname:product_list'))
        assert response.status_code == 200

    def test_cart_detail_view(self, client):
        url = reverse('shopname:cart_detail')
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cart_clear_url(self, async_client):
        response = await async_client.get(reverse('shopname:cart_clear'))
        assert response.status_code == 302

    def test_order_create_url_redirect(self, client):
        response = client.get(reverse('shopname:order_create'))
        assert response.status_code == 302









