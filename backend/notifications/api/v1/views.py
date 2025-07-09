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
        "Submit Review for Hotel (POST)": "hotel/<hotel_id>/create/",
        "List Hotel Reviews (GET)": "hotel/<hotel_id>/list/",
        "API Overview": "overview/"
    })


class UserNotificationsListView(APIView):
    """
    List all notifications for the authenticated user.
    Includes global notifications.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({"detail": "Notification marked as read ✅"})
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
            {'message': 'Custom notification sent ✅'},
            status=status.HTTP_200_OK
        )


class SendGlobalNotificationAPIView(APIView):
    """
    Send a global notification to all users (via Celery task).
    """
    def post(self, request):
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
            {'message': 'Global notification sent ✅'},
            status=status.HTTP_200_OK
        )
