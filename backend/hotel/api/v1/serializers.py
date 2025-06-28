from rest_framework import serializers
from django.utils.text import slugify
from hotel.models.hotel_model import Hotel, HotelLocation, HotelImage
from hotel.models.room_model import Room, RoomImage
from accounts.models import User

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

class HotelLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocation
        fields = ['id', 'country', 'city', 'postal_code', 'address']

class RoomImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'image_url', 'caption']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, required=False)
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_type', 'occupancy', 'bed_type', 'title', 'slug',
            'guests_count', 'room_details', 'has_balcony', 'has_air_conditioning',
            'has_tv', 'pets', 'price_per_night', 'capacity', 'floor', 'is_available',
            'rating', 'created_at', 'updated_at', 'images'
        ]

    def validate(self, data):
        if data.get('guests_count', 1) > data.get('capacity', 1):
            raise serializers.ValidationError("guests_count cannot exceed capacity.")
        return data

    def create(self, validated_data):
        images_data = self.initial_data.get('images', [])
        slug = validated_data.get('slug') or slugify(validated_data['title'])
        validated_data['slug'] = slug
        room = Room.objects.create(**validated_data)
        for image in images_data:
            RoomImage.objects.create(room=room, **image)
        return room

    def update(self, instance, validated_data):
        images_data = self.initial_data.get('images', [])
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data.get('title', instance.title))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                RoomImage.objects.create(room=instance, **image)
        return instance

class HotelSerializer(serializers.ModelSerializer):
    location = HotelLocationSerializer(required=False)
    images = HotelImageSerializer(many=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id', 'owner', 'name', 'description', 'rating', 'phone_number',
            'email', 'website', 'created_at', 'has_parking', 'policy',
            'amenities', 'location', 'images', 'room_count'
        ]
        read_only_fields=["owner",]

    def get_room_count(self, obj):
        return obj.rooms.count()

    def create(self, validated_data):
        location_data = self.initial_data.get('location')
        images_data = self.initial_data.get('images', [])
        hotel = Hotel.objects.create(**validated_data)
        if location_data:
            HotelLocation.objects.create(hotel=hotel, **location_data)
        for image in images_data:
            HotelImage.objects.create(hotel=hotel, **image)
        return hotel

    def update(self, instance, validated_data):
        location_data = self.initial_data.get('location')
        images_data = self.initial_data.get('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if location_data:
            HotelLocation.objects.update_or_create(hotel=instance, defaults=location_data)
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                HotelImage.objects.create(hotel=instance, **image)
        return instance