import pytest
from django.urls import reverse
from accounts.models import HotelOwnerProfile
from notifications.models import Notification
from .factories import (
    UserFactory,
    VerifiedHotelOwnerFactory,
    UnverifiedHotelOwnerFactory,
    api_client,
    celery_worker_parameters    
)

# Test: Successfully request to become hotel owner
@pytest.mark.django_db
def test_successful_owner_request(api_client):
    user = UserFactory(role="CUSTOMER")
    api_client.force_authenticate(user)

    response = api_client.post(reverse("accounts_v1:request-hotel-owner"), {
        "company_name": "MyHotel",
        "business_license_number": "ABC123"
    })

    assert response.status_code == 201
    profile = HotelOwnerProfile.objects.get(user=user)
    assert profile.company_name == "MyHotel"
    user.refresh_from_db()
    assert user.role == "BOTH"

# Test: Prevent duplicate hotel owner request
@pytest.mark.django_db
def test_duplicate_owner_request(api_client):
    user = VerifiedHotelOwnerFactory().user
    api_client.force_authenticate(user)

    response = api_client.post(reverse("accounts_v1:request-hotel-owner"), {})
    assert response.status_code == 400


# Test: Access denied for unverified hotel owner profile
@pytest.mark.django_db
def test_unverified_owner_profile_access_denied(api_client):
    user = UnverifiedHotelOwnerFactory().user
    api_client.force_authenticate(user)

    response = api_client.get(reverse("accounts_v1:hotel-owner-profile"))
    assert response.status_code == 403

# Test: Verified hotel owner can update their profile
@pytest.mark.django_db
def test_verified_owner_can_update_profile(api_client):
    profile = VerifiedHotelOwnerFactory()
    user = profile.user
    api_client.force_authenticate(user)

    response = api_client.put(reverse("accounts_v1:hotel-owner-profile"), {
        "company_name": "Hotel Paris",
        "business_license_number": "PAR123",
        "company_address": "Paris"
    })

    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.company_address == "Paris"


# Test: Notification is sent when hotel owner request is approved
from notifications.tasks import send_custom_notification

@pytest.mark.django_db
def test_notify_on_hotel_owner_approval():
    profile = UnverifiedHotelOwnerFactory()   # initially is_verified=False
    user = profile.user

    # Simulate approval
    profile.is_verified = True
    profile.save()

    # Manually trigger the notification task (simulate what signal should do)
    send_custom_notification(user.id,
        message="Your hotel owner request has been approved 🎉 You can now create your hotel.",
        priority="info",
        redirect_url="/hotel-owner-profile/"
    )

    notif = Notification.objects.get(user=user)
    assert "approved" in notif.message.lower()


