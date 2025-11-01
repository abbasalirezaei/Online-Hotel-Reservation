from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError 

from apps.hotel.models import Room
from apps.accounts.models import CustomerProfile
from apps.discount.models import Coupon

class BookingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    CHECKED_IN = "checked_in", "Checked In"
    CHECKED_OUT = "checked_out", "Checked Out"


class PreferredPaymentStatus(models.TextChoices):
    """User preference for when to pay."""

    PREPAID = "Prepaid", "Prepaid"
    POSTPAID = "Postpaid", "Postpaid"


class ReservationManager(models.Manager):
    def is_room_available(self, room_id, checkin_date, checkout_date):
        """
        Checks if a room is available for a given date range by looking for conflicting bookings.
        A conflict exists if the requested date range overlaps with any existing, non-cancelled booking.
        """
        conflicting_bookings = (
            self.filter(room_id=room_id)
            .exclude(booking_status=BookingStatus.CANCELLED)
            .filter(
                # An existing booking starts before the new one would end
                checking_date__lt=checkout_date,
                # AND the existing booking ends after the new one would start
                checkout_date__gt=checkin_date,
            )
        )

        # If the queryset is empty (no conflicts found), the room is available.
        return not conflicting_bookings.exists()


class Reservation(models.Model):
    """
    Represents a room reservation made by a customer.
    Includes payment method, pricing, status, and optional coupon.
    """

    user = models.ForeignKey(
        CustomerProfile, related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room, related_name="reservations", on_delete=models.CASCADE
    )

    # Key dates
    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Cancelled At"
    )
    updated_at = models.DateTimeField(auto_now=True)

    # Pricing
    nights = models.PositiveIntegerField(default=1, verbose_name="Nights")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Price"
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Coupon Code",
    )

    # Status fields
    prefered_payment_method = models.CharField(
        max_length=25,
        choices=PreferredPaymentStatus.choices,
        default=PreferredPaymentStatus.PREPAID,
    )
    booking_status = models.CharField(
        max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING
    )

    # custom manager
    objects = ReservationManager()

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["room"]),
            models.Index(fields=["booking_status"]),
            models.Index(fields=["checking_date", "checkout_date"]),
        ]

    def clean(self):
        """
        Adds model-level validation to ensure business rules are enforced
        even outside of serializers (e.g., in Django Admin).
        """
        super().clean()
        if self.checking_date and self.checkout_date:
            if self.checking_date >= self.checkout_date:
                raise ValidationError(
                    "Check-in date must be before check-out date."
                )

    def save(self, *args, **kwargs):
        self.clean()
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
    Automatically updates the reservation's booking_status.
    """

    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name="check_in"
    )
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)
    
    check_in_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if (
            self.reservation.booking_status == BookingStatus.CONFIRMED
            or self.reservation.booking_status == BookingStatus.PENDING
        ):
            self.reservation.booking_status = BookingStatus.CHECKED_IN
            self.reservation.save(update_fields=["booking_status"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.email} - CheckIn - {self.room.title}"


class CheckOut(models.Model):
    """
    Represents the check-out event for a reservation.
    Automatically updates the reservation's booking_status and checkout_date.
    """

    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name="check_out"
    )
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    
    check_out_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.reservation.booking_status == BookingStatus.CHECKED_IN:
            self.reservation.booking_status = BookingStatus.CHECKED_OUT
            self.reservation.checkout_date = self.check_out_date
            self.reservation.save(update_fields=["booking_status", "checkout_date"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.email} - CheckOut"