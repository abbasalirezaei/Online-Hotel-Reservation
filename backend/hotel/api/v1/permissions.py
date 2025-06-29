from rest_framework import permissions

class IsHotelOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to read, but only hotel owners can create.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'HOTEL_OWNER'