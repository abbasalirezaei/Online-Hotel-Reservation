from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@shared_task
def send_custom_notification(user_id, message, priority='info', redirect_url=None):
    """
    Task: Send a custom notification to a single user.
    - Creates a Notification instance.
    - Runs async via Celery.
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
    Task: Send a global notification to all users.
    - Creates one Notification with `is_global=True`.
    - All users see it.
    """
    Notification.objects.create(
        user=None,  # Global → no specific user
        message=message,
        notification_type='custom',
        priority=priority,
        redirect_url=redirect_url,
        is_global=True
    )
    return "Global notification created for all users."
