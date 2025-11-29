from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(blank=True, null=True) 

    def __str__(self) -> str:
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to="category_image", blank=True, null=True)

    def __str__(self) -> str:
        return self.name #type:ignore
    

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField()
    image = models.ImageField(upload_to="product_image", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

    def __str__(self) -> str:
        return self.name #type:ignore
    
