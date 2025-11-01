import pytest
from .hotel_factories import (
    HotelFactory,
    AmenityFactory,
    HotelLocationFactory,
    HotelImageFactory,
    RoomFactory,
    RoomImageFactory,
)


@pytest.fixture
def hotel(db):
    hotel = HotelFactory()
    HotelLocationFactory(hotel=hotel)   # <-- ensure location exists
    return hotel


@pytest.fixture
def verified_hotel(db):
    hotel = HotelFactory(is_verified=True)
    HotelLocationFactory(hotel=hotel)
    return hotel


@pytest.fixture
def unverified_hotel(db):
    hotel = HotelFactory(is_verified=False)
    HotelLocationFactory(hotel=hotel)
    return hotel


@pytest.fixture
def hotel_with_location(db):
    hotel = HotelFactory()
    HotelLocationFactory(hotel=hotel)
    return hotel

@pytest.fixture
def hotel_with_images(db):
    hotel = HotelFactory()
    HotelImageFactory.create_batch(3, hotel=hotel)
    return hotel


@pytest.fixture
def hotel_with_rooms(db):
    hotel = HotelFactory()
    RoomFactory.create_batch(2, hotel=hotel)
    return hotel


@pytest.fixture
def amenity(db):
    return AmenityFactory()
