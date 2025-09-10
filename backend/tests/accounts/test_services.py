import pytest
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from apps.accounts.services import (
    validate_activation_code,
    resend_activation_code,
    send_password_reset_email,
    change_user_password,
    request_hotel_owner
)

from apps.accounts.exceptions import (
    ActivationCodeError,
    PasswordMismatchError,
    AlreadyHotelOwnerError
)
from apps.accounts.models import HotelOwnerProfile


#  validate_activation_code
@pytest.mark.django_db
def test_validate_activation_code_success(customer_user):
    customer_user.active_code = "ABC123"
    customer_user.active_code_expires_at = timezone.now() + timezone.timedelta(minutes=10)
    customer_user.is_active = False
    customer_user.save()

    user = validate_activation_code("ABC123")
    assert user == customer_user


@pytest.mark.django_db
def test_validate_activation_code_invalid():
    with pytest.raises(ActivationCodeError, match="Invalid activation code."):
        validate_activation_code("WRONGCODE")


@pytest.mark.django_db
def test_validate_activation_code_expired(customer_user):
    customer_user.active_code = "EXPIRED"
    customer_user.active_code_expires_at = timezone.now() - timezone.timedelta(minutes=1)
    customer_user.is_active = False
    customer_user.save()

    with pytest.raises(ActivationCodeError, match="Activation code expired."):
        validate_activation_code("EXPIRED")


@pytest.mark.django_db
def test_validate_activation_code_already_active(customer_user):
    customer_user.active_code = "ACTIVE"
    customer_user.active_code_expires_at = timezone.now() + timezone.timedelta(minutes=10)
    customer_user.is_active = True
    customer_user.save()

    with pytest.raises(ActivationCodeError, match="Account already activated."):
        validate_activation_code("ACTIVE")


# resend_activation_code
@pytest.mark.django_db
def test_resend_activation_code_success(customer_user):
    customer_user.is_active = False
    customer_user.save()
    user = resend_activation_code(customer_user.email)
    assert user == customer_user


@pytest.mark.django_db
def test_resend_activation_code_user_not_found():
    with pytest.raises(ActivationCodeError, match="No account found with this email."):
        resend_activation_code("notfound@example.com")


@pytest.mark.django_db
def test_resend_activation_code_already_active(customer_user):
    customer_user.is_active = True
    customer_user.save()
    with pytest.raises(ActivationCodeError, match="Account is already activated."):
        resend_activation_code(customer_user.email)


#  send_password_reset_email
@pytest.mark.django_db
def test_send_password_reset_email(customer_user):
    uid, token = send_password_reset_email(customer_user)
    decoded_uid = urlsafe_base64_decode(uid).decode()
    assert str(customer_user.id) == decoded_uid
    assert default_token_generator.check_token(customer_user, token)


#  change_user_password
@pytest.mark.django_db
def test_change_user_password_success(client, customer_user):
    client.force_login(customer_user)
    request = client.post("/fake-url/").wsgi_request

    change_user_password(customer_user, request, "pass1234", "newpass", "newpass")
    assert customer_user.check_password("newpass")

@pytest.mark.django_db
def test_change_user_password_mismatch(customer_user, rf):
    request = rf.post("/fake-url/")
    with pytest.raises(PasswordMismatchError, match="do not match"):
        change_user_password(customer_user, request, "pass1234", "newpass", "wrongconfirm")


@pytest.mark.django_db
def test_change_user_password_wrong_current(customer_user, rf):
    request = rf.post("/fake-url/")
    with pytest.raises(PasswordMismatchError, match="Current password is incorrect."):
        change_user_password(customer_user, request, "wrongpass", "newpass", "newpass")


#  request_hotel_owner
@pytest.mark.django_db
def test_request_hotel_owner_success(customer_user):
    data = {
        "company_name": "TestHotel",
        "business_license_number": "TH123"
    }
    profile = request_hotel_owner(customer_user, data)
    assert profile.user == customer_user
    assert profile.company_name == "TestHotel"
    assert customer_user.role == "hotel_owner"


@pytest.mark.django_db
def test_request_hotel_owner_already_exists(verified_profile):
    user = verified_profile.user
    data = {
        "company_name": "DuplicateHotel",
        "business_license_number": "DUP123"
    }
    with pytest.raises(AlreadyHotelOwnerError):
        request_hotel_owner(user, data)
