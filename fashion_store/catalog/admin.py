from django.contrib import admin
from .models import Category, Product, Size, Color

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)  # ← این خط اضافه شد

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "slug")
    list_filter = ("category", "colors", "sizes")
    search_fields = ("name", "slug")
    autocomplete_fields = ("category",)
