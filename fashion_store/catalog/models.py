from django.db import models
from catalog.utils import unique_slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=10)  # S, M, L, XL
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # #000000
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
