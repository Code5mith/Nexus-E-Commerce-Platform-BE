from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Category, Cart, CartItem, Review, Wishlist, Order, OrderItem
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer, CartSerializer, CartItemSerializer, ReviewSerializer, WishListSerailzer

from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY 

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

@api_view(["GET"])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response("No search query provided", status=400)
    
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


## stripe payment inegration
@api_view(['POST'])
def create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")
    cart = Cart.objects.get(cart_code=cart_code)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email= email,
            payment_method_types=['card'],

            line_items=[ #type:ignore
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.product.name},
                        'unit_amount': int(item.product.price) * 100,  # Amount in cents
                    },
                    'quantity': item.quantity,
                }
                for item in cart.cartitems.all() #type:ignore
            ] + [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'VAT Fee'},
                        'unit_amount': 500,  # $5 in cents
                    },
                    'quantity': 1,
                }
            ],
           
            mode='payment',
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",

            # success_url="https://next-shop-self.vercel.app/success",
            # cancel_url="https://next-shop-self.vercel.app/failed",
            metadata = {"cart_code": cart_code}
        )
        return Response({'data': checkout_session})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# @csrf_exempt
# def my_webhook_view(request):
#   payload = request.body
#   sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#   event = None

#   try:
#     event = stripe.Webhook.construct_event(
#       payload, sig_header, endpoint_secret
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#   except stripe.error.SignatureVerificationError as e:
#     # Invalid signature
#     return HttpResponse(status=400)

#   if (
#     event['type'] == 'checkout.session.completed'
#     or event['type'] == 'checkout.session.async_payment_succeeded'
#   ):
#     session = event['data']['object']
#     cart_code = session.get("metadata", {}).get("cart_code")

#     fulfill_checkout(session, cart_code)


#   return HttpResponse(status=200)



def fulfill_checkout(session, cart_code):
    
    order = Order.objects.create(stripe_checkout_id=session["id"],
        amount=session["amount_total"],
        currency=session["currency"],
        customer_email=session["customer_email"],
        status="Paid")
    

    print(session)


    cart = Cart.objects.get(cart_code=cart_code)
    cartitems = cart.cartitems.all() #type:ignore

    for item in cartitems:
        orderitem = OrderItem.objects.create(order=order, product=item.product, 
                                             quantity=item.quantity)
    cart.delete()

