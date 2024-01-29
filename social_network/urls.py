from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("social.urls.auth_urls")),
    path("api/users/", include("social.urls.users")),
]
