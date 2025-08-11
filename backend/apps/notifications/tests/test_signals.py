import pytest
from apps.notifications.models import Notification
from apps.reviews.models import Review

pytestmark = pytest.mark.django_db

def test_review_triggers_notification(user_factory, hotel_factory):
    """ Signal: should notify hotel owner when new review is created"""
    reviewer = user_factory()
    hotel_owner = user_factory()
    hotel = hotel_factory(owner=hotel_owner)

    review = Review.objects.create(
        user=reviewer,
        hotel=hotel,
        rating=4,
        comment="Great stay!"
    )

    notif = Notification.objects.get(user=hotel_owner)
    assert "New review submitted" in notif.message
    assert notif.notification_type == "review_submitted"

def test_reply_triggers_notification(user_factory, hotel_factory):
    """ Signal: should notify original reviewer when a reply is posted"""
    original_reviewer = user_factory()
    replier = user_factory()
    hotel = hotel_factory(owner=user_factory())
    parent_review = Review.objects.create(
        user=original_reviewer,
        hotel=hotel,
        rating=5,
        comment="Loved it!"
    )

    reply = Review.objects.create(
        user=replier,
        hotel=hotel,
        parent=parent_review,
        rating=4,
        comment="Thanks!"
    )

    notif = Notification.objects.get(user=original_reviewer)
    assert "replied to your review" in notif.message
    assert notif.notification_type == "reply_submitted"