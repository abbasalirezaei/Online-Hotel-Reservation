from django.urls import path,include

app_name='reservations'
urlpatterns = [
   
    path("api/v1/", include("reservations.api.v1.urls")),
]