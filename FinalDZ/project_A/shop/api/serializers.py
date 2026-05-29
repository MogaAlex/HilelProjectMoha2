from decimal import Decimal
from rest_framework import serializers
from shopname.models import Product, Category
from shopname.orders.models import Order, OrderItem
from shopname.cart.models import Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id','name','slug','parent', 'is_active','children']

    def get_children(self, obj):
        active_children = obj.children.filter(is_active=True)
        return CategorySerializer(active_children, many=True).data

class ProductSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'category',
            'stock',
            'is_active',
            'category_name',
            'current_price',
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'category',
            'stock',
            'is_active',
            'current_price',
            'created_at',
            'updated_at',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'get_total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'first_name', 'last_name',
            'email', 'phone_number', 'address',
            'status', 'status_display', 'total_price',
            'items', 'created_at'
        ]
        read_only_fields = ['total_price', 'status']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.current_price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.current_price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_quantity', 'grand_total', 'created_at']

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_grand_total(self, obj):
        return sum(item.quantity * item.product.current_price for item in obj.items.all())



