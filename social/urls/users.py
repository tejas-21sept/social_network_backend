from django.urls import path

from social.views.users import FriendRequestViewSet, UserSearchAPIView

urlpatterns = [
    path("", UserSearchAPIView.as_view(), name="user-search"),
    path(
        "friend-requests/",
        FriendRequestViewSet.as_view({"post": "create"}),
        name="friend-requests",
    ),
    path(
        "friend-requests/<int:pk>",
        FriendRequestViewSet.as_view({"patch": "update"}),
        name="friend-request-detail",
    ),
]
