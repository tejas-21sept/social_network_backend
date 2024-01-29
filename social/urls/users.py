from django.urls import path

from social.views.users import (
    FriendRequestViewSet,
    FriendsListViewSet,
    UserSearchAPIView,
    PendingFriendRequestsViewSet,
)

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
    path(
        "friends/",
        FriendsListViewSet.as_view({"get": "list"}),
        name="friends-list",
    ),
    path(
        "pending-requests/",
        PendingFriendRequestsViewSet.as_view({"get": "list"}),
        name="pending-friend-requests",
    ),
]
