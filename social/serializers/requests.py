from rest_framework import serializers

from social.models import FriendRequest
from social.serializers.user import UserSerializer


# social/serializers.py
class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer class for FriendRequest model instances.

    Attributes:
    - from_user_data: Serialized representation of the 'from_user' field using UserSerializer.
    - to_user_data: Serialized representation of the 'to_user' field using UserSerializer.

    Meta:
    - model: The model class associated with this serializer.
    - fields: The fields to be included in the serialized output.
    """

    from_user_data = UserSerializer(source="from_user", read_only=True)
    to_user_data = UserSerializer(source="to_user", read_only=True)

    class Meta:
        """
        Meta class for FriendRequestSerializer.

        Attributes:
        - model: The model class associated with this serializer.
        - fields: The fields to be included in the serialized output.
        """

        model = FriendRequest
        fields = [
            "id",
            "status",
            "created_at",
            "from_user",
            "from_user_data",
            "to_user",
            "to_user_data",
        ]
