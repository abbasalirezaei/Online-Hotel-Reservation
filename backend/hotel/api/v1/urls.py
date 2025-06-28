# hotels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),

    # Hotel endpoints
    path('hotels/', views.HotelListCreateView.as_view(), name='hotel-list-create'),  # List all hotels or create a new one
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),  # Retrieve hotel details by ID
    path('hotels/<int:hotel_id>/location/', views.HotelLocationView.as_view(), name='hotel-location'),  # Manage hotel location

]