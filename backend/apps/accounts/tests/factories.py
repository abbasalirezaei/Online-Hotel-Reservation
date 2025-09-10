import factory
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.accounts.models import HotelOwnerProfile

# -------------------------------
# 🔧 Fixtures
# -------------------------------


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {"queues": ["default"]}


# -------------------------------
# 👤 User Factory
# -------------------------------

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a user with customizable role.
    Default role is 'customer'.
    """

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "pass1234")
    phone_number = factory.Sequence(lambda n: f"091234567{n % 10}")
    role = "customer"
    is_active = True
    is_staff = False
    is_superuser = False


# -------------------------------
# 🏨 Hotel Owner Factory
# -------------------------------


class HotelOwnerProfileFactory(factory.django.DjangoModelFactory):
    """
    Creates a hotel owner .
    Default is unverified. Use is_verified=True for verified profiles.
    """

    class Meta:
        model = HotelOwnerProfile

    user = factory.SubFactory(UserFactory, role="hotel_owner")
    company_name = factory.Faker("company")
    business_license_number = factory.Sequence(lambda n: f"BL-{n}")
    is_verified = False


"""


# Customer user
customer = UserFactory(role="customer")

---------------
# Hotel owner user
owner = UserFactory(role="hotel_owner")

# Unverified hotel owner profile
unverified_profile = HotelOwnerProfileFactory()

# Verified hotel owner profile
verified_profile = HotelOwnerProfileFactory(is_verified=True)

----------------------
# Admin user
admin = UserFactory(role="admin", is_staff=True, is_superuser=True)


"""
