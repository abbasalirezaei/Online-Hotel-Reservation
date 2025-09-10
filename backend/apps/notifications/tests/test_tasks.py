import pytest
from django.utils import timezone

from apps.notifications.models import Notification
from apps.notifications.tasks import (
    notify_new_booking,
    notify_booking_cancelled,
    remind_checkin,
    notify_checked_in,
    notify_checked_out,
    send_custom_notification,
    send_global_notification,
)

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


@pytest.mark.django_db
def test_notify_new_booking(reservation_factory):
    """✅ Notify hotel owner on new booking."""
    reservation = reservation_factory()
    notify_new_booking(reservation.id)
    notif = Notification.objects.get(user=reservation.room.hotel.owner)
    assert "new booking" in notif.message
    assert reservation.room.hotel.name in notif.message
    assert reservation.user.user.email in notif.message


@pytest.mark.django_db
def test_notify_booking_cancelled(reservation_factory):
    """✅ Notify hotel owner when booking cancelled."""
    reservation = reservation_factory()
    notify_booking_cancelled(reservation.id)
    notif = Notification.objects.get(user=reservation.room.hotel.owner)
    assert "cancelled" in notif.message
    assert f"Booking #{reservation.id}" in notif.message


@pytest.mark.django_db
def test_remind_checkin(reservation_factory):
    """✅ Remind guest for check-in."""
    reservation = reservation_factory()
    remind_checkin(reservation.id)
    notif = Notification.objects.get(user=reservation.user.user)
    assert "check-in" in notif.message
    assert reservation.room.hotel.name in notif.message


@pytest.mark.django_db
def test_notify_checked_in(reservation_factory):
    """✅ Notify hotel owner when guest checked in."""
    reservation = reservation_factory()
    notify_checked_in(reservation.id)
    notif = Notification.objects.get(user=reservation.room.hotel.owner)
    assert "checked in" in notif.message
    assert reservation.user.user.email in notif.message


@pytest.mark.django_db
def test_notify_checked_out(reservation_factory):
    """✅ Notify hotel owner when guest checked out."""
    reservation = reservation_factory()
    notify_checked_out(reservation.id)
    notif = Notification.objects.get(user=reservation.room.hotel.owner)
    assert "checked out" in notif.message
    assert reservation.user.user.email in notif.message
