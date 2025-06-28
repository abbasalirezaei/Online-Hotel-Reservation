# Core Django & DRF
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Local apps
from .permissions import IsHotelOwner
from .serializers import (
    HotelListSerializer, HotelDetailSerializer, HotelCreateSerializer,
    HotelLocationSerializer, RoomCreateSerializer, RoomListSerializer,
    RoomImageSerializer, RoomDetailSerializer
)
from hotel.models import Hotel, Room, HotelLocation, RoomImage
from reservations.models import Reservation


@api_view(['GET'])
def api_overview(request):
    """
    Provides an overview of available API endpoints for client discovery.
    """
    return Response({
        "hotels/": "GET (list) | POST (create)",
        "hotels/<id>/": "GET (detail)",
        "hotels/<id>/location/": "GET | POST | PATCH",
        "hotels/<id>/rooms/": "GET (list rooms) | POST (create room)",
        "rooms/<slug>/": "GET (room detail)",
        "rooms/<id>/images/": "GET | POST room images"
    })


# -> Hotel Views

class HotelListCreateView(generics.ListCreateAPIView):
    """
    Lists all verified hotels (GET) or allows authenticated owners to create new hotels (POST).
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsHotelOwner]

    def get_queryset(self):
        # Return only verified hotels
        return Hotel.verified.all()

    def get_serializer_class(self):
        # Choose appropriate serializer depending on request type
        return HotelCreateSerializer if self.request.method == 'POST' else HotelListSerializer

