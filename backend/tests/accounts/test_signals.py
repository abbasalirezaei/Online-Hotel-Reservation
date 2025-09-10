import pytest
from unittest.mock import patch
from apps.accounts.models import HotelOwnerProfile
from apps.accounts.models import CustomerProfile
from .factories import UserFactory

@pytest.mark.django_db
def test_customer_profile_created(customer_user):
    profile = CustomerProfile.objects.filter(user=customer_user).first()
    assert profile is not None


@patch("apps.accounts.tasks.send_activation_email_task.delay")
@pytest.mark.django_db
def test_activation_email_signal_triggered(mock_task):
    user = UserFactory(is_active=False)
    mock_task.assert_called_once_with(user.id, user.email)


@patch("apps.notifications.tasks.send_custom_notification.delay")
@pytest.mark.django_db
def test_notify_owner_verification_signal_triggered(mock_notify, verified_profile):
    verified_profile.is_verified = True
    verified_profile.save()

    mock_notify.assert_called_once_with(
        user_id=verified_profile.user.id,
        message="Your hotel owner request has been approved 🎉 You can now create your hotel.",
        priority="info",
        redirect_url="/hotel-owner-profile/"
    )
