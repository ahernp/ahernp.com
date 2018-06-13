import collections
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from django.conf import settings

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
    }


class EntryListView(ListView):
    model = Entry
    feed = None

    def get_queryset(self):
        kw_filters = {}

        feed_id = self.kwargs.get("feed_id", None)

        if feed_id is not None:
            self.feed = get_object_or_404(Feed, id=feed_id)
            kw_filters["feed__exact"] = self.feed

        kw_filters["read_flag__exact"] = False
        entries = Entry.objects.filter(**kw_filters).order_by("-published_time")[:settings.MAX_ENTRIES_SHOWN]

        if entries:
            return entries

        del kw_filters["read_flag__exact"]
        from_time = datetime.utcnow() - timedelta(days=settings.MAX_DAYS_SHOWN)
        kw_filters["published_time__gt"] = from_time

        return Entry.objects.filter(**kw_filters).order_by("-published_time")[:settings.MAX_ENTRIES_SHOWN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed"] = self.feed
        context["counts"] = count_entries(self.queryset) if self.queryset is not None else []
        return context
