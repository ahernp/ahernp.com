from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/pages/ahernp-com"), name="homepage"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    path("blog/", include("blog.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("feedreader/", include("feedreader.urls")),
    path("pages/", include("pages.urls")),
    path("core/", include("core.urls")),
    path("timers/", include("timers.urls")),
    path("tools/", include("tools.urls")),
    path("quiz/", include("quiz.urls")),
]
