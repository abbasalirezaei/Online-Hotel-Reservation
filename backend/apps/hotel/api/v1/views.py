# Core Django & DRF
from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404
from django.db.models import Count, F, Sum, Avg

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Local apps
from .permissions import IsHotelOwnerOrReadOnly
from .serializers import (
    HotelListSerializer, HotelDetailSerializer, HotelCreateSerializer,
    HotelLocationSerializer, HotelImageSerializer,
    RoomCreateSerializer, RoomListSerializer,
    RoomImageSerializer, RoomDetailSerializer, AmenitySerializer
)
from apps.hotel.models import (
    Hotel, HotelImage, Amenity,
    HotelLocation, Room, RoomImage
)
from apps.reservations.models import Reservation
from apps.notifications.tasks import send_custom_notification
from .filters import RoomFilter


@api_view(['GET'])
def api_overview(request):
    """Provides an overview of available API endpoints for client discovery."""
    return Response({
        "hotels/": "GET (list) | POST (create)",
        "hotels/<int:pk>/": "GET (detail)",
        "hotels/<int:hotel_id>/location/": "GET | POST (create) | PUT | PATCH | DELETE",
        "hotels/<int:hotel_id>/images/": "GET (list) | POST (create)",
        "hotels/<int:hotel_id>/images/<int:image_id>/": "GET | PUT | DELETE",
        "hotels/<int:hotel_id>/rooms/": "GET (list) | POST (create)",
        "rooms/<slug>/": "GET (detail)",
        "rooms/<int:room_id>/images/": "GET (list) | POST (create)",
        "hotels/<int:hotel_id>/amenities/": "GET (list) | POST (add) | DELETE (remove)",
    })


#  Hotel Views (List and Create)


class HotelListCreateView(generics.ListCreateAPIView):
    """
    Lists all verified hotels (GET) or allows verified owners to create new hotels (POST).
    Optimized for performance with limited fields and prefetching.
    """
    permission_classes = [IsHotelOwnerOrReadOnly]
    filterset_fields = ['location__city']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Cache for 15 minutes
    @method_decorator(cache_page(60 * 15, key_prefix='hotel_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Hotel.verified.annotate(
            room_count=Count('rooms'),
            total_reviews=Count('reviews')
        ).only(
            "id", "name", "description", "owner_id",
            "created_at"
        ).prefetch_related("images").select_related("owner", "location")
        return (
            queryset
        )

    def create(self, request, *args, **kwargs):
        user = request.user

        response = super().create(request, *args, **kwargs)

        # Send notification to the user
        send_custom_notification.delay(
            user.id,
            message="Your request to create a hotel has been submitted. You will be notified once it's reviewed by an admin.",
            priority="info",
            redirect_url="//"
        )
        return response

    def get_serializer_class(self):
        return HotelCreateSerializer if self.request.method == 'POST' else HotelListSerializer


class HotelDetailView(generics.RetrieveUpdateAPIView):
    """Retrieves detailed information for a specific verified hotel by ID."""
    permission_classes = [IsHotelOwnerOrReadOnly]
    queryset = Hotel.verified.annotate(
        room_count=Count('rooms'),
        total_reviews=Count('reviews')
    ).select_related(
        'owner', 'location'
    ).prefetch_related('images').all()
    serializer_class = HotelDetailSerializer


# CRUD operation Hotel Location

class HotelLocationView(generics.ListCreateAPIView):
    serializer_class = HotelLocationSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return HotelLocation.objects.filter(hotel_id=hotel_id, hotel__owner=self.request.user)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
        if hasattr(hotel, 'location'):
            raise ValidationError("This hotel already has a location.")
        serializer.save(hotel=hotel)


class HotelLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelLocationSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return HotelLocation.objects.filter(hotel_id=hotel_id)




# CRUD operations Hotel Images


class HotelImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Allows hotel owners to view, update, or delete a specific hotel image."""
    serializer_class = HotelImageSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        return HotelImage.objects.filter(hotel__owner=self.request.user)

    def get_object(self):
        hotel_id = self.kwargs['hotel_id']
        image_id = self.kwargs['pk']
        return get_object_or_404(HotelImage, id=image_id, hotel_id=hotel_id)


class HotelImageListCreateView(generics.ListCreateAPIView):
    """Lists or adds images for a specific hotel."""
    serializer_class = HotelImageSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        return HotelImage.objects.filter(hotel_id=self.kwargs['hotel_id'])

    def perform_create(self, serializer):
        hotel = get_object_or_404(
            Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
        serializer.save(hotel=hotel)


# CRUD operations Hotel Amenities
class HotelAmenitiesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing amenities associated with a specific hotel.
    Allows listing, adding, and removing amenities for a hotel.
    """
    serializer_class = AmenitySerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        return hotel.amenities.all()

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=self.request.user)
        amenity = serializer.save()
        hotel.amenities.add(amenity)

    def destroy(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=self.request.user)
        amenity = self.get_object()
        hotel.amenities.remove(amenity)
        return Response(status=204)




class OnwerHotelListView(generics.ListAPIView):
    """
    Lists hotels owned by the authenticated user along with stats:
      - reservations_count
      - total_revenue
      - avg_rating
      - popular_rooms (top 3 rooms by reservations)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HotelListSerializer

    def get_queryset(self):
        # Ensure serializer fields room_count and total_reviews exist on each Hotel instance
        return (
            Hotel.verified
            .filter(owner=self.request.user)
            .annotate(
                room_count=Count('rooms', distinct=True),
                total_reviews=Count('reviews', distinct=True),
                reservations_count=Count('rooms__reservations', distinct=True),
                total_revenue=Sum('rooms__reservations__total_price'),
                avg_rating=Avg('reviews__rating'),
            )
            .select_related('location', 'owner')
            .prefetch_related('images')
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        hotels = page or queryset

        serializer = self.get_serializer(hotels, many=True)
        data = serializer.data

        id_index = {h['id']: i for i, h in enumerate(data)}

        for hotel in hotels:
            idx = id_index.get(hotel.id)
            if idx is None:
                continue

            data[idx]['reservations_count'] = int(getattr(hotel, 'reservations_count', 0) or 0)
            total_revenue = getattr(hotel, 'total_revenue', 0) or 0
            try:
                data[idx]['total_revenue'] = float(total_revenue)
            except Exception:
                data[idx]['total_revenue'] = total_revenue

            avg_rating = getattr(hotel, 'avg_rating', None)
            data[idx]['avg_rating'] = float(avg_rating) if avg_rating is not None else None

            top_rooms = (
                Room.objects.filter(hotel=hotel)
                .annotate(reservations_count=Count('reservations'))
                .order_by('-reservations_count')[:3]
            )
            data[idx]['popular_rooms'] = RoomListSerializer(top_rooms, many=True, context={'request': request}).data

        if page is not None:
            return self.get_paginated_response(data)
        return Response(data)
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
        hotel = get_object_or_404(
            Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)
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
