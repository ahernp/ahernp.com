from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import BlogPage


class BlogPageListView(ListView):
    model = BlogPage


class BlogPageDetailView(DetailView):
    model = BlogPage
