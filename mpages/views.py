from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Page


class PageListView(ListView):
    model = Page


class PageDetailView(DetailView):
    model = Page
