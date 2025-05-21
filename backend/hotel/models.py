from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import User
from django.core.validators import RegexValidator
    
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
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="شماره تلفن باید با فرمت صحیح وارد شود. مثل: +989121234567"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=14, null=True, blank=True, verbose_name="شماره تلفن",db_index=True)
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس")
    national_id = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد ملی")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد",db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی",db_index=True)
    
    def __str__(self):
        return self.customer.username
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['national_id']),
        ]
# -------------------------------
# Booking Model
# This model stores information about each booking, including the customer, room, booking date, checking date, and checkout date.
# -------------------------------

class Booking(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('cancelled', 'لغو شده'),
    ]
    BOOKING_STATUS = [
    ('pending', 'در انتظار تایید'),
    ('confirmed', 'تایید شده'),
    ('cancelled', 'لغو شده'),
    ('completed', 'تکمیل شده'),
    ('no_show', 'عدم حضور'),
]
    PAYMENT_METHODS = [
    ('online', 'آنلاین'),
    ('cash', 'نقدی'),
    ('card', 'کارت'),
]
    # booking information
    room = models.ForeignKey('Room', on_delete=models.CASCADE,related_name='room_bookings',verbose_name='اتاق')

    # customer information
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='user_bookings',verbose_name='مشتری')
    phone_number = models.CharField(max_length=14, null=True,verbose_name='شماره تلفن')
    email = models.EmailField(verbose_name='ایمیل')
    
    # payment status
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='online',verbose_name='روش پرداخت')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending',verbose_name='وضعیت پرداخت')
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="کد پیگیری پرداخت")
    
    # booking status
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending',verbose_name='وضعیت رزرو')


    # important date
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ لغو رزرو")
    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(blank=True, null=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # prices
    nights = models.PositiveIntegerField(default=1, verbose_name="تعداد شب اقامت")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت نهایی')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True,verbose_name='کد تخفیف')
    
    # gustes 
    guests_count = models.PositiveIntegerField(default=1,verbose_name='تعداد مهمان')
    guest_note = models.TextField(blank=True, null=True,verbose_name='توضیحات مهمان')
    
    def __str__(self):
        return self.customer.customer.username
    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو ها"
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['room']),
        ]
    @property
    def calculated_nights(self):
        if self.checking_date and self.checkout_date:
            return (self.checkout_date - self.checking_date).days
        return self.nights
    @property
    def calculate_total_price(self):
        base_price = self.room.price_per_night
        discount = self.coupon.discount_percent if self.coupon else 0
        total_price = base_price * self.nights * (1 - discount / 100)
        return total_price

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="کد تخفیف")
    discount_percent = models.PositiveIntegerField(verbose_name="درصد تخفیف")
    valid_from = models.DateTimeField(verbose_name="شروع اعتبار")
    valid_to = models.DateTimeField(verbose_name="پایان اعتبار")
    active = models.BooleanField(default=True, verbose_name="فعال")

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"

    
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
        indexes = [
            models.Index(fields=['customer']),
        ]
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
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['room']),
        ]
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
        indexes = [
            models.Index(fields=['customer']),
        ]
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
        indexes = [
            models.Index(fields=['room']),
        ]
