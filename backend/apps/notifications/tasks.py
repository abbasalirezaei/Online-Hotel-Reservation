from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification
from apps.reservations.models import Reservation

User = get_user_model()


@shared_task
def send_custom_notification(user_id, message, priority='info', redirect_url=None):
    """
    Send a custom notification to a specific user.
    - Runs asynchronously via Celery.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User with ID {user_id} not found."

    Notification.objects.create(
        user=user,
        message=message,
        notification_type='custom',
        priority=priority,
        redirect_url=redirect_url
    )
    return f"Notification sent to user {user.email}."


@shared_task
def send_global_notification(message, priority='info', redirect_url=None):
    """
    Send a global notification visible to all users.
    - Creates a single Notification instance with is_global=True.
    """
    Notification.objects.create(
        user=None,
        message=message,
        notification_type='custom',
        priority=priority,
        redirect_url=redirect_url,
        is_global=True
    )
    return "Global notification created for all users."


@shared_task
def notify_new_booking(reservation_id):
    """
    Notify hotel owner about a new reservation.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    hotel = reservation.room.hotel
    hotel_owner = hotel.owner
    guest_email = reservation.user.user.email  # CustomerProfile → user
    msg = f"You have a new booking for {hotel.name} by {guest_email}."
    Notification.objects.create(
        user=hotel_owner,
        message=msg,
        notification_type='reserved'
    )


@shared_task
def notify_booking_cancelled(reservation_id):
    """
    Notify hotel owner that a booking was cancelled.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    hotel = reservation.room.hotel
    hotel_owner = hotel.owner
    msg = f"Booking #{reservation.id} for {hotel.name} has been cancelled."
    Notification.objects.create(
        user=hotel_owner,
        message=msg,
        notification_type='cancelled'
    )


@shared_task
def remind_checkin(reservation_id):
    """
    Remind guest to check in tomorrow.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    guest_user = reservation.user.user  # CustomerProfile → user
    hotel_name = reservation.room.hotel.name
    msg = f"Reminder: Your check-in for {hotel_name} is tomorrow."
    Notification.objects.create(
        user=guest_user,
        message=msg,
        notification_type='checkin_reminder'
    )


@shared_task
def notify_checked_in(reservation_id):
    """
    Notify hotel owner when guest has checked in.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    hotel = reservation.room.hotel
    hotel_owner = hotel.owner
    guest_email = reservation.user.user.email
    msg = f"Guest {guest_email} has checked in."
    Notification.objects.create(
        user=hotel_owner,
        message=msg,
        notification_type='checked_in'
    )


@shared_task
def notify_checked_out(reservation_id):
    """
    Notify hotel owner when guest has checked out.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    hotel = reservation.room.hotel
    hotel_owner = hotel.owner
    guest_email = reservation.user.user.email
    msg = f"Guest {guest_email} has checked out."
    Notification.objects.create(
        user=hotel_owner,
        message=msg,
        notification_type='checked_out'
    )


@shared_task
def daily_checkin_reminders():
    """

    Periodic task: remind guests who have check-in tomorrow.
    Should be scheduled via Celery Beat.
    
    """
    from datetime import date, timedelta
    tomorrow = date.today() + timedelta(days=1)
    reservations = Reservation.objects.filter(checking_date=tomorrow, booking_status='pending')
    for reservation in reservations:
        remind_checkin.delay(reservation.id)
    return f"Sent reminders for {reservations.count()} reservations"
