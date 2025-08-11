from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("apps.reviews.api.v1.urls")),    
]   