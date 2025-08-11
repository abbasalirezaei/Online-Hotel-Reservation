from django.urls import path, include

urlpatterns = [
    path("api/v1/", include(("apps.notifications.api.v1.urls", "notifications"), namespace="notifications")),
]