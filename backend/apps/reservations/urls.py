from django.urls import path,include

app_name='reservations'
urlpatterns = [
   
    path("api/v1/", include("apps.reservations.api.v1.urls")),
]