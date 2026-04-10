from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid

User = get_user_model()

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Payment(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = 'pending',_('Очікує')
        PROCESSING = 'processing',_('Оброблюється')
        SUCCEEDED = 'SUCCEEDED',_('Успішно')
        FAILED = 'FAILED',_('Невдало')
        CANCELED = 'CANCELED',_('Скасовано')
        REFUNDED = 'REFUNDED',_('Повернуто')
        PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED',_('Частково повернуто')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_charge_id = models.CharField(max_length=255, unique=True, db_index=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators =[MinValueValidator(Decimal('0.50'))])
    currency = models.CharField(max_length=255, default='USD')
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(blank=True)
    metadata = models. JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    class Meta:
        db_table = 'stripe_payments'
        verbose_name = 'Платіж'
        verbose_name_plural = 'Платежі'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Payment {self.id} - {self.amount} {self.currency} ({self.status})'

    @property
    def is_successful(self):
        return self.status == self.Status.SUCCEEDED

    def can_be_refunded(self):
        return {
            self.is_successful and self.refund_amount <= self.amount
        }

