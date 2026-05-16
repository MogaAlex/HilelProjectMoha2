from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import caches
from shopname.orders.models import OrderItem, Order
from shopname.models import Product


@receiver(post_save, sender=OrderItem)
def change_stock_on_order(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save(update_fields=['stock'])
        else:
            order = instance.order
            order.status = Order.Orderstatus.CANCELED
            order.save(update_fields=['status'])


@receiver(post_save, sender=OrderItem)
def change_stock_on_order(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save(update_fields=['stock'])  # Тут вызывается сохранение товара!
        else:
            order = instance.order
            order.status = Order.Orderstatus.CANCELED
            order.save(update_fields=['status'])


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    page_cache = caches['page_cache']
    page_cache.clear()

    default_cache = caches['default']
    cache_key = f"product_detail_{instance.id}"
    default_cache.delete(cache_key)

    print(f"--- [SIGNALS] Кэш страниц и товара {instance.id} успешно сброшен из Redis! ---")