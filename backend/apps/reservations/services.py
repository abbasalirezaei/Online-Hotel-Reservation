from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.reservations.models import Reservation, BookingStatus
from apps.hotel.models import Room
from apps.discount.models import Coupon
from apps.accounts.models import CustomerProfile


@transaction.atomic
def create_reservation(
    user_profile: CustomerProfile,
    room: Room,
    check_in_date,
    check_out_date,
    prefered_payment_method: str,
    coupon_code: str = None,
) -> Reservation:
    """
    Main service function for creating a reservation.

    This handles the business logic of:
    1. Calculating nights.
    2. Validating the coupon.
    3. Calculating the final price.
    4. Creating the Reservation object.

    All operations are wrapped in an atomic transaction to ensure
    data integrity.
    """

    # 1. Calculate nights
    nights = (check_out_date - check_in_date).days
    if nights <= 0:
        # This is also checked in the serializer, but good practice
        # to re-validate in the service layer.
        raise ValidationError("Check-out date must be after check-in date.")

    # 2. Validate coupon and calculate discount
    coupon = None
    discount = Decimal("0")
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if not coupon.is_valid():
                raise ValidationError("Invalid or expired coupon.")
            discount = Decimal(coupon.discount_percent)
        except Coupon.DoesNotExist:
            raise ValidationError("Coupon not found.")

    # 3. Calculate final price
    base_price = room.price_per_night
    total_price = base_price * nights * (Decimal("1") - discount / Decimal("100"))

    # 4. Create the Reservation
    # (Note: The incorrect creation of 'CheckIn' has been removed,
    # as Check-In is a separate business process from 'Booking'.)
    reservation = Reservation.objects.create(
        user=user_profile,
        room=room,
        checking_date=check_in_date,
        checkout_date=check_out_date,
        nights=nights,
        coupon=coupon,
        prefered_payment_method=prefered_payment_method,
        total_price=total_price,
        booking_status=BookingStatus.PENDING,
    )

    return reservation