from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User,Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=['id','username','email']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls,user):
		token=super().get_token(user)

		token['full_name']=user.profile.full_name
		token['bio']=user.profile.bio
		token['image']=str(user.profile.image)
		token['verified']=user.profile.verified

		token['email']=user.email
		token['username']=user.username

		return token

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True,
		required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True,
		required=True)

	class Meta:
		model=User
		fields=['username','email','password','password2']

	def validate(self,attrs):
		if attrs['password']!=attrs['password2']:
			raise serializers.ValidationError(
				{"password":"password fields didn't match."}
				)				
		return attrs

	def create(self,validated_data):
		user =User.objects.create(
			username=validated_data['username'],
			email=validated_data['email']
			)
		user.set_password(validated_data['password'])
		user.save()
		return user
	


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user = None  # Add a user field to store the user instance

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError('User with this email address does not exist.')
        self.user = user  # Store the user instance in the serializer
        return value

    def save(self):
        user = self.user  # Retrieve the user from the serializer
        token = default_token_generator.make_token(user)
        user.set_reset_password_token(token)
        user.send_reset_password_email()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError('Invalid password reset token.')

        if not default_token_generator.check_token(user, attrs['token']):
            raise ValidationError('Invalid password reset token.')

        password = attrs['password']
        confirm_password = attrs['confirm_password']

        # Validate password strength
        validate_password(password)

        if password != confirm_password:
            raise ValidationError('Passwords do not match.')

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['password']
        user.set_password(password)
        user.save()