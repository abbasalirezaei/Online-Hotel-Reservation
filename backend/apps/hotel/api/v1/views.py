# Core Django & DRF
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Local apps
from .permissions import IsHotelOwnerOrReadOnly
from .serializers import (
    HotelListSerializer, HotelDetailSerializer, HotelCreateSerializer,
    HotelLocationSerializer, HotelImageSerializer,
    RoomCreateSerializer, RoomListSerializer,
    RoomImageSerializer, RoomDetailSerializer
)
from apps.hotel.models import (
    Hotel, HotelImage,
    HotelLocation, Room, RoomImage
)
from apps.reservations.models import Reservation
from .filters import RoomFilter


@api_view(['GET'])
def api_overview(request):
    """Provides an overview of available API endpoints for client discovery."""
    return Response({
        "hotels/": "GET (list) | POST (create)",
        "hotels/<id>/": "GET (detail)",
        "hotels/<id>/location/": "GET | POST | PATCH",
        "hotels/<id>/rooms/": "GET (list rooms) | POST (create room)",
        "hotels/<int:hotel_id>/images/": "GET | POST hotel images",
        "rooms/<slug>/": "GET (room detail)",
        "rooms/<id>/images/": "GET | POST room images"
    })


#  Hotel Views (List and Create)

class HotelListCreateView(generics.ListCreateAPIView):
    """
    Lists all verified hotels (GET) or allows authenticated owners to create new hotels (POST).
    Optimized for performance with limited fields and prefetching.
    """
    permission_classes = [IsHotelOwnerOrReadOnly]
    filterset_fields = ['location__city']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return (
            Hotel.verified
            .only("id", "name", "description", "owner_id", "created_at")
            .prefetch_related("images", "location")
        )

    def get_serializer_class(self):
        return HotelCreateSerializer if self.request.method == 'POST' else HotelListSerializer


class HotelDetailView(generics.RetrieveAPIView):
    """Retrieves detailed information for a specific verified hotel by ID."""
    queryset = Hotel.verified.all()
    serializer_class = HotelDetailSerializer


class HotelLocationView(generics.ListCreateAPIView):
    """Allows hotel owners to view or create the location of their hotel."""
    serializer_class = HotelLocationSerializer
    permission_classes = [IsAuthenticated, IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        return HotelLocation.objects.filter(hotel__owner=self.request.user)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
        if hasattr(hotel, 'location'):
            raise ValidationError("This hotel already has a location.")
        serializer.save(hotel=hotel)


class HotelImageListCreateView(generics.ListCreateAPIView):
    """Lists or adds images for a specific hotel."""
    serializer_class = HotelImageSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        return HotelImage.objects.filter(hotel_id=self.kwargs['hotel_id'])

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
        serializer.save(hotel=hotel)


# -> Room Views

class RoomListCreateView(generics.ListCreateAPIView):
    """Lists available rooms for a specific hotel (GET) or allows owners to add new rooms (POST)."""
    serializer_class = RoomListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoomFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price_per_night', 'capacity', 'floor']

    def get_queryset(self):
        return (
            Room.available
            .filter(hotel_id=self.kwargs['hotel_id'])
            .select_related('hotel')
            .order_by('price_per_night')
        )

    def get_serializer_class(self):
        return RoomCreateSerializer if self.request.method == 'POST' else RoomListSerializer

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
        serializer.save(hotel=hotel)


class RoomDetailView(generics.RetrieveAPIView):
    """Retrieves detailed info for a single room by slug."""
    queryset = Room.available.all()
    serializer_class = RoomDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]


# -> Room Image Views

class RoomImageListCreateView(generics.ListCreateAPIView):
    """Lists or adds images for a specific room. Only hotel owners can upload."""
    serializer_class = RoomImageSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        return RoomImage.objects.filter(room_id=self.kwargs['room_id'])

    def perform_create(self, serializer):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        serializer.save(room=room)