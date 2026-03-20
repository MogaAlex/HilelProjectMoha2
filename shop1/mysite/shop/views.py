from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Book
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def list(request):
    products = Book.objects.all()
    return render(request, 'list.html', {"products": products} )

def details(request, pk):
    product = get_object_or_404(Book, id = pk)
    return render(request, 'details.html', {"product": product})

class ProductListView(ListView):
    model = Book
    template_name = 'list.html'
    context_object_name ="products"
    paginate_by = 5
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)  # все книги
        pn = self.request.GET.get('title')  # фильтр
        if pn:
            qs = qs.filter(title__icontains=pn)
        return qs



class ProductDetailView(DetailView):
    model = Book
    template_name = 'details.html'
    context_object_name ="product"



class UpdateBook(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = "__all__"
    template_name = 'update_book.html'
    success_url = reverse_lazy('shop:products_list')
    permission_required = 'shop.change_book'
    raise_exception = True
    login_url = 'login'
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Редактирование статьи',
    # }

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = "__all__"
    template_name = 'create_book.html'
    success_url = reverse_lazy('shop:products_list')

    permission_required = 'shop.add_book'
    raise_exception = True
    login_url = 'login'

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('shop:products_list')
    permission_required = 'shop.delete_book'
    raise_exception = True
    login_url = 'login'

class HomeView(TemplateView):
    template_name ='base.html'




