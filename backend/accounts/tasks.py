import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
logger = logging.getLogger(__name__)

@shared_task
def send_activation_email_task(user_id, email):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} not found for email activation.")
        return False

    code = get_random_string(length=6, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    user.active_code = code
    user.active_code_expires_at = timezone.now() + timedelta(minutes=2)
    user.save(update_fields=['active_code', 'active_code_expires_at'])

    context = {
        "code": code,
        "user": user,
        "activation_link": f"http://localhost:8000/accounts/api/v1/activate/{code}/"
    }
    subject = "Activate Your Account"
    from_email="no-reply@hotel.com"
    to_email = [email]

    text_content = f"Your activation code is: {code}"
    html_content = render_to_string("email/activation_email.html", context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        return True
    except Exception as e:
        logger.error(f"Failed to send activation email to {email}: {str(e)}")
        return False