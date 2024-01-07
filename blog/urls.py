from django.urls import path

from . import rss, views

urlpatterns = [
    path("", views.BlogPageLatestView.as_view(), name="blogpage-latest"),
    path("archive/", views.BlogPageListView.as_view(), name="blogpage-list"),
    path("feed/", rss.LatestBlogPostsFeed(), name="blog-rss-feed"),
    path("<slug:slug>/", views.BlogPageDetailView.as_view(), name="blogpage-detail"),
]
