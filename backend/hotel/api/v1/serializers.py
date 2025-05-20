from hotel.models import Room, Booking, CheckIn, RoomDisplayImages, Category
from rest_framework import serializers

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

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
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
    This serializer handles booking data serialization, including:
    - Booking ID
    - Customer ID
    - Room ID
    - Booking date
    - Check-in date
    - Check-out date
    - Total price
    
    Used for:
    - Creating new bookings
    - Updating existing bookings
    - Listing all bookings
    - Retrieving single booking details
    """
    class Meta:
        model = Booking
        fields = '__all__'

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

    class Meta:
        model = CheckIn
        fields = ('phone_number', 'email', 'customer_id', 'customer_name', 'room_id', 'room_slug',)
