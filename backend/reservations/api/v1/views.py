# Core Django & DRF
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from django.utils import timezone
from django.shortcuts import get_object_or_404
# Local apps
from .serializers import (
    ReservationCreateSerializer,
    ReservationListSerializer,
    OwnerReservationSerializer
)
from hotel.models import Hotel, Room, HotelLocation, RoomImage
from reservations.models import Reservation , BookingStatus
from accounts.models import CustomerProfile


@api_view(['GET'])
def api_overview(request):
    """
    Provides an overview of available API endpoints for client discovery.
    """
    return Response({
        'rooms/<int:room_id>/reserve/',
        'my/',
        '<int:pk>/cancel/',
    })


# -> Reservations Views

class RoomReservationCreateView(generics.CreateAPIView):
    queryset=Reservation.objects.all()
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    
class UserReservationListView(generics.ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user__user=self.request.user).order_by('-booking_date')



class CancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, id=pk, user__user=request.user)

        if reservation.booking_status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            raise ValidationError("Only pending or confirmed reservations can be canceled.")

        reservation.booking_status = BookingStatus.CANCELLED
        reservation.save(update_fields=['booking_status'])
        return Response({"detail": "Reservation cancelled."}, status=status.HTTP_200_OK)





class HotelOwnerReservationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OwnerReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(
            room__hotel__owner=self.request.user
        ).order_by('-booking_date')
