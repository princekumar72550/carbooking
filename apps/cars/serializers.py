from rest_framework import serializers
from .models import Car, Category, Driver

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'experience', 'license_number', 'profile_photo']


class CarSerializer(serializers.ModelSerializer):
    car_model_name = serializers.SerializerMethodField()
    car_type_name = serializers.SerializerMethodField()
    driver_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'name', 'car_model', 'car_model_name', 'car_type', 'car_type_name', 'category_name',
            'price_per_km', 'ac_price_per_km', 'non_ac_price_per_km',
            'car_image', 'driver', 'driver_name', 'is_available'
        ]

    def get_car_model_name(self, obj):
        cm = getattr(obj, 'car_model', None)
        return getattr(cm, 'name', '') or ''

    def get_car_type_name(self, obj):
        ct = getattr(obj, 'car_type', None)
        return getattr(ct, 'name', '') or ''

    def get_driver_name(self, obj):
        drv = getattr(obj, 'driver', None)
        return getattr(drv, 'name', '') or ''

    def get_category_name(self, obj):
        return self.get_car_model_name(obj)