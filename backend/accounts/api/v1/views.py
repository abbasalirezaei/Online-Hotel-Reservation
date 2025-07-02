from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str


from accounts.models import User
from accounts.tasks import send_activation_email_task

from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    RegistrationSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ActivationCodeSerializer,
    ResendActivationCodeSerializer,

)


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token/',
        'token/refresh/',
        'register/',
        'test/',
        'home/',
        'password/reset/',
        'password/reset/confirm/',
        'password/change/',

    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email": email,
                "message": "Account created successfully, please check your email to activate your account."
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyActivationCodeAPIView(APIView):
    def post(self, request):
        serializer = ActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data["code"]

            try:
                user = User.objects.get(active_code=code)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid or expired activation code."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user.is_active:
                return Response(
                    {"message": "Your account is already activated."},
                    status=status.HTTP_200_OK
                )

            user.is_active = True
            user.active_code = None
            user.save(update_fields=["is_active", "active_code"])

            return Response(
                {"message": "Your account has been activated successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendActivationCodeAPIView(APIView):
    def post(self, request):
        serializer = ResendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "No account found with this email."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if user.is_active:
                return Response(
                    {"message": "This account is already activated."},
                    status=status.HTTP_200_OK
                )

            # Send activation code (via celery or directly)
            send_activation_email_task.delay(user.id, user.email)

            return Response(
                {"message": "Activation code resent successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response_data': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response_data': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

#  ==============================================================================


class HomeView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        content = {
            'message': 'Welcome to the JWT Authentication page using React Js and Django!',
            'data': serializer.data

        }
        return Response(content)


#  ==============================================================================


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user  # Access the 'user' field from the serializer

        # Generate the reset password token
        token = default_token_generator.make_token(user)

        # Build the reset password URL
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('accounts:accounts_v1:password_reset_confirm')
        reset_url = f'http://localhost:3000/password/reset/confirm/?uid={uid}&token={token}'

        # Email the reset password link to the user
        subject = 'Reset your password'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url
        })
        send_mail(subject, message, 'ali@gmail.com', [user.email])

        return Response(
            {'detail': 'Password reset email has been sent.', 'uid': uid, 'token': token

             }, status=status.HTTP_200_OK)

#  ==============================================================================


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get(
            'confirm_password')

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            return Response({"detail": "New password and confirmation do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the current password is correct
        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and update the session authentication hash
        user.set_password(new_password)
        user.save()
        # Update the session hash to avoid logging out the user
        update_session_auth_hash(request, user)

        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
