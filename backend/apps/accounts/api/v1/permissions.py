from rest_framework import permissions
from apps.accounts.models import HotelOwnerProfile

class IsVerifiedHotelOwner(permissions.BasePermission):
    """
    Only allows verified hotel owners
    """ 

    def has_permission(self, request, view):
        user = request.user
        if not user or user.role not in ['HOTEL_OWNER', 'BOTH']:
            return False

        try:
            profile = user.hotel_owner_profile
            return profile.is_verified is True
        except HotelOwnerProfile.DoesNotExist:
            return False