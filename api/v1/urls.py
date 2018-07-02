from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from django.urls import path, include

from .views import PageViewSet

router = routers.DefaultRouter()
router.register("pages", PageViewSet)

urlpatterns = [
    path("docs", include_docs_urls(title="ahernp.com")),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
 ]
