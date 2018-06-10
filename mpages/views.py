from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from .models import Page


class PageListView(ListView):
    model = Page

    def get_queryset(self):
        parent_slug = self.kwargs.get('parent_slug', None)
        if parent_slug:
            parent = get_object_or_404(Page, slug=parent_slug)
            return Page.objects.filter(parent=parent)
        return Page.objects.all()


class PageDetailView(DetailView):
    model = Page
