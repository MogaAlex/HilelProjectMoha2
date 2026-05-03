import pytest
from shopname.models import Product, Category
from .factories import ProductFactory, CustomerFactory
from decimal import Decimal
from django.contrib.auth import get_user_model


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

    def test_active_manager_logic(self):
        # Generated with AI, reviewed and modified
        ProductFactory(is_active=True, stock=10)
        ProductFactory(is_active=False, stock=10)
        ProductFactory(is_active=True, stock=0)

        active_count = Product.active.count()
        assert active_count == 1, "Менеджер 'active' должен возвращать только активные товары со стоком > 0"

@pytest.mark.django_db
class TestProductAI:
    def test_active_manager_logic(self):
        # Generated with AI, reviewed and modified
        ProductFactory(is_active=True, stock=10)
        ProductFactory(is_active=False, stock=10)
        ProductFactory(is_active=True, stock=0)

        active_count = Product.active.count()
        assert active_count == 1, "Менеджер 'active' должен возвращать только активные товары со стоком > 0"

    def test_current_price_with_discount(self):
        # Generated with AI, reviewed and modified
        product = ProductFactory(
            price=Decimal('1000.00'),
            discount_price=Decimal('800.00')
        )
        assert product.current_price == Decimal('800.00')


User = get_user_model()


@pytest.mark.django_db
class TestCustomerAI:
    def test_customer_str_full_name(self):
        # Generated with AI, reviewed and modified
        # Создаем пользователя вручную, чтобы точно контролировать имя
        user = User.objects.create(
            username="test_user_1",
            first_name="Taras",
            last_name="Shevchenko"
        )
        # Используем фабрику, переопределяя user
        customer = CustomerFactory(user=user)

        # Проверяем твой метод __str__
        assert str(customer) == "Taras Shevchenko"

    def test_customer_str_email_fallback(self):
        # Generated with AI, reviewed and modified
        # Проверяем случай, когда имени нет
        user = User.objects.create(
            username="test_user_2",
            first_name="",
            last_name="",
            email="test@example.com"
        )
        customer = CustomerFactory(user=user)

        # Должен вернуться email
        assert str(customer) == "test@example.com"
