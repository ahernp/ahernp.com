from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import BlogPage


class BlogPageListView(ListView):
    model = BlogPage


class BlogPageDetailView(DetailView):
    model = BlogPage


class BlogPageLatestView(RedirectView):
    pattern_name = 'blogpage-detail'

    def get_redirect_url(*args, **kwargs):
        latest_blogpage = BlogPage.objects.all().first()
        if latest_blogpage is not None:
            return latest_blogpage.get_absolute_url()
        else:
            return None
