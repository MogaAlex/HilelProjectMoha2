from django.urls import path
from shop.views import (
    product_list,
)

app_name = 'shop'

urlpatterns = [
    path('',product_list, name='product_list'),
]