
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.contrib.auth.models import Group
from shop.models import Book
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ExampleUser
from .forms import ExampleUserCreationForm

# managers = Group.objects.get(name="Managers")

@login_required
def orders_list(request):
    orders = Book.objects.filter(customer=request.user)
    return render(request,"shop/list.html", {"orders": orders})


@permission_required("shop.change_book")
def edit_product(request, product_id):
    product = Book.objects.get(id=product_id)
    return render(request,"shop/update_book.html", {"product": product})


def add_to_cart(request, product_id):
    cart = request.session.get("cart", [])
    cart.append(product_id)
    request.session["cart"] = cart

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # редирект после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

