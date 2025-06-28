from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from accounts.models import User

class VerifiedHotelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True).order_by("-created_at")
    
    def recent(self):
        return self.get_queryset().order_by('-rating')[:5]
class Hotel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hotels',
        limit_choices_to={'role': 'HOTEL_OWNER'}
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    is_verified=models.BooleanField(default=False)
    main_image =models.ImageField(upload_to="hotels/main_images/",blank=True,null=True)
    has_parking = models.BooleanField(default=False)
    policy = models.TextField()
    amenities = models.TextField()

    # Managers
    objects = models.Manager()  # default manager
    verified = VerifiedHotelManager()  # custom manager


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class HotelLocation(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='location')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"Location for {self.hotel.name}"
    
class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/images/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"