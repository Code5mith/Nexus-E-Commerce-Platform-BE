from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Category, Cart, CartItem, Review, Wishlist
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer, CartSerializer, CartItemSerializer, ReviewSerializer, WishListSerailzer

from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=False)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    # return single instance not Query set -> will Break serializer hence get() 
    product = Product.objects.get(slug=slug) 
    serializer = ProductDetailSerializer(product) 
    print(serializer.data)

    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)

    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1
    cartitem.save()

    serializer = CartSerializer(cart)

    return Response(serializer.data)

@api_view(['PUT'])
def update_cart_item_quantity(request):
    cartitem_id = request.data.get('item_id')
    quantity = int(request.data.get('quantity')) # must cast to an int : str by default

    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)

    return Response({"data" : serializer.data, "message" : "cart updated successfully!"})

@api_view(["POST"])
def add_review(request):
    User = get_user_model()

    product_id = request.data.get("product_id")
    email = request.data.get("email")
    rating = request.data.get("rating")
    review = request.data.get("review")

    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=email)

    if Review.objects.filter(product=product, user=user).exists():
        return Response("You have already reviewed this product", status=400)

    review = Review.objects.create(product=product, user=user, rating=rating, review=review)
    serializer = ReviewSerializer(review)
    
    return Response(serializer.data)

@api_view(['PUT'])
def update_review(request, pk):
    review = Review.objects.get(id=pk) 
    rating = request.data.get("rating")
    review_text = request.data.get("review")

    review.rating = rating 
    review.review = review_text
    review.save()

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_review(request, pk):
    review = Review.objects.get(id=pk) 
    review.delete()

    return Response("Review deleted successfully!", status=204)

@api_view(["POST"])
def add_to_wishlist(request):
    email = request.data.get("email")
    product_id = request.data.get("product_id")

    user = User.objects.get(email=email)
    product = Product.objects.get(id=product_id)

    wishlist = Wishlist.objects.filter(user=user, product=product)
    if wishlist:
        wishlist.delete()
        return Response("Product removed from wishlist!", status=204)
    
    new_wishlist = Wishlist.objects.create(user=user, product=product)
    serializer = WishListSerailzer(new_wishlist)
    return Response(serializer.data) 


@api_view(["DELETE"])
def delete_cartitem(request, pk):
    cartitem = CartItem.objects.get(id=pk)
    cartitem.delete()

    return Response("cart item deleted!", status=204)