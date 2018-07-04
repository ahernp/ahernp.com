from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mpages.models import Page

from .serializers import MarkdownToHtmlSerializer, PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    http_method_names = ['get', 'patch']


class MarkdownToHtmlViewSet(viewsets.ViewSet):
    serializer_class = MarkdownToHtmlSerializer,

    def update(self, request):
        page = Page(content=request.POST.get("content", ""))
        serializer = MarkdownToHtmlSerializer(instance=page)
        return Response(serializer.data)
