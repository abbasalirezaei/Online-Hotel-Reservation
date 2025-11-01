import factory
from factory.django import DjangoModelFactory
from django.utils.text import slugify

from apps.hotel.models import Hotel, Amenity, HotelLocation, HotelImage, Room, RoomImage
from tests.accounts.factories import UserFactory


class AmenityFactory(DjangoModelFactory):
    class Meta:
        model = Amenity

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class HotelFactory(DjangoModelFactory):
    class Meta:
        model = Hotel

    owner = factory.SubFactory(UserFactory, role="hotel_owner")
    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    website = factory.Faker("url")
    is_verified = True
    policy = factory.Faker("sentence")

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class HotelLocationFactory(DjangoModelFactory):
    class Meta:
        model = HotelLocation

    hotel = factory.SubFactory(HotelFactory)
    country = factory.Faker("country")
    city = factory.Faker("city")
    postal_code = factory.Faker("postcode")
    address = factory.Faker("address")


class HotelImageFactory(DjangoModelFactory):
    class Meta:
        model = HotelImage

    hotel = factory.SubFactory(HotelFactory)
    image = factory.django.ImageField(color="blue")
    caption = factory.Faker("sentence")


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    hotel = factory.SubFactory(HotelFactory)
    room_type = "Single"
    title = factory.Faker("catch_phrase")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    guests_count = 2
    room_details = factory.Faker("paragraph")
    price_per_night = "100.00"
    capacity = 2
    floor = 1
    rating = 4
    main_image = factory.django.ImageField(color="red")


class RoomImageFactory(DjangoModelFactory):
    class Meta:
        model = RoomImage

    room = factory.SubFactory(RoomFactory)
    image = factory.django.ImageField(color="green")
    caption = factory.Faker("sentence")
