from django.shortcuts import render
from .models import Book, Category
from django.db.models import Q, Count

# def all_categories(request):
#     products = Book.objects.all()
#     return render(request, 'records.html', )

#Копировать - Вставить через manage.py shell
#from shop.models import Book


products = Book.objects.all()
print(products)

active_products = Book.objects.filter(stock__gt=0)
print(active_products)



products_with_purchase_count = Book.objects.annotate(
    purchase_count=Count("title")
)
print(products_with_purchase_count.values("stock"))

products_filtered = Book.objects.filter(
    Q(price__lt=10)
    |
    Q(stock__gt=0)
)
print(products_filtered)