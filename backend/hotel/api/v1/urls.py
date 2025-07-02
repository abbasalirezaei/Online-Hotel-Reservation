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
    path('hotels/<int:hotel_id>/images/', views.HotelImageListCreateView.as_view(), name='hotel-image-list-create'),


    # Room endpoints
    path('hotels/<int:hotel_id>/rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),  # List or create rooms for a hotel
    path('rooms/<slug:slug>/', views.RoomDetailView.as_view(), name='room-detail'),  # Room detail view by slug

    # Room image endpoints
    path('rooms/<int:room_id>/images/', views.RoomImageListCreateView.as_view(), name='room-images'),  # List or upload images for a room

]