import pytest
from django.urls import reverse
from apps.accounts.models import HotelOwnerProfile
from apps.notifications.models import Notification
from apps.notifications.tasks import send_custom_notification
from .factories import (
    UserFactory,
    HotelOwnerProfileFactory,
    api_client,
    celery_worker_parameters,
)


# 1. Request Submission Tests


# @pytest.mark.django_db
# def test_successful_owner_request(api_client):
#     user = UserFactory(role="customer")
#     api_client.force_authenticate(user)

#     response = api_client.post(reverse("accounts:api_v1:request-hotel-owner"), {
#         "company_name": "MyHotel",
#         "business_license_number": "ABC123"
#     })

#     assert response.status_code == 201
#     profile = HotelOwnerProfile.objects.get(user=user)
#     assert profile.company_name == "MyHotel"
#     assert profile.is_verified is False
#     user.refresh_from_db()
#     assert user.role == "customer"


@pytest.mark.django_db
def test_duplicate_owner_request(api_client):
    profile = HotelOwnerProfileFactory(is_verified=True)
    user = profile.user
    api_client.force_authenticate(user)

    response = api_client.post(
        reverse("accounts:api_v1:request-hotel-owner"),
        {"company_name": "DuplicateHotel", "business_license_number": "DUP123"},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_request_missing_required_fields(api_client):
    user = UserFactory(role="customer")
    api_client.force_authenticate(user)

    response = api_client.post(
        reverse("accounts:api_v1:request-hotel-owner"), {}
    )  # Empty payload

    assert response.status_code == 400
    assert "company_name" in response.data or "business_license_number" in response.data


# Permission & Access Control Tests


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "hotel_owner"])
def test_non_customer_cannot_request_hotel_owner(api_client, role):
    user = UserFactory(role=role)
    api_client.force_authenticate(user)

    response = api_client.post(
        reverse("accounts:api_v1:request-hotel-owner"),
        {"company_name": "FakeHotel", "business_license_number": "FAKE123"},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_unverified_owner_profile_access_denied(api_client):
    profile = HotelOwnerProfileFactory(is_verified=False)
    user = profile.user
    api_client.force_authenticate(user)

    response = api_client.get(reverse("accounts:api_v1:hotel-owner-profile"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_verified_owner_can_update_profile(api_client):
    profile = HotelOwnerProfileFactory(is_verified=True)
    user = profile.user
    api_client.force_authenticate(user)

    response = api_client.put(
        reverse("accounts:api_v1:hotel-owner-profile"),
        {
            "company_name": "Hotel Paris",
            "business_license_number": "PAR123",
            "company_address": "Paris",
        },
    )

    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.company_address == "Paris"


#  Notification Tests


@pytest.mark.django_db
def test_notify_on_hotel_owner_approval():
    profile = HotelOwnerProfileFactory(is_verified=False)
    user = profile.user

    profile.is_verified = True
    profile.save()

    send_custom_notification(
        user.id,
        message="Your hotel owner request has been approved  You can now create your hotel.",
        priority="info",
        redirect_url="/hotel-owner-profile/",
    )

    notif = Notification.objects.get(user=user)
    assert "approved" in notif.message.lower()


#  Role Integrity Test


# @pytest.mark.django_db
# def test_role_not_changed_on_request(api_client):
#     user = UserFactory(role="customer")
#     api_client.force_authenticate(user)

#     response = api_client.post(reverse("accounts:api_v1:request-hotel-owner"), {
#         "company_name": "RoleTestHotel",
#         "business_license_number": "ROLE123"
#     })

#     assert response.status_code == 201
#     user.refresh_from_db()
#     assert user.role == "customer"
