from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from social.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
        ]


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSignupSerializer(serializers.ModelSerializer):
    """Create a new user with a hashed password."""

    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
