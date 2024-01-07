from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from pages.models import Page

from .serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    http_method_names = ["get", "put"]

    def update(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            page = Page.objects.get(pk=pk)
            page.content = serializer.validated_data["content"]
            page.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkdownToHtmlViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request):
        page = Page(content=request.data.get("content", ""))
        return Response(page.content_as_html)
