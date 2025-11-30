from rest_framework import serializers
from .models import Product, Category, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','price', 'image']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','price', 'image', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) # serialize the products in the category 
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # serialize the products in the category 
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']
    
    def get_sub_total(self, cartitem):
        total = cartitem.product.price * cartitem.quantity
        return total
    
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'cartitems', 'cart_total']

    def get_cart_total(self, cart):
        items = cart.cartitems.all() # model relation_name property issue  
        total = sum([item.quantity * item.product.price for item in items ])
        return total
    
class CartStatSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'total_quantity']
    
    def get_total_quantity(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity for item in items ])
        return total