from tabnanny import verbose
from django.db import models
from django.utils.text import slugify
from accounts.models import User

# List of models
# Category
# Room
# Customer
# Booking
# Payment
# CheckIn
# CheckOut
# RoomDisplayImages




def category_image_upload_path(instance, filename):
    return f"categories/{instance.slug}/{filename}"


# -------------------------------
# Category Model
# This model stores information about each category, including name.
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name='دسته بندی')
    slug = models.SlugField(unique=True, blank=True,verbose_name='اسلاگ')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
        verbose_name='والد'
    )
    image = models.ImageField(upload_to=category_image_upload_path, null=True, blank=True,verbose_name='تصویر')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"




# -------------------------------
# Room Images Upload Path
# This function returns the path for uploading room images.
# -------------------------------
def room_images_upload_path(instance, file_name):
    return f"{instance.room_slug}/room_cover/{file_name}"

# -------------------------------
# Room Display Images Upload Path
# This function returns the path for uploading room display images.
# -------------------------------
def room_display_images_upload_path(instance, file_name):
    return f"{instance.room.room_slug}/room_display/{file_name}"

# -------------------------------
# Room Model
# This model stores information about each room, including title, slug, bed type, category, and other features.
# -------------------------------
class Room(models.Model):
    BED_TYPES = [
        ('single', 'تک نفره'),
        ('double', 'دو نفره'),
        ('king', 'کینگ'),
        ('twin', 'دوتخته جدا'),
    ]
    title = models.CharField(max_length=30, verbose_name='عنوان اتاق')
    room_slug = models.SlugField(verbose_name='اسلاگ')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='دسته‌بندی')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='قیمت هر شب')
    discount_price = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True,
                                             verbose_name='قیمت تخفیفی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    short_description = models.CharField(max_length=120, blank=True, null=True,                                         verbose_name='توضیح کوتاه')
    is_booked = models.BooleanField(default=False, verbose_name='رزرو شده')
    capacity = models.IntegerField(verbose_name='ظرفیت')
    guests_count = models.IntegerField(default=1, verbose_name='تعداد مهمان')
    room_size = models.CharField(max_length=5, verbose_name='اندازه اتاق')
    bed_count = models.PositiveIntegerField(default=1, verbose_name='تعداد تخت')
    bed_type = models.CharField(max_length=10, choices=BED_TYPES, default='single', verbose_name='نوع تخت')
    floor = models.PositiveIntegerField(default=1, verbose_name='طبقه')
    cover_image = models.ImageField(upload_to=room_images_upload_path, verbose_name='عکس اصلی')
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    pets = models.BooleanField(default=False, verbose_name='اجازه حیوان خانگی')
    breakfast = models.BooleanField(default=True, verbose_name='صبحانه')
    amenities = models.JSONField(default=list, blank=True, verbose_name='امکانات')
    rating = models.FloatField(default=4.5, verbose_name='امتیاز')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    room_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد اتاق')
    active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "اتاق"
        verbose_name_plural = "اتاق ها"

# -------------------------------
# Customer Model
# This model stores information about each customer, including their username and email.
# -------------------------------
class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.username
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"

# -------------------------------
# Booking Model
# This model stores information about each booking, including the customer, room, booking date, checking date, and checkout date.
# -------------------------------
class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(blank=True, null=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.customer.username
    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو ها"

# -------------------------------
# Payment Model
# This model stores information about each payment, including the customer.
# -------------------------------
class Payment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer
    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"   

# -------------------------------
# CheckIn Model
# This model stores information about each check-in, including the customer and room.
# -------------------------------
class CheckIn(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.room.room_slug
    class Meta:
        verbose_name = "چکین"
        verbose_name_plural = "چکین ها"

# -------------------------------
# CheckOut Model
# This model stores information about each check-out, including the customer and check-out date.
# -------------------------------
class CheckOut(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer
    class Meta:
        verbose_name = "چک آوت"
        verbose_name_plural = "چک آوت ها"

# -------------------------------
# RoomDisplayImages Model
# This model stores information about each room display image, including the room and display image.
# -------------------------------
class RoomDisplayImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    display_images = models.ImageField(
        upload_to=room_display_images_upload_path)

    def __str__(self):
        return self.room.room_slug
    class Meta:
        verbose_name = "عکس اتاق"
        verbose_name_plural = "عکس اتاق ها"
