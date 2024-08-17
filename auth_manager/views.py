from rest_framework import generics
from .serializers import (
    TradeServiceUserRegisterSerializer, FoodServiceUserRegisterSerializer, CafeEntrepreneurshipUserRegisterSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import User
from .serializers import VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

import random
from django.core.mail import send_mail

class TradeServiceUserRegisterView(generics.CreateAPIView):
    serializer_class = TradeServiceUserRegisterSerializer

class FoodServiceUserRegisterView(generics.CreateAPIView):
    serializer_class = FoodServiceUserRegisterSerializer

# {
#     "username": "",
#     "email": "",
#     "email2": "",
#     "phone_number": "",
#     "password": "",
#     "password2": "",
#     "first_name": "",
#     "last_name": "",
#     "state": "",
#     "post_code": ""
# }  

class CafeEntrepreneurshipUserRegisterView(generics.CreateAPIView):
    serializer_class = CafeEntrepreneurshipUserRegisterSerializer
# {
#     "username": "",
#     "email": "",
#     "email2": "",
#     "phone_number": "",
#     "password": "",
#     "password2": "",
#     "first_name": "",
#     "last_name": "",
#     "state": "",
#     "post_code": "",
#     "subscription_type":""
# }



# class VerifyOTPView(APIView):
#     serializer_class = VerifyOTPSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             otp = serializer.validated_data['otp']
#             user = User.objects.filter(email=email).first()
#             if user and user.otp == otp:
#                 time_elapsed = timezone.now() - user.otp_created_at
#                 if time_elapsed <= timedelta(minutes=10):
#                     user.is_active = True
#                     user.otp = None
#                     user.otp_created_at = None
#                     user.save()
#                     return Response({'message': 'Account verified successfully.'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'error': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def put(self, request, user_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            user = User.objects.filter(id=user_id).first()
            # user = User.objects.get(id=user_id)
            if user and user.otp == otp:
                time_elapsed = timezone.now() - user.otp_created_at
                if time_elapsed <= timedelta(minutes=10):
                    user.is_active = True
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        'message': 'Account verified successfully.',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid OTP or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ResendOTPView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.filter(email=email).first()

#             if user:
#                 # Generate a new OTP
#                 otp = str(random.randint(100000, 999999))
#                 user.otp = otp
#                 user.otp_created_at = timezone.now()
#                 user.save()

#                 # Send OTP via email
#                 subject = 'Your New OTP Code'
#                 message = f'Your new OTP code is {otp}. It is valid for 10 minutes.'
#                 from_email = 'your_email@example.com'
#                 recipient_list = [email]

#                 send_mail(subject, message, from_email, recipient_list)
#                 return Response({'message': 'OTP resent successfully.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new OTP
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP via email
        subject = 'Your New OTP Code'
        message = f'Your new OTP code is {otp}. It is valid for 10 minutes.'
        from_email = 'your_email@example.com'
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return Response({'error': 'Failed to send OTP email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'OTP resent successfully.'}, status=status.HTTP_200_OK)

class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, requset):
        user = requset.user
        return Response({'message':'your authed', 'user': str(user.username)})
    
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'is_trade_service_user': user.is_trade_service_user,
                'is_food_service_user': user.is_food_service_user,
                'is_cafe_entrepreneurship_user': user.is_cafe_entrepreneurship_user
            },
            'profile': {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'state': profile.state,
                'post_code': profile.post_code,
                'subscription_type': profile.subscription_type,
            }
        }
        return Response({'message': 'Authenticated', 'data': response_data})
    
        