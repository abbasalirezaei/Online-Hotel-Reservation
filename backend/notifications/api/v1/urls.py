from django.urls import path    
from . import views 

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),  # General overview of reservation-related APIs
    path('', views.UserNotificationsListView.as_view(), name='list-notifications'),
    path('<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='mark-read-notification'),
    path('create/', CreateCustomNotificationView.as_view(), name='create-notification'),

]
