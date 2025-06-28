from django.db import models

from django.utils.text import slugify
from .hotel_model import Hotel




class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50, choices=[
        ('Single', 'Single'),
        ('Double', 'Double'), 
        ('Suite', 'Suite'),
        ('Deluxe', 'Deluxe'),
    ])
    occupancy = models.IntegerField(help_text="Maximum number of guests allowed")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    guests_count = models.IntegerField(default=1)
    room_details = models.TextField(help_text="Additional room details and amenities")
    # fetured
    has_balcony = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    pets = models.BooleanField(default=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    floor = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=4.5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} - {self.hotel.name}"
    



class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room/images/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.room.name}"