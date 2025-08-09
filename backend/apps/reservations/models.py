from django.db import models
from django.utils import timezone

from hotel.models import Room
from accounts.models import CustomerProfile
from discount.models import Coupon
from decimal import Decimal
class BookingStatus(models.TextChoices):
    """Enumeration for the reservation status."""
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'




class PreferedPaymentStatus(models.TextChoices):
    """User preference for when to pay."""
    PREPAID = 'Prepaid', 'Prepaid'
    POSTPAID = 'Postpaid', 'Postpaid'


class Reservation(models.Model):
    """
    Represents a room reservation made by a customer.
    Includes payment method, pricing, status, and optional coupon.
    """
    user = models.ForeignKey(
        CustomerProfile,
        related_name="reservations",
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room,
        related_name="reservations",
        on_delete=models.CASCADE
    )

    room_number = models.IntegerField(null=True, blank=True)

    # Key dates
    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name="Cancelled At")
    updated_at = models.DateTimeField(auto_now=True)

    # Pricing
    nights = models.PositiveIntegerField(default=1, verbose_name="Nights")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Coupon Code")

    # Status fields
    prefered_payment_method = models.CharField(max_length=10, choices=PreferedPaymentStatus.choices, default=PreferedPaymentStatus.PREPAID)
    booking_status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['room']),
        ]

    def save(self, *args, **kwargs):
        if self.booking_status == BookingStatus.CANCELLED and not self.cancelled_at:
            self.cancelled_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def calculated_nights(self):
        """Dynamically calculate the number of nights from check-in/check-out."""
        if self.checking_date and self.checkout_date:
            return (self.checkout_date - self.checking_date).days
        return self.nights

    def __str__(self):
        return f"Reservation - {self.user.user.email} - {self.room.title}"


class CheckIn(models.Model):
    """
    Represents the check-in event for a reservation.
    Automatically updates the reservation's checking_date.
    """
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='check_in')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)
    check_in_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.reservation.checking_date = self.check_in_date
        self.reservation.save(update_fields=['checking_date'])

    def __str__(self):
        return f"{self.customer.user.email} - CheckIn - {self.room.title}"


class CheckOut(models.Model):
    """
    Represents the check-out event for a reservation.
    Automatically updates the reservation's checkout_date.
    """
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='check_out')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.reservation.checkout_date = self.check_out_date
        self.reservation.save(update_fields=['checkout_date'])

    def __str__(self):
        return f"{self.customer.user.email} - CheckOut"