from django.contrib import admin
from django.db.models import Model

from shop.models import Book, Category


# Register your models here.
class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookInline]

@admin.register(Book)
class FindBook(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    list_filter = ['title', 'author', 'category']



#admin.site.register(Book)
#admin.site.register(Category)
