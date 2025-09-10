from django.db import models

from django.utils.text import slugify


class HotelOwnerProfile(models.Model):
    slug = models.SlugField(unique=True)
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="hotel_owner_profile",
        limit_choices_to={"role": "hotel_owner"},
    )
    company_name = models.CharField(max_length=100)
    business_license_number = models.CharField(max_length=50, unique=True)
    bank_account_details = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    company_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    support_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    id_document = models.ImageField(
        upload_to="hotel_owners/documents/ids/", blank=True, null=True
    )
    logo = models.ImageField(upload_to="hotel_owners/logos/", blank=True, null=True)

    def __str__(self):
        return f"Hotel Owner Profile for {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Automatically generate slug from full_name
            base_slug = slugify(self.company_name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while HotelOwnerProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
