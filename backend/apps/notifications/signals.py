from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.notifications.models import Notification
from apps.reviews.models import Review
from apps.reservations.models import Reservation
from apps.accounts.models import HotelOwnerProfile
from apps.notifications.tasks import (
    notify_new_booking,
    notify_booking_cancelled,
    remind_checkin,
    notify_checked_in,
    notify_checked_out,
    send_custom_notification    
)


@receiver(post_save, sender=Reservation)
def handle_reservation_created_or_updated(sender, instance, created, **kwargs):
    if created:
        # new booking
        notify_new_booking.delay(instance.id)
    else:
        # booking updated, check status
        if instance.booking_status == 'checked_in':
            notify_checked_in.delay(instance.id)
        elif instance.booking_status == 'checked_out':
            notify_checked_out.delay(instance.id)


@receiver(post_delete, sender=Reservation)
def handle_reservation_deleted(sender, instance, **kwargs):
    # booking cancelled
    notify_booking_cancelled.delay(instance.id)


@receiver(post_save, sender=Review)
def review_or_reply_notification(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.parent is None:
        # ✅ New review → Notify hotel owner
        hotel_owner = instance.hotel.owner
        Notification.objects.create(
            user=hotel_owner,
            message=f"New review submitted by {instance.user.email} for {instance.hotel.name}.",
            notification_type='review_submitted',
            priority='info'
        )
    else:
        # ✅ New reply → Notify original reviewer
        original_reviewer = instance.parent.user
        Notification.objects.create(
            user=original_reviewer,
            message=f"{instance.user.email} replied to your review for {instance.hotel.name}.",
            notification_type='reply_submitted',
            priority='info'
        )


