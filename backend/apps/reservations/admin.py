# reservations/admin.py
from django.contrib import admin
from .models import Reservation, CheckIn, CheckOut


class CheckInInline(admin.StackedInline):
    model = CheckIn
    extra = 0
    readonly_fields = ('check_in_date',)
    can_delete = False


class CheckOutInline(admin.StackedInline):
    model = CheckOut
    extra = 0
    readonly_fields = ('check_out_date',)
    can_delete = False


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

    inlines = [CheckInInline, CheckOutInline]

    def user_email(self, obj):
        return obj.user.user.email
    user_email.short_description = 'Customer Email'


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'customer', 'room', 'check_in_date')
    search_fields = ('customer__user__email', 'room__title')
    readonly_fields = ('check_in_date',)


@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'customer', 'check_out_date')
    search_fields = ('customer__user__email',)
    readonly_fields = ('check_out_date',)
