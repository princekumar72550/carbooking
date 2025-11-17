from django.core.management.base import BaseCommand
from apps.cars.models import Car, Driver
import os
import random
from django.conf import settings

class Command(BaseCommand):
    help = 'Add random sample images to all cars and drivers'

    def handle(self, *args, **options):
        # Define sample image paths
        sample_car_images = [
            'cars/download.jpg',
            'cars/download_1.jpeg',
            'cars/bolero-neo-exterior-right-front-three-quarter.avif',
            'cars/2129020142_e19b33bc4b.jpg',
            'cars/new_images/luxury_car.jpg',
            'cars/new_images/sedan_car.jpg',
            'cars/new_images/truck_car.jpg'
        ]
        
        sample_driver_images = [
            'drivers/download.png',
            'drivers/driver1.jpg',
            'drivers/driver2.jpg',
            'drivers/driver3.jpg'
        ]
        
        # Process all cars
        all_cars = Car.objects.all()
        self.stdout.write(f'Processing {all_cars.count()} cars')
        
        for car in all_cars:
            # Randomly select an image
            random_image = random.choice(sample_car_images)
            car.car_image = random_image
            car.save()
            self.stdout.write(f'Updated car {car.name} with image {random_image}')
            
        # Process all drivers
        all_drivers = Driver.objects.all()
        self.stdout.write(f'Processing {all_drivers.count()} drivers')
        
        for driver in all_drivers:
            # Randomly select an image
            random_image = random.choice(sample_driver_images)
            driver.profile_photo = random_image
            driver.save()
            self.stdout.write(f'Updated driver {driver.name} with image {random_image}')
            
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully updated all cars and drivers with random sample images'
            )
        )