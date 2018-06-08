from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url='/pages/ahernp-com')),
    path("admin/", admin.site.urls),
    path("api/pages/", include("pages.urls")),
    path("pages/", include("markdown.urls")),
    path("blog/", include("blog.urls")),
]
