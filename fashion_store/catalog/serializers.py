from rest_framework import serializers
from catalog.models import Category, Product, Size, Color

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source="category"
    )
    sizes = SizeSerializer(many=True, read_only=True)
    size_ids = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), many=True, write_only=True, source="sizes", required=False
    )
    colors = ColorSerializer(many=True, read_only=True)
    color_ids = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), many=True, write_only=True, source="colors", required=False
    )

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price", "stock", "image",
            "category", "category_id", "sizes", "size_ids", "colors", "color_ids",
            "created_at", "updated_at"
        )

    def create(self, validated_data):
        sizes = validated_data.pop("sizes", [])
        colors = validated_data.pop("colors", [])
        product = super().create(validated_data)
        if sizes: product.sizes.set(sizes)
        if colors: product.colors.set(colors)
        return product

    def update(self, instance, validated_data):
        sizes = validated_data.pop("sizes", None)
        colors = validated_data.pop("colors", None)
        product = super().update(instance, validated_data)
        if sizes is not None: product.sizes.set(sizes)
        if colors is not None: product.colors.set(colors)
        return product
