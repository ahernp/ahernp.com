from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.EntryListView.as_view(), name="recent-entries"),
    path(
        "feed/<int:feed_id>/",
        view=views.FeedEntryListView.as_view(),
        name="feed-recent-entries",
    ),
    path("markread/", view=views.MarkEntryReadView.as_view(), name="mark-entry-read"),
    path(
        "markallread/",
        view=views.MarkAllEntryReadView.as_view(),
        name="mark-all-entry-read",
    ),
    path("feed", view=views.FeedListView.as_view(), name="feeds"),
]
