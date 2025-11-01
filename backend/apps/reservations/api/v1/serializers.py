from rest_framework import serializers
from rest_framework.exceptions import ValidationError



from apps.reservations.models import Reservation

from apps.reservations.services import create_reservation


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
        # All complex business logic is now delegated to the service layer.
        request = self.context["request"]
        user_profile = request.user.customer_profile

        # The service function handles all logic, including coupon
        # validation, price calculation, and the atomic transaction.
        reservation = create_reservation(
            user_profile=user_profile,
            room=validated_data["room"],
            check_in_date=validated_data["checking_date"],
            check_out_date=validated_data["checkout_date"],
            prefered_payment_method=validated_data["prefered_payment_method"],
            coupon_code=validated_data.get("coupon_code"),
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