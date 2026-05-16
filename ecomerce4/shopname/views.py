from django.shortcuts import render, redirect, get_object_or_404, aget_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from botocore.exceptions import ClientError
#from quorum.error import errors_json
from shopname.models import Product, Customer
from shopname.orders.models import Order, OrderItem
from shopname.cart.cart import Cart
from django.contrib import messages
from shopname.forms import OrderCreateForm
from django.core.mail import send_mail
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from django.utils.translation import gettext as _
import logging
from shopname.tasks import test_task, send_confirmation_order_email
from shopname.boto_client import get_s3_client, FILE_BUCKET_NAME


logger = logging.getLogger(__name__)

default_cache = caches['default']


@cache_page(60 * 15, cache="page_cache", key_prefix="product_list")
def product_list(request):

    products = Product.active.all()
    if request.user.is_authenticated:
        user_id = request.user.id
        test_task.delay(user_id)
    return render(request, 'products/list.html', {'products': products})

# async def product_list(request):
#     """
#     Асинхронно відображає список усіх товарів магазину.
#     Використовує асинхронний ітератор для отримання продуктів з бази даних.
#     """
#     products = []
#     async for product in Product.objects.all():
#         products.append(product)
#
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         test_task.delay(user_id)
#     else:
#         pass
#
#     return render(request, 'products/list.html', {'products': products})


def cart_detail(request):
    """
    Відображає вміст кошика та загальну вартість товарів.
    """

    cart = Cart(request)

    context = {
        'cart':cart,
        'total_price':cart.get_total_price(),

    }
    return render(request, 'cart/detail.html', context)

def cart_add(request, product_id):
    """
    Додає товар до кошика за його ID.
    Якщо товар вже є, оновлює його кількість без перезапису.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, override_quantity=False)
        messages.success(request, _(f'{product.name} added to cart!'))
    return redirect('shopname:cart_detail')


async def cart_remove(request, product_id):
    """
    Асинхронно видаляє товар з кошика.
    Використовує sync_to_async для сумісності з класом Cart.
    """
    cart = await sync_to_async(Cart)(request)
    product = await aget_object_or_404(Product, id=product_id, is_active=True)
    await sync_to_async(cart.remove)(product)
    # messages.info(request, f'{product.name} removed from cart!')
    return redirect('shopname:cart_detail')


def order_create(request):
    """
    Обробляє створення замовлення.
    Прив'язує замовлення до Customer (профілю користувача) та переносить товари з кошика в OrderItem.
    """
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
            send_confirmation_order_email.delay(order.id)
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


async def cart_clear(request):
    """
    Асинхронно повністю очищує вміст кошика користувача.
    """
    cart = await sync_to_async(Cart)(request)
    await sync_to_async(cart.clear)()
    return redirect('shopname:cart_detail')


def send_order_email(order):
    """
    Відправляє підтвердження замовлення на електронну пошту клієнта.
    """
    subject = f"Заказ №{order.id}"
    message = f"Привет, {order.first_name}! Твой заказ на сумму {order.total_price} принят."
    recipient_list = [order.email]

    return send_mail(subject, message, 'admin@shop.com', recipient_list)

def upload_s3_files(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        logger.info(f'File: {file.name}')
        try:
            default_storage.save(file.name, ContentFile(file.read()))
        except Exception as e:
            logger.error(str(e))
    return redirect('s3_files_list')

def s3_files_list(request):
    s3_client = get_s3_client()
    files = []
    errors = []
    continuation_token = None

    try:
        while True:
            params = {'Bucket': FILE_BUCKET_NAME}
            if continuation_token:
                params['ContinuationToken'] = continuation_token
            response = s3_client.list_objects_v2(**params)
            for file in response.get('Contents', []):
                file_name = file['Key']
                try:
                    file_params = params.copy()
                    file_params['Key'] = file_name
                    presign_file_url = s3_client.generate_presigned_url(
                        'get_object',
                        Params=file_params,
                        ExpiresIn=30,

                    )
                    files.append({
                        'file_name': file_name,
                        'file_url': presign_file_url,
                        'size': file['Size'],
                        'last_modified': file['LastModified'],
                    })

                except ClientError as err:
                    errors.append(err)
                    logger.error(f'Client error: {err}')
            if response.get('isTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break

    except ClientError as err:
            errors.append(err)
            logger.error(f'Client error: {err}')

    return render(request, 's3_bucket/s3_files_list.html', {'files': files, 'errors': errors})


def product_detail(request, pk):
    cache_key = f"product_detail_{pk}"

    product = default_cache.get(cache_key)

    if not product:
        product = get_object_or_404(Product.active, pk=pk)
        default_cache.set(cache_key, product)
        logger.info(f" Товар {pk} взят из Postgres и сохранен в Redis")
    else:
        logger.info(f" Товар {pk} успешно получен напрямую из низкоуровневого кэша")

    return render(request, 'products/detail.html', {'product': product})