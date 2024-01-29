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


# class FriendRequestAPIView(APIView):
#     """
#     API view for handling friend requests.

#     Endpoint: /api/users/?search=tejas&page=1
#     Methods:
#     - POST: Send a friend request.
#     - PUT: Accept or reject a friend request.

#     POST Parameters:
#     - from_user: User ID sending the friend request.
#     - to_user: User ID receiving the friend request.

#     PUT Parameters:
#     - action: Action to perform ('accept' or 'reject').

#     Returns:
#     - If successful, returns the friend request details.
#     - If unsuccessful, returns an error response with details.

#     Status Codes:
#     - 201 Created: Friend request sent successfully.
#     - 200 OK: Friend request accepted or rejected successfully.
#     - 400 Bad Request: Invalid input data.
#     - 404 Not Found: Friend request not found.
#     - 500 Internal Server Error: Server error during processing.
#     """

#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         """
#         Send a friend request.

#         :param request: Django REST Framework request object.
#         :return: Response with friend request details or error details.
#         """
#         try:
#             if to_user_id := request.data.get("to_user", None):
#                 return self._extracted_from_post_14(to_user_id, request)
#             return Response(
#                 api_response(
#                     status_code=400,
#                     message={"detail": "to_user is not provided."},
#                 ),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         except User.DoesNotExist:
#             return Response(
#                 api_response(
#                     status_code=400,
#                     message={"detail": "User does not exist."},
#                 ),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         except Exception as e:
#             return Response(
#                 api_response(status_code=500, message=str(e)),
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def _extracted_from_post_14(self, to_user_id, request):
#         to_user = User.objects.filter(pk=to_user_id).first()
#         # Check if the authenticated user matches the 'from_user'
#         if request.user == to_user:
#             return Response(
#                 api_response(
#                     status_code=401,
#                     message={
#                         "detail": "You can only send friend requests on your behalf."
#                     },
#                 ),
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         if existing_request := FriendRequest.objects.filter(
#             from_user=request.user, to_user=to_user
#         ).first():
#             return Response(
#                 api_response(
#                     status_code=400,
#                     message={"detail": "Friend request already exists."},
#                 ),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         friend_request = FriendRequest(
#             from_user=request.user, to_user=to_user, status="pending"
#         )
#         friend_request.save()

#         serializer = FriendRequestSerializer(friend_request)
#         return Response(
#             api_response(status_code=201, data=serializer.data),
#             status=status.HTTP_201_CREATED,
#         )

#     def patch(self, request, *args, **kwargs):
#         try:
#             print(f"\nargs - {args} - {kwargs}\n")
#             pk = self.kwargs.get("pk", None)
#             print(f"\npk - {pk}\n")
#             friend_request = FriendRequest.objects.filter(pk=pk).first()
#             print(f"\nfriend_request - {friend_request}\n")
#             action = request.data.get("action", "reject")
#             print(f"\naction - {action}\n")

#             if action == "accept":
#                 friend_request.status = "accepted"
#             elif action == "reject":
#                 friend_request.status = "rejected"
#             else:
#                 return Response(
#                     api_response(
#                         status_code=400,
#                         message={"detail": "Invalid action."},
#                     ),
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             friend_request.save()
#             serializer = FriendRequestSerializer(friend_request)
#             return Response(
#                 api_response(status_code=200, message=str(e)),
#                 status=status.HTTP_200_OK,
#             )

#         except FriendRequest.DoesNotExist:
#             return Response(
#                 api_response(status_code=404, message=serializer.data),
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Exception as e:
#             print(e)
#             return Response(
#                 api_response(
#                     status_code=500,
#                     message=str(e),
#                 ),
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


class FriendRequestViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
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
