from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from notifications.tasks import send_custom_notification, send_global_notification
from notifications.models import Notification
from .serializers import NotificationSerializer

User = get_user_model()

@api_view(['GET'])
def api_overview(request):
    """
    Quick overview for devs: lists key notification-related endpoints.
    """
    return Response({
        "API Overview": "overview/",
        "List Notifications (GET)": "notifications/",
        "Mark Notification as Read (POST)": "notifications/<int:pk>/read/",
        "Send Custom Notification (POST)": "notifications/custom/",
        "Send Global Notification (POST)": "notifications/global/"
    })


class UserNotificationsListView(APIView):
    """
    List all notifications for the authenticated user.
    Includes global notifications.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all notifications for the authenticated user.
        Includes global notifications.

        Returns:
        - A JSON response with a list of notifications for the authenticated user.
        """ 
        user = request.user
        qs = Notification.objects.filter(
            models.Q(user=user) | models.Q(is_global=True)
        ).order_by('-created_at')
        serializer = NotificationSerializer(qs, many=True)
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    """
    Mark a specific notification as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Mark a specific notification as read.
        
        Parameters:
        - `pk`: The ID of the notification to mark as read.
        
        Returns:
        - A JSON response with a success message if the notification is marked as read.
        - A JSON response with an error message if the notification is not found.
        """
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({"detail": "Notification marked as read"})
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class SendCustomNotificationAPIView(APIView):
    """
    Send a custom notification to a specific user (via Celery task).
    """
    def post(self, request):
        """
        Send a custom notification to a specific user (via Celery task).

        Parameters:
        - `user_id`: The ID of the user to send the notification to.
        - `message`: The message to be sent.
        - `priority`: The priority of the message (default: 'info').
        - `redirect_url`: A URL to redirect the user to after reading the message.

        Returns a JSON response with a success message if the notification is sent successfully.        
        """
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        priority = request.data.get('priority', 'info')
        redirect_url = request.data.get('redirect_url')

        if not user_id or not message:
            return Response(
                {'error': 'User ID and message are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_custom_notification.delay(user_id, message, priority, redirect_url)
        return Response(
            {'message': 'Custom notification sent'},
            status=status.HTTP_200_OK
        )


class SendGlobalNotificationAPIView(APIView):
    """
    Send a global notification to all users (via Celery task).
    """
    def post(self, request):
        """
        Send a global notification to all users (via Celery task).

        Parameters:
        - `message`: The message to be sent.
        - `priority`: The priority of the message (default: 'info').
        - `redirect_url`: A URL to redirect the user to after reading the message.

        Returns a JSON response with a success message if the notification is sent successfully.
        """     
        message = request.data.get('message')
        priority = request.data.get('priority', 'info')
        redirect_url = request.data.get('redirect_url')

        if not message:
            return Response(
                {'error': 'Message is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_global_notification.delay(message, priority, redirect_url)
        return Response(
            {'message': 'Global notification sent '},
            status=status.HTTP_200_OK
        )
