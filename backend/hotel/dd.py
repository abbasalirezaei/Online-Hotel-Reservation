from django.db import models

from accounts.models import Customer, User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


def room_images_upload_path(instance, file_name):
    return f"{instance.room_slug}/room_cover/{file_name}"


def room_display_images_upload_path(instance, file_name):
    return f"{instance.room.room_slug}/room_display/{file_name}"


'''
Hotels # I didn't created yet
Room
Room Images
Booking

Check In
Check Out
Payments



'''


class Room(models.Model):
    title = models.CharField(max_length=30)
    room_slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=3)

    description = models.TextField(blank=True, null=True)

    is_booked = models.BooleanField(default=False)
    capacity = models.IntegerField()
    room_size = models.CharField(max_length=5)
    cover_image = models.ImageField(upload_to=room_images_upload_path)
    featured = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="book")
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(blank=True, null=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.customer.username


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer


class CheckIn(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.room.room_slug


class CheckOut(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer


class RoomDisplayImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    display_images = models.ImageField(
        upload_to=room_display_images_upload_path)

    def __str__(self):
        return self.room.room_slug
