from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("check-email/", views.check_email, name="check_username"),
    path("adminusers/", AdminUsersView.as_view(), name="admin-users"),
    path('user-info/<int:user_id>/', views.get_user_info, name='get_user_info'),  # Nueva URL
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", UserInfoAPIView.as_view(), name="user-info")
]
