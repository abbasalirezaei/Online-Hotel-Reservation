from datetime import date, timedelta, datetime
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import (
    TruncDate,
    TruncMonth,
    TruncDay,
    TruncWeek,
    TruncQuarter,
    TruncYear,
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from core.redis_client import redis_client


from django.shortcuts import get_object_or_404

# Local app imports
from .serializers import (
    ReservationCreateSerializer,
    ReservationListSerializer,
    OwnerReservationSerializer,
    ReservationInvoiceSerializer,
)
from apps.hotel.models import Room
from apps.reservations.models import Reservation, BookingStatus
from apps.reservations.tasks import send_reservation_cancellation_email


@api_view(["GET"])
def api_overview(request):
    """
    Endpoint: /api/v1/reservations/overview/

    Provides a human-readable overview of the reservation-related API endpoints.
    Useful for quick testing, onboarding, or self-documentation of the API.
    """
    return Response(
        {
            "Reserve Room": "rooms/<int:room_id>/reserve/",
            "My Reservations": "my/",
            "Cancel Reservation": "<int:pk>/cancel/",
            "Owner Reservations": "owner/",
            "Reservation Invoice": "<int:pk>/invoice/",
            # Reports
            "Daily & Summary Report": "report/",
            "Monthly Reservation Report": "report/monthly/?range=month|week|day|quarter|year",
            "Room Popularity Report": "report/by-room/",
        }
    )


# -------------------------------------
# Reservation Views
# -------------------------------------


class RoomReservationCreateView(generics.CreateAPIView):
    """
    Endpoint: POST /api/v1/reservations/rooms/<room_id>/reserve/

    Allows authenticated users to create a reservation for a specific room.
    The room ID is typically passed in the serializer payload or URL.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data needed for the lock and final check
        room = serializer.validated_data["room"]
        checkin_date = serializer.validated_data["checking_date"]
        checkout_date = serializer.validated_data["checkout_date"]

        # Define the lock key for Redis
        lock_key = f"lock:room:{room.id}"
        lock_timeout_seconds = 15  # The lock will auto-release after 15s

        # Acquire the lock from our redis_client
        lock = redis_client.lock(lock_key, timeout=lock_timeout_seconds)

        try:
            # Attempt to acquire the lock. If it's not acquired within 600 seconds,
            # it means the room is being booked by someone else right now.
            if not lock.acquire(blocking=True, blocking_timeout=600):
                raise ValidationError(
                    "This room is currently being booked by another user. Please try again in a moment.",
                    code="service_unavailable",
                )

            # --- CRITICAL SECTION ---
            # Now that we have the lock, we perform one final check to ensure the
            # room wasn't booked in the milliseconds before we acquired the lock.
            if not Reservation.objects.is_room_available(
                room.id, checkin_date, checkout_date
            ):
                raise ValidationError(
                    "Sorry, this room has just been booked for the selected dates.",
                    code="conflict",
                )

            # If the room is still available, proceed with saving the reservation.
            # The serializer's create method will be called here.
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        finally:
            # Always release the lock when we're done.
            if lock.locked():
                lock.release()


class UserReservationListView(generics.ListAPIView):
    """
    Endpoint: GET /api/v1/reservations/my/

    Returns a list of all reservations made by the current authenticated user.
    Sorted by booking date (newest first).
    """

    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Reservation.objects.select_related(
                "room", "room__hotel"
            )  # Optimize related data fetching
            .filter(user__user=self.request.user)
            .order_by("-booking_date")
        )


class CancelReservationView(APIView):
    """
    Endpoint: POST /api/v1/reservations/<int:pk>/cancel/

    Allows the authenticated user to cancel their own reservation.
    Only reservations in 'PENDING' or 'CONFIRMED' states can be cancelled.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, id=pk, user__user=request.user)

        if reservation.booking_status not in [
            BookingStatus.PENDING,
            BookingStatus.CONFIRMED,
        ]:
            raise ValidationError(
                "Only pending or confirmed reservations can be canceled."
            )

        reservation.booking_status = BookingStatus.CANCELLED
        reservation.save(update_fields=["booking_status"])

        # Trigger confirmation email asynchronously
        send_reservation_cancellation_email.delay(reservation.id)

        return Response({"detail": "Reservation cancelled."}, status=status.HTTP_200_OK)


class HotelOwnerReservationListView(generics.ListAPIView):
    """
    Endpoint: GET /api/v1/reservations/owner/

    Returns all reservations where the current authenticated user is the owner
    of the hotel (through the room relationship).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OwnerReservationSerializer

    def get_queryset(self):
        return (
            Reservation.objects.select_related("room", "user", "user__user")
            .filter(room__hotel__owner=self.request.user)
            .order_by("-booking_date")
        )


class ReservationInvoiceAPIView(generics.RetrieveAPIView):
    """
    Endpoint: GET /api/v1/reservations/<int:pk>/invoice/

    Retrieves the invoice details for a specific reservation.
    Only visible to the reservation’s owner (customer) or staff.
    """

    queryset = Reservation.objects.select_related(
        "room", "room__hotel", "room__hotel__location", "user", "user__user", "coupon"
    )
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationInvoiceSerializer

    def get_object(self):
        reservation = super().get_object()

        if (
            reservation.user.user != self.request.user
            and not self.request.user.is_staff
        ):
            raise PermissionDenied("You are not authorized to view this invoice.")

        return reservation


class ReservationReportView(APIView):
    """
    Endpoint: GET /api/v1/reservations/report/
    Provides daily booking count and revenue for hotel owners.
    Optional query params: ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        qs = Reservation.objects.filter(
            room__hotel__owner=user, booking_status=BookingStatus.CONFIRMED
        )

        if start_date:
            qs = qs.filter(booking_date__date__gte=start_date)
        if end_date:
            qs = qs.filter(booking_date__date__lte=end_date)

        data = (
            qs.annotate(booking_day=TruncDate("booking_date"))
            .values("booking_day")
            .annotate(total_bookings=Count("id"), total_revenue=Sum("total_price"))
            .order_by("-booking_day")
        )

        return Response(data)


class MonthlyReservationReportView(APIView):
    """
    GET /report/monthly/?range=month
    Returns booking count and revenue grouped by time periods (month, week, day, quarter, year).
    Default is monthly.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        period = request.query_params.get("range", "month")  # Default: month

        trunc_map = {
            "day": TruncDay,
            "week": TruncWeek,
            "month": TruncMonth,
            "quarter": TruncQuarter,
            "year": TruncYear,
        }

        truncate = trunc_map.get(period, TruncMonth)

        qs = Reservation.objects.filter(
            room__hotel__owner=user, booking_status=BookingStatus.CONFIRMED
        )

        report = (
            qs.annotate(period=truncate("booking_date"))
            .values("period")
            .annotate(total_bookings=Count("id"), total_revenue=Sum("total_price"))
            .order_by("-period")
        )

        return Response(report)


class RoomWiseReservationReportView(APIView):
    """
    GET /report/by-room/
    Returns popularity of rooms (booking count and revenue per room)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        qs = Reservation.objects.filter(
            room__hotel__owner=user, booking_status=BookingStatus.CONFIRMED
        )

        data = (
            qs.values("room__id", "room__title")
            .annotate(total_bookings=Count("id"), total_revenue=Sum("total_price"))
            .order_by("-total_bookings")
        )

        return Response(data)
