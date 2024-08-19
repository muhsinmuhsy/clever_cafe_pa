from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/trade-service/register/', views.TradeServiceUserRegisterView.as_view(), name='trade-service-register'),
    path('api/food-service/register/', views.FoodServiceUserRegisterView.as_view(), name='food-service-register'),
    path('api/cafe-entrepreneurship/register/', views.CafeEntrepreneurshipUserRegisterView.as_view(), name='food-service-register'),
    # path('api/verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('api/verify-otp/<int:user_id>/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('api/resend-otp/<int:user_id>/', views.ResendOTPView.as_view(), name='resend-otp'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/test/auth/', views.TestAuthView.as_view(), name='test-auth'),
    
    path('api/test/auth/', views.TestAuthView.as_view(), name='test-auth'),
    
    path('api/user/detail/', views.UserView.as_view(), name='user-view'),
    path('api/ceuser/list/', views.CeListView.as_view()), 
    path('api/user/<int:user_id>/detail/', views.UserDetalView.as_view())
]