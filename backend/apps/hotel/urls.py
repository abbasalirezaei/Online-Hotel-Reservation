from django.urls import path,include

app_name='hotel'
urlpatterns = [
   
    path("api/v1/", include("hotel.api.v1.urls")),
]