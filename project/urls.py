from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pages/", include("pages.urls")),
    path("pages/", include("markdown.urls")),
    path("blog/", include("blog.urls")),
]
