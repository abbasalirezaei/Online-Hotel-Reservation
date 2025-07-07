from django.urls import path
from . import views

app_name = "reservations_v1"

urlpatterns = [
    #  Overview of available endpoints
    path('', views.api_overview, name='api-overview'),  # General overview of reservation-related APIs

    #  Reservation Actions
    path('rooms/<int:room_id>/reserve/', views.RoomReservationCreateView.as_view(), name='room-reserve'),  # Create a reservation for a room
    path('my/', views.UserReservationListView.as_view(), name='user-reservations'),  # List current user's reservations
    path('<int:pk>/cancel/', views.CancelReservationView.as_view(), name='cancel-reservation'),  # Cancel a reservation if allowed

    #  Hotel Owner Section
    path('owner/', views.HotelOwnerReservationListView.as_view(), name='owner-reservations'),  # List reservations for hotels owned by current user

    #  Invoice & Reporting
    path('<int:pk>/invoice/', views.ReservationInvoiceAPIView.as_view(), name='reservation-invoice'),  # View invoice for a reservation
    path('report/', views.ReservationReportView.as_view(), name='reservation-report'),  # Daily bookings and revenue report for hotel owner


    path("report/monthly/", views.MonthlyReservationReportView.as_view(), name="monthly-reservation-report"),
    path("report/by-room/", views.RoomWiseReservationReportView.as_view(), name="room-wise-report"),
]