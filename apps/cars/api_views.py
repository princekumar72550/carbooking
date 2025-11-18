from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.conf import settings
from .models import Car, Category, Driver
from .serializers import CarSerializer, CategorySerializer, DriverSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # Try to get cached response
        cache_key = 'categories_list'
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # If not cached, get from database and cache it
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response, settings.API_CACHE_TIMEOUT)
        return response


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # Try to get cached response
        cache_key = 'drivers_list'
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # If not cached, get from database and cache it
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response, settings.API_CACHE_TIMEOUT)
        return response


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        # Try to get cached response
        cache_key = 'cars_list'
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # If not cached, get from database and cache it
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response, settings.API_CACHE_TIMEOUT)
        return response
    
    def get_queryset(self):
        queryset = Car.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        return queryset


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        # Try to get cached response
        cache_key = f'car_detail_{kwargs.get("pk")}'
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # If not cached, get from database and cache it
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response, settings.API_CACHE_TIMEOUT)
        return response