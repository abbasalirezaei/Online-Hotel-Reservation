import uuid
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        suffix = uuid.uuid4().hex[:6]  
        defaults = {
            "email": kwargs.get("email", f"user{suffix}@example.com"),
            "phone_number": kwargs.get("phone_number", f"0912{suffix}"),
            "password": kwargs.get("password", "SuperSecure123!"),
            "is_active": True,
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return create_user


@pytest.fixture
def hotel_factory(db, user_factory):
    def create_hotel(**kwargs):
        from hotel.models import Hotel
        defaults = {
            "name": kwargs.get("name", "Test Hotel"),
            "owner": kwargs.get("owner", user_factory()),
        }
        return Hotel.objects.create(**defaults)
    return create_hotel


@pytest.fixture
def admin_user_factory(db):
    def create_admin(**kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        defaults = {
            "email": "admin@example.com",
            "phone_number": "0930" + uuid.uuid4().hex[:6],
            "password": "AdminSecure123!",
            "is_staff": True,
            "is_superuser": True
        }
        defaults.update(kwargs)
        return User.objects.create_superuser(**defaults)
    return create_admin


@pytest.fixture
def hotel_owner_factory(db):
    def create_hotel_owner(**kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        defaults = {
            "email": kwargs.get("email", f"owner{uuid.uuid4().hex[:6]}@hotel.com"),
            "phone_number": f"0912{uuid.uuid4().hex[:6]}",
            "password": "SecureOwner123!",
            "role": "hotel_owner"
        }
        return User.objects.create_user(**defaults)
    return create_hotel_owner