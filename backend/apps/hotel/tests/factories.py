import factory
from apps.hotel.models import Hotel, Room, HotelLocation, Amenity, HotelImage, RoomImage
from apps.accounts.tests.factories import UserFactory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

class AmenityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Amenity

    name = factory.Sequence(lambda n: f"Amenity {n}")
    description = "A useful amenity for testing."


class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    owner = factory.SubFactory(UserFactory, role='hotel_owner')
    name = factory.Sequence(lambda n: f"Hotel {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = "A nice hotel for testing."
    phone_number = "+989123456789"
    email = factory.Sequence(lambda n: f"hotel{n}@example.com")
    website = "https://example.com"
    is_verified = True
    policy = "No smoking. No pets."
    has_parking = True

    @factory.post_generation
    def amenities(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.amenities.set(extracted)


class HotelLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelLocation

    hotel = factory.SubFactory(HotelFactory)
    country = "Iran"
    city = "Shiraz"
    postal_code = "71345"
    address = "123 Test Street"


class HotelImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelImage

    hotel = factory.SubFactory(HotelFactory)
    image = factory.django.ImageField(color='blue')
    caption = factory.Sequence(lambda n: f"Image {n}")


class RoomFactory(factory.django.DjangoModelFactory):
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


class RoomImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoomImage

    room = factory.SubFactory(RoomFactory)
    image = factory.django.ImageField(color='red')
    caption = factory.Sequence(lambda n: f"Room Image {n}")



"""
Usage:
from apps.hotel.tests.factories import HotelFactory, RoomFactory, AmenityFactory
# Create a hotel instance
hotel = HotelFactory()
# Create a room instance associated with the hotel
room = RoomFactory(hotel=hotel)
# Create an amenity instance
amenity = AmenityFactory()
# Associate the amenity with the hotel
hotel.amenities.add(amenity)
# Create a hotel location instance
hotel_location = HotelLocationFactory(hotel=hotel)
# Create hotel images
hotel_image = HotelImageFactory(hotel=hotel)
# Create room images
room_image = RoomImageFactory(room=room)

"""