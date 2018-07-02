from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mpages.models import Page

from .serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    http_method_names = ['get', 'patch']
