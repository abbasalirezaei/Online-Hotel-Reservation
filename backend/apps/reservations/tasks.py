from celery import shared_task
from django.core.mail import send_mail
from apps.reservations.models import Reservation

@shared_task
def send_reservation_cancellation_email(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        user = reservation.user
        full_name = user.full_name
        hotel_name = reservation.room.hotel.name

        send_mail(
            subject="Reservation Cancelled",
            message=(
                f"Hi {full_name},\n\n"
                f"Your reservation at {hotel_name} from {reservation.checking_date} "
                f"to {reservation.checkout_date} has been successfully cancelled.\n\n"
                f"We hope to host you another time!"
            ),
            from_email="no-reply@hotel.com",
            recipient_list=[user.user.email],
            fail_silently=False
        )

    except Reservation.DoesNotExist:
        pass  