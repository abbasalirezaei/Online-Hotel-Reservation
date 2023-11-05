from django.urls import path
from . import views

app_name="accounts_v1"
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path("home/",  views.HomeView.as_view()),
    path('', views.getRoutes),

    # password rest
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),

    
]