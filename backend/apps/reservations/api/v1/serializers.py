# reservations/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import transaction
from decimal import Decimal

from apps.reservations.models import Reservation, BookingStatus, CheckIn
from apps.hotel.models import Room
from apps.discount.models import Coupon


class ReservationCreateSerializer(serializers.ModelSerializer):
    checking_date = serializers.DateField(write_only=True)
    checkout_date = serializers.DateField(write_only=True)
    coupon_code = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = Reservation
        fields = [
            "room",
            "checking_date",
            "checkout_date",
            "prefered_payment_method",
            "coupon_code",
        ]

    def validate(self, data):
        check_in = data["checking_date"]
        check_out = data["checkout_date"]
        room = data["room"]

        if check_in >= check_out:
            raise ValidationError("Check-in date must be before check-out date.")

        # Use the manager method for the initial availability check.
        if not Reservation.objects.is_room_available(room.id, check_in, check_out):
            raise ValidationError(
                "This room is not available for the selected date range."
            )

        return data

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user.customer_profile
        room = validated_data["room"]
        check_in = validated_data["checking_date"]
        check_out = validated_data["checkout_date"]
        nights = (check_out - check_in).days

        coupon = None
        code = validated_data.get("coupon_code")
        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                if not coupon.is_valid():
                    raise ValidationError("Invalid or expired coupon.")
            except Coupon.DoesNotExist:
                raise ValidationError("Coupon not found.")

        base_price = room.price_per_night
        discount = Decimal(coupon.discount_percent) if coupon else Decimal("0")
        total_price = base_price * nights * (Decimal("1") - discount / Decimal("100"))

        with transaction.atomic():
            reservation = Reservation.objects.create(
                user=user,
                room=room,
                checking_date=check_in,
                checkout_date=check_out,
                nights=nights,
                coupon=coupon,
                prefered_payment_method=validated_data["prefered_payment_method"],
                total_price=total_price,
                booking_status=BookingStatus.PENDING,
            )

            CheckIn.objects.create(
                reservation=reservation,
                customer=user,
                room=room,
                phone_number=user.user.phone_number,
                email=user.user.email,
            )

        return reservation


#  Reservation List
class ReservationListSerializer(serializers.ModelSerializer):
    room_title = serializers.CharField(source="room.title")
    hotel_name = serializers.CharField(source="room.hotel.name")

    class Meta:
        model = Reservation
        fields = [
            "id",
            "room_title",
            "hotel_name",
            "checking_date",
            "checkout_date",
            "total_price",
            "booking_status",
            "prefered_payment_method",
        ]


class OwnerReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="user.full_name")
    customer_email = serializers.CharField(source="user.user.email")
    customer_phone_number = serializers.CharField(source="user.user.phone_number")
    room_title = serializers.CharField(source="room.title")

    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "customer_phone_number",
            "room_title",
            "checking_date",
            "checkout_date",
            "booking_status",
            "total_price",
        ]


class ReservationInvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="user.full_name")
    customer_email = serializers.EmailField(source="user.user.email")
    room_title = serializers.CharField(source="room.title")
    hotel_name = serializers.CharField(source="room.hotel.name")
    hotel_location = serializers.CharField(
        source="room.hotel.location.city", default=""
    )

    discount_percent = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    total = serializers.DecimalField(
        source="total_price", max_digits=10, decimal_places=2
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "hotel_name",
            "hotel_location",
            "room_title",
            "checking_date",
            "checkout_date",
            "nights",
            "prefered_payment_method",
            "booking_status",
            "subtotal",
            "discount_percent",
            "total",
        ]

    def get_discount_percent(self, obj):
        return obj.coupon.discount_percent if obj.coupon else 0

    def get_subtotal(self, obj):
        return obj.room.price_per_night * obj.nights
