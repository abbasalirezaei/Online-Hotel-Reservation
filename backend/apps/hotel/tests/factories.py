import factory
from apps.hotel.models import Hotel, Room , HotelLocation
from apps.accounts.tests.factories import UserFactory  
from django.utils.text import slugify
from factory.django import DjangoModelFactory



class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    owner = factory.SubFactory(UserFactory, role='hotel_owner')
    name = factory.Sequence(lambda n: f"Hotel {n}")
    description = "A nice hotel for testing."
    phone_number = "+989123456789"
    email = factory.Sequence(lambda n: f"hotel{n}@example.com")
    website = "https://example.com"
    is_verified = True
    policy = "No smoking. No pets."
    amenities = {"wifi": True, "pool": False}
    has_parking = True


class HotelLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelLocation

    hotel = factory.SubFactory(HotelFactory)
    country = "Iran"
    city = "Shiraz"
    postal_code = "71345"
    address = "123 Test Street"



class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    hotel = factory.SubFactory(HotelFactory)
    room_type = "Deluxe"
    title = factory.Sequence(lambda n: f"Room {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    guests_count = 2
    room_details = "Spacious room with balcony and air conditioning."
    has_balcony = True
    has_air_conditioning = True
    has_tv = True
    pets = False
    price_per_night = 250.00
    capacity = 3
    floor = 2
    is_available = True
    rating = 4
    main_image = factory.django.ImageField(color='blue') 