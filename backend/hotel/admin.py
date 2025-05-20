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
    """
    Room Admin Configuration
    ------------------------
    This admin configuration manages the display and management of rooms in the Django admin interface.

    Features:
    - Displays room title, category, price per night, booking status, activity status, featured status, cover image, and creation date in list view
    - Allows editing of booking status, activity status, and featured status
    - Filters rooms by category, booking status, activity status, featured status, bed type, and creation date
    - Provides search functionality for room title, room slug, room code, and category name
    - Orders rooms by creation date in descending order
    - Shows cover image thumbnail in list view
    - Optimizes queries by selecting related category
    - Includes an action to update booking status to false for selected rooms
    - Provides fieldsets for room details, room features, room images, and room statistics

    Usage:
    - View all rooms in a hierarchical structure
    - Create new rooms with optional category, price per night, booking status, activity status, featured status, cover image, and room code
    - Edit room details including title, category, price per night, booking status, activity status, featured status, cover image, and room code
    - Search through rooms using title, slug, code, or category name
    - Filter rooms by category, booking status, activity status, featured status, bed type, and creation date
    - Update booking status to false for selected rooms
    - View room statistics including rating, views, and creation date
    """
    inlines = [RoomDisplayImagesStacked]
    list_display = ['title', 'category', 'price_per_night', 'is_booked',
                    'active', 'featured', 'show_cover_image', 'created_at']
    list_editable = ['is_booked', 'active', 'featured']
    list_filter = ['category', 'is_booked', 'active',
                   'featured', 'bed_type', 'created_at']
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


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category Admin Configuration
    ---------------------------
    This admin configuration manages the display and management of categories in the Django admin interface.

    Features:
    - Displays category name with its hierarchy level
    - Shows parent category name
    - Displays category slug and image
    - Filters categories by parent category
    - Provides search functionality for category name and slug
    - Automatically generates slug from category name
    - Shows category image thumbnail in list view
    - Optimizes queries by selecting related parent category
    """

    def get_hierarchy(self, obj):
        """Returns the category name with its hierarchy level"""
        if not obj.parent:
            return obj.name
        return f"{obj.parent.name} → {obj.name}"
    get_hierarchy.short_description = 'دسته‌بندی سلسله‌مراتبی'

    def get_parent_name(self, obj):
        """Returns the parent category name"""
        return obj.parent.name if obj.parent else '-'
    get_parent_name.short_description = 'والد'

    list_display = ('get_hierarchy', 'get_parent_name', 'slug', 'image_tag')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if hasattr(obj, 'image') and obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: contain;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'تصویر'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'phone_number', 'national_id', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'phone_number', 'national_id', 'address')
    list_filter = ('created_at', 'updated_at', 'date_of_birth')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('customer', 'phone_number', 'address', 'national_id', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(CheckIn)
admin.site.register(CheckOut)
admin.site.register(RoomDisplayImages)
