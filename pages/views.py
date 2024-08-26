from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Page


class PageListView(ListView):
    model = Page
    parent = None

    def get_queryset(self):
        parent_slug = self.kwargs.get("parent_slug", None)
        if parent_slug:
            self.parent = get_object_or_404(Page, slug=parent_slug)
            return Page.objects.filter(parent=self.parent)
        return Page.objects.all().select_related("parent")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent"] = self.parent
        return context


class PageDetailView(DetailView):
    model = Page
