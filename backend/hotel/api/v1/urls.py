# hotels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),


    path('hotels/', views.HotelListAPIView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('hotels/create/', views.HotelCreateAPIView.as_view(), name='hotel-create'),
    path('hotels/<int:hotel_id>/locations/', views.HotelLocationCreateAPIView.as_view(), name='hotel-create-locations'),

    
    path('hotels/<int:hotel_id>/rooms/', views.RoomListAPIView.as_view(), name='room-lists'),
    path('hotels/rooms/<slug:slug>/', views.RoomDetailAPIView.as_view(), name='room-detail'),
    path('hotels/<int:hotel_id>/rooms/create/', views.RoomCreateAPIView.as_view(), name='room-create'),
    path('hotels/rooms/<int:room_id>/images/', views.RoomImageCreateAPIView.as_view(), name='room-images'),
    # path('rooms/<int:pk>/', views.RoomDetailAPIView.as_view(), name='room-detail'),
    # path('rooms/<int:pk>/edit/', views.RoomUpdateAPIView.as_view(), name='room-edit'),
    # path('rooms/<int:pk>/availability/', views.RoomAvailabilityAPIView.as_view(), name='room-availability'),
]
