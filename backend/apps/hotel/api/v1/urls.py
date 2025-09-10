# hotels/urls.py
from django.urls import path
from . import views
from .views import HotelAmenitiesViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# CRUD operations for hotel amenities
router.register(r'hotels/(?P<hotel_id>\d+)/amenities', HotelAmenitiesViewSet, basename='hotel-amenities')

app_name = 'api_v1'

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),

    # CRUD operations Hotel endpoints
    path('hotels/', views.HotelListCreateView.as_view(), name='hotel-list-create'),  # List all hotels or create a new one
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),  # Retrieve hotel details by ID
    
    # CRUD operations for hotel images
    path('hotels/<int:hotel_id>/images/', views.HotelImageListCreateView.as_view(), name='hotel-image-list-create'),
    path('hotels/<int:hotel_id>/images/<int:image_id>/', views.HotelImageDetailView.as_view(), name='hotel-image-detail'),  # Retrieve or delete a specific hotel image
    
    
    # CRUD operations for hotel location
    path('hotels/<int:hotel_id>/location/',views.HotelLocationView.as_view(),name='hotel-location'),
    path('hotels/<int:hotel_id>/location/<int:pk>/', views.HotelLocationDetailView.as_view(),name='hotel-location-detail'),

    # Room endpoints
    path('hotels/<int:hotel_id>/rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),  # List or create rooms for a hotel
    path('rooms/<slug:slug>/', views.RoomDetailView.as_view(), name='room-detail'),  # Room detail view by slug


    path('hotels/owner/', views.OnwerHotelListView.as_view(), name='my-hotels'),
    # Room image endpoints
    path('rooms/<int:room_id>/images/', views.RoomImageListCreateView.as_view(), name='room-images'),  # List or upload images for a room

] + router.urls  # Include the router URLs for hotel amenities