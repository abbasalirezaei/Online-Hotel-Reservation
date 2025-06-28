

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from reservations.models import Reservation
from .permissions import IsHotelOwner
from hotel.models import Hotel, Room, HotelLocation
from .serializers import (
    HotelListSerializer,
    HotelDetailSerializer,
    HotelCreateSerializer,
    HotelLocationSerializer,

    RoomCreateSerializer,
    RoomListSerializer,
)


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'hotels/',
        'hotels/<int:pk>/',
        'hotels/create/',
        'hotels/<int:pk>/edit/',
        'rooms/create/',
        'rooms/<int:pk>/',
        'rooms/<int:pk>/edit/',

    ]
    return Response(routes)

# hotel lists


class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.verified.all()
    serializer_class = HotelListSerializer

# hotel detail


class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.verified.all()
    serializer_class = HotelDetailSerializer


#  create hotel by owner
class HotelCreateAPIView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelCreateSerializer

    permission_classes = [IsAuthenticated, IsHotelOwner]


#  create hotel by owner
class HotelLocationCreateAPIView(generics.ListCreateAPIView):
    queryset = HotelLocation.objects.all()
    serializer_class = HotelLocationSerializer

    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        hotel = get_object_or_404(
            Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)

        if hasattr(hotel, 'location'):
            raise ValidationError("This hotel already has a location.")

        serializer.save(hotel=hotel)


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        qs = Room.objects.filter(hotel=hotel_id)
        return qs


class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        hotel = get_object_or_404(
            Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)

        serializer.save(hotel=hotel)


# class RoomUpdateAPIView(generics.UpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [IsAuthenticated, IsHotelOwner]


# class RoomDetailAPIView(generics.RetrieveAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


# class HotelRoomsAPIView(APIView):
#     def get(self, request, hotel_id):
#         rooms = Room.objects.filter(hotel_id=hotel_id)
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)


@api_view(['GET'])
def check_room_availability(request, id):
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    checkin_date = parse_date(checkin)
    checkout_date = parse_date(checkout)

    is_reserved = Reservation.objects.filter(
        room_id=id,
        checking_date__lt=checkout_date,
        checkout_date__gt=checkin_date
    ).exists()

    return Response({"available": not is_reserved})
