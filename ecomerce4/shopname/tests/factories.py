import factory

from shopname.models import Category, Product, Customer
from shopname.orders.models import Order




class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker('word')
    slug = factory.Sequence(lambda n: f'Приключение-{n}')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)


    name = factory.Faker('name')
    description = "description"
    price = 1000
    discount_price = 5
    stock = 12
    slug = factory.Sequence(lambda n: f'Три мушкетера-{n}')



class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    address = factory.Faker('address')
    phone_number = factory.Faker('phone_number')
    total_price = 1000.00