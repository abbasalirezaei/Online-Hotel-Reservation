from rest_framework import permissions

class IsHotelOwner(permissions.BasePermission):
    """
    Custom permission: Only users with role 'HOTEL_OWNER' can create hotels.
    Others can only read.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'HOTEL_OWNER'