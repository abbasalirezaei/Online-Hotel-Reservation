import pytest
from django.urls import reverse
from django.utils import timezone
from django.test import override_settings
import uuid

# Constants for test data
VALID_REGISTRATION_DATA = {
    "email": lambda: f"user_{uuid.uuid4().hex[:8]}@example.com",
    "password": "StrongPass123",
    "password2": "StrongPass123",
    "phone_number": "09123456789",  # Fixed to a valid phone number format
    "full_name": "Abbas Aku",
}

INVALID_ACTIVATION_CODE = "WRONG1"  # 6-character invalid code
VALID_ACTIVATION_CODE = "ABC123"


@pytest.fixture
def authenticated_client(api_client, customer_user):
    """Fixture to provide an authenticated API client."""
    api_client.force_authenticate(customer_user)
    return api_client


@pytest.mark.django_db
class TestAccountsAPI:
    """Test suite for Accounts API endpoints."""

    def test_user_registration_success(self, api_client):
        """
        Test successful user registration.
        Ensures a new user is created with valid data and returns a 201 status code.
        """
        data = {
            key: value() if callable(value) else value
            for key, value in VALID_REGISTRATION_DATA.items()
        }
        response = api_client.post(reverse("accounts:api_v1:auth_register"), data)
        if response.status_code != 201:
            print(f"Registration failed: {response.data}")  # Debug output
        assert (
            response.status_code == 201
        ), f"Expected 201, got {response.status_code}: {response.data}"
        assert "Account created successfully" in response.data.get("message", "")

    def test_activation_code_success(self, api_client, customer_user):
        """
        Test successful activation code verification.
        Verifies that a valid code activates the user account.
        """
        customer_user.active_code = VALID_ACTIVATION_CODE
        customer_user.active_code_expires_at = timezone.now() + timezone.timedelta(
            minutes=5
        )
        customer_user.is_active = False
        customer_user.save()

        response = api_client.post(
            reverse("accounts:api_v1:verify-activation-code"),
            {"code": VALID_ACTIVATION_CODE},
        )
        assert response.status_code == 200
        customer_user.refresh_from_db()
        assert customer_user.is_active is True

    @override_settings(
        REST_FRAMEWORK={"DEFAULT_THROTTLE_CLASSES": [], "DEFAULT_THROTTLE_RATES": {}}
    )
    def test_activation_code_invalid(self, api_client):
        """
        Test submission of an invalid activation code.
        Ensures a 400 status code and appropriate error message.
        """
        response = api_client.post(
            reverse("accounts:api_v1:verify-activation-code"),
            {"code": INVALID_ACTIVATION_CODE},
        )
        if response.status_code != 400:
            print(f"Invalid code test failed: {response.data}")  # Debug output
        assert response.status_code == 400
        assert "Invalid activation code" in str(response.data)

    @override_settings(
        REST_FRAMEWORK={"DEFAULT_THROTTLE_CLASSES": [], "DEFAULT_THROTTLE_RATES": {}}
    )
    def test_resend_activation_code_success(self, api_client, customer_user):
        """
        Test successful resending of activation code.
        Verifies that a new activation code is sent for an inactive user.
        """
        customer_user.is_active = False
        customer_user.save()

        response = api_client.post(
            reverse("accounts:api_v1:activation-resend"), {"email": customer_user.email}
        )
        assert response.status_code == 200
        assert "Activation code resent successfully" in response.data.get("message", "")

    def test_user_dashboard_view(self, authenticated_client, customer_user):
        """
        Test user dashboard view.
        Ensures authenticated users can access their dashboard with correct data.
        """
        response = authenticated_client.get(reverse("accounts:api_v1:user_dashboard"))
        assert response.status_code == 200
        assert response.data["email"] == customer_user.email

    def test_change_password_success(self, authenticated_client, customer_user):
        """
        Test successful password change.
        Verifies that a valid password change request is processed correctly.
        """
        response = authenticated_client.put(
            reverse("accounts:api_v1:change_password"),
            {
                "current_password": "pass1234",
                "new_password": "NewPass1234",
                "confirm_password": "NewPass1234",
            },
        )
        assert response.status_code == 200
        assert "Password changed successfully" in response.data.get("detail", "")

    def test_change_password_wrong_current(self, authenticated_client, customer_user):
        """
        Test password change with incorrect current password.
        Ensures a 400 status code and appropriate error message.
        """
        response = authenticated_client.put(
            reverse("accounts:api_v1:change_password"),
            {
                "current_password": "wrongpass",
                "new_password": "NewPass1234",
                "confirm_password": "NewPass1234",
            },
        )
        assert response.status_code == 400
        assert "Current password is incorrect" in response.data.get("detail", "")

    def test_change_password_mismatch(self, authenticated_client, customer_user):
        """
        Test password change with mismatched new and confirm passwords.
        Ensures a 400 status code and appropriate error message.
        """
        response = authenticated_client.put(
            reverse("accounts:api_v1:change_password"),
            {
                "current_password": "pass1234",
                "new_password": "NewPass1234",
                "confirm_password": "WrongConfirm",
            },
        )
        assert response.status_code == 400
        assert "do not match" in response.data.get("detail", "")

    def test_customer_profile_view(self, authenticated_client, customer_user):
        """
        Test customer profile view.
        Ensures authenticated customers can access their profile data.
        """
        response = authenticated_client.get(reverse("accounts:api_v1:customer_profile"))
        assert response.status_code == 200
        assert response.data["full_name"] == customer_user.customer_profile.full_name

    def test_customer_can_request_hotel_owner(
        self, authenticated_client, customer_user
    ):
        """
        Test hotel owner request by a customer.
        Verifies that a customer can submit a hotel owner request.
        """
        data = {"company_name": "TestHotel", "business_license_number": "TH123"}
        response = authenticated_client.post(
            reverse("accounts:api_v1:request-hotel-owner"), data
        )
        assert response.status_code == 201
        assert response.data["company_name"] == "TestHotel"

    @pytest.mark.parametrize("user_fixture", ["admin_user", "hotel_owner_user"])
    def test_non_customer_cannot_request_hotel_owner(
        self, api_client, request, user_fixture
    ):
        """
        Test that non-customer users cannot request hotel owner status.
        Ensures a 403 status code for admin and hotel owner users.
        """
        user = request.getfixturevalue(user_fixture)
        api_client.force_authenticate(user)
        response = api_client.post(
            reverse("accounts:api_v1:request-hotel-owner"),
            {"company_name": "FakeHotel", "business_license_number": "FAKE123"},
        )
        assert response.status_code == 403

    def test_unverified_owner_profile_access_denied(
        self, api_client, unverified_profile
    ):
        """
        Test access to hotel owner profile for unverified owners.
        Ensures a 403 status code for unauthorized access.
        """
        api_client.force_authenticate(unverified_profile.user)
        response = api_client.get(reverse("accounts:api_v1:hotel-owner-profile"))
        assert response.status_code == 403

    def test_verified_owner_can_update_profile(self, api_client, verified_profile):
        """
        Test profile update for verified hotel owners.
        Verifies that a verified owner can update their profile data.
        """
        api_client.force_authenticate(verified_profile.user)
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
