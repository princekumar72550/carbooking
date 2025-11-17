from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer
from apps.cars.models import Car

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Check if car is available
        car_id = request.data.get('car')
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not car.is_available:
            return Response({'error': 'Car is not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create booking
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set car as unavailable
        car.is_available = False
        car.save()
        
        # Save booking with user
        booking = serializer.save(user=self.request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)