from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from reservations.models import BookingStatus

@receiver(post_save, sender=Payment)
def update_reservation_status_on_payment(sender, instance, **kwargs):
    if instance.status == 'paid':
        reservation = instance.reservation
        if reservation.booking_status == BookingStatus.PENDING:
            reservation.booking_status = BookingStatus.CONFIRMED
            reservation.save(update_fields=['booking_status'])
