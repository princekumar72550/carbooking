from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.booking.models import Booking
from apps.cars.models import Car

class Command(BaseCommand):
    help = 'Update car availability based on booking end dates'

    def handle(self, *args, **options):
        # Get all active bookings where drop_date has passed
        expired_bookings = Booking.objects.filter(
            booking_status='active',
            drop_date__lt=timezone.now()
        )
        
        updated_count = 0
        for booking in expired_bookings:
            # Update booking status to completed
            booking.booking_status = 'completed'
            booking.save()
            
            # Make car available again
            car = booking.car
            car.is_available = True
            car.save()
            
            updated_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} cars and bookings'
            )
        )