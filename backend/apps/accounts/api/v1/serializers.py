from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError

from apps.reservations.api.v1.serializers import ReservationListSerializer
from apps.accounts.models import User, CustomerProfile,HotelOwnerProfile
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['is_admin'] = user.groups.filter(name='admin').exists()
        token['is_staff'] = user.is_staff

        return token

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'password2']

    def validate_phone_number(self, value):
        """
        Custom validator for phone number
        """
        if not re.match(r'^\d{10,11}$', value):
            raise serializers.ValidationError("Phone number must be 10 or 11 digits.")

        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if len(password) < 10:
            raise serializers.ValidationError({"password": "Password must be at least 10 characters long."})

        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise serializers.ValidationError({"password": "Password must contain both letters and numbers."})

        if User.objects.filter(email=attrs.get("email")).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        # Django built-in password validators (optional but good)
        validate_password(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        full_name = validated_data.pop("full_name")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=password,
            role=User.Role.CUSTOMER,
            is_active=False  # Require email activation
        )

        # اگر سیگنال باشه خودش ساخته میشه، ولی اگه نباشه:
        if hasattr(user, "customer_profile"):
            user.customer_profile.full_name = full_name
            user.customer_profile.save()

        return user

class ActivationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    
class ResendActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user = None  # Add a user field to store the user instance

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError(
                'User with this email address does not exist.')
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

class UserDashboardSerializer(serializers.ModelSerializer):
    """Serializer for user dashboard view"""
    booking_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone_number',
            'role',
            'date_joined',
            'is_active',
            'booking_history'
        ]
        read_only_fields = [
            'id',
            'email',
            'phone_number',
            'role',
            'date_joined',
            'is_active',
            'booking_history'
        ]

    def get_booking_history(self, obj):
        """
        Returns the user's booking history through their customer profile.
        Filters and serializes related reservations efficiently.
        """
        profile = getattr(obj, 'customer_profile', None)
        if profile:
            reservations_qs = profile.reservations.select_related('room__hotel')
            return ReservationListSerializer(reservations_qs, many=True).data
        return []

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'full_name', 'national_id', 'date_of_birth', 'loyalty_points',
            'address', 'profile_image', 'gender', 'preferred_payment_method',
            'newsletter_optin'
        ]
        read_only_fields = ['loyalty_points']


class HotelOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwnerProfile
        fields = [
            'company_name',
            'business_license_number',
            'bank_account_details',
            'tax_id',
            'is_verified',
            'company_address',
            'phone_number',
            'support_email',
            'website',
            'id_document',
            'logo'
        ]
        read_only_fields = ['is_verified']


class HotelOwnerProfileCreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwnerProfile
        exclude = ['user', 'is_verified', 'slug']