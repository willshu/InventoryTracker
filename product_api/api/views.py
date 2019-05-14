from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def home(request):
    context = {"products": Product.objects.all()}
    return render(request, 'api/main.html', context)

class ProductList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'id', 'stock')

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  
