

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD


=======
from rest_framework import status
from django.db import transaction

from hotel.models import (
    Category,
    Room,
    Booking,
    CheckIn,
    RoomDisplayImages
)
from .serializers import (
    CategorySerializer,
    RoomSerializer,
    BookingSerializer,
    CheckinSerializer,
    RoomDisplayImagesSerializer
)
>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215


from reservations.models import Reservation
from .permissions import IsHotelOwner
from .serializers import HotelSerializer,RoomSerializer
from hotel.models import Hotel, Room



# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
<<<<<<< HEAD
        'hotels/',
        'hotels/<int:pk>/',
        'hotels/create/',
        'hotels/<int:pk>/edit/',
        'rooms/create/',
        'rooms/<int:pk>/',
        'rooms/<int:pk>/edit/',
=======
        '/get_room_list/',
        '/get_a_room_detail/<str:room_slug>/',
        '/book/',
        '/checkout/',
        '/get_current_checked_in_rooms/',
        '/room-display-images/',
        '/room-display-images/<int:room_id>/',
        'categories/',
        'categories/<slug:slug>/'
>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215

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

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category_name')
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        return queryset



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


<<<<<<< HEAD
class RoomUpdateAPIView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]
=======
#
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Retrieve details of a single category
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'  # or 'pk' if you're using IDs


class RoomDisplayImagesListView(ListAPIView):
    queryset = RoomDisplayImages.objects.all()
    serializer_class = RoomDisplayImagesSerializer


class RoomDisplayImagesByRoomView(ListAPIView):
    serializer_class = RoomDisplayImagesSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return RoomDisplayImages.objects.filter(room_id=room_id)


class BookingCreateApiView(CreateAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def create(self, request, *args, **kwargs):
        # این متد بدون تغییر می‌ماند
        response = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response['data'] = serializer.data
        response['response'] = "Room is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        
        
        try:
            
            # zero checking for necessary data
            room_id = request.data.get('room')
            check_in = request.data['checking_date']
            check_out = request.data['checkout_date']
            if not room_id or not check_in or not check_out:
                return Response({"message": "اطلاعات اتاق، تاریخ ورود و خروج الزامی است"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # FIRST getting room
            room = get_object_or_404(Room, pk=room_id)
            # checking if room is available
            if not room.is_available(check_in, check_out):
                return Response({"response": "Room is already booked"}, status=status.HTTP_400_BAD_REQUEST)
            
            # SECOND getting customer and checking if customer exists
            try:
                customer = Customer.objects.get(customer=request.user)
            except Customer.DoesNotExist:
                return Response({"response": "Customer profile not found for this user"}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            # THIRD adding customer id to request data
            request.data['customer'] = customer.id
            
            # FOURTH using transaction to ensure data consistency
            with transaction.atomic():
                # FIFTH marking room as booked
                room.is_booked = True
                room.save()
                
                # SIXTH creating CheckIn record
                checked_in_room = CheckIn.objects.create(
                    customer=request.user,
                    room=room,
                    phone_number=request.data.get('phone_number', ''),
                    email=request.data.get('email', '')
                )
                
                # SEVENTH calling create method to create Booking
                return self.create(request, *args, **kwargs)
                
        except Exception as e:
            return Response({"response": f"An error occurred: {str(e)}"}, 
                           status=status.HTTP_400_BAD_REQUEST)

>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215


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