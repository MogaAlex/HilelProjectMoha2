import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        SUCCEEDED = 'succeeded', _('Succeeded')
        FAILED = 'failed', _('Failed')
        CANCELED = 'canceled', _('Canceled')
        REFUNDED = 'refunded', _('Refunded')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # кто платит (нужен для изоляции сервиса)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    # Stripe identifiers
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_charge_id = models.CharField(max_length=255, null=True, blank=True)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.50'))]
    )

    currency = models.CharField(max_length=10, default='USD')

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    description = models.CharField(max_length=255, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    error_message = models.TextField(blank=True, null=True)

    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} | {self.amount} {self.currency} | {self.status}"

    @property
    def is_successful(self):
        return self.status == self.Status.SUCCEEDED

    def can_be_refunded(self):
        return self.is_successful and self.refund_amount < self.amount