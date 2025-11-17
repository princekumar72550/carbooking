from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Booking
from apps.cars.models import Car

@receiver(pre_save, sender=Booking)
def update_car_availability(sender, instance, **kwargs):
    # If this is a new booking
    if instance.pk is None:
        # Check if car is available
        if not instance.car.is_available:
            raise ValueError("Car is not available for booking")
        # Set car as unavailable
        instance.car.is_available = False
        instance.car.save()
    else:
        # This is an update to an existing booking
        # Get the original booking
        try:
            original_booking = Booking.objects.get(pk=instance.pk)
            # If booking status changed to cancelled or completed
            if (original_booking.booking_status == 'active' and 
                instance.booking_status in ['cancelled', 'completed']):
                # Make car available again
                instance.car.is_available = True
                instance.car.save()
        except Booking.DoesNotExist:
            pass