import pytest
from rest_framework.test import APIClient
from .factories import UserFactory, HotelOwnerProfileFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user(db, UserFactory):
    """
    یک کاربر عادی با نقش customer می‌سازد.
    """
    return UserFactory(role="customer")

@pytest.fixture
def customer_user():
    return UserFactory(role="customer")


@pytest.fixture
def hotel_owner_user():
    return UserFactory(role="hotel_owner")


@pytest.fixture
def admin_user():
    return UserFactory(role="admin", is_staff=True, is_superuser=True)


@pytest.fixture
def unverified_profile():
    return HotelOwnerProfileFactory(is_verified=False)


@pytest.fixture
def verified_profile():
    return HotelOwnerProfileFactory(is_verified=True)


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {"queues": ["default"]}
