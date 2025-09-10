# import pytest
# from apps.notifications.models import Notification
# from apps.notifications.tasks import send_custom_notification
# from .factories import HotelOwnerProfileFactory

# @pytest.mark.django_db
# def test_notify_on_hotel_owner_approval():
#     profile = HotelOwnerProfileFactory(is_verified=False)
#     user = profile.user

#     profile.is_verified = True
#     profile.save()

#     send_custom_notification(
#         user.id,
#         message="Your hotel owner request has been approved. You can now create your hotel.",
#         priority="info",
#         redirect_url="/hotel-owner-profile/"
#     )

#     notif = Notification.objects.get(user=user)
#     assert "approved" in notif.message.lower()