from django.urls import path    
from . import views 

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),  # General overview of reservation-related APIs

    path('hotel/<int:hotel_id>/create/', views.CreateHotelReviewView.as_view(), name='create-hotel-review'),
    path('hotel/<int:hotel_id>/list/', views.HotelReviewListView.as_view(), name='hotel-review-list'), 
]

