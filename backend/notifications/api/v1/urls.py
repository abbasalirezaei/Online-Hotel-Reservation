from django.urls import path    
from . import views 

urlpatterns = [
    # Overview of available endpoints
    path('', views.api_overview, name='api-overview'),  # General overview of reservation-related APIs
    path('', views.UserNotificationsListView.as_view(), name='list-notifications'),
    path('<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='mark-read-notification'),
    path('custom/', views.SendCustomNotificationAPIView.as_view(), name='send-custom-notification'),
    path('global/', views.SendGlobalNotificationAPIView.as_view(), name='send-global-notification'),

]
