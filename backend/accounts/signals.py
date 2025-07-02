from django.db.models.signals import post_save
from django.dispatch import receiver


from accounts.tasks import send_activation_email_task
# local imports
from .models import User, CustomerProfile


@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_activation_email_signal(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_activation_email_task.delay(instance.id, instance.email)