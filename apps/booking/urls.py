from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking_view, name='booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('my-bookings/history/', views.booking_history_view, name='booking_history'),
    path('cart/', views.cart_view, name='cart'),
]