from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Hotel
from django.core.cache import cache
from apps.notifications.tasks import send_custom_notification


@receiver([post_save, post_delete], sender=Hotel)
def invalidate_hotel_cache(sender, instance, **kwargs):
    """
    Invalidate hotel list caches when a hotel is created, updated, or deleted
    """
    print("Clearing hotel cache")

    # Clear hotel list caches
    cache.delete_pattern("*hotel_list*")


@receiver(pre_save, sender=Hotel)
def store_previous_is_verified(sender, instance, **kwargs):
    """
    Store the previous 'is_verified' state before saving, so we can compare after save.
    """
    if instance.pk:
        try:
            previous = Hotel.objects.get(pk=instance.pk)
            instance._previous_is_verified = previous.is_verified
        except Hotel.DoesNotExist:
            instance._previous_is_verified = None
    else:
        # New hotel creation
        instance._previous_is_verified = None


@receiver(post_save, sender=Hotel)
def notify_owner_on_verification(sender, instance, created, **kwargs):
    """
    Send a notification to the hotel owner when their hotel gets verified.
    """
    if not created:
        prev_status = getattr(instance, "_previous_is_verified", None)
        # Check if changed from False to True
        if prev_status is False and instance.is_verified is True:
            send_custom_notification.delay(
                instance.owner.id,
                message=f"Your hotel '{instance.name}' has been verified!",
                priority="success",
                redirect_url=f"/hotels/{instance.id}/",
            )
