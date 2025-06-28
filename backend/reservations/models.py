from django.db import models
from django.utils import timezone

from hotel.models import Room
from accounts.models import CustomerProfile
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Discount Code")
    discount_percent = models.PositiveIntegerField(verbose_name="Discount Percentage")
    valid_from = models.DateTimeField(verbose_name="Valid From")
    valid_to = models.DateTimeField(verbose_name="Valid To")
    active = models.BooleanField(default=True, verbose_name="Active")

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]

    PAYMENT_METHODS = [
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Awaiting Payment'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

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

    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(blank=True, null=True)
    checkout_date = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name="Cancelled At")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nights = models.PositiveIntegerField(default=1, verbose_name="Nights")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Payment Reference")

    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Coupon Code")

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['room']),
        ]

    def save(self, *args, **kwargs):
        if self.checking_date and self.checkout_date:
            if self.checking_date >= self.checkout_date:
                raise ValueError("Check-in date must be before check-out date.")

            if Reservation.objects.filter(
                room=self.room,
                booking_status__in=['pending', 'confirmed'],
                checking_date__lt=self.checkout_date,
                checkout_date__gt=self.checking_date
            ).exclude(id=self.id).exists():
                raise ValueError("This room is already reserved in the selected date range.")

        if not self.total_price:
            base_price = self.room.price_per_night
            discount = self.coupon.discount_percent if self.coupon and self.coupon.is_valid() else 0
            self.total_price = base_price * self.nights * (1 - discount / 100)
        if self.booking_status == 'cancelled' and not self.cancelled_at:
            self.cancelled_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def calculated_nights(self):
        if self.checking_date and self.checkout_date:
            return (self.checkout_date - self.checking_date).days
        return self.nights

    def __str__(self):
        return f"Reservation - {self.user.user.email} - {self.room.title}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('online', 'Online'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='online')
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ),
        default='pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment for Reservation {self.reservation.id}"


class CheckIn(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='check_in')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)
    check_in_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.email} - CheckIn - {self.room.title}"


class CheckOut(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='check_out')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.email} - CheckOut"
