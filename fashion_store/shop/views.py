from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from shop.models import Cart, CartItem, Order, OrderItem, ShippingAddress, Review
from shop.serializers import (
    CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer,
    ShippingAddressSerializer
)
from catalog.models import Product
from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IsAuthenticatedOnly(permissions.IsAuthenticated):
    pass

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticatedOnly]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related("items__product")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save(cart=cart)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        item_id = request.data.get("item_id")
        CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticatedOnly]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def checkout(self, request):
        user = request.user
        cart = Cart.objects.select_for_update().get(user=user)
        cart_items = cart.items.select_related("product")
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user, status="processing", total_price=0)
        total = 0
        for ci in cart_items:
            price = ci.product.price
            OrderItem.objects.create(
                order=order, product=ci.product, quantity=ci.quantity, price=price,
                size=ci.size, color=ci.color
            )
            # کاهش موجودی
            if ci.product.stock < ci.quantity:
                raise ValueError("Insufficient stock")
            ci.product.stock -= ci.quantity
            ci.product.save(update_fields=["stock"])
            total += price * ci.quantity

        order.total_price = total
        order.save(update_fields=["total_price"])
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
