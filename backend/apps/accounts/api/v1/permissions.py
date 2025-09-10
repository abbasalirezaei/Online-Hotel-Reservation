from rest_framework import permissions
from apps.accounts.models import HotelOwnerProfile

from rest_framework.permissions import BasePermission


class IsVerifiedHotelOwner(BasePermission):
    """
    Allows access only to authenticated users with role 'hotel_owner'
    and a verified hotel owner profile.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.role != "hotel_owner":
            return False

        profile = getattr(user, "hotel_owner_profile", None)
        return profile and profile.is_verified is True


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
