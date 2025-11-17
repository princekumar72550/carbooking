from rest_framework import serializers
from .models import Booking
from apps.cars.serializers import CarSerializer

class BookingSerializer(serializers.ModelSerializer):
    car_details = CarSerializer(source='car', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'car', 'car_details', 'pickup_location', 
            'drop_location', 'pickup_date', 'drop_date', 
            'total_price', 'payment_status', 'booking_status'
        ]
        read_only_fields = ['user', 'total_price']