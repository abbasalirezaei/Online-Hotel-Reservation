from django.db import models
from django.utils import timezone
from reservations.models import Reservation
from .enums import PaymentMethod, PaymentStatus


class Payment(models.Model):
    """
    Represents a payment associated with a reservation.
    Tracks amount, payment method, and transaction status.
    """
    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-set paid_at if status is 'paid' and timestamp missing
        if self.status == PaymentStatus.PAID and not self.paid_at:
            self.paid_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for Reservation {self.reservation.id}"
