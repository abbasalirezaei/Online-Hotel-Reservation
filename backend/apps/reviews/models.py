# reviews/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.hotel.models import Hotel
User = get_user_model()


class Review(models.Model):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')   # for reply 
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} rated {self.hotel.name} ★{self.rating}"
