from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Notification(models.Model):
    TYPE_CHOICES = [
        ('reserved', 'Reserved'),
        ('rejected', 'Rejected'),
        ('checkin_reminder', 'Checkin Reminder'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('review_submitted', 'Review Submitted'),
        ('reply_submitted', 'Reply Submitted'),
        ('custom', 'Custom'),
    ]

    PRIORITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='info')
    booking = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, null=True, blank=True)

    redirect_url = models.URLField(blank=True, null=True)  
    is_global = models.BooleanField(default=False)      
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"🔔 {self.user or 'ALL'} → {self.notification_type} ({self.priority})"