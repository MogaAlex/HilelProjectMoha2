from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shopname.models import Product, Customer
from shopname.orders.models import Order, OrderItem
from shopname.cart.cart import Cart
from django.contrib import messages
from shopname.forms import OrderCreateForm

def product_list(request):
    products = Product.active.all()
    #products = Product.objects.all()
    #return render(request, 'shopname/product_list.html', {'products': products})
    return render(request, 'products/list.html', {'products': products})

def cart_detail(request):
    cart = Cart(request)

    context = {
        'cart':cart,
        'total_price':cart.get_total_price(),

    }
    return render(request, 'cart/detail.html', context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, override_quantity=False)
        messages.success(request, f'{product.name} added to cart!')
    #return redirect('shopname:cart_add')
    return redirect('shopname:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart.remove(product)
    messages.info(request, f'{product.name} removed from cart!')
    return redirect('shopname:cart_detail')

def order_create(request):
    cart = Cart(request)

    if not cart.cart:
        messages.warning(request, 'cart is empty!')
        return redirect('shopname:detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()

            if request.user.is_authenticated:
                try:
                    order.customer = request.user.customer
                except:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    order.customer = customer
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                )
            cart.clear()

            messages.success(request, f'{order.id} added to cart!')
            return render(request, 'order/success_order.html', {'order': order})
        else:
            initial = {}
            if request.user.is_authenticated:

                customer = None
                user = request.user

                initial = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,

                }

                if customer:
                    initial.update({
                        'phone_number': getattr(customer, 'phone_number',''),
                        'address': getattr(customer, 'address',''),
                    })

            form = OrderCreateForm(initial=initial)
    context = {
        'form': form,
        'cart': cart,
        'total_price': cart.get_total_price(),
    }

    return render(request, 'order/create_order.html', context)


def order_create(request):
    cart = Cart(request)

    if not cart.cart:
        messages.warning(request, 'cart is empty!')
        return redirect('shopname:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()

            if request.user.is_authenticated:
                try:
                    order.customer = request.user.customer
                except:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    order.customer = customer

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()

            messages.success(request, f'Замовлення №{order.id} успішно створено!')
            return render(request, 'orders/success_order.html', {'order': order})


    else:
        initial = {}
        if request.user.is_authenticated:
            user = request.user
            initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }

        form = OrderCreateForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'total_price': cart.get_total_price(),
    }

    return render(request, 'orders/create_order.html', context)

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shopname:cart_detail')