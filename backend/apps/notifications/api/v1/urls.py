from django.urls import path
from . import views


app_name = "notifications"
urlpatterns = [
    # Overview of available endpoints
    path(
        "", views.api_overview, name="api-overview"
    ),  # General overview of reservation-related APIs
    path("list/", views.UserNotificationsListView.as_view(), name="list-notifications"),
    path(
        "<int:pk>/read/",
        views.MarkNotificationReadView.as_view(),
        name="mark-read-notification",
    ),
    path(
        "custom/",
        views.SendCustomNotificationAPIView.as_view(),
        name="send-custom-notification",
    ),
    path(
        "global/",
        views.SendGlobalNotificationAPIView.as_view(),
        name="send-global-notification",
    ),
]
