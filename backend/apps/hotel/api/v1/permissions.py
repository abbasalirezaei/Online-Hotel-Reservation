
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHotelOwnerOrReadOnly(BasePermission):
    """
    Allows read-only access to everyone, but write access only to verified hotel owners.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return (
            user.is_authenticated and
            user.role == 'hotel_owner' and
            hasattr(user, 'hotel_owner_profile') and
            user.hotel_owner_profile.is_verified
        )