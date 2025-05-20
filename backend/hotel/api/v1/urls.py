from django.contrib import admin
from django.urls import path, include
from .views import (RoomView, RoomDetailView,
                    BookingCreateApiView, CheckoutView,
                    CheckedInView, getRoutes,
                    RoomDisplayImagesByRoomView, RoomDisplayImagesListView)

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
    path('room-display-images/', RoomDisplayImagesListView.as_view(), name='room_display_images_list'),
    path('room-display-images/<int:room_id>/', RoomDisplayImagesByRoomView.as_view(), name='room_display_images_by_room'),

]
