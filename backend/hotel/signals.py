from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Booking




@receiver(pre_save, sender=Booking)
def set_cancelled_at(sender, instance, **kwargs):
    if not instance.pk:
        # Booking new instance
        return

    try:
        previous = Booking.objects.get(pk=instance.pk)
    except Booking.DoesNotExist:
        return

    if previous.booking_status != 'cancelled' and instance.booking_status == 'cancelled':
        instance.cancelled_at = timezone.now()




@receiver(pre_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, **kwargs):
    if not instance.pk:
        return   # Booking new instance

    try:
        previous = Booking.objects.get(pk=instance.pk)
    except Booking.DoesNotExist:
        return

    # If booking status changed from pending to confirmed:
    if previous.booking_status != 'confirmed' and instance.booking_status == 'confirmed':
        subject = 'تأیید رزرو شما'
        message = f"""
        {instance.customer.first_name} عزیز،

        رزرو شما برای اتاق {instance.room.title} با موفقیت تأیید شد.
        تاریخ ورود: {instance.checking_date}
        تاریخ خروج: {instance.checkout_date}
        تعداد مهمان: {instance.guests_count}
        مبلغ کل: {instance.total_price} تومان

        با تشکر از انتخاب شما.
        """
        recipient_email = instance.email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

