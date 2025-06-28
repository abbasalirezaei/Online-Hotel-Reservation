from rest_framework import serializers

from django.utils.text import slugify
from django.db import transaction

from hotel.models.hotel_model import Hotel, HotelLocation, HotelImage
from hotel.models.room_model import Room, RoomImage
from accounts.models import User

# ----------- Hotel Image -----------


class HotelImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'image_url', 'caption']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_hotel(self, hotel):
        request = self.context.get("request")
        if hotel.owner != request.user:
            raise serializers.ValidationError(
                "شما مجاز به افزودن تصویر برای این هتل نیستید.")
        return hotel

# ----------- Hotel Location  -----------


class HotelLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocation
        fields = ['id', 'hotel', 'country', 'city', 'postal_code', 'address']
        read_only_fields = ['hotel',]

    def validate_hotel(self, hotel):
        request = self.context.get("request")
        if hotel.owner != request.user:
            raise serializers.ValidationError(
                "شما مجاز به افزودن آدرس برای این هتل نیستید.")
        return hotel


class HotelListSerializer(serializers.ModelSerializer):
    # location = HotelLocationSerializer()
    images = HotelImageSerializer(many=True)

    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.SerializerMethodField()

    class Meta:
        model = Hotel

        fields = [
            'id', 'owner', 'name',  'rating',
            'images', 'room_count'
        ]
        read_only_fields = ["owner",]

    def get_room_count(self, obj):
        return obj.rooms.count()
# ----------- Hotel Create -----------


class HotelCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True)

    class Meta:
        model = Hotel
        fields = ['name',
                  'phone_number',
                  'email',
                  'website',
                  'main_image',
                  'has_parking',
                  'policy',
                  'amenities',
                  'description',
                  "uploaded_images"
                  ]

    def create(self, validated_data):

        ploaded_images = validated_data.pop("uploaded_images")
        user = self.context['request'].user
        with transaction.atomic():
            hotel = Hotel.objects.create(owner=user, **validated_data)

            for image_data in ploaded_images:
                HotelImage.objects.create(hotel=hotel, image=image_data)
        return hotel

# ----------- Hotel Detail -----------


class HotelDetailSerializer(serializers.ModelSerializer):
    location = HotelLocationSerializer(read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.SerializerMethodField()

    class Meta:
        model = Hotel

        fields = [
            'id', 'owner', 'name', 'description', 'rating', 'phone_number',
            'email', 'website', 'created_at', 'has_parking', 'policy',
            'amenities', 'location', 'images', 'room_count'
        ]

    def get_room_count(self, obj):
        return obj.rooms.count()


'''
|==================================================|
|--------------- Room Serializers------------------|
|==================================================|
'''


# Room Images
class RoomImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'image_url', 'caption']
        read_only_fields = ['image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# Room Lists
class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            'id',  'hotel', 'title', 'slug',  'room_type', 'main_image'

        ]
        read_only_fields = ['hotel',]


# Room Lists
class RoomDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            "hotel",
            "room_type",
            "occupancy",
            "title",
            "slug",
            "guests_count",
            "room_details",
            "has_balcony",
            "has_air_conditioning",
            "has_tv",
            "pets",
            "price_per_night",
            "capacity",
            "floor",
            "is_available",
            "rating",
            "main_image",
            "created_at",
            "updated_at",

        ]

class RoomCreateSerializer(serializers.ModelSerializer):

    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    slug = serializers.SlugField(required=False, read_only=True)

    class Meta:
        model = Room
        fields = [
            'room_type', 'occupancy', 'title', 'slug', 'hotel',
            'guests_count', 'room_details', 'has_balcony', 'has_air_conditioning',
            'has_tv', 'pets', 'price_per_night', 'capacity', 'floor', 'is_available',
            'rating', 'main_image'
        ]

    def validate(self, data):
        if data.get('guests_count', 1) > data.get('capacity', 1):
            raise serializers.ValidationError(
                "guests_count cannot exceed capacity.")
        return data

    def create(self, validated_data):
        slug = validated_data.get('slug') or slugify(validated_data['title'])
        validated_data['slug'] = slug
        room = Room.objects.create(**validated_data)

        return room

    def update(self, instance, validated_data):
        images_data = self.initial_data.get('images', [])
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(
                validated_data.get('title', instance.title))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                RoomImage.objects.create(room=instance, **image)
        return instance
