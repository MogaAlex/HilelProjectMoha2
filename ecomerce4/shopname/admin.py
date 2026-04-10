from django.contrib import admin
from shopname.models import Product, Customer, Category
from shopname.orders.models import Order, OrderItem

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)

# Register your models here.
