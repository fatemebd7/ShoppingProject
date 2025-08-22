from rest_framework import viewsets, permissions
from catalog.models import Category, Product, Size, Color
from catalog.serializers import CategorySerializer, ProductSerializer, SizeSerializer, ColorSerializer

class IsEmployeeOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET",):
            return True
        user = request.user
        return user.is_authenticated and user.role in ("employee", "admin")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsEmployeeOrAdmin]

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsEmployeeOrAdmin]

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsEmployeeOrAdmin]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("sizes", "colors").all()
    serializer_class = ProductSerializer
    permission_classes = [IsEmployeeOrAdmin]
