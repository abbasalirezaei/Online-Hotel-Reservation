from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("reviews.api.v1.urls")),    
]   