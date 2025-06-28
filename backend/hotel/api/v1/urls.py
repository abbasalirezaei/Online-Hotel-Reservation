<<<<<<< HEAD
# hotels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),


    path('hotels/', views.HotelListAPIView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('hotels/create/', views.HotelCreateAPIView.as_view(), name='hotel-create'),
    path('hotels/<int:pk>/edit/', views.HotelUpdateAPIView.as_view(), name='hotel-edit'),
    # path('hotels/<int:pk>/rooms/', views.RoomListAPIView.as_view(), name='hotel-room-list'),
    
    path('rooms/create/', views.RoomCreateAPIView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', views.RoomDetailAPIView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/edit/', views.RoomUpdateAPIView.as_view(), name='room-edit'),
    # path('rooms/<int:pk>/availability/', views.RoomAvailabilityAPIView.as_view(), name='room-availability'),
=======
from django.contrib import admin
from django.urls import path, include
from .views import (
    RoomView, RoomDetailView,
    BookingCreateApiView, CheckoutView,
    CheckedInView, getRoutes,
    RoomDisplayImagesByRoomView,
    RoomDisplayImagesListView,
    CategoryListView,
    CategoryDetailView,
)

app_name = 'hotel_app'

urlpatterns = [
    path('', getRoutes),
    path('get_room_list/', RoomView.as_view(), name="room_list"),
    path('get_a_room_detail/<str:room_slug>/',
         RoomDetailView.as_view(), name="single_room"),
    path('book/', BookingCreateApiView.as_view(), name='book_room'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('get_current_checked_in_rooms/',
         CheckedInView.as_view(), name="checked_in_rooms"),
    path('room-display-images/', RoomDisplayImagesListView.as_view(),
         name='room_display_images_list'),
    path('room-display-images/<int:room_id>/',
         RoomDisplayImagesByRoomView.as_view(), name='room_display_images_by_room'),


    # category list and detail
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/',
         CategoryDetailView.as_view(), name='category-detail'),

>>>>>>> ccb84c2f80f19e08022025b5ef9443531670b215
]
