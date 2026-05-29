from django.shortcuts import render
from shop.models import Product, Customer




# Create your views here.


def product_list(request):
    products = Product.active.all()
    return render(request, 'products/list.html', {'products': products})