from django.contrib import admin
from django import forms
from .models import Category, Driver, Car, CarModel, CarType

class CarInline(admin.TabularInline):
    model = Car
    extra = 1
    fields = ('name', 'car_type', 'driver', 'price_per_km', 'ac_price_per_km', 'non_ac_price_per_km', 'is_available')
    readonly_fields = ('name', 'car_type', 'driver', 'price_per_km', 'ac_price_per_km', 'non_ac_price_per_km')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # More robust pattern to extract car model ID
        import re
        # Match patterns like /admin/cars/carmodel/3/change/ or /carmodel/3/
        match = re.search(r'/carmodel/(\d+)', request.path)
        if match:
            car_model_id = int(match.group(1))
            return qs.filter(car_model_id=car_model_id)
        return qs

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
    )

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'license_number', 'experience')
    search_fields = ('name', 'license_number')
    list_filter = ('experience',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'car_type', 'driver', 'price_per_km', 'is_available')
    list_filter = ('car_model', 'car_type', 'is_available')
    search_fields = ('name', 'driver__name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'car_model', 'car_type', 'driver')
        }),
        ('Pricing', {
            'fields': ('price_per_km', 'ac_price_per_km', 'non_ac_price_per_km')
        }),
        ('Availability', {
            'fields': ('car_image', 'is_available')
        }),
    )