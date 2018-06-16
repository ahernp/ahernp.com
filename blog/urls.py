from django.urls import path

from . import views
from . import rss

urlpatterns = [
    path("", views.BlogPageListView.as_view(), name="blogpage-list"),
    path("feed/", rss.LatestBlogPostsFeed(), name="blog-rss-feed"),
    path("<slug:slug>/", views.BlogPageDetailView.as_view(), name="blogpage-detail"),
]
