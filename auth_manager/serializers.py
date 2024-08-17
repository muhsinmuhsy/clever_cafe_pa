from rest_framework import serializers
from .models import User, UserProfile
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework.exceptions import ValidationError
from cafe_entrepreneurship.models import Branch as CafeEntrepreneurshipBranch

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'state', 'post_code', 'subscription_type']

class TradeServiceUserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    email2 = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    state = serializers.CharField(source='profile.state')
    post_code = serializers.CharField(source='profile.post_code')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email2', 'phone_number', 'password', 'password2', 'first_name', 'last_name', 'state', 'post_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        """
        Check that the email addresses and passwords match.
        """
        if data['email'] != self.initial_data['email2']:
            raise serializers.ValidationError({"email": "Email addresses must match."})

        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')

        # Check for inactive users with the same username or email and remove them if they are too old
        expiration_time = timezone.now() - timedelta(hours=24)
        User.objects.filter(
            username=username, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        User.objects.filter(
            email=email, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        
        # Check if a user with the same active email exists
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError({'email': 'A user with this email already exists and is active.'})
        
        validated_data.pop('email2')
        validated_data.pop('password2')
        
        profile_data = validated_data.pop('profile')
        
        otp = str(random.randint(1000, 9999))
        validated_data['otp'] = otp
        validated_data['otp_created_at'] = timezone.now()

        user = User.objects.create_user(**validated_data)
        user.is_trade_service_user = True
        user.is_active = False
        user.save()

        UserProfile.objects.create(user=user, **profile_data)

        # Send OTP via email
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
        from_email = 'your_email@example.com'
        recipient_list = [validated_data['email']]

        send_mail(subject, message, from_email, recipient_list)

        return user
    
class FoodServiceUserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    email2 = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    state = serializers.CharField(source='profile.state')
    post_code = serializers.CharField(source='profile.post_code')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email2', 'phone_number', 'password', 'password2', 'first_name', 'last_name', 'state', 'post_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        """
        Check that the email addresses and passwords match.
        """
        if data['email'] != self.initial_data['email2']:
            raise serializers.ValidationError({"email": "Email addresses must match."})

        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')

        # Check for inactive users with the same username or email and remove them if they are too old
        expiration_time = timezone.now() - timedelta(hours=24)
        User.objects.filter(
            username=username, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        User.objects.filter(
            email=email, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        
        # Check if a user with the same active email exists
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError({'email': 'A user with this email already exists and is active.'})
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError({'email': 'A user with this email already exists and is active.'})

        validated_data.pop('email2')
        validated_data.pop('password2')
        
        profile_data = validated_data.pop('profile')
        
        otp = str(random.randint(1000, 9999))
        validated_data['otp'] = otp
        validated_data['otp_created_at'] = timezone.now()

        user = User.objects.create_user(**validated_data)
        user.is_food_service_user = True
        user.is_active = False 
        user.save()

        UserProfile.objects.create(user=user, **profile_data)

        # Send OTP via email
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
        from_email = 'your_email@example.com'
        recipient_list = [validated_data['email']]

        send_mail(subject, message, from_email, recipient_list)

        return user

class CafeEntrepreneurshipUserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    email2 = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    state = serializers.CharField(source='profile.state')
    post_code = serializers.CharField(source='profile.post_code')
    operational_status = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'email2', 'phone_number', 'password', 'password2',
            'first_name', 'last_name', 'state', 'post_code', 'operational_status'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        """
        Check that the email addresses and passwords match.
        """
        if data['email'] != self.initial_data['email2']:
            raise serializers.ValidationError({"email": "Email addresses must match."})

        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        
        # Check for inactive users with the same username or email and remove them if they are too old
        expiration_time = timezone.now() - timedelta(hours=24)
        User.objects.filter(
            username=username, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        User.objects.filter(
            email=email, is_active=False, otp_created_at__lt=expiration_time
        ).delete()
        
        # Check if a user with the same active email exists
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError({'email': 'A user with this email already exists and is active.'})

        validated_data.pop('email2')
        validated_data.pop('password2')
        
        profile_data = validated_data.pop('profile')
        operational_status = validated_data.pop('operational_status')
        
        otp = str(random.randint(1000, 9999))
        validated_data['otp'] = otp
        validated_data['otp_created_at'] = timezone.now()

        user = User.objects.create_user(**validated_data)
        user.is_cafe_entrepreneurship_user = True
        user.is_active = False 
        user.save()

        UserProfile.objects.create(user=user, **profile_data)
        
        CafeEntrepreneurshipBranch.objects.create(user=user, operational_status=operational_status)

        # Send OTP via email
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
        from_email = 'your_email@example.com'
        recipient_list = [validated_data['email']]

        send_mail(subject, message, from_email, recipient_list)

        return user

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be numeric.")
        return value


