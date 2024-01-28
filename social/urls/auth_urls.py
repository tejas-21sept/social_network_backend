from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from social.views.authentication import UserLoginAPIView, UserSignupAPIView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", UserSignupAPIView.as_view(), name="user-signup"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
]
