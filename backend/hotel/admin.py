from django.contrib import admin
from .models.hotel_model import Hotel, HotelLocation, HotelImage
from .models.room_model import Room, RoomImage

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class HotelLocationInline(admin.StackedInline):
    model = HotelLocation
    extra = 0
    max_num = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'rating', 'has_parking', 'created_at')
    list_filter = ('has_parking', 'rating', 'created_at', 'owner')
    search_fields = ('name', 'owner__username', 'location__city', 'location__country')
    inlines = [HotelLocationInline, HotelImageInline]
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'description', 'rating', 'phone_number', 'email', 'website')
        }),
        ('Details', {
            'fields': ('has_parking','is_verified', 'policy', 'amenities')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'room_type',  'price_per_night', 'capacity', 'is_available', 'rating', 'created_at')
    list_filter = ('hotel', 'room_type',  'is_available', 'rating', 'created_at')
    search_fields = ('title', 'hotel__name')
    inlines = [RoomImageInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('hotel', 'title', 'slug', 'room_type', 'bed_type', 'price_per_night', 'capacity', 'guests_count')
        }),
        ('Features', {
            'fields': ('has_balcony', 'has_air_conditioning', 'has_tv', 'pets', 'room_details', 'floor', 'is_available', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(HotelLocation)
class HotelLocationAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'country', 'city', 'postal_code', 'address')
    search_fields = ('hotel__name', 'city', 'country')

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'caption', 'image')
    search_fields = ('hotel__name', 'caption')

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'caption', 'image')
    search_fields = ('room__title', 'caption')