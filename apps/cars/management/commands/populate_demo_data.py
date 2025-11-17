from django.core.management.base import BaseCommand
from apps.cars.models import Category, Driver, Car
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'AC', 'description': 'Air conditioned cars for comfortable travel'},
            {'name': 'Non-AC', 'description': 'Economical cars without air conditioning'},
            {'name': 'Luxury', 'description': 'Premium cars with extra amenities'}
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create drivers
        drivers_data = [
            {
                'name': 'Raj Kumar',
                'phone': '+91 98765 43210',
                'experience': 5,
                'license_number': 'DL01-2025-0001'
            },
            {
                'name': 'Amit Sharma',
                'phone': '+91 98765 43211',
                'experience': 8,
                'license_number': 'DL01-2025-0002'
            },
            {
                'name': 'Vikash Singh',
                'phone': '+91 98765 43212',
                'experience': 3,
                'license_number': 'DL01-2025-0003'
            }
        ]
        
        drivers = []
        for driver_data in drivers_data:
            driver, created = Driver.objects.get_or_create(
                license_number=driver_data['license_number'],
                defaults=driver_data
            )
            drivers.append(driver)
            if created:
                self.stdout.write(f'Created driver: {driver.name}')
            else:
                self.stdout.write(f'Driver already exists: {driver.name}')

        # Create cars
        cars_data = [
            {
                'name': 'Toyota Innova Crysta',
                'category': categories[0],  # AC
                'price_per_km': 15.00,
                'driver': drivers[0],
                'is_available': True
            },
            {
                'name': 'Maruti Suzuki Ertiga',
                'category': categories[0],  # AC
                'price_per_km': 12.00,
                'driver': drivers[1],
                'is_available': True
            },
            {
                'name': 'Hyundai Grand i10',
                'category': categories[1],  # Non-AC
                'price_per_km': 8.00,
                'driver': drivers[2],
                'is_available': True
            },
            {
                'name': 'Mercedes-Benz E-Class',
                'category': categories[2],  # Luxury
                'price_per_km': 25.00,
                'driver': drivers[0],
                'is_available': True
            },
            {
                'name': 'BMW 5 Series',
                'category': categories[2],  # Luxury
                'price_per_km': 30.00,
                'driver': drivers[1],
                'is_available': True
            }
        ]
        
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(
                name=car_data['name'],
                defaults=car_data
            )
            if created:
                self.stdout.write(f'Created car: {car.name}')
            else:
                self.stdout.write(f'Car already exists: {car.name}')

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully populated database with demo data'
            )
        )