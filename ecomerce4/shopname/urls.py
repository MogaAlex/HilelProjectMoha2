from django.urls import path
from shopname.views import product_list, cart_add, cart_detail, cart_remove, order_create, cart_clear

app_name = 'shopname'

urlpatterns = [
    path('',product_list, name='product_list'),
    path('cart/',cart_detail, name='cart_detail'),
    path( 'cart/add/<int:product_id>', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('order/', order_create, name='order_create'),
]