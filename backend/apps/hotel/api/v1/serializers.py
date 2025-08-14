from rest_framework import serializers

from django.utils.text import slugify
from django.db import transaction
from django.db.models import Avg, Count

from apps.hotel.models.hotel_model import Hotel, HotelLocation, HotelImage
from apps.hotel.models.room_model import Room, RoomImage
from apps.accounts.models import User

# ----------- Hotel Image Serializer -----------
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
                "You are not allowed to add images for this hotel.")
        return hotel

# ----------- Hotel Location Serializer -----------

class HotelLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocation
        fields = ['id', 'hotel', 'country', 'city', 'postal_code', 'address']
        read_only_fields = ['hotel',]

    def validate_hotel(self, hotel):
        request = self.context.get("request")
        if hotel.owner != request.user:
            raise serializers.ValidationError(
                "You are not allowed to add an address for this hotel.")
        return hotel

# ----------- Hotel List Serializer -----------

class HotelListSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id', 'owner', 'name', 
            'images', 'room_count', 'total_reviews'   
        ]
        read_only_fields = ["owner",]

    def get_room_count(self, obj):
        return obj.rooms.count()

    def get_total_reviews(self, obj):
        return obj.reviews.aggregate(Count('id'))['id__count']    

# ----------- Hotel Create Serializer -----------

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

# ----------- Hotel Detail Serializer -----------

class HotelDetailSerializer(serializers.ModelSerializer):
    location = HotelLocationSerializer(read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id', 'owner', 'name', 'description', 'phone_number',
            'email', 'website', 'created_at', 'has_parking', 'policy',
            'amenities', 'location', 'images', 'room_count'
        ]

    def get_room_count(self, obj):
        return obj.rooms.count()

'''
|==================================================|
|--------------- Room Serializers -----------------|
|==================================================|
'''

# ----------- Room Image Serializer -----------
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

# ----------- Room List Serializer -----------
class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'title', 'slug', 'price_per_night', 'room_type', 'main_image'
        ]
        read_only_fields = ['hotel',]

# ----------- Room Detail Serializer -----------
class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "hotel",
            "room_type",
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
            "main_image",
            "created_at",
            "updated_at",
        ]

# ----------- Room Create/Update Serializer -----------
class RoomCreateSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    slug = serializers.SlugField(required=False, read_only=True)

    class Meta:
        model = Room
        fields = [
            'room_type', 'title', 'slug', 'hotel',
            'guests_count', 'room_details', 'has_balcony', 'has_air_conditioning',
            'has_tv', 'pets', 'price_per_night', 'capacity', 'floor', 'is_available', 'main_image'
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
