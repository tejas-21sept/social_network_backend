from django.urls import path

from social.views.users import UserSearchAPIView

urlpatterns = [
    path("", UserSearchAPIView.as_view(), name="user-search"),
]
