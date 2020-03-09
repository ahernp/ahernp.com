import collections

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView

from django.conf import settings

from .forms import ToggleEntryReadForm
from .models import Entry, Feed, Group


class FeedCount(object):
    def __init__(self, feed):
        self.feed = feed
        self.total_count = 0


class GroupCount(object):
    def __init__(self, group):
        self.group = group
        self.feed_counts = []
        self.total_count = 0


def count_entries(entries):
    groups = Group.objects.all()
    feeds = Feed.objects.all()

    group_counts = collections.OrderedDict(
        [(group.id, GroupCount(group=group)) for group in groups]
    )
    feed_counts = collections.OrderedDict(
        [(feed.id, FeedCount(feed=feed)) for feed in feeds]
    )

    for entry in entries:
        feed_counts[entry.feed_id].total_count += 1
        if entry.feed.group_id is not None:
            group_counts[entry.feed.group_id].total_count += 1

    total_entries = len(entries)
    non_group_feed_counts = []

    for feed_count in feed_counts.values():
        if feed_count.feed.group_id is not None:
            group_counts[feed_count.feed.group_id].feed_counts.append(feed_count)
        else:
            non_group_feed_counts.append(feed_count)

    return {
        "group_counts": list(group_counts.values()),
        "non_group_feed_counts": non_group_feed_counts,
        "total_entries": total_entries,
        "unread_entries": len([entry for entry in entries if entry.read_flag is False]),
    }


class EntryListView(ListView):
    model = Entry

    def get_queryset(self):
        if "read_flag" in self.request.GET:
            params = {"read_flag": self.request.GET["read_flag"] == "True"}
            entries = Entry.objects.filter(**params).order_by("-published_time")[
                : settings.MAX_ENTRIES_SHOWN
            ]
            if len(entries):
                return entries

        return Entry.objects.all().order_by("-published_time")[
            : settings.MAX_ENTRIES_SHOWN
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counts"] = count_entries(context["object_list"])
        return context


class FeedEntryListView(EntryListView):
    feed = None

    def get_queryset(self):
        feed_id = self.kwargs.get("feed_id")
        self.feed = get_object_or_404(Feed, id=feed_id)
        params = {"feed": self.feed}
        if "read_flag" in self.request.GET:
            params["read_flag"] = self.request.GET["read_flag"] == "True"
        return Entry.objects.filter(**params).order_by("-published_time")[
            : settings.MAX_ENTRIES_SHOWN
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed"] = self.feed
        return context


class MarkEntryReadView(LoginRequiredMixin, View):
    form_class = ToggleEntryReadForm
    login_url = "/admin/login/"
    redirect_field_name = "redirect_to"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            feed_id = form.cleaned_data.get("feed_id", None)
            entry_id = form.cleaned_data.get("entry_id", None)
            entry = get_object_or_404(Entry, id=entry_id)
            entry.read_flag = True
            entry.save()
        else:
            feed_id = None

        if feed_id is None:
            return redirect("recent-entries")
        else:
            return redirect("feed-recent-entries", feed_id=feed_id)


class MarkAllEntryReadView(LoginRequiredMixin, View):
    login_url = "/admin/login/"
    redirect_field_name = "redirect_to"

    def post(self, request, *args, **kwargs):
        Entry.objects.filter(read_flag=False).update(read_flag=True)
        return redirect("recent-entries")


class FeedListView(ListView):
    model = Feed
