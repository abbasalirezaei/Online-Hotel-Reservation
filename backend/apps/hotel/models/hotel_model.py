from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class VerifiedHotelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True).order_by("-created_at")


class Hotel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hotels",
        limit_choices_to={"role": "hotel_owner"},
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(r"^\+?1?\d{9,15}$", message=_("Enter a valid phone number."))
        ],
    )
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    is_verified = models.BooleanField(default=False)
    main_image = models.ImageField(
        upload_to="hotels/main_images/", blank=True, null=True
    )
    has_parking = models.BooleanField(default=False)

    policy = models.TextField()
    amenities = models.ManyToManyField(
        "Amenity",
        related_name="hotels",
        blank=True,
        help_text=_("Select amenities available at the hotel."),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Managers
    objects = models.Manager()
    verified = VerifiedHotelManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_verified"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["slug"]),
        ]
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="amenities/icons/", null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class HotelLocation(models.Model):
    hotel = models.OneToOneField(
        Hotel, on_delete=models.CASCADE, related_name="location"
    )
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.TextField()

    class Meta:
        verbose_name = _("Hotel Location")
        verbose_name_plural = _("Hotel Locations")
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["hotel"]),
        ]

    def __str__(self):
        return f"Location for {self.hotel.name}"


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="hotels/images/")
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("Hotel Image")
        verbose_name_plural = _("Hotel Images")
        indexes = [
            models.Index(fields=["hotel"]),
        ]

    def __str__(self):
        return f"Image for {self.hotel.name}"
