from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "priority", "is_read", "created_at")
    list_filter = ("notification_type", "priority", "is_read", "created_at")
    search_fields = ("user__username", "message", "notification_type")
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            None,
            {"fields": ("user", "message", "notification_type", "priority", "booking")},
        ),
        ("Details", {"fields": ("redirect_url", "is_global", "is_read")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
