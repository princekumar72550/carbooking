from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'pickup_location', 'drop_location', 'pickup_date', 'drop_date', 'total_price', 'payment_status')
    list_filter = ('payment_status', 'pickup_date')
    search_fields = ('user__username', 'car__name')
    date_hierarchy = 'pickup_date'