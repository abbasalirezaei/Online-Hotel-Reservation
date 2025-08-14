# reservations/admin.py
from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'room', 'booking_status', 'checking_date',
        'checkout_date', 'nights', 'total_price', 'prefered_payment_method'
    )
    list_filter = ('booking_status', 'prefered_payment_method', 'booking_date')
    search_fields = ('user__user__email', 'room__title')
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date', 'updated_at', 'cancelled_at', 'total_price')

  
    def user_email(self, obj):
        return obj.user.user.email
    user_email.short_description = 'Customer Email'



