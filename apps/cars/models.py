from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Categories"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    experience = models.IntegerField(help_text="Years of experience")
    license_number = models.CharField(max_length=50, unique=True)
    profile_photo = models.ImageField(upload_to='drivers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = "drivers"


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='car_models/', blank=True, null=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Car Models"


class CarType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Car Types"


class Car(models.Model):
    name = models.CharField(max_length=100)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name="Car Model")
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, verbose_name="Car Type")
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for the default car type", null=True, blank=True)
    ac_price_per_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price for AC variant (if car type is Both)")
    non_ac_price_per_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price for Non-AC variant (if car type is Both)")
    car_image = models.ImageField(upload_to='cars/', blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.car_model.name} - {self.car_type.name})"
    
    class Meta:
        db_table = "cars"