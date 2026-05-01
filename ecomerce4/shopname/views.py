from django.shortcuts import render, redirect, get_object_or_404, aget_object_or_404
from django.contrib.auth.decorators import login_required
from shopname.models import Product, Customer
from shopname.orders.models import Order, OrderItem
from shopname.cart.cart import Cart
from django.contrib import messages
from shopname.forms import OrderCreateForm
from django.core.mail import send_mail
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from django.utils.translation import gettext as _


# def product_list(request):
#     products = Product.active.all()
#     #products = Product.objects.all()
#     #return render(request, 'shopname/product_list.html', {'products': products})
#     return render(request, 'products/list.html', {'products': products})

async def product_list(request):
    products = []
    async for product in Product.objects.all():
        products.append(product)
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

# async def cart_detail(request):
#     cart = await sync_to_async(Cart)(request)
#     total_price = await sync_to_async(cart.get_total_price)()
#     context = {
#         'cart':cart,
#         'total_price':total_price,
#     }
#     return render(request, 'cart/detail.html', context)



def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, override_quantity=False)
        messages.success(request, _(f'{product.name} added to cart!'))
    return redirect('shopname:cart_detail')

# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id, is_active=True)
#     cart.remove(product)
#     messages.info(request, f'{product.name} removed from cart!')
#     return redirect('shopname:cart_detail')

async def cart_remove(request, product_id):
    cart = await sync_to_async(Cart)(request)
    product = await aget_object_or_404(Product, id=product_id, is_active=True)
    await sync_to_async(cart.remove)(product)
    # messages.info(request, f'{product.name} removed from cart!')
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
        messages.warning(request, _('Карта порожна!'))
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

            messages.success(request, _(f'Замовлення №{order.id} успішно створено!'))
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


# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect('shopname:cart_detail')


async def cart_clear(request):
    cart = await sync_to_async(Cart)(request)
    await sync_to_async(cart.clear)()
    return redirect('shopname:cart_detail')


def send_order_email(order):

    subject = f"Заказ №{order.id}"
    message = f"Привет, {order.first_name}! Твой заказ на сумму {order.total_price} принят."
    recipient_list = [order.email]

    return send_mail(subject, message, 'admin@shop.com', recipient_list)