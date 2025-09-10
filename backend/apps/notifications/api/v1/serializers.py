# notifications/serializers.py
from rest_framework import serializers
from apps.notifications.models import Notification

from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "message",
            "notification_type",
            "priority",
            "booking",
            "redirect_url",
            "is_global",
            "is_read",
            "created_at",
        ]
        read_only_fields = ["created_at", "is_read"]


class CustomNotificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    message = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=["info", "warning", "error"], default="info"
    )
    redirect_url = serializers.CharField(required=False)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")


class GlobalNotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=["info", "warning", "error"], default="info"
    )
    redirect_url = serializers.CharField(required=False)
