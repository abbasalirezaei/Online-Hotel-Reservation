from django.urls import path,include

app_name='hotel'
urlpatterns = [
   
    path("api/v1/", include("apps.hotel.api.v1.urls",namespace="api_v1")),
]