from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import User
from social.serializers.search import UserSearchSerializer
from social.utils.responses import api_response


class UserSearchAPIView(APIView):
    """
    API view for searching users by email or name with pagination.

    Endpoint: /api/search/?search=tejas&page=1
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
