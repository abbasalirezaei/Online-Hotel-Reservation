# notifications/serializers.py
from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'notification_type', 'priority',
            'booking', 'redirect_url', 'is_global', 'is_read', 'created_at'
        ]
        read_only_fields = ['created_at', 'is_read']