from django.db.models.signals import post_save
from django.dispatch import receiver

# local imports
# from .models import User, Customer


# @receiver(post_save, sender=User)
# def create_user_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
