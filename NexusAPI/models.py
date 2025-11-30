from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(blank=True, null=True) 

    def __str__(self) -> str:
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="category_image", blank=True, null=True)

    def __str__(self) -> str:
        return self.name #type:ignore
    

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="product_image", blank=True, null=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

    def __str__(self) -> str:
        return self.name #type:ignore
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) #type:ignore
            unique_slug = self.slug
            counter = 1
            if Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{counter}'
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)


class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_code 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item")
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.quantity} x {self.product.name} in cart {self.cart.id}' #type:ignore