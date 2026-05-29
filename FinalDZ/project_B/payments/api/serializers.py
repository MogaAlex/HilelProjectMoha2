from rest_framework import serializers
from .models import Payment
from decimal import Decimal

class PaymentSerializer(serializers.ModelSerializer):
    is_successful = serializers.BooleanField(read_only=True)
    can_be_refunded = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'stripe_payment_intent_id',
            'stripe_charge_id',
            'amount',
            'currency',
            'status',
            'description',
            'metadata',
            'error_message',
            'refund_amount',
            'created_at',
            'updated_at',
            'is_successful',
            'can_be_refunded',
        ]
        read_only_fields = (
            'id',
            'stripe_payment_intent_id',
            'stripe_charge_id',
            'status',
            'created_at',
            'updated_at',
        )

    def get_can_be_refunded(self, obj):
        return obj.can_be_refunded()




class CreatePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.50")
    )

    currency = serializers.ChoiceField(
        choices=[
            ("USD", "USD"),
            ("EUR", "EUR"),
            ("UAH", "UAH"),
        ],
        default="USD"
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )

    metadata = serializers.JSONField(required=False, default=dict)