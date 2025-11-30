from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
admin.site.register(models.CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "featured")
admin.site.register(models.Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug") 
admin.site.register(models.Category, CategoryAdmin)

admin.site.register([models.Cart,models.CartItem, models.Review, models.ProductRating, models.Wishlist, models.Order, models.OrderItem])
