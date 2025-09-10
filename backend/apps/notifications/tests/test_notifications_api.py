import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.notifications.models import Notification

pytestmark = pytest.mark.django_db


def create_notification(user, is_global=False):
    return Notification.objects.create(
        user=None if is_global else user,
        message="Test Notification",
        notification_type="custom",
        priority="info",
        is_global=is_global,
    )


def test_user_can_list_their_notifications(user_factory):
    """✅ Should list personal + global notifications."""
    user = user_factory()
    global_notif = create_notification(user=None, is_global=True)
    user_notif = create_notification(user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("notifications:list-notifications")  # Updated namespace
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    messages = [n["message"] for n in response.data]
    assert "Test Notification" in messages


def test_unauthenticated_user_cannot_list_notifications():
    """✅ Should return 401 for anonymous users."""
    client = APIClient()
    url = reverse("notifications:list-notifications")  # Updated namespace
    response = client.get(url)
    assert response.status_code == 401


def test_user_can_mark_notification_as_read(user_factory):
    """✅ Should mark a single notification as read."""
    user = user_factory()
    notif = create_notification(user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse(
        "notifications:mark-read-notification", args=[notif.id]
    )  # Updated namespace
    response = client.post(url)

    notif.refresh_from_db()
    assert response.status_code == 200
    assert notif.is_read is True


def test_user_cannot_mark_other_users_notification(user_factory):
    """✅ Should not allow marking other users' notifications."""
    user1 = user_factory()
    user2 = user_factory()
    notif = create_notification(user=user1)

    client = APIClient()
    client.force_authenticate(user=user2)

    url = reverse(
        "notifications:mark-read-notification", args=[notif.id]
    )  # Updated namespace
    response = client.post(url)

    assert response.status_code == 404
    notif.refresh_from_db()
    assert notif.is_read is False
