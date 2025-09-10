from django.urls import path, include


app_name = "accounts"
urlpatterns = [
    path("api/v1/", include("apps.accounts.api.v1.urls")),
]
