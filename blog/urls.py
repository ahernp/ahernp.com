from django.urls import path

from . import views

urlpatterns = [
    path("", views.BlogPageListView.as_view(), name="blogpage-list"),
    path("<slug:slug>/", views.BlogPageDetailView.as_view(), name="blogpage-detail"),
]
