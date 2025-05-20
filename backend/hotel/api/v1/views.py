from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/get_room_list/',
        '/get_a_room_detail/<str:room_slug>/',
        '/book/',
        '/checkout/',
        '/get_current_checked_in_rooms/',
        '/room-display-images/',
        '/room-display-images/<int:room_id>/',
        'categories/',
        'categories/<slug:slug>/'

    ]
    return Response(routes)


class RoomView(ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category_name')
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        return queryset



class RoomDetailView(RetrieveAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    lookup_field = 'room_slug'


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
        response = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response['data'] = serializer.data
        response['response'] = "Room is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=request.data['room'])
        if room.is_booked:
            return Response({"response": "Room is already booked"}, status=status.HTTP_200_OK)
        room.is_booked = True
        room.save()

        checked_in_room = CheckIn.objects.create(
            customer=request.user,
            room=room,
            phone_number=request.data['phone_number'],
            email=request.data['email']
        )
        checked_in_room.save()
        return self.create(request, *args, **kwargs)


class CheckoutView(APIView):
    def post(self, request):
        room = get_object_or_404(Room, pk=request.data['pk'])
        checked_in_room = CheckIn.objects.get(room__pk=request.data['pk'])
        print(checked_in_room)
        room.is_booked = False
        room.save()
        checked_in_room.delete()
        return Response({"Checkout Successful"}, status=status.HTTP_200_OK)


class CheckedInView(ListAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = CheckinSerializer
    queryset = CheckIn.objects.order_by('-id')
