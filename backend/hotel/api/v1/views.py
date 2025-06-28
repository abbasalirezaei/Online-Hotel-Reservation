

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response




from reservations.models import Reservation
from .permissions import IsHotelOwner
from .serializers import HotelSerializer,RoomSerializer
from hotel.models import Hotel, Room



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
    serializer_class = HotelSerializer

# hotel detail
class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.verified.all()
    serializer_class = HotelSerializer



#  create hotel by owner
class HotelCreateAPIView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class HotelUpdateAPIView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)





class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def perform_create(self, serializer):
        serializer.save(hotel_owner=self.request.user)


class RoomUpdateAPIView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer



class HotelRoomsAPIView(APIView):
    def get(self, request, hotel_id):
        rooms = Room.objects.filter(hotel_id=hotel_id)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    



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