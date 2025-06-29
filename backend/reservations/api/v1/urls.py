# hotels/urls.py
from django.urls import path
from . import views


urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),
    path('rooms/<int:room_id>/reserve/', views.RoomReservationCreateView.as_view(), name='room-reserve'),
    path('my/', views.UserReservationListView.as_view(), name='user-reservations'),
    path('<int:pk>/cancel/', views.CancelReservationView.as_view(), name='cancel-reservation'),
    path('owner/', views.HotelOwnerReservationListView.as_view(), name='owner-reservations'),

]
