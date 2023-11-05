from rest_framework_simplejwt.views import TokenObtainPairView



from rest_framework.permissions import AllowAny ,  IsAuthenticated
from rest_framework.decorators import permission_classes , api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import generics,status


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str





from accounts.models import User,Profile



from .serializers import (
	UserSerializer,
	MyTokenObtainPairSerializer,
	RegisterSerializer,
      PasswordResetSerializer, PasswordResetConfirmSerializer

	)



# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        

    ]
    return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class=MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
	queryset=User.objects.all()
	permission_classes=[AllowAny]
	serializer_class=RegisterSerializer


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




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
class HomeView(APIView):
     
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {
              'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    


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
            {'detail': 'Password reset email has been sent.','uid':uid,'token':token
              
            }, status=status.HTTP_200_OK)

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
        confirm_password = request.data.get('confirm_password')  # Add this line

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            return Response({"detail": "New password and confirmation do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the current password is correct
        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and update the session authentication hash
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Update the session hash to avoid logging out the user

        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)