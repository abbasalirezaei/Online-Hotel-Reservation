from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string


from apps.accounts.models import HotelOwnerProfile

from apps.notifications.tasks import send_custom_notification
from apps.accounts.tasks import send_activation_email_task
from apps.accounts.exceptions import (
    ActivationCodeError,
    PasswordMismatchError,
    AlreadyHotelOwnerError
)

User = get_user_model()


def validate_activation_code(code):
    """
    Validate the activation code for a user account.
    """
    try:
        user = User.objects.get(active_code=code)
    except User.DoesNotExist:
        raise ActivationCodeError("Invalid activation code.")
    if user.is_active:
        raise ActivationCodeError("Account already activated.")
    if user.active_code_expires_at < timezone.now():
        raise ActivationCodeError("Activation code expired.")
    return user


def resend_activation_code(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ActivationCodeError("No account found with this email.")

    if user.is_active:
        raise ActivationCodeError("Account is already activated.")

    send_activation_email_task.delay(user.id, user.email)
    return user


def send_password_reset_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"http://localhost:3000/password/reset/confirm/?uid={uid}&token={token}"
    subject = 'Reset your password'
    message = render_to_string('registration/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url
    })
    send_mail(subject, message, 'ali@gmail.com', [user.email])
    return uid, token


def change_user_password(user, request, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        raise PasswordMismatchError(
            "New password and confirmation do not match.")

    if not user.check_password(current_password):
        raise PasswordMismatchError("Current password is incorrect.")

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)


def request_hotel_owner(user, validated_data):
    if HotelOwnerProfile.objects.filter(user=user).exists():
        raise AlreadyHotelOwnerError(
            "You have already submitted a hotel owner request.")

    # create hotel owner profile and update user role
    user.role = "hotel_owner"
    user.save(update_fields=["role"])

    profile = HotelOwnerProfile.objects.create(
        user=user, is_verified=False, **validated_data)

    # Send notification to the user
    send_custom_notification.delay(
        user.id,
        message="Your request to become a hotel owner has been submitted. You will be notified once it's reviewed by an admin.",
        priority="info",
        redirect_url="/hotel-owner-profile/"
    )

    return profile
