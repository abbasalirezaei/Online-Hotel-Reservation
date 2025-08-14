from celery import shared_task
from django.core.mail import send_mail
from apps.reservations.models import Reservation
from apps.reservations.models import BookingStatus


@shared_task(bind=True, max_retries=5)
def send_reservation_cancellation_email(self, reservation_id):
    """
    Sends a cancellation email to the user associated with a reservation.

    This Celery task retrieves the reservation by its ID, extracts relevant
    user and hotel information, and sends a personalized email notifying
    the user that their reservation has been cancelled.

    Retries up to 5 times in case the reservation is not found (e.g., due to
    eventual consistency or delayed database updates).

    Args:
        self: The task instance (used for retry logic).
        reservation_id (int): The ID of the reservation to cancel.

    Raises:
        self.retry: If the reservation does not exist, the task will retry
        with exponential backoff.
    """

    
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

    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@shared_task
def cancel_unpaid_reservation(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        if reservation.booking_status == BookingStatus.PENDING:
            reservation.booking_status = BookingStatus.CANCELLED
            reservation.save()
            print(
                f"Reservation {reservation_id} cancelled due to non-payment.")
    except Reservation.DoesNotExist:
        pass
