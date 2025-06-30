from django_filters import rest_framework as filters
from hotel.models import Hotel

class HotelFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Hotel
        fields = ['city', 'min_rating', 'max_price']