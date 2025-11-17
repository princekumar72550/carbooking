from django.urls import path
from . import api_views

urlpatterns = [
    path('booking/', api_views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('booking/my/', api_views.UserBookingsView.as_view(), name='user-bookings'),
]