from django.http import response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status


from .permissions import IsVerifiedHotelOwner, IsCustomer

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

from apps.accounts.services import (
    validate_activation_code,
    resend_activation_code,
    send_password_reset_email,
    change_user_password,
    request_hotel_owner
)


from apps.accounts.services import request_hotel_owner
from apps.accounts.exceptions import AlreadyHotelOwnerError
from apps.accounts.exceptions import (
    PasswordMismatchError,
    ActivationCodeError,
    AlreadyHotelOwnerError
)


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
    def post(self, request):
        serializer = ActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data["code"]
            try:
                user = validate_activation_code(code)
            except ActivationCodeError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.active_code = None
            user.active_code_expires_at = None
            user.save(update_fields=["is_active",
                      "active_code", "active_code_expires_at"])
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendActivationCodeView(generics.GenericAPIView):
    """
    Resends activation code via email for inactive users.
    """
    serializer_class = ResendActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            resend_activation_code(email)
        except ActivationCodeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Activation code resent successfully."}, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    """
    Sends password reset email with token and UID.
    """

    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        uid, token = send_password_reset_email(user)
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
        try:
            change_user_password(
                user, request, current_password,
                new_password, confirm_password)
        except PasswordMismatchError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    Allows authenticated customers to request to become hotel owners.
    """
    serializer_class = HotelOwnerProfileCreateRequestSerializer
    permission_classes = [IsCustomer]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile = request_hotel_owner(user, serializer.validated_data)
        except AlreadyHotelOwnerError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(profile).data, status=status.HTTP_201_CREATED)


class HotelOwnerProfileView(RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated hotel owner's profile.
    """
    permission_classes = [IsVerifiedHotelOwner]
    serializer_class = HotelOwnerProfileSerializer

    def get_object(self):
        return self.request.user.hotel_owner_profile
