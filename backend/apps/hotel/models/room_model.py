from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.text import slugify
from .hotel_model import Hotel


class AvailableRoomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True).order_by("-created_at")


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(
        max_length=50,
        choices=[
            ("Single", "Single"),
            ("Double", "Double"),
            ("Suite", "Suite"),
            ("Deluxe", "Deluxe"),
        ],
    )

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

    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        default=0,
    )
    main_image = models.ImageField(upload_to="room/images/main_image/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()  # default manager
    available = AvailableRoomManager()  # custom manager

    def __str__(self):
        return f"{self.title} - {self.hotel.name}"

    def save(self, *args, **kwargs):
        # generate a unique slug from the title if not provided
        if not self.slug:
            base = slugify(self.title) or "room"
            slug_candidate = base
            counter = 1
            # exclude self to allow updates without false positive conflict
            while Room.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base}-{counter}"
                counter += 1
            self.slug = slug_candidate

        super().save(*args, **kwargs)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room/images/")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.room.title}"
