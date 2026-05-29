from django.db import models
from django.conf import settings  # Импортируем настройки
from django.utils.translation import gettext_lazy as _
from shopname.models import Product

class Cart(models.Model):
    # Указываем модель пользователя строкой 'auth.User' или через settings
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)