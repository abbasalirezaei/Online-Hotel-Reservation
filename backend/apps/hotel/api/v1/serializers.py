from rest_framework import serializers

from django.utils.text import slugify
from django.db import transaction
from django.db.models import Avg, Count

from apps.hotel.models.hotel_model import Hotel, HotelLocation, HotelImage, Amenity
from apps.hotel.models.room_model import Room, RoomImage
from apps.accounts.models import User


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon', 'description']
        

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Amenity name cannot be empty.")
        return value
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
    room_count = serializers.IntegerField(read_only=True)     
    total_reviews = serializers.IntegerField(read_only=True)   

    class Meta:
        model = Hotel
        fields = [
            'id',  'name', 'owner', 
            'images', 'room_count', 'total_reviews'
        ]
        read_only_fields = ["owner", "room_count", "total_reviews"]

# ----------- Hotel Create Serializer -----------


class HotelCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False
    )
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'name', 'phone_number', 'email', 'website', 'main_image',
            'has_parking', 'policy', 'amenities', 'description', 'uploaded_images'
        ]
        read_only_fields = ['room_count', 'total_reviews']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        amenities = validated_data.pop("amenities")
        user = self.context['request'].user

        with transaction.atomic():
            hotel = Hotel.objects.create(
                owner=user, is_verified=False, **validated_data)
            hotel.amenities.set(amenities)
            for image_data in uploaded_images:
                HotelImage.objects.create(hotel=hotel, image=image_data)

        return hotel

# ----------- Hotel Detail Serializer -----------


class HotelDetailSerializer(serializers.ModelSerializer):
    location = HotelLocationSerializer(read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room_count = serializers.IntegerField(read_only=True)      # <- explicit read-only
    total_reviews = serializers.IntegerField(read_only=True)   # <- explicit read-only
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'owner', 'name', 'description', 'phone_number',
            'email', 'website', 'created_at', 'has_parking', 'policy',
            'amenities', 'location', 'images', 'room_count', 'total_reviews', 'main_image'
        ]
        read_only_fields = ['owner', 'room_count', 'total_reviews']

    def validate(self, attrs):
        # Only apply these validations during update
        if self.instance:
            if 'name' in attrs and not attrs['name'].strip():
                raise serializers.ValidationError(
                    {"name": "Hotel name cannot be empty."})

            if 'policy' in attrs and len(attrs['policy']) < 10:
                raise serializers.ValidationError(
                    {"policy": "Policy must be at least 10 characters long."})

            if 'amenities' in attrs:
                allowed_keys = {'wifi', 'pool', 'breakfast', 'parking'}
                invalid_keys = set(attrs['amenities'].keys()) - allowed_keys
                if invalid_keys:
                    raise serializers.ValidationError({
                        "amenities": f"Invalid keys: {', '.join(invalid_keys)}. Allowed keys are: {', '.join(allowed_keys)}."
                    })

        return attrs


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
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    hotel_owner = serializers.CharField(source='hotel.owner.email', read_only=True)

    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "hotel",
            "hotel_name",  # Added field
            "hotel_owner",  # Added field
            "room_type",
            "title",
            "slug",
            "images",
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

    class Meta:
        model = Room
        fields = [
            'room_type', 'title',  'hotel',
            'guests_count', 'room_details', 'has_balcony', 'has_air_conditioning',
            'has_tv', 'pets', 'price_per_night', 'capacity', 'floor', 'is_available', 'main_image'
        ]

    def create(self, validated_data):
        images_data = self.initial_data.get('images', [])
        with transaction.atomic():
            # Let the model's save() generate a unique slug
            room = Room(**validated_data)
            room.save()
            for image in images_data:
                RoomImage.objects.create(room=room, **image)
        return room

    def update(self, instance, validated_data):
        images_data = self.initial_data.get('images', [])
        # Apply incoming fields; don't manually set slug — model.save() will ensure uniqueness
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                RoomImage.objects.create(room=instance, **image)
        return instance
