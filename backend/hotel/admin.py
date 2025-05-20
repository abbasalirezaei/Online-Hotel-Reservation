from django.contrib import admin
from .models import (
    Room,
    Category,
    Customer,
    Booking,
    Payment,
    CheckIn,
    CheckOut,
    RoomDisplayImages
)

from django.utils.html import format_html
def update_room_is_booked_to_false(model_admin, request, query_set):
    query_set.update(is_booked=False)


update_room_is_booked_to_false.short_description = "غیرفعال کردن رزرو برای اتاق های انتخاب شده"

class RoomDisplayImagesStacked(admin.StackedInline):
    model = RoomDisplayImages



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomDisplayImagesStacked]
    list_display = ['title', 'category', 'price_per_night', 'is_booked', 'active', 'featured', 'show_cover_image', 'created_at']
    list_editable = ['is_booked', 'active', 'featured']
    list_filter = ['category', 'is_booked', 'active', 'featured', 'bed_type', 'created_at']
    search_fields = ['title', 'room_slug', 'room_code', 'category__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'show_cover_image']
    actions = [update_room_is_booked_to_false]
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('title', 'room_slug', 'category', 'price_per_night', 'discount_price', 'active', 'featured', 'room_code')
        }),
        ('مشخصات اتاق', {
            'fields': ('capacity', 'guests_count', 'room_size', 'bed_count', 'bed_type', 'floor', 'is_booked', 'pets', 'breakfast', 'amenities')
        }),
        ('توضیحات و عکس', {
            'fields': ('short_description', 'description', 'cover_image', 'show_cover_image')
        }),
        ('آمار', {
            'fields': ('rating', 'views', 'created_at', 'updated_at')
        }),
    )

    def show_cover_image(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" style="border-radius:8px;" />', obj.cover_image.url)
        return "-"
    show_cover_image.short_description = "عکس اتاق"

    class Media:
        css = {
            'all': ('admin_rtl.css',),  # اگر فایل راست‌چین ساختید
        }



admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(CheckIn)
admin.site.register(CheckOut)
admin.site.register(RoomDisplayImages)
