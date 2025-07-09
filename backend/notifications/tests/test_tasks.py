import pytest
from notifications.models import Notification
from notifications.tasks import send_custom_notification, send_global_notification

pytestmark = pytest.mark.django_db


def test_send_custom_notification_task(user_factory):
    """✅ Celery task: creates notification for specific user."""
    user = user_factory()
    result = send_custom_notification(user.id, "Hello!", "info", "/profile")
    notif = Notification.objects.get(user=user)
    assert notif.message == "Hello!"
    assert notif.redirect_url == "/profile"
    assert "Notification sent" in result


def test_send_global_notification_task():
    """✅ Celery task: creates global notification."""
    result = send_global_notification("Global promo!", "warning", "/promos")
    notif = Notification.objects.get(is_global=True)
    assert notif.message == "Global promo!"
    assert notif.redirect_url == "/promos"
    assert "Global notification created" in result
