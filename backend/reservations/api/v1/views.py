# Core Django & DRF
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Local apps
from .serializers import (
    ReservationCreateSerializer
)
from hotel.models import Hotel, Room, HotelLocation, RoomImage
from reservations.models import Reservation
from accounts.models import CustomerProfile


@api_view(['GET'])
def api_overview(request):
    """
    Provides an overview of available API endpoints for client discovery.
    """
    return Response({
        'rooms/<int:room_id>/reserve/',
    })


# -> Reservations Views


class RoomReservationCreateView(generics.CreateAPIView):
    queryset=Reservation.objects.all()
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]
