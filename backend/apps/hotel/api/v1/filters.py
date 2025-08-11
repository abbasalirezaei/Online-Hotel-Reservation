from django_filters import rest_framework as filters
from apps.hotel.models import Room

class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr='gte')
    max_capacity = filters.NumberFilter(field_name="capacity", lookup_expr='lte')
    floor = filters.NumberFilter(field_name="floor")
    room_type = filters.CharFilter(field_name="room_type", lookup_expr='iexact')
    pets_allowed = filters.BooleanFilter(field_name="pets")

    class Meta:
        model = Room
        fields = [
            'min_price', 'max_price', 'min_capacity', 'max_capacity',
            'floor', 'room_type',  'pets_allowed'
        ]