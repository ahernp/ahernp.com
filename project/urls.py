from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/pages/ahernp-com"), name="homepage"),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("feedreader/", include("feedreader.urls")),
    path("pages/", include("mpages.urls")),
    path("timers/", include("timers.urls")),
    path("tools/", include("tools.urls")),
]
