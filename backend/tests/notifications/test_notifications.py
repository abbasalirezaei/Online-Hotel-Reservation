import pytest
from django.test import override_settings
from apps.notifications.models import Notification
from apps.notifications.tasks import send_custom_notification
from ..accounts.factories import HotelOwnerProfileFactory


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_hotel_owner_approval_triggers_notification():
    # Arrange
    profile = HotelOwnerProfileFactory(is_verified=False)
    user = profile.user

    # Act
    profile.is_verified = True
    profile.save()

    send_custom_notification(
        user_id=user.id,
        message="Your hotel owner request has been approved. You can now create your hotel.",
        priority="info",
        redirect_url="/hotel-owner-profile/",
    )

    # Assert
    notifications = Notification.objects.filter(user=user)
    assert notifications.exists()

    notification = notifications.latest("created_at")  # یا .first() اگه ترتیب مهم نیست
    assert "approved" in notification.message.lower()
    assert notification.priority == "info"
    assert notification.redirect_url == "/hotel-owner-profile/"
