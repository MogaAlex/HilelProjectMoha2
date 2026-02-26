from .models import Book, Category
from django.db.models import Q, Count
#Копировать - Вставить через manage.py shell
#from shop.models import Book, Category


products = Book.objects.all()
print(products)

active_products = Book.objects.filter(stock__gt=0)
print(active_products)



products_with_purchase_count = Category.objects.annotate(
    purchase_count=Count("books")
)
print(products_with_purchase_count.values("name","purchase_count"))

products_filtered = Book.objects.filter(
    Q(price__lt=10) | Q(stock__gt=0)
)
print(products_filtered)