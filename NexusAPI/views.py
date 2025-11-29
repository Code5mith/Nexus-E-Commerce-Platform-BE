from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.filter(slug=slug) 
    serializer = ProductDetailSerializer(product) 

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
