import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.reservations.models import Reservation, Room, BookingStatus
from apps.accounts.models import CustomerProfile, HotelOwnerProfile
from apps.hotel.tests.factories import HotelFactory, RoomFactory
from apps.accounts.tests.factories import UserFactory
from apps.reservations.tasks import cancel_unpaid_reservation


@pytest.mark.django_db
def test_create_reservation_success():
    client = APIClient()

    owner_user = UserFactory(role="hotel_owner")
    customer_user = UserFactory(role="customer")

    HotelOwnerProfile.objects.create(user=owner_user)
    CustomerProfile.objects.get_or_create(user=customer_user)

    hotel = HotelFactory(owner=owner_user)
    room = RoomFactory(hotel=hotel)

    checking_date = (timezone.now() + timedelta(days=1)).date().isoformat()
    checkout_date = (timezone.now() + timedelta(days=3)).date().isoformat()

    client.force_authenticate(user=customer_user)

    url = reverse("reservations:v1:room-reserve", kwargs={"room_id": room.id})
    data = {
        "checking_date": checking_date,
        "checkout_date": checkout_date,
        "room": room.id,
        "prefered_payment_method": "Prepaid",
        "coupon_code": "",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["room"] == room.id


@pytest.mark.django_db
def test_create_reservation_fails_with_date_conflict():
    client = APIClient()

    owner_user = UserFactory(role="hotel_owner")
    customer_user = UserFactory(role="customer")

    HotelOwnerProfile.objects.create(user=owner_user)
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=customer_user)

    hotel = HotelFactory(owner=owner_user)
    room = RoomFactory(hotel=hotel)

    Reservation.objects.create(
        user=customer_profile,
        room=room,
        checking_date=timezone.make_aware(datetime(2025, 11, 1)),
        checkout_date=timezone.make_aware(datetime(2025, 11, 5)),
        total_price=600,
        prefered_payment_method="Prepaid",
        nights=4,
        booking_status="PENDING",
    )

    client.force_authenticate(user=customer_user)

    url = reverse("reservations:v1:room-reserve", kwargs={"room_id": room.id})
    data = {
        "checking_date": "2025-11-02",
        "checkout_date": "2025-11-04",
        "room": room.id,
        "prefered_payment_method": "Prepaid",
        "coupon_code": "",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not available" in str(response.data)


@pytest.mark.django_db
@patch("core.redis_client.redis_client.lock")
def test_create_reservation_fails_if_lock_cannot_be_acquired(mock_redis_lock):
    client = APIClient()

    owner_user = UserFactory(role="hotel_owner")
    customer_user = UserFactory(role="customer")

    HotelOwnerProfile.objects.create(user=owner_user)
    CustomerProfile.objects.get_or_create(user=customer_user)

    hotel = HotelFactory(owner=owner_user)
    room = RoomFactory(hotel=hotel)

    mock_lock_instance = MagicMock()
    mock_lock_instance.acquire.return_value = False
    mock_redis_lock.return_value = mock_lock_instance

    client.force_authenticate(user=customer_user)

    url = reverse("reservations:v1:room-reserve", kwargs={"room_id": room.id})
    data = {
        "checking_date": "2025-12-10",
        "checkout_date": "2025-12-12",
        "room": room.id,
        "prefered_payment_method": "Postpaid",
        "coupon_code": "",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "currently being booked" in str(response.data)


@pytest.mark.django_db
@patch("core.redis_client.redis_client.lock")
@patch("apps.reservations.models.ReservationManager.is_room_available")
def test_create_reservation_fails_if_room_booked_during_lock(
    mock_is_available, mock_redis_lock
):
    client = APIClient()

    owner_user = UserFactory(role="hotel_owner")
    customer_user = UserFactory(role="customer")
    HotelOwnerProfile.objects.create(user=owner_user)
    CustomerProfile.objects.get_or_create(user=customer_user)

    hotel = HotelFactory(owner=owner_user)
    room = RoomFactory(hotel=hotel)

    mock_lock_instance = MagicMock()
    mock_lock_instance.acquire.return_value = True
    mock_lock_instance.release.return_value = None
    mock_redis_lock.return_value = mock_lock_instance

    mock_is_available.side_effect = [True, False]

    client.force_authenticate(user=customer_user)

    url = reverse("reservations:v1:room-reserve", kwargs={"room_id": room.id})
    data = {
        "checking_date": "2025-12-20",
        "checkout_date": "2025-12-22",
        "room": room.id,
        "prefered_payment_method": "Postpaid",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "has just been booked" in str(response.data)
    assert mock_is_available.call_count == 2


@pytest.mark.django_db
def test_cancel_unpaid_reservation_task_cancels_pending_reservation():
    user = UserFactory(role="customer")
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=user)
    hotel = HotelFactory()
    room = RoomFactory(hotel=hotel)
    reservation = Reservation.objects.create(
        user=customer_profile,
        room=room,
        checking_date=timezone.make_aware(datetime(2025, 12, 1)),
        checkout_date=timezone.make_aware(datetime(2025, 12, 2)),
        total_price=100,
        prefered_payment_method="Prepaid",
        nights=1,
        booking_status=BookingStatus.PENDING,
    )
    cancel_unpaid_reservation(reservation.id)
    reservation.refresh_from_db()
    assert reservation.booking_status == BookingStatus.CANCELLED


@pytest.mark.django_db
def test_cancel_unpaid_reservation_task_does_not_cancel_confirmed():
    user = UserFactory(role="customer")
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=user)
    hotel = HotelFactory()
    room = RoomFactory(hotel=hotel)
    reservation = Reservation.objects.create(
        user=customer_profile,
        room=room,
        checking_date=timezone.make_aware(datetime(2025, 12, 1)),
        checkout_date=timezone.make_aware(datetime(2025, 12, 2)),
        total_price=100,
        prefered_payment_method="Prepaid",
        nights=1,
        booking_status=BookingStatus.CONFIRMED,
    )
    cancel_unpaid_reservation(reservation.id)
    reservation.refresh_from_db()
    assert reservation.booking_status == BookingStatus.CONFIRMED
