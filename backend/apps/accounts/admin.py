from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.user_model import User
from .models.customer_profile_model import CustomerProfile
from .models.hotel_owner_profile_model import HotelOwnerProfile
# Inline for CustomerProfile
class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'

# Inline for HotelOwnerProfile
class HotelOwnerProfileInline(admin.StackedInline):
    model = HotelOwnerProfile
    can_delete = False
    verbose_name_plural = 'Hotel Owner Profile'
    fk_name = 'user'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'phone_number')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'role', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2', 'phone_number', 'is_active', 'is_staff')}
        ),
    )

    inlines = []

    def get_inlines(self, request, obj):
        if obj is None:
            return []
        if obj.role == 'customer':
            return [CustomerProfileInline]
        elif obj.role == 'hotel_owner':
            return [HotelOwnerProfileInline]
        return []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = self.get_inlines(request, self.model.objects.get(pk=object_id))
        return super().change_view(request, object_id, form_url, extra_context)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'national_id', 'date_of_birth', 'loyalty_points', 'gender', 'newsletter_optin')
    search_fields = ('user__email', 'full_name', 'national_id')
    list_filter = ('gender', 'newsletter_optin')
    readonly_fields = ('slug',)



@admin.register(HotelOwnerProfile)
class HotelOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'business_license_number', 'is_verified', 'phone_number')
    search_fields = ('user__email', 'company_name', 'business_license_number')
    list_filter = ('is_verified',)
    readonly_fields = ('slug',)
    actions = ['mark_as_verified']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__role='hotel_owner')

    @admin.action(description="Mark selected profiles as verified")
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} profile(s) successfully marked as verified.")