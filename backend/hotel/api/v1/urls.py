# hotels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),

    # Hotel endpoints
    path('hotels/', views.HotelListCreateView.as_view(), name='hotel-list-create'),  # List all hotels or create a new one
   
]