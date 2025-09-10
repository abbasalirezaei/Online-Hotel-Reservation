# import pytest
# from django.urls import reverse
# from apps.accounts.models import HotelOwnerProfile
# from .factories import UserFactory, api_client


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


# @pytest.mark.django_db
# def test_request_missing_required_fields(api_client):
#     user = UserFactory(role="customer")
#     api_client.force_authenticate(user)

#     response = api_client.post(
#         reverse("accounts:api_v1:request-hotel-owner"), {})
#     assert response.status_code == 400
#     assert "company_name" in response.data or "business_license_number" in response.data
