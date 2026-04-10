from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()

class Category(MPTTModel):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children')
    is_active = models.BooleanField(_('active'), default=True)

    class MPPTMeta:
        order_inserting_by = ['name']

    def __str__(self):
        return self.name

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, stock__gt=0)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(_('discount price'), max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(_('stock'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(condition=models.Q(stock__gte=0), name='non_negative_stock'),
        ]

    def __str__(self):
        return f'{self.name} - {self.stock}'

    @property
    def current_price(self):
        return self.discount_price or self.price

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.email




