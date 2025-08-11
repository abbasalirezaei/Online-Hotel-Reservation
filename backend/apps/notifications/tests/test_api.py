import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.notifications.models import Notification
from apps.notifications.tasks import send_custom_notification, send_global_notification

pytestmark = pytest.mark.django_db

def test_send_custom_notification_success(hotel_owner_factory, user_factory):
    owner = hotel_owner_factory()
    target_user = user_factory()

    # Directly call the task instead of delay()
    send_custom_notification(target_user.id, "Special offer for you!", "info", "/offers")

    assert Notification.objects.filter(user=target_user, message="Special offer for you!").exists()


def test_send_global_notification_success(hotel_owner_factory):
    owner = hotel_owner_factory()

    send_global_notification("Big discount for all users!", "warning", "/discounts")

    assert Notification.objects.filter(is_global=True, message="Big discount for all users!").exists()


def test_anonymous_cannot_send_custom_notification(user_factory):
    target_user = user_factory()
    client = APIClient()
    url = reverse('notifications:send-custom-notification')

    payload = {
        "user_id": target_user.id,
        "message": "Hello!"
    }

    response = client.post(url, data=payload, format='json')

    assert response.status_code == 401  # anonymous user gets 401


def test_anonymous_cannot_send_global_notification():
    client = APIClient()
    url = reverse('notifications:send-global-notification')

    payload = {
        "message": "Hello everyone!"
    }

    response = client.post(url, data=payload, format='json')

    assert response.status_code == 401
