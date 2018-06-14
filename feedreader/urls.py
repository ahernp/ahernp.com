from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.EntryListView.as_view(), name="recent-entries"),
    path(
        "feed/<int:feed_id>/",
        view=views.FeedEntryListView.as_view(),
        name="feed-recent-entries",
    ),
]