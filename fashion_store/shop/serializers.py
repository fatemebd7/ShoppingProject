from rest_framework import serializers
from shop.models import Cart, CartItem, Order, OrderItem, ShippingAddress, Review
from catalog.serializers import ProductSerializer
from catalog.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )
    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity", "size", "color")

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ("id", "user", "created_at", "items")
        read_only_fields = ("user",)

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        read_only_fields = ("user",)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "price", "size", "color")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "status", "total_price", "items")
        read_only_fields = ("user", "total_price")
