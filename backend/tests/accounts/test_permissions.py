import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture", ["admin_user", "hotel_owner_user"])
def test_non_customer_cannot_request_hotel_owner(api_client, request, user_fixture):
    user = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user)

    response = api_client.post(
        reverse("accounts:api_v1:request-hotel-owner"),
        {"company_name": "FakeHotel", "business_license_number": "FAKE123"},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_unverified_owner_profile_access_denied(api_client, unverified_profile):
    user = unverified_profile.user
    api_client.force_authenticate(user)

    response = api_client.get(reverse("accounts:api_v1:hotel-owner-profile"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_verified_owner_can_update_profile(api_client, verified_profile):
    user = verified_profile.user
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
    verified_profile.refresh_from_db()
    assert verified_profile.company_address == "Paris"
