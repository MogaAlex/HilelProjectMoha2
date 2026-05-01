import pytest
from shopname.models import Product, Category
from .factories import ProductFactory


@pytest.mark.django_db
class TestModels:
    def test_price(self):
        order = ProductFactory(price=2000)
        assert order.price == 2000

    def test_name(self):
        naming = ProductFactory(name="Капица")
        assert naming.name == "Капица"

    def test_description(self):
        desc = ProductFactory(description="абв")
        assert desc.description == "абв"

    def test_stock(self):
        stocker = ProductFactory(stock=100)
        assert stocker.stock == 100

    def test_product_str(self):
        product = ProductFactory(name="Дюма", stock=10)
        assert str(product) == "Дюма - 10"

    def test_current_price(self):

        p1 = ProductFactory(price=1000, discount_price=None)
        assert p1.current_price == 1000

        p2 = ProductFactory(price=1000, discount_price=800)
        assert p2.current_price == 800

