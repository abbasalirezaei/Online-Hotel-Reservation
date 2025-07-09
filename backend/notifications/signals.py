# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from reviews.models import Review

@receiver(post_save, sender=Review)
def review_or_reply_notification(sender, instance, created, **kwargs):
    if not created:
        return
    
    if instance.parent is None:
        # ✅ ریویوی جدید → مالک هتل
        hotel_owner = instance.hotel.owner
        Notification.objects.create(
            user=hotel_owner,
            message=f"New review submitted by {instance.user.email} for {instance.hotel.name}.",
            notification_type='review_submitted',
            priority='info'
        )
    else:
        # ✅ ریپلای جدید → نویسنده ریویوی اصلی
        original_reviewer = instance.parent.user
        Notification.objects.create(
            user=original_reviewer,
            message=f"{instance.user.email} replied to your review for {instance.hotel.name}.",
            notification_type='reply_submitted',
            priority='info'
        )
