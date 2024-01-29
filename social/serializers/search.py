from rest_framework import serializers

from social.models import User


class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, including all fields.

    Note: The 'password' field is marked as write-only for security reasons.
    """

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class UserKeywordSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, including specific fields suitable for keyword searches.

    Fields included: 'id', 'email', 'first_name', 'last_name'.
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
