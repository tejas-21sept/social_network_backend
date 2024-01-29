from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from social.serializers.user import (
    UserLoginSerializer,
    UserSerializer,
    UserSignupSerializer,
)
from social.utils.responses import api_response


class UserSignupAPIView(APIView):
    """
    API view for user signup.

    Endpoint: /api/auth/signup/
    Method: POST

    Parameters (in request body):
    - username: User's username
    - email: User's email address
    - password: User's password

    Returns:
    - If successful, returns an access token for the new user.
    - If unsuccessful, returns an error response with details.

    Status Codes:
    - 201 Created: User successfully created.
    - 400 Bad Request: Invalid input data.
    - 500 Internal Server Error: Server error during user creation.
    """

    def post(self, request):
        """
        Handle POST request for user signup.

        :param request: Django REST Framework request object.
        :return: Response with access token or error details.
        """
        try:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response(
                    api_response(status_code=201, data={"access_token": access_token}),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                api_response(status_code=400, data=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                api_response(status_code=500, data=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserLoginAPIView(APIView):
    """
    API view for user login.

    Endpoint: /api/auth/login/
    Method: POST

    Parameters (in request body):
    - username: User's username
    - password: User's password

    Returns:
    - If successful, returns an access token for the authenticated user.
    - If unsuccessful, returns an error response with details.

    Status Codes:
    - 201 Created: User successfully authenticated.
    - 401 Unauthorized: Invalid credentials.
    - 400 Bad Request: Invalid input data.
    - 500 Internal Server Error: Server error during authentication.
    """

    def post(self, request):
        """
        Handle POST request for user login.

        :param request: Django REST Framework request object.
        :return: Response with access token or error details.
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = authenticate(
                    username=serializer.validated_data["username"],
                    password=serializer.validated_data["password"],
                )

                if user is None:
                    return Response(
                        api_response(
                            status_code=401,
                            data=serializer.errors,
                            message="Invalid credentials",
                        ),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response(
                    api_response(status_code=201, data={"access_token": access_token}),
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                api_response(status_code=400, data=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                api_response(status_code=500, data=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
