<<<<<<< HEAD
=======
from hotel.models import Room, Booking, CheckIn, RoomDisplayImages, Category
>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215
from rest_framework import serializers
from django.utils.text import slugify
from hotel.models.hotel_model import Hotel, HotelLocation, HotelImage
from hotel.models.room_model import Room, RoomImage
from accounts.models import User

<<<<<<< HEAD
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
=======
# Room serializer


class RoomSerializer(serializers.ModelSerializer):
    """
    Room Model Serializer
    --------------------
    This serializer manages room information serialization, including:
    - Room title
    - Room slug
    - Bed type
    - Category
    - Room images
    - Room display images
    
    Used for:
    - Creating new rooms
    - Updating room information
    - Listing available rooms
    - Retrieving room details
    """
    category_name = serializers.CharField(source='category.name')
>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215

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
<<<<<<< HEAD
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
=======
        category_data = validated_data.pop('category', None)
        room = super().create(validated_data)
        if category_data:
            room.category = Category.objects.get(name=category_data['name'])
            room.save()
        return room

# Category serializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Model Serializer
    ------------------------
    This serializer handles category data serialization, including:
    - Category name
    - Parent category (if exists)
    - Category slug
    - Category image (if exists)

    Used for:
    - Creating new categories
    - Updating existing categories
    - Listing all categories
    - Retrieving single category details
    """
    class Meta:
        model = Category
        fields = '__all__'

# RoomDisplayImages serializer
class RoomDisplayImagesSerializer(serializers.ModelSerializer):
    """
    RoomDisplayImages Model Serializer
    ---------------------------------
    This serializer handles room display image data serialization, including:
    - Room display image ID
    - Room ID
    - Room display image (if exists)

    Used for:
    - Creating new room display images
    - Updating existing room display images
    - Listing all room display images
    - Retrieving single room display image details
    """
    class Meta:
        model = RoomDisplayImages
        fields = ['id', 'room', 'display_images']
        
        
# Booking serializer

class BookingSerializer(serializers.ModelSerializer):
    """
    Booking Model Serializer
    ----------------------
    This serializer handles booking data serialization, including all fields from the Booking model such as:
    - booking_id
    - customer (foreign key to Customer)
    - room (foreign key to Room)
    - phone_number
    - email
    - payment_method
    - payment_status
    - transaction_id
    - booking_status
    - cancelled_at
    - booking_date
    - checking_date
    - checkout_date
    - created_at
    - updated_at
    - nights
    - total_price
    - coupon
    - guests_count
    - guest_note
    
    Used for:
    - Creating new bookings
    - Updating existing bookings
    - Listing all bookings
    - Retrieving single booking details
    """
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_date', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Validate that the check-out date is after the check-in date.
        """
        if data['checking_date'] >= data['checkout_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data
    
# Checkin serializer
class CheckinSerializer(serializers.ModelSerializer):
    """
    Checkin Model Serializer
    ----------------------
    This serializer handles check-in data serialization, including:
    - Phone number
    - Email
    - Customer ID
    - Customer name
    - Room ID
    - Room slug
    
    Used for:
    - Creating new check-ins
    - Updating existing check-ins
    - Listing all check-ins
    - Retrieving single check-in details
    """
    room_id = serializers.IntegerField(source='room.pk')
    room_slug = serializers.SlugField(source='room.room_slug')
    customer_id = serializers.IntegerField(source='customer.pk')
    customer_name = serializers.CharField(source='customer.username')
>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215

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