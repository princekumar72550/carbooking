from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def booking_view(request):
    return render(request, 'booking/booking.html')

@login_required
def my_bookings_view(request):
    # Get all bookings for the current user
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def booking_history_view(request):
    # Get completed and cancelled bookings for the current user
    history_bookings = Booking.objects.filter(
        user=request.user,
        booking_status__in=['completed', 'cancelled']
    ).order_by('-created_at')
    
    return render(request, 'booking/booking_history.html', {'bookings': history_bookings})

def cart_view(request):
    # This view will be used to display the cart contents
    # The actual cart data will be managed via JavaScript
    return render(request, 'booking/cart.html')