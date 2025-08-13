
import factory
from django.contrib.auth import get_user_model
from apps.accounts.models import HotelOwnerProfile

import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='session')
def celery_worker_parameters():
    return {"queues": ["default"]}


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'pass1234')
    phone_number = factory.Sequence(lambda n: f"091234567{n % 10}")
    role = "CUSTOMER"
    is_active = True


class VerifiedHotelOwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelOwnerProfile

    user = factory.SubFactory(UserFactory, role="BOTH")
    company_name = factory.Faker("company")
    business_license_number = factory.Sequence(lambda n: f"VR-{n}")
    is_verified = True


class UnverifiedHotelOwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelOwnerProfile

    user = factory.SubFactory(UserFactory, role="BOTH")
    company_name = factory.Faker("company")
    business_license_number = factory.Sequence(lambda n: f"UN-{n}")
    is_verified = False