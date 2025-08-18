
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHotelOwnerOrReadOnly(BasePermission):
    """
    Allows read-only access to everyone, but write access only to verified hotel owners.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        profile = getattr(user, 'hotel_owner_profile', None)
        return (
            user.is_authenticated and
            getattr(user, 'role', None) == 'hotel_owner' and
            profile and profile.is_verified
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.hotel.owner == request.user