from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class CustomerProfile(models.Model):
    slug = models.SlugField(unique=True)
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='customer_profile',
        limit_choices_to={'role': 'CUSTOMER'}
    )
    full_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='customers/profile_images/', blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female')],
        blank=True
    )
    preferred_payment_method = models.CharField(
        max_length=20,
        choices=[
            ('CREDIT_CARD', _('Credit Card')),
            ('PAYPAL', _('PayPal')),
            ('BANK_TRANSFER', _('Bank Transfer'))
        ],
        blank=True,
        null=True
    )
    newsletter_optin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Customer Profile for {self.user.email}"


    def save(self, *args, **kwargs):
        if not self.slug:
            # Automatically generate slug from full_name
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while CustomerProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)