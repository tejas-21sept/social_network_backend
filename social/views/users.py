from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from social.models import FriendRequest, User
from social.serializers.requests import FriendRequestSerializer
from social.serializers.search import UserSearchSerializer
from social.serializers.user import UserSerializer
from social.utils.responses import api_response


class UserSearchAPIView(APIView):
    """
    API view for searching users by email or name with pagination.

    Endpoint: /api/users/?search=tejas&page=1
    Method: GET

    Parameters (in query parameters):
    - search: Search keyword (email or name)
    - page: Page number for pagination (default is 1)

    Returns:
    - If search keyword matches an exact email, returns the associated user.
    - If the search keyword contains any part of the name, returns a paginated list of users.
    - If no results are found, returns a 404 response.

    Status Codes:
    - 200 OK: Successful response with user data.
    - 404 Not Found: No results found.
    - 500 Internal Server Error: Server error during the search process.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            search_keyword = request.query_params.get("search", "")
            page_number = request.query_params.get("page", 1)

            if User.objects.filter(email__iexact=search_keyword).exists():
                queryset = User.objects.filter(email__iexact=search_keyword)
            else:
                queryset = User.objects.filter(
                    Q(first_name__icontains=search_keyword)
                    | Q(last_name__icontains=search_keyword)
                )

            paginator = Paginator(queryset, 10)
            try:
                page_users = paginator.page(page_number)
            except Exception as e:
                return Response(
                    api_response(status_code=404, message="No more results."),
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = UserSearchSerializer(page_users, many=True)
            return Response(
                api_response(status_code=200, data=serializer.data),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                api_response(status_code=500, message=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FriendRequestViewSet(viewsets.GenericViewSet):
    """
    A ViewSet for handling FriendRequest operations.

    Attributes:
    - permission_classes: List of permission classes to apply for authentication.
    - authentication_classes: List of authentication classes to apply for user authentication.
    - queryset: Queryset representing all FriendRequest objects.
    - serializer_class: Serializer class to use for FriendRequest serialization.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new FriendRequest.

        Parameters:
        - request: The request object containing data for creating the FriendRequest.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: HTTP response indicating the success or failure of the request.
        """
        try:
            if to_user_id := request.data.get("to_user", None):
                return self._extracted_from_post_14(to_user_id, request)
            return Response(
                api_response(
                    status_code=400,
                    message={"detail": "to_user is not provided."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                api_response(
                    status_code=400,
                    message={"detail": "User does not exist."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                api_response(status_code=500, message=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _extracted_from_post_14(self, to_user_id, request):
        """
        Extract and process the creation of a FriendRequest.

        Parameters:
        - to_user_id: ID of the user to whom the friend request is sent.
        - request: The request object.

        Returns:
        - Response: HTTP response indicating the success or failure of the request.
        """
        to_user = User.objects.filter(pk=to_user_id).first()
        # Check if the authenticated user matches the 'from_user'
        if request.user == to_user:
            return Response(
                api_response(
                    status_code=401,
                    message={
                        "detail": "You can only send friend requests on your behalf."
                    },
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if existing_request := FriendRequest.objects.filter(
            from_user=request.user, to_user=to_user
        ).first():
            return Response(
                api_response(
                    status_code=400,
                    message={"detail": "Friend request already exists."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request = FriendRequest(
            from_user=request.user, to_user=to_user, status="pending"
        )
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(
            api_response(status_code=201, data=serializer.data),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update the status of a FriendRequest.

        Parameters:
        - request: The request object containing data for updating the FriendRequest status.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: HTTP response indicating the success or failure of the request.
        """
        try:
            friend_request = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
            friend_request = self.get_object()
            action = request.data.get("action", "reject")

            if request.user == friend_request.to_user:
                if action == "accept":
                    friend_request.status = "accepted"
                elif action == "reject":
                    friend_request.status = "rejected"
                else:
                    return Response(
                        api_response(
                            status_code=400,
                            message={"detail": "Invalid action."},
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                friend_request.save()
                serializer = FriendRequestSerializer(friend_request)
                return Response(
                    api_response(status_code=200, data=serializer.data),
                    status=status.HTTP_200_OK,
                )
            return Response(
                api_response(
                    status_code=403,
                    message={
                        "detail": "You don't have permission to modify this request."
                    },
                ),
                status=status.HTTP_403_FORBIDDEN,
            )

        except FriendRequest.DoesNotExist:
            return Response(
                api_response(
                    status_code=404,
                    message={"detail": "Friend request not found."},
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                api_response(
                    status_code=500,
                    message={"detail": str(e)},
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FriendsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            friends = User.objects.filter(
                received_requests__from_user=user, received_requests__status="accepted"
            )
            serializer = self.get_serializer(friends, many=True)
            return Response(
                api_response(
                    status_code=200,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                api_response(
                    status_code=500,
                    message={"detail": str(e)},
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
