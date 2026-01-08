"""
users/urls.py
"""

# core import
from django.urls import path

# views import
from .views import (
    UserListView,
    
    UserRegistrationView,
    ResendingOtpView,
    ActivatingAccountView,    
    
    UserLoginView,
    LoginOtpResendView,
    LoginOtpCheckView,
    
    ForgetPasswordRequestView,
    PasswordResetVerifyOTPView,
    PasswordResetConfirmView,
    PasswordChangeView,
    TokenRefreshViewCustom,
    TokenVerifyViewCustom,

)


urlpatterns = [
    # this shows all users for admin
    path('list/', UserListView.as_view(), name='user-list'),
    
    # user registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('register/activate/via-otp', ActivatingAccountView.as_view(), name='activate-account'),
    path('register/activate/otp/resend/', ResendingOtpView.as_view(), name='resend-otp'),
    
    # user login
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('login/otp/verify/', LoginOtpCheckView.as_view(), name='login-otp'),
    path('login/otp/resend/', LoginOtpResendView.as_view(), name='login-otp-resend'),

    # forget password
    path('forget-password/', ForgetPasswordRequestView.as_view(), name='forget-password'),
    path('forget-password/otp/resend/', ForgetPasswordRequestView.as_view(), name='forget-password-otp-resend'),    
    path('forget-password/otp/verify/', PasswordResetVerifyOTPView.as_view(), name='forget-password-otp'),
    path('forget-password/confirm/', PasswordResetConfirmView.as_view(), name='forget-password-confirm'),

    # change password if logged in
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),

    # token operations
    path('token/refresh/', TokenRefreshViewCustom.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyViewCustom.as_view(), name='token-verify'),

]