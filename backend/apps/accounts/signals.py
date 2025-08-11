from django.db.models.signals import post_save
from django.dispatch import receiver


# local imports
from apps.accounts.tasks import send_activation_email_task
from .models import User, CustomerProfile
from apps.accounts.models import HotelOwnerProfile
from apps.notifications.tasks import send_custom_notification    

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_activation_email_signal(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_activation_email_task.delay(instance.id, instance.email)


@receiver(post_save, sender=HotelOwnerProfile)
def notify_owner_verification(sender, instance, created, **kwargs):
    if not created and instance.is_verified:
        send_custom_notification.delay(
            user_id=instance.user.id,
            message="Your hotel owner request has been approved 🎉 You can now create your hotel.",
            priority="info",
            redirect_url="/hotel-owner-profile/"
        )
