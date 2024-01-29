from rest_framework import serializers

from social.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model.

    Fields:
    - from_user: User ID sending the friend request.
    - to_user: User ID receiving the friend request.
    - status: Status of the friend request (choices: 'pending', 'accepted', 'rejected').
    - created_at: Timestamp when the friend request was created (auto-generated).
    """

    class Meta:
        model = FriendRequest
        fields = "__all__"
