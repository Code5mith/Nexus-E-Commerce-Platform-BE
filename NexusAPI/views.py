from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
