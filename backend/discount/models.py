from django.db import models
from django.utils import timezone



# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True,verbose_name="Discount Code")
    discount_percent = models.PositiveIntegerField(verbose_name="Discount Percentage")
    start_date = models.DateTimeField(verbose_name="Valid From")
    end_date = models.DateTimeField(verbose_name="Valid To")
    active = models.BooleanField(default=True, verbose_name="Active")

    def is_valid(self):
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
