from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.EntryListView.as_view(), name="recent-entries"),
    path(
        "feed/<slug:feed_id>/",
        view=views.EntryListView.as_view(),
        name="recent-entries-filter",
    ),
]
