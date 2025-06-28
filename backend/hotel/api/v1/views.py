

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
from hotel.models import (
    Hotel, Room, HotelLocation, RoomImage
)
from .serializers import (
    HotelListSerializer,
    HotelDetailSerializer,
    HotelCreateSerializer,
    HotelLocationSerializer,

    RoomCreateSerializer,
    RoomListSerializer,
    RoomImageSerializer,
    RoomDetailSerializer,
)


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [

        'hotels/',
        'hotels/<int:pk>/',
        'hotels/create/',
        'hotels/<int:hotel_id>/locations/',
        'hotels/<int:hotel_id>/rooms/',
        'hotels/rooms/<slug:slug>/',
        'hotels/<int:hotel_id>/rooms/create/',
        'hotels/rooms/<int:room_id>/images/'

    ]
    return Response(routes)


'''
|==================================================|
|--------------- Hotels Views    ------------------|
|==================================================|
'''


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


'''
|==================================================|
|--------------- Rooms Views     ------------------|
|==================================================|
'''


# room list
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        qs = Room.objects.filter(hotel=hotel_id)
        return qs


# room create
class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        hotel = get_object_or_404(
            Hotel, id=self.kwargs['hotel_id'], owner=self.request.user)

        serializer.save(hotel=hotel)


# room detail
class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_slug = self.kwargs["slug"]
        qs = Room.objects.filter(slug=room_slug)
        return qs


# room images
class RoomImageCreateAPIView(generics.ListCreateAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        room = get_object_or_404(
            Room, id=self.kwargs['room_id'])

        serializer.save(room=room)
