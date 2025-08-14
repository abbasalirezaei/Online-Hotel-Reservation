from email import message
from django.http import response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.urls import reverse

from apps.accounts.models import User
from apps.accounts.tasks import send_activation_email_task
from .permissions import IsVerifiedHotelOwner,IsCustomer
from apps.notifications.tasks import send_custom_notification
from .serializers import (
    UserSerializer,
    CustomerProfileSerializer,
    HotelOwnerProfileSerializer,
    HotelOwnerProfileCreateRequestSerializer,
    MyTokenObtainPairSerializer,
    RegistrationSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ActivationCodeSerializer,
    ResendActivationCodeSerializer,
    UserDashboardSerializer,
)


from apps.accounts.models import HotelOwnerProfile


@api_view(['GET'])
def getRoutes(request):
    """
    Returns available API endpoints for inspection/debugging.
    """
    routes = [
        'token/',
        'token/refresh/',
        'register/',
        'activate/code/',
        'activation/resend/',
        'customer-profile/',
        'hotel-owner-profile/',
        'request-hotel-owner/', 
        'dashboard/',

        'password/reset/',
        'password/reset/confirm/',
        'password/change/',
    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    JWT token generation endpoint.
    """
    serializer_class = MyTokenObtainPairSerializer


class RegistrationApiView(generics.GenericAPIView):
    """
    Handles user registration and sends activation code.
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            return Response({
                "email": email,
                "message": "Account created successfully. Please check your email to activate your account."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyActivationCodeAPIView(APIView):
    """
    Verifies the activation code and activates the user's account.
    """

    def post(self, request):
        serializer = ActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data["code"]
            try:
                user = User.objects.get(active_code=code)
            except User.DoesNotExist:
                return Response({"error": "Invalid activation code."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_active:
                return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)

            if user.active_code_expires_at and user.active_code_expires_at < timezone.now():
                return Response({"error": "Activation code has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.active_code = None
            user.active_code_expires_at = None
            user.save(update_fields=["is_active",
                      "active_code", "active_code_expires_at"])
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendActivationCodeAPIView(APIView):
    """
    Resends activation code via email for inactive users.
    """

    def post(self, request):
        serializer = ResendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

            if user.is_active:
                return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)

            send_activation_email_task.delay(user.id, user.email)
            return Response({"message": "Activation code resent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    """
    Sends password reset email with token and UID.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"http://localhost:3000/password/reset/confirm/?uid={uid}&token={token}"
        subject = 'Reset your password'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url
        })
        send_mail(subject, message, 'ali@gmail.com', [user.email])
        return Response({
            'detail': 'Password reset email sent.',
            'uid': uid,
            'token': token
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Confirms and sets new password using token and UID.
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password has been reset successfully.'})


class ChangePasswordView(APIView):
    """
    Allows authenticated user to change their current password.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"detail": "New password and confirmation do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({"detail": "Password changed successfully"})


class UserDashboardView(APIView):
    """
    Returns dashboard data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDashboardSerializer(request.user)
        return Response(serializer.data)


class CustomerProfileView(RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated customer's profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get_object(self):
        return self.request.user.customer_profile



class RequestHotelOwnerView(CreateAPIView):
    """
    POST /hotel-owner/request/
    Allows authenticated customers to request to become hotel owners.
    Creates HotelOwnerProfile with is_verified=False.
    Sends notification to user that request is submitted.
    """
    serializer_class = HotelOwnerProfileCreateRequestSerializer
    permission_classes = [IsCustomer]
    queryset = HotelOwnerProfile.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user

        # Check if the user has already submitted a request
        if HotelOwnerProfile.objects.filter(user=user).exists():
            return Response(
                {"detail": "You have already submitted a hotel owner request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with creating the profile
        response = super().create(request, *args, **kwargs)

        # Send notification to the user
        send_custom_notification.delay(
            user.id,
            message="Your request to become a hotel owner has been submitted. You will be notified once it's reviewed by an admin.",
            priority="info",
            redirect_url="/hotel-owner-profile/"
        )

        return response

    def perform_create(self, serializer):
        # Save the profile with is_verified=False (pending admin approval)
        serializer.save(user=self.request.user, is_verified=False)

class HotelOwnerProfileView(RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated hotel owner's profile.
    """
    permission_classes = [IsVerifiedHotelOwner]
    serializer_class = HotelOwnerProfileSerializer

    def get_object(self):
        return self.request.user.hotel_owner_profile
    
