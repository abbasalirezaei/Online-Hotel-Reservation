# reservations/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from decimal import Decimal


from reservations.models import Reservation, BookingStatus
from hotel.models import Room
from discount.models import Coupon


class ReservationCreateSerializer(serializers.ModelSerializer):
    checking_date = serializers.DateField(write_only=True)
    checkout_date = serializers.DateField(write_only=True)
    coupon_code = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Reservation
        fields = [
            'room', 'checking_date', 'checkout_date', 
            'prefered_payment_method', 'coupon_code'
        ]

    def validate(self, data):
        check_in = data['checking_date']
        check_out = data['checkout_date']
        room = data['room']

        if check_in >= check_out:
            raise ValidationError(
                "Check-in date must be before check-out date.")

        # checking conflict
        conflict = Reservation.objects.filter(
            room=room,
            booking_status__in=[
                BookingStatus.PENDING, BookingStatus.CONFIRMED],
            checking_date__lt=check_out,
            checkout_date__gt=check_in
        )
        if conflict.exists():
            raise ValidationError(
                "This room is already reserved in the selected date range.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user.customer_profile
        room = validated_data['room']
        check_in = validated_data['checking_date']
        check_out = validated_data['checkout_date']
        nights = (check_out - check_in).days

        # validate the coupon
        coupon = None
        code = validated_data.get('coupon_code')
        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                if not coupon.is_valid():
                    raise ValidationError("Invalid or expired coupon.")
            except Coupon.DoesNotExist:
                raise ValidationError(
                    "Coupon not found, please Enter Valid Coupon.")

        # calculate total_price
        base_price = room.price_per_night
        discount = Decimal(coupon.discount_percent) if coupon else Decimal('0')
        total_price = base_price * nights * \
            (Decimal('1') - discount / Decimal('100'))

        return Reservation.objects.create(
            user=user,
            room=room,
            checking_date=check_in,
            checkout_date=check_out,
            nights=nights,
            coupon=coupon,
            prefered_payment_method=validated_data['prefered_payment_method'],
            total_price=total_price
        )


'''class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            'id', 'room',
            'user', 'room_number',
            'coupen', 'prefered_payment_method'
        ]
'''
