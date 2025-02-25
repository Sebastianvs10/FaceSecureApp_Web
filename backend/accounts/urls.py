# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import *

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("check-email/", views.check_email, name="check_email"),
    path("adminusers/", AdminUsersView.as_view(), name="admin-users"),
    path('user-info/<int:user_id>/', views.get_user_info, name='get_user_info'),  # Nueva URL
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", UserInfoAPIView.as_view(), name="user-info")
]
