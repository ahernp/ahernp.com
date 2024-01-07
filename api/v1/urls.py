from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from .views import MarkdownToHtmlViewSet, PageViewSet

router = routers.SimpleRouter()
router.register("pages", PageViewSet)

urlpatterns = [
    path("docs/", include_docs_urls(title="ahernp.com")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "markdown-to-html",
        MarkdownToHtmlViewSet.as_view({"post": "update"}),
        name="markdown-to-html",
    ),
    path("", include(router.urls)),
]
