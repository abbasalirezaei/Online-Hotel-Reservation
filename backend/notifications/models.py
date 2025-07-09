from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
# Create your models here.


class Notification(models.Model):
    TYPE_CHOICES = [
        ('reserved', 'Reserved'),
        ('rejected', 'Rejected'),
        ('checkin_reminder', 'Checkin Reminder'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    booking = models.ForeignKey(
        'booking.Bookings', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
