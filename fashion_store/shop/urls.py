from rest_framework.routers import DefaultRouter
from django.urls import path, include
from shop.views import CartViewSet, OrderViewSet, ShippingAddressViewSet

router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"addresses", ShippingAddressViewSet, basename="address")

urlpatterns = [path("", include(router.urls))]
