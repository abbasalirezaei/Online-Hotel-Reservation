import uuid
import pytest
from django.contrib.auth import get_user_model
from apps.reservations.models import Reservation
from django.utils import timezone

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
        from apps.hotel.models import Hotel
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



@pytest.fixture
def reservation_factory(db, user_factory):
    from apps.reservations.models import Reservation
    from apps.hotel.models import Hotel, Room

    def create_reservation(**kwargs):
        # کاربر
        user = kwargs.get("user", user_factory())
        customer_profile = user.customer_profile

        # مالک هتل
        owner = user_factory(role='HOTEL_OWNER')

        # هتل
        hotel = Hotel.objects.create(
            name=kwargs.get("hotel_name", "Test Hotel"),
            owner=owner,
            description="Test description",
        )

        # اتاق
        room = Room.objects.create(
            hotel=hotel,
            title="Standard Room",
            room_details="A nice standard room",
            price_per_night=100,
            capacity=2,
            is_available=True,
            rating=5,   
        )

        defaults = {
            "user": customer_profile,
            "room": room,
            "nights": kwargs.get("nights", 2),
            "total_price": kwargs.get("total_price", 200),
            "prefered_payment_method": kwargs.get("prefered_payment_method", "PREPAID"),
            "booking_status": kwargs.get("booking_status", "pending"),
            "checking_date": kwargs.get("checking_date", "2025-07-15"),
            "checkout_date": kwargs.get("checkout_date", "2025-07-17"),
        }
        return Reservation.objects.create(**defaults)
    return create_reservation
