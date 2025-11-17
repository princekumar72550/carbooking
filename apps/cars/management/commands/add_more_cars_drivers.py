from django.core.management.base import BaseCommand
from apps.cars.models import CarModel, CarType, Car, Driver
import random

class Command(BaseCommand):
    help = 'Add more cars and drivers to the database'

    def handle(self, *args, **options):
        # Get existing car models and types
        car_models = list(CarModel.objects.all())
        car_types = list(CarType.objects.all())
        
        if not car_models or not car_types:
            self.stdout.write(
                self.style.ERROR(
                    'No car models or car types found. Please run populate_demo_data first.'
                )
            )
            return
            
        # Create additional drivers
        additional_drivers_data = [
            {
                'name': 'Suresh Patel',
                'phone': '+91 98765 43213',
                'experience': 6,
                'license_number': 'DL01-2025-0004'
            },
            {
                'name': 'Manoj Verma',
                'phone': '+91 98765 43214',
                'experience': 4,
                'license_number': 'DL01-2025-0005'
            },
            {
                'name': 'Deepak Yadav',
                'phone': '+91 98765 43215',
                'experience': 7,
                'license_number': 'DL01-2025-0006'
            },
            {
                'name': 'Anil Gupta',
                'phone': '+91 98765 43216',
                'experience': 5,
                'license_number': 'DL01-2025-0007'
            },
            {
                'name': 'Ramesh Tiwari',
                'phone': '+91 98765 43217',
                'experience': 9,
                'license_number': 'DL01-2025-0008'
            },
            {
                'name': 'Sunil Mishra',
                'phone': '+91 98765 43218',
                'experience': 3,
                'license_number': 'DL01-2025-0009'
            }
        ]
        
        new_drivers = []
        for driver_data in additional_drivers_data:
            driver, created = Driver.objects.get_or_create(
                license_number=driver_data['license_number'],
                defaults=driver_data
            )
            new_drivers.append(driver)
            if created:
                self.stdout.write(f'Created driver: {driver.name}')
            else:
                self.stdout.write(f'Driver already exists: {driver.name}')
                
        # Combine existing and new drivers
        all_drivers = list(Driver.objects.all())
        
        # Create additional cars
        additional_cars_data = [
            {
                'name': 'Toyota Fortuner Alpha',
                'car_model': car_models[0],  # Toyota Fortuner
                'car_type': car_types[0],    # AC
                'price_per_km': 16.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Toyota Fortuner Beta',
                'car_model': car_models[0],  # Toyota Fortuner
                'car_type': car_types[1],    # Non-AC
                'price_per_km': 13.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Toyota Fortuner Gamma',
                'car_model': car_models[0],  # Toyota Fortuner
                'car_type': car_types[2],    # Both
                'price_per_km': None,
                'ac_price_per_km': 17.00,
                'non_ac_price_per_km': 14.00,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Thar Delta',
                'car_model': car_models[1],  # Mahindra Thar
                'car_type': car_types[0],    # AC
                'price_per_km': 14.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Thar Epsilon',
                'car_model': car_models[1],  # Mahindra Thar
                'car_type': car_types[1],    # Non-AC
                'price_per_km': 11.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Thar Zeta',
                'car_model': car_models[1],  # Mahindra Thar
                'car_type': car_types[2],    # Both
                'price_per_km': None,
                'ac_price_per_km': 15.00,
                'non_ac_price_per_km': 12.00,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Bolero Eta',
                'car_model': car_models[2],  # Mahindra Bolero
                'car_type': car_types[0],    # AC
                'price_per_km': 12.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Bolero Theta',
                'car_model': car_models[2],  # Mahindra Bolero
                'car_type': car_types[1],    # Non-AC
                'price_per_km': 9.00,
                'ac_price_per_km': None,
                'non_ac_price_per_km': None,
                'driver': random.choice(all_drivers),
                'is_available': True
            },
            {
                'name': 'Mahindra Bolero Iota',
                'car_model': car_models[2],  # Mahindra Bolero
                'car_type': car_types[2],    # Both
                'price_per_km': None,
                'ac_price_per_km': 13.00,
                'non_ac_price_per_km': 10.00,
                'driver': random.choice(all_drivers),
                'is_available': True
            }
        ]
        
        for car_data in additional_cars_data:
            # Create a unique name by appending a random number if needed
            car_name = car_data['name']
            counter = 1
            while Car.objects.filter(name=car_name).exists():
                car_name = f"{car_data['name']} #{counter}"
                counter += 1
                
            car_data['name'] = car_name
            car = Car.objects.create(**car_data)
            self.stdout.write(f'Created car: {car.name}')
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {len(additional_cars_data)} cars and {len(new_drivers)} drivers'
            )
        )