from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('list/', views.ProductListView.as_view(), name='products_list'),
    path('list/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('edit/<int:pk>/', views.UpdateBook.as_view(), name='edit_product'),
    path('add/', views.BookCreateView.as_view(), name='add_product'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_product'),
    ]