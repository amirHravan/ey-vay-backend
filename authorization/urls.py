from django.urls import path
from .views import (
    SendVerificationCodeView,
    VerifyCodeView,
    RegisterBuyerView,
    LoginView,
    LogoutView,
    RefreshTokenView,
)

urlpatterns = [
    path('auth/send-verification-code/', SendVerificationCodeView.as_view(), name='send-verification-code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('auth/register/buyer/', RegisterBuyerView.as_view(), name='register-buyer'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
]
