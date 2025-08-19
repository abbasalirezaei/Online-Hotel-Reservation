import pytest
from rest_framework.test import APIRequestFactory
from apps.hotel.api.v1.permissions import IsHotelOwnerOrReadOnly
from apps.hotel.models import Hotel, Room
from apps.hotel.tests.factories import HotelFactory, RoomFactory
from apps.accounts.tests.factories import UserFactory, HotelOwnerProfileFactory


@pytest.mark.django_db
class TestIsHotelOwnerOrReadOnly:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsHotelOwnerOrReadOnly()

    # Read-Only Access
    def test_read_only_access(self):
        hotel = HotelFactory()
        request = self.factory.get('/api/v1/hotels/')
        request.user = UserFactory()
        assert self.permission.has_object_permission(
            request, None, hotel) is True
        assert self.permission.has_permission(request, None) is True

    # Hotel Ownership Checks
    def test_owner_write_access(self):
        hotel = HotelFactory()
        request = self.factory.put('/api/v1/hotels/')
        request.user = hotel.owner
        assert self.permission.has_object_permission(
            request, None, hotel) is True

    def test_non_owner_write_access_denied(self):
        hotel = HotelFactory()
        request = self.factory.put('/api/v1/hotels/')
        request.user = UserFactory()
        assert self.permission.has_object_permission(
            request, None, hotel) is False

    # Hotel Owner Profile Verification (has_permission)
    def test_verified_hotel_owner_has_permission(self):
        profile = HotelOwnerProfileFactory(is_verified=True)
        request = self.factory.post('/api/v1/hotels/')
        request.user = profile.user
        request.user.role = 'hotel_owner'
        assert self.permission.has_permission(request, None) is True

    def test_unverified_hotel_owner_permission_denied(self):
        profile = HotelOwnerProfileFactory(is_verified=False)
        request = self.factory.post('/api/v1/hotels/')
        request.user = profile.user
        request.user.role = 'hotel_owner'
        assert self.permission.has_permission(request, None) is False

    def test_non_owner_role_permission_denied(self):
        user = UserFactory(role='customer')
        request = self.factory.post('/api/v1/hotels/')
        request.user = user
        assert self.permission.has_permission(request, None) is False

    #  Room Ownership Checks
    def test_room_owner_write_access(self):
        room = RoomFactory()
        request = self.factory.put('/api/v1/rooms/')
        request.user = room.hotel.owner
        assert self.permission.has_object_permission(
            request, None, room) is True

    def test_non_room_owner_write_access_denied(self):
        room = RoomFactory()
        request = self.factory.put('/api/v1/rooms/')
        request.user = UserFactory()
        assert self.permission.has_object_permission(
            request, None, room) is False
